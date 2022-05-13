import this
import numpy as np
import nltk as nl
from nltk.stem.lancaster import LancasterStemmer
from regex import E
stemmer = LancasterStemmer()
import json 
import tensorflow as tf
import tflearn as tl
import random 
import pickle

#nl.download('punkt')

with open("Etiquetas.json", encoding='utf-8') as archivo:
    datos = json.load(archivo)

    #Listas para obtener correos de los registros de empleado y alumno
    Alumnos = [{'Nombre':'Luis','Nua':345805, 'Correo': 'jl.gutierrezbecerra@ugto.mx'}, {
        'Nombre':'Eduardo','Nua':345806, 'Correo': 'le.santoyoparamo@ugto.mx'},{ 
        'Nombre':'Roman', 'Nua':345807, 'Correo':'br.lopezcano@ugto.mx'},{ 
        'Nombre':'Adrian', 'Nua':345808, 'Correo':'ad.lopezgarcia@ugto.mx'},{ 
        'Nombre':'Mariana', 'Nua':345809, 'Correo':'me.garciahernandez@ugto.mx'},{ 
        'Nombre':'Jimena', 'Nua':345810, 'Correo':'pj.renteriamondelo@ugto.mx'}]

    Empleados = [{'Nombre':'Enrique','Nue':475801, 'Correo': 'ae.martinezhernandez@ugto.mx'},{
        'Nombre':'Jorge','Nue':475802, 'Correo': 'ja.torresmejia@ugto.mx'},{
        'Nombre':'Monica','Nue':475803, 'Correo': 'mm.villasenior@ugto.mx'},{
        'Nombre':'Martha','Nue':475804, 'Correo': 'mp.andradevillas@ugto.mx'},{
        'Nombre':'Andrea','Nue':475805, 'Correo': 'ma.diazmedrano@ugto.mx'},{
        'Nombre':'Daniel','Nue':475806, 'Correo': 'da.gutierrezvalderrama@ugto.mx'}]

#Si es la primera vez se crea todo el modelo, sino solamente se carga 
try:
    with open("modelo2.pickle", "rb") as archivoModelo:
        palabras, tags, entrenamiento, salida = pickle.load(archivoModelo)
except:
    palabras = []
    tags = []
    auxX = []
    auxY = []

    for contenido in datos["Etiquetas"]:
        for patrones in contenido["patrones"]:
            auxpalabra = nl.word_tokenize(patrones)
            palabras.extend(auxpalabra)
            auxX.append(auxpalabra)
            auxY.append(contenido["tag"])

            if contenido["tag"] not in tags:
                tags.append(contenido["tag"])

    #NOTE: SOBRECARGA DE CAST STR NECESARIO
    palabras = [stemmer.stem(str(p).lower()) for p in palabras] 
    palabras = sorted(list(set(palabras)))
    tags = sorted(tags)

    entrenamiento = []
    salida = []
    salidaVacia = [0 for _ in range(len(tags))]

    #NOTE: ALGORITMO DE LA CUBETA PARA CLASIFICAR PALABRAS 
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

    entrenamiento = np.array(entrenamiento)
    salida = np.array(salida)

    with open("modelo2.pickle", "wb") as archivoModelo:
        pickle.dump((palabras, tags, entrenamiento, salida), archivoModelo)

tf.compat.v1.reset_default_graph() #Se pone en blaco la red 

#Creacion de la red (reciben entrada, predicen, catalogan)
red = tl.input_data(shape=[None, len(entrenamiento[0])])
red = tl.fully_connected(red, 13)
red = tl.fully_connected(red, 13)
red = tl.fully_connected(red, len(salida[0]), activation="softmax")
red = tl.regression(red)

modelo = tl.DNN(red)

#se carga el modelo de entrenamiento en caso de existir, sino, se crea 
"""try:
    modelo.load("modelo2.chat")
except:"""
modelo.fit(entrenamiento, salida, n_epoch=1000, batch_size=12, show_metric=True)
modelo.save("modelo2.chat")

#Funcion para obtener el correo solicitado
def get_user_email(user_profile, user_number, debug=False): 
    if debug: print("get_user_email > " + user_profile + ", " + str(user_number))
    if user_profile == "empleado":
        for  Empleado in Empleados:
            if user_number == Empleado['Nue']:
                print("Su correo es:\t", Empleado['Correo'])  
            else:
                print("Datos erroneos, verifica e intentalo de nuevo")
                
    elif user_profile == "alumno":
        for Alumno in Alumnos:
            if user_number == Alumno['Nua']:
                print("Su correo es:\t", Alumno['Correo'])
            else:
                print("Datos erroneos, verifica e intentalo de nuevo")
               
#Funcion para recuperar contraseña olvidada
def get_password(user_profile, user_id):
    if user_profile == "empleado":
        for Empleado in Empleados:
            if user_id == Empleado['Nue']:
                send_password_email(Empleado['Correo'])
    if user_profile == "alumno":
        for Alumno in Alumnos:
            if user_id == Alumno['Nua']:
                send_password_email(Alumno['Correo'])
               
#Funcion para enviar contraseña temporal por correo
def send_password_email(user_email):
    print("Se envio una contraseña temporal a su correo registrado: ", user_email)

#Funcion principal del bot
def botInit():
    print("Bot: Hola soy tu asistente en linea, ¿que puedo hacer por ti?")
    while True:
        try:
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

            #Si detecta que el tag solicita le recuperacion de correo se manda llamar a la funcion
            if tag == 'correo':
                #user_profile = input("Bot: Eres alumno o empleado\t")
                print("Bot: Eres alumno o empleado\t")
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

                for idaux in datos["Etiquetas"]:
                    if idaux["tag"] == tag:
                        user_profile = tag
                        user_number = int(input("Bot: Ingresa tu identificador\t"))

                get_user_email(user_profile, user_number, True)
            
            elif tag == 'password':#Recuperar contraseña
                print("Bot: Eres alumno o empleado\t")
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

                for idaux in datos["Etiquetas"]:
                    if idaux["tag"] == tag:
                        user_profile = tag
                        user_number = int(input("Bot: Ingresa tu identificador\t"))

                get_password(user_profile, user_number)

            else:
                for tagAux in datos["Etiquetas"]:
                    if tagAux["tag"] == tag:
                        respuesta = tagAux["respuesta"]
                #Se elige una respuesta al azar según el patron que detecta 
                print("Bot: ", random.choice(respuesta))
                #Finalizacion del programa

            if tag == 'despedida':
                break
            
        except:
            print("Bot: Disculpa, no entiendo lo que necesitas")
botInit()