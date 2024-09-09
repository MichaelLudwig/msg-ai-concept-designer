import streamlit as st
import openAI_API
import word_export
import io
import json
import re
import unicodedata

# Funktion zum Initialisieren der session_state Variablen
def initialize_session_state():
    if 'new_title' not in st.session_state:
        st.session_state.new_title = ""
    if 'new_header' not in st.session_state:
        st.session_state.new_header = ""
    if 'new_content_focus' not in st.session_state:
        st.session_state.new_content_focus = ""
    if 'new_doctype' not in st.session_state:
        st.session_state.new_doctype = "Fachkonzept"
    if 'new_chapter_count' not in st.session_state:
        st.session_state.new_chapter_count = 8
    if 'new_word_count' not in st.session_state:
        st.session_state.new_word_count = 100
    if 'new_writing_style' not in st.session_state:
        st.session_state.new_writing_style = "msg Konzept"
    if 'new_context' not in st.session_state:
        st.session_state.new_context = ""
    if 'new_stakeholder' not in st.session_state:
        st.session_state.new_stakeholder = "Technisches Fachpersonal"
    if 'toc_list' not in st.session_state:
        st.session_state.toc_list = []
    if 'kapitel_header' not in st.session_state:
        st.session_state.kapitel_header = []
    if 'kapitel_info' not in st.session_state:
        st.session_state.kapitel_info = []
    if 'kapitel_inhalt' not in st.session_state:
        st.session_state.kapitel_inhalt = []
    if 'kapitel_prompt' not in st.session_state:
        st.session_state.kapitel_prompt = []
    if 'glossar' not in st.session_state:
        st.session_state.glossar = ""

# Initialisiere session_state
initialize_session_state()

st.set_page_config(layout="wide")
main_heading=st.title("AI Concept Designer")
#main_heading=st.title("Modulare Interaktive Konzept Erstellung (MIKE)")


#--Sidebar ---------------------------------------------------------------------------------------------------------------------------------------
st.sidebar.title("App-Steuerung")

#Schaltflächen für neues Dokument
st.sidebar.subheader("Neues Dokument", divider='grey')
newdoc_form = st.sidebar.form("newdoc_form_key")
st.session_state.new_title = newdoc_form.text_input("Dokumenttitel", value=st.session_state.new_title, help="Der Titel, den das Dokument haben soll")

document_types = ["Fachkonzept", "IT-Konzept", "Anforderungskonzept", 
    "Architekturkonzept", "Infrastrukturkonzept", "Migrationskonzept", "Deploymentkonzept", "Testkonzept", "Backupkonzept", "Schnittstellenkonzept", 
    "Sicherheitskonzept", "Rollen- und Rechtekonzept",  
    "Changemanagementkonzept", "Löschkonzept", "Verschlüsselungskonzept", "Datensicherungskonzept", 
    "Betriebsführungskonzept", "Betriebsführungshandbuch", "Notfallkonzept", 
    "Dokumentationskonzept", "Risikomanagementkonzept", "Compliancekonzept", "Qualitätsmanagementkonzept",
    "Schulungskonzept", "Kommunikationskonzept", "Benutzerhandbuch"]

default_index = document_types.index(st.session_state.new_doctype) if st.session_state.new_doctype in document_types else 0

st.session_state.new_doctype = newdoc_form.selectbox("Dokumenttyp", 
    options=document_types,
    index=default_index)

st.session_state.new_content_focus = newdoc_form.text_area("Inhaltlicher Schwerpunkt", value=st.session_state.new_content_focus, help="Nenne alle Aspekte, die im Dokument zwingend behandelt werden sollen. Sie werden nach Themen geclustert und im Output z.b. in Form von Kapiteln erscheinen")
st.session_state.new_chapter_count = newdoc_form.slider("Anzahl der Kapitel.", min_value=1, max_value=30, value=st.session_state.new_chapter_count)
new_submitted = newdoc_form.form_submit_button("Dokumentstruktur erstellen")


#Schaltflächen für die Kapitelbearbeitung 
st.sidebar.subheader("Kapitel Steuerelemente", divider='grey')  
#st.sidebar.markdown(f"[Zurück zum Inhaltsverzeichnis](#inhaltsverzeichnis)")
st.session_state.new_word_count = st.sidebar.slider("Anzahl der Wörter pro Kapitel.", min_value=50, max_value=1000, value=st.session_state.new_word_count, step=50)

writing_styles = ["msg Konzept", "Fachlich", "Technisch", "Akademisch", "Sarkastisch"]
default_style_index = writing_styles.index(st.session_state.new_writing_style) if st.session_state.new_writing_style in writing_styles else 0

st.session_state.new_writing_style = st.sidebar.selectbox(
    "Wähle den Schreibstil.",
    options=writing_styles,
    index=default_style_index
)

if st.session_state.new_writing_style == "msg Konzept":
    st.session_state.new_writing_style = "Schreibe den Text in einem formalen und strukturierten Stil, wie es in Konzepten üblich ist. Verwende präzise und sachliche Sprache mit klaren, kurzen Sätzen. Es wird eine objektive und distanzierte Haltung eingenommen. Der Text verzichtet auf persönliche Ansprache oder emotionalen Ausdruck und konzentriert sich stattdessen auf klare Darstellung von Informationen und Anweisungen. Der Text soll in der dritten Person Singular und im Präsens geschrieben sein."        
st.session_state.new_context = st.sidebar.text_area("Kontext", value=st.session_state.new_context, help="Nenne hier Dinge wie Branche und Größe des Kunden, vorhandene Infrastruktur (keine sensiblen Daten!), Ziel des Konzepts, etc.")
st.session_state.new_stakeholder = st.sidebar.text_input("Zielgruppe", value=st.session_state.new_stakeholder, help="Beschreibe die Leserschaft deines Dokuments, z.b. Admins, Management, C-Level, fachliche Leitung, etc.")


#Schaltflächen für den Word Export
st.sidebar.subheader("Word Export", divider='grey')

if st.sidebar.button("Glossar (re)generieren", key="Glossar"):
    st.session_state.glossar = openAI_API.generate_glossar(st.session_state.kapitel_inhalt)

if st.sidebar.button("Word Dokument generieren", key="word_export"):
        if 'glossar' not in st.session_state:
            st.session_state.glossar = openAI_API.generate_glossar(st.session_state.kapitel_inhalt)
        word_export.export_dokument_to_word(st.session_state.new_title, st.session_state.new_header, st.session_state.toc_list, st.session_state.kapitel_inhalt, st.session_state.glossar)


#Schaltflächen für den Export und import des aktuellen Bearbeitungsstands
st.sidebar.subheader("Projekt Speichern oder Laden", divider='grey')

# Funktion zum Speichern des SessionState in JSON und Download anbieten
def save_sessionstate_to_json():
    # SessionState in ein JSON-kompatibles Format umwandeln
    session_dict = {k: v for k, v in st.session_state.items() if v not in [False, True]}
    
    # JSON in einen BytesIO-Stream schreiben
    json_str = json.dumps(session_dict, indent=4)
    json_bytes = json_str.encode('utf-8')
    json_io = io.BytesIO(json_bytes)
    
    # Download-Button anzeigen
    st.sidebar.download_button(
        label="Aktuelles Projekt in Datei speichern",
        data=json_io,
        file_name="session_state.json",
        mime="application/json"
    )

# Download-Button anzeigen
save_sessionstate_to_json()

#-------Sessionstate setzen wenn Projekt importiert wurde -------------------
def upload_sessionstate_from_json(uploaded_file):
    if uploaded_file is not None:
        # JSON-Daten lesen und in den SessionState schreiben
        session_dict = json.load(uploaded_file)
        for key, value in session_dict.items():
            if key not in st.session_state:
                st.session_state[key] = value
        st.session_state.project_loaded = True
        return True
    return False

# JSON-Datei hochladen
uploaded_file = st.sidebar.file_uploader("Bestehendes Projekt per JSON Datei einlesen", type="json", key="project_uploader")

# Automatisch Projekt laden, wenn eine Datei hochgeladen wurde
if uploaded_file is not None and 'project_loaded' not in st.session_state:
    if upload_sessionstate_from_json(uploaded_file):
        st.sidebar.success("Projekt wurde erfolgreich geladen. Die Seite wird automatisch aktualisiert.")
        st.session_state.project_uploader = None  # Reset file uploader

# Überprüfen, ob ein Projekt geladen wurde und die Seite aktualisieren
if 'project_loaded' in st.session_state and st.session_state.project_loaded:
    del st.session_state.project_loaded




#--App Logik ---------------------------------------------------------------------------------------------------------------------------------------
# Konzeptinhaltsverzeichnis aus gegebenen Parametern per ChatBot erstellen lassen
if new_submitted:
    
    # Überschriften für Hauptbereich aus Parametern erzeugen
    st.session_state.new_header = st.session_state.new_doctype + ": " + st.session_state.new_title

    with st.spinner(text="Inhaltsverzeichnis wird erstellt ..."):
        # Inhaltsverzeichnis + Infotexte + Prompts aus Paramtetern per Chatbot erzeugen
        st.session_state.toc_list = openAI_API.generate_toc(st.session_state.new_doctype, st.session_state.new_title, st.session_state.new_content_focus, st.session_state.new_chapter_count)
    
    # Leere SessionState Elemente erzeugen die im Weiteren mit Inhalten gefüllt werden
    st.session_state.kapitel_header = [item["title"] for item in st.session_state.toc_list]
    st.session_state.kapitel_info = [item["help_text"] for item in st.session_state.toc_list]
    st.session_state.kapitel_prompt = [item["prompt_text"] for item in st.session_state.toc_list]
    st.session_state.kapitel_inhalt = [""] * len(st.session_state.toc_list)
    st.session_state.glossar = ""

    



#--Content Area ---------------------------------------------------------------------------------------------------------------------------------------

st.header(st.session_state.new_header, divider='grey') 

# Funktion zur Generierung von URL-freundlichen Ankern
def generate_anchor(text):
    # Entferne Umlaute und konvertiere zu ASCII
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
    # Konvertiere zu Kleinbuchstaben und ersetze Leerzeichen durch Bindestriche
    text = re.sub(r'\W+', '-', text.lower()).strip('-')
    return text

# Inhaltsverzeichnis mit Links zu Kapiteln erstellen
st.subheader("Inhaltsverzeichnis")
for i, item in enumerate(st.session_state.toc_list):
    title_text = item["title"]
    anchor = generate_anchor(title_text)
    st.markdown(f"- [{title_text}](#{anchor})")

# Erstellen der Webseiten-Struktur mit Überschriften, Infoboxen und Textboxen
for i, item in enumerate(st.session_state.toc_list):
    title_text = st.session_state.kapitel_header[i]
    anchor = generate_anchor(title_text)
    
    st.markdown(f'<a name="{anchor}"></a>', unsafe_allow_html=True)
    st.header(title_text)
    
    st.info(st.session_state.kapitel_info[i])
    st.session_state.kapitel_prompt[i] = st.text_area(f"Prompt zum generieren des Inhalts", value=st.session_state.kapitel_prompt[i], height=100, key=f"prompt_{i}")
    
    if st.button("Kapitel " + title_text + " generieren", key=f"button_chapter_{i}"):
        openAI_API.generate_chapter(title_text, st.session_state.kapitel_prompt[i], st.session_state.new_doctype, st.session_state.new_title, st.session_state.new_writing_style, st.session_state.new_word_count, st.session_state.new_context, st.session_state.new_stakeholder, i)
    
    st.session_state.kapitel_inhalt[i] = st.text_area(f"Textbaustein für {title_text}", value=st.session_state.kapitel_inhalt[i], height=300, key=f"inhalt_{i}")

if 'glossar' in st.session_state:
    st.header("Glossar")

    if st.session_state.glossar == "":
        st.write("Zur Erstellung des Glossars bitte die Schaltfläche im Navigationsbereich im Bereich Word Export benutzen.")
    
    st.write(st.session_state.glossar)

#if "toc_list" in st.session_state:
    #st.write(st.session_state.toc_list)
