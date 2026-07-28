/*
==========================================================
XML Validator Dashboard
Version : 2.0
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

        if (matchSearch && matchStatus) {

            row.style.display = "";

        } else {

            row.style.display = "none";

        }

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
   View Details
====================================================== */

function initializeViewButtons() {

    const buttons = document.querySelectorAll(".view-details");

    buttons.forEach((button) => {

        button.addEventListener("click", () => {

            const store =
                button.dataset.store;

            showStoreDetails(store);

        });

    });

}

/* ======================================================
   Store Details
====================================================== */

function showStoreDetails(store) {

    const details = dashboardDetails[store];

    document.getElementById("modalStore").textContent = store;

    let html = "";
    const differences = details.differences || [];
    const missing = details.missing || [];
    const duplicates = details.duplicates || [];
    const zeroValues = details.zero_values || [];

    if (differences.length > 0) {

        html += "<h5>Differences</h5>";

        html += `
        <table class="table table-bordered table-sm">

            <thead>

                <tr>

                    <th>Node</th>

                    <th>Key</th>

                    <th>Attribute</th>

                    <th>CB Value</th>

                    <th>AC Value</th>

                </tr>

            </thead>

            <tbody>
        `;

        differences.forEach(item => {

            html += `
            <tr>

                <td>${item.Node}</td>

                <td>${item.Key}</td>

                <td>${item.Attribute}</td>

                <td>${item["CB Value"]}</td>

                <td>${item["AC Value"]}</td>

            </tr>
            `;

        });

        html += "</tbody></table>";

    }

    /* ==========================================
       Missing Records
    ========================================== */

    if (missing.length > 0) {

        html += "<h5 class='mt-4'>Missing Records</h5>";

        html += `
        <table class="table table-bordered table-sm">

            <thead>

                <tr>

                    <th>Key</th>

                    <th>Date</th>

                    <th>Missing In</th>

                    <th>CB Attributes</th>

                    <th>AC Attributes</th>

                </tr>

            </thead>

            <tbody>
        `;

        missing.forEach(item => {

            html += `
            <tr>

                <td>${item.Key}</td>

                <td>${item.Date}</td>

                <td>${item["Missing In"]}</td>

                <td>${formatAttributes(item["CB Attributes"])}</td>

                <td>${formatAttributes(item["AC Attributes"])}</td>

            </tr>
            `;

        });

        html += "</tbody></table>";

    }

    /* ==========================================
       No Validation Issues
    ========================================== */

    if (
        differences.length === 0 &&
        missing.length === 0
    ) {

        html = "<p>No validation issues found.</p>";

    }

    document.getElementById("modalContent").innerHTML = html;

    const modal = new bootstrap.Modal(
        document.getElementById("storeDetailsModal")
    );

    modal.show();

}

/* ======================================================
   Utility Functions
====================================================== */

function formatAttributes(attributes) {

    if (!attributes || attributes === "-") {
        return "-";
    }

    // Agar object already hai
    if (typeof attributes === "object") {

        let formatted = "";

        Object.entries(attributes).forEach(([key, value]) => {
            formatted += `<strong>${key}</strong> : ${value}<br>`;
        });

        return `<div class="mb-0" style="font-family: monospace; white-space: pre-line;">${formatted}</div>`;
    }

    // Agar Python dict string hai
    if (typeof attributes === "string") {

        let text = attributes.trim();

        // { } hatao
        text = text.replace(/^\{|\}$/g, "");

        // ',' ke basis par split
        const pairs = text.split(",");

        let formatted = "";

        pairs.forEach(pair => {

            const parts = pair.split(":");

            if (parts.length >= 2) {

                const key = parts[0].replace(/'/g, "").trim();

                const value = parts.slice(1).join(":").replace(/'/g, "").trim();

                formatted += `<strong>${key}</strong> : ${value}<br>`;

            }

        });

        return `
<div class="mb-0"
     style="font-family: monospace; white-space: pre-line; line-height:1.5;">
    ${formatted}
</div>`;
    }

    return attributes;
}

function getVisibleRowCount() {

    const rows =
        document.querySelectorAll(
            "#storeTable tbody tr"
        );

    let count = 0;

    rows.forEach((row) => {

        if (row.style.display !== "none") {

            count++;

        }

    });

    return count;

}

/* ======================================================
   Dashboard Ready
====================================================== */

console.log(
    "XML Validator Dashboard Loaded Successfully"
);

console.log(
    "Visible Stores :",
    getVisibleRowCount()
);

/* ======================================================
   Future Features
====================================================== */

/*

Planned Features

✔ Export Excel

✔ Export PDF

✔ Drill Down

✔ Theme Toggle

✔ Pagination

✔ Sorting

✔ Charts (Optional)

✔ Auto Refresh

*/