# Projektübersicht
In einem Offshore-Windpark werden verschiedene Betriebsparameter überwacht, darunter die Temperaturen von Kabeln. Dieses Projekt konzentriert sich darauf, die bereitgestellten CSV-Dateien zu verarbeiten und diese Temperaturdaten in einer PostgreSQL-Datenbank zu speichern. Das Skript liest die Daten, bereinigt sie und berechnet stündliche Durchschnittswerte, die dann in der Datenbank gespeichert werden.

Das Skript läuft kontinuierlich und überwacht ein Verzeichnis auf neue CSV-Dateien, die in regelmäßigen Abständen von 60 Sekunden verarbeitet werden.

# Funktionen

- **Automatisierte CSV-Dateiverarbeitung**: Neue Dateien werden alle 60 Sekunden erkannt und verarbeitet.
- **Datenbereinigung**: Ungültige Daten (Temperaturen außerhalb des Bereichs von -50°C bis 150°C) werden gefiltert.
- **Stündliche Durchschnittswerte**: Es werden Durchschnittstemperaturen pro Stunde berechnet.
- **Datenbankspeicherung**: Die bereinigten und aggregierten Daten werden in PostgreSQL gespeichert.
- **Automatische Tabellenerstellung**: Falls die erforderlichen Tabellen nicht existieren, erstellt das Skript diese automatisch.
- **Shell-Umgebung**: Das Skript ist für die Ausführung in der PowerShell oder einer anderen Shell-Umgebung ausgelegt.

# Verwendete Technologien

- **Docker**: Zur Containerisierung von PostgreSQL und Spark.
- **Apache Spark**: Zur effizienten Verarbeitung großer Datenmengen.
- **PostgreSQL**: Die relationale Datenbank, in der die Sensordaten gespeichert werden.
- **Python**: Zur Implementierung des Datenverarbeitungs-Skripts.
- **Psycopg2**: Eine Python-Bibliothek zur Verbindung mit PostgreSQL.
- **PySpark**: Die Python-Schnittstelle für Apache Spark.

# Einrichtungsanleitung

## 1. Repository klonen

Klone dieses Repository auf deine lokale Maschine:

```
git clone https://github.com/marvin2911/Projekt_Offshore_Windfarm.git
cd Projekt_Offshore_Windfarm
```

## 2. Anpassen der Umgebungsvariablen (falls notwendig)

Die Datei `.env`, die die PostgreSQL-Zugangsdaten enthält, ist bereits im Projekt enthalten. Falls du die Datenbankzugangsdaten ändern musst, kannst du die Datei entsprechend anpassen:

```
POSTGRES_USER=benutzername
POSTGRES_PASSWORD=passwort
POSTGRES_DB=windfarm_db
```

## 3. Docker Compose starten

Stelle sicher, dass Docker auf deinem System installiert ist, und starte die Dienste mit Docker Compose:

```
docker-compose up -d
```

Dies startet:

- Eine **PostgreSQL-Datenbank** auf Port 5432.
- Eine **Spark-Instanz**, die automatisch das Datenverarbeitungs-Skript ausführt.

## 4. CSV-Dateien hinzufügen

Ein Beispiel für eine CSV-Datei befindet sich bereits im Ordner `/data`. Du kannst weitere CSV-Dateien in dieses Verzeichnis legen, und das Skript wird sie alle 60 Sekunden erkennen und verarbeiten.

Beispielverzeichnis für CSV-Dateien:

```
./data/
```
Das Skript prüft regelmäßig auf neue Dateien und verarbeitet sie automatisch.

Hinweis: Achte darauf, dass die CSV-Dateien im Verzeichnis /data unterschiedliche Namen haben, um sicherzustellen, dass sie korrekt verarbeitet werden und keine Datei doppelt verarbeitet wird.

# Funktionsweise

- **Dateierkennung**: Das Skript läuft in einer Endlosschleife und überwacht das Verzeichnis `/data` auf neue CSV-Dateien.
- **Datenverarbeitung**: Sobald eine neue Datei erkannt wird, liest das Skript die Daten in einen Spark-DataFrame ein.
- **Datenbereinigung**: Datensätze mit fehlenden oder ungültigen Werten werden entfernt. Nur Temperaturen im Bereich von -50°C bis 150°C bleiben bestehen.
- **Datenaggregation**: Durchschnittstemperaturen werden stündlich berechnet.
- **Datenbankspeicherung**: Die bereinigten und aggregierten Daten werden in der PostgreSQL-Datenbank gespeichert.
- **Automatische Tabellenerstellung**: Falls die benötigten Tabellen nicht existieren, werden sie vom Skript automatisch in der Datenbank angelegt.

## Verwendung

- **Skript ausführen**: Das Skript wird automatisch ausgeführt, sobald Docker Compose gestartet wurde. Es überwacht das Verzeichnis `/data` auf neue Dateien und verarbeitet diese.
  
- **Dienste stoppen**: Um die Dienste zu stoppen, nutze den Befehl:

```
docker-compose down
```

## Datenbankschema

### Tabelle: `temperature_data`

Speichert die rohen Temperaturmessungen.

| Spalte      | Typ        | Beschreibung                          |
|-------------|------------|----------------------------------------|
| `id`        | SERIAL     | Primärschlüssel                        |
| `timestamp` | TIMESTAMP  | Zeitpunkt der Temperaturmessung        |
| `temperature` | FLOAT    | Temperaturmessung in Grad Celsius      |

### Tabelle: `hourly_average_temperatures`

Speichert die stündlich aggregierten Durchschnittstemperaturen.

| Spalte            | Typ        | Beschreibung                                 |
|-------------------|------------|---------------------------------------------|
| `id`              | SERIAL     | Primärschlüssel                             |
| `hour`            | INT        | Stunde des Tages (0-23)                     |
| `avg_temperature` | FLOAT      | Durchschnittstemperatur für die Stunde      |



