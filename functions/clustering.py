import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from typing import Tuple


def compute_rfm_scores(customer_df: pd.DataFrame) -> pd.DataFrame:
    print("\n📈 Analyse RFM en cours...")

    rfm_df = customer_df.rename(columns={'Recency': 'R', 'NumInvoices': 'F', 'Revenue': 'M'})

    rfm_df['R_score'] = pd.qcut(rfm_df['R'], 5, labels=[5, 4, 3, 2, 1]).astype(int)
    rfm_df['F_score'] = pd.qcut(rfm_df['F'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5]).astype(int)
    rfm_df['M_score'] = pd.qcut(rfm_df['M'], 5, labels=[1, 2, 3, 4, 5]).astype(int)

    rfm_df['RFM_Score'] = (
        rfm_df['R_score'].astype(str) +
        rfm_df['F_score'].astype(str) +
        rfm_df['M_score'].astype(str)
    )

    def segment_rfm(row):
        if row['R_score'] >= 4 and row['F_score'] >= 4 and row['M_score'] >= 4:
            return 'Champions'
        elif row['R_score'] >= 3 and row['F_score'] >= 3 and row['M_score'] >= 3:
            return 'Loyal'
        elif row['R_score'] >= 4 and row['F_score'] <= 2:
            return 'Nouveaux'
        elif row['R_score'] <= 2 and row['F_score'] >= 4:
            return 'À relancer'
        elif row['R_score'] <= 2 and row['F_score'] <= 2:
            return 'Inactifs'
        else:
            return 'Autres'

    rfm_df['Segment'] = rfm_df.apply(segment_rfm, axis=1)
    print("\n✅ Analyse RFM terminée. Aperçu des segments clients :")
    display(rfm_df[['CustomerID', 'R', 'F', 'M', 'RFM_Score', 'Segment']].head())

    fig = px.pie(rfm_df, names='Segment', title='🧠 Segmentation des clients (RFM)',
                 color_discrete_sequence=px.colors.sequential.RdBu)
    fig.show()

    return rfm_df


def perform_kmeans_clustering(rfm_df: pd.DataFrame, n_clusters: int = 4) -> Tuple[pd.DataFrame, go.Figure, px.scatter_3d]:
    features_rfm = ['R', 'F', 'M']
    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(rfm_df[features_rfm])

    inertia = []
    K_range = range(1, 11)
    for k in K_range:
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(rfm_scaled)
        inertia.append(kmeans.inertia_)

    fig_elbow = go.Figure()
    fig_elbow.add_trace(go.Scatter(
        x=list(K_range), y=inertia, mode='lines+markers', marker=dict(size=8),
        line=dict(color='royalblue'), name='Inertie'))
    fig_elbow.update_layout(
        title="Méthode du coude pour déterminer le nombre optimal de clusters",
        xaxis_title="Nombre de clusters (K)",
        yaxis_title="Inertie intra-cluster (distorsion)",
        template="plotly_white")

    # Appliquer le clustering avec le k optimal spécifié
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    rfm_df['Cluster'] = kmeans.fit_predict(rfm_scaled)

    fig_cluster_3d = px.scatter_3d(
        rfm_df, x='R', y='F', z='M',
        color='Cluster', symbol='Cluster',
        title="Segmentation des clients par K-means (RFM)",
        labels={'R': 'Récence', 'F': 'Fréquence', 'M': 'Montant'},
        template="plotly_white")

    fig_elbow.show()
    fig_cluster_3d.show()

    return rfm_df, fig_elbow, fig_cluster_3d


def summarize_clusters(rfm_df: pd.DataFrame) -> pd.DataFrame:
    cluster_counts = rfm_df['Cluster'].value_counts().reset_index()
    cluster_counts.columns = ['Cluster', 'Nb_clients']
    cluster_counts.sort_values(by='Cluster', inplace=True)

    cluster_profile = rfm_df.groupby('Cluster')[['R', 'F', 'M']].mean().round(1)
    cluster_profile['Nb_clients'] = cluster_counts.set_index('Cluster')['Nb_clients']

    print("\n📊 Profil des clusters :")
    display(cluster_profile)
    return cluster_profile