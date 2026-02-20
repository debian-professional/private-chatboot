# DeepSeek Chat Server

> Ein produktionsreifer, selbst gehosteter KI-Chat-Server mit professionellem Feature-Set –
> gebaut mit purem JavaScript und Python, ohne externe Frameworks.

---

## Inhaltsverzeichnis

- [Über das Projekt](#über-das-projekt)
- [Was diesen ChatBot von anderen unterscheidet](#was-diesen-chatbot-von-anderen-unterscheidet)
- [Features im Überblick](#features-im-überblick)
- [Sicherheitsarchitektur](#sicherheitsarchitektur)
- [Technischer Aufbau](#technischer-aufbau)
- [Installation](#installation)
- [Konfiguration](#konfiguration)
- [Verwendung](#verwendung)
- [Projektstruktur](#projektstruktur)
- [Versionierung](#versionierung)
- [Manifest](#manifest)
- [Lizenz](#lizenz)

---

## Über das Projekt

**DeepSeek Chat Server** ist ein vollständig selbst gehosteter KI-Chat-Client, der die DeepSeek API
anbindet und auf einem eigenen Linux-Server unter Apache läuft. Das Projekt wurde von Grund auf
neu entwickelt – ohne vorgefertigte Frameworks, ohne NodeJS, ohne React.

Das Ergebnis: Eine einzige `index.html` Datei und eine Handvoll Python-CGI-Scripts, die zusammen
ein professionelles, produktionsreifes Chat-System ergeben.

**Technologie-Stack:**
- **Frontend:** Reines HTML5 / CSS3 / Vanilla JavaScript
- **Backend:** Python 3 (CGI-Scripts unter Apache)
- **Webserver:** Apache 2.4 mit SSL/HTTPS
- **KI-Modelle:** DeepSeek V3.2 (`deepseek-chat`) und DeepSeek Reasoner (`deepseek-reasoner`)
- **PDF-Erzeugung:** ReportLab (serverseitig)
- **PDF-Lesen:** PDF.js (clientseitig)

---

## Was diesen ChatBot von anderen unterscheidet

### 1. Vollständige Datensouveränität
Im Gegensatz zu kommerziellen Chat-Clients wie ChatGPT oder Claude läuft dieser Server
**vollständig auf eigener Hardware**. Keine Daten verlassen unkontrolliert den Server.
Der API-Key ist serverseitig in einer Umgebungsvariable gespeichert – der Browser sieht
ihn niemals.

### 2. Produktionsreife Sicherheitsarchitektur
- Der API-Key wird **ausschliesslich** als Apache-Umgebungsvariable gespeichert
- Ein Python CGI-Proxy übernimmt die Kommunikation mit der DeepSeek API
- **Magic Bytes Prüfung** blockiert das Hochladen von ausführbaren Dateien,
  auch wenn diese umbenannt wurden (z.B. `virus.exe` → `virus.jpg`)
- Erkennung von: Windows PE, Linux ELF32/64, macOS Mach-O, ARM, Shell Scripts, Python Bytecode
- SSL/HTTPS mit eigenem Zertifikat

### 3. Echtes Streaming – Token für Token
Die KI-Antworten erscheinen **Token für Token** in Echtzeit, genau wie bei ChatGPT oder Claude.
Implementiert über Server-Sent Events (SSE) mit ReadableStream API. Keine Wartezeit bis die
vollständige Antwort vorliegt – die Antwort beginnt nach Millisekunden zu erscheinen.

### 4. Zwei KI-Modi mit automatischer Konfiguration
| Modus | Modell | Kontext | Output |
|-------|--------|---------|--------|
| Normaler Chat | `deepseek-chat` | 100.000 Token | 8.192 Token |
| DeepThink | `deepseek-reasoner` | 65.000 Token | 32.768 Token |

Die gesamte Token-Konfiguration passt sich **automatisch** an den gewählten Modus an –
inklusive der Kontext-Auslastungsanzeige im Header.

### 5. Live Kontext-Auslastungsanzeige
Direkt unter der IP-Adresse zeigt der Header die aktuelle Kontext-Auslastung in Prozent an.
Ab 90% erscheint eine **rote, blinkende Warnung** – damit der Benutzer weiss, wann er den
Chat exportieren oder eine neue Session starten sollte. Die Anzeige ist modellabhängig und
aktualisiert sich bei jeder Nachricht, jedem Löschen und jedem Modellwechsel automatisch.

### 6. Vollständiges Export-System in 4 Formaten
Jede Nachricht und der gesamte Chat können exportiert werden:

| Format | Gesamt-Chat | Einzelnachricht | Methode |
|--------|-------------|-----------------|---------|
| PDF | ✅ | ✅ | Server (ReportLab) |
| Markdown | ✅ | ✅ | Server / Client |
| TXT | ✅ | ✅ | Server / Client |
| RTF | ✅ | ✅ | Server / Client |

Das PDF enthält ein professionelles Layout mit Header, Statistiken, Inhaltsverzeichnis
und farbcodiertem Chat-Verlauf.

### 7. Persistentes Session-Management
- **Automatisches Speichern** nach jeder Nachricht (serverseitig als JSON)
- Sessions können geladen, verwaltet und gelöscht werden
- Eindeutige Session-IDs im Format `YYYY-MM-DD_HHMMSS_random`
- Vollständige Chat-Historien bleiben auch nach Browser-Neustart erhalten

### 8. Intelligente Nachrichtenverwaltung
- **Hover-Buttons** erscheinen bei jeder Nachricht:
  - Links: Kopieren, Mag ich, Mag ich gar nicht, Regenerieren
  - Rechts: Exportieren (Dropdown), Löschen
- Löschen entfernt die Nachricht **und alle nachfolgenden** aus Kontext und UI
- **Regenerieren** generiert eine neue KI-Antwort auf dieselbe Frage

### 9. Feedback-System mit Server-Logging
Like und Dislike werden in die serverseitige Log-Datei geschrieben:
```
2026-02-17 17:23:45 | 192.168.1.1 | FEEDBACK | LIKE | msgId:42 | "Die Antwort war..."
```
Damit können Antwortqualitäten nachvollzogen und ausgewertet werden.

### 10. Konsequentes Design-System
Alle Buttons folgen einem einheitlichen **Pill-Style** (border-radius: 20px, height: 36px):
- 🔵 Blau – Aktions-Buttons
- 🔴 Rot – Destruktive Aktionen
- 🟢 Grün – Konstruktive Aktionen
- ⚫ Dunkel/Blau – Toggle-Buttons

Dieses Design-System ist im **Manifest** festgehalten und gilt verbindlich für alle
zukünftigen Erweiterungen.

### 11. Lebendes Manifest als Projektgedächtnis
Jede Änderung am Projekt wird in einer separaten `manifest` Datei dokumentiert –
mit Datum, Uhrzeit und detaillierter Beschreibung. Das Manifest enthält:
- Verbindliche Design-Vorschriften
- Technische Konventionen
- Vollständige Änderungshistorie (60+ Einträge)
- Strikte Verbote (z.B. keine eckigen Buttons, kein PHP)

Dieses Konzept macht das Projekt **wartbar, erweiterbar und nachvollziehbar** –
auch nach langen Pausen oder bei Zusammenarbeit mit KI-Assistenten.

---

## Features im Überblick

### Chat & KI
- ✅ Echtzeit-Streaming (Token für Token)
- ✅ Echter Multi-Turn-Kontext (Gesprächsgedächtnis)
- ✅ DeepThink Modus mit deepseek-reasoner
- ✅ Kontext-Auslastungsanzeige (0–100%, Warnung ab 90%)
- ✅ Automatische Umlaut-Ersetzung für die API
- ✅ Datenschutz-Toggle (X-No-Training Header)

### Dateien
- ✅ PDF-Upload mit Text-Extraktion (PDF.js)
- ✅ TXT-Upload
- ✅ Magic Bytes Sicherheitsprüfung
- ✅ Automatische Kürzung auf 50.000 Zeichen
- ✅ Fortschrittsanzeige bei PDF-Verarbeitung

### Export & Sessions
- ✅ Gesamt-Export: PDF, Markdown, TXT, RTF
- ✅ Einzelnachricht-Export: PDF, Markdown, TXT, RTF
- ✅ Session-Speicherung (automatisch, serverseitig)
- ✅ Session-Verwaltung (laden, löschen)

### UI/UX
- ✅ Dark Mode (immer aktiv)
- ✅ Pill-Style Design-System
- ✅ Hover-Buttons pro Nachricht (6 Buttons)
- ✅ Feedback-Buttons (Like, Dislike, Kopieren, Regenerieren)
- ✅ Flexible Textarea (animierter Fokus)
- ✅ Sie/Du Anredeform (persistent gespeichert)
- ✅ Einstellungen mit Toggle-Switches
- ✅ Log-Dateien Anzeige im Browser

### Infrastruktur
- ✅ Apache 2.4 mit SSL/HTTPS
- ✅ API-Key in Umgebungsvariable (niemals im Client)
- ✅ Python CGI-Proxy
- ✅ Git-Workflow mit Deploy-Script
- ✅ Serverseitiges Logging

---

## Sicherheitsarchitektur

```
Browser (Client)
      │
      │  HTTPS (SSL)
      ▼
Apache 2.4
      │
      │  intern
      ▼
Python CGI-Script ──► DeepSeek API
(liest API-Key aus          (external)
 Umgebungsvariable)
```

**Prinzipien:**
1. Der API-Key verlässt den Server niemals
2. Der Client kommuniziert ausschliesslich mit dem lokalen Proxy
3. Alle Dateien werden vor der Verarbeitung auf Magic Bytes geprüft
4. Sessions werden mit restriktiven Dateirechten gespeichert (600/700)

---

## Technischer Aufbau

### Frontend (index.html)
Eine einzige HTML-Datei enthält das gesamte Frontend:
- CSS (Dark Mode, Pill-Buttons, Animationen)
- JavaScript (Streaming, Session-Management, Export, Feedback)
- HTML (Layout, Overlays, Modals)

### Backend (Python CGI-Scripts)
| Script | Funktion |
|--------|----------|
| `deepseek-api.py` | API-Proxy mit Streaming, Logging |
| `save-session.py` | Session speichern (POST) |
| `load-session.py` | Sessions laden (GET/POST) |
| `delete-session.py` | Session löschen (POST) |
| `export-pdf.py` | PDF-Export mit ReportLab |
| `export-markdown.py` | Markdown-Export |
| `export-txt.py` | TXT-Export |
| `export-rtf.py` | RTF-Export (ohne externe Library) |
| `get-log.py` | Log-Datei abrufen |
| `feedback-log.py` | Like/Dislike loggen |

---

## Installation

### Voraussetzungen
- Linux-Server (Debian/Ubuntu empfohlen)
- Apache 2.4 mit CGI-Modul
- Python 3.8+
- ReportLab (`pip install reportlab`)
- SSL-Zertifikat
- DeepSeek API-Key

### 1. Repository klonen
```bash
git clone https://github.com/debian-professional/private-chatboot.git
cd private-chatboot
```

### 2. Apache konfigurieren
```apache
<VirtualHost *:443>
    ServerName your-domain.com
    DocumentRoot /var/www/deepseek-chat
    ScriptAlias /cgi-bin/ /var/www/deepseek-chat/cgi-bin/

    <Directory /var/www/deepseek-chat/cgi-bin>
        Options +ExecCGI
        AddHandler cgi-script .py
    </Directory>

    SSLEngine on
    SSLCertificateFile /path/to/cert.pem
    SSLCertificateKeyFile /path/to/key.pem
</VirtualHost>
```

### 3. API-Key konfigurieren
In `/etc/apache2/envvars`:
```bash
export DEEPSEEK_API_KEY="your-api-key-here"
```

### 4. Verzeichnisse erstellen
```bash
mkdir -p /var/www/deepseek-chat/sessions
chmod 700 /var/www/deepseek-chat/sessions
chmod +x /var/www/deepseek-chat/cgi-bin/*.py
```

### 5. Deployen
```bash
./deploy.sh
```

---

## Konfiguration

### Modell-Konfiguration (index.html)
```javascript
const MODEL_CONFIG = {
    'deepseek-chat': {
        maxContextTokens:   100000,
        maxOutputTokens:    8192,
        maxContextMessages: 50
    },
    'deepseek-reasoner': {
        maxContextTokens:   65000,
        maxOutputTokens:    32768,
        maxContextMessages: 30
    }
};
```

Bei einem Modellwechsel muss **nur dieser Block** angepasst werden.

---

## Verwendung

### Chat
1. Nachricht eingeben und **Enter** drücken (oder Senden-Button)
2. **Shift+Enter** für eine neue Zeile
3. **DeepThink** aktivieren für tiefgehende Analysen

### Datei hochladen
1. **Datei hochladen** klicken
2. PDF oder TXT auswählen
3. Frage zur Datei stellen

### Exportieren
- **Exportieren** Dropdown → gesamten Chat exportieren
- Hover über eine Nachricht → **Exportieren** Button → Einzelnachricht exportieren

### Session laden
- **Exportieren** → **Chat-Verlauf laden** → gespeicherte Session auswählen

---

## Projektstruktur

```
/var/www/deepseek-chat/
├── index.html              # Gesamtes Frontend
├── manifest                # Design-Manifest & Änderungshistorie
├── files-directorys        # Datei- und Verzeichnisübersicht
├── deploy.sh               # Deploy-Script
├── cgi-bin/
│   ├── deepseek-api.py     # API-Proxy (Streaming)
│   ├── save-session.py     # Session speichern
│   ├── load-session.py     # Sessions laden
│   ├── delete-session.py   # Session löschen
│   ├── export-pdf.py       # PDF-Export
│   ├── export-markdown.py  # Markdown-Export
│   ├── export-txt.py       # TXT-Export
│   ├── export-rtf.py       # RTF-Export
│   ├── get-log.py          # Log abrufen
│   ├── feedback-log.py     # Feedback loggen
│   └── deepseek-chat.log   # Server-Log
└── sessions/               # Gespeicherte Chat-Sessions (JSON)
```

---

## Versionierung

Das Projekt verwendet **Git Tags** für Milestones:

| Version | Datum | Beschreibung |
|---------|-------|--------------|
| v0.80 | 20.02.2026 | Erster stabiler Release mit vollem Feature-Set |

```bash
# Aktuellen Stand als Version taggen
git tag -a v0.80 -m "Version 0.80 - stable release"
git push origin v0.80
```

---

## Manifest

Das Projekt enthält ein detailliertes **Design-Manifest** (`manifest` Datei), das:
- Alle Design-Entscheidungen dokumentiert
- Verbindliche Regeln für Erweiterungen festlegt
- Eine vollständige Änderungshistorie führt (60+ Einträge)
- Als Projektgedächtnis für KI-assistierte Entwicklung dient

Das Manifest ist **integraler Bestandteil des Projekts** und muss bei jeder
Änderung aktualisiert werden.

---

## Philosophie

Dieses Projekt beweist, dass man **keine modernen JavaScript-Frameworks** braucht,
um ein professionelles, produktionsreifes Web-Applikation zu bauen.

- Kein React, kein Vue, kein Angular
- Kein NodeJS, kein npm
- Kein PHP
- Nur: **HTML + CSS + JavaScript + Python**

Einfach. Wartbar. Verständlich. Sicher.

---

*Entwickelt mit Leidenschaft und KI-Unterstützung – aber jede Entscheidung
wurde vom Menschen getroffen.*
