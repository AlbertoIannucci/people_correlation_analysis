from extract_transform import modello
import pymysql

# Funzione per ottenere la stringa di connessione
def _getconnection():
    return pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="",
        database="people"
    )

# Funzione per il caricamento dei dati nel db (per tabelle di decodifica)
def load_decodifica(df):
    with _getconnection() as connection:
        with connection.cursor() as cursor:
            workclass_uniche = df["workclass"].unique()
            valori_workclass = [(row,) for row in workclass_uniche]

            education_uniche = df["education"].unique()
            valori_education = [(row,) for row in education_uniche]

            marital_status_uniche = df["marital_status"].unique()
            valori_marital_status = [(row,) for row in marital_status_uniche]

            occupation_uniche = df["occupation"].unique()
            valori_occupation = [(row,) for row in occupation_uniche]

            relationship_uniche = df["relationship"].unique()
            valori_relationship = [(row,) for row in relationship_uniche]

            race_uniche = df["race"].unique()
            valori_race = [(row,) for row in race_uniche]

            # Caricamento dati nelle diverse tabelle
            cursor.executemany("INSERT INTO workclass(name) VALUES (%s)", valori_workclass)
            cursor.executemany("INSERT INTO education(name) VALUES (%s)", valori_education)
            cursor.executemany("INSERT INTO marital_status(name) VALUES (%s)", valori_marital_status)
            cursor.executemany("INSERT INTO occupation(name) VALUES (%s)", valori_occupation)
            cursor.executemany("INSERT INTO relationship(name) VALUES (%s)", valori_relationship)
            cursor.executemany("INSERT INTO race(name) VALUES (%s)", valori_race)

            connection.commit()
            print("Dati caricati con successo")

# Funzione per il caricamento dei dati nella main table
def load(df):
    with _getconnection() as connection:
        with connection.cursor() as cursor:
            sql = ("INSERT INTO person(age, fk_id_workclass, fk_id_education, fk_id_marital_status, fk_id_occupation, "
                   "fk_id_relationship, fk_id_race, sex, capital_gain, capital_loss, hours_per_week, native_country, target) "
                   "VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")

            valori = [(
                row["age"],
                row["workclass_code"],
                row["education_code"],
                row["marital_status_code"],
                row["occupation_code"],
                row["relationship_code"],
                row["race_code"],
                row["sex"],
                row["capital_gain"],
                row["capital_loss"],
                row["hours_per_week"],
                row["native_country"],
                row["target"]
            ) for _, row in df.iterrows()]

            cursor.executemany(sql, valori)
            connection.commit()
            print("Dati caricati con successo")

#load_decodifica(modello.dataframe_sistemato)
#load(modello.dataframe_sistemato)