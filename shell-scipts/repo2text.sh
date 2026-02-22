#!/bin/bash

# === Konfiguration ===
OUTPUT_FILE_PREFIX="repo_export"

# === Funktion: Zeige Hilfe an ===
show_help() {
    echo "Verwendung: $0 [GitHub-Repository-URL]"
    echo ""
    echo "Beschreibung:"
    echo "  Klont ein GitHub-Repository, extrahiert den Text aller Textdateien"
    echo "  und schreibt sie mit deutlichen Trennern in eine einzige Textdatei."
    echo "  Das Repository wird nach der Extraktion automatisch gelöscht."
    echo ""
    echo "Argumente:"
    echo "  [GitHub-Repository-URL]  Optional: Die HTTPS- oder SSH-URL des Repos."
    echo "                            Wenn keine URL angegeben wird, erfolgt eine interaktive Eingabe."
    echo ""
    echo "Beispiele:"
    echo "  $0 https://github.com/kubernetes/kubernetes.git"
    echo "  $0   # dann URL eingeben"
}

# === Hauptprogramm ===

# Prüfen, ob eine URL als Argument übergeben wurde
if [ $# -ge 1 ]; then
    REPO_URL="$1"
else
    # Interaktiv nach der URL fragen
    read -p "Bitte gib die GitHub-Repository-URL ein: " REPO_URL
    if [ -z "$REPO_URL" ]; then
        echo "Fehler: Keine URL eingegeben."
        show_help
        exit 1
    fi
fi

# Prüfen, ob git installiert ist
if ! command -v git &> /dev/null; then
    echo "Fehler: 'git' ist nicht installiert. Bitte installiere es mit:"
    echo "  sudo apt update && sudo apt install git -y"
    exit 1
fi

# Repository-Namen aus der URL extrahieren
REPO_NAME=$(basename "$REPO_URL" .git)

# Temporäres Verzeichnis zum Klonen erstellen
TEMP_DIR=$(mktemp -d -t "${REPO_NAME}-XXXXX")

if [ ! -d "$TEMP_DIR" ]; then
    echo "Fehler: Konnte kein temporäres Verzeichnis erstellen."
    exit 1
fi

echo "=== Klone Repository '$REPO_URL' nach '$TEMP_DIR' ==="

# Repository klonen (nur Standard-Branch, ohne Historie)
if ! git clone --depth 1 "$REPO_URL" "$TEMP_DIR"; then
    echo "Fehler beim Klonen des Repositories. Löschen des Temp-Verzeichnisses."
    rm -rf "$TEMP_DIR"
    exit 1
fi

echo "=== Klonen erfolgreich. Extrahiere Textdateien... ==="

# Ausgabedateinamen bestimmen
OUTPUT_FILE="${OUTPUT_FILE_PREFIX}_${REPO_NAME}.txt"

# Temporäre Datei für den Inhalt (ohne Header)
CONTENT_FILE="${OUTPUT_FILE}.content"
> "$CONTENT_FILE"

file_count=0

# Rekursive Suche nach allen Dateien im geklonten Repo (außer .git)
while IFS= read -r -d '' file; do
    # Prüfen, ob die Datei eine Textdatei ist
    mime_type=$(file -b --mime-type "$file")

    if [[ "$mime_type" == text/* ]]; then
        relative_path="${file#$TEMP_DIR/}"

        {
            echo "========================================================================="
            echo "Datei: $relative_path"
            echo "========================================================================="
            cat "$file"
            echo
            echo
        } >> "$CONTENT_FILE"

        ((file_count++))
        echo "  + Hinzugefügt: $relative_path"
    else
        echo "  - Überspringe (keine Textdatei): ${file#$TEMP_DIR/}"
    fi
done < <(find "$TEMP_DIR" -type f -not -path "$TEMP_DIR/.git/*" -print0)

echo "=== Aufräumen: Lösche temporäres Repository ==="
rm -rf "$TEMP_DIR"

# Jetzt Header mit Metadaten erstellen und mit Inhalt kombinieren
{
    echo "========================================================================="
    echo "Repository Export"
    echo "========================================================================="
    echo "Export-Datum: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "Repository-URL: $REPO_URL"
    echo "Anzahl extrahierter Textdateien: $file_count"
    echo "========================================================================="
    echo
    cat "$CONTENT_FILE"
} > "$OUTPUT_FILE"

# Temporäre Inhaltsdatei löschen
rm -f "$CONTENT_FILE"

echo "==============================================="
echo "Fertig! Es wurden $file_count Textdateien extrahiert."
echo "Die Ausgabedatei wurde erstellt: $(pwd)/$OUTPUT_FILE"
echo "==============================================="

