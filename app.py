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

# Persoonlijke Gegevens
st.header("Persoonlijke Gegevens")
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
st.markdown("Voer hieronder de relevante voorgeschiedenis in:")
voorgeschiedenis_jaren = st.text_area("Jaar/probleem/opmerking (per regel)", height=100)
medicatie = st.text_area("Uw huidige medicatie gebruik", height=80)

# CARDIOVASCULAIR RISICOMANAGEMENT
st.header("CARDIOVASCULAIR RISICOMANAGEMENT")
st.markdown("""
Wat is cardiovasculair risicomanagement?  
Cardiovasculair risicomanagement (CVRM) is het geheel van maatregelen en behandelingen dat gericht is op het voorkomen of beperken van hart- en vaatziekten (zoals een hartinfarct of beroerte), door het verminderen van risicofactoren bij mensen met een verhoogd risico.

Wat is het doel van CVRM?  
- Nieuwe hart- en vaatziekten voorkomen (primaire preventie)  
- Ernstige complicaties of herhaling voorkomen bij mensen die al een hart- of vaatziekte hebben gehad (secundaire preventie)

Wat houdt CVRM in?  
- Risico-inschatting: berekening van individuele 10-jaars risico (SCORE2)  
- Leefstijladviezen: stoppen met roken, gezonde voeding (minder zout, verzadigd vet, suikers), voldoende lichaamsbeweging, afvallen bij overgewicht, matig alcoholgebruik, stressreductie  
- Medicatie indien nodig: bloeddrukverlagers, cholesterolverlagers, bloedverdunners, diabetesmedicatie  
- Regelmatige controle en begeleiding door huisarts, praktijkondersteuner, diëtist of specialist
""")

# SCORE2
st.header("SCORE2")
st.markdown("Geef hieronder uw berekende 10-jaars risico volgens SCORE2:")
score2 = st.selectbox("Uw SCORE2 uitkomst", ["normaal", "verhoogd", "te hoog"])
onder50 = st.radio("Bent u onder de 50 jaar?", ["Ja", "Nee"])
if onder50 == "Ja":
    kalender_leeftijd = st.number_input("Uw kalender leeftijd (jaar)", min_value=0)
    hartleeftijd = st.number_input("Uw hartleeftijd (jaar)", min_value=0)
lifetime = st.number_input("Lifetime risico (LIFE-CVD2 model, %)", min_value=0.0, max_value=100.0, format="%.2f")

# Risicofactoren
st.header("Risicofactoren op hart- en vaatziekte")
st.markdown("Selecteer alle risicofactoren die op u van toepassing zijn:")
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
st.markdown("Geef uw VO₂ max en conditie-classificatie:")
col1, col2 = st.columns(2)
with col1:
    vo2max = st.number_input("VO₂ max (ml/min/kg)", min_value=0.0, format="%.2f")
with col2:
    conditie = st.selectbox("Conditie classificatie", ["zeer slecht", "slecht", "gemiddeld", "goed", "zeer goed", "uitstekend"])
fiets_conclusie = st.radio("Conclusie fietsproef", ["Geen afwijkingen", "Afwijkingen, verder onderzoek nodig"])

# ROKEN - Longfunctie
st.header("ROKEN - Longfunctie")
st.markdown("Geef uw rookhistorie en longfunctie-resultaat:")
sboog = st.radio("Heeft u lang gerookt?", ["Nee", "Incidenteel", "Structureel"])
longfunctie = st.radio("Longfunctie onderzoek", ["Binnen normale grenzen", "Restrictieve stoornis", "Obstructieve stoornis"])
st.markdown("""
Advies om de impact van roken op uw cardiovasculaire risico te verminderen:
- Verwijzing stoppen-met-roken (ikstopnu.nl, Stoplijn 0800-1995)
- Medicamenteuze ondersteuning mogelijk
- Contact huisarts voor vervolg
""")

# Cholesterol profiel
st.header("Cholesterol profiel")
st.markdown("Vul de gemeten cholesterolwaarden in:")
col1, col2 = st.columns(2)
with col1:
    ldl = st.number_input("LDL-cholesterol (mmol/L)", format="%.2f")
    totaal_chol = st.number_input("Totaal cholesterol (mmol/L)", format="%.2f")
with col2:
    streef_ldl = st.text_input("Streef LDL-gehalte (mmol/L)", max_chars=10)
    adv_chol = st.multiselect("Advies cholesterol", ["Leefstijladviezen", "Cholesterol verlagend middel", "Contact huisarts"])
st.markdown("""
Advies ter verlaging van cholesterol:
- Minder verzadigde vetten, meer onverzadigde vetten
- Diëtist of Voedingscentrum apps
- Statines zoals simvastatine, pravastatine
- Contact huisarts
""")

# BLOEDDRUK
st.header("BLOEDDRUK")
st.markdown("Vul bovendruk, onderdruk en bevinding in:")
col1, col2 = st.columns(2)
with col1:
    bp_syst = st.number_input("Systolische druk (mm Hg)", format="%.0f")
    bp_diast = st.number_input("Diastolische druk (mm Hg)", format="%.0f")
with col2:
    bp_conclusie = st.selectbox("Bevinding", ["Optimaal", "Normaal", "Hoog normaal", "Graad 1", "Graad 2", "Graad 3", "Isol. systolische hypertensie"])
ecg = st.radio("ECG afwijkingen", ["Geen afwijkingen", "Wel afwijkingen"])
urine = st.radio("Urine afwijkingen", ["Geen afwijkingen", "Wel afwijkingen"])
adv_bp = st.multiselect("Advies bloeddruk", ["Leefstijladviezen", "Medicatie", "Contact huisarts"])
st.markdown("""
Advies bij hypertensie:
- Zoutinname <6g/dag, matig alcoholgebruik
- Medicatie bij hoge waarden
- Contact huisarts
""")

# BLOEDSUIKER
st.header("BLOEDSUIKER")
st.markdown("Vul bloedsuikermetingen en conclusie in:")
col1, col2 = st.columns(2)
with col1:
    suiker1 = st.number_input("Meting 1 (mmol/L)", format="%.2f")
    suiker2 = st.number_input("Meting 2 (mmol/L)", format="%.2f")
with col2:
    hba1c = st.number_input("HbA1c (mmol/mol)", format="%.0f")
suiker_concl = st.selectbox("Conclusie", ["Normaal", "Pre-diabetes", "Diabetes mellitus"])
advisering = st.multiselect("Advies bloedsuiker", ["Leefstijladviezen", "Metformine/Glicazide/GLP1/SGLT2", "Contact huisarts"])
st.markdown("""
Advies bij verhoogde bloedsuiker:
- Gezonde voeding, lichaamsbeweging
- Medicatie volgens richtlijnen
- Contact huisarts
""")

# GEWICHT
st.header("GEWICHT")
st.markdown("Vul lichaamsmaten en advies in:")
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
sarcopenie = st.selectbox("Sarcopenie status", ["Wel", "Geen", "Mogelijk"])
pal = st.selectbox("PAL factor", ["1.2 (zeer inactief)", "1.4-1.5 (zittend)", "1.6-1.7 (licht actief)", "1.8-1.9 (staand)", "2.0-2.4 (actief)", ">2.4 (extreem)"])
bmr = st.number_input("Basale metabolisme (kcal/dag)", format="%.0f")
totaal_behoefte = st.number_input("Totale energiebehoefte (kcal/dag)", format="%.0f")
intake_adv = st.number_input("Aanbevolen intake bij afvallen (kcal/dag)", format="%.0f")
adv_gew = st.multiselect("Advies gewicht", ["Leefstijladviezen", "Basis GLI", "GLI aanvullend", "Gespecialiseerde GLI", "Contact huisarts"])
st.markdown("""
Advies bij overgewicht:
- Dieet aanpassen, meer bewegen
- GLI-programma's
- Contact huisarts
""")

# PDF-generatie
def generate_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    font_path = os.path.join(os.path.dirname(__file__), "DejaVuSans.ttf")
    pdf.add_font("DejaVu", "", font_path, uni=True)
    pdf.set_font("DejaVu", size=12)
    pdf.cell(0, 10, "FASE 2 Health Check Boskalis International", ln=True, align="C")
    pdf.ln(5)
    for key, value in data.items():
        pdf.multi_cell(0, 6, f"{key}: {value}")
    buffer = io.BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer

if st.button("Genereer PDF"):
    data = {
        "Naam deelnemer": naam,
        "Geboortedatum": str(geboortedatum),
        "Leeftijd": leeftijd,
        "Geslacht": geslacht,
        "Divisie": divisie,
        "Subafdeling": subafdeling,
        "Datum": str(datum),
        **rf_primair,
        **other_selected,
        **({"Uw kalender leeftijd": kalender_leeftijd, "Uw hartleeftijd": hartleeftijd} if onder50 == "Ja" else {}),
        "Lifetime risico": lifetime,
        "VO₂ max": vo2max,
        "Conditie": conditie,
        "Fiets conclusie": fiets_conclusie,
        "Rookhistorie": sboog,
        "Longfunctie": longfunctie,
        "LDL": ldl,
        "Totaal cholesterol": totaal_chol,
        "Streef LDL": streef_ldl,
        "Advies cholesterol": ", ".join(adv_chol),
        "BP systolisch": bp_syst,
        "BP diastolisch": bp_diast,
        "BP bevinding": bp_conclusie,
        "ECG afwijkingen": ecg,
        "Urine afwijkingen": urine,
        "Advies BP": ", ".join(adv_bp),
        "Bloedsuiker metingen": f"{suiker1}, {suiker2}, HbA1c {hba1c}",
        "Suiker status": suiker_concl,
        "Advies suiker": ", ".join(advisering),
        "BMI": bmi,
        "Buikomvang": taille,
        "Co-morbiditeiten": comorbid,
        "GGR score": ggr,
        "Glucose steekproef": glucose,
        "Handknijpkracht links": hand_links,
        "Handknijpkracht rechts": hand_rechts,
        "Sarcopenie status": sarcopenie,
        "PAL factor": pal,
        "Basale metabolisme": bmr,
        "Totale energiebehoefte": totaal_behoefte,
        "Aanbevolen intake": intake_adv,
        "Advies gewicht": ", ".join(adv_gew)
    }
    buffer = generate_pdf(data)
    st.download_button("Download ingevuld formulier als PDF", buffer, file_name="health_check.pdf", mime="application/pdf")
