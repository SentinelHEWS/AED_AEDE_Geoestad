import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pyproj
from skgstat import Variogram

mesInteres = "JULIO" #Puedes escribir o MARZO, ABRIL, MAYO, JUNIO o JULIO.
varInteres = "VELVIENTO" #Puedes escribir o VELVIENTO, TEMPERATURA, HUMEDAD o DIRVIENTO.
estimador = "matheron" #Escribir entre "matheron", "cressie", "genton", "dowd"

nombrePlot = mesInteres + "_" + varInteres + estimador + "SEMIVARIOGRAMA_PROMEDIO.png" 

ruta = (f"{mesInteres}_{varInteres}.csv")

dataset = pd.read_csv(ruta)
dataset = dataset.reset_index()

dataset["ESTACION"] = dataset["ESTACION"].str.replace("_NASAPOWER_MARJUL25","")
coords = dataset[["X","Y"]].values.tolist()
valores = dataset["PROMEDIO"].values.tolist()

modelos = ["spherical","exponential","gaussian","matern"]
variogramas_modelos = {}

for modelo in modelos:
  V = Variogram(coords,valores,estimator="matheron",model=modelo,maxlag=175000,n_lags=33)
  variogramas_modelos[modelo] = V

for model, V in variogramas_modelos.items():
  plt.plot(V.bins, V.fitted_model(V.bins), label = model)

plt.scatter(
    variogramas_modelos['spherical'].bins,
    variogramas_modelos['spherical'].experimental,
    color = "black",
    label = "Datos"
)

plt.xlabel("Distancia (m)")
plt.ylabel("Semivarianza")
plt.legend()
plt.title(f"SEMIVARIOGRAMA PARA VELOCIDAD DEL VIENTO DEL MES DE {mesInteres} \n (ESTIMADOR MATHERON)",fontsize="12",loc="center")
ax = plt.gca()
leg = ax.get_legend()
for text in leg.get_texts():
  text.set_color('#525252')
if leg is not None:
  leg.get_frame().set_linewidth(0)
  leg.get_frame().set_edgecolor("none")
plt.grid(False)
plt.tight_layout()
print(V)
plt.savefig(nombrePlot, dpi=200)