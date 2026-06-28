import streamlit as st
import pandas as pd

st.set_page_config(page_title="Simulateur Concerts - Maison Madera", page_icon="🎤", layout="wide")

st.markdown("""
<style>
    .stMetric {background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);}
</style>
""", unsafe_allow_html=True)

st.title("🎤 Simulateur Concerts Privés - Maison Madera")
st.caption("Outil de simulation stratégique | Version Web avec TVA 18%")

# ==================== SECTION 1 ====================
st.markdown("### 1. Informations sur l'événement")

col1, col2, col3 = st.columns(3)
with col1:
    artiste = st.text_input("Artiste / DJ", value="Daraa J")
with col2:
    date_event = st.text_input("Date de l'événement", value="15/07/2026")
with col3:
    restaurant = st.text_input("Restaurant", value="Maison Madera")

# ==================== SECTION 2 : CATÉGORIES ====================
st.markdown("### 2. Catégories de Billets (Prix TTC)")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Entrée Simple**")
    nb_simple = st.number_input("Nombre", min_value=0, value=80, step=5)
    prix_simple = st.number_input("Prix TTC (FCFA)", min_value=0, value=15000, step=1000)

with col2:
    st.markdown("**Dîner + Concert**")
    nb_standard = st.number_input("Nombre", min_value=0, value=170, step=5)
    prix_standard = st.number_input("Prix TTC (FCFA)", min_value=0, value=25000, step=1000)

with col3:
    st.markdown("**Dîner + Concert VIP**")
    nb_vip = st.number_input("Nombre", min_value=0, value=50, step=5)
    prix_vip = st.number_input("Prix TTC (FCFA)", min_value=0, value=39340, step=1000)

ca_ttc = (nb_simple * prix_simple) + (nb_standard * prix_standard) + (nb_vip * prix_vip)
total_participants = nb_simple + nb_standard + nb_vip

# TVA
taux_tva = 0.18
ca_ht = ca_ttc / (1 + taux_tva)
tva_collectee = ca_ttc - ca_ht

# ==================== SECTION 3 : COÛTS ====================
st.markdown("### 3. Coûts de l'Événement")

col1, col2 = st.columns(2)

with col1:
    cachet = st.number_input("Cachet Artiste (FCFA)", value=2500000, step=50000)
    food = st.number_input("Food & Drink (FCFA)", value=1000000, step=50000)
    sono = st.number_input("Sono & Technique (FCFA)", value=900000, step=50000)

with col2:
    chaises = st.number_input("Chaises / Mobilier (FCFA)", value=300000, step=10000)
    hotesses = st.number_input("Hôtesses (FCFA)", value=100000, step=10000)
    serveurs = st.number_input("Serveurs extra (FCFA)", value=60000, step=5000)
    bracelets = st.number_input("Bracelets & Contrôle (FCFA)", value=120000, step=10000)

cout_total = cachet + food + sono + chaises + hotesses + serveurs + bracelets
cout_fixe = cachet + sono + chaises + hotesses + serveurs
cout_variable = food + bracelets

# ==================== RÉSULTATS ====================
st.markdown("### 4. Résultats Financiers (avec TVA 18%)")

col1, col2, col3, col4 = st.columns(4)

marge_brute = ca_ttc - cout_total
commission = round(marge_brute * 0.30)
benefice = marge_brute - commission

with col1:
    st.metric("CA TTC", f"{ca_ttc:,.0f} FCFA")
with col2:
    st.metric("CA Hors Taxe (HT)", f"{ca_ht:,.0f} FCFA")
with col3:
    st.metric("TVA Collectée (18%)", f"{tva_collectee:,.0f} FCFA", delta="À reverser")
with col4:
    st.metric("Bénéfice Net", f"{benefice:,.0f} FCFA", delta=f"{(benefice/ca_ttc)*100:.1f}%")

# ==================== SCÉNARIOS ====================
st.markdown("### 5. Scénarios Comparatifs (avec TVA)")

col1, col2, col3 = st.columns(3)
var_cons = col1.slider("Conservateur", 0.50, 1.0, 0.75, 0.05)
var_base = 1.0
var_opti = col3.slider("Optimiste", 1.0, 1.5, 1.20, 0.05)

def calc_scenario(var):
    ca_ttc_sc = ca_ttc * var
    ca_ht_sc = ca_ttc_sc / (1 + taux_tva)
    tva_sc = ca_ttc_sc - ca_ht_sc
    var_cost_sc = cout_variable * var
    total_cost_sc = cout_fixe + var_cost_sc
    marge_sc = ca_ttc_sc - total_cost_sc
    comm_sc = round(marge_sc * 0.30)
    benef_sc = marge_sc - comm_sc
    return int(total_participants * var), ca_ttc_sc, ca_ht_sc, tva_sc, total_cost_sc, marge_sc, comm_sc, benef_sc

p_c, ca_ttc_c, ca_ht_c, tva_c, cost_c, marge_c, comm_c, benef_c = calc_scenario(var_cons)
p_b, ca_ttc_b, ca_ht_b, tva_b, cost_b, marge_b, comm_b, benef_b = calc_scenario(var_base)
p_o, ca_ttc_o, ca_ht_o, tva_o, cost_o, marge_o, comm_o, benef_o = calc_scenario(var_opti)

data = {
    "Indicateur": ["Participants", "CA TTC", "CA HT", "TVA 18%", "Coûts Totaux", "Marge Brute", "Bénéfice Net"],
    "Conservateur": [p_c, f"{ca_ttc_c:,.0f}", f"{ca_ht_c:,.0f}", f"{tva_c:,.0f}", f"{cost_c:,.0f}", f"{marge_c:,.0f}", f"{benef_c:,.0f}"],
    "Base": [p_b, f"{ca_ttc_b:,.0f}", f"{ca_ht_b:,.0f}", f"{tva_b:,.0f}", f"{cost_b:,.0f}", f"{marge_b:,.0f}", f"{benef_b:,.0f}"],
    "Optimiste": [p_o, f"{ca_ttc_o:,.0f}", f"{ca_ht_o:,.0f}", f"{tva_o:,.0f}", f"{cost_o:,.0f}", f"{marge_o:,.0f}", f"{benef_o:,.0f}"]
}

st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)

# ==================== NÉGOCIATION ====================
st.markdown("### 6. Aide à la Négociation")

objectif = st.number_input("Objectif de Bénéfice Net souhaité (FCFA)", value=1500000, step=100000)

if benefice >= objectif:
    st.success(f"✅ Objectif atteint. Tu peux négocier une réduction du cachet.")
else:
    st.warning(f"⚠️ Objectif non atteint. Il faut réduire le cachet ou augmenter le CA.")

st.caption("Application Web - Maison Madera | TVA 18% incluse")