import streamlit as st
from fpdf import FPDF
import io
import os

# Zorg dat 'DejaVuSans.ttf' in dezelfde map staat als dit script.
# Deze font ondersteunt Unicode (accenten, bullets, etc.).

st.set_page_config(page_title="FASE 2 Health Check Boskalis International", layout="wide")

st.title("FASE 2 Health Check Boskalis International")
st.markdown("""
Vervolg modules geïndiceerd op grond van uitslagen Fase 1 PMO onderzoek
""")

# Persoonlijke Gegevens in twee kolommen
col1, col2 = st.columns(2)
with col1:
    naam = st.text_input("Naam deelnemer", max_chars=50)
    geboortedatum = st.date_input("Geboortedatum")
    leeftijd = st.number_input("Leeftijd (jaren)", min_value=0, max_value=120)
    geslacht = st.selectbox("Geslacht", ["Man", "Vrouw"])
with col2:
    divisie = st.selectbox("Divisie", ["CBS", "CS", "Salvage", "DR", "OE"])
    subafdeling = st.text_input("Subafdeling", max_chars=50)
    datum = st.date_input("Datum")

# Relevante voorgeschiedenis
st.header("Relevante voorgeschiedenis")
voorgeschiedenis_jaren = st.text_area("Jaar/probleem/opmerking (per regel)", height=100)
medicatie = st.text_area("Uw huidige medicatie gebruik", height=80)

# CARDIOVASCULAIR RISICOMANAGEMENT
st.header("CARDIOVASCULAIR RISICOMANAGEMENT")
st.markdown("""
Wat is cardiovasculair risicomanagement?  
Cardiovasculair risicomanagement (CVRM) is het geheel van maatregelen en behandelingen dat gericht is op het voorkomen of beperken van hart- en vaatziekten (zoals een hartinfarct of beroerte), door het verminderen van risicofactoren bij mensen met een verhoogd risico.

Wat is het doel van CVRM?  
- Nieuwe hart- en vaatziekten voorkomen (primaire preventie)  
- Ernstige complicaties of herhaling voorkomen (secundaire preventie)

Wat houdt CVRM in?  
- Risico-inschatting: berekening van individuele 10-jaars risico (SCORE2)  
- Leefstijladviezen: stoppen met roken, gezonde voeding (minder zout, verzadigd vet, suikers), voldoende lichaamsbeweging, afvallen bij overgewicht, matig alcoholgebruik, stressreductie  
- Medicatie indien nodig: bloeddrukverlagers, cholesterolverlagers, bloedverdunners, diabetesmedicatie  
- Regelmatige controle en begeleiding door huisarts, praktijkondersteuner, diëtist of specialist
""")

# SCORE2
st.header("SCORE2")
score2 = st.selectbox("Uw SCORE2 uitkomst", ["normaal", "verhoogd", "te hoog"])
onder50 = st.radio("Bent u onder de 50 jaar?", ["Ja", "Nee"])
if onder50 == "Ja":
    kalender_leeftijd = st.number_input("Uw kalender leeftijd (jaar)", min_value=0)
    hartleeftijd = st.number_input("Uw hartleeftijd (jaar)", min_value=0)
lifetime = st.number_input("Lifetime risico (LIFE-CVD2 model, %)", min_value=0.0, max_value=100.0, format="%.2f")

# Risicofactoren
st.header("Risicofactoren op hart- en vaatziekte")
col1, col2 = st.columns(2)
with col1:
    rf_primair = {rf: st.checkbox(rf) for rf in ["Roken", "Cholesterol", "Bloeddruk", "Glucose (suiker)", "Lichaamsgewicht"]}
with col2:
    other_rfs = [
        "Doorgemaakte hart- en vaatziekte", "Diabetes mellitus", "Chronische nierschade",
        "Belaste familie-anamnese voor premature HVZ", "Vermoeden erfelijke dyslipidemie",
        "Obesitas (BMI ≥ 30)", "COPD", "Reumatoide arthritis", "Arthritis psoriatica",
        "Ankyloserende spondylitis", "Jicht", "Maligniteiten", "HIV", "IBD",
        "OSAS (slaapapnoe)", "Vrouwen: Pre-eclampsie", "Zwangerschapshypertensie/-diabetes", "PCOS"
    ]
    other_selected = {rf: st.checkbox(rf) for rf in other_rfs}

# Fietsproef
st.header("Fietsproef (ergometrie)")
col1, col2 = st.columns(2)
with col1:
    vo2max = st.number_input("VO₂ max (ml/min/kg)", min_value=0.0, format="%.2f")
with col2:
    conditie = st.selectbox("Conditie classificatie", ["zeer slecht", "slecht", "gemiddeld", "goed", "zeer goed", "uitstekend"])
fiets_conclusie = st.radio("Conclusie fietsproef", ["Geen afwijkingen", "Afwijkingen, verder onderzoek nodig"])

# ROKEN - Longfunctie
st.header("ROKEN - Longfunctie")
sboog = st.radio("Heeft u lang gerookt?", ["Nee", "Incidenteel", "Structureel"], index=0)
longfunctie = st.radio("Longfunctie onderzoek", ["Binnen normale grenzen", "Restrictieve stoornis", "Obstructieve stoornis"], index=0)

# Cholesterol profiel
st.header("Cholesterol profiel")
col1, col2 = st.columns(2)
with col1:
    ldl = st.number_input("LDL-cholesterol (mmol/L)", format="%.2f")
    totaal_chol = st.number_input("Totaal cholesterol (mmol/L)", format="%.2f")
with col2:
    streef_ldl = st.text_input("Streef LDL-gehalte (mmol/L)", max_chars=10)
    adv_chol = st.multiselect("Advies cholesterol", ["Leefstijladviezen", "Cholesterol verlagend middel", "Contact huisarts"])

# BLOEDDRUK
st.header("BLOEDDRUK")
col1, col2 = st.columns(2)
with col1:
    bp_syst = st.number_input("Systolische druk (mm Hg)", format="%.0f")
    bp_diast = st.number_input("Diastolische druk (mm Hg)", format="%.0f")
with col2:
    bp_conclusie = st.selectbox("Bevinding", ["Optimaal", "Normaal", "Hoog normaal", "Graad 1", "Graad 2", "Graad 3", "Isol. systolische hypertensie"])
ecg = st.radio("ECG afwijkingen", ["Geen afwijkingen", "Wel afwijkingen"])
urine = st.radio("Urine afwijkingen", ["Geen afwijkingen", "Wel afwijkingen"])
adv_bp = st.multiselect("Advies bloeddruk", ["Leefstijladviezen", "Medicatie", "Contact huisarts"])

# BLOEDSUIKER
st.header("BLOEDSUIKER")
col1, col2 = st.columns(2)
with col1:
    suiker1 = st.number_input("Meting 1 (mmol/L)", format="%.2f")
    suiker2 = st.number_input("Meting 2 (mmol/L)", format="%.2f")
with col2:
    hba1c = st.number_input("HbA1c (mmol/mol)", format="%.0f")
suiker_concl = st.selectbox("Conclusie", ["Normaal", "Pre-diabetes", "Diabetes mellitus"])
advisering = st.multiselect("Advies bloedsuiker", ["Leefstijladviezen", "Medicatie", "Contact huisarts"])

# GEWICHT
st.header("GEWICHT")
col1, col2, col3 = st.columns(3)
with col1:
    bmi = st.number_input("BMI", format="%.1f")
    taille = st.number_input("Buikomvang (cm)", format="%.1f")
with col2:
    comorbid = st.radio("Co-morbiditeiten aanwezig?", ["Nee", "Ja"])
    ggr = st.text_input("GGR score", max_chars=10)
with col3:
    glucose = st.number_input("Glucose steekproef (mmol/L)", format="%.2f")
hand_links = st.number_input("Handknijpkracht links (kg)", format="%.1f")
hand_rechts = st.number_input("Handknijpkracht rechts (kg)", format="%.1f")
