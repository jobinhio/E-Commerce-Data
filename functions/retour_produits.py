import pandas as pd

def detecter_produits_problemes_qualite(df, seuil_retour=0.0, top_n=10):
    """
    Détecte les produits avec un taux de retour moyen élevé.

    Paramètres :
    - df : DataFrame contenant la colonne 'ReturnRateProduct'
    - seuil_retour : seuil minimal pour considérer un produit comme problématique
    - top_n : nombre de produits à afficher

    Retour :
    - DataFrame des produits avec taux de retour élevé
    """
    try:
        produits = (
            df[df['ReturnRateProduct'] > seuil_retour]
            .groupby(['StockCode', 'Description'])
            .agg({'ReturnRateProduct': 'mean'})
            .reset_index()
            .sort_values(by='ReturnRateProduct', ascending=False)
        )
        print("🔍 Produits posant potentiellement des problèmes de qualité :")
        display(produits.head(top_n))
        return produits

    except Exception as e:
        print(f"❌ Erreur dans l'analyse des produits problématiques : {e}")
        return pd.DataFrame()


def detecter_produits_les_plus_retournes(df, top_n=10):
    """
    Identifie les produits les plus retournés (quantité totale retournée).

    Paramètres :
    - df : DataFrame contenant 'IsCancelled' == True
    - top_n : nombre de produits à afficher

    Retour :
    - DataFrame des produits les plus retournés
    """
    try:
        retours = df[df['IsCancelled'] == True]

        produits_retournes = (
            retours.groupby(['StockCode', 'Description'])
            .agg({'Quantity': 'sum', 'ReturnRateProduct': 'mean'})
            .reset_index()
            .sort_values(by='Quantity', ascending=True)  # Quantité négative = retour
        )
        print("🔁 Produits les plus retournés en quantité :")
        display(produits_retournes.head(top_n))
        return produits_retournes

    except Exception as e:
        print(f"❌ Erreur dans l'identification des retours : {e}")
        return pd.DataFrame()