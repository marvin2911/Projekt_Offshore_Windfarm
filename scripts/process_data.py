import os
import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, hour, avg

# PostgreSQL-Verbindungsdetails
postgres_user = os.getenv('POSTGRES_USER')
postgres_password = os.getenv('POSTGRES_PASSWORD')
postgres_db = os.getenv('POSTGRES_DB')
postgres_url = f"jdbc:postgresql://db:5432/{postgres_db}"

# SparkSession erstellen
spark = SparkSession.builder \
    .appName("WindfarmDataProcessing") \
    .config("spark.jars.packages", "org.postgresql:postgresql:42.2.18") \
    .getOrCreate()

# Pfad zum Datenordner
data_path = "/data"

# Set zum Speichern bereits verarbeiteter Dateien
processed_files = set()

while True:
    # Liste aller CSV-Dateien im Datenordner
    files = [f for f in os.listdir(data_path) if f.endswith(".csv")]

    for file in files:
        if file not in processed_files:
            file_path = os.path.join(data_path, file)
            try:
                # Daten laden
                df = spark.read.csv(file_path, header=True, inferSchema=True)
                # Datenvorverarbeitung
                df_clean = df.dropna()
                df_filtered = df_clean.filter((col("temperature") >= -50) & (col("temperature") <= 150))
                # Daten in PostgreSQL laden
                df_filtered.write \
                    .format("jdbc") \
                    .option("url", postgres_url) \
                    .option("dbtable", "temperature_data") \
                    .option("user", postgres_user) \
                    .option("password", postgres_password) \
                    .option("driver", "org.postgresql.Driver") \
                    .mode("append") \
                    .save()
                # Stündliche Durchschnittstemperaturen berechnen
                df_agg = df_filtered.withColumn("hour", hour(col("timestamp"))) \
                    .groupBy("hour") \
                    .agg(avg("temperature").alias("avg_temperature"))
                # Aggregierte Daten in PostgreSQL speichern
                df_agg.write \
                    .format("jdbc") \
                    .option("url", postgres_url) \
                    .option("dbtable", "hourly_average_temperatures") \
                    .option("user", postgres_user) \
                    .option("password", postgres_password) \
                    .option("driver", "org.postgresql.Driver") \
                    .mode("append") \
                    .save()
                # Datei als verarbeitet markieren
                processed_files.add(file)
                # Optional: Verarbeitete Datei löschen
                os.remove(file_path)
                print(f"Datei {file} wurde erfolgreich verarbeitet.")
            except Exception as e:
                print(f"Fehler beim Verarbeiten der Datei {file}: {e}")
    # Wartezeit vor dem nächsten Scan (z.B. 60 Sekunden)
    time.sleep(60)

# SparkSession beenden (wird eigentlich nie erreicht wegen der Endlosschleife)
spark.stop()
