import streamlit as st
import pandas as pd
from openai import OpenAI
import json
import openAI_API
import word_export


OpenAI.api_key = st.secrets["OPENAI_API_KEY"]



def generate_chapter(title_text, prompt_text, new_doctype, new_title, new_writing_style, new_word_count, index):
    client = OpenAI()
    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages=[
            {"role":"user" , "content": "Du schreibst mehrere Kapitel eines " + new_doctype + " zum Thema " + new_title },
            {"role":"user" , "content": "Schreibe den Inhalt für das Kapitel" + title_text},
            {"role":"user" , "content": "Beachte den folgenden Kontext und gehe inhaltlich üassend zum Kapitel darauf ein: " + new_context},
            {"role":"user" , "content": "Das Kapitel ist für folgende Zielgruppe zu schreiben. " + new_stakeholder + " Passe den technischen Detailierungsgrad dieser Zielgruppe an."},
            {"role":"user" , "content": prompt_text},
            {"role":"user" , "content": "Der Artikel sollte im folgenden Stil geschreiben sein: " + new_writing_style},
            {"role":"user" , "content": "Der Artikel soll maximal " + str(new_word_count) + " Worte beinhalten."},
            {"role":"user" , "content": "Starte jedes Unterkapitel mit dem Präfix #### und verzichte dabei auf Nummerierungen. Nenne nicht noch einmal den Kapitelnamen zu Begin sondern beginne direkt mit dem Inhalt."},
        ]
    )
    chapter_content = response.choices[0].message.content
    st.session_state.kapitel_inhalt[index] = chapter_content
    return chapter_content

def generate_glossar(content):
    client = OpenAI()
    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages=[
            {"role":"user" , "content": "Du hast ein Konzeptdokument mit folgenden Kapitelinhalten erzeugt" + str(content)},
            {"role":"user" , "content": "Erstelle ein ausführliches alphabetisch sortiertes Glossar. Gehe auf Abkürzungen und nicht allgemein bekannte technische Begriffe ein."}            
        ]
    )
    result = ''
    result = response.choices[0].message.content    
    return result

main_heading=st.title("AI Concept Designer")

#--Sidebar ---------------------------------------------------------------------------------------------------------------------------------------
if 'new_title' not in st.session_state:
    st.session_state.new_title = ""
if 'new_header' not in st.session_state:
    st.session_state.new_header = ""

st.sidebar.title("App-Steuerung")

#Schaltflächen für neues Dokument
st.sidebar.subheader("Neues Dokument", divider='grey')
newdoc_form = st.sidebar.form("newdoc_form_key")
new_title = newdoc_form.text_input("Dokumenttitel")
new_doctype = newdoc_form.selectbox("Dokumenttyp",
    ["Marktanalyse", "Anforderungskonzept", "Fachkonzept", "IT-Konzept", 
    "Architekturkonzept", "Infrastrukturkonzept", "Migrationskonzept", "Deploymentkonzept", "Testkonzept", "Backupkonzept", "Schnittstellenkonzept", 
    "Sicherheitskonzept", "Rollen- und Rechtekonzept",  
    "Datenschutzkonzept", "Datenschutzerklärung", "Schutzbedarfsfeststellung (nach BSI Grundschutz)", "Auftragsverarbeitungs-Vertrag", "Verzeichnis von Verarbeitungstätigkeiten", "Datenschutzfolgeabschätzung",
    "Changemanagementkonzept", "Löschkonzept", "Verschlüsselungskonzept", "Datensicherungskonzept", 
    "Betriebsführungskonzept", "Betriebsführungshandbuch", "Notfallkonzept", 
    "Dokumentationskonzept", "Risikomanagementkonzept", "Compliancekonzept", "Qualitätsmanagementkonzept",
    "Schulungskonzept", "Kommunikationskonzetpt", "Benutzerhandbuch"])
new_content_focus = newdoc_form.text_area("Inhaltlicher Schwerpunkt")
new_chapter_count = newdoc_form.slider("Anzahl der Kapitel.", min_value=1, max_value=30, value=8)

new_submitted = newdoc_form.form_submit_button("Dokumentstruktur erstellen")

if 'toc_list' in st.session_state:
    toc_list=st.session_state.toc_list
else:
    toc_list=[]

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
    st.session_state.glossar = generate_glossar(st.session_state.kapitel_inhalt)

if st.sidebar.button("Word Dokument generieren", key="word_export"):
        if 'glossar' not in st.session_state:
            st.session_state.glossar = generate_glossar(st.session_state.kapitel_inhalt)
        word_export.export_dokument_to_word(st.session_state.new_title, st.session_state.new_header, st.session_state.toc_list, st.session_state.kapitel_inhalt, st.session_state.glossar)

# Konzeptinhaltsverzeichnis aus gegebenen Parametern per ChatBot erstellen lassen
if new_submitted:
    
    #Inhaltsbereich generieren  
    st.header(new_doctype + ": " + new_title, divider='grey')    
    st.session_state.new_title = new_title
    st.session_state.new_header = new_doctype + ": " + new_title

    
    toc_list = openAI_API.generate_toc(new_doctype, new_title, new_content_focus, new_chapter_count)
    #st.write(toc_list)
    st.session_state.toc_list = toc_list
    st.session_state.kapitel_info = [""] * len(toc_list)
    st.session_state.kapitel_inhalt = [""] * len(toc_list)
    st.session_state.kapitel_prompt = [""] * len(toc_list)
    st.session_state.prompt_area = [""] * len(toc_list)



#--Content Area ---------------------------------------------------------------------------------------------------------------------------------------
# Erstellen der Struktur mit Überschriften Infoboxen und Textboxen
for i, item in enumerate(toc_list):
    title_text = item["title"]
    help_text= item["help_text"]
    prompt_text= item["prompt_text"]

    st.session_state.kapitel_info[i] = help_text
    st.session_state.kapitel_prompt[i] = prompt_text

    #if st.session_state.kapitel_inhalt[i] == "":
        #generate_chapter(title_text, prompt_text, new_doctype, new_title, new_writing_style, new_word_count, i)

    st.header(title_text)
    
    st.info(help_text)
    st.session_state.prompt_area[i] = st.text_area(f"Prompt zum generieren des Inhalts", value=st.session_state.kapitel_prompt[i], height=100)
    if st.button("Kapitel " + title_text + " generieren", key="button_chapter_" + str(i)):
        prompt_text = st.session_state.prompt_area[i]
        generate_chapter(title_text, prompt_text, new_doctype, new_title, new_writing_style, new_word_count, i)
               
    st.session_state.kapitel_inhalt[i] = st.text_area(f"Textbaustein für {title_text}", value=st.session_state.kapitel_inhalt[i], height=300)

if 'glossar' in st.session_state:
    st.header("Glossar")
    st.write(st.session_state.glossar)


#st.write(st.session_state.toc_list)

