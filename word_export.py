import streamlit as st
from docx import Document
from io import BytesIO
#from docx.enum.text import WD_PARAGRAPH_ALIGNMENT




def replace_placeholder(doc, placeholder, replacement):
    # Platzhalter in Absätzen
    for paragraph in doc.paragraphs:
        if placeholder in paragraph.text:
            paragraph.text = paragraph.text.replace(placeholder, replacement)
    
    for section in doc.sections:
        # Platzhalter in Kopfzeilen
        header = section.header
        for paragraph in header.paragraphs:
            if placeholder in paragraph.text:
                paragraph.text = paragraph.text.replace(placeholder, replacement)

def insert_chapter_at_placeholder(doc, placeholder, chapter):
    for paragraph in doc.paragraphs:
        if placeholder in paragraph.text:
            # Füge das Kapitel vor dem Platzhalter ein
            for element in chapter:
                new_paragraph = paragraph.insert_paragraph_before()
                new_paragraph.text = element['text']
                new_paragraph.style = element['style']
                if 'alignment' in element:
                    new_paragraph.alignment = element['alignment']
            # Entferne den Platzhalter-Text
            paragraph.text = paragraph.text.replace(placeholder, '')




def export_dokument_to_word (new_title,new_header,toc_list, content):
    
    # Bestehendes Dokument öffnen
    document = Document('IT-Konzept Template.docx')#---Plazhalter ersetzen------------------------------------------------------------------------------------
    replacements = {
        '{{Titel}}': new_header,
        '{{Titel2}}': "Pilotimplementierung KI Konzept Designer"
    }
    
    # Platzhalter ersetzen
    for placeholder, replacement in replacements.items():
        replace_placeholder(document, placeholder, replacement)

    # Kapitelstruktur einsetzen -----------------------------------------------------------------------------------
    # Definition der neuen Kapitel
    chapter_content = []
    for i, item in enumerate(toc_list):
        title_text = item["title"]
        help_text= item["help_text"]
        chapter_content.append({"text": title_text, "style": "Heading 1"})
        chapter_content.append({"text": "Hinweis", "style": "Hinweistext"})
        chapter_content.append({"text": help_text, "style": "Hinweistext"})
        chapter_content.append({"text": content[i], "style": "Normal"})

    chapters = [
        {
            "placeholder": "{{Kapitelstruktur}}",
            "content": chapter_content
        }
    ]
    for chapter in chapters:
        insert_chapter_at_placeholder(document, chapter['placeholder'], chapter['content'])

    # Save the document to a BytesIO object
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

if st.sidebar.button("Download Word Template"):
    word_file = create_word_document()
    
    # Provide the file as a download
    st.sidebar.download_button(
        label="Download Word file",
        data=word_file,
        file_name="Konzept.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

    
    # Geändertes Dokument speichern
    #document.save('IT-Konzept Test 01.docx')

    #print("Das Dokument wurde erfolgreich aktualisiert.")
