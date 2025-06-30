import streamlit as st
from fpdf import FPDF
import io

st.set_page_config(page_title="FASE 2 Health Check Boskalis International", layout="wide")

st.title("FASE 2 Health Check Boskalis International")

# Introductie
st.markdown("""
Vervolg modules geïndiceerd op grond van uitslagen Fase 1 PMO onderzoek
""")

# Persoonlijke Gegevens
st.header("Persoonlijke Gegevens")
naam = st.text_input("Naam deelnemer")
geboortedatum = st.date_input("Geboortedatum")
leeftijd = st.number_input("Leeftijd (jaren)", min_value=0, max_value=120)
geslacht = st.selectbox("Geslacht", ["Man", "Vrouw"])
divisie = st.selectbox("Divisie", ["CBS", "CS", "Salvage", "DR", "OE"])
subafdeling = st.text_input("Subafdeling")
datum = st.date_input("Datum")

# Relevante voorgeschiedenis
st.header("Relevante voorgeschiedenis")
voorgeschiedenis = st.text_area("Relevante voorgeschiedenis")
medicatie = st.text_area("Uw huidige medicatie gebruik")

# CARDIOVASCULAIR RISICOMANAGEMENT
st.header("CARDIOVASCULAIR RISICOMANAGEMENT")
st.markdown("""
**Wat is cardiovasculair risicomanagement?**  
Cardiovasculair risicomanagement (CVRM) is het geheel van maatregelen gericht op het beperken van risicofactoren bij mensen met een verhoogd risico.

**Wat is het doel van CVRM?**  
- Primaire preventie: nieuwe hart- en vaatziekten voorkomen  
- Secundaire preventie: complicaties of herhaling voorkomen bij mensen die al een hart- of vaatziekte hebben gehad

**Wat houdt CVRM in?**  
- Risico-inschatting (SCORE2)  
- Leefstijladviezen (stoppen met roken, gezonde voeding, valpreventie bij overgewicht, matig alcoholgebruik en stressreductie)  
- Regelmatige controle en begeleiding zoals monitoring door huisarts, praktijkondersteuner, diëtist of specialist.
""")

# SCORE2
st.header("SCORE2")
score2 = st.selectbox(
    "Tijdens de Health Check bij Boskalis heeft de Corporate Travel Clinic berekend dat uw individuele risico op hart- en vaatziekten in de komende 10 jaar",  
    ["normaal", "verhoogd", "te hoog"]
)
onder50 = st.radio("Bent u onder de 50 jaar?", ["Ja", "Nee"])
if onder50 == "Ja":
    kalender_leeftijd = st.number_input("Uw kalender leeftijd (jaar)", min_value=0)
    hartleeftijd = st.number_input("Uw hartleeftijd (jaar)", min_value=0)
lifetime = st.number_input(
    "Uw lifetime risico op hart- en vaatziekten volgens het LIFE-CVD2 model (%)",  
    min_value=0.0, max_value=100.0, format="%.2f"
)

# Risicofactoren
st.header("Risicofactoren op hart- en vaatziekte")
st.markdown("Om een goed beeld te krijgen van de risicofactoren die aanleiding gaven voor de Health Check, zijn bij u vastgesteld:")
rf_primair = {
    "Roken": st.checkbox("Roken"),
    "Cholesterol": st.checkbox("Cholesterol"),
    "Bloeddruk": st.checkbox("Bloeddruk"),
    "Glucose (suiker)": st.checkbox("Glucose (suiker)"),
    "Lichaamsgewicht": st.checkbox("Lichaamsgewicht")
}

st.markdown("Daarnaast is het goed om te weten dat er ook nog andere aandoeningen zijn die het toekomstige cardiovasculaire risico kunnen verhogen:")
other_rfs = [
    "Doorgemaakte hart- en vaatziekte", "Diabetes mellitus", "Chronische nierschade",
    "Belaste familie-anamnese voor premature HVZ", "Vermoeden erfelijke dyslipidemie",
    "Obesitas (BMI ≥ 30)", "COPD", "Reumatoide arthritis", "Arthritis psoriatica",
    "Ankyloserende spondylitis", "Jicht", "Maligniteiten", "HIV", "IBD",
    "OSAS (slaapapnoe)", "Vrouwen: Pre-eclampsie",
    "Zwangerschapshypertensie/-diabetes", "PCOS"
]
other_selected = {rf: st.checkbox(rf) for rf in other_rfs}

# Fietsproef
st.header("Fietsproef (ergometrie)")
vo2max = st.number_input("VO₂ max (ml/min/kg)", min_value=0.0, format="%.2f")
fiets_conclusie = st.radio("Conclusie fietsproef", ["Geen afwijkingen", "Afwijkingen, verder onderzoek nodig"])

# ROKEN - Longfunctie
st.header("ROKEN - Longfunctie")
sboog = st.radio("Heeft u lang gerookt?", ["Nee", "Incidenteel", "Structureel"])
longfunctie = st.radio("Longfunctie onderzoek", ["Normaal binnen grenzen", "Restrictieve stoornis"])

# Cholesterol profiel
st.header("Cholesterol profiel")
ldl = st.number_input("LDL-cholesterol (mmol/L)", format="%.2f")
totaal_chol = st.number_input("Totaal cholesterol (mmol/L)", format="%.2f")
streef_ldl = st.text_input("Streef LDL-gehalte (mmol/L)")
adv_chol = st.multiselect(
    "Advies cholesterol", ["Leefstijladviezen", "Cholesterol verlagend middel", "Contact huisarts"]
)

# BLOEDDRUK
st.header("BLOEDDRUK")
bp_syst = st.number_input("Systolische druk (mm Hg)", format="%.0f")
bp_diast = st.number_input("Diastolische druk (mm Hg)", format="%.0f")
bp_conclusie = st.radio("Bevinding bloeddruk", ["Normaal", "Verhoogd"])
ecg = st.radio("ECG afwijkingen", ["Wel afwijkingen", "Geen afwijkingen"])
urine = st.radio("Urine afwijkingen", ["Wel afwijkingen", "Geen afwijkingen"])
adv_bp = st.multiselect("Advies bloeddruk", ["Leefstijladviezen", "Medicatie", "Contact huisarts"])

# BLOEDSUIKER
st.header("BLOEDSUIKER")
suiker_concl = st.selectbox("Status", ["Normaal", "Pre-diabetes", "Diabetes mellitus"])
adv_suiker = st.multiselect(
    "Advies bloedsuiker", ["Leefstijladviezen", "Bloedsuikerverlagende medicatie", "Contact huisarts" ]
)

# GEWICHT
st.header("GEWICHT")
bmi = st.number_input("BMI", format="%.1f")
taille = st.number_input("Buikomvang (cm)", format="%.1f")
comorbid = st.radio("Co-morbiditeiten aanwezig?", ["Nee", "Ja"] )
ggr = st.text_input("GGR score")
glucose = st.number_input("Glucose steekproef (mmol/L)", format="%.2f")
hand_links = st.number_input("Handknijpkracht links (kg)", format="%.1f")
hand_rechts = st.number_input("Handknijpkracht rechts (kg)", format="%.1f")
sarcopenie = st.radio("Er is bij u sprake van sarcopenie", ["Wel", "Geen", "Mogelijk"] )

st.markdown("""
De belangrijkste aandachtspunten om overgewicht te verminderen zijn vooral gericht op het:
- Aanpassen van uw leefstijl, in het bijzonder uw dieet
- Stimuleren van (meer) bewegen. Hiervoor is uw PAL factor van belang.
""")
pal = st.selectbox("PAL factor", ["<1.4 (zeer laag)", "1.4-1.6 (laag)", "1.6-1.8 (matig)", ">1.8 (hoog)"])
bmr = st.number_input("Basale metabolisme (kcal/dag)", format="%.0f")
cal_need = st.number_input("Totale calorische behoefte (kcal/dag)", format="%.0f")
intake_adv = st.number_input("Aanbevolen calorische inname bij afvallen (kcal/dag)", format="%.0f")

st.markdown("Uw persoonlijke advies om de impact van overgewicht op uw risico op hart- en vaatziekten te verminderen")
st.markdown("De calorische behoefte wordt geschat aan de hand van de basale metabolisme en totale behoefte zoals hierboven vermeld.")
st.markdown("Om de belangrijkste oorzaken van uw overgewicht vast te stellen, vragen wij u om de vragenlijst checkoorzakenovergewicht.nl in te vullen.")
st.markdown("Als u wilt afvallen dan is het advies om ongeveer 300-500 kcal onder uw behoefte te zitten; uw intake dan rond de bovenstaande aanbeveling zou moeten zijn.")
adv_gew = st.multiselect(
    "Advies gewicht", [
        "Leefstijladviezen (voeding, zout, verzadigde vetzuren, beweging)",
        "Basis Gecombineerde Leefstijlinterventie (GLI)",
        "Basis GLI (met aanvullende zorg)",
        "Gespecialiseerde GLI",
        "Contact huisarts"
    ]
)

# PDF-generatie
if st.button("Genereer PDF"):
    data = {
        "Naam deelnemer": naam,
        "Geboortedatum": str(geboortedatum),
        "Leeftijd": leeftijd,
        "Geslacht": geslacht,
        "Divisie": divisie,
        "Subafdeling": subafdeling,
        "Datum": str(datum),
        "Voorgeschiedenis": voorgeschiedenis,
        "Medicatie": medicatie,
        "SCORE2 risico": score2,
        **({k: v for k, v in rf_primair.items()}),
        **other_selected,
        "VO2max": vo2max,
        "Fietsconclusie": fiets_conclusie,
        "Roken historie": sboog,
        "Longfunctie": longfunctie,
        "LDL": ldl,
        "Totaal cholesterol": totaal_chol,
        "Streef LDL": streef_ldl,
        "Advies cholesterol": ", ".join(adv_chol),
        "Syst. druk": bp_syst,
        "Diast. druk": bp_diast,
        "BP bevinding": bp_conclusie,
        "ECG": ecg,
        "Urine": urine,
        "Advies BP": ", ".join(adv_bp),
        "Bloedsuiker status": suiker_concl,
        "Advies suiker": ", ".join(adv_suiker),
        "BMI": bmi,
        "Buikomvang": taille,
        "Comorbiditeiten": comorbid,
        "GGR score": ggr,
        "Glucose steekproef": glucose,
        "Handkracht L": hand_links,
        "Handkracht R": hand_rechts,
        "Sarcopenie": sarcopenie,
        "PAL": pal,
        "BMR": bmr,
        "Calorische behoefte": cal_need,
        "Aanbevolen intake": intake_adv,
        "Advies gewicht": ", ".join(adv_gew)
    }
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "FASE 2 Health Check Boskalis International", ln=True, align="C")
    pdf.ln(5)
    for key, value in data.items():
        pdf.cell(0, 8, f"{key}: {value}", ln=True)
    buffer = io.BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    st.download_button(
        "Download ingevuld formulier als PDF",
        buffer,
        file_name="health_check.pdf",
        mime="application/pdf"
    )

