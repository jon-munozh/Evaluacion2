Evaluación N.º 2 — GraphHopper API REST
Integrantes: Jonathan Munoz y Daniel Bustamante
Asignatura: Telepresencia y Entornos de Colaboración Humana
Descripción

Este proyecto consiste en un programa desarrollado en Python que utiliza la API REST de GraphHopper para calcular rutas entre diferentes ubicaciones geográficas.

El programa permite consultar recorridos según el medio de transporte seleccionado y obtener información sobre distancias, duración estimada e instrucciones de navegación.

Funcionalidades
Selección del medio de transporte: automóvil, bicicleta o a pie.

Ingreso de ciudad de origen y destino.

Consulta de coordenadas geográficas mediante la API de GraphHopper.

Cálculo de distancias en kilómetros y millas con dos decimales.

Visualización del tiempo estimado del viaje.

Instrucciones de navegación paso a paso en español.

Finalización del programa mediante s o salir.

Tecnologías utilizadas
Python 3

Librería Requests

API REST GraphHopper

Visual Studio Code

Git y GitHub

Máquina virtual DEVASC

Ejecución
Instalar Python 3 y la librería requests.

Obtener una API Key desde GraphHopper.

Ejecutar el programa mediante el comando:

python3 graphhopper_evaluacion2.py

Ingresar la API Key cuando sea solicitada.

Seleccionar el medio de transporte.

Ingresar origen y destino para consultar la ruta.

Seguridad
La API Key no está incorporada directamente en el código fuente. El programa la solicita al ejecutarse para evitar publicar credenciales privadas en GitHub.

Resultado
Se realizó una prueba de cálculo de ruta entre Washington, D.C. y Baltimore, Maryland, obteniendo instrucciones de navegación en español, distancias con dos decimales y la posibilidad de terminar correctamente el programa.
