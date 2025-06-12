import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def calcul_honoraires_grille(investissement, paliers):
    fees = 0
    for min_, max_, fixe, taux in paliers:
        if investissement > min_:
            tranche = min(investissement, max_) - min_
            fees += fixe + taux * tranche
    return fees

st.title("Calculateur d'honoraires basé sur les paliers d'investissement")

default_paliers = [
    (0, 30000, 3600, 0.0),
    (30000, 45000, 0, 0.09),
    (45000, 60000, 0, 0.08),
    (60000, 90000, 0, 0.07),
    (90000, np.inf, 0, 0.06)
]

paliers = []
min_invest = 10000  # Palier d'investissement minimal

for i in range(len(default_paliers)):
    min_ = min_invest if i == 0 else paliers[i-1][1]
    max_ = st.number_input(
        f"Palier {i + 1} - Maximum (€)", 
        min_value=min_ + 1, 
        value=int(default_paliers[i][1]) if np.isfinite(default_paliers[i][1]) else 1000000,  # Utilisation d'un grand nombre si infini
        format='%d'
    )
    fixe = st.number_input(f"Palier {i + 1} - Fixe (€)", value=float(default_paliers[i][2]), format='%f')
    taux = st.number_input(f"Palier {i + 1} - Taux (%)", value=float(default_paliers[i][3]) * 100, format='%f') / 100
    paliers.append((min_, max_, fixe, taux))

investissements = np.arange(20000, 200000, 1000)
montants_honoraires = [calcul_honoraires_grille(i, paliers) for i in investissements]
pourcentages_honoraires = [calcul_honoraires_grille(i, paliers) / i * 100 for i in investissements]

fig, ax1 = plt.subplots(figsize=(10, 6))

color = 'tab:blue'
ax1.set_xlabel('Investissements publicitaires (€)')
ax1.set_ylabel('Montant honoraires (€)', color=color)
line1 = ax1.plot(investissements, montants_honoraires, color=color, label='Montant honoraires')
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('Pourcentage honoraires (%)', color=color)
line2 = ax2.plot(investissements, pourcentages_honoraires, color=color, label='% honoraires')
ax2.tick_params(axis='y', labelcolor=color)

ax1.grid(True, linestyle='--', alpha=0.7)
ax2.grid(True, linestyle=':', alpha=0.7)

# Ajouter des annotations tous les 20 000 €
step = 20000
for inv, mont, perc in zip(investissements, montants_honoraires, pourcentages_honoraires):
    if inv % step == 0:  # Tous les paliers de 20k€
        # Annotation pour les montants (axe gauche)
        ax1.annotate(f'{mont}€', 
                    xy=(inv, mont), 
                    xytext=(5, 5), 
                    textcoords='offset points',
                    fontweight='bold')
        
        # Annotation pour les pourcentages (axe droit)
        ax2.annotate(f'{perc:.1f}%', 
                    xy=(inv, perc), 
                    xytext=(5, -15), 
                    textcoords='offset points',
                    fontweight='bold')

lines = line1 + line2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=2)

plt.title('Grille dégressive des honoraires', pad=20, fontsize=14)
plt.tight_layout()

st.pyplot(fig)
