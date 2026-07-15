# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from datetime import datetime
import os
import base64

st.set_page_config(
    page_title="Smart-Ombor Ultra ERP v5.0",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background-color: #f1f5f9 !important;
    }
    
    /* Hide Streamlit default styling elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Moy Sklad Inspired Top Bar Menu */
    .top-navbar {
        background: linear-gradient(90deg, #1e3a8a 0%, #0d9488 100%);
        padding: 15px 30px;
        border-radius: 18px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 30px;
        box-shadow: 0 10px 25px -5px rgba(30, 58, 138, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .brand-section {
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    .brand-logo {
        background: rgba(255, 255, 255, 0.2);
        padding: 10px;
        border-radius: 12px;
        font-size: 20px;
        backdrop-filter: blur(10px);
    }
    
    .brand-title {
        color: #ffffff !important;
        font-weight: 800;
        font-size: 20px;
        margin: 0;
        letter-spacing: -0.02em;
    }
    
    .brand-subtitle {
        color: #99f6e4 !important;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        display: block;
    }

    /* Floating Glass Cards */
    .floating-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 24px;
        border: 1px solid rgba(255, 255, 255, 0.6);
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.05);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 24px;
    }
    
    .floating-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.1);
        border-color: rgba(99, 102, 241, 0.3);
    }

    /* Premium Styled Inputs */
    div[data-testid="stTextInput"] input, 
    div[data-testid="stNumberInput"] input,
    div[data-testid="stSelectbox"] div[role="combobox"] {
        background-color: rgba(255, 255, 255, 0.9) !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 14px !important;
        padding: 12px 16px !important;
        font-weight: 500 !important;
        color: #0f172a !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02) !important;
        transition: all 0.25s ease !important;
    }
    
    div[data-testid="stTextInput"] input:focus, 
    div[data-testid="stNumberInput"] input:focus {
        border-color: #0d9488 !important;
        box-shadow: 0 0 0 4px rgba(13, 148, 136, 0.15) !important;
    }

    /* Premium Buttons */
    div.stButton > button {
        background: linear-gradient(135deg, #0d9488 0%, #1e3a8a 100%) !important;
        color: white !important;
        border-radius: 14px !important;
        border: none !important;
        padding: 14px 28px !important;
        font-size: 14px !important;
        font-weight: 700 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 10px 15px -3px rgba(13, 148, 136, 0.3) !important;
        width: 100% !important;
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 20px 25px -5px rgba(13, 148, 136, 0.4) !important;
    }

    /* Modern Table with hover lift */
    .modern-table-container {
        width: 100%;
        overflow-x: auto;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.5);
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        box-shadow: 0 10px 30px -15px rgba(0,0,0,0.05);
    }
    
    .modern-table {
        width: 100%;
        border-collapse: collapse;
        text-align: left;
    }
    
    .modern-table th {
        background-color: rgba(241, 245, 249, 0.8);
        padding: 18px 24px;
        font-size: 12px;
        font-weight: 800;
        color: #334155;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        border-bottom: 1px solid #e2e8f0;
    }
    
    .modern-table td {
        padding: 18px 24px;
        font-size: 14px;
        color: #1e293b;
        border-bottom: 1px solid #f1f5f9;
        font-weight: 500;
        transition: all 0.15s ease;
    }
    
    .modern-table tr:hover td {
        background-color: rgba(248, 250, 252, 0.9);
        color: #0f172a;
    }

    /* Marketplace Yandex-like Grid Layout */
    .catalog-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
        gap: 25px;
        padding: 15px 0;
    }
    
    .catalog-card {
        background: white;
        border-radius: 24px;
        border: 1px solid #e2e8f0;
        overflow: hidden;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        position: relative;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.01);
    }
    
    .catalog-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 25px 35px -10px rgba(0, 0, 0, 0.08);
        border-color: #0d9488;
    }
    
    .catalog-img-container {
        width: 100%;
        height: 200px;
        background-color: #f8fafc;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        position: relative;
        border-bottom: 1px solid #f1f5f9;
    }
    
    .catalog-img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    
    .catalog-badge {
        position: absolute;
        top: 12px;
        left: 12px;
        padding: 6px 12px;
        border-radius: 10px;
        font-size: 11px;
        font-weight: 800;
        color: white;
        z-index: 2;
    }
</style>
""", unsafe_allow_html=True)

FAYL_OMBOR = "onlayn_ombor.xlsx"
DEFAULT_PLACEHOLDER = "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&q=80&w=300"

def bazani_yuklash():
    if os.path.exists(FAYL_OMBOR):
        try:
            ombor_df = pd.read_excel(FAYL_OMBOR, sheet_name="Ombor")
            kirim_df = pd.read_excel(FAYL_OMBOR, sheet_name="Kirim")
            chiqim_df = pd.read_excel(FAYL_OMBOR, sheet_name="Chiqim")
            
            try:
                agent_df = pd.read_excel(FAYL_OMBOR, sheet_name="Agentlar")
            except Exception:
                agent_df = pd.DataFrame(columns=["Agent Nomi", "Telefon", "Joriy Qarz"])
            
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
            st.error(f"Baza yuklanishida xatolik: {e}")
            
    ombor_df = pd.DataFrame(columns=["Mahsulot Nomi", "Miqdori", "O'lchov Birligi", "Narxi", "Kategoriya", "Rasm"])
    kirim_df = pd.DataFrame(columns=["Sana", "Mahsulot Nomi", "Miqdori", "Mas'ul"])
    chiqim_df = pd.DataFrame(columns=["Sana", "Mahsulot Nomi", "Miqdori", "Qabul qiluvchi", "Agent", "Chiqim Turi", "Jami Summa"])
    agent_df = pd.DataFrame(columns=["Agent Nomi", "Telefon", "Joriy Qarz"])
    return ombor_df, kirim_df, chiqim_df, agent_df

def bazani_saqlash(ombor, kirim, chiqim, agentlar):
    with pd.ExcelWriter(FAYL_OMBOR, engine="openpyxl") as writer:
        ombor.to_excel(writer, sheet_name="Ombor", index=False)
        kirim.to_excel(writer, sheet_name="Kirim", index=False)
        chiqim.to_excel(writer, sheet_name="Chiqim", index=False)
        agentlar.to_excel(writer, sheet_name="Agentlar", index=False)

ombor, kirim, chiqim, agentlar = bazani_yuklash()

def to_base64(uploaded_file):
    if uploaded_file is not None:
        file_bytes = uploaded_file.read()
        b64_string = base64.b64encode(file_bytes).decode("utf-8")
        file_type = uploaded_file.type
        return f"data:{file_type};base64,{b64_string}"
    return ""

def format_money(amount):
    return f"{amount:,.0f} UZS".replace(",", " ")

st.markdown("""
<div class="top-navbar">
    <div class="brand-section">
        <div class="brand-logo">⚡</div>
        <div>
            <h1 class="brand-title">Smart-Ombor ERP</h1>
            <span class="brand-subtitle">Moy Sklad Premium v5.0</span>
        </div>
    </div>
    <div style="color: white; font-weight: 500; font-size: 14px;">
        <i class="fa-regular fa-clock"></i> Tezkor Operatsiyalar va Onlayn Hisob-Kitob
    </div>
</div>
""", unsafe_allow_html=True)

# Login and role assignment via sidebar
st.sidebar.markdown("### 🔐 TIZIMGA KIRISH")
rol = st.sidebar.radio("Kirish rejimini tanlang:", ["👤 Agent Rejimi", "🔐 Admin Rejimi"])
administrator_tasdiq = False

if rol == "🔐 Admin Rejimi":
    parol = st.sidebar.text_input("Maxfiy parolni kiriting:", type="password")
    if parol == "19920904":
        administrator_tasdiq = True
        st.sidebar.success("🔓 ADMIN TASDIQLANDI!")
    else:
        if parol != "":
            st.sidebar.error("❌ Maxfiy parol noto'g'ri!")

# Navigation Menus
if administrator_tasdiq:
    menyu = st.sidebar.radio(
        "ASOSIY BO'LIMLAR",
        ["🛍️ Yandex Katalog", "📊 Boshqaruv Paneli", "📦 Mahsulotlar Qoldig'i", "👥 Agentlar & Qarzdorlik", "📥 Yangi Kirim", "📤 Yangi Chiqim", "🕒 Amallar Tarixi"]
    )
else:
    menyu = "🛍️ Yandex Katalog (Agent)"
    st.sidebar.markdown("""
    <div style="padding: 15px; background: rgba(255, 255, 255, 0.1); border-radius: 12px; margin-top: 15px;">
        <p style="font-size: 12px; color: #cbd5e1; margin: 0;">Siz <b>Agent Rejimi</b>dasiz. Faqat qoldiqlar va mahsulot katalogini ko'rishingiz mumkin.</p>
    </div>
    """, unsafe_allow_html=True)

def mahsulot_katalogini_chizish(admin_view=False):
    st.markdown("""
    <div class="floating-card" style="margin-bottom: 25px;">
        <h2 style="font-size: 26px; font-weight: 800; color: #0f172a; margin-bottom: 6px;">🛍️ Onlayn Mahsulotlar Katalogi</h2>
        <p style="font-size: 14px; color: #64748b; margin: 0;">Mavjud barcha mahsulotlarning joriy ombor zaxiralari va vizual galereyasi</p>
    </div>
    """, unsafe_allow_html=True)

    col_q, col_t = st.columns([3, 1])
    with col_q:
        qidiruv_txt = st.text_input("🔍 Mahsulot nomi bo'yicha qidirish...", placeholder="Kabel, Sement, Armatura...")
    with col_t:
        toifa_turlari = ["Barchasi"] + list(ombor["Kategoriya"].unique()) if not ombor.empty else ["Barchasi"]
        tanlangan_toifa = st.selectbox("Turkum bo'yicha saralash:", toifa_turlari)

    filtr_ombor = ombor.copy()
    if qidiruv_txt:
        filtr_ombor = filtr_ombor[filtr_ombor["Mahsulot Nomi"].str.lower().str.contains(qidiruv_txt.lower())]
    if tanlangan_toifa != "Barchasi":
        filtr_ombor = filtr_ombor[filtr_ombor["Kategoriya"] == tanlangan_toifa]

    if filtr_ombor.empty:
        st.info("Katalogda qidiruv bo'yicha mahsulot topilmadi.")
        return

    html_cards = '<div class="catalog-grid">'
    for idx, row in filtr_ombor.iterrows():
        rasm_src = row["Rasm"] if row["Rasm"] != "" else DEFAULT_PLACEHOLDER
        nomi = row["Mahsulot Nomi"]
        kat = row["Kategoriya"]
        miqdor = row["Miqdori"]
        birligi = row["O'lchov Birligi"]
        
        narx_str = format_money(row["Narxi"]) if admin_view else "Sotuvda"

        if miqdor <= 0:
            status_text = "Tugagan"
            status_bg = "#ef4444"
        elif miqdor <= 15:
            status_text = "Zaxira kam"
            status_bg = "#f59e0b"
        else:
            status_text = "Mavjud"
            status_bg = "#10b981"

        html_cards += f"""
        <div class="catalog-card">
            <div class="catalog-img-container">
                <span class="catalog-badge" style="background-color: {status_bg};">{status_text}</span>
                <img src="{rasm_src}" class="catalog-img" alt="{nomi}" />
            </div>
            <div style="padding: 18px; flex-grow: 1; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="font-size: 11px; color: #94a3b8; text-transform: uppercase; font-weight: 800; letter-spacing: 0.05em; margin-bottom: 4px;">{kat}</div>
                    <h3 style="font-size: 15px; font-weight: 700; color: #0f172a; margin: 0 0 10px 0; line-height: 1.4;">{nomi}</h3>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #f1f5f9; padding-top: 12px; margin-top: auto;">
                    <span style="font-size: 15px; font-weight: 800; color: #0d9488;">{narx_str}</span>
                    <span style="font-size: 12px; font-weight: 700; color: #475569; background: #e2e8f0; padding: 4px 8px; border-radius: 8px;">{miqdor:g} {birligi}</span>
                </div>
            </div>
        </div>
        """
    html_cards += '</div>'
    st.markdown(html_cards, unsafe_allow_html=True)

if menyu in ["🛍️ Yandex Katalog", "🛍️ Yandex Katalog (Agent)"]:
    mahsulot_katalogini_chizish(admin_view=administrator_tasdiq)

elif administrator_tasdiq and menyu == "📊 Boshqaruv Paneli":
    st.markdown("""
    <div class="floating-card">
        <h2 style="font-size: 26px; font-weight: 800; color: #0f172a; margin-bottom: 6px;">📊 Boshqaruv Dashboard</h2>
        <p style="font-size: 14px; color: #64748b; margin: 0;">Real vaqt rejimidagi umumiy hisob-kitoblar va oylik aylanma</p>
    </div>
    """, unsafe_allow_html=True)

    # Calculate KPIs
    jami_turlar = len(ombor)
    jami_dona = int(ombor["Miqdori"].sum()) if jami_turlar > 0 else 0
    jami_qiymat = (ombor["Miqdori"] * ombor["Narxi"]).sum() if jami_turlar > 0 else 0
    jami_agent_qarzlari = agentlar["Joriy Qarz"].sum() if not agentlar.empty else 0

    def kpi_card(title, value, subtitle, icon, icon_color, bg_gradient):
        return f"""
        <div class="floating-card" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0;">
            <div>
                <span style="font-size: 11px; font-weight: 800; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; display: block; margin-bottom: 6px;">{title}</span>
                <h3 style="font-size: 26px; font-weight: 800; color: #0f172a; margin: 0; letter-spacing: -0.02em;">{value}</h3>
                <span style="font-size: 12px; color: #64748b; display: block; margin-top: 8px;">{subtitle}</span>
            </div>
            <div style="background: {bg_gradient}; padding: 14px; border-radius: 18px; color: {icon_color}; font-size: 24px; display: flex; align-items: center; justify-content: center; width: 56px; height: 56px;">
                {icon}
            </div>
        </div>
        """

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(kpi_card("MAHSULOT TURLARI", f"{jami_turlar} xil", "Joriy turkumlar", "📦", "#0d9488", "linear-gradient(135deg, #ccfbf1 0%, #99f6e4 100%)"), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi_card("UMUMIY QOLDIQ", f"{jami_dona} dona", "Ombor hajmi", "📊", "#3b82f6", "linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%)"), unsafe_allow_html=True)
    with c3:
        st.markdown(kpi_card("OMBOR QIYMATI", format_money(jami_qiymat), "Sotuv bahosida", "💰", "#f59e0b", "linear-gradient(135deg, #fef3c7 0%, #fde68a 100%)"), unsafe_allow_html=True)
    with c4:
        st.markdown(kpi_card("AGENTLAR QARZI", format_money(jami_agent_qarzlari), "Yig'ilishi kerak", "👥", "#ef4444", "linear-gradient(135deg, #fee2e2 0%, #fca5a5 100%)"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    g1, g2 = st.columns([3, 2])
    with g1:
        st.markdown('<div class="floating-card"><h4>📈 Top 10 Mahsulot Qoldig\'i</h4>', unsafe_allow_html=True)
        if jami_turlar > 0:
            st.bar_chart(data=ombor.head(10), x="Mahsulot Nomi", y="Miqdori", color="#0d9488")
        st.markdown('</div>', unsafe_allow_html=True)
    with g2:
        st.markdown('<div class="floating-card"><h4>⚠️ Minimal Zaxira Ogohlantirishi</h4>', unsafe_allow_html=True)
        kam_qoldiq = ombor[ombor["Miqdori"] <= 15]
        if not kam_qoldiq.empty:
            for _, r in kam_qoldiq.iterrows():
                st.markdown(f"""
                <div style="background: #fffbeb; border: 1px solid #fef3c7; border-left: 5px solid #f59e0b; padding: 12px 15px; border-radius: 12px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: #92400e; font-weight: 700; font-size: 13px;">🚨 {r['Mahsulot Nomi']}</span>
                    <span style="background: #f59e0b; color: white; padding: 4px 10px; border-radius: 8px; font-weight: 800; font-size: 11px;">{r['Miqdori']:g} {r['O\'lchov Birligi']}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("Zaxira yetarli darajada xavfsiz!")
        st.markdown('</div>', unsafe_allow_html=True)

elif administrator_tasdiq and menyu == "📦 Mahsulotlar Qoldig'i":
    st.markdown("""
    <div class="floating-card">
        <h2 style="font-size: 26px; font-weight: 800; color: #0f172a; margin-bottom: 6px;">📦 Mahsulotlar Balansi & Rasmlar</h2>
        <p style="font-size: 14px; color: #64748b; margin: 0;">Mavjud tovarlar ro'yxati hamda ularning rasmlarini tahrirlash</p>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("🖼️ Mahsulot rasmiga o'zgartirish kiritish"):
        if not ombor.empty:
            tanlangan_prod = st.selectbox("Mahsulotni tanlang:", ombor["Mahsulot Nomi"].unique())
            yangi_rasm_fayl = st.file_uploader("Yangi rasm yuklang (PNG, JPG, JPEG):", type=["png", "jpg", "jpeg"], key="edit_img_u")
            if st.button("Rasmni saqlash"):
                if yangi_rasm_fayl:
                    b64_str = to_base64(yangi_rasm_fayl)
                    ombor.loc[ombor["Mahsulot Nomi"] == tanlangan_prod, "Rasm"] = b64_str
                    bazani_saqlash(ombor, kirim, chiqim, agentlar)
                    st.success(f"✅ '{tanlangan_prod}' rasmi muvaffaqiyatli yuklandi!")
                    st.rerun()

    html_table = """
    <div class="modern-table-container">
        <table class="modern-table">
            <thead>
                <tr>
                    <th>Turkum</th>
                    <th>Mahsulot Nomi</th>
                    <th>Zaxira Qoldig'i</th>
                    <th>Narxi (UZS)</th>
                </tr>
            </thead>
            <tbody>
    """
    for idx, row in ombor.iterrows():
        html_table += f"""
                <tr>
                    <td><span style="background: #f1f5f9; padding: 4px 10px; border-radius: 8px; font-weight: 700; font-size: 12px; color: #475569;">{row['Kategoriya']}</span></td>
                    <td style="font-weight: 700; color: #0f172a;">{row['Mahsulot Nomi']}</td>
                    <td style="font-weight: 800; color: {'#ef4444' if row['Miqdori'] <= 15 else '#10b981'};">{row['Miqdori']:g} {row['O\'lchov Birligi']}</td>
                    <td style="font-weight: 700; color: #0d9488;">{format_money(row['Narxi'])}</td>
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
    <div class="floating-card">
        <h2 style="font-size: 26px; font-weight: 800; color: #0f172a; margin-bottom: 6px;">👥 Agentlar va To'lovlar Tizimi</h2>
        <p style="font-size: 14px; color: #64748b; margin: 0;">Agentlar joriy hisob-kitob balansi hamda qarz yopish operatsiyalari</p>
    </div>
    """, unsafe_allow_html=True)

    t1, t2 = st.tabs(["👥 Agentlar Ro'yxati", "➕ Yangi Agent & To'lov Qabul Qilish"])
    
    with t1:
        if not agentlar.empty:
            agent_html = '<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px;">'
            for _, r in agentlar.iterrows():
                qarz_rang = '#ef4444' if r['Joriy Qarz'] > 0 else '#10b981'
                qarz_bg = '#fef2f2' if r['Joriy Qarz'] > 0 else '#ecfdf5'
                agent_html += f"""
                <div class="floating-card" style="margin-bottom: 0;">
                    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 14px;">
                        <div style="background: #ccfbf1; color: #0d9488; width: 44px; height: 44px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 16px;">
                            {r['Agent Nomi'][0]}
                        </div>
                        <div>
                            <h4 style="margin: 0; color: #0f172a; font-size: 16px; font-weight: 800;">{r['Agent Nomi']}</h4>
                            <span style="font-size: 11px; color: #64748b; font-weight: 600;">👤 Agent</span>
                        </div>
                    </div>
                    <div style="font-size: 13px; color: #475569; margin-bottom: 16px;">
                        📞 Tel: <strong>{r['Telefon']}</strong>
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
            st.info("Hozircha hech qanday agent mavjud emas.")

    with t2:
        col_ag, col_tol = st.columns(2)
        with col_ag:
            st.markdown('<div class="floating-card"><h4>👥 Yangi Agent qo\'shish</h4>', unsafe_allow_html=True)
            with st.form("agent_add_form_new"):
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

        with col_tol:
            st.markdown('<div class="floating-card"><h4>💰 Qarzni yopish (To\'lov qabul qilish)</h4>', unsafe_allow_html=True)
            if not agentlar.empty:
                with st.form("qarz_yopish_form_new"):
                    t_agent = st.selectbox("Agentni tanlang:", agentlar["Agent Nomi"].unique())
                    summa = st.number_input("To'lov Summasi:", min_value=1000.0, step=50000.0)
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
                        st.success(f"✅ Muvaffaqiyatli qarz to'lovi qabul qilindi!")
                        st.rerun()

elif administrator_tasdiq and menyu == "📥 Yangi Kirim":
    st.markdown("""
    <div class="floating-card">
        <h2 style="font-size: 26px; font-weight: 800; color: #0f172a; margin-bottom: 6px;">📥 Yangi Kirim Operatsiyasi</h2>
        <p style="font-size: 14px; color: #64748b; margin: 0;">Omborxonaga yangi yoki mavjud tovarlarni qabul qilish</p>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        kirim_shakli = st.radio("Kirim shakli:", ["Mavjud mahsulot qoldig'ini oshirish", "Yangi mahsulot yaratish"])
        
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
                st.success(f"✅ Muvaffaqiyatli: {miqdor} {birligi} '{nomi}' qabul qilindi!")
                st.rerun()

elif administrator_tasdiq and menyu == "📤 Yangi Chiqim":
    st.markdown("""
    <div class="floating-card">
        <h2 style="font-size: 26px; font-weight: 800; color: #0f172a; margin-bottom: 6px;">📤 Ombardan Mahsulot Chiqim Qilish</h2>
        <p style="font-size: 14px; color: #64748b; margin: 0;">Agentlarga mahsulot yuklash yoki naqd savdo operatsiyalari</p>
    </div>
    """, unsafe_allow_html=True)

    if ombor.empty:
        st.warning("Omborda mahsulotlar mavjud emas.")
    else:
        with st.container():
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
                    st.success(f"✅ Chiqim muvaffaqiyatli amalga oshirildi! Jami: {format_money(jami)}")
                    st.rerun()

elif administrator_tasdiq and menyu == "🕒 Amallar Tarixi":
    st.markdown("""
    <div class="floating-card">
        <h2 style="font-size: 26px; font-weight: 800; color: #0f172a; margin-bottom: 6px;">🕒 Ombor Harakatlari Jurnali</h2>
        <p style="font-size: 14px; color: #64748b; margin: 0;">Tizimdagi barcha kirim va chiqim operatsiyalarining xronologiyasi</p>
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
            st.info("Hozircha kirim qilinmagan.")

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
                            <td><span style="background: #e0f2fe; color: #0369a1; padding: 4px 10px; border-radius: 8px; font-weight: 700; font-size: 12px;">{r['Agent']}</span></td>
                            <td style="font-weight: 700; color: #0d9488;">{summa_str}</td>
                        </tr>
                """
            html_chiqim += """
                    </tbody>
                </table>
            </div>
            """
            st.markdown(html_chiqim, unsafe_allow_html=True)
        else:
            st.info("Hozircha chiqim qilinmagan.")
