import this
import numpy as np
import nltk as nl
from nltk.stem.lancaster import LancasterStemmer
from sympy import false, true
stemmer = LancasterStemmer()
import json 
import tensorflow as tf
import tflearn as tl
import random 
import pickle

#nl.download('punkt')

with open("Etiquetas.json", encoding="utf-8") as archivo:
    datos = json.load(archivo)

palabras = []
tags = []
auxX = []
auxY = []

Alumnos = [{'Nombre':'Luis','Nua':345805, 'Correo': 'jl.gutierrezbecerra@ugto.mx'}, {
    'Nombre':'Luis','Nua':345807, 'Correo': 'le.santoyoparamo@ugto.mx'},{'Nombre':'Andres',
    'Nua':345901, 'Correo':'aa.cardososanchez@ugto.mx'}]

Empleados = [{'Nombre':'Enrique','Nue':475816, 'Correo': 'ae.martinezhernandez@ugto.mx'},{
    'Nombre':'Jorge','Nue':475809, 'Correo': 'ja.torresmejia@ugto.mx'},{'Nombre':'Mario',
    'Nue':475304, 'Correo': 'M.torresaraujo@ugto.mx'}]

for contenido in datos["Etiquetas"]:
    for patrones in contenido["patrones"]:
        auxpalabra = nl.word_tokenize(patrones)
        palabras.extend(auxpalabra)
        auxX.append(auxpalabra)
        auxY.append(contenido["tag"])

        if contenido["tag"] not in tags:
            tags.append(contenido["tag"])

#NOTE: SOBRECARGA DE CAST STR NECESARIO
palabras = [stemmer.stem(str(p).lower()) for p in palabras] #Cast necesario para usar lower
palabras = sorted(list(set(palabras)))
tags = sorted(tags)

entrenamiento = []
salida = []
salidaVacia = [0 for _ in range(len(tags))]

#NOTE: ALGORITMO DE LA CUBETA PARA CLASIFICAR PALABRAS 
#REF: https¨//xyz.com.mx/jlsfksdhfk
for x, documento in enumerate(auxX):
    bucket = []
    auxpalabra = [stemmer.stem(str(p).lower()) for p in documento]
    for p in palabras:
        if p in auxpalabra:
            bucket.append(1)
        else:
            bucket.append(0)
    filaSalida = salidaVacia[:]
    filaSalida[tags.index(auxY[x])]=1
    entrenamiento.append(bucket)
    salida.append(filaSalida)

#TODO 1: FORMATEO DE RESULTADO ...

entrenamiento = np.array(entrenamiento)
salida = np.array(salida)

tf.compat.v1.reset_default_graph() #Se pone en blaco la red 

#Creacion de la red (reciben entrada, predicen, catalogan)
red = tl.input_data(shape=[None, len(entrenamiento[0])])
red = tl.fully_connected(red, 13)
red = tl.fully_connected(red, 13)
red = tl.fully_connected(red, len(salida[0]), activation="softmax")
red = tl.regression(red)

modelo = tl.DNN(red)
modelo.fit(entrenamiento, salida, n_epoch=1000, batch_size=12, show_metric=True)
modelo.save("modelo.chat")

#Funcion para obtener el correo solicitado
def get_user_email(user_profile, user_number):
    if user_profile == "empleado":
        for Empleado in Empleados:
            if user_number == Empleado['Nue']:
                print("Su correo es:\t", Empleado['Correo'])
                break
            else:
                print("Datos erroneos, verifica e intentalo de nuevo")
                break
    elif user_profile == "alumno":
        for Alumno in Alumnos:
            if user_number == Alumno['Nua']:
                print("Su correo es:\t", Alumno['Correo'])
                break
            else:
                print("Datos erroneos, verifica e intentalo de nuevo")
                break

#Funcion de entrada de datos del usuario 
run = true
def botInit():
    while run == true:
        entrada = input("Tú: ")
        bucket = [0 for _ in range(len(palabras))]
        entradap = nl.word_tokenize(entrada)
        entradap = [stemmer.stem(palabra.lower()) for palabra in entradap]
        for palabrasimple in entradap:
            for i, palabra in enumerate(palabras):
                if palabra == palabrasimple:
                    bucket[i] = 1
        resultado = modelo.predict([np.asarray(bucket)])
        resultadosIndex = np.argmax(resultado)
        tag = tags[resultadosIndex]

        if tag == 'correo':
            user_profile = input("Bot: Eres alumno o empleado\t")
            user_profile = user_profile.lower()
            user_number = int(input("Bot: Ingresa tu identificador\t"))

            get_user_email(user_profile, user_number)
        else:
            for tagAux in datos["Etiquetas"]:
                if tagAux["tag"] == tag:
                    respuesta = tagAux["respuesta"]
                #Se elige una respuesta al azar según el patron que detecta 
            print("Bot: ", random.choice(respuesta))
        
        if tag == 'despedida':
            run = false
botInit()