import streamlit as st
import falcon
import time
import dill
import yaml
import streamlit_authenticator as stauth

st.set_page_config(
    page_title="Ký số",
    page_icon="📝",
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

    #ký số
    st.header(f"**Chọn file cần ký số**")
    dulieu = st.file_uploader("**File ký**", label_visibility="collapsed")
    if dulieu is not None:
        start = time.time()
        sig = sk.sign(dulieu.getvalue())
        timeky= (time.time() - start)
        st.header("Chữ ký số là:")
        st.code(str(sig.hex()))
        st.header("Thời gian ký số là (s):")
        st.code(timeky)
        st.sidebar.success("Ký số hoàn thành")
        with open("chukyfalcon.sig", 'wb') as opFile:
                dill.dump(sig, opFile)
        with open('chukyfalcon.sig', mode='rb') as file:
            btn = st.download_button(label='Tải chữ ký',
                                        data=file,
                                        file_name='chukyfalcon.sig')
    authenticator.logout('Thoát', 'main')
   