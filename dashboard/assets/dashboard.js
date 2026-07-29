/*
==========================================================
Any Connector XML Validator Dashboard
Version : 3.0
==========================================================
*/

document.addEventListener("DOMContentLoaded", () => {

    initializeDashboard();

});

/* ======================================================
   Dashboard Initialization
====================================================== */

function initializeDashboard() {

    initializeSearch();

    initializeStatusFilter();

    initializeRefreshButton();

    initializeViewButtons();

}

/* ======================================================
   Search
====================================================== */

function initializeSearch() {

    const searchBox = document.getElementById("storeSearch");

    if (!searchBox) return;

    searchBox.addEventListener("keyup", filterTable);

}

/* ======================================================
   Status Filter
====================================================== */

function initializeStatusFilter() {

    const filter = document.getElementById("statusFilter");

    if (!filter) return;

    filter.addEventListener("change", filterTable);

}

/* ======================================================
   Common Table Filter
====================================================== */

function filterTable() {

    const searchValue =
        document
            .getElementById("storeSearch")
            .value
            .toUpperCase();

    const statusValue =
        document
            .getElementById("statusFilter")
            .value;

    const rows =
        document.querySelectorAll(
            "#storeTable tbody tr"
        );

    rows.forEach((row) => {

        const store =
            row.cells[0]
                .innerText
                .toUpperCase();

        const status =
            row.cells[1]
                .innerText
                .trim()
                .toUpperCase();

        const matchSearch =
            store.includes(searchValue);

        const matchStatus =
            statusValue === "ALL"
            || status === statusValue;

        row.style.display =
            (matchSearch && matchStatus)
                ? ""
                : "none";

    });

}

/* ======================================================
   Refresh Button
====================================================== */

function initializeRefreshButton() {

    const button =
        document.querySelector(".btn-primary");

    if (!button) return;

    button.addEventListener("click", () => {

        location.reload();

    });

}

/* ======================================================
   View Buttons
====================================================== */

function initializeViewButtons() {

    const buttons =
        document.querySelectorAll(
            ".view-details"
        );

    buttons.forEach((button) => {

        button.addEventListener("click", () => {

            const store =
                button.dataset.store;

            showStoreDetails(store);

        });

    });

}

/* ======================================================
   Dynamic Table Generator
====================================================== */

function generateDynamicTable(title, records) {

    if (!records || records.length === 0) {
        return "";
    }

    const headers = Object.keys(records[0]);

    let html = `

        <h5 class="mt-4">${title}</h5>

        <div class="table-responsive">

            <table class="table table-bordered table-sm dynamic-table">

                <thead>

                    <tr>

    `;

    headers.forEach(header => {

        // Store column modal me already visible hai
        if (header === "Store") return;

        html += `<th>${header}</th>`;

    });

    html += `

                    </tr>

                </thead>

                <tbody>

    `;

    records.forEach(record => {

        html += "<tr>";

        headers.forEach(header => {

            if (header === "Store") return;

            let value = record[header];

            if (
                value === undefined ||
                value === null ||
                value === ""
            ) {

                value = "-";

            }

            if (typeof value === "object") {

                value = formatAttributes(value);

            }

            html += `<td>${value}</td>`;

        });

        html += "</tr>";

    });

    html += `

                </tbody>

            </table>

        </div>

    `;

    return html;

}
/* ======================================================
   Store Details
====================================================== */

function showStoreDetails(store) {

    const details = dashboardDetails[store];

    if (!details) {
        return;
    }

    const downloadButton = document.getElementById("downloadStoreReport");

    if (downloadButton) {

        downloadButton.onclick = () => {

            if (!details.report_file) {

                alert("Store report not found.");

                return;

            }

            window.open(details.report_file, "_blank");

        };

    }

    const validationFailure =
        details.validation_failure || false;

    const failureReason =
        details.failure_reason || "";

    if (!details) {

        return;

    }

    document.getElementById("modalStore").textContent = "Store Details";

    let html = "";
    /* ==========================================
   Store Information Card
========================================== */

const infoCard = `

<div class="card border-primary mb-4">

    <div class="card-header bg-primary text-white fw-bold">

        Store Information

    </div>

    <div class="card-body">

        <div class="row">

            <div class="col-md-6">

                <table class="table table-borderless table-sm mb-0">

                    <tr>

                        <th width="140">Store No</th>

                        <td>${details.store || "-"}</td>

                    </tr>

                    <tr>

                        <th>Business Date</th>

                        <td>${details.cb_date || details.ac_date || "-"}</td>

                    </tr>

                </table>

            </div>

            <div class="col-md-6">

                <table class="table table-borderless table-sm mb-0">

                    <tr>

                        <th width="120">CB File</th>

                        <td title="${details.cb_file || "-"}">

                            ${details.cb_file || "-"}

                        </td>

                    </tr>

                    <tr>

                        <th>AC File</th>

                        <td title="${details.ac_file || "-"}">

                            ${details.ac_file || "-"}

                        </td>

                    </tr>

                </table>

            </div>

        </div>

    </div>

</div>

`;
    /* ==========================================
   Validation Failure
========================================== */

if (validationFailure) {

    html = infoCard + `

        <div class="alert alert-danger">

            <h4 class="mb-3">

                Validation Failed

            </h4>

            <p>

                <strong>Reason :</strong>

                ${failureReason}

            </p>

            <hr>

            <table class="table table-bordered">

                <tr>

                    <th width="180">

                        CB File

                    </th>

                    <td>

                        ${details.cb_file || "-"}

                    </td>

                </tr>

                <tr>

                    <th>

                        AC File

                    </th>

                    <td>

                        ${details.ac_file || "-"}

                    </td>

                </tr>

                <tr>

                    <th>

                        CB Date

                    </th>

                    <td>

                        ${details.cb_date || "-"}

                    </td>

                </tr>

                <tr>

                    <th>

                        AC Date

                    </th>

                    <td>

                        ${details.ac_date || "-"}

                    </td>

                </tr>

            </table>

        </div>

    `;

    document.getElementById("modalContent").innerHTML = html;

    const modal = new bootstrap.Modal(
        document.getElementById(
            "storeDetailsModal"
        )
    );

    modal.show();

    return;

}

    const differences =
        details.differences || [];
        html += infoCard;

    const missing =
        details.missing || [];

    const duplicates =
        details.duplicates || [];

    const zeroValues =
        details.zero_values || [];

    /* ==========================================
       Summary Card
    ========================================== */

    html += `

        <div class="row mb-3">

            <div class="col-md-3">

                <div class="card border-0 bg-light">

                    <div class="card-body text-center">

                        <h6 class="mb-1">Differences</h6>

                        <h4 class="mb-0 text-danger">

                            ${differences.length}

                        </h4>

                    </div>

                </div>

            </div>

            <div class="col-md-3">

                <div class="card border-0 bg-light">

                    <div class="card-body text-center">

                        <h6 class="mb-1">Missing</h6>

                        <h4 class="mb-0 text-warning">

                            ${missing.length}

                        </h4>

                    </div>

                </div>

            </div>

            <div class="col-md-3">

                <div class="card border-0 bg-light">

                    <div class="card-body text-center">

                        <h6 class="mb-1">Duplicates</h6>

                        <h4 class="mb-0 text-primary">

                            ${duplicates.length}

                        </h4>

                    </div>

                </div>

            </div>

            <div class="col-md-3">

                <div class="card border-0 bg-light">

                    <div class="card-body text-center">

                        <h6 class="mb-1">Zero Values</h6>

                        <h4 class="mb-0 text-info">

                            ${zeroValues.length}

                        </h4>

                    </div>

                </div>

            </div>

        </div>

    `;

    /* ==========================================
       Dynamic Tables
    ========================================== */

    html += generateDynamicTable(

        "Differences",

        differences

    );

    html += generateDynamicTable(

        "Missing Records",

        missing

    );

    html += generateDynamicTable(

        "Duplicate Records",

        duplicates

    );

    html += generateDynamicTable(

        "Zero Value Records",

        zeroValues

    );

    /* ==========================================
       No Issues
    ========================================== */

if (

    differences.length === 0 &&

    missing.length === 0 &&

    duplicates.length === 0 &&

    zeroValues.length === 0

) {

    html = infoCard + `

        <div class="alert alert-success mb-0">

            <strong>

                ✓ No validation issues found for this store.

            </strong>

        </div>

    `;

}

    document.getElementById(

        "modalContent"

    ).innerHTML = html;

    const modal = new bootstrap.Modal(

        document.getElementById(

            "storeDetailsModal"

        )

    );

    modal.show();

}
/* ======================================================
   Utility Functions
====================================================== */

function formatAttributes(attributes) {

    if (
        attributes === null ||
        attributes === undefined ||
        attributes === "" ||
        attributes === "-"
    ) {

        return "-";

    }

    /* ------------------------------------------
       Already Object
    ------------------------------------------ */

    if (typeof attributes === "object") {

        let html = "";

        Object.entries(attributes).forEach(([key, value]) => {

            html += `
                <div class="mb-1">
                    <strong>${key}</strong> :
                    ${value}
                </div>
            `;

        });

        return html;

    }

    /* ------------------------------------------
       Python Dictionary String
    ------------------------------------------ */

    if (typeof attributes === "string") {

        let text = attributes.trim();

        if (
            text.startsWith("{") &&
            text.endsWith("}")
        ) {

            text = text.substring(
                1,
                text.length - 1
            );

            let html = "";

            text.split(",").forEach(pair => {

                const parts = pair.split(":");

                if (parts.length < 2) return;

                const key =
                    parts[0]
                        .replace(/'/g, "")
                        .trim();

                const value =
                    parts
                        .slice(1)
                        .join(":")
                        .replace(/'/g, "")
                        .trim();

                html += `
                    <div class="mb-1">
                        <strong>${key}</strong> :
                        ${value}
                    </div>
                `;

            });

            return html;

        }

    }

    return attributes;

}

/* ======================================================
   Visible Store Count
====================================================== */

function getVisibleRowCount() {

    const rows = document.querySelectorAll(
        "#storeTable tbody tr"
    );

    let count = 0;

    rows.forEach(row => {

        if (
            row.style.display !== "none"
        ) {

            count++;

        }

    });

    return count;

}

/* ======================================================
   Dashboard Ready
====================================================== */

console.log(
    "====================================="
);

console.log(
    "Any Connector XML Validator Loaded"
);

console.log(
    "Visible Stores :",
    getVisibleRowCount()
);

console.log(
    "====================================="
);

/* ======================================================
   Future Features
====================================================== */

/*

Roadmap

✔ Download Failed Report

✔ Export PDF

✔ Export Excel

✔ Charts

✔ Sorting

✔ Pagination

✔ Theme Toggle

✔ Auto Refresh

*/