# Multi-LLM Chat Client – OpenAI, DeepSeek, Google Gemini, Hugging Face & GroqCloud

**Multi-LLM Chat Client** ist ein vollständig eigenständiger, lokal gehosteter Chat-Client mit Unterstützung für mehrere KI-Anbieter: OpenAI, DeepSeek, Google Gemini, Hugging Face und GroqCloud. Entwickelt mit Fokus auf **Sicherheit, Einfachheit und professionelle Nutzbarkeit**. Die Architektur kommt ohne exotische Frameworks aus und verwendet ausschliesslich bewährte Technologien: Apache als Webserver, Python CGI für serverseitige Logik und reines HTML/JavaScript/CSS auf der Client-Seite.

Wichtigste Highlights:
- **Multi-LLM-Unterstützung** – Wechsel zwischen OpenAI, DeepSeek, Google Gemini, Hugging Face und GroqCloud über einen Anbieter-Toggle im LLM-Einstellungs-Panel.
- **Multi-Datei-Upload** – Mehrere Dateien gleichzeitig auswählen und senden. Inhalte werden kombiniert und gemeinsam als Kontext gesendet.
- **Audio-Aufnahme via Mikrofon** – Audio direkt im Browser aufnehmen und an die KI senden. Unterstützt von Google Gemini (alle Modelle) und OpenAI (gpt-4o, gpt-4.1). Der Aufnahme-Button erscheint automatisch nur bei audio-fähigen Modellen.
- **Einzigartiges Kontextmanagement** – Einzelne Nachrichten zusammen mit allen nachfolgenden löschen. Der Chat bleibt konsistent, die Token-Nutzung wird dynamisch aktualisiert.
- **Maximale Sicherheit** – Der API-Key ist clientseitig nie sichtbar, Uploads werden via Magic-Byte-Prüfung gegen ausführbare Dateien geschützt, Sessions werden mit restriktiven Dateiberechtigungen gespeichert.
- **Keine exotischen Frameworks** – Alles basiert auf Apache, Python, Bash und reinem HTML/JS.
- **Professionelle Exportfunktionen** – PDF, Markdown, TXT, RTF für den gesamten Chat oder einzelne Nachrichten, plus direktes Kopieren in die Zwischenablage.
- **Mehrsprachige Unterstützung** – Vollständige UI-Übersetzung via externer `language.xml` (Englisch, Deutsch, Spanisch, erweiterbar).
- **Audio-Aufnahme** – Integrierter Mikrofon-Button (MediaRecorder API) für direkte Spracheingabe. Automatisch sichtbar nur wenn ein audio-fähiges Modell aktiv ist (alle Gemini-Modelle, OpenAI gpt-4o und gpt-4.1). Audio wird als base64 WebM/MP4 übertragen — keine Transkription, das Modell verarbeitet Sprache direkt.
- **Kompressor (Kontext-Komprimierung)** – Automatische intelligente Komprimierung des Chat-Verlaufs, wenn das Kontextfenster sich füllt. Ein zweites LLM fasst die ältesten 50% der Nachrichten zusammen und injiziert die Zusammenfassung in den System-Prompt — das Gespräch kann unbegrenzt fortgeführt werden, ohne den roten Faden zu verlieren. Konfigurierbare Schwellwerte (70%/85%/95%), animierter Banner als visuelle Rückmeldung, Ergebnisdateien werden auf dem Datenträger gespeichert. Die Zusammenfassung wird automatisch verworfen, wenn der Kontext nach manuellem Löschen von Nachrichten unter den zuletzt ausgelösten Schwellwert fällt.
- **Guthaben- und Tageslimit-Banner** – Dauerhafte visuelle Banner bei erschöpftem Guthaben (rot, bezahlte Anbieter) und Tageslimits (blau, Free-Tier-Anbieter), jeweils mit Schliessen-Button.
- **Kontextfenster-Überschreitung** – Wenn die maximale Kontextgrösse erreicht wird, erscheint direkt im Chat eine interaktive Box mit zwei Optionen: Neuen Chat mit aktuellem Kontext starten (Option C: letzte Komprimierungszusammenfassung + nachfolgende Nachrichten), oder sauberen neuen Chat starten. Die aktuelle Session wird in beiden Fällen automatisch gespeichert.
- **Zwischenablage-Integration** – Ctrl+V-Handler mit Dialog für Text, Bilder und Schutz gegen versehentliches Einfügen von Dateipfaden.
- **Streaming-Antworten** – KI-Antworten erscheinen Token für Token, genau wie bei ChatGPT oder Claude.
- **429-Rate-Limit-Handling** – Automatischer Wiederholungsversuch mit Countdown-Anzeige für Google Gemini Free Tier Limits.
- **Enthaltenes Tool** – Das Skript `repo2text.sh` exportiert das gesamte Repository als Textdatei, ideal für die Arbeit mit KI-Assistenten (wie diesem).

---

## Inhaltsverzeichnis

- [Übersicht](#übersicht)
- [Architektur](#architektur)
- [Einzigartiges Kontextmanagement](#einzigartiges-kontextmanagement)
- [Features im Detail](#features-im-detail)
  - [Chat-Interface](#chat-interface)
  - [Streaming-Antworten](#streaming-antworten)
  - [Zwischenablage-Handler (Ctrl+V)](#zwischenablage-handler-ctrlv)
  - [Datei-Upload mit Sicherheitsprüfung](#datei-upload-mit-sicherheitsprüfung)
  - [Umlaut-Platzhalter-System](#umlaut-platzhalter-system)
  - [DeepThink-Modus](#deepthink-modus)
  - [Modellerkennung & Fähigkeiten](#modellerkennung--fähigkeiten)
  - [Mehrsprachiges System](#mehrsprachiges-system)
  - [Einstellungen (Toggles statt Radio-Buttons)](#einstellungen-toggles-statt-radio-buttons)
  - [Session-Management](#session-management)
  - [Exportfunktionen](#exportfunktionen)
  - [Feedback-Buttons & Logging](#feedback-buttons--logging)
  - [Dynamische Kontext-Anzeige](#dynamische-kontext-anzeige)
  - [Datei-Card-Anzeige](#datei-card-anzeige)
  - [Audio-Aufnahme](#audio-aufnahme)
  - [Kompressor — Intelligente Kontext-Komprimierung](#kompressor--intelligente-kontext-komprimierung)
  - [Guthaben- und Tageslimit-Banner](#guthaben--und-tageslimit-banner)
  - [Kontextfenster-Überschreitung](#kontextfenster-überschreitung)
- [Das Hilfsskript `repo2text.sh`](#das-hilfsskript-repo2textsh)
- [Sicherheitsarchitektur im Detail](#sicherheitsarchitektur-im-detail)
- [Deployment & Verwendung](#deployment--verwendung)
  - [Voraussetzungen](#voraussetzungen)
  - [Installation](#installation)
  - [Konfiguration](#konfiguration)
  - [Deploy-Skripte](#deploy-skripte)
- [Projektstruktur](#projektstruktur)
- [Modell-Konfiguration](#modell-konfiguration)
- [Design-Manifest](#design-manifest)
- [Bekannte Einschränkungen & technische Hinweise](#bekannte-einschränkungen--technische-hinweise)
- [Abhängigkeiten](#abhängigkeiten)
- [Fazit / Warum dieses Projekt heraussticht](#fazit--warum-dieses-projekt-heraussticht)

---

## Übersicht

Multi-LLM Chat Client ist eine **lokale Webanwendung**, die über verschiedene APIs kommuniziert. Entwickelt für eine private Serverumgebung (Debian), läuft sie auf jedem System mit Apache und Python 3. Ziel war ein **sicherer, erweiterbarer und benutzerfreundlicher** Chat-Client ohne Cloud-Abhängigkeiten und mit voller Datenkontrolle.

Das Projekt ist über mehrere Wochen aktiver Entwicklung kontinuierlich gewachsen und hat Features wie Streaming, Session-Management, Exportfunktionen, Mehrsprachigkeit, Zwischenablage-Integration, intelligente Kontext-Komprimierung und robuste Sicherheitsmassnahmen hinzugewonnen — ohne jemals externe JavaScript-Frameworks einzuführen.

---

## Architektur

Die Architektur ist bewusst einfach, aber durchdacht:

### 1. Client
- Reines HTML/JavaScript/CSS, ausgeliefert via Apache.
- Keine Build-Tools, kein Node.js, keine externen Bibliotheken (ausser PDF.js für browserbasierte PDF-Textextraktion).
- Die gesamte Client-Logik (Nachrichtenverarbeitung, UI-Updates, Streaming-Empfang, Sprachwechsel, Zwischenablage-Handling) ist in einer einzigen `index.html` gekapselt.
- Alle UI-Texte werden beim Start aus einer externen `language.xml` geladen — keine hartkodierten Strings im HTML.

### 2. Server
- **Apache** mit CGI-Unterstützung (`mod_cgi`).
- **Python CGI-Skripte** unter `/cgi-bin/` übernehmen:
  - Kommunikation mit der OpenAI API (`openai-api.py`) — nativer Endpunkt mit Streaming (Server-Sent Events)
  - Kommunikation mit der DeepSeek API (`deepseek-api.py`) — mit Streaming (Server-Sent Events)
  - Kommunikation mit der Google Gemini API (`google-api.py`) — konvertiert OpenAI-Format in Gemini-Format
  - Kommunikation mit der Hugging Face Inference API (`hugging-api.py`) — OpenAI-kompatibler Router-Endpunkt
  - Kommunikation mit der GroqCloud API (`groq-api.py`) — OpenAI-kompatibler Endpunkt, LPU-beschleunigte Inferenz
  - Kontext-Komprimierung (`compress-context.py`) — fasst die ältesten 50% der Nachrichten via einem zweiten LLM-Aufruf zusammen, wenn Kontext-Schwellwerte erreicht werden
  - Modellerkennung (`deepseek-models.py`) — fragt `/v1/models` beim Start ab
  - Session-Speicherung und -Abruf (`save-session.py`, `load-session.py`, `delete-session.py`)
  - Exporte in verschiedenen Formaten (`export-pdf.py`, `export-markdown.py`, `export-txt.py`, `export-rtf.py`)
  - Feedback-Logging (`feedback-log.py`)
  - Log-Anzeige (`get-log.py`)
- API-Keys werden ausschliesslich über Apache-Umgebungsvariablen (`OPENAI_API_KEY`, `DEEPSEEK_API_KEY`, `GOOGLE_API_KEY`, `HF_API_KEY`, `GRQ_API_KEY` in `/etc/apache2/envvars`) bereitgestellt — **nie im Client-Code**.
- Ein einziger `ScriptAlias /cgi-bin/ /var/www/deepseek-chat/cgi-bin/` deckt alle Skripte ab — keine Apache-Änderungen beim Hinzufügen neuer Skripte nötig.

### 3. Datenspeicherung
- **Sessions** werden als JSON-Dateien in `/var/www/deepseek-chat/sessions/` mit `chmod 700` gespeichert.
- **Logs** werden nach `/var/www/deepseek-chat/logs/multi-llm-chat.log` geschrieben (ohne API-Key oder Session-Inhalte).
- **Kompressor-Ergebnisse** werden nach `/var/www/deepseek-chat/kompressor/` geschrieben — eine Datei pro Komprimierungsrunde.
- **Einstellungen** verbleiben lokal im Browser (`localStorage`) mit Versionskontrolle.
- **Sprachdaten** werden beim Seitenaufruf aus `language.xml` via `fetch()` geladen.

### 4. Hilfsskripte
- `deploy.sh`, `sync-back.sh`, `install.sh`, `tag-release.sh` erleichtern das Deployment zwischen Entwicklungs- und Produktionsverzeichnissen.
- `repo2text.sh` exportiert das gesamte Repository als Textdatei für KI-Assistenten.

---

## Einzigartiges Kontextmanagement

Eines der herausragenden Features ist die Möglichkeit, **einzelne Nachrichten zusammen mit allen nachfolgenden zu löschen**. Dies geht weit über das typische „letzte Nachricht löschen" hinaus und ermöglicht eine flexible Korrektur des Gesprächsverlaufs.

**Implementierung**:
- Jede Nachricht (Benutzer & KI) erhält eine eindeutige `id` (Format: `msg_N`) und wird in einem Array `contextHistory.messages` gespeichert.
- Die Funktion `deleteMessage(msgId)` ermittelt den Index der Nachricht, kürzt das Array ab `index` und entfernt alle folgenden Elemente aus dem DOM (inklusive Trennlinien).
- Die Token-Schätzung (`updateContextEstimation()`) wird sofort neu berechnet, ebenso die prozentuale Kontextauslastung im Header.
- Wenn der Kontext nach dem Löschen unter den zuletzt ausgelösten Kompressor-Schwellwert fällt, wird die Komprimierungszusammenfassung automatisch verworfen und das Schwellwert-Tracking zurückgesetzt.
- Die geänderte Session wird anschliessend automatisch gespeichert (`saveSession()`).

**Warum ist das einzigartig?**
Viele Chat-Clients erlauben nur das Löschen der letzten Nachricht oder gar keine Verlaufsmanipulation. Hier kann der Benutzer **jeden beliebigen Punkt im Gespräch als neuen Startpunkt definieren** — perfekt zum Testen, Korrigieren oder Bereinigen des Kontextfensters ohne Verlust des gesamten Chats.

**Regenerieren-Funktion**: Zusätzlich zur Löschung hat jede KI-Antwort einen „Regenerieren"-Button, der die alte Antwort löscht und automatisch eine neue auf Basis derselben Benutzernachricht erzeugt — unter Verwendung des vollständigen Gesprächskontexts bis zu diesem Punkt.

---

## Features im Detail

### Chat-Interface

- **Dark Mode** (fest, keine Option) — augenschonend, professionelles Erscheinungsbild.
  - Hintergrund: `#121212`, Text: `#f0f0f0`, Akzent: `#0056b3`
- **Server-Header** zeigt Servername, interne IP-Adresse, dynamische Kontextauslastung und erkannte Modellnamen.
- **Nachrichten-Container** mit Hover-Buttons (Feedback, Export, Löschen).
- **Textarea** erweitert sich beim Fokus von 40px auf 120px mit sanfter CSS-Animation — Enter sendet, Shift+Enter erzeugt eine neue Zeile.
- Alle Buttons folgen einem strikten **Pill-Style**-Design (border-radius: 20px, height: 36px) — keine eckigen Buttons.
- Benutzernachrichten erscheinen in Blau (`#4dabf7`), KI-Antworten in Weiss auf dunklem Hintergrund.
- Automatische Zeilenumbruch-Beibehaltung (`white-space: pre-wrap`) für alle Nachrichteninhalte.
- Automatisches Scrollen zur neuesten Nachricht während und nach dem Streaming.

### Streaming-Antworten

KI-Antworten werden **Token für Token** via Server-Sent Events (SSE) empfangen und angezeigt:

- Alle fünf CGI-Proxy-Skripte senden Anfragen an ihre jeweiligen APIs mit `stream: True` und leiten den Event-Stream direkt weiter.
- `index.html` liest den Stream via `ReadableStream`-API und `TextDecoder`.
- Jedes empfangene Token wird dem Nachrichten-Element in Echtzeit hinzugefügt.
- Der psychologische Effekt ist erheblich: die ersten Token erscheinen innerhalb von ~0,3 Sekunden statt 8+ Sekunden auf eine vollständige Antwort zu warten.
- Sowohl `sendMessage()` als auch `handleRegenerate()` verwenden identische Streaming-Logik.
- Auto-Scroll bleibt während des Streamings aktiv.

**Technische Header** aller CGI-Proxy-Skripte für korrektes Streaming:
```
Content-Type: text/event-stream
X-Accel-Buffering: no
Cache-Control: no-cache
```

### OpenAI-Integration

Der Client unterstützt OpenAI als ersten KI-Anbieter (oben in der LLM-Auswahl) via `openai-api.py`:

- **Architektur**: Verwendet den nativen OpenAI Chat-Completions-Endpunkt — keine Formatkonvertierung erforderlich. Der SSE-Stream wird direkt weitergeleitet.
- **Endpunkt**: `https://api.openai.com/v1/chat/completions`
- **API-Key**: `OPENAI_API_KEY` in `/etc/apache2/envvars` — nie dem Client gegenüber exponiert.
- **Free Tier**: `gpt-4o-mini`, `gpt-5-mini`.
- **Paid Tier**: `gpt-5.4`, `gpt-5.2-chat-latest`, `gpt-4o`, `gpt-4.1`, `gpt-4o-mini`.
- Das Modell-Dropdown in den LLM-Einstellungen aktualisiert sich automatisch basierend auf dem gewählten Tier.
- **Audio-Input**: `gpt-4o` und `gpt-4.1` unterstützen direkte Mikrofon-Aufnahmen. Wenn eines dieser Modelle aktiv ist, wird der Audio-Aufnahme-Button sichtbar. Audio wird als `input_audio` im OpenAI-Format gesendet.
- Der DeepThink-Button und -Indikator werden ausgeblendet, wenn OpenAI aktiv ist.
- System-Prompt identifiziert das aktive Modell: *„You are [model], an AI assistant made by OpenAI."*

### Google Gemini-Integration

Der Client unterstützt Google Gemini als zweiten KI-Anbieter via `google-api.py`:

- **Architektur**: Das CGI-Skript konvertiert das intern verwendete OpenAI-Format in das Gemini-spezifische `contents`-Format, sendet die Anfrage und konvertiert die Antwort zurück in das von `index.html` erwartete OpenAI-SSE-Format.
- **API-Key**: `GOOGLE_API_KEY` in `/etc/apache2/envvars` — nie dem Client gegenüber exponiert.
- **Free Tier** (Standard): `gemini-2.5-flash` — 5 Anfragen pro Minute, 20 Anfragen pro Tag.
- **Paid Tier**: `gemini-2.5-flash`, `gemini-2.5-pro`, `gemini-1.5-pro`, `gemini-2.0-flash`.
- Das Modell-Dropdown in den LLM-Einstellungen aktualisiert sich automatisch basierend auf dem gewählten Tier.
- **Audio-Input**: Alle Gemini-Modelle unterstützen direkte Mikrofon-Aufnahmen. Der Audio-Aufnahme-Button ist immer sichtbar wenn Google Gemini aktiv ist. Audio wird als `inline_data` im nativen Gemini-Format gesendet.
- Der DeepThink-Button und -Indikator werden ausgeblendet, wenn Google Gemini aktiv ist.

### Hugging Face-Integration

Der Client unterstützt Hugging Face Inference Providers als dritten KI-Anbieter via `hugging-api.py`:

- **Architektur**: Verwendet den OpenAI-kompatiblen Hugging Face Router-Endpunkt — keine Formatkonvertierung erforderlich. Der SSE-Stream wird direkt weitergeleitet.
- **Endpunkt**: `https://router.huggingface.co/v1/chat/completions` — der Router wählt automatisch den schnellsten verfügbaren Anbieter.
- **API-Key**: `HF_API_KEY` in `/etc/apache2/envvars` — ein Write-Token von huggingface.co/settings/tokens mit der Berechtigung „Make calls to Inference Providers".
- **Free Tier**: `Qwen/Qwen2.5-72B-Instruct`, `mistralai/Mistral-7B-Instruct-v0.3`, `microsoft/Phi-3.5-mini-instruct`.
- **Paid Tier**: `meta-llama/Meta-Llama-3.1-70B-Instruct`, `meta-llama/Meta-Llama-3.1-405B-Instruct`, `Qwen/Qwen2.5-72B-Instruct`, `mistralai/Mixtral-8x7B-Instruct-v0.1`.
- Das Modell-Dropdown aktualisiert sich automatisch basierend auf dem gewählten Tier.
- Der DeepThink-Button und -Indikator werden ausgeblendet, wenn Hugging Face aktiv ist.

### GroqCloud-Integration

Der Client unterstützt GroqCloud als vierten KI-Anbieter via `groq-api.py`:

- **Architektur**: Verwendet den OpenAI-kompatiblen GroqCloud-Endpunkt — keine Formatkonvertierung. Der SSE-Stream wird direkt weitergeleitet.
- **Endpunkt**: `https://api.groq.com/openai/v1/chat/completions`
- **API-Key**: `GRQ_API_KEY` in `/etc/apache2/envvars`.
- **Hinweis**: Ein `User-Agent`-Header ist erforderlich, um Cloudflare-Schutz zu umgehen (ohne ihn: Fehlercode 1010).
- **Free & Paid Tier**: `llama-3.3-70b-versatile`, `llama-3.1-8b-instant`, `meta-llama/llama-4-scout-17b-16e-instruct`, `qwen/qwen3-32b`. Nur Paid: `moonshotai/kimi-k2-instruct-0905`.
- Das Modell-Dropdown aktualisiert sich automatisch basierend auf dem gewählten Tier.
- Der DeepThink-Button und -Indikator werden ausgeblendet, wenn GroqCloud aktiv ist.
- Alle Modelle laufen auf GroqClouds LPU-Hardware (Language Processing Unit) für sehr geringe Latenz.

### LLM-Einstellungs-Panel

Ein dediziertes **LLM-Einstellungs**-Panel (getrennt vom Haupt-Einstellungs-Panel) hält anbieterspezifische Optionen aus der Haupt-UI heraus:

- **Anbieterauswahl**: Umschalten zwischen OpenAI, DeepSeek, Google Gemini, Hugging Face und GroqCloud — immer nur einer aktiv.
- **OpenAI-Optionen**: Free / Paid Auswahl mit automatischer Modelllistenaktualisierung.
- **DeepSeek-Optionen**: Standardmodus (Normal Chat / DeepThink), Datenschutz-Toggle (X-No-Training-Header).
- **Google-Optionen**: Free / Paid Auswahl mit automatischer Modelllistenaktualisierung.
- **Hugging Face-Optionen**: Free / Paid Auswahl mit automatischer Modelllistenaktualisierung.
- **GroqCloud-Optionen**: Free / Paid Auswahl mit automatischer Modelllistenaktualisierung.
- **Kompressor-Optionen**: Aktivierungs-Toggle, Auswahl des Komprimierungs-Anbieters (nur bezahlte Anbieter), Auswahl des Komprimierungs-Modells. Standard: aktiviert, DeepSeek / `deepseek-chat`.
- **Modell-Dropdown**: Immer sichtbar, Inhalt aktualisiert sich automatisch basierend auf Anbieter und Plan.
- Alle Einstellungen werden in `localStorage` gespeichert und bleiben nach dem Seitenreload erhalten.

### 429-Rate-Limit-Handling

Das Google Gemini Free Tier erzwingt strenge Rate Limits (5 RPM, 20 RPD). Der Client behandelt diese elegant:

- Bei einer 429-Antwort wiederholt der Client automatisch bis zu **3 Mal** mit **15-Sekunden-Intervallen**.
- Während der Wartezeit wird ein Countdown direkt im Chat angezeigt: *„Rate limit erreicht – warte 15 Sekunden und versuche erneut... (Versuch 1/3)"*
- Nach 3 fehlgeschlagenen Versuchen wird die Tageslimit-Prüfung ausgelöst und bei Bedarf der blaue Tageslimit-Banner angezeigt.
- Ausführliche Fehlerdetails werden zur Diagnose ins Server-Log geschrieben.
- Die Wiederholungslogik unterscheidet zwischen temporären RPM-Limits (wiederholbar) und erschöpftem Tageskontingent (nicht wiederholbar).

### Zwischenablage-Handler (Ctrl+V)

Ein ausgefeilter Zwischenablage-Handler fängt Einfüge-Ereignisse ab und reagiert intelligent basierend auf dem Inhaltstyp:

**Textinhalt** → Einfüge-Dialog erscheint mit zwei Optionen:
- „An Cursorposition einfügen" — fügt den Text direkt an der Cursorposition ins Eingabefeld ein
- „Als Datei anhängen" — behandelt den Zwischenablagentext als `clipboard.txt` und hängt ihn als Datei an die nächste Nachricht an

**Bildinhalt** → Eine Vorschau-Box erscheint über dem Eingabefeld mit dem Bild, seiner Grösse in KB und einem Entfernen-Button. Das Bild ist bereit, mit der nächsten Nachricht gesendet zu werden (sofern das Modell Bilder unterstützt).

**Dateipfade vom Dateimanager (XFCE/Thunar, KDE/Dolphin)** → Diese werden blockiert und ein Alert angezeigt:
> „Im Dateimanager kopierte Dateien können vom Browser nicht gelesen werden. Bitte stattdessen den Upload-Button verwenden."

**Technischer Hintergrund**: Unter Linux/X11/Firefox blockiert `e.preventDefault()` Einfüge-Ereignisse nicht zuverlässig. Die Lösung: Einfügen erlauben, dann sofort den Inhalt via `setTimeout(0)` prüfen und leeren falls Dateipfade erkannt werden. Erkennungslogik: 2 oder mehr Zeilen, bei denen jede mit `/` oder `file://` beginnt. Ein `requestAnimationFrame`-Aufruf stellt sicher, dass das Eingabefeld visuell geleert wird bevor der Alert-Dialog erscheint.

### Datei-Upload mit Sicherheitsprüfung

- Akzeptierte Formate: `.txt`, `.pdf`, `.doc`, `.docx`, `.jpg`, `.jpeg`, `.png`, `.csv`, `.xlsx`, `.pptx`
- Verarbeitbare Formate (Inhaltsextraktion): `.txt`, `.pdf`
- Andere akzeptierte Formate: als binärer Kontext angehängt (ohne Textextraktion)
- Maximale Dateigrösse: **10 MB**
- Maximaler extrahierter Inhalt: **250.000 Zeichen**

**Magic-Byte-Prüfung** (erste 20 Bytes) erkennt und blockiert ausführbare Dateien unabhängig von der Dateinamenserweiterung:

| Plattform | Format | Signatur |
|-----------|--------|----------|
| Windows 32/64 bit | PE/MZ Executable | `4D 5A` |
| Linux 32 bit | ELF32 | `7F 45 4C 46 01` |
| Linux 64 bit | ELF64 | `7F 45 4C 46 02` |
| ARM 32 bit | ELF32 ARM | `7F 45 4C 46 01 01 01 00 ... 02 00 28 00` |
| ARM 64 bit | ELF64 AArch64 | `7F 45 4C 46 02 01 01 00 ... 02 00 B7 00` |
| macOS 32 bit | Mach-O | `CE FA ED FE` |
| macOS 64 bit | Mach-O | `CF FA ED FE` |
| macOS Universal | Fat Binary | `CA FE BA BE` |
| macOS/iOS ARM 32 | Big Endian | `FE ED FA CE` |
| macOS/iOS ARM 64 | Big Endian | `FE ED FA CF` |
| Linux/macOS | Shell-Skript | `23 21` (#!) |
| Python | Bytecode (.pyc) | `55 0D 0D 0A` |

**PDF-Extraktion**: Verwendet PDF.js 3.11.174 von CDN mit automatischem Fallback auf einen sekundären CDN. Fortschritt wird seitenweise angezeigt. Extraktions-Timeout: 30 Sekunden.

**Hochgeladene Dateien werden als Datei-Cards** in der Benutzernachricht angezeigt (siehe [Datei-Card-Anzeige](#datei-card-anzeige)).

### Umlaut-Platzhalter-System

Eine einzigartige Lösung für ein grundlegendes Problem mit der DeepSeek API und deutschem Text:

**Problem**: DeepSeek ersetzt intern deutsche Umlaute in Dateiinhalten durch ASCII-Äquivalente (z.B. `Ä → AeNDERUNG`, `Ü → MUeSSEN`). Dieses Verhalten kann nicht via System-Prompts oder API-Parameter unterdrückt werden.

**Lösung**: Vor dem Senden von Dateiinhalten an DeepSeek werden Umlaute durch eindeutige Platzhalter ersetzt. DeepSeek gibt diese Platzhalter unverändert zurück. JavaScript ersetzt sie anschliessend nach Empfang der Antwort wieder durch echte Umlaute.

| Original | Platzhalter |
|----------|-------------|
| `ä` | `[[AE]]` |
| `ö` | `[[OE]]` |
| `ü` | `[[UE]]` |
| `ß` | `[[SS]]` |
| `Ä` | `[[CAE]]` |
| `Ö` | `[[COE]]` |
| `Ü` | `[[CUE]]` |

**Wichtiges Implementierungsdetail**: Die Funktionen `encodeUmlautsForAI()` und `decodeUmlautsFromAI()` verwenden **ausschliesslich Unicode-Escape-Sequenzen** (`\u00e4` statt `ä`) und `split/join` statt Regex — dies ist entscheidend um Korruption beim Dateitransfer via Git zu vermeiden.

Die Dekodierung läuft **sowohl während des Streamings** (Token für Token) als auch nach Empfang der vollständigen Antwort.

Dieses System wird **nur auf Dateiinhalte angewendet**, nicht auf reguläre Benutzernachrichten oder System-Prompts.

### DeepThink-Modus

- Umschaltbar über einen dedizierten Button (Pill-Modus-Stil) in der zweiten Button-Zeile.
- Im DeepThink-Modus wird das Modell `deepseek-reasoner` verwendet (echtes Chain-of-Thought-Reasoning).
- Der Button ändert sich visuell: dunkel/inaktiv (`#2d2d2d`) → aktiv blau (`#1e3a5f` Hintergrund, `#4dabf7` Rahmen und Text).
- Eine Indikatorleiste erscheint unterhalb der Buttons mit „DeepThink-Modus aktiv: Tiefgehende Analyse läuft".
- Kontext- und Ausgabe-Token-Limits werden automatisch angepasst (siehe [Modell-Konfiguration](#modell-konfiguration)).
- Der Modus wird bei jeder Nachricht aufgezeichnet und in Exporten angezeigt.
- Der Standardmodus (Chat oder DeepThink) kann in den Einstellungen gesetzt werden und wird in `localStorage` gespeichert.

### Modellerkennung & Fähigkeiten

Beim Start fragt der Client `/cgi-bin/deepseek-models.py` ab, das seinerseits den DeepSeek `/v1/models`-Endpunkt aufruft:

- Erkannte Modell-IDs werden im Server-Header angezeigt: `Model: deepseek-chat, deepseek-reasoner`
- Eine `MODEL_CAPABILITIES`-Map definiert welche Modelle Bilder unterstützen:
  ```javascript
  const MODEL_CAPABILITIES = {
      'deepseek-chat':     { images: false, text: true },
      'deepseek-reasoner': { images: false, text: true },
      'deepseek-v4':       { images: true,  text: true },  // bereit für zukünftige Modelle
      'default':           { images: false, text: true },
  };
  ```
- Wenn ein Bild via Zwischenablage eingefügt oder eine `.jpg`/`.png`-Datei hochgeladen wird und das aktuelle Modell keine Bilder unterstützt, blockiert ein Alert die Operation.
- Diese Architektur ist **vorwärtskompatibel**: wenn DeepSeek V4 mit Bildunterstützung veröffentlicht wird, funktioniert es automatisch ohne Codeänderungen.

### Mehrsprachiges System

Die UI unterstützt mehrere Sprachen, die aus einer externen `language.xml`-Datei geladen werden:

**Aktuell enthaltene Sprachen**:
- Englisch (`en`) — Standard
- Deutsch (`de`) — mit formeller/informeller Anredeform (Sie/Du)
- Spanisch (`es`) — mit formeller/informeller Anredeform (Usted/Tú)
- Benutzerdefinierter Slot (`custom`) — aktivierbar via `visible="true"` in `language.xml`

**So funktioniert es**:
- Alle UI-Texte werden über numerische IDs referenziert (z.B. `t(205)` = Send-Button-Label).
- `loadLanguage()` lädt und parst `language.xml` beim Seitenaufruf.
- `t(id)` gibt den Text für die aktuelle Sprache zurück, mit Fallback auf Englisch falls nicht gefunden.
- `tf(id, ...args)` unterstützt Platzhalter-Substitution (`{0}`, `{1}`, ...).
- `tform(idFormal, idInformal)` gibt den passenden Text basierend auf der gewählten Anredeform zurück.
- Sprachumschaltung erfolgt sofort ohne Seitenreload.
- Die gewählte Sprache wird in `localStorage` gespeichert.

**Anredeform-System (Deutsch/Spanisch)**:
- Sprachen können `has_address_form="true"` in `language.xml` deklarieren.
- Für solche Sprachen zeigt das Einstellungs-Panel eine Gruppe „Anredeform" (Formell/Informell).
- Die gewählte Form beeinflusst: System-Prompt (erzwingt konsistente KI-Antworten), Eingabe-Platzhalter, alle Einstellungsbeschreibungen.
- Englisch hat keine Anredeformunterscheidung.

**System-Prompt** wird dynamisch basierend auf Sprache, Anredeform und Modus erstellt:
- Basis-Prompt (Text-IDs 29/30 für formell/informell)
- DeepThink-Ergänzung (Text-IDs 31/32)
- Eine strenge Anweisung für die Datei-Darstellung wird immer auf Englisch angehängt, um konsistentes Verhalten unabhängig von der UI-Sprache sicherzustellen.

### Einstellungen (Toggles statt Radio-Buttons)

Alle Einstellungen verwenden **Toggle-Schalter** (Links-nach-Rechts-Schieberegler), niemals Radio-Buttons oder Checkboxen:

| Gruppe | Einstellung | Toggle-Farbe |
|--------|-------------|-------------|
| Sprache | EN / DE / ES / Custom | Grün (persönliche Präferenz) |
| Anredeform | Formell / Informell | Grün (persönliche Präferenz) |
| Standardmodus | Normal Chat / DeepThink | Blau (technischer Modus) |
| Datenschutz | Daten nicht für Training verwenden | Grün |

**Toggle-Verhalten**:
- Innerhalb einer Gruppe verhalten sich Toggles wie Radio-Buttons: einen aktivieren deaktiviert die anderen.
- Klick irgendwo auf die `setting-item`-Zeile aktiviert den Toggle (nicht nur das Toggle-Element selbst).
- Visuelles Feedback: Aktive Elemente erhalten einen farbigen Hintergrund (`#1a2e1a` grün oder `#1e3a5f` blau).

**Datenschutz-Toggle**: Setzt den Header `X-No-Training: true` in API-Anfragen (unterstützt durch DeepSeeks Opt-out-Mechanismus).

**Einstellungs-Persistenz**: Alle Einstellungen werden in `localStorage` unter dem Key `deepseekSettings` gespeichert. Aktuelle `SETTINGS_VERSION: 1.7`. Die Funktion `migrateSettings()` gewährleistet Rückwärtskompatibilität mit älteren Einstellungen.

### Session-Management

Jedes Gespräch wird automatisch als benannte Session verwaltet:

- **Session-ID-Format**: `YYYY-MM-DD_HHMMSS_random` (z.B. `2026-02-16_143045_abc123`) — clientseitig generiert, serverseitig validiert.
- **Automatisches Speichern**: Nach jedem Nachrichten-Paar (Benutzer + KI) wird das vollständige `contextHistory.messages`-Array als JSON-Datei auf dem Server gespeichert.
- **Session-Dateiformat**: `{sessionId}.json` in `/var/www/deepseek-chat/sessions/`, `chmod 600`.
- **Chat-Verlauf laden Modal**: Zeigt alle gespeicherten Sessions mit ID, Datum, Nachrichten-Vorschau und Nachrichtenanzahl. Jede Session hat [Laden] (grün) und [Löschen] (rot) Buttons.
- **Ladeverhalten**: Beim Laden einer Session wird der aktuelle Chat zuerst automatisch gespeichert, dann wird die gewählte Session mit vollständiger Nachrichtenhistorie und UI-Wiederherstellung geladen.
- **Session-Löschung**: Die JSON-Datei wird sofort vom Server gelöscht.

**CGI-Skripte**:
- `save-session.py` — POST: empfängt `{sessionId, messages}`, validiert ID-Format, schreibt JSON
- `load-session.py` — GET: gibt Liste mit Vorschauen zurück; GET mit `?id=`: gibt vollständige Session-Daten zurück
- `delete-session.py` — DELETE: entfernt Session-Datei

### Exportfunktionen

**Globaler Export** (Dropdown-Button in der Hauptzeile):

| Format | Erzeugung | Enthält |
|--------|-----------|---------|
| PDF | Serverseitig (ReportLab) | Header, Statistiken, Inhaltsverzeichnis, vollständiger Chat |
| Markdown | Serverseitig | Identische Struktur wie PDF, mit Markdown-Ankern |
| TXT | Serverseitig | Reiner Text mit Trennzeichen |
| RTF | Serverseitig | RTF-Format, Umlaute als RTF-Codes (keine externe Bibliothek) |
| **In Zwischenablage kopieren** | **Clientseitig (kein Server-Roundtrip)** | **Reiner Text, identisches Format wie TXT-Export** |

**Nachrichtenweiser Export** (Hover-Button auf jeder Nachricht):

| Format | Erzeugung |
|--------|-----------|
| TXT | Clientseitig (JavaScript Blob, kein Server-Roundtrip) |
| Markdown | Clientseitig |
| RTF | Clientseitig |
| PDF | Serverseitig (einzelne Nachricht an `export-pdf.py` gesendet) |

**Export-Inhalt** (PDF/Markdown):
- Header mit Servername, IP, Exportdatum, Sprach-/Anredeform-Einstellungen
- Statistik-Abschnitt: Nachrichtenanzahl, verwendete Modi, angehängte Dateien, geschätzte Token, Dauer
- Inhaltsverzeichnis mit allen Nachrichten
- Vollständige Chat-Historie mit Zeitstempeln und Modus-Indikatoren
- Farbkodierung nach Nachrichtenrolle und Modus

**In Zwischenablage kopieren**: Der gesamte Chat wird clientseitig als reiner Text zusammengestellt und direkt via `navigator.clipboard.writeText()` in die Systemzwischenablage geschrieben. Eine kurze „Kopiert!"-Bestätigung erscheint für 2 Sekunden im Export-Button.

**PDF-technischer Hinweis**: Binäre PDF-Daten werden ausschliesslich via `sys.stdout.buffer` mit als Bytes kodierten HTTP-Headern geschrieben — vermeidet den „Bad header"-Fehler bei Mischung von `print()` (Textmodus) mit Binärausgabe.

### Feedback-Buttons & Logging

Vier Buttons erscheinen beim Hover für jede KI-Antwort (links unten):

- **Kopieren** — Kopiert Nachrichtentext in die Zwischenablage; zeigt „Kopiert!" für 2 Sekunden, dann zurücksetzen.
- **Gefällt mir** — Markiert die Antwort positiv (blau hervorgehoben); sendet einen LIKE-Eintrag ins Server-Log. Nochmaliger Klick entfernt den Like.
- **Gefällt mir nicht** — Markiert die Antwort negativ (rot hervorgehoben); sendet einen DISLIKE-Eintrag. Gefällt mir und Gefällt mir nicht sind gegenseitig exklusiv.
- **Regenerieren** — Entfernt die aktuelle KI-Antwort aus Kontext und DOM, ruft dann die API erneut mit derselben Benutzernachricht und vollständiger vorheriger Historie auf.

**Serverseitiges Log-Format** (`multi-llm-chat.log`):
```
2026-02-17 17:30:00 | IP: 192.168.1.x | POST /cgi-bin/deepseek-api.py | Status: 200
2026-02-17 17:30:00 | IP: 192.168.1.x | FEEDBACK | LIKE | msg_5 | "Erste 60 Zeichen der Nachricht..."
```
**Nie geloggt**: API-Keys, Session-Inhalte oder Nachrichtentext über die 60-Zeichen-Feedback-Vorschau hinaus.

### Dynamische Kontext-Anzeige

Der Server-Header zeigt vier Informationszeilen:
1. Servername (in Blau, `#4dabf7`)
2. `IP: xxx.xxx.xxx.xxx`
3. `Kontext: XX% (modellname)`
4. `Modell: deepseek-chat, deepseek-reasoner`

**Berechnung der Kontextauslastung**:
- Geschätzte Token = Gesamtzeichen in aktuellen Nachrichten × `TOKENS_PER_CHAR` (0,25)
- Nur die letzten N Nachrichten werden gezählt (N = `maxContextMessages` aus `MODEL_CONFIG`)
- System-Prompt-Token werden separat hinzugefügt
- Prozentwert = geschätzte Token / `maxContextTokens` × 100

**Warnsystem**: Ab 90% wird die Kontextzeile rot und blinkt (CSS-Animation, Deckkraft 0 → 1, 1-Sekunden-Zyklus) — eine gut sichtbare Warnung, dass das Kontextfenster fast voll ist.

Die Anzeige aktualisiert sich automatisch bei: jeder gesendeten Nachricht, jeder gelöschten Nachricht, jedem Modellwechsel.

### Datei-Card-Anzeige

Wenn eine Datei hochgeladen oder Zwischenablagentext angehängt wird, zeigt die Benutzernachricht eine **Datei-Card** — ein kompaktes visuelles Element ähnlich wie bei Claude oder ChatGPT:

```
┌─────────────────────────────────────┐
│  [PDF]  │  filename.pdf             │
│  Icon   │  PDF-Dokument             │
└─────────────────────────────────────┘
```

- Zeigt Dateityp-Badge (PDF, TXT, XLSX etc.) abgeleitet aus der Dateiendung
- Zeigt gekürzten Dateinamen (max. 30 Zeichen mit `...`)
- Gilt für: echte Datei-Uploads via Upload-Button, Zwischenablagentext als Datei (`clipboard.txt`), alle anderen akzeptierten Formate und Audio-Aufnahmen
- Audio-Aufnahmen zeigen das Badge `AUDIO` mit dem lokalisierten Label (z.B. „Audioaufnahme")

### Multi-Datei-Upload

Der Upload-Button unterstützt die Auswahl von **mehreren Dateien gleichzeitig**:

- Alle ausgewählten Dateien werden einzeln validiert (Formatprüfung, Magic-Byte-Prüfung, Bild-Fähigkeitsprüfung).
- Textextrahierbare Dateien (`.txt`, `.pdf`) werden der Reihe nach verarbeitet; ihre Inhalte werden mit einem `---`-Trennzeichen und einem `[dateiname]`-Header kombiniert.
- Die Datei-Info-Leiste zeigt alle Dateien mit ` | ` getrennt in einer einzigen Zeile.
- Eine Datei-Card wird pro Datei in der Benutzernachricht angezeigt.
- Akzeptierte Formate: `.txt`, `.pdf`, `.doc`, `.docx`, `.jpg`, `.jpeg`, `.png`, `.csv`, `.xlsx`, `.pptx`

### Audio-Aufnahme

Der Client verfügt über einen integrierten **Mikrofon-Aufnahme-Button**, der direkte Spracheingabe für audio-fähige Modelle ermöglicht:

- **Button**: `audioButton` — Pill-Modus-Stil, positioniert in Button-Zeile 2 neben dem DeepThink-Button.
- **Sichtbarkeit**: Der Button wird nur angezeigt, wenn das aktuell gewählte Modell Audio-Input unterstützt. Er wird automatisch ausgeblendet, wenn ein nicht-audio-fähiges Modell aktiv ist. Dies wird von `updateAudioButtonVisibility()` gesteuert, das bei jedem Modellwechsel aufgerufen wird.
- **Audio-fähige Modelle** (Konstante `AUDIO_CAPABLE_MODELS`):
  - **Google Gemini**: `gemini-2.5-flash`, `gemini-2.5-pro`, `gemini-1.5-pro`, `gemini-2.0-flash`
  - **OpenAI**: `gpt-4o`, `gpt-4.1`
- **Aufnahme-Ablauf**: `getUserMedia()` → `MediaRecorder`-API → stückweise Aufnahme → `Blob` beim Stopp zusammengesetzt → base64-kodiert.
- **MIME-Typ**: `audio/webm` (Chrome/Firefox) oder `audio/mp4` (Safari) — zur Laufzeit automatisch erkannt.
- **Nach der Aufnahme**: Die Audio-Daten werden im `fileInfo`-Feld mit einer AUDIO-Badge-Card angezeigt.
- **Senden**: `audio_data` (base64-String) und `audio_mime_type` werden im JSON-Anfragekörper neben der Textnachricht übermittelt. Das `hasFile`-Flag wird für Audio **nicht** gesetzt — kein Dateiverarbeitungs-System-Prompt wird injiziert.
- **Gegenseitige Exklusivität**: Datei-Upload und Audio-Aufnahme sind gegenseitig exklusiv. Eine Aufnahme starten löscht ausstehende Dateianhänge und umgekehrt.
- **Backend — Google (`google-api.py`)**: Audio wird als `inline_data`-Block im nativen Gemini-Format an die letzte Benutzernachricht angehängt. Das Modell empfängt und verarbeitet das Audio direkt.
- **Backend — OpenAI (`openai-api.py`)**: Audio wird als `input_audio`-Block im OpenAI-Format (`format: webm` oder `mp4`) an die letzte Benutzernachricht angehängt.
- **Wartungsregel** (im Manifest dokumentiert): Sobald ein integrierter LLM-Anbieter Audio-Unterstützung für ein Modell hinzufügt oder entfernt, **muss** `AUDIO_CAPABLE_MODELS` in `index.html` sofort aktualisiert werden.

### Kompressor — Intelligente Kontext-Komprimierung

Jedes Sprachmodell hat ein endliches Kontextfenster. In langen Sitzungen — insbesondere mit grossen Datei-Uploads, ausgedehnten Analyse-Workflows oder mehrstündigen Gesprächen — füllt sich der Kontext auf und führt zu API-Fehlern (400/413), die den Benutzer zwingen, einen neuen Chat zu starten und den gesamten Gesprächsfaden zu verlieren.

Der **Kompressor** löst dieses Problem automatisch und transparent.

#### Grundprinzip

Statt alte Nachrichten blind abzuschneiden oder einen manuellen Neustart zu erzwingen, **fasst** der Kompressor die älteste Hälfte des Gesprächs via einem zweiten, dedizierten LLM-Aufruf **zusammen**. Diese Zusammenfassung wird in den System-Prompt nachfolgender Anfragen injiziert. Das aktive Modell „erinnert" sich durch die Zusammenfassung an die Vergangenheit — das Gespräch kann unbegrenzt fortgeführt werden ohne Kontextverlust.

#### Auslöse-Schwellwerte

| Schwellwert | Aktion |
|-------------|--------|
| **70%** Kontextauslastung | Erste Komprimierungsrunde |
| **85%** Kontextauslastung | Zweite Komprimierungsrunde |
| **95%** Kontextauslastung | Dritte Komprimierungsrunde |

Jeder Schwellwert löst pro Sitzung höchstens einmal aus. Nach jeder Komprimierung wird der Zähler zurückgesetzt, sodass die Schwellwerte erneut auslösen können, wenn sich der Kontext wieder füllt.

#### Komprimierungs-Ablauf

1. Der Client schätzt die Kontextauslastung nach jeder gesendeten Nachricht.
2. Wenn ein Schwellwert überschritten wird, wird `compress-context.py` **vor** dem Haupt-API-Aufruf aufgerufen.
3. Die ältesten 50% der Nachrichten werden extrahiert. Der Cutoff rückt zur nächsten Benutzernachricht vor, um API-Kompatibilität zu gewährleisten (Kontext beginnt immer mit einer Benutzeranfrage).
4. Base64-Daten, Bilder und multimodale Inhalte werden herausgefiltert — nur reiner Text wird an das Komprimierungs-LLM gesendet.
5. Das Komprimierungs-LLM gibt eine strukturierte Zusammenfassung zurück.
6. Die alten Nachrichten werden durch einen einzelnen Zusammenfassungs-Eintrag ersetzt (Flag `compressed: true`).
7. Die Zusammenfassung wird dem effektiven System-Prompt aller nachfolgenden Aufrufe hinzugefügt — niemals als eigenständige Nachricht gesendet (was bei den meisten APIs zu 400-Fehlern führen würde).
8. Der aktualisierte Kontext wird gespeichert. Der Haupt-API-Aufruf erfolgt mit dem komprimierten Kontext.

#### Intelligentes Verwerfen der Zusammenfassung bei manuellem Löschen

Wenn der Benutzer manuell Nachrichten löscht, prüft der Kompressor ob der Kontextprozentsatz unter den **zuletzt ausgelösten Schwellwert** fällt (nicht nur unter 70%). Falls ja, wird die Komprimierungszusammenfassung automatisch entfernt und das gesamte Schwellwert-Tracking zurückgesetzt — so entspricht der Komprimierungszustand immer dem tatsächlichen Gesprächsinhalt.

#### Anbieter-Einschränkung (nur bezahlt)

Der Kompressor erfordert einen separaten LLM-Aufruf, der grosse Token-Mengen umfassen kann. Die Free-Tier-Rate-Limits von Groq (6.000–12.000 TPM) und Hugging Face sind für eine zuverlässige Komprimierung realer Gespräche unzureichend. Nur bezahlte Anbieter werden angeboten:

| Anbieter | Komprimierungs-Modelle |
|----------|------------------------|
| DeepSeek | `deepseek-chat`, `deepseek-reasoner` |
| OpenAI | `gpt-4o-mini`, `gpt-4o`, `gpt-4.1` |
| Google | `gemini-2.5-flash`, `gemini-2.5-pro`, `gemini-1.5-pro` |

**Empfohlener Standard**: DeepSeek + `deepseek-chat` — keine Rate Limits, niedrigste Kosten, zuverlässigste Ergebnisse.

#### Ergebnisdateien

Jede Komprimierungsrunde wird gespeichert unter:
```
/var/www/deepseek-chat/kompressor/kompressor_JJJJMMTT_HHMMSS.txt
```

### Guthaben- und Tageslimit-Banner

Der Client bietet klare, dauerhafte visuelle Rückmeldung wenn API-Kontingente erschöpft sind:

**Roter Banner — „Guthaben muss erneuert werden !"** (bezahlte Anbieter):
- Wird angezeigt wenn eine bezahlte API erschöpftes Guthaben meldet
- **DeepSeek**: ausgelöst durch HTTP 402
- **OpenAI**: ausgelöst durch HTTP 429 + `insufficient_quota` im JSON-Antwort-Body
- Bleibt sichtbar bis er manuell über den ×-Button geschlossen wird

**Blauer Banner — „Tageslimit erreicht !"** (Free-Tier-Anbieter):
- Wird angezeigt wenn eine Free-Tier-API ein erschöpftes Tageskontingent meldet
- **Google Gemini**: ausgelöst durch HTTP 429 + tägliche Schlüsselwörter im Antwort-Body
- **GroqCloud**: ausgelöst durch HTTP 429
- **Hugging Face**: ausgelöst durch HTTP 429
- Bleibt sichtbar bis er manuell über den ×-Button geschlossen wird

Beide Banner werden als fixierte Elemente am oberen Rand des Browserfensters mit einem ×-Schliessen-Button gemäss der Standard-Pill-Style-Konvention implementiert.

### Kontextfenster-Überschreitung

Wenn das Kontextfenster des aktiven Modells vollständig gefüllt ist und die API einen Fehler zurückgibt (HTTP 400 mit kontextbezogenen Schlüsselwörtern), zeigt der Client keine generische Fehlermeldung. Stattdessen erscheint direkt im Chat eine **interaktive Box**:

- **Blau umrandete Box** mit der Meldung: *„Die maximale Chat-Grösse des aktuellen LLM's wurde erreicht."*
- **Grüner Button**: „Neuen Chat starten mit aktuellem Kontext" — implementiert **Option C**:
  1. Die aktuelle Session wird automatisch gespeichert
  2. Die letzte Komprimierungszusammenfassung (falls vorhanden) wird mit allen nachfolgenden Nachrichten als reiner Text kombiniert
  3. Ein neuer Chat startet mit diesem kombinierten Kontext als vorgeladener Dateianhang — das Gespräch wird nahtlos fortgesetzt
- **Blauer Button**: „Neuen Chat starten ohne Kontext" — sauberer Neustart:
  1. Die aktuelle Session wird automatisch gespeichert
  2. Ein neuer Chat startet mit leerem Kontext

Dieser Ansatz ermöglicht **verkettete Gespräche** über mehrere Sessions — theoretisch unbegrenzt lang.

Alle fünf CGI-Proxy-Skripte erkennen Kontext-Überlauf via HTTP-Statuscode-Analyse und Schlüsselwortabgleich im Antwort-Body und geben `error_type: 'context_exceeded'` an den Client zurück.

---

### API-Proxy-Infoblock (ab 08.03.2026)

Jedes der fünf CGI-Proxy-Skripte (`openai-api.py`, `deepseek-api.py`, `google-api.py`, `hugging-api.py`, `groq-api.py`) enthält direkt nach der Kodierungsdeklaration einen strukturierten Dokumentations-Header:

- **Import-Datum** — wann die Datei zuletzt aktualisiert wurde
- **Modellversion** — Version jedes unterstützten Modells/Untermodells
- **Kontextfenster** — Eingabe- und Ausgabe-Token-Limits pro Modell
- **Fähigkeiten** — Nur Text / Text + Bilder + Audio + Video
- **Free/Paid-Zuordnung** — für Anbieter mit Tier-Unterscheidung
- **Quelllink** — offizielle API-Dokumentation

Dies stellt sicher, dass Modellinformationen immer direkt im Quellcode nachvollziehbar sind, ohne externe Dokumentation konsultieren zu müssen.

## Das Hilfsskript `repo2text.sh`

Dieses Bash-Skript wurde speziell entwickelt, um **den gesamten Quellcode eines GitHub-Repositories als einzelne Textdatei zu exportieren** — ideal, um den vollständigen Projektkontext an einen KI-Assistenten weiterzugeben.

**So funktioniert es**:
- Klont das Repository mit `git clone --depth 1`.
- Analysiert alle Textdateien (MIME-Typ + `grep -Iq .`) und schreibt sie mit Trennzeichen in eine Ausgabedatei.
- Verwendet `sort -z -u` um Dateipfade vor der Verarbeitung zu deduplizieren — verhindert doppelte Dateieinträge.
- Verwendet einen eindeutigen Begrenzer (`############ FILE: ... ############`) der nicht im Quellcode vorkommen kann, um fehlerhafte Trennungen zu vermeiden.
- Respektiert explizit `.gitignore` und `.gitattributes`.
- Unterstützt TXT, JSON und Markdown als Ausgabeformate.
- Erstellt ein ZIP-Archiv der Exportdatei.
- Enthält Metadaten: Commit-Hash, Branch, Zeitstempel.

**Besondere Optionen**:
- `--flat`: Nur Dateinamen ohne Pfade verwenden.
- `-o, --only PFAD`: Nur ein bestimmtes Unterverzeichnis exportieren.
- `-md5, --md5`: MD5-Prüfsumme für jede Datei berechnen und einschliessen.
- Intelligente Erkennung der Remote-URL beim Ausführen innerhalb eines Git-Repositories.
- Sowohl `md5sum` (Linux) als auch `md5` (macOS) werden unterstützt.

**Beispiele**:

```bash
# Einfacher Export (interaktive URL-Eingabe)
./repo2text.sh

# Export mit URL als Markdown
./repo2text.sh -f md https://github.com/debian-professional/multi-llm-chat.git

# Nur das Verzeichnis 'shell-scripts' mit flacher Struktur exportieren
./repo2text.sh --flat -o shell-scripts https://github.com/debian-professional/multi-llm-chat.git

# Export mit MD5-Prüfsummen
./repo2text.sh -md5 https://github.com/debian-professional/multi-llm-chat.git
```

**Warum ist das nützlich?**
- Ermöglicht vollständige Projektdokumentation in einer einzigen Datei.
- Perfekt zum Einfügen ganzer Codebasen in KI-Chats.
- Die MD5-Option hilft beim Überprüfen der Dateiintegrität nach dem Export.

> `repo2text` ist auch als eigenständiges Projekt verfügbar: [github.com/debian-professional/repo2text](https://github.com/debian-professional/repo2text)

---

## Sicherheitsarchitektur im Detail

Sicherheit hatte während des gesamten Projekts höchste Priorität. Hier alle wichtigen Massnahmen:

### 1. API-Key — Nie dem Client gegenüber exponiert
- Alle API-Keys werden **ausschliesslich** in Apache-Umgebungsvariablen gehalten (gesetzt in `/etc/apache2/envvars`).
- Jedes CGI-Skript ruft seinen Key via `os.environ.get('..._API_KEY')` ab.
- Der Client kommuniziert nur mit lokalen CGI-Proxies — nie direkt mit externen APIs.
- Selbst bei einem XSS-Angriff könnten die Keys nicht von der Seite gelesen werden.

### 2. Magic-Byte-Prüfung gegen ausführbare Dateien
- Vor dem Lesen einer hochgeladenen Datei werden die ersten 20 Bytes gegen eine umfassende Signatur-Datenbank geprüft (siehe [Datei-Upload mit Sicherheitsprüfung](#datei-upload-mit-sicherheitsprüfung)).
- Bei übereinstimmender Signatur wird der Upload mit einer detaillierten Fehlermeldung blockiert, die die erkannte Plattform und das Format anzeigt.
- Dieser Schutz funktioniert auch wenn bösartige Dateien umbenannt werden (z.B. `virus.exe` → `rechnung.pdf`).

### 3. Sichere Session-Speicherung
- Sessions-Verzeichnis: `/var/www/deepseek-chat/sessions/` — `chmod 700`
- Jede Session-Datei: `chmod 600`
- Session-ID-Format wird serverseitig validiert — kein Path-Traversal möglich.

### 4. Logging ohne sensible Daten
- Log enthält: Zeitstempel, IP-Adressen, HTTP-Methoden, Pfade, Statuscodes, Fehlermeldungen.
- **Nie geloggt**: API-Keys, Session-Inhalte, Nachrichtentext (über 60-Zeichen-Feedback-Vorschauen hinaus).
- OPTIONS-Anfragen werden gefiltert, um Log-Überflutung zu verhindern.

### 5. Keine direkte Client-API-Kommunikation
- Alle sicherheitskritischen Operationen finden serverseitig via Python CGI statt.
- Der Client hat keine Kenntnis von API-Zugangsdaten, Server-Pfaden oder Session-Speicherorten.

### 6. Input-Validierung
- Dateiformate werden per Erweiterung und per Magic Bytes validiert.
- Session-IDs werden serverseitig gegen das erwartete Format-Regex validiert.
- Zwischenablage-Einfügen wird gefiltert, um Dateipfade zu blockieren bevor sie die API erreichen.

### 7. Transportsicherheit
- HTTPS wird via Apache-SSL-Konfiguration erzwungen (`deepseek-chat-ssl.conf`).
- HTTP-Konfiguration (`deepseek-chat.conf`) wird via `a2dissite` deaktiviert.

---

## Deployment & Verwendung

### Voraussetzungen

- Debian-basiertes System (oder jedes Linux mit Apache, Python 3, Bash)
- Apache mit CGI-Modul (`a2enmod cgi`) und SSL (`a2enmod ssl`)
- Python 3 mit Paketen: `reportlab`
- Für `repo2text.sh`: `jq`, `pv`, `zip`, `git`
- Ein gültiger API-Key für mindestens einen der unterstützten Anbieter

### Installation

**1. Repository klonen** (als Benutzer `source`):
```bash
git clone https://github.com/debian-professional/multi-llm-chat.git /home/source/multi-llm-chat
```

**2. API-Keys konfigurieren**:
```bash
# Zu /etc/apache2/envvars hinzufügen:
export DEEPSEEK_API_KEY="hier-deepseek-api-key-eintragen"
export OPENAI_API_KEY="hier-openai-api-key-eintragen"
export GOOGLE_API_KEY="hier-google-api-key-eintragen"
export HF_API_KEY="hier-huggingface-token-eintragen"
export GRQ_API_KEY="hier-groqcloud-api-key-eintragen"
```

**3. Apache-Konfiguration aktivieren**:
```bash
a2ensite deepseek-chat-ssl.conf
a2dissite deepseek-chat.conf   # einfache HTTP-Konfiguration deaktivieren
systemctl restart apache2
```

**4. Erforderliche Verzeichnisse erstellen**:
```bash
mkdir -p /var/www/deepseek-chat/sessions
chown www-data:www-data /var/www/deepseek-chat/sessions
chmod 700 /var/www/deepseek-chat/sessions
```

**5. Deploy-Skript ausführen** (als root):
```bash
./deploy.sh source
```

**6. Hilfsskripte installieren**:
```bash
./install.sh   # als root — kopiert deploy.sh und sync-back.sh ins Produktionsverzeichnis
```

### Konfiguration

**Modell-Konfiguration** (`MODEL_CONFIG` in `index.html`):
```javascript
const MODEL_CONFIG = {
    // OpenAI
    'gpt-5.4':              { maxContextTokens: 1050000, maxOutputTokens: 16384, maxContextMessages: 100 },
    'gpt-5.2-chat-latest':  { maxContextTokens: 128000,  maxOutputTokens: 16384, maxContextMessages: 80  },
    'gpt-4o':               { maxContextTokens: 128000,  maxOutputTokens: 16384, maxContextMessages: 80  },
    'gpt-4.1':              { maxContextTokens: 1048576, maxOutputTokens: 32768, maxContextMessages: 100 },
    'gpt-4o-mini':          { maxContextTokens: 128000,  maxOutputTokens: 16384, maxContextMessages: 80  },
    'gpt-5-mini':           { maxContextTokens: 128000,  maxOutputTokens: 16384, maxContextMessages: 80  },
    // DeepSeek
    'deepseek-chat':     { maxContextTokens: 100000,  maxOutputTokens: 8192,  maxContextMessages: 50  },
    'deepseek-reasoner': { maxContextTokens: 65000,   maxOutputTokens: 32768, maxContextMessages: 30  },
    // Google Gemini
    'gemini-2.5-flash':  { maxContextTokens: 1048576, maxOutputTokens: 8192,  maxContextMessages: 100 },
    'gemini-2.5-pro':    { maxContextTokens: 1048576, maxOutputTokens: 65536, maxContextMessages: 100 },
    'gemini-1.5-pro':    { maxContextTokens: 2097152, maxOutputTokens: 8192,  maxContextMessages: 100 },
    'gemini-2.0-flash':  { maxContextTokens: 1048576, maxOutputTokens: 8192,  maxContextMessages: 100 },
    // Hugging Face
    'Qwen/Qwen2.5-72B-Instruct':               { maxContextTokens: 128000, maxOutputTokens: 8192, maxContextMessages: 80 },
    'mistralai/Mistral-7B-Instruct-v0.3':      { maxContextTokens: 32768,  maxOutputTokens: 4096, maxContextMessages: 40 },
    'microsoft/Phi-3.5-mini-instruct':         { maxContextTokens: 128000, maxOutputTokens: 4096, maxContextMessages: 60 },
    'meta-llama/Meta-Llama-3.1-70B-Instruct':  { maxContextTokens: 128000, maxOutputTokens: 8192, maxContextMessages: 80 },
    'meta-llama/Meta-Llama-3.1-405B-Instruct': { maxContextTokens: 128000, maxOutputTokens: 8192, maxContextMessages: 80 },
    'mistralai/Mixtral-8x7B-Instruct-v0.1':    { maxContextTokens: 32768,  maxOutputTokens: 4096, maxContextMessages: 40 },
    // GroqCloud
    'llama-3.3-70b-versatile':                   { maxContextTokens: 128000, maxOutputTokens: 8192, maxContextMessages: 80 },
    'llama-3.1-8b-instant':                      { maxContextTokens: 131072, maxOutputTokens: 8192, maxContextMessages: 80 },
    'meta-llama/llama-4-scout-17b-16e-instruct': { maxContextTokens: 131072, maxOutputTokens: 8192, maxContextMessages: 80 },
    'qwen/qwen3-32b':                            { maxContextTokens: 131072, maxOutputTokens: 8192, maxContextMessages: 80 },
    'moonshotai/kimi-k2-instruct-0905':          { maxContextTokens: 131072, maxOutputTokens: 8192, maxContextMessages: 80 }
};
const OPENAI_MODELS_FREE = ['gpt-4o-mini', 'gpt-5-mini'];
const OPENAI_MODELS_PAID = ['gpt-5.4', 'gpt-5.2-chat-latest', 'gpt-4o', 'gpt-4.1', 'gpt-4o-mini'];
const DEEPSEEK_MODELS    = ['deepseek-chat', 'deepseek-reasoner'];
const GOOGLE_MODELS_FREE = ['gemini-2.5-flash'];
const GOOGLE_MODELS_PAID = ['gemini-2.5-flash', 'gemini-2.5-pro', 'gemini-1.5-pro', 'gemini-2.0-flash'];
const HF_MODELS_FREE     = ['Qwen/Qwen2.5-72B-Instruct', 'mistralai/Mistral-7B-Instruct-v0.3', 'microsoft/Phi-3.5-mini-instruct'];
const HF_MODELS_PAID     = ['meta-llama/Meta-Llama-3.1-70B-Instruct', 'meta-llama/Meta-Llama-3.1-405B-Instruct', 'Qwen/Qwen2.5-72B-Instruct', 'mistralai/Mixtral-8x7B-Instruct-v0.1'];
const GROQ_MODELS_FREE   = ['llama-3.3-70b-versatile', 'llama-3.1-8b-instant', 'meta-llama/llama-4-scout-17b-16e-instruct', 'qwen/qwen3-32b'];
const GROQ_MODELS_PAID   = ['llama-3.3-70b-versatile', 'llama-3.1-8b-instant', 'meta-llama/llama-4-scout-17b-16e-instruct', 'qwen/qwen3-32b', 'moonshotai/kimi-k2-instruct-0905'];
// Modelle mit nativem Audio-Input-Support (Mikrofon-Aufnahme-Button)
const AUDIO_CAPABLE_MODELS = ['gemini-2.5-flash','gemini-2.5-pro','gemini-1.5-pro','gemini-2.0-flash','gpt-4o','gpt-4.1'];
```

**API-Key-Konfiguration** (`/etc/apache2/envvars`):
```bash
export OPENAI_API_KEY="sk-proj-..."
export DEEPSEEK_API_KEY="sk-..."
export GOOGLE_API_KEY="AIza..."
export HF_API_KEY="hf_..."
export GRQ_API_KEY="gsk_..."
```

**Sprachkonfiguration** (`language.xml`):
- Einen neuen `<language id="custom" name="..." visible="true">`-Block hinzufügen, um den benutzerdefinierten Sprachslot zu aktivieren.
- `has_address_form="true"` für Sprachen mit formell/informell-Unterscheidung setzen.

### Deploy-Skripte

| Skript | Funktion |
|--------|----------|
| `deploy.sh <user>` | Kopiert Dateien von `/home/<user>/multi-llm-chat/var/www/deepseek-chat/` nach `/var/www/deepseek-chat/`, setzt Berechtigungen, lädt Apache neu |
| `sync-back.sh <user>` | Kopiert geänderte Dateien aus der Produktion zurück ins Quell-Repo |
| `install.sh` | Installiert `deploy.sh` und `sync-back.sh` im Produktionsverzeichnis |
| `tag-release.sh` | Erstellt einen neuen Git-Tag mit automatisch inkrementierter Versionsnummer (z.B. v0.93 → v0.94) und pusht ihn. Führt automatisch `git fetch --tags` aus, um Konflikte mit bereits vorhandenen Remote-Tags zu vermeiden. |

---

## Projektstruktur

```
/
├── etc/apache2/sites-available/
│   ├── deepseek-chat.conf              (deaktiviert — nur HTTP, leitet zu HTTPS weiter)
│   └── deepseek-chat-ssl.conf          (aktiv — SSL, CGI, API-Key via envvars)
├── shell-scripts/
│   ├── repo2text.sh                    Gesamtes Repo als einzelne Textdatei exportieren
│   ├── deploy.sh                       Kopiert Quell-Repo → Produktion
│   ├── sync-back.sh                    Kopiert Produktion → Quell-Repo
│   ├── install.sh                      Installiert deploy/sync-back-Skripte
│   └── tag-release.sh                  Erstellt und pusht Git-Versions-Tags
├── var/www/deepseek-chat/
│   ├── index.html                      Hauptanwendung (gesamtes JS/CSS/HTML)
│   ├── language.xml                    Alle UI-Texte in allen Sprachen (EN, DE, ES, Custom)
│   ├── manifest                        Design-Manifest (alle Konventionen)
│   ├── changelog                       Vollständige Entwicklungshistorie
│   ├── files-directorys                Dateiübersicht / Verzeichnisliste
│   ├── cgi-bin/
│   │   ├── openai-api.py              Streaming-Proxy zur OpenAI API
│   │   ├── deepseek-api.py            Streaming-Proxy zur DeepSeek API
│   │   ├── google-api.py              Streaming-Proxy zur Google Gemini API
│   │   ├── hugging-api.py             Streaming-Proxy zur Hugging Face Inference API
│   │   ├── groq-api.py                Streaming-Proxy zur GroqCloud API (LPU-beschleunigt)
│   │   ├── compress-context.py        Kontext-Komprimierung via zweitem LLM-Aufruf
│   │   ├── deepseek-models.py         Fragt /v1/models-Endpunkt ab
│   │   ├── save-session.py            Speichert Chat-Sessions (POST)
│   │   ├── load-session.py            Lädt Session-Liste (GET) oder Session (GET ?id=)
│   │   ├── delete-session.py          Löscht Session (DELETE)
│   │   ├── export-pdf.py              PDF-Export mit ReportLab
│   │   ├── export-markdown.py         Markdown-Export
│   │   ├── export-txt.py              TXT-Export
│   │   ├── export-rtf.py              RTF-Export (keine externe Bibliothek)
│   │   ├── feedback-log.py            Like/Dislike-Logging
│   │   └── get-log.py                 Liest und gibt Log-Datei zurück
│   ├── logs/                          Server-Log-Dateien (automatisch erstellt)
│   ├── kompressor/                    Komprimierungs-Ergebnisdateien (automatisch erstellt)
│   └── sessions/                      Chat-Session-JSON-Dateien (automatisch erstellt)
```

---

## Modell-Konfiguration

Das `MODEL_CONFIG`-Objekt in `index.html` ist die einzige Wahrheitsquelle für alle modellspezifischen Limits. Es deckt alle fünf Anbieter ab (vollständiges Objekt siehe Abschnitt Konfiguration).

Quellen: [OpenAI API Docs](https://platform.openai.com/docs), [DeepSeek API Docs](https://api-docs.deepseek.com), [Google Gemini Docs](https://ai.google.dev/gemini-api/docs), [Hugging Face Inference Providers](https://huggingface.co/docs/inference-providers), [GroqCloud Docs](https://console.groq.com/docs/models) (Stand 19.03.2026).

---

## Design-Manifest

Das Projekt enthält eine **`manifest`-Datei**, die alle Design-Entscheidungen und Konventionen dokumentiert. Jede Änderung am Projekt wird dort dokumentiert. Wichtige Regeln:

- **Alle Buttons**: Nur Pill-Style (border-radius: 20px, height: 36px) — eckige Buttons sind verboten.
- **Button-Farben**: Blau (`#0056b3`) für Aktionen, Dunkel/Blau-Toggle für Modi, Rot (`#dc3545`) für destruktive, Grün (`#28a745`) für konstruktive.
- **Einstellungen**: Nur Toggle-Schalter — keine Radio-Buttons, keine Checkboxen.
- **Keine Emojis** in Buttons oder Labels (Ausnahme: das DeepThink-Icon ✦).
- **Kein PHP** — ausschliesslich JavaScript und Python.
- **Keine externen JS-Frameworks** — kein Node, kein React, kein Vue.
- **Formatierungs-Beibehaltung**: Bestehende Einrückung und Formatierung in `index.html` darf niemals geändert werden.
- **`AUDIO_CAPABLE_MODELS` nachführen**: Sobald ein Modell Audio-Unterstützung erhält oder verliert, muss die Konstante sofort aktualisiert werden (Manifest-Regel E.1).
- **Guthaben/Tageslimit-Banner implementieren**: Beim Hinzufügen eines neuen LLM-Anbieters muss der entsprechende Banner (rot für bezahlt, blau für kostenlos) im CGI-Skript und Client implementiert werden (Manifest-Regel E.1).
- Das Manifest ist eine **separate Datei** und darf nie in `index.html` eingebettet werden.

---

## Bekannte Einschränkungen & technische Hinweise

### „Lost in the Middle" — Eine bekannte KI-Einschränkung
Alle aktuellen Sprachmodelle neigen dazu, Inhalte am **Anfang und Ende** eines langen Kontexts zuverlässig zu erinnern, aber Inhalte **in der Mitte** werden manchmal übersehen oder halluziniert. (Liu et al., 2023: „Lost in the Middle: How Language Models Use Long Contexts")

**Praktische Auswirkung auf dieses Projekt**:
- Ein Repository-Export von ~686.000 Zeichen ≈ ~171.500 Token.
- DeepSeek-Kontextfenster: 100.000 Token → der vollständige Repository-Export **überschreitet** das DeepSeek-Kontextfenster und kann nicht als einzelne Datei geladen werden. Der Client blockiert den Upload mit einer klaren Fehlermeldung.
- Google Gemini (1–2 Mio. Token Kontext) kann den vollständigen Export problemlos verarbeiten.
- **Empfehlung**: Bei der Arbeit mit DeepSeek oder anderen Modellen mit kleinerem Kontextfenster nur die relevanten Einzeldateien hochladen statt des gesamten Repository-Exports.

### GitHub Raw URL Caching
Nach einem `git push` ist die neue Version **nicht sofort** via `raw.githubusercontent.com`-URLs verfügbar — GitHub cached diese bis zu 10 Minuten. Das ist normal und kann nicht umgangen werden. Die Dateien sind korrekt auf GitHub gespeichert, sobald `git push` erfolgreich ist.

### Nano und Unicode — Kritische Warnung
**Niemals** Dateien mit Unicode-Escape-Sequenzen (wie die Umlaut-Funktionen) mit `nano` oder durch Kopieren in ein Terminal bearbeiten. Nano korrumpiert `\u00e4` zu `M-CM-$`, was für JavaScript binärer Müll ist.

**Der einzig sichere Arbeitsablauf**:
1. Dateien lokal bearbeiten (VS Code, gedit, kate oder ein geeigneter Editor).
2. `git add` / `git commit` / `git push` von der lokalen Maschine.
3. Auf dem Server: `git pull` (im Quell-Repo als Benutzer `source`).
4. Als root: `./deploy.sh source`.

### Linux/X11/Firefox Einfüge-Verhalten
Unter Linux mit X11 und Firefox blockiert `e.preventDefault()` in Paste-Event-Handlern nicht zuverlässig das browsernative Einfügeverhalten für Inhalte aus Dateimanagern. Die hier implementierte Lösung (Einfügen erlauben, Inhalt in `setTimeout(0)` prüfen, leeren wenn Dateipfade erkannt) ist der zuverlässige Workaround für diese plattformspezifische Einschränkung.

### Erkennung der Kontextfenster-Überschreitung
Die Erkennung des Kontext-Überlaufs in allen fünf CGI-Skripten verwendet HTTP-Statuscode-Analyse kombiniert mit Schlüsselwortabgleich im API-Antwort-Body. Obwohl die Schlüsselwörter breit genug sind um die meisten API-Antworten abzufangen, können Ausnahmefälle mit ungewöhnlichen Fehlermeldungen durch Änderungen in der Anbieter-Infrastruktur nicht sofort erkannt werden und würden auf eine generische Fehlermeldung zurückfallen.

---

## Abhängigkeiten

| Komponente | Zweck | Installation |
|------------|-------|-------------|
| Apache2 | Webserver, CGI-Unterstützung | `apt install apache2` |
| Python 3 | Serverseitige CGI-Skripte | `apt install python3` |
| reportlab | PDF-Export | `pip3 install reportlab` |
| pdf.js 3.11.174 | Clientseitige PDF-Extraktion | Via CDN geladen (automatischer Fallback) |
| jq | JSON-Verarbeitung in `repo2text.sh` | `apt install jq` |
| pv | Fortschrittsanzeige in `repo2text.sh` | `apt install pv` |
| git | Versionsverwaltung | `apt install git` |
| zip | Archiv-Erstellung in `repo2text.sh` | `apt install zip` |

**Keine exotischen Frameworks** — alle Abhängigkeiten sind Standardpakete in einer Debian-Umgebung oder werden von etablierten CDNs geladen.

---

## Fazit / Warum dieses Projekt heraussticht

Dieses Projekt demonstriert professionelle Webentwicklung in einem minimalistischen, sicherheitsorientierten Ansatz:

**Architektur**:
- Saubere Trennung von Client (reines HTML/JS) und Server (Python CGI) ohne Vermischung der Verantwortlichkeiten.
- API-Key nie exponiert — selbst ein vollständiger XSS-Kompromiss kann ihn nicht leaken.
- Single-File-Client (`index.html`), vollständig eigenständig und intern hochmodular.

**Benutzererfahrung**:
- Streaming-Antworten mit Sub-Sekunden-Ersttoken-Latenz.
- Einzigartiges flexibles Kontextmanagement (beliebige Nachricht + alle nachfolgenden löschen).
- Intelligentes Zwischenablage-Handling für Text, Bilder und Dateipfad-Schutz.
- **Audio-Aufnahme** direkt im Browser — Mikrofon-Input für Google Gemini (alle Modelle) und OpenAI gpt-4o / gpt-4.1.
- **Kompressor** — automatische Kontext-Komprimierung ermöglicht unbegrenzt lange Gespräche, unabhängig von der Grösse des Kontextfensters.
- **Kontextfenster-Überschreitung** — interaktive Box im Chat mit intelligentem Kontext-Übernahme über Sessions hinweg (Option C).
- **Guthaben/Tageslimit-Banner** — klare, dauerhafte visuelle Rückmeldung bei erschöpftem Guthaben oder Tageslimit.
- **In Zwischenablage kopieren** — gesamter Chat mit einem Klick direkt in die Systemzwischenablage exportiert.
- Mehrsprachige Unterstützung mit Anredeformunterscheidung, aus externem XML geladen.

**Engineering**:
- Magic-Byte-Prüfung, die Malware unabhängig von der Dateinamenserweiterung erkennt.
- Umlaut-Platzhalter-System löst eine grundlegende DeepSeek API-Einschränkung.
- Vorwärtskompatible Modell-Fähigkeits-Map, bereit für bildunterstützende Modelle.
- Präzises Verwerfen der Kompressor-Zusammenfassung: Zusammenfassung wird ungültig wenn Kontext nach manuellem Löschen unter den zuletzt ausgelösten Schwellwert fällt.
- Vollständige Audit-Trail via Git und detailliertem Changelog.

**Tooling**:
- `repo2text.sh` als praktisches Tool für KI-gestützte Entwicklung, mit eindeutigem Begrenzer und Deduplizierung via `sort -z -u`.
- Deployment-Skripte für konsistente, berechtigungskorrekte Deployments.
- Versions-Tagging für sauberes Release-Management, mit automatischer Remote-Tag-Synchronisierung.

**Für einen professionellen Entwickler** demonstriert dieses Projekt:
- **Sicherheitsbewusstsein** — API-Key-Schutz, Malware-Erkennung, sichere Session-Speicherung.
- **Strukturierte Disziplin** — Manifest, Versions-Tags, strikte Design-Konventionen, dokumentierter Changelog.
- **Problemlösungstiefe** — X11-Einfügeverhalten, Umlaut-Korruption, PDF-Binärausgabe, „Lost in the Middle", Kontext-Überlauf-Behandlung.
- **Vollständige Dokumentation** — sowohl inline als auch in dedizierten Dateien.

Multi-LLM Chat Client ist ein **Showcase für professionelle Webentwicklung** — ohne unnötigen Overhead, aber mit höchsten Ansprüchen an Sicherheit, Korrektheit und Benutzerfreundlichkeit.

---

*Zuletzt aktualisiert: 19.03.2026*
