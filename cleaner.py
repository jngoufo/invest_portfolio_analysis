# cleaner.py (Version Finale, Définitive et Robuste)
import pandas as pd
import logging
import sys
import configparser
from sqlalchemy import create_engine, text
from datetime import datetime
import os

# --- Configuration de base ---
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# --- Configuration du logging ---
log_filename = f"./log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename, mode='w', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

logging.info("--- Début du script Python (nettoyage et chargement) ---")

# --- 1. Lecture de la configuration ---
try:
    config = configparser.ConfigParser()
    config.read('config.ini')
    db_config = config['database']
    settings_config = config['settings']
    USD_TO_CAD_RATE = float(settings_config['usd_to_cad_rate'])
    logging.info(f"Configuration lue avec succès. Taux de change USD->CAD : {USD_TO_CAD_RATE}")
except Exception as e:
    logging.error(f"ERREUR: Impossible de lire 'config.ini'. Erreur: {e}")
    exit()

# --- 2. Nettoyage des données ---
try:
    logging.info("Étape de nettoyage démarrée.")
    raw_csv_path = './source/tipranks_raw.csv'
    df = pd.read_csv(raw_csv_path)

    # Standardisation complète des noms de colonnes
    df.columns = [
        col.strip().lower().replace(' ', '_').replace('%', '_pct').replace('/', '_').replace('.', '')
        for col in df.columns
    ]
    logging.info(f"Noms de colonnes standardisés.")
    
    # --- CORRECTION FINALE : Filtrer les lignes vides ---
    df.dropna(subset=['ticker'], inplace=True)
    logging.info(f"Lignes vides filtrées. {len(df)} lignes valides restantes.")

    df['original_holding_value'] = df.get('holding_value')

    def clean_numeric_column(series, is_percentage=False):
        series_str = series.astype(str).str.strip()
        if is_percentage: series_str = series_str.str.replace('%', '', regex=False)
        series_str = series_str.str.replace('[^0-9.]', '', regex=True)
        return pd.to_numeric(series_str, errors='coerce')

    def detect_currency(value_str):
        if isinstance(value_str, str) and 'C' in value_str.upper(): return 'CAD'
        return 'USD'
    if 'original_holding_value' in df.columns:
        df['currency'] = df['original_holding_value'].apply(detect_currency)

    # Nettoyage sur les noms de colonnes standardisés
    for col in ['holding_value', 'price', 'purchase_price', 'no_of_shares']:
        if col in df.columns: df[col] = clean_numeric_column(df[col])
            
    pct_cols = ['holding_gain_daily_change__pct', 'holding_gain_change__pct', 'six_month_pct', 'year_to_date_pct', 'one_year_pct', '_pct_of_portfolio']
    for col in pct_cols:
        if col in df.columns: df[col] = clean_numeric_column(df[col], is_percentage=True)
            
    target_cols = ['highest_price_target', 'lowest_price_target']
    for col in target_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.split(' ').str[0]
            df[col] = clean_numeric_column(df[col])
            
    if 'holding_value' in df.columns:
        df['holding_value_cad'] = df.apply(lambda r: r['holding_value'] * USD_TO_CAD_RATE if r.get('currency') == 'USD' else r['holding_value'], axis=1)
    
    df = df.rename(columns={
        'no_of_shares': 'shares', 'holding_gain_change__pct': 'holding_gain_change_pct',
        'six_month_pct': 'six_month_return_pct', 'year_to_date_pct': 'ytd_return_pct', 
        'one_year_pct': 'one_year_return_pct', '_pct_of_portfolio': 'portfolio_pct'
    })
    
    final_columns = ['ticker','name','shares','price','purchase_price','holding_value','holding_gain_change_pct','six_month_return_pct','ytd_return_pct','one_year_return_pct','portfolio_pct','industry','p_e_ratio','currency','holding_value_cad','highest_price_target','lowest_price_target']
    df_final = df[[col for col in final_columns if col in df.columns]].copy()
    df_final = df_final.where(pd.notna(df_final), None)
    
    logging.info("Nettoyage des données terminé avec succès.")
except Exception as e:
    logging.error(f"ERREUR PENDANT L'ÉTAPE DE NETTOYAGE : {e}", exc_info=True)
    exit()

# --- 3. Chargement dans MySQL ---
try:
    logging.info("Étape de chargement dans MySQL démarrée.")
    connection_string = f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}"
    engine = create_engine(connection_string)
    
    week_num = datetime.now().isocalendar()[1]
    table_id = ((week_num - 1) % 12) + 1
    table_name = f"portfolio_week_{table_id}"
    logging.info(f"Préparation de la mise à jour de la table : {table_name}")

    with engine.connect() as conn:
        trans = conn.begin()
        try:
            conn.execute(text(f"DROP TABLE IF EXISTS {table_name};"))
            conn.execute(text(f"CREATE TABLE {table_name} LIKE portfolio_template;"))
            
            if not df_final.empty:
                cols = ", ".join([f"`{c}`" for c in df_final.columns])
                placeholders = ", ".join([f":{c}" for c in df_final.columns])
                insert_stmt = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"
                data_to_insert = df_final.to_dict(orient='records')
                conn.execute(text(insert_stmt), data_to_insert)
            
            trans.commit()
            logging.info(f"{len(df_final)} lignes ont été insérées dans la table '{table_name}'.")
        except Exception as e:
            trans.rollback()
            logging.error(f"ERREUR lors de la transaction SQL. Annulation des changements. Erreur: {e}", exc_info=True)
            exit()
            
    logging.info("Chargement dans MySQL réussi !")
except Exception as e:
    logging.error(f"ERREUR LORS DE LA CONNEXION OU DU CHARGEMENT DANS MYSQL : {e}", exc_info=True)
    exit()

logging.info("--- Processus complet terminé avec succès ---")