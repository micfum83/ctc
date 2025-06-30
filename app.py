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

# ... [overige form velddefinities onveranderd] ...

# PDF-generatie

def generate_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    # Registreer en gebruik Unicode-capabele font
    font_path = os.path.join(os.path.dirname(__file__), "DejaVuSans.ttf")
    pdf.add_font("DejaVu", "", font_path, uni=True)
    pdf.set_font("DejaVu", size=12)

    pdf.cell(0, 10, "FASE 2 Health Check Boskalis International", ln=True, align="C")
    pdf.ln(5)
    for key, value in data.items():
        text = f"{key}: {value}"
        # breek regels indien nodig
        pdf.multi_cell(0, 6, text)
    buffer = io.BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer

if st.button("Genereer PDF"):
    # Verzamel alle data (zelfde als eerder)
    data = {
        "Naam": naam,
        "Geboortedatum": str(geboortedatum),
        "Leeftijd": leeftijd,
        "Geslacht": geslacht,
        "Divisie": divisie,
        "Subafdeling": subafdeling,
        "Datum": str(datum),
        # ... voeg hier alle andere velden toe zoals voorheen ...
    }
    pdf_buffer = generate_pdf(data)
    st.download_button("Download ingevuld formulier als PDF", pdf_buffer,
                       file_name="health_check.pdf", mime="application/pdf")
