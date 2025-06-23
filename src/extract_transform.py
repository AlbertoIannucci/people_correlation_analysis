from modello_base import ModelloBase
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency, spearmanr, contingency
import numpy as np

class DatasetCleaner(ModelloBase):

    # Metodo di inizializzazione
    def __init__(self, dataset_path):
        self.dataframe = pd.read_csv(dataset_path)
        self.dataframe_sistemato = self.sistemazione()

    # Metodo di sistemazione del dataset
    def sistemazione(self):
        # Copia del dataframe
        df_sistemato = self.dataframe.copy()

        # Conversione ? con nan
        df_sistemato = df_sistemato.replace("?", np.nan)

        # Drop variabili fnlwgt e education-num
        varibaili_da_droppare = ["fnlwgt", "education-num"]
        df_sistemato = df_sistemato.drop(varibaili_da_droppare, axis=1)

        # 6.1 Drop valori nan
        # df_sistemato = df_sistemato.dropna()

        # 6.2 Sostituzione valori nan
        variabili_da_sistemare = ["workclass", "occupation", "native-country"]
        for col in variabili_da_sistemare:
            df_sistemato[col] = df_sistemato.groupby("education")[col].transform(
                lambda x: x.fillna(x.mode()[0])
            )

        df_sistemato = df_sistemato.rename(columns={
            "marital-status":"marital_status",
            "capital-gain":"capital_gain",
            "capital-loss":"capital_loss",
            "hours-per-week":"hours_per_week",
            "native-country":"native_country"
        })

        # Inserimento colonne di codifica
        mappa_workclass = dict(zip(df_sistemato["workclass"].unique(), range(1, df_sistemato["workclass"].nunique() + 1)))
        df_sistemato["workclass_code"] = df_sistemato["workclass"].replace(mappa_workclass)

        mappa_education = dict(zip(df_sistemato["education"].unique(), range(1, df_sistemato["education"].nunique() + 1)))
        df_sistemato["education_code"] = df_sistemato["education"].replace(mappa_education)

        mappa_marital_status = dict(zip(df_sistemato["marital_status"].unique(), range(1, df_sistemato["marital_status"].nunique() + 1)))
        df_sistemato["marital_status_code"] = df_sistemato["marital_status"].replace(mappa_marital_status)

        mappa_occupation = dict(zip(df_sistemato["occupation"].unique(), range(1, df_sistemato["occupation"].nunique() + 1)))
        df_sistemato["occupation_code"] = df_sistemato["occupation"].replace(mappa_occupation)

        mappa_relationship = dict(zip(df_sistemato["relationship"].unique(), range(1, df_sistemato["relationship"].nunique() + 1)))
        df_sistemato["relationship_code"] = df_sistemato["relationship"].replace(mappa_relationship)

        mappa_race = dict(zip(df_sistemato["race"].unique(), range(1, df_sistemato["race"].nunique() + 1)))
        df_sistemato["race_code"] = df_sistemato["race"].replace(mappa_race)

        return df_sistemato

    # Metodo per calcolare la correlazione tra variabili categoriali e target
    def corr_categoriali(self):
        variabili_categoriali = ["workclass", "education", "marital_status", "occupation", "relationship", "race", "sex"]

        risultati_confronto = {
            "variabile":[],
            "p-value":[],
            "cramer":[]
        }

        for col in variabili_categoriali:
            tabella_contingenza = pd.crosstab(self.dataframe_sistemato[col], self.dataframe_sistemato["target"])
            chi_due, p_value, _, _ = chi2_contingency(tabella_contingenza)
            cramer = contingency.association(tabella_contingenza, method="cramer")

            risultati_confronto["variabile"].append(col)
            risultati_confronto["p-value"].append(format(p_value, ".53f"))
            risultati_confronto["cramer"].append(cramer)

        df = pd.DataFrame(risultati_confronto)
        print("********** CONFRONTO CORRELAZIONI CATEGORIALI **********", df.to_string(), sep="\n")

    # Metodo per calcolare la correlazione tra variabili quantitative e target
    def corr_quantitative(self):
        variabili_quantitative = ["age", "capital_gain", "capital_loss", "hours_per_week"]

        risultati_confronto = {
            "variabile":[],
            "p-value":[],
            "spearman":[]
        }

        for col in variabili_quantitative:
            spearman, p_value = spearmanr(self.dataframe_sistemato[col], self.dataframe_sistemato["target"])

            risultati_confronto["variabile"].append(col)
            risultati_confronto["p-value"].append(format(p_value, ".53f"))
            risultati_confronto["spearman"].append(spearman)

        df = pd.DataFrame(risultati_confronto)
        print("********** CONFRONTO CORRELAZIONI QUANTITATIVE **********", df.to_string(), sep="\n")

    # Metodo per la realizzazione di un grafico
    def grafico(self):
        mappatura = {
            "Wife": "Moglie",
            "Own-child": "Figlio/a",
            "Husband": "Marito",
            "Not-in-family": "Nessuna famiglia",
            "Other-relative": "Altra relazione",
            "Unmarried": "Non sposato/a"
        }

        # Rimappatura
        self.dataframe_sistemato['relationship'] = self.dataframe_sistemato['relationship'].map(mappatura)

        # Creazione della tabella di contingenza tra 'relationship' e 'target'
        tabella_contingenza = pd.crosstab(self.dataframe_sistemato['relationship'],
                                          self.dataframe_sistemato['target'])

        # Creiamo un grafico a barre affiancate (side-by-side)
        tabella_contingenza.plot(kind="bar", stacked=False, color=["red", "green"], figsize=(10, 6))

        # Titolo e etichette degli assi
        plt.title("Distribuzione del Reddito per tipo di Relazione Familiare", fontsize=16)
        plt.xlabel("Relazione Familiare", fontsize=12)
        plt.ylabel("Frequenza", fontsize=12)
        plt.legend(title="Reddito", bbox_to_anchor=(1.05, 1), loc='upper left')  # Posizione della legenda
        plt.tick_params(axis="x", rotation=45)  # Ruota le etichette dell'asse x per miglior leggibilità
        plt.tight_layout()  # Migliora il layout per evitare sovrapposizioni

        # Mostriamo il grafico
        plt.show()

# Estrazione
modello = DatasetCleaner("../Dataset/people.csv")
# Trasformazione
# Passo 1. Analisi generali del dataset
# modello.analisi_generali(modello.dataframe)
# Risultati:
# Osservazioni= 32561; Variabili= 15; Tipi= int e object; Valori nan= non sembra
# Passo 2. Analisi valori univoci
# modello.analisi_valori_univoci(modello.dataframe, ["fnlwgt"])
# Valori nan camuffati con '?'
# Passo 3. Rendo visibile i valori nan camuffati
# modello.analisi_generali(modello.dataframe_sistemato)
# Passo 4. Drop variabile fnlwgt -> non utile all'analisi
# Passo 5. Drop variabile education-num -> ridondante con education
# Passo 6. Gestione valori nan
# Passo 6.1 Prova con drop valori nan
# Percentuale dataset perso = [(32561 - 30162) / 32561] * 100 = 7.3%
# La percentuale detaset perso è maggiore del 5% -> evito il drop
# Passo 6.2 Sostituzione valori nan
# Passo 7. Rimappatura etichette snake_case
# Passo 8. Inserisco colonne di codifica per agevolare l’implementazione di tabelle di decodifica all'interno di un database MySQL
# Passo 9. Calcolo correlazioni tra variabili categoriali e target (categoriale)
#modello.corr_categoriali()
# Valore con correlazione maggiore tra le categoriali= relationship (0.45)
# Passo 10. Calcolo correlazioni tra variabili quantitative e target (categoriale)
#modello.corr_quantitative()
# Valore con correlazione maggiore tra le quantitative= capital_gain (0.278)
# Passo 11. Grafico tra relationship e target
modello.grafico()