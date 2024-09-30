# PROJEKT_OFFSHORE_WINDFARM

## Übersicht
Dieses Projekt verarbeitet Sensordaten von Kabeltemperaturen aus einem Offshore-Windpark. Die Daten werden als CSV-Dateien bereitgestellt und automatisch bereinigt, gefiltert sowie in eine PostgreSQL-Datenbank geladen. Alle 60 Sekunden prüft das Skript auf neue Daten.


# Dateien

## data/windpark_data.csv

Beinhaltet Timestamp und Temperaturwerte.

## scripts/process_data.py

Python-Skript mit Apache Spark zur:
- Bereinigung der Daten (Entfernung ungültiger Werte außerhalb von -50°C bis 150°C und Nullwerte).
- Berechnung stündlicher Durchschnittstemperaturen.
- Speicherung der Daten in die PostgreSQL-Datenbank.
- Überwacht alle 60 Sekunden das `data`-Verzeichnis auf neue CSV-Dateien.

## .env

Enthält die Zugangsdaten für die PostgreSQL-Datenbank:

```bash
POSTGRES_USER=benutzername
POSTGRES_PASSWORD=passwort
POSTGRES_DB=windfarm_db
```

## docker-compose.yml

Docker-Konfiguration zum Starten der PostgreSQL- und Spark-Container.

# Funktionsweise

## Automatisierte Datenverarbeitung:

- Das Skript überwacht das `data`-Verzeichnis und verarbeitet neue CSV-Dateien.
- Bereinigte Rohdaten werden in die Tabelle `temperature_data` gespeichert.
- Stündliche Durchschnittswerte werden in `hourly_average_temperatures` abgelegt.
- Verarbeitete Dateien werden gelöscht, um Duplikate zu vermeiden.

## Wichtiger Hinweis zu CSV-Dateien:

Jede neue CSV-Datei muss einen eindeutigen Namen haben, um mehrfache Verarbeitungen zu verhindern.

# Datenbankstruktur

**Datenbank:** `windfarm_db` (muss manuell erstellt werden).

## Tabellen (manuell zu erstellen):

- `temperature_data`: Speichert die bereinigten Rohdaten.
- `hourly_average_temperatures`: Enthält die stündlich aggregierten Durchschnittstemperaturen.


# Manuelle Erstellung der PostgreSQL-Datenbank und Tabellen

1. **Container starten:**

   ```powershell
   docker-compose up -d
   ```

## 2. In den PostgreSQL-Container einloggen:

Verbinde dich mit der Standarddatenbank `postgres`, um die neue Datenbank zu erstellen:

```bash
docker exec -it <postgres_container_name> psql -U <postgres_user> -d postgres
```

## 3. Datenbank erstellen:

Nachdem du dich eingeloggt hast, erstelle die Datenbank `windfarm_db`:

```sql
CREATE DATABASE windfarm_db;
```

## 4. Tabellen in PostgreSQL erstellen

Nachdem die Datenbank `windfarm_db` erstellt wurde, kannst du die Tabellen anlegen.

### Tabellen erstellen:

**Für die Rohdaten (`temperature_data`):**

```sql
CREATE TABLE temperature_data (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    temperature NUMERIC NOT NULL
);
```

**Für die stündlichen Durchschnittswerte (`hourly_average_temperatures`):**

```sql
CREATE TABLE hourly_average_temperatures (
    id SERIAL PRIMARY KEY,
    hour TIMESTAMP NOT NULL,
    avg_temperature NUMERIC NOT NULL
);
```

## 5. Tabelleninhalt anzeigen:

Um die Daten in den Tabellen anzuzeigen, kannst du die folgenden Befehle verwenden:

```sql
SELECT * FROM temperature_data;
```

```sql
SELECT * FROM hourly_average_temperatures;
```

# Docker

## PostgreSQL-Container:
Hält die Datenbank für die Temperaturdaten bereit.

## Spark-Container:
Führt das Skript `process_data.py` zur Datenverarbeitung aus.

## Abhängigkeiten:
Der Spark-Container startet erst, wenn der PostgreSQL-Container läuft.

# Voraussetzungen

- Installation von Docker und Docker Compose.
- Manuelle Erstellung der PostgreSQL-Datenbank `windfarm_db` sowie der Tabellen `temperature_data` und `hourly_average_temperatures`.

# Datenverarbeitung starten

- Lege die CSV-Dateien im `data`-Verzeichnis ab.
- Das Skript `process_data.py` prüft alle 60 Sekunden auf neue Dateien.
- Nach erfolgreicher Verarbeitung wird die Datei gelöscht.
- Die Daten werden in die PostgreSQL-Datenbank geladen.




