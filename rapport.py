import streamlit as st


st.title("Analyse aéronautique par Yellow Wings")

# onglets
tab1, tab2, tab3, tab4 = st.tabs(["Rapport prédictions", "Notebook 1", "Notebook 2", "Notebook 3"])

# onglet Rapport prédictions
with tab1:
    st.header("Rapport prédictions")
    st.write("""
    - Identifier des corrélations entre variables pour prédire les voyants
    - Construire un modèle prédisant les voyants après chaque vol
    - Si voyant prédit, prévoir 3 jours d'immobilisation pour contrôles et changement des pièces à +75% d'usure
    - Pour chaque vol, estimer le coût d'immobilisation selon le voyant
    - Comparer les coûts totaux dans différents scénarios
    - Optimiser le modèle pour maximiser les économies en maintenance
    - Proposer des axes de développement futur
    """)

# Notebook 1
with tab2:
    st.header("Notebook 1")
    st.write("Automatisation et mise à jour des datasets")
    st.write("""
    - Script pour récupérer automatiquement ces fichiers chaque jour
    - Mettre à jour les datasets composants et aéronefs selon les nouvelles données
    """)

# onglet Notebook 2
with tab3:
    st.header("Notebook 2")
    st.write("Analyse, visualisation et préparation des données")
    st.write("""
    - Analyser et visualiser l'évolution des dégradations et états des voyants
    """)

# onglet Notebook 3
with tab4:
    st.header("Notebook 3")
    st.write("Modélisation, prédictions et calcul des coûts")
    st.write("""
    - Identifier des corrélations entre variables pour prédire les voyants
    - Construire un modèle prédisant les voyants après chaque vol
    - Estimer le coût d'immobilisation selon le voyant
    - Comparer les coûts totaux dans différents scénarios
    - Optimiser le modèle pour maximiser les économies en maintenance
    - Proposer des axes de développement futur
    """)

# Footer ou informations supplémentaires
st.sidebar.header("Version Alpha Roadmap")
st.sidebar.write("Cela nous servira de guide, à remplir au fur et à mesure")