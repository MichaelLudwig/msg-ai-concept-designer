# Project Requirements Document (PRD)

## 1. Einleitung

Der **AI Concept Designer** ist ein digitales Werkzeug, das mithilfe Künstlicher Intelligenz (KI) die Erstellung von professionellen Konzeptdokumenten automatisiert und vereinfacht. Ziel ist es, auch Personen ohne tiefgehende technische Kenntnisse in die Lage zu versetzen, hochwertige und strukturierte Dokumente für verschiedene Anwendungsbereiche (z.B. IT-Konzepte, Fachkonzepte, Testkonzepte) zu erstellen.

## 2. Zielgruppe

Dieses Dokument richtet sich an Projektbeteiligte, Fachabteilungen, Berater:innen und Entscheider:innen, die Konzeptdokumente benötigen, aber wenig oder keine Erfahrung mit KI, Programmierung oder Streamlit haben. Es ist bewusst laienverständlich gehalten und erklärt alle relevanten Begriffe und Abläufe.

## 3. Problemstellung und Nutzen

Die Erstellung von Konzeptdokumenten ist oft zeitaufwändig, erfordert viel Erfahrung und führt zu uneinheitlichen Ergebnissen. Der AI Concept Designer löst dieses Problem, indem er:
- die Strukturierung und Gliederung automatisiert,
- Hilfetexte und Prompts für die einzelnen Kapitel generiert,
- die eigentlichen Inhalte der Kapitel auf Knopfdruck KI-gestützt erstellt,
- ein Glossar mit Erklärungen zu Fachbegriffen bereitstellt,
- und den Export in ein professionelles Word-Dokument ermöglicht.

Dadurch sparen Nutzer:innen Zeit, erhalten konsistente und qualitativ hochwertige Dokumente und können sich auf die inhaltlichen Schwerpunkte konzentrieren.

## 4. Hauptfunktionen (Features)

- **Dokumenttyp wählen:** Auswahl aus verschiedenen Konzeptarten (z.B. IT-Konzept, Testkonzept, Architekturkonzept).
- **Titel und Schwerpunkte festlegen:** Eingabe des Dokumenttitels und der inhaltlichen Schwerpunkte.
- **Kapitelanzahl bestimmen:** Festlegung, wie viele Kapitel das Dokument enthalten soll.
- **Automatische Gliederung:** Die KI erstellt ein Inhaltsverzeichnis mit passenden Kapiteln.
- **Hilfetexte und Prompts:** Zu jedem Kapitel werden Hilfetexte und Prompts generiert, die die inhaltliche Ausarbeitung unterstützen.
- **Kapitelinhalte generieren:** Die KI erstellt auf Wunsch die Inhalte der einzelnen Kapitel, angepasst an Zielgruppe und Kontext.
- **Glossar:** Automatische Erstellung eines Glossars mit Erklärungen zu Fachbegriffen und Abkürzungen.
- **Word-Export:** Export des fertigen Dokuments als professionell formatiertes Word-Dokument.
- **Projekt speichern/laden:** Möglichkeit, den Bearbeitungsstand als Datei zu speichern und später wieder zu laden.

## 5. Bedienung und Ablauf (aus Nutzersicht)

1. **Start der Anwendung:** Die Anwendung wird im Browser geöffnet (z.B. über einen bereitgestellten Link oder lokal installiert).
2. **Eingabe der Dokumentdaten:** In der Seitenleiste werden Titel, Dokumenttyp, Schwerpunkte, Kapitelanzahl und weitere Angaben gemacht.
3. **Erstellung der Gliederung:** Mit einem Klick wird ein Inhaltsverzeichnis samt Hilfetexten und Prompts generiert.
4. **Kapitel bearbeiten:** Für jedes Kapitel kann die KI per Knopfdruck einen Textvorschlag erstellen. Die Vorschläge können manuell angepasst werden.
5. **Glossar generieren:** Nach der Inhaltserstellung kann ein Glossar automatisch erzeugt werden.
6. **Export:** Das fertige Dokument kann als Word-Datei heruntergeladen werden.
7. **Projekt speichern/laden:** Der aktuelle Stand kann als Datei gespeichert und später wieder geladen werden.

## 6. Technische Grundlagen (laienverständlich erklärt)

### Was ist Künstliche Intelligenz (KI)?
Künstliche Intelligenz bezeichnet Computerprogramme, die in der Lage sind, Aufgaben zu lösen, die normalerweise menschliche Intelligenz erfordern – z.B. Texte schreiben, Zusammenhänge erkennen oder Vorschläge machen. Im AI Concept Designer wird KI genutzt, um Texte zu generieren und Vorschläge zu machen.

### Was ist Streamlit?
Streamlit ist eine Software, mit der man einfach und schnell interaktive Webanwendungen erstellen kann – ohne tiefgehende Programmierkenntnisse. Die Benutzeroberfläche des AI Concept Designers basiert auf Streamlit und läuft im Webbrowser.

### Wie funktioniert die Textgenerierung?
Die Anwendung nutzt die Schnittstelle (API) von OpenAI, um Texte zu generieren. Die Nutzer:innen geben Vorgaben (Prompts), und die KI erstellt daraufhin passende Textbausteine.

## 7. Anforderungen an die Umgebung

- Ein moderner Webbrowser (z.B. Chrome, Firefox, Edge)
- Zugang zur Anwendung (z.B. über eine bereitgestellte URL oder lokale Installation)
- Für die Textgenerierung wird ein Zugang zu OpenAI (API-Key) benötigt (dies wird in der Regel durch die Bereitsteller der Anwendung konfiguriert)

## 8. Glossar (wichtige Begriffe)

- **KI (Künstliche Intelligenz):** Computerprogramme, die Aufgaben mit "menschlicher Intelligenz" lösen.
- **Prompt:** Eine Vorgabe oder Frage, mit der die KI gesteuert wird.
- **API:** Eine Schnittstelle, über die Programme miteinander kommunizieren.
- **Streamlit:** Ein Werkzeug zur Erstellung von Webanwendungen.
- **OpenAI:** Ein Anbieter von KI-Technologien.

## 9. Zielzustand und Erfolgskriterien

- Nutzer:innen können ohne technisches Vorwissen professionelle Konzeptdokumente erstellen.
- Die Anwendung ist einfach und intuitiv bedienbar.
- Die generierten Dokumente sind qualitativ hochwertig und konsistent.
- Die Zeit für die Dokumentenerstellung wird deutlich reduziert.

---

*Dieses PRD wurde automatisch auf Basis des aktuellen Projektstandes erstellt und richtet sich an eine nicht-technische Zielgruppe.* 