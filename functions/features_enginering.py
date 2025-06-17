import pandas as pd
import numpy as np

def enrich_ecommerce_data(df, df_retours):
    """
    Effectue le feature engineering sur les données e-commerce.
    
    Paramètres :
    - df : DataFrame des commandes normales
    - df_retours : DataFrame des commandes annulées
    
    Retourne :
    - df_fe : DataFrame enrichi
    - customer_df : Agrégations client
    """
    try:
        print("\n🚀 Enrichissement des données...")

        # ➤ Fusion des jeux de données
        df_fe = pd.concat([df.copy(), df_retours.copy()], ignore_index=True)

        # ➤ Calcul du TotalPrice
        df_fe['TotalPrice'] = df_fe['Quantity'] * df_fe['UnitPrice']

        # ➤ Conversion des dates
        df_fe['InvoiceDate'] = pd.to_datetime(df_fe['InvoiceDate'])

        # ➤ Extraction des variables temporelles
        df_fe['Year'] = df_fe['InvoiceDate'].dt.year
        df_fe['Month'] = df_fe['InvoiceDate'].dt.month
        df_fe['Day'] = df_fe['InvoiceDate'].dt.day
        df_fe['Weekday'] = df_fe['InvoiceDate'].dt.day_name()
        df_fe['Hour'] = df_fe['InvoiceDate'].dt.hour
        df_fe['IsWeekend'] = df_fe['Weekday'].isin(['Saturday', 'Sunday'])

        # ➤ Commandes annulées
        df_fe['IsCancelled'] = df_fe['InvoiceNo'].astype(str).str.startswith('C')

        # ➤ Agrégation client
        customer_df = df_fe.groupby('CustomerID').agg({
            'InvoiceNo': pd.Series.nunique,
            'Quantity': 'sum',
            'TotalPrice': 'sum',
            'Country': 'first'
        }).reset_index().rename(columns={
            'InvoiceNo': 'NumInvoices',
            'Quantity': 'TotalQuantity',
            'TotalPrice': 'Revenue',
        })
        customer_df['AverageBasketValue'] = customer_df['Revenue'] / customer_df['NumInvoices']

        # ➤ Taux de retour client
        returns_df = df_fe[df_fe['IsCancelled']]
        returns_per_client = returns_df.groupby('CustomerID')['Quantity'].sum().abs()

        def safe_return_rate(customer_id):
            try:
                total_qty = customer_df.loc[customer_df['CustomerID'] == customer_id, 'TotalQuantity'].values[0]
                return 0 if total_qty == 0 else returns_per_client.get(customer_id, 0) / total_qty
            except IndexError:
                return 0

        customer_df['ReturnRateCustomer'] = customer_df['CustomerID'].map(safe_return_rate)

        # ➤ Recency (RFM)
        last_date = df_fe['InvoiceDate'].max()
        recency_df = df_fe.groupby('CustomerID').agg({
            'InvoiceDate': lambda x: (last_date - x.max()).days
        }).reset_index().rename(columns={'InvoiceDate': 'Recency'})
        customer_df = pd.merge(customer_df, recency_df, on='CustomerID', how='left')

        # ➤ Diversité produit par commande
        df_fe['DistinctProductsPerInvoice'] = df_fe.groupby('InvoiceNo')['StockCode'].transform('nunique')

        # ➤ Prix moyen par produit
        avg_price_product = df_fe.groupby('StockCode')['UnitPrice'].mean().reset_index().rename(
            columns={'UnitPrice': 'AveragePricePerProduct'}
        )
        df_fe = df_fe.merge(avg_price_product, on='StockCode', how='left')

        # ➤ Taux de retour par produit
        returns_by_product = returns_df.groupby('StockCode')['Quantity'].sum().abs()
        total_sold_by_product = df_fe.groupby('StockCode')['Quantity'].sum()
        return_rate_product = returns_by_product / total_sold_by_product
        return_rate_product = return_rate_product.replace([np.inf, -np.inf], np.nan).fillna(0)
        df_fe['ReturnRateProduct'] = df_fe['StockCode'].map(return_rate_product)

        print("\n✅ Feature engineering terminé.")

        return df_fe, customer_df

    except Exception as e:
        print(f"\n❌ Une erreur est survenue pendant le feature engineering : {e}")
        return None, None