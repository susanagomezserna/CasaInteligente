import os
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image
import time
import glob
import paho.mqtt.client as paho
import json
from gtts import gTTS
from googletrans import Translator

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
client1= paho.Client("SGS1")
client1.on_message = on_message

title_alignment=
"""
<style>
#the-title {
  text-align: center
}
</style>
"""
st.markdown(title_alignment, unsafe_allow_html=True)

st.title("Casa Inteligente")
st.subheader("Control por *voz*")

image = Image.open('voice_ctrl.png')

st.image(image, width=200)

st.divider()


st.subheader("Toca el Botón y dale instrucciones")
col1, col2 = st.columns(2)
with col1: 
    image = Image.open('bombillo.png')

    st.image(image, width=100)
    st.write("Para encender y apagar las luces: *Turn on/Turn off*")

with col2:  
    image = Image.open('door2.png')

    st.image(image, width=100)
    st.write("Para abrir y cerrar la puerta: *Open/Close*")

stt_button = Button(label=" Inicio ", width=200)

stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
 
    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }
        }
        if ( value != "") {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    }
    recognition.start();
    """))

result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0)

if result:
    if "GET_TEXT" in result:
        st.write(result.get("GET_TEXT"))
        client1.on_publish = on_publish                            
        client1.connect(broker,port)  
        message =json.dumps({"Act1":result.get("GET_TEXT").strip()})
        ret= client1.publish("VozSGS", message)

    
    try:
        os.mkdir("temp")
    except:
        pass
