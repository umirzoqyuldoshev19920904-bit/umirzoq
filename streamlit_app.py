import streamlit as st
import pandas as pd
from datetime import datetime
import os
import base64

# Sahifaning yuqori sozlamalari
st.set_page_config(
    page_title="Smart-Ombor Ultra ERP v4.0",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium CSS - Streamlit elementlarini butunlay o'zgartirish va brend dizayn berish
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    /* Umumiy fon sozlamalari */
    .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background-color: #f8fafc !important;
    }
    
    /* Streamlit menyulari va keraksiz elementlarni yashirish */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Sidebar premium dizayni */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important;
        border-right: 1px solid #334155 !important;
    }
    [data-testid="stSidebar"] * {
        color: #f1f5f9 !important;
    }
    
    /* Sidebar navigatsiya tugmalari dizayni */
    div[data-testid="stSidebarUserContent"] div[role="radiogroup"] {
        gap: 12px !important;
        padding-top: 10px;
    }
    div[data-testid="stSidebarUserContent"] div[role="radiogroup"] label {
        background-color: rgba(30, 41, 59, 0.7) !important;
        color: #94a3b8 !important;
        border-radius: 16px !important;
        padding: 14px 18px !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        cursor: pointer !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        width: 100% !important;
        display: flex !important;
        align-items: center !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
    }
    div[data-testid="stSidebarUserContent"] div[role="radiogroup"] label[data-checked="true"] {
        background: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%) !important;
        color: white !important;
        border-color: #6366f1 !important;
        box-shadow: 0 10px 15px -3px rgba(79, 70, 229, 0.4) !important;
        transform: translateY(-2px);
    }
    div[data-testid="stSidebarUserContent"] div[role="radiogroup"] label:hover {
        background-color: #1e293b !important;
        color: #f1f5f9 !important;
        transform: translateY(-1px);
    }
    div[data-testid="stSidebarUserContent"] div[role="radiogroup"] label div[role="presentation"] {
        display: none !important;
    }

    /* Streamlit kiritish maydonlari (Inputs) dizaynini modernizatsiya qilish */
    div[data-testid="stTextInput"] input, 
    div[data-testid="stNumberInput"] input,
    div[data-testid="stSelectbox"] div[role="combobox"] {
        background-color: white !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 14px !important;
        padding: 12px 16px !important;
        font-weight: 500 !important;
        color: #1e293b !important;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05) !important;
        transition: all 0.2s ease !important;
    }
    div[data-testid="stTextInput"] input:focus, 
    div[data-testid="stNumberInput"] input:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.1) !important;
    }

    /* Tugmalar (Buttons) premium dizayni */
    div.stButton > button {
        background: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%) !important;
        color: white !important;
        border-radius: 14px !important;
        border: none !important;
        padding: 14px 28px !important;
        font-size: 15px !important;
        font-weight: 700 !important;
        letter-spacing: -0.01em !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 10px 15px -3px rgba(79, 70, 229, 0.3) !important;
        width: 100% !important;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 20px 25px -5px rgba(79, 70, 229, 0.4) !important;
    }
    div.stButton > button:active {
        transform: translateY(0);
    }

    /* Tabs (Tablar) dizayni */
    button[data-baseweb="tab"] {
        font-size: 15px !important;
        font-weight: 700 !important;
        color: #64748b !important;
        border-bottom-width: 3px !important;
        transition: all 0.2s ease !important;
    }
    button[aria-selected="true"] {
        color: #4f46e5 !important;
        border-bottom-color: #4f46e5 !important;
    }

    /* Silliq premium kartochka (Soft Premium Card) */
    .soft-card {
        background: white;
        padding: 28px;
        border-radius: 24px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 20px -2px rgba(148, 163, 184, 0.06), 0 2px 4px -1px rgba(148, 163, 184, 0.03);
        margin-bottom: 24px;
    }

    /* Zamonaviy Neon KPI Card */
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: 20px;
        margin-bottom: 25px;
    }
    .kpi-card {
        background: white;
        padding: 24px;
        border-radius: 24px;
        border: 1px solid #f1f5f9;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.02);
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: transform 0.3s ease;
    }
    .kpi-card:hover {
        transform: translateY(-4px);
    }

    /* HTML Jadvallari uchun modern dizayn (st.dataframe o'rniga) */
    .modern-table-container {
        width: 100%;
        overflow-x: auto;
        border-radius: 20px;
        border: 1px solid #e2e8f0;
        background: white;
        box-shadow: 0 10px 30px -10px rgba(0,0,0,0.03);
    }
    .modern-table {
        width: 100%;
        border-collapse: collapse;
        text-align: left;
    }
    .modern-table th {
        background-color: #f8fafc;
        padding: 18px 24px;
        font-size: 13px;
        font-weight: 700;
        color: #475569;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        border-bottom: 1px solid #e2e8f0;
    }
    .modern-table td {
        padding: 18px 24px;
        font-size: 14px;
        color: #334155;
        border-bottom: 1px solid #f1f5f9;
        font-weight: 500;
    }
    .modern-table tr:last-child td {
        border-bottom: none;
    }
    .modern-table tr:hover {
        background-color: #f8fafc;
    }

    /* Yandex Market Premium Card Grid */
    .yandex-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
        gap: 24px;
        padding: 10px 0;
    }
    .yandex-card {
        background: white;
        border-radius: 24px;
        border: 1px solid #e2e8f0;
        overflow: hidden;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        position: relative;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.01), 0 2px 4px -1px rgba(0, 0, 0, 0.01);
    }
    .yandex-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.05), 0 10px 10px -5px rgba(0, 0, 0, 0.02);
    }
    .yandex-img-container {
        width: 100%;
        height: 220px;
        background-color: #f8fafc;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        position: relative;
        border-bottom: 1px solid #f1f5f9;
    }
    .yandex-img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .yandex-card:hover .yandex-img {
        transform: scale(1.08);
    }
    .yandex-badge {
        position: absolute;
        top: 12px;
        left: 12px;
        padding: 6px 12px;
        border-radius: 10px;
        font-size: 11px;
        font-weight: 800;
        color: white;
        z-index: 2;
        letter-spacing: 0.02em;
    }
    .yandex-info {
        padding: 20px;
        flex-grow: 1;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .yandex-cat {
        font-size: 11px;
        color: #94a3b8;
        text-transform: uppercase;
        font-weight: 800;
        letter-spacing: 0.06em;
        margin-bottom: 6px;
    }
    .yandex-title {
        font-size: 15px;
        font-weight: 700;
        color: #0f172a;
        margin: 0 0 12px 0;
        line-height: 1.5;
        height: 44px;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
    }
    .yandex-price-box {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: auto;
        border-top: 1px solid #f1f5f9;
        padding-top: 14px;
    }
    .yandex-price {
        font-size: 16px;
        font-weight: 800;
        color: #4f46e5;
    }
    .yandex-stock {
        font-size: 13px;
        font-weight: 700;
        color: #64748b;
        background: #f1f5f9;
        padding: 4px 8px;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

FAYL_OMBOR = "onlayn_ombor.xlsx"
DEFAULT_PLACEHOLDER = "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&q=80&w=300"

def bazani_yuklash():
    """Barcha zaruriy ma'lumotlar jadvallarini Exceldan yuklaydi yoki yaratadi."""
    if os.path.exists(FAYL_OMBOR):
        try:
            ombor_df = pd.read_excel(FAYL_OMBOR, sheet_name="Ombor")
            kirim_df = pd.read_excel(FAYL_OMBOR, sheet_name="Kirim")
            chiqim_df = pd.read_excel(FAYL_OMBOR, sheet_name="Chiqim")
            
            try:
                agent_df = pd.read_excel(FAYL_OMBOR, sheet_name="Agentlar")
            except Exception:
                agent_df = pd.DataFrame(columns=["Agent Nomi", "Telefon", "Joriy Qarz"])
            
            # Yangi rasm ustunini tekshirish va qo'shish
            if "Rasm" not in ombor_df.columns:
                ombor_df["Rasm"] = ""
            
            ombor_df["Miqdori"] = pd.to_numeric(ombor_df["Miqdori"], errors='coerce').fillna(0)
            if "Narxi" not in ombor_df.columns:
                ombor_df["Narxi"] = 10000.0
            if "Kategoriya" not in ombor_df.columns:
                ombor_df["Kategoriya"] = "Boshqa"
                
            ombor_df["Narxi"] = pd.to_numeric(ombor_df["Narxi"], errors='coerce').fillna(10000.0)
            ombor_df["Rasm"] = ombor_df["Rasm"].fillna("")
            kirim_df["Miqdori"] = pd.to_numeric(kirim_df["Miqdori"], errors='coerce').fillna(0)
            chiqim_df["Miqdori"] = pd.to_numeric(chiqim_df["Miqdori"], errors='coerce').fillna(0)
            agent_df["Joriy Qarz"] = pd.to_numeric(agent_df["Joriy Qarz"], errors='coerce').fillna(0)
            
            return ombor_df, kirim_df, chiqim_df, agent_df
        except Exception as e:
            st.error(f"Baza yuklanishida xatolik yuz berdi: {e}. Yangi baza tuzilmoqda...")
            
    ombor_df = pd.DataFrame(columns=["Mahsulot Nomi", "Miqdori", "O'lchov Birligi", "Narxi", "Kategoriya", "Rasm"])
    kirim_df = pd.DataFrame(columns=["Sana", "Mahsulot Nomi", "Miqdori", "Mas'ul"])
    chiqim_df = pd.DataFrame(columns=["Sana", "Mahsulot Nomi", "Miqdori", "Qabul qiluvchi", "Agent", "Chiqim Turi", "Jami Summa"])
    agent_df = pd.DataFrame(columns=["Agent Nomi", "Telefon", "Joriy Qarz"])
    return ombor_df, kirim_df, chiqim_df, agent_df

def bazani_saqlash(ombor, kirim, chiqim, agentlar):
    """Barcha o'zgarishlarni Excelga mukammal tarzda yozadi."""
    with pd.ExcelWriter(FAYL_OMBOR, engine="openpyxl") as writer:
        ombor.to_excel(writer, sheet_name="Ombor", index=False)
        kirim.to_excel(writer, sheet_name="Kirim", index=False)
        chiqim.to_excel(writer, sheet_name="Chiqim", index=False)
        agentlar.to_excel(writer, sheet_name="Agentlar", index=False)

# Ma'lumotlarni xotiraga chaqirish
ombor, kirim, chiqim, agentlar = bazani_yuklash()

def to_base64(uploaded_file):
    """Yuklangan rasm faylini Base64 formatiga o'tkazadi."""
    if uploaded_file is not None:
        file_bytes = uploaded_file.read()
        b64_string = base64.b64encode(file_bytes).decode("utf-8")
        file_type = uploaded_file.type
        return f"data:{file_type};base64,{b64_string}"
    return ""

def format_money(amount):
    return f"{amount:,.0f} UZS".replace(",", " ")

# Sidebar Brending
st.sidebar.markdown("""
<div style="display: flex; align-items: center; gap: 14px; padding: 20px 0 30px 0; border-bottom: 1px solid rgba(255,255,255,0.08); margin-bottom: 25px;">
    <div style="background: linear-gradient(135deg, #6366f1 0%, #3b82f6 100%); padding: 14px; border-radius: 18px; display: flex; align-items: center; justify-content: center; box-shadow: 0 10px 15px -3px rgba(99, 102, 241, 0.4);">
        <span style="font-size: 24px; color: white;">⚡</span>
    </div>
    <div>
        <h2 style="font-size: 19px; font-weight: 800; color: white; margin: 0; padding: 0; letter-spacing: -0.02em;">Smart-Ombor</h2>
        <span style="font-size: 10px; color: #818cf8; font-weight: 700; text-transform: uppercase; letter-spacing: 0.12em;">Ultra ERP v4.0</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Kirish roli
rol = st.sidebar.radio("🔑 TIZIMGA KIRISH REJIMI", ["👤 Agent Rejimi", "🔐 Admin Rejimi"])
administrator_tasdiq = False

if rol == "🔐 Admin Rejimi":
    parol = st.sidebar.text_input("Maxfiy parolni kiriting:", type="password")
    if parol == "19920904":
        administrator_tasdiq = True
        st.sidebar.success("🔓 ADMIN TASDIQLANDI!")
    else:
        if parol != "":
            st.sidebar.error("❌ Maxfiy parol noto'g'ri!")
        st.sidebar.info("Agent rejimidan foydalanish uchun yuqoridagi 'Agent Rejimi' tugmasini bosing.")

# Rolga muvofiq navigatsiya menyusini yaratish
if administrator_tasdiq:
    menyu = st.sidebar.radio(
        "ASOSIY BO'LIMLAR",
        ["🛍️ Yandex Katalog", "📊 Boshqaruv Paneli", "📦 Mahsulotlar Qoldig'i", "👥 Agentlar & Qarzdorlik", "📥 Yangi Kirim", "📤 Yangi Chiqim", "🕒 Amallar Tarixi"]
    )
else:
    menyu = "🛍️ Yandex Katalog (Agent)"
    st.sidebar.markdown("""
    <div style="padding: 18px; background: rgba(30, 41, 59, 0.5); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 18px; margin-top: 25px;">
        <p style="font-size: 12px; color: #94a3b8; margin: 0; line-height: 1.6;">Siz hozirda <b>Agent Rejimi</b>dasiz. Sizga faqat joriy mahsulotlar rasmlari va qoldig'i ko'rsatiladi.</p>
    </div>
    """, unsafe_allow_html=True)

def mahsulot_katalogini_chizish(admin_view=False):
    """Yandex.jpg dagi kabi mahsulotlarni chiroyli rasm va kartochkalar ko'rinishida chiqaradi."""
    st.markdown("""
    <div style="margin-bottom: 30px;">
        <h1 style="font-size: 36px; font-weight: 800; color: #0f172a; margin-bottom: 8px; letter-spacing: -0.03em;">🛍️ Onlayn Katalog</h1>
        <p style="font-size: 16px; color: #64748b; margin: 0;">Mavjud barcha mahsulotlarning vizual ko'rgazmasi va joriy zaxirasi</p>
    </div>
    """, unsafe_allow_html=True)

    # Qidiruv va Toifa filtri
    col_q, col_t = st.columns([3, 1])
    with col_q:
        qidiruv_txt = st.text_input("🔍 Mahsulot nomi bo'yicha qidirish...", placeholder="Masalan: Armatura, Kabel...")
    with col_t:
        toifa_turlari = ["Barchasi"] + list(ombor["Kategoriya"].unique()) if not ombor.empty else ["Barchasi"]
        tanlangan_toifa = st.selectbox("Turkum bo'yicha saralash:", toifa_turlari)

    # Filtrlash
    filtr_ombor = ombor.copy()
    if qidiruv_txt:
        filtr_ombor = filtr_ombor[filtr_ombor["Mahsulot Nomi"].str.lower().str.contains(qidiruv_txt.lower())]
    if tanlangan_toifa != "Barchasi":
        filtr_ombor = filtr_ombor[filtr_ombor["Kategoriya"] == tanlangan_toifa]

    if filtr_ombor.empty:
        st.info("Katalogda hech qanday mahsulot topilmadi.")
        return

    # Kartochkalar to'plamini chizish
    html_cards = '<div class="yandex-grid">'
    
    for idx, row in filtr_ombor.iterrows():
        # Rasm mavjudligini tekshirish
        rasm_src = row["Rasm"] if row["Rasm"] != "" else DEFAULT_PLACEHOLDER
        nomi = row["Mahsulot Nomi"]
        kat = row["Kategoriya"]
        miqdor = row["Miqdori"]
        birligi = row["O'lchov Birligi"]
        
        # Narxni faqat admin ko'ra oladi
        if admin_view:
            narx_str = format_money(row["Narxi"])
        else:
            narx_str = "Sotuvda"

        # Status va uning rangi
        if miqdor <= 0:
            status_text = "Tugagan"
            status_bg = "#ef4444" # Rose/Red
        elif miqdor <= 15:
            status_text = "Zaxira kam"
            status_bg = "#f59e0b" # Amber
        else:
            status_text = "Mavjud"
            status_bg = "#10b981" # Emerald

        # Kartochka HTML
        html_cards += f"""
        <div class="yandex-card">
            <div class="yandex-img-container">
                <span class="yandex-badge" style="background-color: {status_bg};">{status_text}</span>
                <img src="{rasm_src}" class="yandex-img" alt="{nomi}" />
            </div>
            <div class="yandex-info">
                <div>
                    <div class="yandex-cat">{kat}</div>
                    <h3 class="yandex-title">{nomi}</h3>
                </div>
                <div class="yandex-price-box">
                    <span class="yandex-price">{narx_str}</span>
                    <span class="yandex-stock">{miqdor:g} {birligi}</span>
                </div>
            </div>
        </div>
        """
    
    html_cards += '</div>'
    st.markdown(html_cards, unsafe_allow_html=True)

# Sahifalar yo'nalishi
if menyu in ["🛍️ Yandex Katalog", "🛍️ Yandex Katalog (Agent)"]:
    mahsulot_katalogini_chizish(admin_view=administrator_tasdiq)

elif administrator_tasdiq and menyu == "📊 Boshqaruv Paneli":
    st.markdown("""
    <div style="margin-bottom: 30px;">
        <h1 style="font-size: 36px; font-weight: 800; color: #0f172a; margin-bottom: 8px; letter-spacing: -0.03em;">📊 Boshqaruv Paneli</h1>
        <p style="font-size: 16px; color: #64748b; margin: 0;">Real vaqtda umumiy hisob-kitoblar va grafik tahlillar</p>
    </div>
    """, unsafe_allow_html=True)

    # KPIs
    jami_turlar = len(ombor)
    jami_dona = int(ombor["Miqdori"].sum()) if jami_turlar > 0 else 0
    jami_qiymat = (ombor["Miqdori"] * ombor["Narxi"]).sum() if jami_turlar > 0 else 0
    jami_agent_qarzlari = agentlar["Joriy Qarz"].sum() if not agentlar.empty else 0

    def kpi_card(title, value, subtitle, icon, icon_color, bg_gradient):
        return f"""
        <div style="background: white; padding: 26px; border-radius: 24px; border: 1px solid #e2e8f0; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.02);">
            <div>
                <span style="font-size: 11px; font-weight: 800; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.08em; display: block; margin-bottom: 8px;">{title}</span>
                <h3 style="font-size: 28px; font-weight: 800; color: #0f172a; margin: 0; letter-spacing: -0.02em;">{value}</h3>
                <span style="font-size: 13px; color: #64748b; display: block; margin-top: 10px;">{subtitle}</span>
            </div>
            <div style="background: {bg_gradient}; padding: 16px; border-radius: 20px; color: {icon_color}; font-size: 28px; display: flex; align-items: center; justify-content: center; width: 64px; height: 64px; box-shadow: inset 0 2px 4px rgba(255,255,255,0.1);">
                {icon}
            </div>
        </div>
        """

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(kpi_card("Maxsulot turlari", f"{jami_turlar} xil", "Mavjud tovarlar", "📦", "#4f46e5", "linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%)"), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi_card("Umumiy qoldiq", f"{jami_dona} dona", "Barcha zaxira", "📊", "#10b981", "linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%)"), unsafe_allow_html=True)
    with c3:
        st.markdown(kpi_card("Ombor qiymati", format_money(jami_qiymat), "Sotish qiymatida", "💰", "#f59e0b", "linear-gradient(135deg, #fef3c7 0%, #fde68a 100%)"), unsafe_allow_html=True)
    with c4:
        st.markdown(kpi_card("Yig'iladigan qarzlar", format_money(jami_agent_qarzlari), "Agentlardagi haqqimiz", "👥", "#ef4444", "linear-gradient(135deg, #fee2e2 0%, #fca5a5 100%)"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    g1, g2 = st.columns([3, 2])
    with g1:
        st.markdown('<div class="soft-card"><h4>📈 Mahsulotlar Miqdori Tahlili (Top 10)</h4></div>', unsafe_allow_html=True)
        if jami_turlar > 0:
            st.bar_chart(data=ombor.head(10), x="Mahsulot Nomi", y="Miqdori", color="#4f46e5")
    with g2:
        st.markdown('<div class="soft-card"><h4>⚠️ Zaxirasi kamaygan mahsulotlar</h4></div>', unsafe_allow_html=True)
        kam_qoldiq = ombor[ombor["Miqdori"] <= 15]
        if not kam_qoldiq.empty:
            for _, r in kam_qoldiq.iterrows():
                olchov_birligi = r["O'lchov Birligi"]
                st.markdown(f"""
                <div style="background: #fffbeb; border: 1px solid #fef3c7; border-left: 6px solid #f59e0b; padding: 16px; border-radius: 16px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong style="color: #92400e; font-size: 14px;">🚨 {r['Mahsulot Nomi']}</strong>
                        <div style="color: #b45309; font-size: 12px; margin-top: 4px;">Tezda kirim qilish tavsiya etiladi</div>
                    </div>
                    <span style="background: #f59e0b; color: white; padding: 6px 12px; border-radius: 10px; font-weight: 800; font-size: 12px;">{r['Miqdori']:g} {olchov_birligi}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("Barcha mahsulotlar zaxirasi yetarli!")

elif administrator_tasdiq and menyu == "📦 Mahsulotlar Qoldig'i":
    st.markdown("""
    <div style="margin-bottom: 30px;">
        <h1 style="font-size: 36px; font-weight: 800; color: #0f172a; margin-bottom: 8px; letter-spacing: -0.03em;">📦 Mahsulotlar Qoldig'i & Rasmlar</h1>
        <p style="font-size: 16px; color: #64748b; margin: 0;">Mavjud tovarlarni boshqarish hamda rasmlarini yangilash bo'limi</p>
    </div>
    """, unsafe_allow_html=True)

    # 🖼️ Rasm tahrirlash expanderi
    with st.expander("🖼️ Mahsulot rasmiga o'zgartirish kiritish / yangilash"):
        if not ombor.empty:
            tanlangan_prod = st.selectbox("Rasmini yangilamoqchi bo'lgan mahsulotingizni tanlang:", ombor["Mahsulot Nomi"].unique())
            yangi_rasm_fayl = st.file_uploader("Yangi rasm yuklang (PNG, JPG, JPEG):", type=["png", "jpg", "jpeg"], key="edit_img")
            
            if st.button("Rasmni saqlash"):
                if yangi_rasm_fayl:
                    b64_str = to_base64(yangi_rasm_fayl)
                    ombor.loc[ombor["Mahsulot Nomi"] == tanlangan_prod, "Rasm"] = b64_str
                    bazani_saqlash(ombor, kirim, chiqim, agentlar)
                    st.success(f"✅ '{tanlangan_prod}' mahsulotining rasmi muvaffaqiyatli yangilandi!")
                    st.rerun()
                else:
                    st.error("Iltimos, avval rasmni tanlang!")

    # Mahsulotlar Jadvali HTML formatda (Modern dizayn)
    html_table = """
    <div class="modern-table-container">
        <table class="modern-table">
            <thead>
                <tr>
                    <th>Turkum</th>
                    <th>Mahsulot Nomi</th>
                    <th>Zaxira qoldig'i</th>
                    <th>Narxi (UZS)</th>
                </tr>
            </thead>
            <tbody>
    """
    for idx, row in ombor.iterrows():
        olchov_birligi = row["O'lchov Birligi"]
        html_table += f"""
                <tr>
                    <td style="color: #64748b;"><span style="background: #f1f5f9; padding: 4px 10px; border-radius: 8px; font-weight: 700; font-size: 12px;">{row['Kategoriya']}</span></td>
                    <td style="font-weight: 700; color: #0f172a;">{row['Mahsulot Nomi']}</td>
                    <td style="font-weight: 800; color: {'#ef4444' if row['Miqdori'] <= 15 else '#10b981'};">{row['Miqdori']:g} {olchov_birligi}</td>
                    <td style="font-weight: 700; color: #4f46e5;">{format_money(row['Narxi'])}</td>
                </tr>
        """
    html_table += """
            </tbody>
        </table>
    </div>
    """
    st.markdown(html_table, unsafe_allow_html=True)

elif administrator_tasdiq and menyu == "👥 Agentlar & Qarzdorlik":
    st.markdown("""
    <div style="margin-bottom: 30px;">
        <h1 style="font-size: 36px; font-weight: 800; color: #0f172a; margin-bottom: 8px; letter-spacing: -0.03em;">👥 Agentlar va To'lovlar Tizimi</h1>
        <p style="font-size: 16px; color: #64748b; margin: 0;">Olib ketilgan mahsulotlar qarzdorliklarini tahlil qilish va qabul qilingan pullarni hisobga olish</p>
    </div>
    """, unsafe_allow_html=True)

    t1, t2 = st.tabs(["👥 Agentlar Ro'yxati", "➕ Yangi Agent & To'lov Qabul Qilish"])
    
    with t1:
        if not agentlar.empty:
            # Agentlar ro'yxatini chiroyli modern kartochkalar shaklida chiqarish
            agent_html = '<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px;">'
            for _, r in agentlar.iterrows():
                qarz_rang = '#ef4444' if r['Joriy Qarz'] > 0 else '#10b981'
                qarz_bg = '#fef2f2' if r['Joriy Qarz'] > 0 else '#ecfdf5'
                agent_html += f"""
                <div style="background: white; border: 1px solid #e2e8f0; border-radius: 20px; padding: 24px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.01); display: flex; flex-direction: column; justify-content: space-between;">
                    <div>
                        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 14px;">
                            <div style="background: #e0e7ff; color: #4f46e5; width: 44px; height: 44px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 16px;">
                                {r['Agent Nomi'][0]}
                            </div>
                            <div>
                                <h4 style="margin: 0; color: #0f172a; font-size: 16px; font-weight: 800;">{r['Agent Nomi']}</h4>
                                <span style="font-size: 12px; color: #64748b; font-weight: 600;">👤 Agent</span>
                            </div>
                        </div>
                        <div style="font-size: 13px; color: #475569; margin-bottom: 16px;">
                            📞 Tel: <strong>{r['Telefon']}</strong>
                        </div>
                    </div>
                    <div style="background: {qarz_bg}; padding: 12px 16px; border-radius: 12px; display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 11px; font-weight: 800; color: #64748b; text-transform: uppercase;">Qarz:</span>
                        <span style="font-weight: 800; color: {qarz_rang}; font-size: 14px;">{format_money(r['Joriy Qarz'])}</span>
                    </div>
                </div>
                """
            agent_html += '</div>'
            st.markdown(agent_html, unsafe_allow_html=True)
        else:
            st.info("Hali hech qanday agent qo'shilmagan.")

    with t2:
        col_ag, col_tol = st.columns(2)
        with col_ag:
            st.markdown('<div class="soft-card"><h4>👥 Yangi Agent qo\'shish</h4>', unsafe_allow_html=True)
            with st.form("agent_add_form"):
                nomi = st.text_input("F.I.Sh:").strip().capitalize()
                tel = st.text_input("Telefon:")
                submit_agent = st.form_submit_button("Saqlash")
                if submit_agent and nomi:
                    if nomi not in agentlar["Agent Nomi"].values:
                        yangi_agent = pd.DataFrame([{"Agent Nomi": nomi, "Telefon": tel, "Joriy Qarz": 0.0}])
                        agentlar = pd.concat([agentlar, yangi_agent], ignore_index=True)
                        bazani_saqlash(ombor, kirim, chiqim, agentlar)
                        st.success(f"✅ {nomi} muvaffaqiyatli qo'shildi!")
                        st.rerun()
                    else:
                        st.error("Bunday agent allaqachon mavjud!")
            st.markdown('</div>', unsafe_allow_html=True)

        with col_tol:
            st.markdown('<div class="soft-card"><h4>💰 Qarzni so\'ndirish (To\'lov)</h4>', unsafe_allow_html=True)
            if not agentlar.empty:
                with st.form("qarz_yopish_form"):
                    t_agent = st.selectbox("Agentni tanlang:", agentlar["Agent Nomi"].unique())
                    summa = st.number_input("Summa:", min_value=1000.0, step=50000.0)
                    izoh = st.text_input("Izoh:")
                    submit_tolov = st.form_submit_button("To'lovni tasdiqlash")
                    if submit_tolov:
                        agentlar.loc[agentlar["Agent Nomi"] == t_agent, "Joriy Qarz"] -= summa
                        sana = datetime.now().strftime("%Y-%m-%d %H:%M")
                        yangi_qayd = pd.DataFrame([{
                            "Sana": sana, "Mahsulot Nomi": "Qarz to'lovi", "Miqdori": 0,
                            "Qabul qiluvchi": t_agent, "Agent": t_agent, "Chiqim Turi": f"Qarz yopilishi ({izoh})", "Jami Summa": -summa
                        }])
                        chiqim = pd.concat([chiqim, yangi_qayd], ignore_index=True)
                        bazani_saqlash(ombor, kirim, chiqim, agentlar)
                        st.success(f"✅ Muvaffaqiyatli: {t_agent} hisobidan {format_money(summa)} qabul dili!")
                        st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

elif administrator_tasdiq and menyu == "📥 Yangi Kirim":
    st.markdown("""
    <div style="margin-bottom: 30px;">
        <h1 style="font-size: 36px; font-weight: 800; color: #0f172a; margin-bottom: 8px; letter-spacing: -0.03em;">📥 Yangi Kirim Operatsiyasi</h1>
        <p style="font-size: 16px; color: #64748b; margin: 0;">Omborxonaga yangi yoki mavjud tovarlarni qabul qilish paneli</p>
    </div>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        kirim_shakli = st.radio("Kirim shakli:", ["Mavjud mahsulot qoldig'ini oshirish", "Yangi mahsulot yaratish (Rasm bilan)"])
        
        col_k1, col_k2 = st.columns(2)
        with col_k1:
            if kirim_shakli == "Mavjud mahsulot qoldig'ini oshirish" and not ombor.empty:
                nomi = st.selectbox("Mahsulot:", ombor["Mahsulot Nomi"].unique())
                birligi = ombor.loc[ombor["Mahsulot Nomi"] == nomi, "O'lchov Birligi"].values[0]
                kategoriya = ombor.loc[ombor["Mahsulot Nomi"] == nomi, "Kategoriya"].values[0]
                bosh_narx = float(ombor.loc[ombor["Mahsulot Nomi"] == nomi, "Narxi"].values[0])
                rasm_b64 = ombor.loc[ombor["Mahsulot Nomi"] == nomi, "Rasm"].values[0]
            else:
                nomi = st.text_input("Yangi mahsulot nomi:").strip().capitalize()
                kategoriya = st.selectbox("Turkum:", ["Qurilish materiallari", "Elektrotexnika", "Santexnika", "Boshqa"])
                birligi = st.selectbox("Birligi:", ["dona", "kg", "metr", "litr", "qop"])
                bosh_narx = 10000.0
                rasm_b64 = ""

            # 📸 Rasm yuklash maydoni
            rasm_fayl = st.file_uploader("Mahsulot rasmini yuklang (Ixtiyoriy):", type=["png", "jpg", "jpeg"])
            if rasm_fayl:
                rasm_b64 = to_base64(rasm_fayl)

        with col_k2:
            miqdor = st.number_input("Miqdori:", min_value=0.1, value=1.0)
            narx = st.number_input("Sotish narxi:", min_value=0.0, value=bosh_narx)
            masul = st.text_input("Mas'ul shaxs:", value="Ombor mudiri")

        if st.button("📥 Kirimni tasdiqlash"):
            if nomi and masul:
                if nomi in ombor["Mahsulot Nomi"].values:
                    ombor.loc[ombor["Mahsulot Nomi"] == nomi, "Miqdori"] += miqdor
                    ombor.loc[ombor["Mahsulot Nomi"] == nomi, "Narxi"] = narx
                    if rasm_b64 != "":
                        ombor.loc[ombor["Mahsulot Nomi"] == nomi, "Rasm"] = rasm_b64
                else:
                    yangi_qator = pd.DataFrame([{
                        "Mahsulot Nomi": nomi, "Miqdori": miqdor, "O'lchov Birligi": birligi, 
                        "Narxi": narx, "Kategoriya": kategoriya, "Rasm": rasm_b64
                    }])
                    ombor = pd.concat([ombor, yangi_qator], ignore_index=True)

                sana = datetime.now().strftime("%Y-%m-%d %H:%M")
                yangi_kirim = pd.DataFrame([{"Sana": sana, "Mahsulot Nomi": nomi, "Miqdori": miqdor, "Mas'ul": masul}])
                kirim = pd.concat([kirim, yangi_kirim], ignore_index=True)

                bazani_saqlash(ombor, kirim, chiqim, agentlar)
                st.success(f"✅ Muvaffaqiyatli: {miqdor} {birligi} '{nomi}' omborga qabul qilindi!")
                st.rerun()
            else:
                st.error("Barcha maydonlarni to'ldiring!")

elif administrator_tasdiq and menyu == "📤 Yangi Chiqim":
    st.markdown("""
    <div style="margin-bottom: 30px;">
        <h1 style="font-size: 36px; font-weight: 800; color: #0f172a; margin-bottom: 8px; letter-spacing: -0.03em;">📤 Ombardan Mahsulot Chiqim Qilish</h1>
        <p style="font-size: 16px; color: #64748b; margin: 0;">Tovarlarni agentlarga yuklash yoki naqd savdo qilish paneli</p>
    </div>
    """, unsafe_allow_html=True)

    if ombor.empty:
        st.warning("Omborda mahsulotlar mavjud emas.")
    else:
        with st.container(border=True):
            col_ch1, col_ch2 = st.columns(2)
            with col_ch1:
                nomi = st.selectbox("Mahsulot:", ombor["Mahsulot Nomi"].unique())
                qoldiq = ombor.loc[ombor["Mahsulot Nomi"] == nomi, "Miqdori"].values[0]
                birligi = ombor.loc[ombor["Mahsulot Nomi"] == nomi, "O'lchov Birligi"].values[0]
                narx = ombor.loc[ombor["Mahsulot Nomi"] == nomi, "Narxi"].values[0]
                
                st.info(f"Mavjud zaxira: {qoldiq} {birligi} | Sotish narxi: {format_money(narx)}")
                shart = st.radio("Chiqim sharti:", ["Naqd sotuv", "Agentga qarzga yuklash"])

            with col_ch2:
                miqdor = st.number_input("Chiqim miqdori:", min_value=0.1, max_value=float(qoldiq), value=1.0)
                if shart == "Agentga qarzga yuklash" and not agentlar.empty:
                    agent = st.selectbox("Agent:", agentlar["Agent Nomi"].unique())
                    kimga = agent
                else:
                    agent = "Naqd"
                    kimga = st.text_input("Qabul qiluvchi:")

            if st.button("📤 Chiqimni tasdiqlash"):
                if kimga:
                    jami = miqdor * narx
                    ombor.loc[ombor["Mahsulot Nomi"] == nomi, "Miqdori"] -= miqdor
                    
                    if shart == "Agentga qarzga yuklash" and agent != "Naqd":
                        agentlar.loc[agentlar["Agent Nomi"] == agent, "Joriy Qarz"] += jami

                    sana = datetime.now().strftime("%Y-%m-%d %H:%M")
                    yangi_chiqim = pd.DataFrame([{
                        "Sana": sana, "Mahsulot Nomi": nomi, "Miqdori": miqdor,
                        "Qabul qiluvchi": kimga, "Agent": agent, "Chiqim Turi": shart, "Jami Summa": jami
                    }])
                    chiqim = pd.concat([chiqim, yangi_chiqim], ignore_index=True)

                    bazani_saqlash(ombor, kirim, chiqim, agentlar)
                    st.success(f"✅ Muvaffaqiyatli: {miqdor} {birligi} '{nomi}' chiqarildi. Jami summa: {format_money(jami)}")
                    st.rerun()

elif administrator_tasdiq and menyu == "🕒 Amallar Tarixi":
    st.markdown("""
    <div style="margin-bottom: 30px;">
        <h1 style="font-size: 36px; font-weight: 800; color: #0f172a; margin-bottom: 8px; letter-spacing: -0.03em;">🕒 Ombor Harakatlari Jurnali</h1>
        <p style="font-size: 16px; color: #64748b; margin: 0;">Barcha kirim va chiqim operatsiyalarining batafsil xronologiyasi</p>
    </div>
    """, unsafe_allow_html=True)

    tb1, tb2 = st.tabs(["📥 Barcha Kirimlar", "📤 Barcha Chiqimlar"])
    
    with tb1:
        if not kirim.empty:
            kirim_sorted = kirim.sort_values(by="Sana", ascending=False)
            html_kirim = """
            <div class="modern-table-container">
                <table class="modern-table">
                    <thead>
                        <tr>
                            <th>Sana</th>
                            <th>Mahsulot Nomi</th>
                            <th>Kirim Miqdori</th>
                            <th>Mas'ul Shaxs</th>
                        </tr>
                    </thead>
                    <tbody>
            """
            for _, r in kirim_sorted.iterrows():
                html_kirim += f"""
                        <tr>
                            <td style="color: #64748b;">{r['Sana']}</td>
                            <td style="font-weight: 700; color: #0f172a;">{r['Mahsulot Nomi']}</td>
                            <td style="font-weight: 800; color: #10b981;">+{r['Miqdori']:g}</td>
                            <td style="color: #475569;">{r['Mas\'ul']}</td>
                        </tr>
                """
            html_kirim += """
                    </tbody>
                </table>
            </div>
            """
            st.markdown(html_kirim, unsafe_allow_html=True)
        else:
            st.info("Hozircha hech qanday kirim amalga oshirilmagan.")

    with tb2:
        if not chiqim.empty:
            chiqim_sorted = chiqim.sort_values(by="Sana", ascending=False)
            html_chiqim = """
            <div class="modern-table-container">
                <table class="modern-table">
                    <thead>
                        <tr>
                            <th>Sana</th>
                            <th>Mahsulot Nomi</th>
                            <th>Miqdori</th>
                            <th>Qabul Qiluvchi</th>
                            <th>Agent / Shart</th>
                            <th>Jami Summa</th>
                        </tr>
                    </thead>
                    <tbody>
            """
            for _, r in chiqim_sorted.iterrows():
                summa_str = format_money(r['Jami Summa']) if r['Jami Summa'] >= 0 else format_money(abs(r['Jami Summa'])) + " (Qaytarildi)"
                html_chiqim += f"""
                        <tr>
                            <td style="color: #64748b;">{r['Sana']}</td>
                            <td style="font-weight: 700; color: #0f172a;">{r['Mahsulot Nomi']}</td>
                            <td style="font-weight: 800; color: #ef4444;">-{r['Miqdori']:g}</td>
                            <td style="color: #475569;">{r['Qabul qiluvchi']}</td>
                            <td><span style="background: #eff6ff; color: #3b82f6; padding: 4px 10px; border-radius: 8px; font-weight: 700; font-size: 12px;">{r['Agent']}</span></td>
                            <td style="font-weight: 700; color: #4f46e5;">{summa_str}</td>
                        </tr>
                """
            html_chiqim += """
                    </tbody>
                </table>
            </div>
            """
            st.markdown(html_chiqim, unsafe_allow_html=True)
        else:
            st.info("Hozircha hech qanday chiqim amalga oshirilmagan.")
