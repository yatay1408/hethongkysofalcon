import streamlit as st
import falcon
import time
import dill
import yaml
import streamlit_authenticator as stauth
#from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
import sys
from audio_recorder_streamlit import audio_recorder
import os
st.set_page_config(
    page_title="Ký số nội dung giọng nói",
    page_icon="🎤",
)
#tải file băm mật khẩu
with open('config.yaml', 'r') as file:
    config = yaml.load(file, Loader=yaml.SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login("Login", "main")
if authentication_status == False:
    st.error("Bạn đã nhập sai mật khẩu hoặc tên người dùng")

if authentication_status == None:
    st.warning("Bạn chưa nhập mật khẩu hoặc tên người dùng")

if authentication_status:
    st.write(f"# {name} đang sử dụng dịch vụ")
    #load khoá
    with open('key.yaml', 'r') as file:
        key = yaml.load(file, Loader=yaml.SafeLoader)
    f = key[name]['f']
    g = key[name]['g']
    F = key[name]['F']
    G = key[name]['G']
    sk = falcon.SecretKey(1024,[f,g,F,G])
    pk = falcon.PublicKey(sk)
    #xác thực
    st.header("Chọn chữ ký số")
    chuky = st.file_uploader("**Chọn chữ ký số**", label_visibility="collapsed")

    if chuky is not None:
        sigauth = dill.load(chuky)
    #Ký số giọng nói
    audio_bytes = audio_recorder()
    if audio_bytes:
            with open('myfile.wav', mode='bx') as f:
             f.write(audio_bytes)
            # display audio data as received on the backend
            r = sr.Recognizer()
            audiowav=sr.AudioFile('myfile.wav')
            with audiowav as source:
             audio = r.record(audiowav)
             text = r.recognize_google(audio, language= "vi-VN")

            if (len(sys.argv)>1):
                    text=str(sys.argv[1])
            os.remove('myfile.wav')
            start = time.time()
            xacthuc = pk.verify(text.encode('UTF-8'), sigauth)
            timexacthuc= (time.time() - start)
            st.header("Thời gian xác thực là (s):")
            st.code(timexacthuc)
            st.header("Kết quả xác thực là:")
            st.code(xacthuc)
            if xacthuc == 'Xác thực thành công': st.sidebar.success("Xác thực thành công") 
            else: 
                st.sidebar.error("Xác thực thất bại")
    authenticator.logout('Thoát', 'main')