import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# 1. Load dataset
df = pd.read_csv("Mall_Customers.csv")

print("First 5 rows:")
print(df.head())

print("\nDataset shape:")
print(df.shape)

print("\nMissing values:")
print(df.isnull().sum())

# 2. Basic information
print("\nDataset information:")
print(df.info())

# 3. Select features
X = df[["Annual Income (k$)", "Spending Score (1-100)"]]

# 4. Visualize data
plt.figure(figsize=(8, 5))
plt.scatter(
    X["Annual Income (k$)"],
    X["Spending Score (1-100)"]
)
plt.xlabel("Annual Income (k$)")
plt.ylabel("Spending Score")
plt.title("Customer Distribution")
plt.show()

# 5. Scale the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 6. Elbow Method
inertia = []

for k in range(1, 11):
    model = KMeans(n_clusters=k, random_state=42, n_init=10)
    model.fit(X_scaled)
    inertia.append(model.inertia_)

plt.figure(figsize=(8, 5))
plt.plot(range(1, 11), inertia, marker="o")
plt.xlabel("Number of Clusters")
plt.ylabel("Inertia")
plt.title("Elbow Method")
plt.show()

# 7. Apply K-Means
kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)

df["Cluster"] = kmeans.fit_predict(X_scaled)

# 8. Silhouette Score
score = silhouette_score(X_scaled, df["Cluster"])

print("\nSilhouette Score:", score)

# 9. Display cluster information
print("\nCluster counts:")
print(df["Cluster"].value_counts())

print("\nCluster averages:")
print(
    df.groupby("Cluster")[[
        "Age",
        "Annual Income (k$)",
        "Spending Score (1-100)"
    ]].mean()
)

# 10. Visualize clusters
plt.figure(figsize=(10, 6))

sns.scatterplot(
    data=df,
    x="Annual Income (k$)",
    y="Spending Score (1-100)",
    hue="Cluster",
    palette="viridis",
    s=100
)

plt.title("Customer Segmentation using K-Means")
plt.xlabel("Annual Income (k$)")
plt.ylabel("Spending Score")
plt.legend(title="Cluster")
plt.show()