import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

mesInteres = "JULIO" #Puedes escribir o MARZO, ABRIL, MAYO, JUNIO o JULIO.
varInteres = "VELVIENTO" #Puedes escribir o VELVIENTO, TEMPERATURA, HUMEDAD o DIRVIENTO.

nombrePlot = mesInteres + "_" + varInteres + "_PROMEDIO_VARIANZA_PLOT.png"

ruta = (f"{mesInteres}_{varInteres}.csv")

dataset = pd.read_csv(ruta)
dataset = dataset.reset_index()

dataset["ESTACION"] = dataset["ESTACION"].str.replace("_NASAPOWER_MARJUL25","")
estaciones = dataset["ESTACION"].values.tolist()
promedio = dataset["PROMEDIO"].values.tolist()
varianza = dataset["VARIANZA"].values.tolist()

#GRÁFICO DE LÍNEAS ESTACIONES VS PROMEDIO
plt.title(f"GRÁFICO DE LÍNEAS PARA PROMEDIO Y VARIANZA DEL MES DE {mesInteres}",loc="center")
plt.plot(estaciones,promedio)
plt.xticks(rotation=90)
plt.tight_layout()

plt.plot(estaciones,varianza)
plt.xticks(rotation=90)
plt.tight_layout()

plt.legend(["Promedio","Varianza"])
plt.savefig(nombrePlot, dpi=200)