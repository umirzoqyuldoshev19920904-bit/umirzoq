import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Sahifa sozlamalari
st.set_page_config(page_title="Onlayn Omborxona", page_icon="📦", layout="wide")

# Fayllarni saqlash bazasi (Buni keyinchalik bulutli xizmatga ham ulash mumkin)
FAYL_OMBOR = "onlayn_ombor.xlsx"

# Dastlabki bazani tekshirish yoki yaratish
def bazani_yuklash():
    if os.path.exists(FAYL_OMBOR):
        try:
            ombor_df = pd.read_excel(FAYL_OMBOR, sheet_name="Ombor")
            kirim_df = pd.read_excel(FAYL_OMBOR, sheet_name="Kirim")
            chiqim_df = pd.read_excel(FAYL_OMBOR, sheet_name="Chiqim")
            return ombor_df, kirim_df, chiqim_df
        except Exception:
            pass
            
    ombor_df = pd.DataFrame(columns=["Mahsulot Nomi", "Miqdori", "O'lchov Birligi"])
    kirim_df = pd.DataFrame(columns=["Sana", "Mahsulot Nomi", "Miqdori", "Mas'ul"])
    chiqim_df = pd.DataFrame(columns=["Sana", "Mahsulot Nomi", "Miqdori", "Qabul qiluvchi"])
    return ombor_df, kirim_df, chiqim_df

def bazani_saqlash(ombor, kirim, chiqim):
    with pd.ExcelWriter(FAYL_OMBOR, engine="openpyxl") as writer:
        ombor.to_excel(writer, sheet_name="Ombor", index=False)
        kirim.to_excel(writer, sheet_name="Kirim", index=False)
        chiqim.to_excel(writer, sheet_name="Chiqim", index=False)

# Ma'lumotlarni yuklash
ombor, kirim, chiqim = bazani_yuklash()

# --- VEB DIZAYN ---
st.title("🏢 Shaxsiy Onlayn Omborxona Tizimi")
st.markdown("---")

# Yon panel (Sidebar) navigatsiyasi
menyu = st.sidebar.selectbox("Bo'limni tanlang:", ["📦 Ombor Qoldig'i", "📥 Kirim qilish", "📤 Chiqim qilish", "📊 Hisobotlar"])

# 1. OMBOR QOLDIG'I BO'LIMI
if menyu == "📦 Ombor Qoldig'i":
    st.subheader("Hozirda omborda mavjud mahsulotlar")
    
    # Qidiruv tizimi
    qidiruv = st.text_input("🔍 Mahsulot nomi bo'yicha qidirish...").strip().lower()
    
    if not ombor.empty:
        filtr_ombor = ombor.copy()
        if qidiruv:
            filtr_ombor = filtr_ombor[filtr_ombor["Mahsulot Nomi"].str.lower().str.contains(qidiruv)]
        
        # Vizual jadval
        st.dataframe(filtr_ombor, use_container_width=True)
        
        # Grafik chiqarish (Agar mahsulotlar ko'p bo'lsa)
        st.bar_chart(data=filtr_ombor, x="Mahsulot Nomi", y="Miqdori")
    else:
        st.warning("Omboringiz hozircha bo'sh! 'Kirim qilish' bo'limidan mahsulot qo'shing.")

# 2. KIRIM QILISH BO'LIMI
elif menyu == "📥 Kirim qilish":
    st.subheader("📥 Yangi mahsulot qabul qilish")
    
    with st.form("kirim_form"):
        nomi = st.text_input("Mahsulot nomi:").strip().capitalize()
        miqdori = st.number_input("Miqdori:", min_value=0.1, step=1.0)
        birligi = st.selectbox("O'lchov birligi:", ["dona", "kg", "litr", "metr", "quti"])
        masul = st.text_input("Mas'ul shaxs (Ismingiz):").strip().capitalize()
        
        submit = st.form_submit_button("Omborga qo'shish")
        
        if submit:
            if nomi and masul:
                # Omborni yangilash
                if nomi in ombor["Mahsulot Nomi"].values:
                    ombor.loc[ombor["Mahsulot Nomi"] == nomi, "Miqdori"] += miqdori
                else:
                    yangi_qator = pd.DataFrame([{"Mahsulot Nomi": nomi, "Miqdori": miqdori, "O'lchov Birligi": birligi}])
                    ombor = pd.concat([ombor, yangi_qator], ignore_index=True)
                
                # Kirim tarixini yozish
                sana = datetime.now().strftime("%Y-%m-%d %H:%M")
                yangi_kirim = pd.DataFrame([{"Sana": sana, "Mahsulot Nomi": nomi, "Miqdori": miqdori, "Mas'ul": masul}])
                kirim = pd.concat([kirim, yangi_kirim], ignore_index=True)
                
                bazani_saqlash(ombor, kirim, chiqim)
                st.success(f"✅ Muvaffaqiyatli: {miqdori} {birligi} '{nomi}' omborga qo'shildi!")
            else:
                st.error("Iltimos, barcha maydonlarni to'ldiring!")

# 3. CHIQIM QILISH BO'LIMI
elif menyu == "📤 Chiqim qilish":
    st.subheader("📤 Ombordan mahsulot chiqarish")
    
    if ombor.empty:
        st.warning("Omborda hech qanday mahsulot yo'q, avval kirim qiling!")
    else:
        with st.form("chiqim_form"):
            nomi = st.selectbox("Mahsulotni tanlang:", ombor["Mahsulot Nomi"].unique())
            
            # Tanlangan mahsulot qoldig'ini topish
            qoldiq = ombor.loc[ombor["Mahsulot Nomi"] == nomi, "Miqdori"].values[0]
            birligi = ombor.loc[ombor["Mahsulot Nomi"] == nomi, "O'lchov Birligi"].values[0]
            st.info(f"ℹ️ Ombordagi qoldiq: {qoldiq} {birligi}")
            
            miqdori = st.number_input("Chiqim miqdori:", min_value=0.1, max_value=float(qoldiq), step=1.0)
            qabul_qiluvchi = st.text_input("Kimga yoki Qayerga berildi:").strip().capitalize()
            
            submit = st.form_submit_button("Ombordan chiqarish")
            
            if submit:
                if qabul_qiluvchi:
                    # Miqdorni kamaytirish
                    ombor.loc[ombor["Mahsulot Nomi"] == nomi, "Miqdori"] -= miqdori
                    # Agar miqdor 0 bo'lib qolsa, ro'yxatdan o'chirish (ixtiyoriy)
                    ombor = ombor[ombor["Miqdori"] > 0]
                    
                    # Chiqim tarixini yozish
                    sana = datetime.now().strftime("%Y-%m-%d %H:%M")
                    yangi_chiqim = pd.DataFrame([{"Sana": sana, "Mahsulot Nomi": nomi, "Miqdori": miqdori, "Qabul qiluvchi": qabul_qiluvchi}])
                    chiqim = pd.concat([chiqim, yangi_chiqim], ignore_index=True)
                    
                    bazani_saqlash(ombor, kirim, chiqim)
                    st.success(f"✅ Muvaffaqiyatli: {miqdori} {birligi} '{nomi}' chiqarildi!")
                    st.rerun()
                else:
                    st.error("Iltimos, qabul qiluvchi ismini kiriting!")

# 4. HISTOBOTLAR BO'LIMI
elif menyu == "📊 Hisobotlar":
    st.subheader("📊 Kirim va Chiqim amallari tarixi")
    
    tab1, tab2 = st.tabs(["📥 Kirimlar Tarixi", "📤 Chiqimlar Tarixi"])
    
    with tab1:
        st.write("Barcha kirim qilingan mahsulotlar:")
        st.dataframe(kirim, use_container_width=True)
        
    with tab2:
        st.write("Barcha chiqim qilingan mahsulotlar:")
        st.dataframe(chiqim, use_container_width=True)
