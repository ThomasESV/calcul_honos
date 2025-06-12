import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO

# Configuration minimale
st.set_page_config(layout="wide")
st.title("Grille d'honoraires simplifiée")

# Fonction de calcul modifiée
def calcul_honoraires(inv, paliers):
    fees = 0
    for min_, max_, fixe, taux in paliers:
        if inv > min_:
            tranche = min(inv, max_) - max(min_, 10000)
            fees += fixe + taux * tranche if tranche > 0 else 0
    return fees

# Interface simplifiée
paliers = [
    (10000, 30000, 3600, 0),
    (30000, 45000, 0, 0.09),
    (45000, 60000, 0, 0.08)
]

max_x = st.slider("Plage d'affichage (k€)", 10, 200, 150)
x = np.linspace(10000, max_x*1000, 300)
y = [calcul_honoraires(v, paliers) for v in x]

# Graphique minimal
fig, ax = plt.subplots()
ax.plot(x, y, color='blue')
ax.set_xlabel("Investissement (€)")
ax.set_ylabel("Honoraires (€)", color='blue')

# Export direct sans pandas
buf = BytesIO()
plt.savefig(buf, format='png')
st.image(buf, caption="Graphique des honoraires")