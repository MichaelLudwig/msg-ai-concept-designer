import streamlit as st
import pandas as pd
from openai import OpenAI
import json

OpenAI.api_key = st.secrets["OPENAI_API_KEY"]

def generate_toc(new_doctype, new_title, new_content_focus, new_chapter_count):
    client = OpenAI()
    response = client.chat.completions.create(
        #model="gpt-3.5-turbo",
        model="gpt-4o-mini",
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
    return toc_list