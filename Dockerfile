# Basis-Image
FROM python:3.9

# Setze das Arbeitsverzeichnis
WORKDIR /app

# Kopiere die requirements Datei und installiere Abhängigkeiten
COPY requirements.txt .
RUN pip install -r requirements.txt

# Kopiere den restlichen Code
COPY . .

# Exponiere den Port, auf dem die App läuft
EXPOSE 8501

# Starte die Streamlit-App
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
