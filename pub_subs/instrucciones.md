# Guia de uso

## 1. Ejecutar el *broker*
Abre una terminal (*cmd*)
~~~bash
python broker.py
~~~

Se mostrara como resultado:

~~~bash
[BROKER] Escuchando en 0.0.0.0:14000
~~~

## 2. Ejecutar uno o mas suscriptores
Abre una terminal y ejecuta un suscriptor o mas
~~~bash
python subscriber.py
~~~

Caundo se te pida , escribe el tema (*topc*), por ejemplo
~~~
El sistema mantendra la conexion abierta esperando mensajes del *Broker*
~~~

## Ejecuta una o mas publicaciones

En otra terminal
~~~bash
python publisher.py
~~~
Envia un mensaje en este formato:

~~~bash
deportes: ¡El america gano 15-0!
~~~

Todos los *suscriptores* suscritos a *deportes* recibiran:
~~~bash
[deportes] ¡El pumas gano 5-0!
~~~
