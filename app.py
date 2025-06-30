import streamlit as st
from fpdf import FPDF
import io

st.set_page_config(page_title="FASE 2 Health Check Boskalis International", layout="wide")

st.title("FASE 2 Health Check Boskalis International")

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
st.markdown("""
Voer hieronder de relevante voorgeschiedenis in:
- Jaar
- Medische probleem
- Opmerking
""")
voorgeschiedenis_jaren = st.text_area("Jaar/opmerkingen (per regel)")
medicatie = st.text_area("Uw huidige medicatie gebruik")

# CARDIOVASCULAIR RISICOMANAGEMENT
st.header("CARDIOVASCULAIR RISICOMANAGEMENT")
st.markdown("""
Wat is cardiovasculair risicomanagement?  
Cardiovasculair risicomanagement (CVRM) is het geheel van maatregelen en behandelingen dat gericht is op het voorkomen of beperken van hart- en vaatziekten (zoals een hartinfarct of beroerte), door het verminderen van risicofactoren bij mensen met een verhoogd risico.  

Wat is het doel van CVRM?  
- Nieuwe hart- en vaatziekten voorkomen (primaire preventie)  
- Ernstige complicaties of herhaling voorkomen bij mensen die al een hart- of vaatziekte hebben gehad (secundaire preventie)  

Wat houdt CVRM in?  
- Risico-inschatting: berekening van individuele 10‑jaars risico (SCORE2)  
- Leefstijladviezen: stoppen met roken, gezonde voeding (minder zout, verzadigd vet, suikers), voldoende lichaamsbeweging, afvallen bij overgewicht, matig alcoholgebruik, stressreductie  
- Medicatie indien nodig: bloeddrukverlagers, cholesterolverlagers, bloedverdunners, diabetesmedicatie  
- Regelmatige controle en begeleiding door huisarts, praktijkondersteuner, diëtist of specialist
""")

# SCORE2
st.header("SCORE2")
st.markdown("""
Tijdens de Health Check is uw persoonlijke 10‑jaars risico op hart- en vaatziekten berekend met SCORE2. Geef hieronder de uitkomst:
""")
score2 = st.selectbox("Uw SCORE2 uitkomst", ["normaal", "verhoogd", "te hoog"])

onder50 = st.radio("Bent u onder de 50 jaar?", ["Ja", "Nee"])
if onder50 == "Ja":
    kalender_leeftijd = st.number_input("Uw kalender leeftijd (jaar)", min_value=0)
    hartleeftijd = st.number_input("Uw hartleeftijd (jaar)", min_value=0)
lifetime = st.number_input("Lifetime risico (LIFE-CVD2 model, %)", min_value=0.0, max_value=100.0, format="%.2f")

# Risicofactoren
st.header("Risicofactoren op hart- en vaatziekte")
st.markdown("""
Om een goed beeld te krijgen zijn de volgende primaire risicofactoren vastgesteld:
""")
rf_primair = {rf: st.checkbox(rf) for rf in ["Roken", "Cholesterol", "Bloeddruk", "Glucose (suiker)", "Lichaamsgewicht"]}
st.markdown("""
Daarnaast kunnen ook deze aandoeningen uw risico verhogen:
""")
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
st.markdown("""
Om inzicht te krijgen in uw fysieke conditie is een inspanningsproef (fietsergometrie) verricht. De VO₂ max geeft aan hoeveel zuurstof uw lichaam maximaal kan verwerken en is een goede voorspeller van uw uithoudingsvermogen en cardiovasculaire gezondheid. Ook wordt uw hartactiviteit tijdens inspanning gemonitord om mogelijke ritmestoornissen of vernauwingen op te sporen.
""")
vo2max = st.number_input("VO₂ max (ml/min/kg)", min_value=0.0, format="%.2f")
conditie = st.selectbox("Conditie classificatie", ["zeer slecht", "slecht", "gemiddeld", "goed", "zeer goed", "uitstekend"])
fiets_conclusie = st.radio("Conclusie fietsproef", ["Geen afwijkingen", "Afwijkingen, verder onderzoek nodig"])

# ROKEN - Longfunctie
st.header("ROKEN - Longfunctie")
st.markdown("""
Roken bevat schadelijke stoffen die longen, hart en bloedvaten beschadigen en verhoogt het risico op kanker en hart- en vaatziekten. Passief roken is ook schadelijk. Onderstaand geeft uw rookhistorie en longfunctieonderzoek weer:
""")
sboog = st.radio("Heeft u lang gerookt?", ["Nee", "Incidenteel", "Structureel"])
longfunctie = st.radio("Longfunctie onderzoek", ["Binnen normale grenzen", "Restrictieve stoornis", "Obstructieve stoornis"])  
st.markdown("""
Uw persoonlijke advies om de impact van roken op uw cardiovasculaire risico te verminderen:
- Verwijzing stoppen-met-roken (niet-medicamenteuze ondersteuning): ikstopnu.nl, Stoplijn 0800-1995, Thuisarts.nl
- Verwijzing voor medicamenteuze ondersteuning
- Contact huisarts voor vervolg
""")

# Cholesterol profiel
st.header("Cholesterol profiel")
st.markdown("""
Het cholesterolgehalte beïnvloedt aderverkalking. LDL (‘slecht’) hoopt zich op in vaatwanden, HDL (‘goed’) voert cholesterol af naar de lever. Een te hoog LDL verhoogt hart- en vaatziekterisico.
""")
ldl = st.number_input("LDL-cholesterol (mmol/L)", format="%.2f")
totaal_chol = st.number_input("Totaal cholesterol (mmol/L)", format="%.2f")
streef_ldl = st.text_input("Streef LDL-gehalte (mmol/L)")
adv_chol = st.multiselect("Advies cholesterol", ["Leefstijladviezen", "Cholesterol verlagend middel", "Contact huisarts"] )
st.markdown("""
Uw persoonlijke advies om de impact van cholesterol te verminderen:
- Minder dierlijke producten, vervang verzadigde door onverzadigde vetten
- Zie Thuisarts.nl en Voedingscentrum apps
- Statines zoals simvastatine of pravastatine
- Contact huisarts voor vervolg
""")

# BLOEDDRUK
st.header("BLOEDDRUK")
st.markdown("""
Hypertensie: bovendruk >140 of onderdruk >90 mm Hg. Langdurige hoge druk beschadigt vaten, hart, nieren, hersenen en ogen. Vaak zonder klachten (‘stille moordenaar’).
""")
bp_syst = st.number_input("Systolische druk (mm Hg)", format="%.0f")
bp_diast = st.number_input("Diastolische druk (mm Hg)", format="%.0f")
bp_conclusie = st.radio("Bevinding", ["Optimaal", "Normaal", "Hoog normaal", "Graad 1", "Graad 2", "Graad 3", "Isol. systolische hypertensie"] )
ecg = st.radio("ECG afwijkingen", ["Geen afwijkingen", "Wel afwijkingen"])
urine = st.radio("Urine afwijkingen", ["Geen afwijkingen", "Wel afwijkingen"])
adv_bp = st.multiselect("Advies bloeddruk", ["Leefstijladviezen (zoutbeperking 6g/dag, matig alcohol)", "Medicatie (≥180 mm Hg)", "Contact huisarts"] )

# BLOEDSUIKER
st.header("BLOEDSUIKER")
st.markdown("""
Diabetes mellitus is een chronische stoornis in glucose‑regulatie. Type 1: geen insulineproductie. Type 2: insulineresistentie. Pre-diabetes is omkeerbaar.
""")
suiker1 = st.number_input("Bloedsuiker meting 1 (mmol/L)", format="%.2f")
suiker2 = st.number_input("Bloedsuiker meting 2 (mmol/L)", format="%.2f")
hba1c = st.number_input("HbA1c (mmol/mol)", format="%.0f")
suiker_concl = st.selectbox("Conclusie", ["Normaal", "Pre-diabetes", "Diabetes mellitus"]) 
advisering = st.multiselect("Advies bloedsuiker", ["Leefstijladviezen", "Metformine/Glicazide/GLP1-agonist/SGLT2-remmer", "Contact huisarts"]) 
st.markdown("""
Voor nier- en urinechecks: nierfunctie normaal/licht/sterk afwijkend en urine eiwit ja/nee.
""")

# GEWICHT
st.header("GEWICHT")
st.markdown("""
Overgewicht (BMI>25) en obesitas (BMI>30) verhogen risico op hart‑, vaatziekten, diabetes, artrose, slaapapneu, kanker en psychische klachten. Visceraal vet is metabool actief. Sarcopenie (spierverlies) kan samen voorkomen.
""")
bmi = st.number_input("BMI", format="%.1f")
taille = st.number_input("Buikomvang (cm)", format="%.1f")
comorbid = st.radio("Co-morbiditeiten aanwezig?", ["Nee", "Ja"] )
ggr = st.text_input("GGR score")
glucose = st.number_input("Glucose steekproef (mmol/L)", format="%.2f")
hand_links = st.number_input("Handknijpkracht links (kg)", format="%.1f")
hand_rechts = st.number_input("Handknijpkracht rechts (kg)", format="%.1f")
sarcopenie = st.radio("Sarcopenie status", ["Wel", "Geen", "Mogelijk"]) 

pal = st.selectbox("PAL factor", ["1.2 (zeer inactief)", "1.4-1.5 (zittend)", "1.6-1.7 (licht actief)", "1.8-1.9 (staand)", "2.0-2.4 (actief)", ">2.4 (extreem)"])
bmr = st.number_input("Basale metabolisme (kcal/dag)", format="%.0f")
totaal_behoefte = st.number_input("Totale energiebehoefte (kcal/dag)", format="%.0f")
intake_adv = st.number_input("Aanbevolen intake bij afvallen (kcal/dag)", format="%.0f")
adv_gew = st.multiselect("Advies gewicht", ["Leefstijladviezen (voeding, zout, vetten, beweging)", "Basis GLI", "GLI aanvullend", "Gespecialiseerde GLI", "Contact huisarts"] )

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
        "Voorgeschiedenis (jaar/probleem)": voorgeschiedenis_jaren,
        "Medicatie": medicatie,
        "SCORE2 risico": score2,
        **rf_primair,
        **other_selected,
        "Kalender leeftijd": onder50 and kalender_leeftijd or "",
        "Hartleeftijd": onder50 and hartleeftijd or "",
        "Lifetime risico": lifetime,
        "VO2 max": vo2max,
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
        "Hand links": hand_links,
        "Hand rechts": hand_rechts,
        "Sarcopenie": sarcopenie,
        "PAL factor": pal,
        "BMR": bmr,
        "Energiebehoefte": totaal_behoefte,
        "Intake advies": intake_adv,
        "Advies gewicht": ", ".join(adv_gew)
    }
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "FASE 2 Health Check Boskalis International", ln=True, align="C")
    pdf.ln(5)
    for key, value in data.items():
        pdf.cell(0, 6, f"{key}: {value}", ln=True)
    buffer = io.BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    st.download_button(
        "Download ingevuld formulier als PDF",
        buffer,
        file_name="health_check.pdf",
        mime="application/pdf"
    )
