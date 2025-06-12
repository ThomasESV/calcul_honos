import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Configuration de la page
st.set_page_config(page_title="Générateur de grille honoraires", layout="wide")
st.title("📊 Grille d'honoraires dégressive")

# Fonction de calcul (identique à votre logique)
def calcul_honoraires(investissement, paliers):
    fees = 0
    for min_, max_, fixe, taux in paliers:
        if investissement > min_:
            tranche = min(investissement, max_) - min_
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
    for i in range(5):  # 5 lignes modifiables
        cols = st.columns([1,1,1,1,1])
        with cols[0]: min_ = cols[0].number_input(f"Min_{i}", value=30000*i, min_value=0, step=5000, label_visibility="collapsed")
        with cols[1]: max_ = cols[1].number_input(f"Max_{i}", value=30000*(i+1) if i<4 else 999999, min_value=0, step=5000, label_visibility="collapsed")
        with cols[2]: fixe = cols[2].number_input(f"Fixe_{i}", value=3600 if i==0 else 0, min_value=0, step=100, label_visibility="collapsed")
        with cols[3]: taux = cols[3].number_input(f"Taux_{i}", value=0.09 if i==1 else 0.0, min_value=0.0, max_value=1.0, step=0.01, format="%.2f", label_visibility="collapsed")
        with cols[4]: 
            if cols[4].button("✕", key=f"del_{i}"):
                continue  # Pour supprimer une ligne (implémentation avancée)
        paliers.append((min_, max_, fixe, taux))

# Paramètres du graphique
with st.sidebar:
    st.header("Paramètres")
    max_x = st.number_input("Montant max à afficher (€)", value=150000, step=10000)
    pas_annotation = st.number_input("Intervalle d'annotation (€)", value=20000, step=5000)

# Génération des données
x = np.linspace(10000, max_x, 500)
y = np.array([calcul_honoraires(v, paliers) for v in x])
pourcentages = np.where(x > 0, y/x*100, 0)

# Création du graphique
fig, ax1 = plt.subplots(figsize=(10,6))
ax1.plot(x, y, color='#1f77b4', linewidth=2, label='Honoraires (€)')
ax2 = ax1.twinx()
ax2.plot(x, pourcentages, color='#ff7f0e', linestyle='--', label='Taux (%)')

# Annotations
for xi in range(0, int(max_x)+1, pas_annotation):
    yi = calcul_honoraires(xi, paliers)
    pct = yi/xi*100 if xi>0 else 0
    ax1.annotate(f"{yi:,.0f}€", (xi, yi), textcoords="offset points", xytext=(0,10), ha='center', color="#1f77b4")
    if xi > 0:
        ax2.annotate(f"{pct:.1f}%", (xi, pct), textcoords="offset points", xytext=(0,-15), ha='center', color="#ff7f0e")

# Mise en forme
ax1.set_xlabel("Investissements (€)")
ax1.set_ylabel("Honoraires (€)", color="#1f77b4")
ax2.set_ylabel("Taux (%)", color="#ff7f0e")
plt.title("Évolution des honoraires par palier")
plt.grid(True)

# Affichage dans Streamlit
st.pyplot(fig)
