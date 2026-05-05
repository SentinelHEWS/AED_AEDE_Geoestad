import pandas as pd
import geopandas as gpd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pyproj
from skgstat import Variogram
import gstools as gs
from pykrige.ok import OrdinaryKriging
from pykrige.uk import UniversalKriging
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error
from shapely.geometry import Point

print("Este script no tiene checks porque me dio flojera hacerlo. Mete todos los datos bien si no quieres errores. Susceptible a error humano ngl.")
mesInteres = input("Mes de Interés (Sólo se pueden entre MARZO y JULIO): ")

velviento = pd.read_csv(f"{mesInteres}_VELVIENTO.csv")

coords = velviento[["X","Y"]]
valores = velviento["PROMEDIO"].values

modelos = ["spherical","exponential","gaussian","matern"]
variogramas_modelos = {}

for modelo in modelos:
  V = Variogram(coords,valores,estimator="cressie",model=modelo,maxlag=175000,n_lags=33)

  variogramas_modelos[modelo] = V

  plt.figure(figsize=(7,7), dpi = 200)

for model, V in variogramas_modelos.items():
  plt.plot(V.bins, V.fitted_model(V.bins), label = model)

plt.scatter(
    variogramas_modelos['spherical'].bins,
    variogramas_modelos['spherical'].experimental,
    color = "black",
    label = "Empirico"
)
plt.xlabel("Distancia (m)")
plt.ylabel("Semivarianza")
plt.legend()
plt.figtext(0.5, 0.95, "Semivariograma empírico de la velocidad del viento",
            fontweight = 'bold',
            color = "#525252",
            ha = 'center',
            fontsize = 14) # Titulo
plt.figtext(0.5, 0.93, "Comparación de modelos teóricos basado en el estimador Cressie",
            style = "italic",
            color = "#525252",
            ha = 'center',
            fontsize = 12) # Subtitulo
plt.figtext(0.05, 0.05, "Datos de NASA-POWER",
            color = "#525252",
            fontsize = 10) # Pie de gráfico
ax = plt.gca()
leg = ax.get_legend()

for text in leg.get_texts():
  text.set_color('#525252')
if leg is not None:
  leg.get_frame().set_linewidth(0)
  leg.get_frame().set_edgecolor("none")
plt.grid(False)
plt.tight_layout(rect = [0,0.05,1,0.92])
pathf1 = (f"{mesInteres}_SEMIVARS_VELVIENTO_PROM.png")
plt.savefig(pathf1,dpi=200)

print(V)

print("¡ATENCIÓN! Fíjate bien. Vas a meter cada valor que haya printeado el comando anterior en el input correspondiente. Si lo haces mal, te va a dar mal. Ponte liste.")
rangInput = float(input("Range: "))
sillInput = float(input("Sill: "))
nuggInput = float(input("Nugget: "))

mapaMUN = gpd.read_file('MUNICIPIOS.shp')
x = velviento['X'].values.astype(float)
y = velviento['Y'].values.astype(float)
z = velviento["PROMEDIO"].values.astype(float)

OK_best = OrdinaryKriging(
  x, y, z,
  variogram_model='gaussian',
  variogram_parameters={
      'nugget':nuggInput,
      'sill':sillInput,
      'range':rangInput,
  },
  nlags=20,
  verbose=True,
  enable_plotting=True
)

union_municipios = mapaMUN.union_all()
minx, miny, maxx, maxy = mapaMUN.total_bounds
resolucion = 100
xi = np.linspace(minx, maxx, resolucion)
yi = np.linspace(miny, maxy, resolucion)
xi_grid, yi_grid = np.meshgrid(xi, yi)

z_grid, var_grid = OK_best.execute("grid", xi, yi)

print(z_grid)

puntos = gpd.GeoDataFrame(
             geometry=[Point(xi_grid[i, j], yi_grid[i, j])
             for i in range(resolucion)
             for j in range(resolucion)],
            crs=mapaMUN.crs)
dentro = puntos.within(union_municipios)
dentro_grid = dentro.values.reshape(resolucion, resolucion)


fig, ax = plt.subplots(figsize=(10, 10))
z_masked   = np.where(dentro_grid,z_grid,np.nan)
var_masked = np.where(dentro_grid,var_grid,np.nan)
im = ax.pcolormesh(xi_grid,yi_grid,z_grid,cmap='viridis',shading='auto',vmin=np.nanmin(z_masked), vmax=np.nanmax(z_masked))
contours = ax.contour(xi_grid, yi_grid, z_grid,levels=8, colors='white',linewidths=0.5, alpha=0.4)
ax.clabel(contours, inline=True, fontsize=7, fmt='%.1f')
mapaMUN.plot(ax=ax, facecolor='none', edgecolor='black', linewidth=0.8)
cbar = plt.colorbar(im, ax=ax, orientation='horizontal',shrink=0.5, pad=0.02, label='Promedio (Kriging)')
ax.set_title(f'Interpolación Kriging — modelo Crissie: Gaussiano', fontsize=13)
ax.set_axis_off()
plt.tight_layout()
pathf2 = (f"{mesInteres}_OK_VELVIENTO.png")
plt.savefig(pathf2,dpi=200)

plt.clf()

errores = []
predichos = []
observados = []

for i in range(len(x)):
  x_train = np.delete(x, i)
  y_train = np.delete(y, i)
  z_train = np.delete(z, i)

  OK = OrdinaryKriging(
  x_train, y_train, z_train,
  variogram_model='gaussian',
  variogram_parameters={
    'nugget':nuggInput,
    'sill':sillInput,
    'range':rangInput},
  verbose=False,
  enable_plotting=False)

  z_pred, _ = OK.execute('points', [x[i]], [y[i]])
  predichos.append(z_pred[0])
  observados.append(z[i])
  errores.append(z[i] - z_pred[0])

arrayrmse = np.array(errores)
arrayobservados = np.array(observados)
arraypredichos = np.array(predichos)

MAE = np.mean(np.abs(errores))
RMSE = np.sqrt(np.mean(arrayrmse**2))
ME = np.mean(errores)
print(f"========== COMIENZA VALIDACIÓN KRIGING ORDINARIO {mesInteres} ==========")
print("MAE:", MAE)
print("RMSE:", RMSE)
print("ME (sesgo):", ME)
print(f"========== TERMINA VALIDACIÓN KRIGING ORDINARIO {mesInteres} ==========")

plt.scatter(arrayobservados, arraypredichos)
plt.plot([arrayobservados.min(), arrayobservados.max()],
[arrayobservados.min(), arrayobservados.max()], 'r--')
plt.xlabel("Observado")
plt.ylabel("Predicho")
plt.title("Validación Kriging")
plt.tight_layout()
pathf3 = (f"{mesInteres}_VALOK_VELVIENTO.png")
plt.savefig(pathf3,dpi=200)

plt.clf()

plt.scatter(velviento["X"], velviento["Y"], c=errores, cmap='coolwarm')
plt.colorbar(label="Error")
plt.title("Mapa de residuos")
plt.tight_layout()
pathf4 = (f"{mesInteres}_VALOKRES_VELVIENTO.png")
plt.savefig(pathf4,dpi=200)