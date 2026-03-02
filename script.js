// script.js
window.addEventListener("DOMContentLoaded", () => {

    // Use local backend instead of Vercel
    // script.js
const API_BASE = ""; // empty = same domain

    async function fetchData(url) {
        try {
            const res = await fetch(`${API_BASE}${url}`);
            if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
            return await res.json();
        } catch (err) {
            console.error("Fetch error:", err);
            return null; // return null so we can check in loadDashboard
        }
    }

    async function loadDashboard() {
        const workers = await fetchData("/metrics/workers");
        const stations = await fetchData("/metrics/stations");
        const factory = await fetchData("/metrics/factory");

        // Workers Table
        const workersBody = document.querySelector("#workers-table tbody");
        if (workers) {
            workersBody.innerHTML = "";
            workers.forEach(w => {
                workersBody.innerHTML += `
                    <tr>
                        <td>${w.worker_id}</td>
                        <td>${w.worker_name}</td>
                        <td>${w.working_events}</td>
                        <td>${w.idle_events}</td>
                        <td>${w.utilization}</td>
                        <td>${w.total_units}</td>
                    </tr>`;
            });
        } else {
            workersBody.innerHTML = "<tr><td colspan='6'>Failed to load worker data</td></tr>";
        }

        // Stations Table
        const stationsBody = document.querySelector("#stations-table tbody");
        if (stations) {
            stationsBody.innerHTML = "";
            stations.forEach(s => {
                stationsBody.innerHTML += `
                    <tr>
                        <td>${s.station_id}</td>
                        <td>${s.station_name}</td>
                        <td>${s.working_events}</td>
                        <td>${s.idle_events}</td>
                        <td>${s.utilization}</td>
                        <td>${s.total_units}</td>
                    </tr>`;
            });
        } else {
            stationsBody.innerHTML = "<tr><td colspan='6'>Failed to load station data</td></tr>";
        }

        // Factory Table
        const factoryBody = document.querySelector("#factory-table tbody");
        if (factory && Object.keys(factory).length) {
            factoryBody.innerHTML = `
                <tr>
                    <td>${factory.total_working_events}</td>
                    <td>${factory.total_idle_events}</td>
                    <td>${factory.utilization}</td>
                    <td>${factory.total_units}</td>
                </tr>`;
        } else {
            factoryBody.innerHTML = "<tr><td colspan='4'>Failed to load factory data</td></tr>";
        }
    }

    // Load dashboard immediately and then every 5 seconds
    loadDashboard();
    setInterval(loadDashboard, 5000);

});