import streamlit as st
import subprocess
import os
import pandas as pd

st.set_page_config(page_title="CB to AC Payroll Validation Dashboard", layout="wide")

st.title("CB to AC Payroll Validation Dashboard")

st.caption("Validate and compare payroll exports between CB and AC environments.")

left, center, right = st.columns([2, 2, 2])

with center:

    run_clicked = st.button("Run Payroll Validation", use_container_width=True)

if run_clicked:

    with st.spinner("Running payroll validation..."):

        result = subprocess.run(
            ["py", "src/run_all.py"], capture_output=True, text=True
        )

    st.session_state["validation_complete"] = True

    st.session_state["stdout"] = result.stdout

    st.session_state["stderr"] = result.stderr


if st.session_state.get("validation_complete", False):

    report_path = "reports/" "Master_Comparison_Report.xlsx"

    if os.path.exists(report_path):

        try:

            summary = pd.read_excel(report_path, sheet_name="MASTER_SUMMARY")

            total_files = len(summary)

            pass_count = len(summary[summary["Status"] == "PASS"])

            fail_count = len(summary[summary["Status"] == "FAIL"])

            missing_count = len(
                summary[summary["Status"].astype(str).str.contains("MISSING", na=False)]
            )

            st.success(
                f"Payroll validation completed successfully. "
                f"{total_files} files processed."
            )

            metric1, metric2, metric3, metric4 = st.columns(4)

            metric1.metric("Total Files", total_files)

            metric2.metric("Passed", pass_count)

            metric3.metric("Failed", fail_count)

            metric4.metric("Missing", missing_count)

            st.markdown("---")

            filter1, filter2 = st.columns(2)

            with filter1:

                store_filter = st.selectbox(
                    "Store",
                    ["All"] + sorted(summary["Store"].astype(str).unique().tolist()),
                )

            with filter2:

                status_filter = st.selectbox(
                    "Status",
                    ["All"] + sorted(summary["Status"].astype(str).unique().tolist()),
                )

            filtered_summary = summary.copy()

            if store_filter != "All":

                filtered_summary = filtered_summary[
                    filtered_summary["Store"].astype(str) == store_filter
                ]

            if status_filter != "All":

                filtered_summary = filtered_summary[
                    filtered_summary["Status"].astype(str) == status_filter
                ]

            st.subheader("Validation Summary")

            st.dataframe(filtered_summary, width="stretch", hide_index=True)

            st.markdown("---")

            st.subheader("Validation Report")

            with open(report_path, "rb") as file:

                st.download_button(
                    label=("Download Validation Report"),
                    data=file,
                    file_name=("Master_Comparison_Report.xlsx"),
                    mime=(
                        "application/"
                        "vnd.openxmlformats-"
                        "officedocument."
                        "spreadsheetml.sheet"
                    ),
                    use_container_width=True,
                )

        except Exception as e:

            st.error(f"Unable to read report: {e}")

    else:

        st.error("Validation report was not generated.")

    if st.session_state.get("stderr"):

        st.error(st.session_state["stderr"])
