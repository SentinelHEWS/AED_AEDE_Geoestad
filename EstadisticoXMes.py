# ESCRITO POR UN HUMANO, NO POR IA

'''
   _____  _______________  __  ____________________  _  __________
  /  _/ |/ / __/_  __/ _ \/ / / / ___/ ___/  _/ __ \/ |/ / __/ __/
 _/ //    /\ \  / / / , _/ /_/ / /__/ /___/ // /_/ /    / _/_\ \  
/___/_/|_/___/ /_/ /_/|_|\____/\___/\___/___/\____/_/|_/___/___/  
                                                                  

IMPORTANTE: En la variable "path" establece tu ruta a los documentos que quieres analizar.
IMPORTANTE: Si estás corriendo en Colab es necesario importar librería de GDrive

1. En "mesAnalisis" y dentro de las comillas después del igual, escribe el mes que te interesa analizar (cualquiera entre MARZO y JULIO).
2. Exactamente en la línea 51, dentro de los argumentos de pd.read_csv, cambia el número dentro de los corchetes de "usecols" al número de columna de tu variable interés.
IMPORTANTE: Python comienza numeración desde el 0, no desde el 1.
3. Exactamente en la línea 86, dentro de los argumentos de dfFinal.to_csv, casi al final se encuentran llaves con el texto "mesAnalisis" y después viene hardcodeada la variable interés.
IMPORTANTE: Sigue el paso 3 para cambiar el nombre de los archivos finales para que coincidan con tu variable y te organices mejor.
La verdad es que me dio flojera moverle para que diera el nombre automático lol

IMPORTANTE PARTE MIL: Las coordenadas X y Y vienen hardcodeadas y asumen que tus datos corresponden a como los hemos manejado en clase (pues pandas les hace organización alfabética A-Z automáticamente).
VERIFICA QUE LAS COORDENADAS CORRESPONDAN A TUS DATOS.
SI HAY MÁS COORDENADAS QUE DATOS O VICEVERSA, EL SCRIPT VA A TIRAR ERROR.
PUEDES ARREGLARO QUITANDO DE LA LISTA DE COORDENADAS X y Y LAS QUE NO TE INTERESAN.
'''

import pandas as pd
import glob
import os
import numpy as np

path = ("*csv")

mesAnalisis = "JULIO" 

nDatos = []
maximoDatos = []
minimoDatos = []
promedioDatos = []
varianzaDatos = []
desvestDatos = []
nombreDatos = []

if mesAnalisis == "MARZO":
    doyRead = np.arange(0,32)
elif mesAnalisis == "ABRIL":
    doyRead = np.arange(31,62)
elif mesAnalisis == "MAYO":
    doyRead = np.arange(61,93)
elif mesAnalisis == "JUNIO":
    doyRead = np.arange(92,123)
elif mesAnalisis == "JULIO":
    doyRead = np.arange(122,154)
else:
    ValueError

coordenadasX = [777310.993,594039.274,589979.77,738750.53,791066.28,666540.01,642927.35,509223.458,599638.0242,635282.46,452659.315,648494.61,628072.34,624643.491,615591.21,594124.88,653802.69,695209.5,673093.47,544082.54,724428.031,724438.95,572407.27,541801.61,672805.39,679443,707202.88,655714.33,624038.09,586233.04,624672.08,720649.04,449899.639]
coordenadasY = [2982268.186,2794433.89,2790714.73,2779899.39,2986800.23,2843138.4,2855848,2998714.564,2936953.205,2821613.53,2674880.018,2826246.17,2699219.52,2952312.747,2857610.68,2794188.37,2825875.5,2850424.08,2773582.01,2785319.85,2726620.477,2725943.5,2811650.36,2825731.63,2850173.74,2731536.83,2745988.58,2888397.13,2891779.9,2934578.84,2952220.76,2802033.41,2924571.899]

for file in glob.glob(path):
    datos = pd.read_csv(file,usecols=[5],skiprows = lambda x: x not in doyRead) 
    name = os.path.basename(file).split('.',1)[0]

    # Estadística
    n = len(datos)
    maximo = np.max(datos)
    minimo = np.min(datos)
    promedio = np.mean(datos)
    varianza = np.var(datos)
    desvest = np.std(datos)

    # DataFrames
    nDatos.append(n)
    maximoDatos.append(maximo)
    minimoDatos.append(minimo)
    promedioDatos.append(promedio)
    varianzaDatos.append(varianza)
    desvestDatos.append(desvest)
    nombreDatos.append(name)

final = {
    "ESTACION":nombreDatos,
    "X":coordenadasX,
    "Y":coordenadasY,
    "CANT_DATOS":nDatos,
    "MAX":maximoDatos,
    "MIN":minimoDatos,
    "PROMEDIO":promedioDatos,
    "VARIANZA":varianzaDatos,
    "DESVEST":desvestDatos,
}

dfFinal = pd.DataFrame(final)
dfFinal.to_csv(f"{mesAnalisis}_DIRVIENTO.csv",index=False) #cambiar nombre para mejor soriganziación