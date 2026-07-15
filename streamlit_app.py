import streamlit as st
import pandas as pd
from datetime import datetime
import os
import base64

# Sahifaning yuqori sozlamalari
st.set_page_config(
    page_title="Smart-Ombor Pro ERP v3.0",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium CSS - Glassmorphism, Neon va Yandex Market kartochkalari dizayni
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    /* Umumiy fon */
    .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background-color: #f4f6fa !important;
    }
    
    /* Sidebar dizayni */
    [data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid #1e293b;
    }
    [data-testid="stSidebar"] * {
        color: #f1f5f9 !important;
    }
    
    /* Sidebar navigatsiya tugmalari */
    div[data-testid="stSidebarUserContent"] div[role="radiogroup"] {
        gap: 8px !important;
    }
    div[data-testid="stSidebarUserContent"] div[role="radiogroup"] label {
        background-color: #1e293b !important;
        color: #94a3b8 !important;
        border-radius: 12px !important;
        padding: 10px 14px !important;
        border: 1px solid #334155 !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
        display: flex !important;
        align-items: center !important;
    }
    div[data-testid="stSidebarUserContent"] div[role="radiogroup"] label[data-checked="true"] {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
        color: white !important;
        border-color: #6366f1 !important;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3) !important;
    }
    div[data-testid="stSidebarUserContent"] div[role="radiogroup"] label:hover {
        background-color: #334155 !important;
        color: #f1f5f9 !important;
    }
    div[data-testid="stSidebarUserContent"] div[role="radiogroup"] label div[role="presentation"] {
        display: none !important;
    }

    /* Asosiy Tugmalar */
    div.stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 10px 20px !important;
        font-weight: 700 !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 10px rgba(99, 102, 241, 0.2) !important;
    }
    div.stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 8px 16px rgba(79, 70, 229, 0.3) !important;
    }

    /* Premium Karta Konteyneri */
    .premium-card {
        background: white;
        padding: 24px;
        border-radius: 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
        margin-bottom: 20px;
    }

    /* Yandex Market Style Mahsulot Kartasi */
    .yandex-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
        gap: 20px;
        padding: 10px 0;
    }
    .yandex-card {
        background: white;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        overflow: hidden;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        position: relative;
    }
    .yandex-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.08);
    }
    .yandex-img-container {
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
    .yandex-img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.5s ease;
    }
    .yandex-card:hover .yandex-img {
        transform: scale(1.05);
    }
    .yandex-badge {
        position: absolute;
        top: 10px;
        left: 10px;
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 11px;
        font-weight: 700;
        color: white;
        z-index: 2;
    }
    .yandex-info {
        padding: 15px;
        flex-grow: 1;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .yandex-cat {
        font-size: 11px;
        color: #94a3b8;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 0.05em;
        margin-bottom: 4px;
    }
    .yandex-title {
        font-size: 14px;
        font-weight: 700;
        color: #1e293b;
        margin: 0 0 10px 0;
        line-height: 1.4;
        height: 40px;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
    }
    .yandex-price-box {
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        margin-top: auto;
    }
    .yandex-price {
        font-size: 16px;
        font-weight: 800;
        color: #0f172a;
    }
    .yandex-stock {
        font-size: 12px;
        font-weight: 600;
        color: #64748b;
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
<div style="display: flex; align-items: center; gap: 14px; padding: 15px 0 30px 0; border-bottom: 1px solid #1e293b; margin-bottom: 25px;">
    <div style="background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%); padding: 12px; border-radius: 14px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);">
        <span style="font-size: 22px;">⚡</span>
    </div>
    <div>
        <h2 style="font-size: 18px; font-weight: 800; color: white; margin: 0; padding: 0; letter-spacing: -0.02em;">Smart-Ombor ERP</h2>
        <span style="font-size: 10px; color: #818cf8; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em;">Yandex Style v3.0</span>
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
        st.sidebar.success("🔓  MALADES PAROL TO'GRI !")
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
    <div style="padding: 18px; background: rgba(30, 41, 59, 0.5); border: 1px solid #334155; border-radius: 14px; margin-top: 25px;">
        <p style="font-size: 12px; color: #94a3b8; margin: 0; line-height: 1.5;">Siz hozirda <b>Agent Rejimi</b>dasiz. Sizga faqat joriy mahsulotlar rasmlari va qoldig'i ko'rsatiladi.</p>
    </div>
    """, unsafe_allow_html=True)

def mahsulot_katalogini_chizish(admin_view=False):
    """Yandex.jpg dagi kabi mahsulotlarni chiroyli rasm va kartochkalar ko'rinishida chiqaradi."""
    st.markdown("""
    <div style="margin-bottom: 25px;">
        <h1 style="font-size: 32px; font-weight: 800; color: #0f172a; margin-bottom: 6px; letter-spacing: -0.03em;">🛍️ Onlayn Katalog</h1>
        <p style="font-size: 15px; color: #64748b; margin: 0;">Mavjud barcha mahsulotlarning vizual ko'rgazmasi va joriy zaxirasi</p>
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
            status_bg = "#f43f5e" # Rose
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
        <h1 style="font-size: 32px; font-weight: 800; color: #0f172a; margin-bottom: 6px; letter-spacing: -0.03em;">📊 Boshqaruv Paneli</h1>
        <p style="font-size: 15px; color: #64748b; margin: 0;">Real vaqtda umumiy hisob-kitoblar va grafik tahlillar</p>
    </div>
    """, unsafe_allow_html=True)

    # KPIs
    jami_turlar = len(ombor)
    jami_dona = int(ombor["Miqdori"].sum()) if jami_turlar > 0 else 0
    jami_qiymat = (ombor["Miqdori"] * ombor["Narxi"]).sum() if jami_turlar > 0 else 0
    jami_agent_qarzlari = agentlar["Joriy Qarz"].sum() if not agentlar.empty else 0

    def kpi_card(title, value, subtitle, icon, icon_color, bg_gradient):
        return f"""
        <div style="background: white; padding: 24px; border-radius: 20px; border: 1px solid #e2e8f0; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 12px rgba(0,0,0,0.02);">
            <div>
                <span style="font-size: 11px; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.08em; display: block; margin-bottom: 6px;">{title}</span>
                <h3 style="font-size: 26px; font-weight: 800; color: #0f172a; margin: 0;">{value}</h3>
                <span style="font-size: 12px; color: #64748b; display: block; margin-top: 8px;">{subtitle}</span>
            </div>
            <div style="background: {bg_gradient}; padding: 14px; border-radius: 16px; color: {icon_color}; font-size: 26px; display: flex; align-items: center; justify-content: center; width: 56px; height: 56px;">
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
        st.markdown('<div class="premium-card"><h4>📈 Mahsulotlar Miqdori Tahlili</h4></div>', unsafe_allow_html=True)
        if jami_turlar > 0:
            st.bar_chart(data=ombor.head(10), x="Mahsulot Nomi", y="Miqdori", color="#6366f1")
    with g2:
        st.markdown('<div class="premium-card"><h4>⚠️ Zaxirasi kamaygan mahsulotlar</h4></div>', unsafe_allow_html=True)
        kam_qoldiq = ombor[ombor["Miqdori"] <= 15]
        if not kam_qoldiq.empty:
            for _, r in kam_qoldiq.iterrows():
                st.warning(f"🚨 **{r['Mahsulot Nomi']}**: Omborda atigi {r['Miqdori']} {r['O\'lchov Birligi']} qoldi!")
        else:
            st.success("Barcha mahsulotlar zaxirasi yetarli!")

elif administrator_tasdiq and menyu == "📦 Mahsulotlar Qoldig'i":
    st.markdown("""
    <div style="margin-bottom: 30px;">
        <h1 style="font-size: 32px; font-weight: 800; color: #0f172a; margin-bottom: 6px; letter-spacing: -0.03em;">📦 Mahsulotlar Qoldig'i & Rasmlar</h1>
        <p style="font-size: 15px; color: #64748b; margin: 0;">Mavjud tovarlarni boshqarish hamda rasmlarini yangilash bo'limi</p>
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

    # Mahsulotlar Jadvali
    st.dataframe(
        ombor[["Kategoriya", "Mahsulot Nomi", "Miqdori", "O'lchov Birligi", "Narxi"]],
        use_container_width=True,
        hide_index=True
    )

elif administrator_tasdiq and menyu == "👥 Agentlar & Qarzdorlik":
    st.markdown("### 👥 Agentlar va To'lovlar Tizimi")
    t1, t2 = st.tabs(["👥 Agentlar Ro'yxati", "➕ Yangi Agent & To'lov Qabul Qilish"])
    
    with t1:
        if not agentlar.empty:
            for _, r in agentlar.iterrows():
                st.markdown(f"""
                <div class="premium-card" style="border-left: 5px solid {'#ef4444' if r['Joriy Qarz'] > 0 else '#10b981'};">
                    <h4>👤 {r['Agent Nomi']}</h4>
                    <p>📞 Tel: {r['Telefon']}</p>
                    <h5>Mavjud Qarz: {format_money(r['Joriy Qarz'])}</h5>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Hali hech qanday agent qo'shilmagan.")

    with t2:
        col_ag, col_tol = st.columns(2)
        with col_ag:
            st.subheader("Yangi Agent qo'shish")
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

        with col_tol:
            st.subheader("Qarzni so'ndirish (To'lov)")
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
                        st.success(f"✅ Muvaffaqiyatli: {t_agent} hisobidan {format_money(summa)} qabul qilindi!")
                        st.rerun()

elif administrator_tasdiq and menyu == "📥 Yangi Kirim":
    st.markdown("### 📥 Omborga Yangi Kirim Qilish")
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
    st.markdown("### 📤 Ombordan Mahsulot Chiqim Qilish")
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
    st.markdown("### 🕒 Ombor Harakatlari Jurnali")
    tb1, tb2 = st.tabs(["📥 Barcha Kirimlar", "📤 Barcha Chiqimlar"])
    with tb1:
        st.dataframe(kirim.sort_values(by="Sana", ascending=False), use_container_width=True, hide_index=True)
    with tb2:
        st.dataframe(chiqim.sort_values(by="Sana", ascending=False), use_container_width=True, hide_index=True)
