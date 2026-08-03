import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Plenhyage 25 Simülatörü", layout="wide")
st.title("💉 Plenhyage 25 - Karar Destek & Kârlılık Simülatörü")
st.markdown("Bu interaktif simülatör, **Plenhyage 25** ürününün biyolojik verimlilik skoru (BEI) ile aylık net kârlılığını hesaplar.")
st.divider()

st.sidebar.header("⚙️ Simülasyon Parametreleri")
patient_count = st.sidebar.slider("Aylık Target Hasta Sayısı", 1, 50, 10, 1)
session_price = st.sidebar.number_input("Hastadan Alınan Seans Ücreti (TL)", value=4500, step=250)
box_cost = st.sidebar.number_input("Kliniğe Ürün Maliyeti (TL)", value=1800, step=100)
sessions_per_patient = st.sidebar.slider("Hasta Başı Ortalama Seans Sayısı", 1, 4, 2, 1)

p25_conc, p25_mw, p25_visc, p25_std_sessions, p25_cost_index = 25.0, 2500, 55.0, 2.5, 1.2
bei_score = round((p25_conc * (p25_mw / 1000.0) * (p25_visc / 20.0)) / (p25_std_sessions * p25_cost_index), 2)

gross_revenue = patient_count * sessions_per_patient * session_price
total_cost = patient_count * sessions_per_patient * box_cost
net_profit = gross_revenue - total_cost
roi_margin = (net_profit / gross_revenue) * 100 if gross_revenue > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("🧬 Plenhyage 25 BEI Skoru", f"{bei_score} / 60")
col2.metric("💰 Toplam Brüt Ciro", f"{gross_revenue:,.0f} TL")
col3.metric("📉 Toplam Ürün Maliyeti", f"{total_cost:,.0f} TL")
col4.metric("🚀 Aylık Net Klinik Kârı", f"{net_profit:,.0f} TL", delta=f"%{roi_margin:.1f} Kâr Marjı")

st.divider()

with st.expander("ℹ️ BEI (Biyolojik Verimlilik Skoru) Nasıl Hesaplanmaktadır?"): 
    st.markdown('''
    **BEI (Biological Efficiency Index)** formülü, ürünün hücresel düzeydeki verimini ölçer:
    
    $$\\text{BEI} = \\frac{\\text{Konsantrasyon (mg/ml)} \\times \\left(\\frac{\\text{Molekül Ağırlığı (kDa)}}{1000}\\right) \\times \\left(\\frac{\\text{Viskozite (cP)}}{20}\\right)}{\\text{Standart Seans Sayısı} \\times \\text{Maliyet İndeksi}}$$
    
    * **Plenhyage 25 Parametreleri:** $25\\text{ mg/ml (Konsantrasyon)} \\times 2.5\\text{ (MW İndeksi)} \\times 2.75\\text{ (Viskozite İndeksi)} / (2.5 \\times 1.2) = \\mathbf{57.29}$
    ''')

st.divider()

col_left, col_right = st.columns([1, 1])
with col_left:
    st.subheader("📊 Aylık Finansal Dağılım")
    fig, ax = plt.subplots(figsize=(6, 4))
    categories = ['Ürün Maliyeti', 'Net Kâr']
    values = [total_cost, net_profit]
    ax.bar(categories, values, color=['#ff6b6b', '#51cf66'], width=0.5)
    ax.set_ylabel("TL")
    for i, v in enumerate(values):
        ax.text(i, v / 2 if v > 0 else 0, f"{v:,.0f} TL", ha='center', va='center', color='white', fontweight='bold', fontsize=12)
    st.pyplot(fig)

with col_right:
    st.subheader("📋 Simülasyon Özeti")
    st.write(f"- **Hedeflenen Hasta:** {patient_count} kişi / ay")
    st.write(f"- **Toplam Uygulanan Seans:** {int(patient_count * sessions_per_patient)} seans")
    st.write(f"- **Seans Başı Net Kâr:** {session_price - box_cost:,.0f} TL")
    st.write(f"- **Klinik Verimlilik Oranı:** %{roi_margin:.2f}")
