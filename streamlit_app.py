import streamlit as st
import pandas as pd
from openai import OpenAI
import json
import word_export


OpenAI.api_key = st.secrets["OPENAI_API_KEY"]

def generate_toc(new_doctype, new_title, new_content_focus, new_chapter_count, new_context):
    client = OpenAI()
    response = client.chat.completions.create(
        #model="gpt-3.5-turbo",
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Du bist ein Assistent, der Inhaltsverzeichnisse mit einer kurzen Beschreibung pro Kapitel für bestimmte Themengebiete erstellt"},
            {"role":"user" , "content": "Erstelle ein durchnummeriertes Inhaltsverzeichnis für ein " + new_doctype + " zum Thema " + new_title + " mit etwa " + str(new_chapter_count) + " Kapiteln."},
            {"role":"user" , "content": "Der inhaltliche Schwerpunkt sollte auf folgende Punkte gesetzt werden: " + new_content_focus},
            {"role": "user", "content": "Erstelle zu jedem Kapitel einen Hilfetext mit etwa 50 Wörtern. Beschreibe hier, welche Inhalte in das Kapitel eingearbeitet werden müssen und worauf insbesondere zu achten ist."},
            {"role": "user", "content": "Die Hilfeexte sollen dem IT Berater dabei helfen, das jeweilige Kapitel professionel auszuarbeiten und alle wichtigen Rahmenbedingungen wie Thema und Schwerpunkte zu beachten."},
            {"role": "user", "content": "Neben dem Hilfetext erstelle für jedes Kapitel einen Prompt, mit dem chatgpt den passenden Inhalt für dieses Kapitel erzeugen kann."},
            {"role": "user", "content": new_context},
        ],
        functions=[
            {
                "name": "generate_toc",
                "description": "Generates a nummerated table of contents with description for a given topic",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "toc": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "title": {
                                        "type": "string",
                                        "description": "The title of the chapter"
                                    },
                                    "help_text": {
                                        "type": "string",
                                        "description": "A description of what should be included in the chapter with about 50 words"
                                    },
                                    "prompt_text": {
                                        "type": "string",
                                        "description": "A prompt to make a chatbot like chatgpt generate the content for this specific chapter."
                                    }
                                },
                                "required": ["title", "help_text", "prompt_text"]
                            },
                            "description": "The generated table of contents with help texts"
                        }
                    },
                    "required": ["toc"]
                }
            }
        ],
        function_call="auto"
    )

    # Parse the response
    #toc = response.choices[0].message["function_call"]["arguments"]["toc"]
    toc = response.choices[0].message.function_call.arguments
    data = json.loads(toc)
    toc_list = data["toc"]
    return toc_list

def generate_chapter(title_text, prompt_text, new_doctype, new_title, new_writing_style, new_word_count, index):
    client = OpenAI()
    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages=[
            {"role":"user" , "content": "Du schreibst mehrere Kapitel eines " + new_doctype + " zum Thema " + new_title },
            {"role":"user" , "content": "Schreibe den Inhalt für das Kapitel" + title_text},
            {"role":"user" , "content": prompt_text},
            {"role":"user" , "content": "Der Artikel sollte im folgenden Stil geschreiben sein: " + new_writing_style},
            {"role":"user" , "content": "Der Artikel soll maximal " + str(new_word_count) + " Worte beinhalten."},
        ]
    )
    result = ''
    result = response.choices[0].message.content
    st.session_state.kapitel_inhalt[index] = result
    st.text = st.session_state.kapitel_inhalt[index]
    return result

def generate_glossar(content):
    client = OpenAI()
    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages=[
            {"role":"user" , "content": "Du hast ein Konzeptdokument mit folgenden Kapitelinhalten erzeugt" + str(content)},
            {"role":"user" , "content": "Erstelle ein Glossar. Gehe auf Abkürzungen und nicht allgemein bekannte technische Begriffe ein."}            
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
exp_newdoc = st.sidebar.expander("Neues Dokument")
newdoc_form = exp_newdoc.form("newdoc_form_key")
newdoc_form.subheader("Neues Dokument erstellen")
new_title = newdoc_form.text_input("Dokumenttitel")
new_content_focus = newdoc_form.text_area("Inhaltlicher Schwerpunkt")
new_doctype = newdoc_form.selectbox("Wähle einen Dokumenttyp",["IT Konzept", "Fachkonzept", "Berechtigungskonzept", "Benutzerhandbuch"])
new_writing_style = newdoc_form.selectbox("Wähle den Schreibstil.", ["Fachlich", "Technisch", "Akademisch", "Sarkastisch"])
new_chapter_count = newdoc_form.slider("Anzahl der Kapitel.", min_value=1, max_value=20, value=8)
new_word_count = newdoc_form.slider("Anzahl der Wörter pro Kapitel.", min_value=50, max_value=500, value=100, step=50)
new_submitted = newdoc_form.form_submit_button("Dokument erstellen")
new_context = ""
if new_doctype in ["IT Konzept", "Fachkonzept"]:
    new_context += "Das erste Kapitel ist die Managementsummary. Danach fürge die weiteren Kapitel hinzu."

if 'toc_list' in st.session_state:
    toc_list=st.session_state.toc_list
else:
    toc_list=[]

if new_submitted:
    main_title=st.header(new_doctype + ": " + new_title, divider='blue')
    st.session_state.new_title = new_title
    st.session_state.new_header = new_doctype + ": " + new_title

    
    toc_list = generate_toc(new_doctype, new_title, new_content_focus, new_chapter_count, new_context)
    #st.write(toc_list)
    st.session_state.toc_list = toc_list
    st.session_state.kapitel_info = [""] * len(toc_list)
    st.session_state.kapitel_inhalt = [""] * len(toc_list)
    st.session_state.kapitel_prompt = [""] * len(toc_list)
    st.session_state.prompt_area = [""] * len(toc_list)
        
#if st.sidebar.button("Word Dokument generieren", key="word_export"):
        #st.sidebar.write("Word Export gestartet")
        #glossar = generate_glossar(st.session_state.kapitel_inhalt)
        #st.write(glossar)
        #word_export.export_dokument_to_word(st.session_state.new_title, st.session_state.new_header, st.session_state.toc_list, st.session_state.kapitel_inhalt)

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
        
        
#st.write(st.session_state)

