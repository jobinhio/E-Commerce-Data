import pandas as pd
import numpy as np

# ==============================================
# 💡 MODULE 1 : Chargement et vérification des données
# ==============================================
def load_and_check_data(filepath: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(filepath, encoding='ISO-8859-1')
        print(f"✅ Données chargées avec succès. Dimensions : {df.shape}")
    except Exception as e:
        raise Exception(f"❌ Erreur lors du chargement : {e}")

    if df.isnull().sum().any():
        print("⚠️ Des valeurs manquantes ont été détectées.")
    return df