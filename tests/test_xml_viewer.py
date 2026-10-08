import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "webapp"))

from xml_viewer import render_xml  # noqa: E402


def _depths(html):
    return [int(d) for d in re.findall(r'style="--d:(\d+)"', html)]


def test_single_line_xml_is_split_into_indented_lines():
    html, parsed, lines = render_xml(
        b'<Poll a="1"><KEYS><KEY c="x" v="1"/><KEY c="y" v="2"><DK id="43" v="5"/></KEY></KEYS></Poll>'
    )

    assert parsed
    # Poll, KEYS, KEY x, KEY y (open), DK, KEY y (close), KEYS close, Poll close
    assert lines == 8
    assert _depths(html) == [0, 1, 2, 2, 3, 2, 1, 0]


def test_elements_with_children_are_collapsible():
    html, _, _ = render_xml(b"<Poll><KEYS><KEY c=\"x\"/></KEYS></Poll>")

    assert html.count('class="blk"') == 2  # Poll and KEYS, not the leaf KEY
    assert html.count('class="tog"') == 2


def test_file_content_is_escaped_never_rendered_as_markup():
    html, parsed, _ = render_xml(
        b'<Poll note="&lt;script&gt;alert(1)&lt;/script&gt; &quot;x&quot;">'
        b"<html:script xmlns:html=\"http://www.w3.org/1999/xhtml\">alert(2)</html:script>"
        b"<!-- <img src=x onerror=alert(3)> --></Poll>"
    )

    assert parsed
    assert "<script" not in html
    assert "<img" not in html
    assert "&lt;script&gt;alert(1)" in html


def test_malformed_xml_falls_back_to_escaped_plain_text():
    html, parsed, lines = render_xml(b"<Poll><KEY c='x'>\n<b>not closed</Poll>")

    assert not parsed
    assert lines == 2
    assert "<b>" not in html
    assert "&lt;b&gt;not closed" in html
