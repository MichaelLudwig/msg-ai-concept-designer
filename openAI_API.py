import streamlit as st
from openai import OpenAI
import openai
import os
import json

#hole dir den ai_key entweder aus der OS Umgebungsvariable oder dem Streamlit Secret Vault

#Azure OpenAI Connection
if "AZURE_OPENAI_API_KEY" in os.environ:
    client = openai.AzureOpenAI(
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        api_version="2023-03-15-preview",
        azure_endpoint="https://mlu-azure-openai-service-sw.openai.azure.com/"
    )
    openAI_model = "gpt-4o-mini-sw"
    #st.session_state.ai_api_info="Azure OpenAI - Region Europa"
#if "AZURE_OPENAI_API_KEY" in os.environ:
#    client = OpenAI(api_key=os.environ["AZURE_OPENAI_API_KEY"])
#    openAI_model = "gpt-4o-mini"
    #st.session_state.ai_api_info="Azure OpenAI - Region Europa"    
elif "OPENAI_API_KEY" in st.secrets:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    openAI_model = "gpt-4o-mini"
    #st.session_state.ai_api_info="powered by OpenAI"
else:
    raise ValueError("Kein gültiger API-Schlüssel gefunden.")
    


#st.header(st.secrets["OPENAI_API_KEY"])

def generate_toc(new_doctype, new_title, new_content_focus, new_chapter_count):

    response = client.chat.completions.create(
        model=openAI_model,
        messages=[
            {"role": "system", "content": "Du bist ein Assistent, der Inhaltsverzeichnisse mit einer kurzen Beschreibung pro Kapitel für bestimmte Themengebiete erstellt"},
            {"role":"user" , "content": "Erstelle ein durchnummeriertes Inhaltsverzeichnis für ein " + new_doctype + " zum Thema " + new_title + " mit etwa " + str(new_chapter_count) + " Kapiteln."},
            {"role":"user" , "content": "Der inhaltliche Schwerpunkt sollte auf folgende Punkte gesetzt werden: " + new_content_focus},
            {"role": "user", "content": "Erstelle zu jedem Kapitel einen Hilfetext mit etwa 50 Wörtern. Beschreibe hier, welche Inhalte in das Kapitel eingearbeitet werden müssen und worauf insbesondere zu achten ist."},
            {"role": "user", "content": "Die Hilfetexte sollen dem IT Berater dabei helfen, das jeweilige Kapitel professionel auszuarbeiten und alle wichtigen Rahmenbedingungen wie Thema und Schwerpunkte zu beachten."},
            {"role": "user", "content": "Neben dem Hilfetext erstelle für jedes Kapitel einen Prompt, mit dem chatgpt den passenden Inhalt für dieses Kapitel erzeugen kann."},
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
    toc = json.loads(response.choices[0].message.function_call.arguments)
    toc_list = toc["toc"]

    #toc_list.input_tokens = response['usage']['prompt_tokens']
    #toc_list.output_tokens = response['usage']['completion_tokens']
    st.write("Verwendete AI Tokens zur Erstellung des Inhaltsverzeichnisses: " + str(response.usage.total_tokens))

    return toc_list

def generate_chapter(title_text, prompt_text, new_doctype, new_title, new_writing_style, new_word_count, new_context, new_stakeholder, index):

    response = client.chat.completions.create(
        model = openAI_model,
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
    st.write("Verwendete AI Tokens zur Erstellung dieses Kapitels: " + str(response.usage.total_tokens))
    return chapter_content

def generate_glossar(content):

    response = client.chat.completions.create(
        model = openAI_model,
        messages=[
            {"role":"user" , "content": "Du hast ein Konzeptdokument mit folgenden Kapitelinhalten erzeugt" + str(content)},
            {"role":"user" , "content": "Erstelle ein ausführliches alphabetisch sortiertes Glossar. Gehe auf Abkürzungen und nicht allgemein bekannte technische Begriffe ein."},
            {"role":"user" , "content": "Sollten dir keine Inhalte vorliegen, weise mich darauf hin und erstelle kein Glossar."}            
        ]
    )

    glossar = response.choices[0].message.content     
    st.write("Verwendete AI Tokens zur Erstellung des Glossars: " + str(response.usage.total_tokens))
    return glossar