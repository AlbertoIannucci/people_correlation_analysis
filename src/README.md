## 🐍 Script Python – Processo ETL

Il progetto è strutturato in moduli Python che implementano un pipeline ETL completa: **Estrazione**, **Trasformazione** e **Caricamento** dei dati.

### 📌 `modello_base.py`
Classe astratta di supporto che contiene metodi riutilizzabili per l'esplorazione e l'analisi preliminare di dataset in formato `pandas.DataFrame`.

### 📌 `extract_transform.py`
Script dedicato alla fase di **data cleaning e trasformazione**:
- Gestione dei valori mancanti
- Calcoli derivati 
- Conversioni di tipo
- Rimappatura delle colonne in snake_case
- Aggiunta di codifiche per chiavi esterne
- Studio di correlazione

### 📌 `load.py`
Script per la fase di **caricamento dei dati** nel database MySQL:
- Popolamento delle tabelle di decodifica 
- Inserimento dei record nella tabella principale `sale` con gestione delle chiavi esterne
