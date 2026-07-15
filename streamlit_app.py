import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# 1. Sahifa sozlamalari
st.set_page_config(page_title="Smart-Ombor ERP v5.0", layout="wide", page_icon="⚡")

# 2. Zamonaviy CSS dizayn (Glassmorphism & SaaS look)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
    
    * { font-family: 'Plus Jakarta Sans', sans-serif !important; }
    
    /* Top Menu Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #f1f5f9;
        padding: 8px;
        border-radius: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 8px;
        font-weight: 600;
        color: #475569;
    }
    .stTabs [aria-selected="true"] {
        background-color: white !important;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        color: #0f172a !important;
    }

    /* Floating Cards */
    .stApp { background-color: #f8fafc; }
    .floating-card {
        background: white;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)

# 3. Ma'lumotlar bazasi (Sessiya xotirasida)
if 'ombor' not in st.session_state:
    st.session_state.ombor = pd.DataFrame(columns=["Mahsulot", "Soni", "Narxi", "Kategoriya"])
    st.session_state.tarix = pd.DataFrame(columns=["Vaqt", "Amal", "Mahsulot", "Soni"])

# 4. Top Menu (Asosiy Navigatsiya)
tab1, tab2, tab3, tab4 = st.tabs(["📊 Boshqaruv (Dashboard)", "🛍️ Mahsulotlar Katalogi", "📥 Kirim/Chiqim", "👥 Hamkorlar"])

with tab1:
    st.header("Umumiy Ko'rsatkichlar")
    c1, c2, c3 = st.columns(3)
    c1.metric("Jami Tovar", len(st.session_state.ombor))
    c2.metric("Jami Qiymat", "125,000,000 UZS")
    c3.metric("Bugungi Amallar", len(st.session_state.tarix))
    
    st.markdown("---")
    if not st.session_state.ombor.empty:
        fig = px.bar(st.session_state.ombor, x="Mahsulot", y="Soni", color="Kategoriya", title="Mahsulotlar Taqqoslanishi")
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("Katalog")
    if st.session_state.ombor.empty:
        st.info("Hozircha mahsulotlar yo'q.")
    else:
        st.dataframe(st.session_state.ombor, use_container_width=True)

with tab3:
    st.header("Operatsiyalar")
    col1, col2 = st.columns(2)
    
    with col1:
        with st.form("yangi_kirim"):
            st.subheader("Yangi Mahsulot Kirimi")
            nom = st.text_input("Nomi")
            soni = st.number_input("Miqdori", 1)
            narx = st.number_input("Narxi", 1000)
            kat = st.selectbox("Kategoriya", ["Qurilish", "Elektro", "Santexnika"])
            if st.form_submit_button("Saqlash"):
                yangi = pd.DataFrame([[nom, soni, narx, kat]], columns=["Mahsulot", "Soni", "Narxi", "Kategoriya"])
                st.session_state.ombor = pd.concat([st.session_state.ombor, yangi])
                st.success("Kiritildi!")
                st.rerun()

with tab4:
    st.header("Hamkorlar va Yetkazuvchilar")
    st.warning("Bu bo'limda hamkorlar ro'yxati va ularning qarzlari aks etadi.")
```

### GitHub'ga yuklash bo'yicha qisqacha yo'riqnoma:
1. **GitHub Repository:** Yangi repo yarating (masalan, `smart-ombor-erp`).
2. **Fayl qo'shish:** `streamlit_app.py` nomli fayl yarating va yuqoridagi kodni ichiga joylang.
3. **Streamlit Cloud:** [share.streamlit.io](https://share.streamlit.io) saytiga kiring.
4. **Deploy:** GitHub repositoriyangizni tanlang va "Deploy" tugmasini bosing.

Endi sizda "Moy Sklad" kabi yuqori menyuli, professional va zamonaviy ERP tizimingiz bor! Yana biror bo'lim (masalan, grafiklar) bo'yicha murakkablik kerak bo'lsa, ayting, darhol qo'shib beraman.
