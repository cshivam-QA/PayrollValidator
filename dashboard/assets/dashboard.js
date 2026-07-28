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

    if (details.differences.length > 0) {

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

        details.differences.forEach(item => {

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

    } else {

        html = "<p>No differences found.</p>";

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