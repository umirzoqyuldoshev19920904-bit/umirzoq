<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ultra ERP - Professional Boshqaruv</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script defer src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        [x-cloak] { display: none !important; }
        .glass { background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(10px); }
    </style>
</head>
<body class="bg-slate-100 text-slate-800" x-data="erpSystem()">

    <div class="min-h-screen flex flex-col md:flex-row">
        <!-- Sidebar -->
        <aside class="w-full md:w-64 bg-slate-900 text-white p-6 flex flex-col hidden md:flex">
            <h2 class="text-2xl font-bold mb-8 text-blue-400"><i class="fas fa-warehouse mr-2"></i>Ultra ERP</h2>
            <nav class="space-y-4">
                <template x-for="link in ['Dashboard', 'Mahsulotlar', 'Agentlar', 'Moliya']">
                    <button @click="activeTab = link" :class="activeTab === link ? 'text-blue-400' : 'text-slate-400'" class="block text-left hover:text-white transition">
                        <i :class="link === 'Dashboard' ? 'fa-chart-line' : (link === 'Mahsulotlar' ? 'fa-boxes' : 'fa-users')" class="fas mr-3"></i>
                        <span x-text="link"></span>
                    </button>
                </template>
            </nav>
        </aside>

        <!-- Main Content -->
        <main class="flex-1 p-4 md:p-8 overflow-y-auto">
            <!-- Header -->
            <header class="flex justify-between items-center mb-8">
                <h1 class="text-2xl font-bold" x-text="activeTab"></h1>
                <div class="bg-white px-4 py-2 rounded-lg shadow-sm font-semibold">Admin: Karim</div>
            </header>

            <div x-show="activeTab === 'Dashboard'" class="space-y-6">
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div class="bg-white p-6 rounded-xl shadow-lg border-l-4 border-blue-500">
                        <p class="text-sm text-slate-500">Bugungi Foyda</p>
                        <h3 class="text-2xl font-bold" x-text="stats.dailyProfit + ' UZS'"></h3>
                    </div>
                    <div class="bg-white p-6 rounded-xl shadow-lg border-l-4 border-green-500">
                        <p class="text-sm text-slate-500">Oylik Foyda</p>
                        <h3 class="text-2xl font-bold" x-text="stats.monthlyProfit + ' UZS'"></h3>
                    </div>
                    <div class="bg-white p-6 rounded-xl shadow-lg border-l-4 border-purple-500">
                        <p class="text-sm text-slate-500">Jami Yillik</p>
                        <h3 class="text-2xl font-bold" x-text="stats.yearlyProfit + ' UZS'"></h3>
                    </div>
                </div>
                
                <!-- Chart Area -->
                <div class="bg-white p-6 rounded-xl shadow-md h-64">
                    <canvas id="mainChart"></canvas>
                </div>
            </div>

            <div x-show="activeTab === 'Agentlar'" class="bg-white p-6 rounded-xl shadow-md">
                <table class="w-full text-left">
                    <thead><tr class="border-b"><th class="py-3">Agent</th><th class="py-3">Balance</th><th class="py-3">Status</th></tr></thead>
                    <tbody>
                        <template x-for="agent in agents">
                            <tr class="border-b">
                                <td class="py-3" x-text="agent.name"></td>
                                <td class="py-3" x-text="agent.balance + ' UZS'"></td>
                                <td class="py-3"><span :class="agent.balance > 0 ? 'text-green-500' : 'text-red-500'" x-text="agent.balance > 0 ? 'Foydali' : 'Qarzdor'"></span></td>
                            </tr>
                        </template>
                    </tbody>
                </table>
            </div>
        </main>
    </div>

    <script>
        function erpSystem() {
            return {
                activeTab: 'Dashboard',
                stats: { dailyProfit: '1,200,000', monthlyProfit: '45,000,000', yearlyProfit: '540,000,000' },
                agents: [
                    { name: 'Aliyev B.', balance: 500000 },
                    { name: 'Karimov S.', balance: -200000 }
                ],
                init() {
                    const ctx = document.getElementById('mainChart').getContext('2d');
                    new Chart(ctx, {
                        type: 'line',
                        data: {
                            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
                            datasets: [{ label: 'Savdo', data: [1200, 1900, 3000, 2500, 4000], borderColor: '#3b82f6', tension: 0.4 }]
                        },
                        options: { responsive: true, maintainAspectRatio: false }
                    });
                }
            }
        }
    </script>
</body>
</html>
