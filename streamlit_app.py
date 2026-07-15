import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Sahifa sozlamalarini o'rnatamiz (Keng ekran rejimi)
st.set_page_config(
    page_title="Smart-Ombor ERP | Professional Boshqaruv Tizimi",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS orqali Streamlit interfeysini butunlay o'zgartiramiz (Premium Dizayn)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    /* Umumiy fon va shriftlar */
    .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background-color: #f8fafc !important;
    }
    
    /* Sarlavhalarni sozlash */
    h1, h2, h3, h4, h5, h6, p, span, div {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    /* Chap panel (Sidebar) dizaynini o'zgartirish */
    [data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid #1e293b;
    }
    [data-testid="stSidebar"] * {
        color: #f1f5f9 !important;
    }
    [data-testid="stSidebarNav"] {
        background-color: transparent !important;
    }
    
    /* Tugmalarni premium ko'rinishga keltirish */
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
    
    /* Forma va kiritish maydonchalari */
    div[data-baseweb="input"] {
        border-radius: 12px !important;
        border: 1px solid #e2e8f0 !important;
        background-color: #ffffff !important;
    }
    div[data-baseweb="select"] {
        border-radius: 12px !important;
    }
    
    /* Bloklarni ajratish kontentlari */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Excel bazasi bilan ishlash
FAYL_OMBOR = "onlayn_ombor.xlsx"

def bazani_yuklash():
    """Excel faylini yuklaydi yoki yangi yaratadi."""
    if os.path.exists(FAYL_OMBOR):
        try:
            ombor_df = pd.read_excel(FAYL_OMBOR, sheet_name="Ombor")
            kirim_df = pd.read_excel(FAYL_OMBOR, sheet_name="Kirim")
            chiqim_df = pd.read_excel(FAYL_OMBOR, sheet_name="Chiqim")
            
            # Ma'lumot turlarini to'g'rilaymiz
            ombor_df["Miqdori"] = pd.to_numeric(ombor_df["Miqdori"], errors='coerce').fillna(0)
            if "Narxi" not in ombor_df.columns:
                ombor_df["Narxi"] = 10000.0  # Standart boshlang'ich narx
            ombor_df["Narxi"] = pd.to_numeric(ombor_df["Narxi"], errors='coerce').fillna(10000.0)
            
            kirim_df["Miqdori"] = pd.to_numeric(kirim_df["Miqdori"], errors='coerce').fillna(0)
            chiqim_df["Miqdori"] = pd.to_numeric(chiqim_df["Miqdori"], errors='coerce').fillna(0)
            
            return ombor_df, kirim_df, chiqim_df
        except Exception as e:
            st.error(f"Baza yuklanishida xatolik: {e}. Yangi baza yaratilmoqda...")
            
    ombor_df = pd.DataFrame(columns=["Mahsulot Nomi", "Miqdori", "O'lchov Birligi", "Narxi"])
    kirim_df = pd.DataFrame(columns=["Sana", "Mahsulot Nomi", "Miqdori", "Mas'ul"])
    chiqim_df = pd.DataFrame(columns=["Sana", "Mahsulot Nomi", "Miqdori", "Qabul qiluvchi"])
    return ombor_df, kirim_df, chiqim_df

def bazani_saqlash(ombor, kirim, chiqim):
    """O'zgarishlarni Excelga yozadi."""
    with pd.ExcelWriter(FAYL_OMBOR, engine="openpyxl") as writer:
        ombor.to_excel(writer, sheet_name="Ombor", index=False)
        kirim.to_excel(writer, sheet_name="Kirim", index=False)
        chiqim.to_excel(writer, sheet_name="Chiqim", index=False)

# Ma'lumotlarni yuklab olamiz
ombor, kirim, chiqim = bazani_yuklash()

# Chiroyli HTML kartalar yaratish uchun funksiya
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
            <h3 style="font-size: 26px; font-weight: 800; color: #0f172a; margin: 0; line-height: 1.1;">{value}</h3>
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

# Sidebar sarlavhasi va brending
st.sidebar.markdown("""
<div style="display: flex; align-items: center; gap: 12px; padding: 10px 0 25px 0; border-bottom: 1px solid #1e293b; margin-bottom: 20px;">
    <div style="background-color: #4f46e5; padding: 10px; border-radius: 12px; display: flex; align-items: center; justify-content: center;">
        <span style="font-size: 20px;">📦</span>
    </div>
    <div>
        <h2 style="font-size: 18px; font-weight: 800; color: white; margin: 0; padding: 0;">Smart-Ombor</h2>
        <span style="font-size: 11px; color: #818cf8; font-weight: 600; text-transform: uppercase; tracking: 0.1em;">Boshqaruv ERP</span>
    </div>
</div>
""", unsafe_allow_html=True)

menyu = st.sidebar.radio(
    "Asosiy Menyu",
    ["📊 Boshqaruv Paneli", "📦 Mahsulotlar Qoldig'i", "📥 Yangi Kirim", "📤 Yangi Chiqim", "🕒 Amallar Tarixi"]
)

# Foydalanuvchi ma'lumoti pastki qismda
st.sidebar.markdown("""
<div style="position: fixed; bottom: 15px; left: 15px; display: flex; align-items: center; gap: 10px; border-top: 1px solid #1e293b; padding-top: 15px; width: 230px;">
    <div style="width: 36px; height: 36px; background-color: #3b82f6; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; color: white;">
        K
    </div>
    <div>
        <h4 style="font-size: 13px; font-weight: 600; color: white; margin: 0;">Karim Umirzoq</h4>
        <span style="font-size: 10px; color: #64748b;">Bosh administrator</span>
    </div>
</div>
""", unsafe_allow_html=True)

if menyu == "📊 Boshqaruv Paneli":
    # Sahifa Sarlavhasi
    st.markdown("""
    <div style="margin-bottom: 25px;">
        <h1 style="font-size: 28px; font-weight: 800; color: #0f172a; margin-bottom: 4px;">Tahliliy Ko'rsatkichlar</h1>
        <p style="font-size: 14px; color: #64748b; margin: 0;">Omborxonani real vaqtda boshqarish va monitoring qilish tizimi</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Ma'lumotlarni hisoblash
    jami_turlar = len(ombor)
    jami_dona = int(ombor["Miqdori"].sum()) if jami_turlar > 0 else 0
    
    # Narx bo'yicha jami qiymat
    if jami_turlar > 0:
        ombor["Jami_Qiymat"] = ombor["Miqdori"] * ombor["Narxi"]
        jami_qiymat = ombor["Jami_Qiymat"].sum()
    else:
        jami_qiymat = 0
        
    bugungi_sana = datetime.now().strftime("%Y-%m-%d")
    bugungi_chiqimlar = len(chiqim[chiqim["Sana"].astype(str).str.contains(bugungi_sana)])
    
    # KPI Kartalarini 4 ta ustunda chiqaramiz
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(kpi_card("Mavjud Mahsulotlar", f"{jami_turlar} turda", "Yangi mahsulotlar qo'shildi", "📦", "#4f46e5", "#f0f2fe"), unsafe_allow_html=True)
    with col2:
        st.markdown(kpi_card("Umumiy Qoldiq", f"{jami_dona} dona", "Zaxira yetarli darajada", "📊", "#10b981", "#ecfdf5"), unsafe_allow_html=True)
    with col3:
        st.markdown(kpi_card("Jami Qiymat", format_money(jami_qiymat), "Aylanma mablag' hajmi", "💰", "#f59e0b", "#fffbeb"), unsafe_allow_html=True)
    with col4:
        st.markdown(kpi_card("Bugungi Chiqimlar", f"{bugungi_chiqimlar} ta amal", "Chiquvchi loglar soni", "🚚", "#f43f5e", "#fff5f5"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Grafik va Tarix qismi
    g_col1, g_col2 = st.columns([3, 2])
    
    with g_col1:
        st.markdown("""
        <div style="background-color: white; padding: 20px; border-radius: 16px; border: 1px solid #e2e8f0; margin-bottom: 20px;">
            <h4 style="margin: 0 0 15px 0; font-size: 16px; font-weight: 700; color: #0f172a;">📦 Mahsulotlar Qoldig'i (Top 10)</h4>
        </div>
        """, unsafe_allow_html=True)
        if jami_turlar > 0:
            saralangan_ombor = ombor.sort_values(by="Miqdori", ascending=False).head(10)
            st.bar_chart(data=saralangan_ombor, x="Mahsulot Nomi", y="Miqdori", color="#4f46e5")
        else:
            st.info("Grafik ko'rsatish uchun omborda mahsulot mavjud emas.")
            
    with g_col2:
        st.markdown("""
        <div style="background-color: white; padding: 20px; border-radius: 16px; border: 1px solid #e2e8f0;">
            <h4 style="margin: 0 0 15px 0; font-size: 16px; font-weight: 700; color: #f43f5e; display: flex; align-items: center; gap: 8px;">
                ⚠️ Zaxirasi Tugayotgan Mahsulotlar
            </h4>
        </div>
        """, unsafe_allow_html=True)
        
        kam_qoldiq = ombor[ombor["Miqdori"] <= 10] # Zaxira kamligi chegarasi (10 dona)
        if not kam_qoldiq.empty:
            for index, row in kam_qoldiq.iterrows():
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px; background-color: #fff5f5; border-radius: 10px; margin-bottom: 8px; border: 1px solid #fee2e2;">
                    <div>
                        <b style="color: #991b1b; font-size: 13px;">{row['Mahsulot Nomi']}</b>
                        <div style="font-size: 11px; color: #b91c1c;">Zaxiradan kam qoldi</div>
                    </div>
                    <span style="background-color: #fca5a5; color: #7f1d1d; padding: 4px 10px; border-radius: 8px; font-size: 12px; font-weight: 700;">
                        {row['Miqdori']} {row['O'lchov Birligi']}
                    </span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align: center; padding: 30px; color: #10b981;">
                <span style="font-size: 32px;">😊</span>
                <p style="margin-top: 10px; font-size: 13px; font-weight: 600;">Hamma mahsulotlar zaxirasi yetarli darajada!</p>
            </div>
            """, unsafe_allow_html=True)

elif menyu == "📦 Mahsulotlar Qoldig'i":
    st.markdown("""
    <div style="margin-bottom: 25px;">
        <h1 style="font-size: 28px; font-weight: 800; color: #0f172a; margin-bottom: 4px;">Omborda Mavjud Mahsulotlar</h1>
        <p style="font-size: 14px; color: #64748b; margin: 0;">Barcha mahsulotlar ro'yxati, narxi va joriy holati</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Qidiruv tizimi
    q_col1, q_col2 = st.columns([3, 1])
    with q_col1:
        qidiruv = st.text_input("🔍 Mahsulot nomi bo'yicha tezkor qidiruv...", placeholder="Mahsulot nomini kiriting...")
    with q_col2:
        eksport = st.download_button(
            label="📥 Excel yuklab olish",
            data=open(FAYL_OMBOR, "rb") if os.path.exists(FAYL_OMBOR) else b"",
            file_name="ombor_qoldigi.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
    if not ombor.empty:
        filtr_ombor = ombor.copy()
        if qidiruv:
            filtr_ombor = filtr_ombor[filtr_ombor["Mahsulot Nomi"].str.lower().str.contains(qidiruv.lower())]
            
        # Jadvalni chiroyli ko'rsatish
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
        
        # Formatlangan nusxa ko'rsatamiz
        korish_df = filtr_ombor.copy()
        korish_df["Narxi (UZS)"] = korish_df["Narxi"].apply(format_money)
        korish_df["Jami Qiymati"] = (korish_df["Miqdori"] * korish_df["Narxi"]).apply(format_money)
        
        st.dataframe(
            korish_df[["Mahsulot Nomi", "Miqdori", "O'lchov Birligi", "Narxi (UZS)", "Jami Qiymati"]],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.warning("Hali omborga hech qanday mahsulot kirim qilinmagan.")

elif menyu == "📥 Yangi Kirim":
    st.markdown("""
    <div style="margin-bottom: 25px;">
        <h1 style="font-size: 28px; font-weight: 800; color: #10b981; margin-bottom: 4px;">📥 Yangi Kirim Amali</h1>
        <p style="font-size: 14px; color: #64748b; margin: 0;">Omborga yangi tovar yoki mahsulot qabul qilish</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            # Mavjud mahsulotlardan tanlash yoki yangi qo'shish
            tanlash_turi = st.radio("Kirim turi:", ["Mavjud mahsulotni ko'paytirish", "Yangi mahsulot yaratish"])
            
            if tanlash_turi == "Mavjud mahsulotni ko'paytirish" and not ombor.empty:
                nomi = st.selectbox("Mahsulotni tanlang:", ombor["Mahsulot Nomi"].unique())
                birligi = ombor.loc[ombor["Mahsulot Nomi"] == nomi, "O'lchov Birligi"].values[0]
                narx_bosh = float(ombor.loc[ombor["Mahsulot Nomi"] == nomi, "Narxi"].values[0])
            else:
                nomi = st.text_input("Yangi mahsulot nomi:", placeholder="Masalan: Armatura A500C 12mm").strip().capitalize()
                birligi = st.selectbox("O'lchov birligi:", ["dona", "kg", "litr", "metr", "qop", "quti"])
                narx_bosh = 10000.0

        with col2:
            miqdori = st.number_input("Kirim miqdori:", min_value=0.1, value=1.0, step=1.0)
            narxi = st.number_input("Sotib olingan narxi (1 dona/birlik uchun UZS):", min_value=0.0, value=narx_bosh, step=500.0)
            masul = st.text_input("Qabul qiluvchi mas'ul shaxs (Ism):", value="Karim Umirzoq").strip().capitalize()
            
        submit = st.button("📥 Kirimni tasdiqlash va saqlash")
        
        if submit:
            if nomi and masul:
                # Omborni yangilaymiz
                if nomi in ombor["Mahsulot Nomi"].values:
                    ombor.loc[ombor["Mahsulot Nomi"] == nomi, "Miqdori"] += miqdori
                    ombor.loc[ombor["Mahsulot Nomi"] == nomi, "Narxi"] = narxi
                else:
                    yangi_qator = pd.DataFrame([{"Mahsulot Nomi": nomi, "Miqdori": miqdori, "O'lchov Birligi": birligi, "Narxi": narxi}])
                    ombor = pd.concat([ombor, yangi_qator], ignore_index=True)
                
                # Kirim tarixiga yozish
                sana = datetime.now().strftime("%Y-%m-%d %H:%M")
                yangi_kirim = pd.DataFrame([{"Sana": sana, "Mahsulot Nomi": nomi, "Miqdori": miqdori, "Mas'ul": masul}])
                kirim = pd.concat([kirim, yangi_kirim], ignore_index=True)
                
                bazani_saqlash(ombor, kirim, chiqim)
                st.success(f"✅ Muvaffaqiyatli: {miqdori} {birligi} '{nomi}' omborga qabul qilindi!")
                st.balloons()
            else:
                st.error("Iltimos, barcha maydonlarni to'ldiring!")

elif menyu == "📤 Yangi Chiqim":
    st.markdown("""
    <div style="margin-bottom: 25px;">
        <h1 style="font-size: 28px; font-weight: 800; color: #f43f5e; margin-bottom: 4px;">📤 Yangi Chiqim Amali</h1>
        <p style="font-size: 14px; color: #64748b; margin: 0;">Ombordan mahsulot yoki tovarlarni chiqarish</p>
    </div>
    """, unsafe_allow_html=True)
    
    if ombor.empty:
        st.warning("Omborda hech qanday mahsulot yo'q, avval kirim qiling!")
    else:
        with st.container(border=True):
            col1, col2 = st.columns(2)
            with col1:
                nomi = st.selectbox("Chiqim qilinadigan mahsulot:", ombor["Mahsulot Nomi"].unique())
                
                # Mavjud qoldiq ma'lumotlarini topamiz
                qoldiq = ombor.loc[ombor["Mahsulot Nomi"] == nomi, "Miqdori"].values[0]
                birligi = ombor.loc[ombor["Mahsulot Nomi"] == nomi, "O'lchov Birligi"].values[0]
                
                st.info(f"ℹ️ Ombordagi joriy qoldiq: **{qoldiq} {birligi}**")
                
            with col2:
                miqdori = st.number_input("Chiqim miqdori:", min_value=0.1, max_value=float(qoldiq), value=1.0, step=1.0)
                qabul_qiluvchi = st.text_input("Kimga yoki Qayerga topshirildi:", placeholder="Masalan: Blok B qurilishi").strip().capitalize()
                
            submit = st.button("📤 Chiqimni tasdiqlash")
            
            if submit:
                if qabul_qiluvchi:
                    # Miqdorni kamaytiramiz
                    ombor.loc[ombor["Mahsulot Nomi"] == nomi, "Miqdori"] -= miqdori
                    
                    # Qoldiq 0 bo'lsa ham qatorda tursin (narxi o'chib ketmasligi uchun)
                    # Faqat bazaga yoziladi
                    
                    # Chiqim tarixiga yozish
                    sana = datetime.now().strftime("%Y-%m-%d %H:%M")
                    yangi_chiqim = pd.DataFrame([{"Sana": sana, "Mahsulot Nomi": nomi, "Miqdori": miqdori, "Qabul qiluvchi": qabul_qiluvchi}])
                    chiqim = pd.concat([chiqim, yangi_chiqim], ignore_index=True)
                    
                    bazani_saqlash(ombor, kirim, chiqim)
                    st.success(f"✅ Muvaffaqiyatli: {miqdori} {birligi} '{nomi}' chiqarildi!")
                else:
                    st.error("Iltimos, topshirilgan joy yoki shaxsni kiriting!")

elif menyu == "🕒 Amallar Tarixi":
    st.markdown("""
    <div style="margin-bottom: 25px;">
        <h1 style="font-size: 28px; font-weight: 800; color: #0f172a; margin-bottom: 4px;">🕒 Amallar Tarixi</h1>
        <p style="font-size: 14px; color: #64748b; margin: 0;">Barcha kirim va chiqim operatsiyalarining batafsil loglari</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📥 Kirimlar Tarixi", "📤 Chiqimlar Tarixi"])
    
    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        if not kirim.empty:
            st.dataframe(kirim.sort_values(by="Sana", ascending=False), use_container_width=True, hide_index=True)
        else:
            st.info("Kirimlar tarixi hozircha bo'sh.")
            
    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        if not chiqim.empty:
            st.dataframe(chiqim.sort_values(by="Sana", ascending=False), use_container_width=True, hide_index=True)
        else:
            st.info("Chiqimlar tarixi hozircha bo'sh.")
