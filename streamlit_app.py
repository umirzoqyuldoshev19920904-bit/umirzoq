<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UltraWarehouse Pro - Murakkab Ombor Boshqaruvi</title>
    <!-- Tailwind CSS, Alpine.js, Chart.js va FontAwesome ulash -->
    <script src="https://tailwindcss.com"></script>
    <script defer src="https://unpkg.com"></script>
    <script src="https://jsdelivr.net"></script>
    <link rel="stylesheet" href="https://cloudflare.com">
    
    <style>
        [x-cloak] { display: none !important; }
        .glass-nav { background: rgba(15, 23, 42, 0.9); backdrop-filter: blur(12px); }
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: #f1f1f1; }
        ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
    </style>
</head>
<body class="bg-slate-50 text-slate-900 font-sans antialiased" x-data="warehouseSystem()" x-init="initCharts()">

    <div class="min-h-screen flex flex-col md:flex-row">
        
        <!-- SIDEBAR: Chap menyu -->
        <aside class="w-full md:w-68 bg-slate-900 text-slate-300 p-6 flex flex-col justify-between border-r border-slate-800 shadow-xl">
            <div>
                <div class="flex items-center gap-3 mb-8 px-2">
                    <div class="bg-blue-600 p-2.5 rounded-xl text-white shadow-lg shadow-blue-500/30">
                        <i class="fas fa-boxes-stacked text-xl"></i>
                    </div>
                    <div>
                        <h2 class="text-lg font-bold text-white tracking-tight">UltraWarehouse</h2>
                        <span class="text-xs text-blue-400 font-medium">Professional v2.5</span>
                    </div>
                </div>

                <nav class="space-y-1.5">
                    <template x-for="menu in menus">
                        <button @click="activeTab = menu.id" 
                                :class="activeTab === menu.id ? 'bg-blue-600 text-white font-medium shadow-md shadow-blue-600/10' : 'hover:bg-slate-800/60 hover:text-slate-100'"
                                class="w-full flex items-center justify-between px-4 py-3 rounded-xl transition-all duration-200 group text-sm">
                            <div class="flex items-center gap-3">
                                <i :class="menu.icon" class="text-slate-400 group-hover:text-blue-400 transition-colors"></i>
                                <span x-text="menu.name"></span>
                            </div>
                            <!-- Dinamik bildirishnomalar hisoblagichi -->
                            <template x-if="menu.id === 'products' && lowStockCount() > 0">
                                <span class="bg-amber-500/20 text-amber-400 text-xs px-2 py-0.5 rounded-full font-bold" x-text="lowStockCount()"></span>
                            </template>
                        </button>
                    </template>
                </nav>
            </div>

            <div class="pt-6 border-t border-slate-800 mt-6 flex items-center gap-3 px-2">
                <div class="w-9 h-9 rounded-full bg-slate-700 flex items-center justify-center font-bold text-white border border-slate-600">K</div>
                <div>
                    <p class="text-sm font-semibold text-slate-200">Karimov Admin</p>
                    <p class="text-xs text-slate-500">Bosh operator</p>
                </div>
            </div>
        </aside>

        <!-- ASOSIY KONTENT -->
        <main class="flex-1 flex flex-col h-screen overflow-y-auto">
            
            <!-- HEADER -->
            <header class="bg-white border-b border-slate-200 px-6 py-4 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 sticky top-0 z-40 shadow-sm">
                <div>
                    <h1 class="text-xl font-bold text-slate-900" x-text="menus.find(m => m.id === activeTab).name"></h1>
                    <p class="text-xs text-slate-500 mt-0.5">Tizim holati: <span class="text-emerald-500 font-medium">Onlayn</span> • Sync faol</p>
                </div>
                
                <div class="flex items-center gap-3 w-full sm:w-auto justify-end">
                    <button @click="openModal('addModal')" class="bg-blue-600 hover:bg-blue-700 text-white font-medium px-4 py-2.5 rounded-xl shadow-lg shadow-blue-600/20 transition text-sm flex items-center gap-2">
                        <i class="fas fa-plus text-xs"></i> Yangi Mahsulot
                    </button>
                </div>
            </header>

            <!-- KONTENT HUDUDI -->
            <div class="p-6 space-y-6 flex-1">

                <!-- TAB 1: ANALITIKA -->
                <div x-show="activeTab === 'dashboard'" x-cloak class="space-y-6">
                    <!-- Statisika kartalari -->
                    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
                        <div class="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex items-center justify-between">
                            <div>
                                <p class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Jami Mahsulotlar</p>
                                <h3 class="text-2xl font-bold text-slate-800 mt-1" x-text="products.length + ' ta'"></h3>
                            </div>
                            <div class="bg-blue-50 p-3 rounded-xl text-blue-600"><i class="fas fa-box text-xl"></i></div>
                        </div>
                        <div class="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex items-center justify-between">
                            <div>
                                <p class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Ombor Balansi</p>
                                <h3 class="text-2xl font-bold text-slate-800 mt-1" x-text="formatMoney(totalValue())"></h3>
                            </div>
                            <div class="bg-emerald-50 p-3 rounded-xl text-emerald-600"><i class="fas fa-wallet text-xl"></i></div>
                        </div>
                        <div class="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex items-center justify-between">
                            <div>
                                <p class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Kam qolganlar</p>
                                <h3 class="text-2xl font-bold mt-1" :class="lowStockCount() > 0 ? 'text-amber-500' : 'text-slate-800'" x-text="lowStockCount() + ' tur'"></h3>
                            </div>
                            <div class="bg-amber-50 p-3 rounded-xl text-amber-600"><i class="fas fa-triangle-exclamation text-xl"></i></div>
                        </div>
                        <div class="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex items-center justify-between">
                            <div>
                                <p class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Faol Omborlar</p>
                                <h3 class="text-2xl font-bold text-slate-800 mt-1" x-text="warehouses.length + ' ta'"></h3>
                            </div>
                            <div class="bg-purple-50 p-3 rounded-xl text-purple-600"><i class="fas fa-warehouse text-xl"></i></div>
                        </div>
                    </div>

                    <!-- Grafik qismi -->
                    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                        <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm lg:col-span-2">
                            <h3 class="text-sm font-bold text-slate-800 mb-4 uppercase tracking-wider text-slate-400">Kategoriya bo'yicha zaxira tahlili</h3>
                            <div class="h-64"><canvas id="analyticsChart"></canvas></div>
                        </div>
                        <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
                            <h3 class="text-sm font-bold text-slate-800 mb-4 uppercase tracking-wider text-slate-400">Omborlar ulushi</h3>
                            <div class="h-64"><canvas id="pieChart"></canvas></div>
                        </div>
                    </div>
                </div>

                <!-- TAB 2: MAHSULOTLAR RO'YXATI (Barcha operatsiyalar bilan) -->
                <div x-show="activeTab === 'products'" x-cloak class="space-y-4">
                    <!-- Filtrlar paneli -->
                    <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm grid grid-cols-1 sm:grid-cols-3 gap-4">
                        <div class="relative">
                            <i class="fas fa-search absolute left-3.5 top-3.5 text-slate-400 text-sm"></i>
                            <input type="text" x-model="searchQuery" placeholder="Nom yoki SKU bo'yicha qidirish..." class="w-full bg-slate-50 border border-slate-200 rounded-xl pl-10 pr-4 py-2.5 text-sm focus:outline-none focus:border-blue-500 focus:bg-white transition">
                        </div>
                        <div>
                            <select x-model="filterWarehouse" class="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-blue-500 focus:bg-white transition">
                                <option value="">Barcha Omborlar</option>
                                <template x-for="wh in warehouses">
                                    <option :value="wh" x-text="wh"></option>
                                </template>
                            </select>
                        </div>
                        <div>
