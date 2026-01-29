/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, onMounted, useState } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";
import { loadJS } from "@web/core/assets";

export class KprtsDashboard extends Component {
    static template = "kprts.Dashboard";

    setup() {
        this.state = useState({
            total: 0,
            open: 0,
            progress: 0,
            disposed: 0,
            disposed_within_60: 0,
            disposed_beyond_60: 0,

            gender_male: 0,
            gender_female: 0,
            gender_other: 0,
        });

        this._charts = {
            status: null,
            total: null,
            gender: null,
            disposal_time: null, // ✅ NEW
        };

        onMounted(async () => {
            const data = await rpc("/web/dataset/call_kw", {
                model: "kprts.complaint",
                method: "get_dashboard_stats",
                args: [[]],
                kwargs: {},
            });

            this.state.total = data.total || 0;
            this.state.open = data.open || 0;
            this.state.progress = data.progress || 0;
            this.state.disposed = data.disposed || 0;
            this.state.disposed_within_60 = data.disposed_within_60 || 0;
            this.state.disposed_beyond_60 = data.disposed_beyond_60 || 0;

            this.state.gender_male = data.gender_male || 0;
            this.state.gender_female = data.gender_female || 0;
            this.state.gender_other = data.gender_other || 0;

            await this._ensureChartJsLoaded();
            this._renderPieCharts();
        });
    }

    async _ensureChartJsLoaded() {
        if (window.Chart) return;

        const candidates = [
            "/web/static/lib/Chart/Chart.js",
            "/web/static/lib/chartjs/chart.js",
            "/web/static/lib/chartjs/Chart.js",
        ];

        for (const url of candidates) {
            try {
                await loadJS(url);
                if (window.Chart) return;
            } catch (e) {}
        }
    }

    _renderPieCharts() {
        if (!window.Chart) return;

        // destroy existing charts safely
        Object.values(this._charts).forEach(chart => {
            if (chart) chart.destroy();
        });

        this._charts.status = null;
        this._charts.total = null;
        this._charts.gender = null;
        this._charts.disposal_time = null;

        // -----------------------
        // Complaint Status Pie
        // -----------------------
        const statusCanvas = document.getElementById("kprts_status_pie");
        if (statusCanvas) {
            this._charts.status = new Chart(statusCanvas, {
                type: "pie",
                data: {
                    labels: ["Open", "In Progress", "Disposed"],
                    datasets: [{
                        data: [
                            this.state.open,
                            this.state.progress,
                            this.state.disposed,
                        ],
                        backgroundColor: ["#f39c12", "#f1c40f", "#2ecc71"],
                    }],
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { position: "bottom" } },
                },
            });
        }

        // -----------------------
        // Disposed vs Total Pie
        // -----------------------
        const totalCanvas = document.getElementById("kprts_total_pie");
        if (totalCanvas) {
            this._charts.total = new Chart(totalCanvas, {
                type: "pie",
                data: {
                    labels: ["Disposed", "Remaining"],
                    datasets: [{
                        data: [
                            this.state.disposed,
                            Math.max(this.state.total - this.state.disposed, 0),
                        ],
                        backgroundColor: ["#27ae60", "#e74c3c"],
                    }],
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { position: "bottom" } },
                },
            });
        }

        // -----------------------
        // Gender Pie
        // -----------------------
        const genderCanvas = document.getElementById("kprts_gender_pie");
        if (genderCanvas) {
            this._charts.gender = new Chart(genderCanvas, {
                type: "pie",
                data: {
                    labels: ["Male", "Female", "Other"],
                    datasets: [{
                        data: [
                            this.state.gender_male,
                            this.state.gender_female,
                            this.state.gender_other,
                        ],
                        backgroundColor: ["#3498db", "#e91e63", "#9b59b6"],
                    }],
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { position: "bottom" } },
                },
            });
        }

        // -----------------------
        // ✅ Disposed Time Pie (NEW)
        // -----------------------
        const disposalCanvas = document.getElementById("kprts_disposal_time_pie");
        if (disposalCanvas) {
            this._charts.disposal_time = new Chart(disposalCanvas, {
                type: "pie",
                data: {
                    labels: [
                        "Disposed within 60 Days",
                        "Disposed beyond 60 Days",
                    ],
                    datasets: [{
                        data: [
                            this.state.disposed_within_60,
                            this.state.disposed_beyond_60,
                        ],
                        backgroundColor: ["#2ecc71", "#c0392b"],
                    }],
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { position: "bottom" } },
                },
            });
        }
    }
}

registry.category("actions").add("kprts_dashboard", KprtsDashboard);
