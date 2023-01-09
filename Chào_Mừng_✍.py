import streamlit as st
from PIL import Image
import yaml
import streamlit_authenticator as stauth

st.set_page_config(
    page_title="Chào mừng",
    page_icon="✍",
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

    logo = Image.open("hvktmm.png")
    col1, col2, col3 = st.columns(3)
    col2.image(logo, width=250)

    st.write(f"# Chào mừng {name} đến với hệ thống ký số Falcon👋")

    st.sidebar.success("Lựa chọn dịch vụ cần sử dụng")

    st.markdown(
        """
        Đây là một hệ thống ký số trực tuyến được xây dựng dựa trên mã nguồn mở của mật mã hậu lượng tử Falcon.

        **👈 Lựa chọn các dịch vụ từ thanh trượt** để sử dụng các dịch vụ tương ứng.
        ### Tác giả
        - Xây dựng và thiết kế bởi: Quách Đức Huy - H29 - Học viện kỹ thuật mật mã
        - Nếu có thắc mắc gì về hệ thống vui lòng liên lạc qua địa chỉ Email: qdhuy2000gl@gmail.com
    """
    )
 


