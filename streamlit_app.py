import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Sahifa asosiy sozlamalari
st.set_page_config(
    page_title="Smart-Ombor Pro ERP",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght=300;400;500;600;700;800&display=swap');
    
    .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background-color: #f8fafc !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid #1e293b;
    }
    [data-testid="stSidebar"] * {
        color: #f1f5f9 !important;
    }
    
    div.stButton > button {
        background: linear-gradient(135deg, #4f46e5 0%, #3730a3 100%) !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.2) !important;
        width: 100%;
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #4338ca 0%, #2e268f 100%) !important;
        box-shadow: 0 10px 15px -3px rgba(79, 70, 229, 0.4) !important;
        transform: translateY(-1px);
    }
    
    .agent-card {
        background-color: white;
        padding: 20px;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 12px;
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
            
            # Agentlar uchun varoqni yuklash
            try:
                agent_df = pd.read_excel(FAYL_OMBOR, sheet_name="Agentlar")
            except Exception:
                agent_df = pd.DataFrame(columns=["Agent Nomi", "Telefon", "Joriy Qarz"])
            
            # Ma'lumotlar formatini tekshirish
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
    """Barcha o'zgarishlarni Excelga yozadi."""
    with pd.ExcelWriter(FAYL_OMBOR, engine="openpyxl") as writer:
        ombor.to_excel(writer, sheet_name="Ombor", index=False)
        kirim.to_excel(writer, sheet_name="Kirim", index=False)
        chiqim.to_excel(writer, sheet_name="Chiqim", index=False)
        agentlar.to_excel(writer, sheet_name="Agentlar", index=False)

# Ma'lumotlarni xotiraga yuklab olamiz
ombor, kirim, chiqim, agentlar = bazani_yuklash()

def kpi_card(title, value, subtitle, icon, text_color, icon_bg):
    return f"""
    <div style="
        background-color: white;
        padding: 24px;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
    ">
        <div>
            <span style="font-size: 11px; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; display: block; margin-bottom: 6px;">{title}</span>
            <h3 style="font-size: 24px; font-weight: 800; color: #0f172a; margin: 0; line-height: 1.1;">{value}</h3>
            <span style="font-size: 12px; font-weight: 600; color: {text_color}; display: flex; align-items: center; gap: 4px; margin-top: 8px;">
                {subtitle}
            </span>
        </div>
        <div style="background-color: {icon_bg}; padding: 14px; border-radius: 14px; color: {text_color}; display: flex; align-items: center; justify-content: center; font-size: 24px; width: 54px; height: 54px;">
            {icon}
        </div>
    </div>
    """

def format_money(amount):
    return f"{amount:,.0f} UZS".replace(",", " ")

st.sidebar.markdown("""
<div style="display: flex; align-items: center; gap: 12px; padding: 10px 0 25px 0; border-bottom: 1px solid #1e293b; margin-bottom: 20px;">
    <div style="background-color: #4f46e5; padding: 10px; border-radius: 12px; display: flex; align-items: center; justify-content: center;">
        <span style="font-size: 20px;">📦</span>
    </div>
    <div>
        <h2 style="font-size: 17px; font-weight: 800; color: white; margin: 0; padding: 0;">Smart-Ombor ERP</h2>
        <span style="font-size: 10px; color: #818cf8; font-weight: 600; text-transform: uppercase;">Pro Boshqaruv</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Kirish Rejimini tanlash
rol = st.sidebar.radio("🔑 Kirish Rejimi", ["👤 Agent Rejimi (Qoldiq)", "🔐 Admin Rejimi (To'liq ERP)"])

administrator_tasdiq = False

if rol == "🔐 Admin Rejimi (To'liq ERP)":
    parol = st.sidebar.text_input("Maxfiy parolni kiriting:", type="password")
    if parol == "19920904":
        administrator_tasdiq = True
        st.sidebar.success("Kirish muvaffaqiyatli!")
    else:
        if parol != "":
            st.sidebar.error("❌ Parol noto'g'ri!")
        st.sidebar.info("Agent rejimidan foydalanish uchun yuqoridagi tegishli tugmani bosing.")

if administrator_tasdiq:
    menyu = st.sidebar.radio(
        "Asosiy Bo'limlar",
        ["📊 Boshqaruv Paneli", "📦 Mahsulotlar Qoldig'i", "👥 Agentlar & Qarzdorlik", "📥 Yangi Kirim", "📤 Yangi Chiqim", "🕒 Amallar Tarixi"]
    )
else:
    menyu = "📦 Mahsulotlar Qoldig'i (Agent Rejimi)"
    st.sidebar.markdown("""
    <div style="padding: 15px; background-color: #1e293b; border-radius: 12px; margin-top: 20px;">
        <p style="font-size: 12px; color: #94a3b8; margin: 0;">Siz <b>Agent Rejimidan</b> foydalanmoqdasiz. Sizga faqat joriy ombor qoldig'i ma'lumotlari ko'rsatiladi.</p>
    </div>
    """, unsafe_allow_html=True)

if administrator_tasdiq and menyu == "📊 Boshqaruv Paneli":
    st.markdown("""
    <div style="margin-bottom: 25px;">
        <h1 style="font-size: 28px; font-weight: 800; color: #0f172a; margin-bottom: 4px;">📊 Tahliliy Ko'rsatkichlar (Maxfiy)</h1>
        <p style="font-size: 14px; color: #64748b; margin: 0;">Omborxonaning real vaqt rejimida moliyaviy va tovar ko'rsatkichlari</p>
    </div>
    """, unsafe_allow_html=True)
    
    # KPIs Hisob-kitobi
    jami_turlar = len(ombor)
    jami_dona = int(ombor["Miqdori"].sum()) if jami_turlar > 0 else 0
    jami_qiymat = (ombor["Miqdori"] * ombor["Narxi"]).sum() if jami_turlar > 0 else 0
    jami_agent_qarzlari = agentlar["Joriy Qarz"].sum() if not agentlar.empty else 0
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(kpi_card("Mavjud Mahsulotlar", f"{jami_turlar} turda", "Ombordagi faol tovar turlari", "📦", "#4f46e5", "#f0f2fe"), unsafe_allow_html=True)
    with col2:
        st.markdown(kpi_card("Umumiy Zaxira", f"{jami_dona} dona", "Barcha qoldiq miqdori", "📊", "#10b981", "#ecfdf5"), unsafe_allow_html=True)
    with col3:
        st.markdown(kpi_card("Ombor Jami Qiymati", format_money(jami_qiymat), "Aylanma mablag' hajmi", "💰", "#f59e0b", "#fffbeb"), unsafe_allow_html=True)
    with col4:
        st.markdown(kpi_card("Agentlarning Jami Qarzi", format_money(jami_agent_qarzlari), "Yig'ilishi kerak bo'lgan mablag'", "👥", "#ef4444", "#fef2f2"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    g_col1, g_col2 = st.columns([3, 2])
    
    with g_col1:
        st.markdown("""
        <div style="background-color: white; padding: 20px; border-radius: 16px; border: 1px solid #e2e8f0; margin-bottom: 20px;">
            <h4 style="margin: 0 0 15px 0; font-size: 16px; font-weight: 700; color: #0f172a;">📦 Mahsulotlar Miqdori Tahlili</h4>
        </div>
        """, unsafe_allow_html=True)
        if jami_turlar > 0:
            saralangan_ombor = ombor.sort_values(by="Miqdori", ascending=False).head(10)
            st.bar_chart(data=saralangan_ombor, x="Mahsulot Nomi", y="Miqdori", color="#4f46e5")
        else:
            st.info("Omborda grafik ko'rsatish uchun mahsulotlar yetarli emas.")
            
    with g_col2:
        st.markdown("""
        <div style="background-color: white; padding: 20px; border-radius: 16px; border: 1px solid #e2e8f0; height: 100%;">
            <h4 style="margin: 0 0 15px 0; font-size: 16px; font-weight: 700; color: #ef4444; display: flex; align-items: center; gap: 8px;">
                ⚠️ Kam Qolgan Mahsulotlar (Zaxira Ogohlantirishi)
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
                <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px; background-color: #fef2f2; border-radius: 10px; margin-bottom: 8px; border: 1px solid #fee2e2;">
                    <div>
                        <b style="color: #991b1b; font-size: 13px;">{nomi}</b>
                        <div style="font-size: 11px; color: #b91c1c;">Zaxiradan tez orada tugashi mumkin</div>
                    </div>
                    <span style="background-color: #fca5a5; color: #7f1d1d; padding: 4px 10px; border-radius: 8px; font-size: 12px; font-weight: 700;">
                        {miqdori} {birligi}
                    </span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align: center; padding: 40px; color: #10b981;">
                <span style="font-size: 36px;">😊</span>
                <p style="margin-top: 10px; font-size: 13px; font-weight: 600;">Hamma mahsulotlar yetarli darajada!</p>
            </div>
            """, unsafe_allow_html=True)

elif administrator_tasdiq and menyu == "📦 Mahsulotlar Qoldig'i":
    st.markdown("""
    <div style="margin-bottom: 25px;">
        <h1 style="font-size: 28px; font-weight: 800; color: #0f172a; margin-bottom: 4px;">📦 Mavjud Mahsulotlar va Moliyaviy Qiymati</h1>
        <p style="font-size: 14px; color: #64748b; margin: 0;">Barcha mahsulotlar, ularning narxlari va jami moliyaviy hisobi</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Qidiruv va filtrlar
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
    <div style="margin-bottom: 25px;">
        <h1 style="font-size: 28px; font-weight: 800; color: #4f46e5; margin-bottom: 4px;">📦 Ombordagi Mahsulotlar Qoldig'i (Agentlar uchun)</h1>
        <p style="font-size: 14px; color: #64748b; margin: 0;">Real vaqtda omborda mavjud bo'lgan mahsulotlar va ularning miqdori</p>
    </div>
    """, unsafe_allow_html=True)
    
    qidiruv_agent = st.text_input("🔍 Kerakli mahsulotni qidiring...", placeholder="Mahsulot nomini kiriting...")
    
    if not ombor.empty:
        filtr_agent = ombor.copy()
        if qidiruv_agent:
            filtr_agent = filtr_agent[filtr_agent["Mahsulot Nomi"].str.lower().str.contains(qidiruv_agent.lower())]
            
        # Agentlarga narxlar va moliyaviy hisob-kitoblar mutlaqo ko'rinmaydi
        st.markdown("""
        <style>
            div[data-testid="stDataFrame"] {
                border-radius: 16px !important;
                box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05) !important;
                border: 1px solid #e2e8f0 !important;
                background-color: white !important;
            }
        </style>
        """, unsafe_allow_html=True)
        
        # Status ustuni qo'shish
        def status_belgilash(qty):
            if qty <= 0:
                return "❌ Tugagan"
            elif qty <= 15:
                return "⚠️ Kam qolgan"
            else:
                return "✅ Zaxira yetarli"
                
        filtr_agent["Zaxira Holati"] = filtr_agent["Miqdori"].apply(status_belgilash)
        
        st.dataframe(
            filtr_agent[["Kategoriya", "Mahsulot Nomi", "Miqdori", "O'lchov Birligi", "Zaxira Holati"]],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Hozirda omborda mahsulot qoldig'i mavjud emas.")

elif administrator_tasdiq and menyu == "👥 Agentlar & Qarzdorlik":
    st.markdown("""
    <div style="margin-bottom: 25px;">
        <h1 style="font-size: 28px; font-weight: 800; color: #0f172a; margin-bottom: 4px;">👥 Agentlar va Ularning Qarzlari</h1>
        <p style="font-size: 14px; color: #64748b; margin: 0;">Doimiy mahsulot olib ketuvchi mijozlar (agentlar) qarzdorlik tahlili va to'lov qabul qilish</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["💰 Agentlar Ro'yxati & Qarzlar", "➕ Yangi Agent Qo'shish & To'lov Yopish"])
    
    with tab1:
        if not agentlar.empty:
            for idx, row in agentlar.iterrows():
                f_qarz = format_money(row["Joriy Qarz"])
                st.markdown(f"""
                <div class="agent-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <h4 style="margin: 0; font-size: 18px; font-weight: 700; color: #1e293b;">👤 {row['Agent Nomi']}</h4>
                            <p style="margin: 4px 0 0 0; font-size: 12px; color: #64748b;">📞 Telefon: {row['Telefon']}</p>
                        </div>
                        <div style="text-align: right;">
                            <span style="font-size: 11px; font-weight: 700; color: #94a3b8; text-transform: uppercase;">Mavjud Qarz:</span>
                            <h3 style="margin: 0; font-size: 20px; font-weight: 800; color: {'#ef4444' if row['Joriy Qarz'] > 0 else '#10b981'};">{f_qarz}</h3>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Hozircha hech qanday agent qo'shilmagan.")
            
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
                        
                        # Chiqim (To'lov jurnali sifatida ham ko'rish mumkin bo'lgan qaydni amallar tarixiga yozamiz)
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
    <div style="margin-bottom: 25px;">
        <h1 style="font-size: 28px; font-weight: 800; color: #10b981; margin-bottom: 4px;">📥 Tezkor Kirim Amali</h1>
        <p style="font-size: 14px; color: #64748b; margin: 0;">Omborxonaga yangi yoki mavjud tovarlarni tezda kirim qilish shakli</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            kirim_turi = st.radio("Kirim turi:", ["Mavjud mahsulotni ko'paytirish", "Yangi mahsulot yaratish"])
            
            if kirim_turi == "Mavjud mahsulotni ko'paytirish" and not ombor.empty:
                nomi = st.selectbox("Mahsulotni tanlang:", ombor["Mahsulot Nomi"].unique())
                birligi = ombor.loc[ombor["Mahsulot Nomi"] == nomi, "O'lchov Birligi"].values[0]
                kategoriya = ombor.loc[ombor["Mahsulot Nomi"] == nomi, "Kategoriya"].values[0]
                narx_bosh = float(ombor.loc[ombor["Mahsulot Nomi"] == nomi, "Narxi"].values[0])
            else:
                nomi = st.text_input("Yangi mahsulot nomi:", placeholder="Masalan: Armatura A500C 16mm").strip().capitalize()
                kategoriya = st.selectbox("Turkum / Kategoriya:", ["Qurilish materiallari", "Elektrotexnika", "Santexnika", "Asbob-uskunalar", "Boshqa"])
                birligi = st.selectbox("O'lchov birligi:", ["dona", "kg", "litr", "metr", "qop", "quti"])
                narx_bosh = 10000.0

        with col2:
            miqdori = st.number_input("Kirim miqdori:", min_value=0.1, value=1.0, step=1.0)
            narxi = st.number_input("Tanlangan mahsulot narxi (UZS):", min_value=0.0, value=narx_bosh, step=1000.0)
            masul = st.text_input("Qabul qiluvchi mas'ul shaxs:", value="Karim Umirzoq").strip().capitalize()
            
        submit = st.button("📥 Kirimni omborga yozish")
        
        if submit:
            if nomi and masul:
                # Omborni yangilaymiz
                if nomi in ombor["Mahsulot Nomi"].values:
                    ombor.loc[ombor["Mahsulot Nomi"] == nomi, "Miqdori"] += miqdori
                    ombor.loc[ombor["Mahsulot Nomi"] == nomi, "Narxi"] = narxi
                else:
                    yangi_qator = pd.DataFrame([{"Mahsulot Nomi": nomi, "Miqdori": miqdori, "O'lchov Birligi": birligi, "Narxi": narxi, "Kategoriya": kategoriya}])
                    ombor = pd.concat([ombor, yangi_qator], ignore_index=True)
                
                # Kirim tarixiga yozish
                sana = datetime.now().strftime("%Y-%m-%d %H:%M")
                yangi_kirim = pd.DataFrame([{"Sana": sana, "Mahsulot Nomi": nomi, "Miqdori": miqdori, "Mas'ul": masul}])
                kirim = pd.concat([kirim, yangi_kirim], ignore_index=True)
                
                bazani_saqlash(ombor, kirim, chiqim, agentlar)
                st.success(f"✅ Muvaffaqiyatli: {miqdori} {birligi} '{nomi}' omborga qabul qilindi!")
                st.balloons()
            else:
                st.error("Iltimos, barcha maydonlarni to'ldiring!")

elif administrator_tasdiq and menyu == "📤 Yangi Chiqim":
    st.markdown("""
    <div style="margin-bottom: 25px;">
        <h1 style="font-size: 28px; font-weight: 800; color: #f43f5e; margin-bottom: 4px;">📤 Mahsulot Chiqim Qilish / Agentga Yuklash</h1>
        <p style="font-size: 14px; color: #64748b; margin: 0;">Ombordan mahsulotlarni chiqim qilish yoki agent hisobiga (qarzga) o'tkazish</p>
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
                
                st.info(f"ℹ️ Ombordagi joriy qoldiq: **{qoldiq} {birligi}** | Mahsulot Narxi: **{format_money(narxi)}**")
                
                chiqim_turi = st.radio("Chiqim sharti (Turi):", ["Naqd/Plastik sotuv", "Agentga qarz hisobiga yuklash"])
                
            with col2:
                miqdori = st.number_input("Chiqim miqdori:", min_value=0.1, max_value=float(qoldiq), value=1.0, step=1.0)
                
                # Chiqim turiga qarab agentni tanlash yoki oddiy oluvchini kiritish
                if chiqim_turi == "Agentga qarz hisobiga yuklash":
                    if not agentlar.empty:
                        tanlangan_agent = st.selectbox("Mahsulotni olib ketayotgan agent:", agentlar["Agent Nomi"].unique())
                        qabul_qiluvchi = tanlangan_agent
                    else:
                        st.error("Hech qanday agent topilmadi. Avval 'Agentlar & Qarzdorlik' bo'limida agent yarating.")
                        tanlangan_agent = "Noma'lum"
                        qabul_qiluvchi = "Noma'lum"
                else:
                    tanlangan_agent = "Yo'q (Naqd Sotuv)"
                    qabul_qiluvchi = st.text_input("Qabul qiluvchi shaxs/tashkilot nomi:", placeholder="Masalan: Blok B qurilishi")
                    
            submit = st.button("📤 Chiqimni tasdiqlash va rasmiylashtirish")
            
            if submit:
                if qabul_qiluvchi:
                    jami_summa = miqdori * narxi
                    
                    # 1. Ombordagi mahsulot qoldig'ini kamaytirish
                    ombor.loc[ombor["Mahsulot Nomi"] == nomi, "Miqdori"] -= miqdori
                    
                    # 2. Agar agent bo'lsa, uning qarzini oshirish
                    if chiqim_turi == "Agentga qarz hisobiga yuklash" and tanlangan_agent != "Noma'lum":
                        agentlar.loc[agentlar["Agent Nomi"] == tanlangan_agent, "Joriy Qarz"] += jami_summa
                        
                    # 3. Chiqim tarixiga yozish
                    sana = datetime.now().strftime("%Y-%m-%d %H:%M")
                    yangi_chiqim = pd.DataFrame([{
                        "Sana": sana, "Mahsulot Nomi": nomi, "Miqdori": miqdori,
                        "Qabul qiluvchi": qabul_qiluvchi, "Agent": tanlangan_agent,
                        "Chiqim Turi": chiqim_turi, "Jami Summa": jami_summa
                    }])
                    chiqim = pd.concat([chiqim, yangi_chiqim], ignore_index=True)
                    
                    bazani_saqlash(ombor, kirim, chiqim, agentlar)
                    st.success(f"✅ Muvaffaqiyatli: {miqdori} {birligi} '{nomi}' chiqarildi! Jami: {format_money(jami_summa)}")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("Iltimos, kerakli barcha maydonlarni to'ldiring!")

elif administrator_tasdiq and menyu == "🕒 Amallar Tarixi":
    st.markdown("""
    <div style="margin-bottom: 25px;">
        <h1 style="font-size: 28px; font-weight: 800; color: #0f172a; margin-bottom: 4px;">🕒 Ombor Harakatlari Tarixi</h1>
        <p style="font-size: 14px; color: #64748b; margin: 0;">Kirim va chiqim amallarining batafsil jurnallari</p>
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
            # Chiqim formatlash
            chiqim_ko_df = chiqim.copy()
            if "Jami Summa" in chiqim_ko_df.columns:
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
