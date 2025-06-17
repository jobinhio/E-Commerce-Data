import os
import plotly.express as px
import plotly.graph_objects as go

def creer_dossier_resultats(path="./Resultats"):
    try:
        os.makedirs(path, exist_ok=True)
        print(f"📁 Dossier de sortie prêt : {path}")
    except Exception as e:
        print(f"❌ Erreur lors de la création du dossier : {e}")

def top_10_produits_vendus(df, save_path):
    try:
        top = df.groupby('Description')['Quantity'].sum().nlargest(10).reset_index()
        fig = px.bar(top, x='Quantity', y='Description', orientation='h',
                     title='🔝 Top 10 des produits les plus vendus (en quantité)',
                     labels={'Description': 'Produit', 'Quantity': 'Quantité vendue'},
                     template='plotly_white')
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})
        fig.write_image(f"{save_path}/top_10_produits_vendus.png")
        fig.show()
    except Exception as e:
        print(f"❌ Erreur top_10_produits_vendus : {e}")

def top_10_produits_rentables(df, save_path):
    try:
        top = df.groupby('Description')['TotalPrice'].sum().nlargest(10).reset_index()
        fig = px.bar(top, x='TotalPrice', y='Description', orientation='h',
                     title='💰 Top 10 des produits les plus rentables (CA)',
                     labels={'Description': 'Produit', 'TotalPrice': "Chiffre d'affaires"},
                     template='plotly_white')
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})
        fig.write_image(f"{save_path}/top_10_produits_rentables.png")
        fig.show()
    except Exception as e:
        print(f"❌ Erreur top_10_produits_rentables : {e}")

def ventes_par_jour(df, save_path):
    try:
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        sales = df.groupby('Weekday')['TotalPrice'].sum().reindex(days).reset_index()
        fig = px.bar(sales, x='Weekday', y='TotalPrice',
                     title='📅 Chiffre d\'affaires par jour de la semaine',
                     labels={'TotalPrice': "Chiffre d'affaires"},
                     template='plotly_white')
        fig.write_image(f"{save_path}/ventes_par_jour_semaine.png")
        fig.show()
    except Exception as e:
        print(f"❌ Erreur ventes_par_jour : {e}")

def ventes_par_heure(df, save_path):
    try:
        hourly = df.groupby('Hour')['TotalPrice'].sum().reset_index()
        fig = px.line(hourly, x='Hour', y='TotalPrice', markers=True,
                      title='⏰ Chiffre d\'affaires par heure de la journée',
                      labels={'TotalPrice': "Chiffre d'affaires"},
                      template='plotly_white')
        fig.write_image(f"{save_path}/ventes_par_heure.png")
        fig.show()
    except Exception as e:
        print(f"❌ Erreur ventes_par_heure : {e}")

def heatmap_ventes(df, save_path):
    try:
        pivot = df.pivot_table(index='Weekday', columns='Hour', values='TotalPrice', aggfunc='sum').fillna(0)
        pivot = pivot.reindex(columns=range(24), fill_value=0)
        fig = px.imshow(pivot,
                        labels=dict(x="Heure", y="Jour de la semaine", color="Chiffre d'affaires"),
                        x=pivot.columns, y=pivot.index,
                        title="🌡️ Heatmap des ventes par heure et jour de la semaine",
                        color_continuous_scale='Blues')
        fig.write_image(f"{save_path}/heatmap_ventes_jour_heure.png")
        fig.show()
    except Exception as e:
        print(f"❌ Erreur heatmap_ventes : {e}")

def distribution_diversite(df, save_path):
    try:
        diversity = df.groupby('InvoiceNo')['DistinctProductsPerInvoice'].max().reset_index()
        fig = px.histogram(diversity, x='DistinctProductsPerInvoice', nbins=20,
                           title="📦 Distribution de la diversité produit par commande",
                           labels={'DistinctProductsPerInvoice': "Nb de produits distincts"},
                           template='plotly_white')
        fig.write_image(f"{save_path}/distribution_diversite_produit.png")
        fig.show()
    except Exception as e:
        print(f"❌ Erreur distribution_diversite : {e}")

def analyser_ventes(df):
    save_path = "./img"
    creer_dossier_resultats(save_path)
    print("\n🔍 Analyse des ventes en cours...\n")

    top_10_produits_vendus(df, save_path)
    top_10_produits_rentables(df, save_path)
    ventes_par_jour(df, save_path)
    ventes_par_heure(df, save_path)
    heatmap_ventes(df, save_path)
    distribution_diversite(df, save_path)

    print("\n✅ Analyse des ventes terminée. Les visualisations ont été enregistrées dans le dossier './img/'")