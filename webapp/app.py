"""
Web front-end for the XML Integration Validator.

This is a standalone add-on: it imports and calls the existing,
untouched comparison pipeline (src/run_comparison.py) the same way
desktop_app.py does. No existing project file is modified.

Run locally:
    pip install flask
    python webapp/app.py
    -> open http://127.0.0.1:5000

Concurrency note: the underlying report generators (master_report_
generator.py, store_report_exporter.py, pdf_generator.py) always
write to a handful of FIXED file paths, not a per-run path. To keep
concurrent users from clobbering each other's output, every request
runs inside a single global lock, and the resulting files are copied
into a private per-run folder before the lock is released.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import sys
import threading
import time
import uuid
from pathlib import Path

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)

# The pipeline's "generated on" timestamps use datetime.now()/pd.Timestamp.now()
# with no explicit timezone, which follows the host machine's system clock.
# That's fine on someone's own (IST) desktop, but a cloud host like Render
# defaults to UTC. Force IST here at the process level so those unmodified
# call sites report the right time without editing report_parser.py /
# pdf_generator.py / store_report_exporter.py. time.tzset() is POSIX-only
# (no-op guard keeps this harmless on local Windows development).
os.environ["TZ"] = "Asia/Kolkata"
if hasattr(time, "tzset"):
    time.tzset()

# ---------------------------------------------------------------------------
# Make the existing src/ package importable, exactly like desktop_app.py does.
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_PATH = PROJECT_ROOT / "src"

for path in (str(PROJECT_ROOT), str(SRC_PATH)):
    if path not in sys.path:
        sys.path.insert(0, path)

import run_comparison as run_comparison_module  # noqa: E402
from run_comparison import run_comparison  # noqa: E402

# The pipeline calls webbrowser.open(...) unconditionally at the end
# (fine on someone's desktop, fatal on a headless server with no
# browser). We don't touch run_comparison.py; we just neutralise the
# call at runtime from here.
run_comparison_module.webbrowser.open = lambda *a, **kw: True

INTEGRATIONS = [
    "Payroll",
    "Timekeeping",
    "Food Out",
    "Vendor Schedule",
    "Labor Forecast",
    "Schedule Out",
    "PMIX Out",
    "ERS DPKeys",
]

FOOD_OUT_CLIENTS = {
    "BWW": "bww",
    "Arby's": "arbys",
    "Little Caesars": "lc",
}

RUNS_DIR = Path(__file__).resolve().parent / "runs"
RUNS_DIR.mkdir(parents=True, exist_ok=True)

RUN_MAX_AGE_SECONDS = 24 * 60 * 60  # prune anything older than this

run_lock = threading.Lock()

app = Flask(__name__)
app.secret_key = "xml-integration-validator-webapp"  # only used for flash()
app.config["MAX_CONTENT_LENGTH"] = 200 * 1024 * 1024  # 200 MB per request


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _safe_name(filename: str, fallback: str) -> str:
    name = os.path.basename(filename or "").strip()
    name = re.sub(r"[^A-Za-z0-9._ ()\-]", "_", name)
    return name or fallback


def _save_uploads(files, dest_dir: Path) -> int:
    dest_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    used_names: set = set()
    for i, f in enumerate(files):
        if not f or not f.filename:
            continue
        # Folder pickers (webkitdirectory) can include non-XML junk
        # (Thumbs.db, .DS_Store, ...) and nested subfolders in the
        # filename path - only keep actual .xml files, flattened.
        if not f.filename.lower().endswith(".xml"):
            continue
        name = _safe_name(os.path.basename(f.filename), f"file_{i}.xml")
        stem, suffix = os.path.splitext(name)
        n = 1
        while name in used_names:
            name = f"{stem}_{n}{suffix}"
            n += 1
        used_names.add(name)
        f.save(dest_dir / name)
        count += 1
    return count


def _prune_old_runs() -> None:
    cutoff = time.time() - RUN_MAX_AGE_SECONDS
    for entry in RUNS_DIR.iterdir():
        try:
            if entry.is_dir() and entry.stat().st_mtime < cutoff:
                shutil.rmtree(entry, ignore_errors=True)
        except OSError:
            pass


def _copy_into(src_path: str, output_dir: Path, used_names: set) -> str:
    """Copy an existing report file into this run's output folder,
    returning the name it was stored under (de-duplicated)."""

    src = Path(src_path)
    if not src.exists():
        return ""

    name = src.name
    stem, suffix = src.stem, src.suffix
    n = 1
    while name in used_names:
        name = f"{stem}_{n}{suffix}"
        n += 1

    shutil.copy2(src, output_dir / name)
    used_names.add(name)
    return name


def _rewrite_dashboard_links(html: str, run_id: str, output_dir: Path, used_names: set) -> str:
    """Copy every per-store excel/pdf referenced in the embedded
    dashboardDetails JSON into this run's output folder, and rewrite
    the JSON so the dashboard's "View Report" / "View PDF" buttons
    point at our own /download route instead of a local file path."""

    match = re.search(r"const dashboardDetails = (\{.*?\});", html, re.DOTALL)
    if not match:
        return html

    try:
        details = json.loads(match.group(1))
    except ValueError:
        return html

    for entry in details.values():
        if not isinstance(entry, dict):
            continue
        for key in ("report_file", "pdf_file"):
            value = entry.get(key)
            if not value:
                continue
            stored_name = _copy_into(value, output_dir, used_names)
            entry[key] = (
                url_for("download", run_id=run_id, filename=stored_name)
                if stored_name
                else ""
            )

    new_json = json.dumps(details)
    return html[: match.start(1)] + new_json + html[match.end(1):]


def _inject_master_download_banner(html: str, master_url: str) -> str:
    banner = (
        '<div style="position:sticky;top:0;z-index:9999;background:#111827;'
        'color:#fff;padding:8px 16px;font:600 12px/1.4 Segoe UI,Arial,sans-serif;'
        'display:flex;justify-content:space-between;align-items:center;">'
        '<span>XML Integration Validator &mdash; web preview</span>'
        f'<a href="{master_url}" style="color:#8ab4ff;text-decoration:none;'
        'border:1px solid #8ab4ff;border-radius:6px;padding:4px 10px;">'
        "Download Master Excel Report</a></div>"
    )
    if "<body>" in html:
        return html.replace("<body>", "<body>" + banner, 1)
    return banner + html


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/", methods=["GET"])
def index():
    return render_template(
        "upload.html",
        integrations=INTEGRATIONS,
        clients=list(FOOD_OUT_CLIENTS.keys()),
    )


@app.route("/run", methods=["POST"])
def run():
    integration = (request.form.get("integration") or "Payroll").lower()
    client_label = request.form.get("client") or "BWW"
    client = FOOD_OUT_CLIENTS.get(client_label, "bww")
    mode = request.form.get("mode") or "folder"

    run_id = uuid.uuid4().hex[:12]
    run_dir = RUNS_DIR / run_id
    upload_dir = run_dir / "upload"
    output_dir = run_dir / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        if mode == "file":
            cb_files = request.files.getlist("cb_file")
            ac_files = request.files.getlist("ac_file")
            if not cb_files or not cb_files[0].filename:
                flash("Please choose a CB XML file.")
                return redirect(url_for("index"))
            if not ac_files or not ac_files[0].filename:
                flash("Please choose an AC XML file.")
                return redirect(url_for("index"))

            cb_dir = upload_dir / "cb"
            ac_dir = upload_dir / "ac"
            _save_uploads(cb_files[:1], cb_dir)
            _save_uploads(ac_files[:1], ac_dir)
            cb_file_path = str(next(cb_dir.iterdir()))
            ac_file_path = str(next(ac_dir.iterdir()))

            run_kwargs = dict(
                integration=integration,
                cb_file=cb_file_path,
                ac_file=ac_file_path,
                client=client,
            )
        else:
            cb_files = request.files.getlist("cb_files")
            ac_files = request.files.getlist("ac_files")

            cb_dir = upload_dir / "cb"
            ac_dir = upload_dir / "ac"
            cb_count = _save_uploads(cb_files, cb_dir)
            ac_count = _save_uploads(ac_files, ac_dir)

            if cb_count == 0:
                flash("Please choose at least one CB XML file.")
                return redirect(url_for("index"))
            if ac_count == 0:
                flash("Please choose at least one AC XML file.")
                return redirect(url_for("index"))

            run_kwargs = dict(
                cb_folder=str(cb_dir),
                ac_folder=str(ac_dir),
                integration=integration,
                client=client,
            )

        with run_lock:
            try:
                result = run_comparison(**run_kwargs)
            except Exception as exc:  # noqa: BLE001
                flash(f"Comparison failed: {exc}")
                shutil.rmtree(run_dir, ignore_errors=True)
                return redirect(url_for("index"))

            used_names: set = set()

            master_name = _copy_into(result["report_path"], output_dir, used_names)
            master_url = (
                url_for("download", run_id=run_id, filename=master_name)
                if master_name
                else "#"
            )

            dashboard_html = Path(result["dashboard_path"]).read_text(encoding="utf-8")
            dashboard_html = _rewrite_dashboard_links(
                dashboard_html, run_id, output_dir, used_names
            )
            dashboard_html = _inject_master_download_banner(dashboard_html, master_url)

            (output_dir / "dashboard.html").write_text(dashboard_html, encoding="utf-8")

        _prune_old_runs()

        return redirect(url_for("view", run_id=run_id))

    finally:
        shutil.rmtree(upload_dir, ignore_errors=True)


@app.route("/view/<run_id>", methods=["GET"])
def view(run_id):
    safe_id = re.sub(r"[^a-f0-9]", "", run_id)
    html_path = RUNS_DIR / safe_id / "output" / "dashboard.html"
    if not html_path.exists():
        flash("This report has expired or does not exist. Please run a new comparison.")
        return redirect(url_for("index"))
    return html_path.read_text(encoding="utf-8")


@app.route("/download/<run_id>/<path:filename>", methods=["GET"])
def download(run_id, filename):
    safe_id = re.sub(r"[^a-f0-9]", "", run_id)
    output_dir = (RUNS_DIR / safe_id / "output").resolve()
    target = (output_dir / filename).resolve()

    if output_dir not in target.parents and target != output_dir:
        return "Not found", 404
    if not target.exists():
        return "Not found", 404

    return send_file(target, as_attachment=True, download_name=target.name)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
