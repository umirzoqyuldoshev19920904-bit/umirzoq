import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Sahifaning eng yuqori darajali sozlamalari (Premium ko'rinish uchun)
st.set_page_config(
    page_title="Smart-Ombor Pro ERP v2.0",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium CSS - Standart Streamlit dizaynini o'chirib, yuqori darajadagi SaaS dizaynni yaratish
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    /* Umumiy fon va matnlar */
    .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background-color: #f8fafc !important;
    }
    
    /* Sidebar fonini va elementlarini butunlay o'zgartirish */
    [data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid #1e293b;
    }
    [data-testid="stSidebar"] * {
        color: #f1f5f9 !important;
    }
    
    /* Sidebar ichidagi Radio navigatsiya menyusini zamonaviy tugmalarga aylantirish */
    div[data-testid="stSidebarUserContent"] div[role="radiogroup"] {
        gap: 10px !important;
    }
    div[data-testid="stSidebarUserContent"] div[role="radiogroup"] label {
        background-color: #1e293b !important;
        color: #94a3b8 !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        border: 1px solid #334155 !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        width: 100% !important;
        display: flex !important;
        align-items: center !important;
    }
    div[data-testid="stSidebarUserContent"] div[role="radiogroup"] label[data-checked="true"] {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
        color: white !important;
        border-color: #6366f1 !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.35) !important;
        transform: translateY(-1px);
    }
    div[data-testid="stSidebarUserContent"] div[role="radiogroup"] label:hover {
        background-color: #334155 !important;
        color: #f1f5f9 !important;
        transform: translateX(4px);
    }
    /* Radio aylanachalarini yashirish */
    div[data-testid="stSidebarUserContent"] div[role="radiogroup"] label div[role="presentation"] {
        display: none !important;
    }
    div[data-testid="stSidebarUserContent"] div[role="radiogroup"] label [data-testid="stWidgetLabel"] {
        margin-left: 0px !important;
    }

    /* Asosiy Premium tugmalar */
    div.stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
        color: white !important;
        border-radius: 14px !important;
        border: none !important;
        padding: 12px 24px !important;
        font-weight: 700 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2) !important;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #4f46e5 0%, #3730a3 100%) !important;
        box-shadow: 0 10px 20px rgba(79, 70, 229, 0.4) !important;
        transform: translateY(-2px);
    }
    
    /* Oq rangli kartalar va vizual joziba */
    .premium-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        padding: 24px;
        border-radius: 20px;
        border: 1px solid rgba(226, 232, 240, 0.8);
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.03);
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    .premium-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 20px 35px -5px rgba(0, 0, 0, 0.08);
    }
</style>
""", unsafe_allow_html=True)

FAYL_OMBOR = "onlayn_ombor.xlsx"

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
            
            ombor_df["Miqdori"] = pd.to_numeric(ombor_df["Miqdori"], errors='coerce').fillna(0)
            if "Narxi" not in ombor_df.columns:
                ombor_df["Narxi"] = 10000.0
            if "Kategoriya" not in ombor_df.columns:
                ombor_df["Kategoriya"] = "Boshqa"
                
            ombor_df["Narxi"] = pd.to_numeric(ombor_df["Narxi"], errors='coerce').fillna(10000.0)
            kirim_df["Miqdori"] = pd.to_numeric(kirim_df["Miqdori"], errors='coerce').fillna(0)
            chiqim_df["Miqdori"] = pd.to_numeric(chiqim_df["Miqdori"], errors='coerce').fillna(0)
            agent_df["Joriy Qarz"] = pd.to_numeric(agent_df["Joriy Qarz"], errors='coerce').fillna(0)
            
            return ombor_df, kirim_df, chiqim_df, agent_df
        except Exception as e:
            st.error(f"Baza yuklanishida xatolik yuz berdi: {e}. Yangi baza tuzilmoqda...")
            
    ombor_df = pd.DataFrame(columns=["Mahsulot Nomi", "Miqdori", "O'lchov Birligi", "Narxi", "Kategoriya"])
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

def kpi_card(title, value, subtitle, icon, icon_color, bg_gradient):
    """Premium KPI kartasini chizib beruvchi vizual HTML blok."""
    return f"""
    <div style="
        background: white;
        padding: 24px;
        border-radius: 20px;
        border: 1px solid #f1f5f9;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.02), 0 4px 6px -4px rgba(0, 0, 0, 0.02);
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
        transition: all 0.3s ease;
    ">
        <div>
            <span style="font-size: 11px; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.08em; display: block; margin-bottom: 6px;">{title}</span>
            <h3 style="font-size: 26px; font-weight: 800; color: #0f172a; margin: 0; line-height: 1.1;">{value}</h3>
            <span style="font-size: 12px; font-weight: 500; color: #64748b; display: flex; align-items: center; gap: 4px; margin-top: 8px;">
                {subtitle}
            </span>
        </div>
        <div style="background: {bg_gradient}; padding: 14px; border-radius: 16px; color: {icon_color}; display: flex; align-items: center; justify-content: center; font-size: 26px; width: 56px; height: 56px; box-shadow: 0 8px 16px -4px rgba(0,0,0,0.1);">
            {icon}
        </div>
    </div>
    """

def format_money(amount):
    return f"{amount:,.0f} UZS".replace(",", " ")

# Sidebar Brending va sarlavha
st.sidebar.markdown("""
<div style="display: flex; align-items: center; gap: 14px; padding: 15px 0 30px 0; border-bottom: 1px solid #1e293b; margin-bottom: 25px;">
    <div style="background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%); padding: 12px; border-radius: 14px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);">
        <span style="font-size: 22px;">⚡</span>
    </div>
    <div>
        <h2 style="font-size: 18px; font-weight: 800; color: white; margin: 0; padding: 0; letter-spacing: -0.02em;">Smart-Ombor ERP</h2>
        <span style="font-size: 10px; color: #818cf8; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em;">Professional v2.0</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Kirish Rolini boshqarish va tanlash
rol = st.sidebar.radio("🔑 TIZIMGA KIRISH REJIMI", ["👤 Agent Rejimi", "🔐 Admin Rejimi"])

administrator_tasdiq = False

if rol == "🔐 Admin Rejimi":
    st.sidebar.markdown("<div style='margin-top:-15px; margin-bottom:15px;'></div>", unsafe_allow_html=True)
    parol = st.sidebar.text_input("Maxfiy parolni kiriting:", type="password")
    if parol == "19920904":
        administrator_tasdiq = True
        st.sidebar.success("🔓 Kirish muvaffaqiyatli!")
    else:
        if parol != "":
            st.sidebar.error("❌ Maxfiy parol noto'g'ri!")
        st.sidebar.info("Agent rejimidan foydalanish uchun yuqoridagi 'Agent Rejimi' tugmasini bosing.")

# Rolga qarab navigatsiyani chiqarish
if administrator_tasdiq:
    menyu = st.sidebar.radio(
        "ASOSIY BO'LIMLAR",
        ["📊 Boshqaruv Paneli", "📦 Mahsulotlar Qoldig'i", "👥 Agentlar & Qarzdorlik", "📥 Yangi Kirim", "📤 Yangi Chiqim", "🕒 Amallar Tarixi"]
    )
else:
    menyu = "📦 Mahsulotlar Qoldig'i (Agent Rejimi)"
    st.sidebar.markdown("""
    <div style="padding: 18px; background: rgba(30, 41, 59, 0.5); border: 1px solid #334155; border-radius: 14px; margin-top: 25px;">
        <p style="font-size: 12px; color: #94a3b8; margin: 0; line-height: 1.5;">Siz hozirda <b>Agent Rejimidasiz</b>. Sizga faqat joriy ombor qoldig'i ma'lumotlari narxlarsiz ko'rinadi.</p>
    </div>
    """, unsafe_allow_html=True)

if administrator_tasdiq and menyu == "📊 Boshqaruv Paneli":
    st.markdown("""
    <div style="margin-bottom: 30px;">
        <h1 style="font-size: 32px; font-weight: 800; color: #0f172a; margin-bottom: 6px; letter-spacing: -0.03em;">📊 Boshqaruv va Tahliliy Panel</h1>
        <p style="font-size: 15px; color: #64748b; margin: 0;">Omborxonaning real vaqt rejimida moliyaviy aylanmasi va zaxira ko'rsatkichlari</p>
    </div>
    """, unsafe_allow_html=True)
    
    # KPIs Hisob-kitobi
    jami_turlar = len(ombor)
    jami_dona = int(ombor["Miqdori"].sum()) if jami_turlar > 0 else 0
    jami_qiymat = (ombor["Miqdori"] * ombor["Narxi"]).sum() if jami_turlar > 0 else 0
    jami_agent_qarzlari = agentlar["Joriy Qarz"].sum() if not agentlar.empty else 0
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(kpi_card("Faol Mahsulotlar", f"{jami_turlar} xil", "Mavjud tovar turlari", "📦", "#4f46e5", "linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%)"), unsafe_allow_html=True)
    with col2:
        st.markdown(kpi_card("Umumiy Zaxira", f"{jami_dona} dona", "Barcha qoldiq miqdori", "📊", "#10b981", "linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%)"), unsafe_allow_html=True)
    with col3:
        st.markdown(kpi_card("Ombor Umumiy Qiymati", format_money(jami_qiymat), "Mavjud tovar pul summasi", "💰", "#f59e0b", "linear-gradient(135deg, #fef3c7 0%, #fde68a 100%)"), unsafe_allow_html=True)
    with col4:
        st.markdown(kpi_card("Yig'iladigan Qarzlar", format_money(jami_agent_qarzlari), "Agentlarning umumiy qarzi", "👥", "#ef4444", "linear-gradient(135deg, #fee2e2 0%, #fca5a5 100%)"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    g_col1, g_col2 = st.columns([3, 2])
    
    with g_col1:
        st.markdown("""
        <div class="premium-card">
            <h4 style="margin: 0 0 20px 0; font-size: 18px; font-weight: 700; color: #0f172a; display: flex; align-items: center; gap: 10px;">
                <span style="background: #e0e7ff; padding: 6px; border-radius: 8px; font-size: 16px;">📈</span> Mahsulotlar Miqdori Top-10 Tahlili
            </h4>
        </div>
        """, unsafe_allow_html=True)
        if jami_turlar > 0:
            saralangan_ombor = ombor.sort_values(by="Miqdori", ascending=False).head(10)
            st.bar_chart(data=saralangan_ombor, x="Mahsulot Nomi", y="Miqdori", color="#6366f1")
        else:
            st.info("Omborda grafik ko'rsatish uchun mahsulotlar yetarli emas.")
            
    with g_col2:
        st.markdown("""
        <div class="premium-card" style="height: 100%;">
            <h4 style="margin: 0 0 20px 0; font-size: 18px; font-weight: 700; color: #ef4444; display: flex; align-items: center; gap: 10px;">
                <span style="background: #fee2e2; padding: 6px; border-radius: 8px; font-size: 16px;">⚠️</span> Zaxirasi Kamaygan Mahsulotlar
            </h4>
        </div>
        """, unsafe_allow_html=True)
        
        kam_qoldiq = ombor[ombor["Miqdori"] <= 15]
        if not kam_qoldiq.empty:
            for index, row in kam_qoldiq.iterrows():
                nomi = row["Mahsulot Nomi"]
                miqdori = row["Miqdori"]
                birligi = row["O'lchov Birligi"]
                
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; align-items: center; padding: 14px; background-color: #fef2f2; border-radius: 12px; margin-bottom: 10px; border: 1px solid #fee2e2; transition: all 0.2s;">
                    <div>
                        <b style="color: #991b1b; font-size: 14px;">{nomi}</b>
                        <div style="font-size: 11px; color: #b91c1c; margin-top: 2px;">Tugash arafasida turibdi</div>
                    </div>
                    <span style="background-color: #fca5a5; color: #7f1d1d; padding: 6px 12px; border-radius: 10px; font-size: 12px; font-weight: 800;">
                        {miqdori} {birligi}
                    </span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align: center; padding: 60px 20px; color: #10b981;">
                <span style="font-size: 48px;">✨</span>
                <p style="margin-top: 15px; font-size: 14px; font-weight: 700; color: #047857;">Hamma mahsulotlar zaxirasi yetarli darajada!</p>
            </div>
            """, unsafe_allow_html=True)

elif administrator_tasdiq and menyu == "📦 Mahsulotlar Qoldig'i":
    st.markdown("""
    <div style="margin-bottom: 30px;">
        <h1 style="font-size: 32px; font-weight: 800; color: #0f172a; margin-bottom: 6px; letter-spacing: -0.03em;">📦 Mavjud Mahsulotlar Ro'yxati</h1>
        <p style="font-size: 15px; color: #64748b; margin: 0;">Barcha mahsulotlar, ularning narxi, miqdori va umumiy moliyaviy qiymati</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Qidiruv va filtrlar
    with st.container(border=True):
        q_col1, q_col2 = st.columns([3, 1])
        with q_col1:
            qidiruv = st.text_input("🔍 Mahsulot nomi bo'yicha tezkor qidiruv...", placeholder="Masalan: Armatura")
        with q_col2:
            kat_turlari = ["Barchasi"] + list(ombor["Kategoriya"].unique()) if not ombor.empty else ["Barchasi"]
            kategoriya_tanlash = st.selectbox("Turkum bo'yicha saralash:", kat_turlari)
        
    if not ombor.empty:
        filtr_ombor = ombor.copy()
        if qidiruv:
            filtr_ombor = filtr_ombor[filtr_ombor["Mahsulot Nomi"].str.lower().str.contains(qidiruv.lower())]
        if kategoriya_tanlash != "Barchasi":
            filtr_ombor = filtr_ombor[filtr_ombor["Kategoriya"] == kategoriya_tanlash]
            
        # Ma'lumotlarni formatlash va jami qiymatni hisoblash
        korish_df = filtr_ombor.copy()
        korish_df["Jami Qiymat (UZS)"] = korish_df["Miqdori"] * korish_df["Narxi"]
        
        # Pullarni formatlash
        korish_df["Sotish Narxi"] = korish_df["Narxi"].apply(format_money)
        korish_df["Jami Qiymati"] = korish_df["Jami Qiymat (UZS)"].apply(format_money)
        
        st.dataframe(
            korish_df[["Kategoriya", "Mahsulot Nomi", "Miqdori", "O'lchov Birligi", "Sotish Narxi", "Jami Qiymati"]],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.warning("Omboringizda hali hech qanday mahsulot mavjud emas.")

elif menyu == "📦 Mahsulotlar Qoldig'i (Agent Rejimi)":
    st.markdown("""
    <div style="margin-bottom: 30px;">
        <h1 style="font-size: 32px; font-weight: 800; color: #4f46e5; margin-bottom: 6px; letter-spacing: -0.03em;">📦 Ombordagi Mahsulotlar Qoldig'i</h1>
        <p style="font-size: 15px; color: #64748b; margin: 0;">Real vaqtda omborda sotuvga tayyor bo'lgan mahsulotlar va ularning miqdori (Agentlar uchun)</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container(border=True):
        qidiruv_agent = st.text_input("🔍 Kerakli mahsulot nomini yozib qidiring...", placeholder="Masalan: Kabel, Armatura...")
    
    if not ombor.empty:
        filtr_agent = ombor.copy()
        if qidiruv_agent:
            filtr_agent = filtr_agent[filtr_agent["Mahsulot Nomi"].str.lower().str.contains(qidiruv_agent.lower())]
            
        # Status ustuni qo'shish
        def status_belgilash(qty):
            if qty <= 0:
                return "❌ Tugagan"
            elif qty <= 15:
                return "⚠️ Zaxira kam"
            else:
                return "✅ Sotuvda mavjud"
                
        filtr_agent["Zaxira Holati"] = filtr_agent["Miqdori"].apply(status_belgilash)
        
        # Agentlarga narxlar mutlaqo ko'rsatilmadi
        st.dataframe(
            filtr_agent[["Kategoriya", "Mahsulot Nomi", "Miqdori", "O'lchov Birligi", "Zaxira Holati"]],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Hozirda omborda mahsulot qoldig'i mavjud emas.")

elif administrator_tasdiq and menyu == "👥 Agentlar & Qarzdorlik":
    st.markdown("""
    <div style="margin-bottom: 30px;">
        <h1 style="font-size: 32px; font-weight: 800; color: #0f172a; margin-bottom: 6px; letter-spacing: -0.03em;">👥 Agentlar Tizimi va Qarzdorlik</h1>
        <p style="font-size: 15px; color: #64748b; margin: 0;">Olib ketilgan mahsulotlar uchun hisob-kitoblar, qarzlar tahlili va to'lovlarni boshqarish bo'limi</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["💰 Agentlar Ro'yxati & Qarzlar", "➕ Yangi Agent Qo'shish & To'lov Yopish"])
    
    with tab1:
        if not agentlar.empty:
            for idx, row in agentlar.iterrows():
                f_qarz = format_money(row["Joriy Qarz"])
                st.markdown(f"""
                <div class="premium-card" style="border-left: 6px solid {'#ef4444' if row['Joriy Qarz'] > 0 else '#10b981'};">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
                        <div>
                            <h4 style="margin: 0; font-size: 20px; font-weight: 800; color: #1e293b;">👤 {row['Agent Nomi']}</h4>
                            <p style="margin: 6px 0 0 0; font-size: 13px; color: #64748b; display: flex; align-items: center; gap: 6px;">
                                <span style="font-size: 14px;">📞</span> {row['Telefon']}
                            </p>
                        </div>
                        <div style="text-align: right;">
                            <span style="font-size: 11px; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em;">Mavjud Qarz:</span>
                            <h3 style="margin: 4px 0 0 0; font-size: 22px; font-weight: 800; color: {'#ef4444' if row['Joriy Qarz'] > 0 else '#10b981'};">{f_qarz}</h3>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Hozircha tizimda hech qanday agent qo'shilmagan.")
            
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### ➕ Yangi Agent Ro'yxatdan O'tkazish")
            with st.form("yangi_agent_form"):
                y_agent_nomi = st.text_input("Agent ismi va familiyasi:").strip().capitalize()
                y_agent_tel = st.text_input("Telefon raqami:", placeholder="+998 90 123-45-67")
                bosh_qarz = st.number_input("Boshlang'ich qarz miqdori (agar bo'lsa):", min_value=0.0, step=50000.0)
                
                agent_submit = st.form_submit_button("Agentni saqlash")
                if agent_submit:
                    if y_agent_nomi:
                        if y_agent_nomi in agentlar["Agent Nomi"].values:
                            st.error("Bunday agent allaqachon ro'yxatdan o'tgan!")
                        else:
                            yangi_qator = pd.DataFrame([{"Agent Nomi": y_agent_nomi, "Telefon": y_agent_tel, "Joriy Qarz": bosh_qarz}])
                            agentlar = pd.concat([agentlar, yangi_qator], ignore_index=True)
                            bazani_saqlash(ombor, kirim, chiqim, agentlar)
                            st.success(f"✅ {y_agent_nomi} muvaffaqiyatli agent sifatida qo'shildi!")
                            st.rerun()
                    else:
                        st.error("Agent ismini kiritishingiz shart!")
                        
        with col2:
            st.markdown("##### 💵 Agent Qarzini Yopish (To'lov Qabul Qilish)")
            if not agentlar.empty:
                with st.form("qarz_yopish_form"):
                    t_agent = st.selectbox("To'lov qilayotgan agentni tanlang:", agentlar["Agent Nomi"].unique())
                    tolov_summasi = st.number_input("To'lov summasi (UZS):", min_value=1000.0, step=50000.0)
                    izoh_tolov = st.text_input("To'lov usuli / Izoh:", placeholder="Masalan: Plastik karta, naqd va hk")
                    
                    tolov_submit = st.form_submit_button("To'lovni tasdiqlash")
                    if tolov_submit:
                        agentlar.loc[agentlar["Agent Nomi"] == t_agent, "Joriy Qarz"] -= tolov_summasi
                        
                        # To'lov qaydini chiqim/tarixlar bo'limiga salbiy summa qilib saqlaymiz
                        sana = datetime.now().strftime("%Y-%m-%d %H:%M")
                        yangi_qayd = pd.DataFrame([{
                            "Sana": sana, "Mahsulot Nomi": "Qarz To'lovi", "Miqdori": 0,
                            "Qabul qiluvchi": t_agent, "Agent": t_agent, "Chiqim Turi": f"Qarz To'lovi ({izoh_tolov})", "Jami Summa": -tolov_summasi
                        }])
                        chiqim = pd.concat([chiqim, yangi_qayd], ignore_index=True)
                        
                        bazani_saqlash(ombor, kirim, chiqim, agentlar)
                        st.success(f"✅ Muvaffaqiyatli: {t_agent} hisobidan {format_money(tolov_summasi)} qabul qilindi!")
                        st.rerun()
            else:
                st.info("To'lovni amalga oshirish uchun avval agent yaratishingiz kerak.")

elif administrator_tasdiq and menyu == "📥 Yangi Kirim":
    st.markdown("""
    <div style="margin-bottom: 30px;">
        <h1 style="font-size: 32px; font-weight: 800; color: #10b981; margin-bottom: 6px; letter-spacing: -0.03em;">📥 Yangi Kirim Amali</h1>
        <p style="font-size: 15px; color: #64748b; margin: 0;">Omborxonaga yangi yoki mavjud tovarlarni tezda qabul qilib zaxirani to'ldirish</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            kirim_turi = st.radio("Kirim shaklini tanlang:", ["Mavjud mahsulotni ko'paytirish", "Yangi mahsulot yaratish"])
            
            if kirim_turi == "Mavjud mahsulotni ko'paytirish" and not ombor.empty:
                nomi = st.selectbox("Mavjud mahsulotlardan tanlang:", ombor["Mahsulot Nomi"].unique())
                birligi = ombor.loc[ombor["Mahsulot Nomi"] == nomi, "O'lchov Birligi"].values[0]
                kategoriya = ombor.loc[ombor["Mahsulot Nomi"] == nomi, "Kategoriya"].values[0]
                narx_bosh = float(ombor.loc[ombor["Mahsulot Nomi"] == nomi, "Narxi"].values[0])
            else:
                nomi = st.text_input("Yangi mahsulot nomi:", placeholder="Masalan: Armatura A500C 16mm").strip().capitalize()
                kategoriya = st.selectbox("Kategoriya / Turkum:", ["Qurilish materiallari", "Elektrotexnika", "Santexnika", "Asbob-uskunalar", "Boshqa"])
                birligi = st.selectbox("O'lchov birligi:", ["dona", "kg", "litr", "metr", "qop", "quti"])
                narx_bosh = 10000.0

        with col2:
            miqdori = st.number_input("Kirim qilinayotgan miqdor:", min_value=0.1, value=1.0, step=1.0)
            narxi = st.number_input("Sotib olish narxi (UZS):", min_value=0.0, value=narx_bosh, step=1000.0)
            masul = st.text_input("Qabul qilib olgan mas'ul shaxs:", value="Karim Umirzoq").strip().capitalize()
            
        submit = st.button("📥 Kirim amalini tasdiqlash va omborga yozish")
        
        if submit:
            if nomi and masul:
                # Omborni yangilash
                if nomi in ombor["Mahsulot Nomi"].values:
                    ombor.loc[ombor["Mahsulot Nomi"] == nomi, "Miqdori"] += miqdori
                    ombor.loc[ombor["Mahsulot Nomi"] == nomi, "Narxi"] = narxi
                else:
                    yangi_qator = pd.DataFrame([{"Mahsulot Nomi": nomi, "Miqdori": miqdori, "O'lchov Birligi": birligi, "Narxi": narxi, "Kategoriya": kategoriya}])
                    ombor = pd.concat([ombor, yangi_qator], ignore_index=True)
                
                # Kirim tarixiga qo'shish
                sana = datetime.now().strftime("%Y-%m-%d %H:%M")
                yangi_kirim = pd.DataFrame([{"Sana": sana, "Mahsulot Nomi": nomi, "Miqdori": miqdori, "Mas'ul": masul}])
                kirim = pd.concat([kirim, yangi_kirim], ignore_index=True)
                
                bazani_saqlash(ombor, kirim, chiqim, agentlar)
                st.success(f"✅ Muvaffaqiyatli: {miqdori} {birligi} '{nomi}' omborga qabul qilindi!")
                st.balloons()
                st.rerun()
            else:
                st.error("Iltimos, barcha zaruriy maydonlarni to'ldiring!")

elif administrator_tasdiq and menyu == "📤 Yangi Chiqim":
    st.markdown("""
    <div style="margin-bottom: 30px;">
        <h1 style="font-size: 32px; font-weight: 800; color: #f43f5e; margin-bottom: 6px; letter-spacing: -0.03em;">📤 Yangi Chiqim Amali</h1>
        <p style="font-size: 15px; color: #64748b; margin: 0;">Ombordan mahsulot chiqim qilish, sotish yoki agentlar hisobiga qarz qilib rasmiylashtirish</p>
    </div>
    """, unsafe_allow_html=True)
    
    if ombor.empty:
        st.warning("Omborda mahsulot mavjud emas, avval kirim qiling!")
    else:
        with st.container(border=True):
            col1, col2 = st.columns(2)
            
            with col1:
                nomi = st.selectbox("Chiqim qilinadigan mahsulot:", ombor["Mahsulot Nomi"].unique())
                qoldiq = ombor.loc[ombor["Mahsulot Nomi"] == nomi, "Miqdori"].values[0]
                birligi = ombor.loc[ombor["Mahsulot Nomi"] == nomi, "O'lchov Birligi"].values[0]
                narxi = ombor.loc[ombor["Mahsulot Nomi"] == nomi, "Narxi"].values[0]
                
                st.markdown(f"""
                <div style="padding: 12px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; margin-bottom: 15px;">
                    <span style="font-size: 12px; font-weight:700; color: #64748b; text-transform: uppercase;">Mavjud zaxira:</span>
                    <h4 style="margin: 2px 0 0 0; color:#0f172a; font-weight:800;">{qoldiq} {birligi} | Sotish: {format_money(narxi)}</h4>
                </div>
                """, unsafe_allow_html=True)
                
                chiqim_turi = st.radio("Chiqim shartini tanlang:", ["Naqd/Plastik sotuv", "Agentga qarz hisobiga yuklash"])
                
            with col2:
                miqdori = st.number_input("Chiqim qilinadigan miqdor:", min_value=0.1, max_value=float(qoldiq), value=1.0, step=1.0)
                
                if chiqim_turi == "Agentga qarz hisobiga yuklash":
                    if not agentlar.empty:
                        tanlangan_agent = st.selectbox("Mahsulotni yuklab oluvchi agentni tanlang:", agentlar["Agent Nomi"].unique())
                        qabul_qiluvchi = tanlangan_agent
                    else:
                        st.error("Hech qanday ro'yxatga olingan agent topilmadi. Avval agent yarating.")
                        tanlangan_agent = "Noma'lum"
                        qabul_qiluvchi = "Noma'lum"
                else:
                    tanlangan_agent = "Yo'q (Naqd Sotuv)"
                    qabul_qiluvchi = st.text_input("Qabul qiluvchi shaxs/tashkilot nomi:", placeholder="Masalan: G'isht zavod binosi")
                    
            submit = st.button("📤 Chiqimni rasmiylashtirish va tasdiqlash")
            
            if submit:
                if qabul_qiluvchi:
                    jami_summa = miqdori * narxi
                    
                    # Ombordagi qoldiqni kamaytirish
                    ombor.loc[ombor["Mahsulot Nomi"] == nomi, "Miqdori"] -= miqdori
                    
                    # Agent qarzini ko'paytirish
                    if chiqim_turi == "Agentga qarz hisobiga yuklash" and tanlangan_agent != "Noma'lum":
                        agentlar.loc[agentlar["Agent Nomi"] == tanlangan_agent, "Joriy Qarz"] += jami_summa
                        
                    # Chiqim tarixiga yozish
                    sana = datetime.now().strftime("%Y-%m-%d %H:%M")
                    yangi_chiqim = pd.DataFrame([{
                        "Sana": sana, "Mahsulot Nomi": nomi, "Miqdori": miqdori,
                        "Qabul qiluvchi": qabul_qiluvchi, "Agent": tanlangan_agent,
                        "Chiqim Turi": chiqim_turi, "Jami Summa": jami_summa
                    }])
                    chiqim = pd.concat([chiqim, yangi_chiqim], ignore_index=True)
                    
                    bazani_saqlash(ombor, kirim, chiqim, agentlar)
                    st.success(f"✅ Muvaffaqiyatli: {miqdori} {birligi} '{nomi}' muvaffaqiyatli topshirildi. Jami qiymat: {format_money(jami_summa)}")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("Iltimos, barcha zaruriy ma'lumotlarni to'ldiring!")

elif administrator_tasdiq and menyu == "🕒 Amallar Tarixi":
    st.markdown("""
    <div style="margin-bottom: 30px;">
        <h1 style="font-size: 32px; font-weight: 800; color: #0f172a; margin-bottom: 6px; letter-spacing: -0.03em;">🕒 Ombor Harakatlari Jurnali</h1>
        <p style="font-size: 15px; color: #64748b; margin: 0;">Barcha kirish va chiqish amallarining batafsil yozib borilgan jurnali</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📥 Barcha Kirimlar", "📤 Barcha Chiqimlar"])
    
    with tab1:
        if not kirim.empty:
            st.dataframe(kirim.sort_values(by="Sana", ascending=False), use_container_width=True, hide_index=True)
        else:
            st.info("Kirimlar jurnali hozircha bo'sh.")
            
    with tab2:
        if not chiqim.empty:
            chiqim_ko_df = chiqim.copy()
            if "Jami Summa" in chiqim_ko_df.columns:
                # To'lovlarni salbiy qiymatini chiroyli formatlash
                chiqim_ko_df["Jami Summa (UZS)"] = chiqim_ko_df["Jami Summa"].apply(format_money)
                st.dataframe(
                    chiqim_ko_df[["Sana", "Mahsulot Nomi", "Miqdori", "Qabul qiluvchi", "Agent", "Chiqim Turi", "Jami Summa (UZS)"]].sort_values(by="Sana", ascending=False),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.dataframe(chiqim_ko_df.sort_values(by="Sana", ascending=False), use_container_width=True, hide_index=True)
        else:
            st.info("Chiqimlar jurnali hozircha bo'sh.")
