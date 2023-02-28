import streamlit as st
import falcon
import time
import dill
import pickle
from pathlib import Path 
import os
# st.set_page_config(page_title="Tạo khoá", page_icon="🔑")
# st.markdown("# Sinh khoá cho ký số Falcon")
# st.sidebar.header("Sinh khoá")

# # st.header("Nhập độ dài khoá:")

# # n = int(st.text_input("Nhập độ dài khoá:",placeholder = "Bạn chưa nhập thông điệp",label_visibility="hidden"))
# #st.line_chart('loss.pkl')
# n = st.selectbox(
# 'Chọn độ dài của khoá',
# (128, 256, 512, 1024))
# if n:
start = time.time()
sk = falcon.SecretKey(1024)
pk = falcon.PublicKey(sk)
timeky= (time.time() - start)
print("Thời gian tạo khoá là (s):")
print(timeky)
print(sk)
#     with open( "FalconPriv.pem", 'wb') as privFile:
#                 dill.dump(sk, privFile)
#     st.write('Kích thước khoá bí mật là (kb): ',os.stat("FalconPriv.pem").st_size/1024)
#     with open('FalconPriv.pem', mode='rb') as file:
#             btn = st.download_button(label='Tải khoá bí mật',
#                                         data=file,
#                                         file_name='FalconPriv.pem')

#     with open("FalconPub.pub", 'wb') as pubFile:
#                 dill.dump(pk, pubFile)
#     st.write("Kích thước khoá công khai là (kb): ",os.stat("FalconPub.pub").st_size/1024)
#     with open('FalconPub.pub', mode='rb') as file:
#             btn = st.download_button(label='Tải khoá công khai',
#                                         data=file,
#                                         file_name='FalconPub.pub')
# progress_bar = st.sidebar.progress(0)
# status_text = st.sidebar.empty()
# status_text.text("Hoàn thành việc sinh khoá")
# progress_bar.empty()


