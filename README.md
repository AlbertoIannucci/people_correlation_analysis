# Analisi delle Correlazioni - Dataset "people.csv" 📊
Questo progetto Python esegue un'analisi approfondita delle correlazioni sul dataset "people.csv", con un focus sull'individuazione delle correlazioni significative tra le varie caratteristiche (variabili numeriche e categoriali) e la variabile target

🎯 Obiettivo del Progetto:

Identificare le caratteristiche chiave che influenzano la variabile target (es. "Reddito") 💡

Mostrare come eseguire analisi delle correlazioni utilizzando Python 🐍

## 📂 Contenuto del repository

- `extract_transform.py`: Script per il caricamento e la pulizia del dataset originale (CSV), con studio di correlazione.
- `load.py`: Script per il caricamento dei dati nel database MySQL, incluse le tabelle di decodifica e la tabella principale.
- `db_schema.png`: Diagramma E-R.

## 🧰 Tecnologie utilizzate

- **Linguaggi**: Python
- **Librerie principali**: `pandas`, `pymysql`
- **Database**: MySQL
- **Strumenti statistici**: Test chi_2, cramer, spearman

## 🧪 Funzionalità principali

### 1. Data Cleaning (ET)
- Conversioni di tipo e gestione dei NaN
- Rimappatura colonne in snake_case
- Creazione di codifiche per chiavi esterne
- Studio della correlazione

### 2. Database Design (Modello Relazionale)
- Tabelle: `occupation`, `education`, `workclass`, `race`, `marital_status`, `relationship`, `person`
- Relazioni gestite tramite foreign key

### 3. Data Loading (L)
- Inserimento automatico dei dati tramite `pymysql`
- Separazione tra dati principali e tabelle di decodifica

## 📊 Risultati Chiave

**Variabile maggiormente correlata alla variabile target**: relationship (cramer 0.45, grado di dipendenza media)

## 🔒 Licenza

Distribuito sotto licenza MIT. Vedi il file `LICENSE` per maggiori dettagli.
