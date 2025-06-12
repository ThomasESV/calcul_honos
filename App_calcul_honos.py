import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter
import io

# Configuration de la page
st.set_page_config(page_title="Générateur de grille honoraires", layout="wide")
st.title("📊 Grille d'honoraires dégressive")

# Fonction de calcul modifiée pour minimum 10 000 €
def calcul_honoraires(investissement, paliers):
    fees = 0
    for min_, max_, fixe, taux in paliers:
        if investissement > min_:
            tranche = min(investissement, max_) - max(min_, 10000)  # Modification ici
            if tranche > 0:  # Évite les tranches négatives
                fees += fixe + taux * tranche
    return fees

# Widgets pour saisir les paliers
with st.expander("🔧 Configurer les paliers", expanded=True):
    cols = st.columns([1,1,1,1,1])
    with cols[0]: st.markdown("**Seuil min**")
    with cols[1]: st.markdown("**Seuil max**")
    with cols[2]: st.markdown("**Montant fixe**")
    with cols[3]: st.markdown("**Taux**")
    with cols[4]: st.markdown("**Actions**")

    paliers = []
    for i in range(5):
        cols = st.columns([1,1,1,1,1])
        with cols[0]: 
            min_val = 10000 if i == 0 else 30000*i  # Définit 10k comme minimum
            min_ = cols[0].number_input(f"Min_{i}", value=min_val, min_value=10000, step=5000, label_visibility="collapsed")
        with cols[1]: 
            max_ = cols[1].number_input(f"Max_{i}", value=30000*(i+1) if i<4 else 999999, min_value=10000, step=5000, label_visibility="collapsed")
        with cols[2]: 
            fixe = cols[2].number_input(f"Fixe_{i}", value=3600 if i==0 else 0, min_value=0, step=100, label_visibility="collapsed")
        with cols[3]: 
            taux = cols[3].number_input(f"Taux_{i}", value=0.09 if i==1 else 0.0, min_value=0.0, max_value=1.0, step=0.01, format="%.2f", label_visibility="collapsed")
        paliers.append((min_, max_, fixe, taux))

# Paramètres du graphique
with st.sidebar:
    st.header("Paramètres")
    min_x = st.number_input("Montant min à afficher (€)", value=10000, step=1000)  # Nouveau paramètre
    max_x = st.number_input("Montant max à afficher (€)", value=150000, step=10000)
    pas_annotation = st.number_input("Intervalle d'annotation (€)", value=20000, step=5000)

# Génération des données (commence à min_x)
x = np.linspace(min_x, max_x, 500)  # Modification ici
y = np.array([calcul_honoraires(v, paliers) for v in x])
pourcentages = np.where(x > 0, y/x*100, 0)

# Création du graphique
fig, ax1 = plt.subplots(figsize=(10,6))
ax1.plot(x, y, color='#1f77b4', linewidth=2, label='Honoraires (€)')
ax2 = ax1.twinx()
ax2.plot(x, pourcentages, color='#ff7f0e', linestyle='--', label='Taux (%)')

# Annotations (débute à min_x)
for xi in range(int(min_x), int(max_x)+1, pas_annotation):  # Modification ici
    yi = calcul_honoraires(xi, paliers)
    pct = yi/xi*100 if xi>0 else 0
    ax1.annotate(f"{yi:,.0f}€", (xi, yi), textcoords="offset points", xytext=(0,10), ha='center', color="#1f77b4")
    ax2.annotate(f"{pct:.1f}%", (xi, pct), textcoords="offset points", xytext=(0,-15), ha='center', color="#ff7f0e")

# Mise en forme
ax1.set_xlabel("Investissements (€)")
ax1.set_ylabel("Honoraires (€)", color="#1f77b4")
ax2.set_ylabel("Taux (%)", color="#ff7f0e")
plt.title(f"Évolution des honoraires (à partir de {min_x:,.0f} €)")
plt.grid(True)

# Affichage
st.pyplot(fig)

# Fonction utilitaire pour l'export
def fig_to_bytes(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=120, bbox_inches="tight")
    buf.seek(0)
    return buf
