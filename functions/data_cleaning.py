import pandas as pd

def clean_ecommerce_data(df):
    """
    Nettoyage des données e-commerce.
    - Supprime doublons, valeurs manquantes critiques, anomalies dans StockCode, descriptions indésirables.
    - Exclut les transactions erronées (quantité/prix ≤ 0).
    
    Retourne :
        - df_clean : DataFrame nettoyé
        - df_retours : Transactions invalides (Quantity ou UnitPrice ≤ 0)
    """
    print("✅ Nettoyage des données en cours...")

    # 1. Suppression des doublons
    initial_shape = df.shape
    df.drop_duplicates(inplace=True)
    print(f"🗑️ Doublons supprimés : {initial_shape[0] - df.shape[0]} lignes supprimées")

    # 2. Suppression des lignes avec valeurs manquantes critiques
    missing_before = df.isnull().sum()
    df.dropna(subset=['CustomerID', 'Description'], inplace=True)
    missing_after = df.isnull().sum()
    print("🧩 Valeurs manquantes supprimées :")
    print(f"- Description : {missing_before['Description'] - missing_after['Description']}")
    print(f"- CustomerID  : {missing_before['CustomerID'] - missing_after['CustomerID']}")

    # 3. Détection et suppression des anomalies dans StockCode
    mask_non_standard = ~df['StockCode'].str.match(r'^[A-Z0-9]+$', na=False)
    df['stockcode_length'] = df['StockCode'].str.len()
    df_outliers_length = df[(df['stockcode_length'] < 4) | (df['stockcode_length'] > 10)]
    stockcode_exceptions = ['POST', 'BANK CHARGES', 'C2', 'DOT', 'M', 'AMAZONFEE', 'PADS', 'S', 'D']

    df = df[~df['StockCode'].isin(stockcode_exceptions)]
    df = df[~mask_non_standard]
    df.drop(columns='stockcode_length', inplace=True)

    print("📦 Anomalies dans StockCode exclues :")
    print(f"- Codes spéciaux exclus : {len(stockcode_exceptions)} types")
    print(f"- Formats non standards : {mask_non_standard.sum()} lignes supprimées")
    print(f"- Longueurs anormales : {df_outliers_length.shape[0]} identifiés")

    # 4. Suppression de descriptions non pertinentes
    descriptions_to_exclude = ['Next Day Carriage', 'High Resolution Image']
    desc_exclues = df[df['Description'].isin(descriptions_to_exclude)]
    df = df[~df['Description'].isin(descriptions_to_exclude)]
    print(f"📝 Descriptions supprimées : {len(descriptions_to_exclude)} types exclus")
    print(f"- Lignes supprimées : {desc_exclues.shape[0]}")

    # 5. Traitement des transactions annulées ou erronées
    invalid_transactions = df[(df['Quantity'] <= 0) | (df['UnitPrice'] <= 0)]
    print(f"⚠️ Transactions annulées ou invalides détectées : {invalid_transactions.shape[0]}")
    df_retours = invalid_transactions.copy()
    df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]

    # 6. Résultat final
    print("✅ Nettoyage terminé.")
    print(f"📦 Dimensions finales du dataset : {df.shape}")

    return df, df_retours
