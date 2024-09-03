import streamlit as st
import openAI_API
import word_export
import io
import json

 

        

st.set_page_config(layout="wide")
main_heading=st.title("AI Concept Designer")
#main_heading=st.title("Modulare Interaktive Konzept Erstellung (MIKE)")


#--Sessionstate Handling ---------------------------------------------------------------------------------------------------------------------------------------
if 'new_title' not in st.session_state:
    st.session_state.new_title = ""
if 'new_header' not in st.session_state:
    st.session_state.new_header = ""
if 'toc_list' in st.session_state:
    toc_list=st.session_state.toc_list
else:
    toc_list=[]



#--Sidebar ---------------------------------------------------------------------------------------------------------------------------------------
st.sidebar.title("App-Steuerung")

#Schaltflächen für neues Dokument
st.sidebar.subheader("Neues Dokument", divider='grey')
newdoc_form = st.sidebar.form("newdoc_form_key")
st.session_state.new_title = newdoc_form.text_input("Dokumenttitel")
new_doctype = newdoc_form.selectbox("Dokumenttyp",
    ["Fachkonzept", "IT-Konzept", "Anforderungskonzept", 
    # "Marktanalyse",
    "Architekturkonzept", "Infrastrukturkonzept", "Migrationskonzept", "Deploymentkonzept", "Testkonzept", "Backupkonzept", "Schnittstellenkonzept", 
    "Sicherheitskonzept", "Rollen- und Rechtekonzept",  
    #"Datenschutzkonzept", "Datenschutzerklärung", "Schutzbedarfsfeststellung (nach BSI Grundschutz)", "Auftragsverarbeitungs-Vertrag", "Verzeichnis von Verarbeitungstätigkeiten", "Datenschutzfolgeabschätzung",
    "Changemanagementkonzept", "Löschkonzept", "Verschlüsselungskonzept", "Datensicherungskonzept", 
    "Betriebsführungskonzept", "Betriebsführungshandbuch", "Notfallkonzept", 
    "Dokumentationskonzept", "Risikomanagementkonzept", "Compliancekonzept", "Qualitätsmanagementkonzept",
    "Schulungskonzept", "Kommunikationskonzept", "Benutzerhandbuch"])
st.session_state.new_content_focus = ""
st.session_state.new_content_focus = newdoc_form.text_area("Inhaltlicher Schwerpunkt", value=st.session_state.new_content_focus)
new_chapter_count = newdoc_form.slider("Anzahl der Kapitel.", min_value=1, max_value=30, value=8)
new_submitted = newdoc_form.form_submit_button("Dokumentstruktur erstellen")


#Schaltflächen für die Kapitelbearbeitung 
st.sidebar.subheader("Kapitel Steuerelemente", divider='grey')  
#st.sidebar.markdown(f"[Zurück zum Inhaltsverzeichnis](#inhaltsverzeichnis)")
new_word_count = st.sidebar.slider("Anzahl der Wörter pro Kapitel.", min_value=50, max_value=1000, value=100, step=50)
new_writing_style = st.sidebar.selectbox("Wähle den Schreibstil.", ["msg Konzept", "Fachlich", "Technisch", "Akademisch", "Sarkastisch"])
if new_writing_style == "msg Konzept":
    new_writing_style = "Schreibe den Text in einem formalen und strukturierten Stil, wie es in Konzepten üblich ist. Verwende präzise und sachliche Sprache mit klaren, kurzen Sätzen. Es wird eine objektive und distanzierte Haltung eingenommen. Der Text verzichtet auf persönliche Ansprache oder emotionalen Ausdruck und konzentriert sich stattdessen auf klare Darstellung von Informationen und Anweisungen. Der Text soll in der dritten Person Singular und im Präsens geschrieben sein."        
new_context = st.sidebar.text_area("Kontext")
new_stakeholder = st.sidebar.text_input("Zielgruppe", value="Technisches Fachpersonal")


#Schaltflächen für den Word Export
st.sidebar.subheader("Word Export", divider='grey')

if st.sidebar.button("Glossar (re)generieren", key="Glossar"):
    st.session_state.glossar = openAI_API.generate_glossar(st.session_state.kapitel_inhalt)

if st.sidebar.button("Word Dokument generieren", key="word_export"):
        if 'glossar' not in st.session_state:
            st.session_state.glossar = openAI_API.generate_glossar(st.session_state.kapitel_inhalt)
        word_export.export_dokument_to_word(st.session_state.new_title, st.session_state.new_header, st.session_state.toc_list, st.session_state.kapitel_inhalt, st.session_state.glossar)


#Schaltflächen zum Speichern des aktuellen Projektes




#--App Logik ---------------------------------------------------------------------------------------------------------------------------------------
# Konzeptinhaltsverzeichnis aus gegebenen Parametern per ChatBot erstellen lassen
if new_submitted:
    
    # Überschriften für Hauptbereich aus Parametern erzeugen
    #st.header(new_doctype + ": " + new_title, divider='grey')    
    #st.session_state.new_title = new_title
    st.session_state.new_header = new_doctype + ": " + st.session_state.new_title

    with st.spinner(text="Inhaltsverzeichnis wird erstellt ..."):

    #Inhaltsverzeichnis + Infotexte + Prompts aus Paramtetern per Chatbot erzeugen
        toc_list = openAI_API.generate_toc(new_doctype, st.session_state.new_title, new_content_focus, new_chapter_count)
    
    #Leere SessionState Elemente erzeugen die im Weiteren mit Inhalten gefüllt werden, die über die gesamte Session erhalen bleiben sollen (da häufige Page Reloads)
    st.session_state.toc_list = toc_list
    st.session_state.kapitel_header = [""] * len(toc_list)
    st.session_state.kapitel_info = [""] * len(toc_list)
    st.session_state.kapitel_inhalt = [""] * len(toc_list)
    st.session_state.kapitel_prompt = [""] * len(toc_list)
    # st.session_state.prompt_area = [""] * len(toc_list)
    st.session_state.glossar = ""

    



#--Content Area ---------------------------------------------------------------------------------------------------------------------------------------

st.header(st.session_state.new_header, divider='grey') 

#Inhaltsverzeichnis mit Links zu Kapiteln erstellen (in der Form noch buggy, da Links zu Üeberschriften mit Umlauten nicht Funktionieren)
#for i, item in enumerate(toc_list):
#    #Nachhalten des Inhaltsverzeichnisses mit Links
#    title_text = item["title"]
#    header_text = title_text.lower()  # In Kleinbuchstaben umwandeln
#    formatted_header = re.sub(r'[^a-z0-9\säöü-]', '', header_text)  # Nicht-alphanumerische Zeichen entfernen
#    formatted_header = re.sub(r'\s+', '-', formatted_header)  # Leerzeichen durch Bindestriche ersetzen
#    st.markdown(f"[{title_text}](#{formatted_header})")

# Erstellen der Webseinte-Struktur mit Überschriften Infoboxen und Textboxen
for i, item in enumerate(toc_list):
    title_text = item["title"]
    help_text= item["help_text"]
    prompt_text= item["prompt_text"]

    #Inhalte aus generierten Kapitelverzeichnis in SessionState nachhalten damit sie beim reload erhalten bleiben
    if st.session_state.kapitel_info[i] == "":
        st.session_state.kapitel_info[i] = help_text
    
    if st.session_state.kapitel_prompt[i] == "":
        st.session_state.kapitel_prompt[i] = prompt_text

    #Aufbau der Seitenkomponente für jedes Kapitel
    #Titel
    st.header(title_text) 
    st.info(st.session_state.kapitel_info[i])
    st.session_state.kapitel_prompt[i] = st.text_area(f"Prompt zum generieren des Inhalts", value=st.session_state.kapitel_prompt[i], height=100)
    
    #Schaltfläche um die Kapitelinhalte zu generieren
    if st.button("Kapitel " + title_text + " generieren", key="button_chapter_" + str(i)):
        prompt_text = st.session_state.prompt_area[i]
        openAI_API.generate_chapter(title_text, st.session_state.kapitel_prompt[i], new_doctype, st.session_state.new_title, new_writing_style, new_word_count, new_context, new_stakeholder, i)

    #Kapitelinhalt Sessionstate anpassen, so dass Änderungen in der Textbox nachgehalten werden und nicht durch den zuvor generierten Inhaltstext beim Page-reload überschrieben werden           
    st.session_state.kapitel_inhalt[i] = st.text_area(f"Textbaustein für {title_text}", value=st.session_state.kapitel_inhalt[i], height=300)

if 'glossar' in st.session_state:
    st.header("Glossar")

    if st.session_state.glossar == "":
        st.write("Zur Erstellung des Glossars bitte die Schaltfläche im Navigationsbereich im Bereich Word Export benutzen.")
    
    st.write(st.session_state.glossar)

#if "toc_list" in st.session_state:
    #st.write(st.session_state.toc_list)



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

#-------Sessionstate setzen wenn Projekt impoortiert wurde -------------------
def upload_sessionstate_from_json(uploaded_file):
    if uploaded_file is not None:
        # JSON-Daten lesen und in den SessionState schreiben
        session_dict = json.load(uploaded_file)
        st.session_state.update(session_dict)
        st.success("Projekt wurde eingelesen! Bitte unten links auf das x neben der Datei klicken um diese zu entfernen und die Seite neu zu laden!")

# JSON-Datei hochladen
uploaded_file = st.sidebar.file_uploader("Bestehendes Projekt per JSON Datei einlesen", type="json")

# Button zum Hochladen und SessionState aktualisieren
if uploaded_file is not None:
    upload_sessionstate_from_json(uploaded_file)
