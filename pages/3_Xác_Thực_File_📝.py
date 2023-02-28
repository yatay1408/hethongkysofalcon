import streamlit as st
import falcon
import time
import dill
import yaml
import streamlit_authenticator as stauth

st.set_page_config(
    page_title="Xác thực File",
    page_icon="✅",
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
    #load khoá
    st.write(f"# {name} đang sử dụng dịch vụ")
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
        
        st.header("Chọn file xác thực")
        dulieuauth = st.file_uploader("**Tải file cần xác thực**", label_visibility="collapsed")
        if dulieuauth:
                start = time.time()
                xacthuc = pk.verify(dulieuauth.getvalue(), sigauth)
                timexacthuc= (time.time() - start)
                st.header("Thời gian xác thực là (s):")
                st.code(timexacthuc)
                st.header("Kết quả xác thực là:")
                st.code(xacthuc)
                if xacthuc == 'Xác thực thành công': st.sidebar.success("Xác thực thành công") 
                else: 
                    st.sidebar.error("Xác thực thất bại")
    authenticator.logout('Thoát', 'main')
