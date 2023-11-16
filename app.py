import paho.mqtt.client as paho
import time
import streamlit as st
import json
values = 0.0
act1="OFF"

def on_publish(client,userdata,result):             #create function for callback
    print("el dato ha sido publicado \n")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received=str(message.payload.decode("utf-8"))
    st.write(message_received)

        


broker="broker.mqttdashboard.com"
port=1883
client1= paho.Client("SGS")
client1.on_message = on_message



st.title("Casa Inteligente")
st.subheader("Control manual")
st.write('')
st.subheader("Presiona ON/OFF para encender o apagar las luces de tu casa.")

if st.button('ON'):
    act1="ON"
    client1= paho.Client("SGS")                           
    client1.on_publish = on_publish                          
    client1.connect(broker,port)  
    message =json.dumps({"Act1":act1})
    ret= client1.publish("LucesSGS", message)
 
    #client1.subscribe("Sensores")
    
    
else:
    st.write('')

if st.button('OFF'):
    act1="OFF"
    client1= paho.Client("SGS")                           
    client1.on_publish = on_publish                          
    client1.connect(broker,port)  
    message =json.dumps({"Act1":act1})
    ret= client1.publish("LucesSGS", message)
  
    
else:
    st.write('')

st.subheader("Desliza para abrir o cerrar tu puerta.")

values = st.slider('',0.0, 100.0)
st.write('Apertura:', values)

if st.button('Ejecutar acción'):
    client1= paho.Client("SGS")                           
    client1.on_publish = on_publish                          
    client1.connect(broker,port)   
    message =json.dumps({"Analog": float(values)})
    ret= client1.publish("PuertaSGS", message)
    
 
else:
    st.write('')
