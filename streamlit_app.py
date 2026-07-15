import streamlit as st
import pandas as pd
from datetime import datetime
import os
import base64

st.set_page_config(
    page_title="Smart-Ombor Ultra ERP v5.0",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    .stApp { font-family: 'Plus Jakarta Sans', sans-serif !important; background-color: #f1f5f9 !important; }
    .top-navbar { background: linear-gradient(90deg, #1e3a8a 0%, #0d9488 100%); padding: 20px; border-radius: 18px; color: white; margin-bottom: 20px; }
    .floating-card { background: white; padding: 20px; border-radius: 20px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); margin-bottom: 20px; }
    div.stButton > button { background: #0d9488 !important; color: white !important; border-radius: 10px !important; width: 100%; }
</style>
""", unsafe_allow_html=True)

FAYL_OMBOR = "onlayn_ombor.xlsx"

def bazani_yuklash():
    if os.path.exists(FAYL_OMBOR):
        try:
            return pd.read_excel(FAYL_OMBOR, sheet_name="Ombor"), pd.read_excel(FAYL_OMBOR, sheet_name="Kirim"), \
                   pd.read_excel(FAYL_OMBOR, sheet_name="Chiqim"), pd.read_excel(FAYL_OMBOR, sheet_name="Agentlar")
        except: pass
    
    ombor = pd.DataFrame(columns=["Mahsulot Nomi", "Miqdori", "O'lchov Birligi", "Narxi", "Kategoriya", "Rasm"])
    kirim = pd.DataFrame(columns=["Sana", "Mahsulot Nomi", "Miqdori", "Mas'ul"])
    chiqim = pd.DataFrame(columns=["Sana", "Mahsulot Nomi", "Miqdori", "Qabul qiluvchi", "Agent", "Chiqim Turi", "Jami Summa"])
    agentlar = pd.DataFrame(columns=["Agent Nomi", "Telefon", "Joriy Qarz"])
    return ombor, kirim, chiqim, agentlar

def bazani_saqlash(ombor, kirim, chiqim, agentlar):
    with pd.ExcelWriter(FAYL_OMBOR, engine="openpyxl") as writer:
        ombor.to_excel(writer, sheet_name="Ombor", index=False)
        kirim.to_excel(writer, sheet_name="Kirim", index=False)
        chiqim.to_excel(writer, sheet_name="Chiqim", index=False)
        agentlar.to_excel(writer, sheet_name="Agentlar", index=False)

ombor, kirim, chiqim, agentlar = bazani_yuklash()

st.sidebar.title("🔐 TIZIMGA KIRISH")
rol = st.sidebar.radio("Kirish rejimi:", ["👤 Agent Rejimi", "🔐 Admin Rejimi"])
administrator_tasdiq = False

if rol == "🔐 Admin Rejimi":
    parol = st.sidebar.text_input("Admin paroli:", type="password")
    if parol == "19920904":
        administrator_tasdiq = True
        st.sidebar.success("Admin huquqi faol!")
    else:
        st.sidebar.warning("Parol noto'g'ri.")

# Menyuni aniqlash
if administrator_tasdiq:
    menyu = st.sidebar.radio("ASOSIY BO'LIMLAR", ["🛍️ Katalog", "📊 Dashboard", "📦 Mahsulotlar", "👥 Agentlar", "📥 Kirim", "📤 Chiqim"])
else:
    menyu = "🛍️ Katalog"

st.markdown('<div class="top-navbar"><h1>⚡ Smart-Ombor ERP</h1></div>', unsafe_allow_html=True)

if "🛍️ Katalog" in menyu:
    st.subheader("Mahsulotlar Katalogi")
    st.table(ombor)

elif administrator_tasdiq:
    if menyu == "📊 Dashboard":
        st.subheader("Boshqaruv Paneli")
        col1, col2 = st.columns(2)
        col1.metric("Jami Mahsulot", len(ombor))
        col2.metric("Umumiy Qarz", f"{agentlar['Joriy Qarz'].sum():,.0f} UZS")
        
    elif menyu == "📦 Mahsulotlar":
        st.subheader("Mahsulotlar Qoldig'i")
        st.dataframe(ombor)
        
    elif menyu == "📥 Kirim":
        st.subheader("Yangi Kirim")
        with st.form("kirim_form"):
            nomi = st.text_input("Mahsulot nomi")
            miqdor = st.number_input("Miqdori", min_value=0.1)
            if st.form_submit_button("Saqlash"):
                yangi_qator = pd.DataFrame([{"Mahsulot Nomi": nomi, "Miqdori": miqdor, "O'lchov Birligi": "dona", "Narxi": 0, "Kategoriya": "Boshqa", "Rasm": ""}])
                ombor = pd.concat([ombor, yangi_qator], ignore_index=True)
                bazani_saqlash(ombor, kirim, chiqim, agentlar)
                st.success("Saqlandi!")
                st.rerun()

else:
    st.info("Iltimos, Admin rejimiga o'ting va parolni kiriting.")
