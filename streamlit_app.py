import streamlit as st
import openAI_API
import word_export

st.set_page_config(layout="wide")
main_heading=st.title("AI Concept Designer")
#main_heading=st.title("Modulare Interaktive Konzept Erstellung (MIKE)")


#--Sessionstat Handling ---------------------------------------------------------------------------------------------------------------------------------------
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
new_title = newdoc_form.text_input("Dokumenttitel")
new_doctype = newdoc_form.selectbox("Dokumenttyp",
    ["Fachkonzept", "IT-Konzept", "Anforderungskonzept", "Marktanalyse",
    "Architekturkonzept", "Infrastrukturkonzept", "Migrationskonzept", "Deploymentkonzept", "Testkonzept", "Backupkonzept", "Schnittstellenkonzept", 
    "Sicherheitskonzept", "Rollen- und Rechtekonzept",  
    "Datenschutzkonzept", "Datenschutzerklärung", "Schutzbedarfsfeststellung (nach BSI Grundschutz)", "Auftragsverarbeitungs-Vertrag", "Verzeichnis von Verarbeitungstätigkeiten", "Datenschutzfolgeabschätzung",
    "Changemanagementkonzept", "Löschkonzept", "Verschlüsselungskonzept", "Datensicherungskonzept", 
    "Betriebsführungskonzept", "Betriebsführungshandbuch", "Notfallkonzept", 
    "Dokumentationskonzept", "Risikomanagementkonzept", "Compliancekonzept", "Qualitätsmanagementkonzept",
    "Schulungskonzept", "Kommunikationskonzept", "Benutzerhandbuch"])
new_content_focus = newdoc_form.text_area("Inhaltlicher Schwerpunkt")
new_chapter_count = newdoc_form.slider("Anzahl der Kapitel.", min_value=1, max_value=30, value=8)
new_submitted = newdoc_form.form_submit_button("Dokumentstruktur erstellen")


#Schaltflächen für die Kapitelbearbeitung 
st.sidebar.subheader("Kapitel Steuerelemente", divider='grey')   
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




#--App Logik ---------------------------------------------------------------------------------------------------------------------------------------
# Konzeptinhaltsverzeichnis aus gegebenen Parametern per ChatBot erstellen lassen
if new_submitted:
    
    # Überschriften für Hauptbereich aus Parametern erzeugen
    #st.header(new_doctype + ": " + new_title, divider='grey')    
    st.session_state.new_title = new_title
    st.session_state.new_header = new_doctype + ": " + new_title

    with st.spinner(text="Inhaltsverzeichnis wird erstellt ..."):

    #Inhaltsverzeichnis + Infotexte + Prompts aus Paramtetern per Chatbot erzeugen
        toc_list = openAI_API.generate_toc(new_doctype, new_title, new_content_focus, new_chapter_count)
    
    #Leere SessionState Elemente erzeugen die im Weiteren mit Inhalten gefüllt werden, die über die gesamte Session erhalen bleiben sollen (da häufige Page Reloads)
    st.session_state.toc_list = toc_list
    st.session_state.kapitel_header = [""] * len(toc_list)
    st.session_state.kapitel_info = [""] * len(toc_list)
    st.session_state.kapitel_inhalt = [""] * len(toc_list)
    st.session_state.kapitel_prompt = [""] * len(toc_list)
    st.session_state.prompt_area = [""] * len(toc_list)
    st.session_state.glossar = ""

    



#--Content Area ---------------------------------------------------------------------------------------------------------------------------------------

st.header(st.session_state.new_header, divider='grey') 

# Erstellen der Webseinte-Struktur mit Überschriften Infoboxen und Textboxen
for i, item in enumerate(toc_list):
    title_text = item["title"]
    help_text= item["help_text"]
    prompt_text= item["prompt_text"]

    #Inhalte aus generierten Kapitelverzeichnis in SessionState nachhalten damit sie beim reload erhalten bleiben
    st.session_state.kapitel_info[i] = help_text
    st.session_state.kapitel_prompt[i] = prompt_text

    #Aufbau der Seitenkomponente für jedes Kapitel
    st.session_state.kapitel_header[i] = st.header(title_text)    
    st.info(help_text)
    st.session_state.prompt_area[i] = st.text_area(f"Prompt zum generieren des Inhalts", value=st.session_state.kapitel_prompt[i], height=100)
    
    #Schaltfläche um die Kapitelinhalte zu generieren
    if st.button("Kapitel " + title_text + " generieren", key="button_chapter_" + str(i)):
        prompt_text = st.session_state.prompt_area[i]
        openAI_API.generate_chapter(title_text, prompt_text, new_doctype, new_title, new_writing_style, new_word_count, new_context, new_stakeholder, i)

    #Kapitelinhalt Sessionstate anpassen, so dass Änderungen in der Textbox nachgehalten werden und nicht durch den zuvor generierten Inhaltstext beim Page-reload überschrieben werden           
    st.session_state.kapitel_inhalt[i] = st.text_area(f"Textbaustein für {title_text}", value=st.session_state.kapitel_inhalt[i], height=300)

if 'glossar' in st.session_state:
    st.header("Glossar")

    if st.session_state.glossar == "":
        st.write("Zur Erstellung des Glossars bitte die Schaltfläche im Navigationsbereich im Bereich Word Export benutzen.")
    
    st.write(st.session_state.glossar)


#st.write(st.session_state.toc_list)

