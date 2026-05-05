# ESCRITO POR UN HUMANO, NO POR IA
# POR IDW

import libpysal
from libpysal.weights import DistanceBand
import geopandas as gpd
import matplotlib.pyplot as plt
import esda
from libpysal import weights 
from splot.esda import plot_moran
from splot import esda as esdaplot
import seaborn as sns
import numpy as np
import pandas as pd


mesInteres = "ABRIL"

mhr = gpd.read_file(f'{mesInteres}.shp')

W_D_inv=DistanceBand.from_dataframe(mhr,threshold=175000,binary=False,p=2,alpha=-2.0,ids="ESTACION")
W_D_inv.transform = 'r'
W_D_inv.neighbors

W_D_inv_dense,ids=W_D_inv.full()
print("Dimension de W:",W_D_inv_dense.shape)
W_D_inv_dense

W_D_inv2=DistanceBand.from_dataframe(mhr,threshold=175000,binary=False,p=2,alpha=-2)

fig, ax = plt.subplots(figsize=(10,10))
mhr.plot(ax=ax, facecolor="cyan", edgecolor="magenta")

W_D_inv2.plot(
    mhr,
    edge_kws = dict(linewidth = 1, color = "magenta"),
    ax = ax
)

plt.title("Mapa de pesos espaciales por distancia (33 EMA) \n DISTANCIA INVERSA A 175,000m")
for nomEMA, row in mhr.iterrows():
  x = row.geometry.centroid.x
  y = row.geometry.centroid.y
  ax.text(x,y,row["ESTACION"],color="darkblue",fontsize=10,ha="center",fontweight="bold")

ax.set_axis_off()
ax = plt.gca()
plt.grid(False)
plt.tight_layout()
pathF = (f"{mesInteres}_INVIDW.png")
#plt.savefig(pathF, dpi=200)

plt.clf()
Moran_W_idw=esda.moran.Moran(mhr['PROMEDIO'],W_D_inv2)
print(f"el valor del índice es de: {Moran_W_idw.I:.2f}")
print(f"el valor del estadístico Z de Moran es de: {Moran_W_idw.z_norm:.2f}")
print(f"el valor del probabilidad p-valor del estadístico Z de Moran es de:{Moran_W_idw.p_norm:.2f}")

promedioSTD = (mhr['PROMEDIO'] - mhr['PROMEDIO'].mean()) / np.std(mhr['PROMEDIO'])
promedioSTDlags = weights.spatial_lag.lag_spatial(W_D_inv2,promedioSTD)

f, ax = plt.subplots(1, figsize = (10,10), dpi = 100)
sns.regplot(
    x = promedioSTD,
    y = promedioSTDlags,
    ci = None,
    data = mhr,
    line_kws = {'color': 'r'}
)
ax.axvline(0, c="k", alpha=0.5)
ax.axhline(0, c="k", alpha=0.5)
plt.title("Gráfico de Moran (VELVIENTO) \n MATRIZ PESO IDW")
ax = plt.gca()
plt.grid(False)
plt.tight_layout()
#pathF1 = ("MORAN.png")
#plt.savefig(pathF1, dpi=200)

#LOCAL
plt.clf()

np.random.seed(123)
lmoran = esda.moran.Moran_Local(mhr["PROMEDIO"],W_D_inv2)

df_moran_local=pd.DataFrame(
    {
        'Poligono':mhr['ESTACION'],
        "Moran_I": lmoran.Is,
        "Z_value":lmoran.z_sim,
        "P_value":lmoran.p_z_sim 
    }
)
df_moran_local

f, axs=plt.subplots(nrows=2,ncols=2, figsize=(10,5),dpi=200)
axs = axs.flatten()

ax=axs[0]
mhr.assign(
    Is=lmoran.Is
).plot(
    column="Is",
    cmap="plasma",
    k=5,
    edgecolor="white",
    linewidth=0.1,
    alpha=0.75,
    ax=ax,
    legend=True
)

ax=axs[1]
esdaplot.lisa_cluster(lmoran,mhr,p=1,ax=ax)

ax = axs[2]
labels = pd.Series(
    1 * (lmoran.p_sim < 0.05),
    index = mhr.index
).map({1: "Significativo", 0:"No significativo"})
mhr.assign(
    cl=labels
).plot(
    column="cl",
    categorical=True,
    k=2,
    cmap="Paired",
    edgecolor="white",
    legend=True,
    ax=ax
)

ax = axs[3]
esdaplot.lisa_cluster(lmoran, mhr, p = 0.05, ax = ax)
for i, ax in enumerate(axs.flatten()):
  ax.set_axis_off()
  ax.set_title(
      [
          "Estadísticos locales",
          "Cuadrantes",
          "Significancia estadística",
          "Cluster Moran"
      ][i],
      y = 0
  )

plt.figtext(0.4, 0.95, "Gráfico de Moran local de la variable Humedad",
            fontweight = 'bold',
            color = "#525252",
            ha = 'center',
            fontsize = 14) # Titulo
plt.figtext(0.4, 0.87, "Matriz de peso de IDW a 250,000m",
            style = "italic",
            color = "#525252",
            ha = 'center',
            fontsize = 12) # Subtitulo
ax = plt.gca()
plt.grid(False)
plt.tight_layout(rect = [0,0.05,0.85,0.89])
pathF2 = ("MORANLOC.png")
plt.savefig(pathF2, dpi=200)