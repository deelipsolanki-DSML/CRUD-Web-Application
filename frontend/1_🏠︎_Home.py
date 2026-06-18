import streamlit as st
import requests as req

st.title("🌐 Web Database", text_alignment = 'center')
st.divider()

try:
    response = req.get('http://127.0.0.1:8000')
    st.write(f"status code: ", response.status_code)
    st.write(f"<h2 style='text-align: center;'>{response.json()['message']}</h2>", unsafe_allow_html = True)
    st.space("small")
    st.subheader("🔗 Links")
    # 1. Link to an internal login page 
    st.page_link("pages/1_👤_Login.py", label="Login to your existing account", icon="👤")

    # 2. Link to an internal create account page
    st.page_link("pages/2_✚_Create Account.py", label="Create new account", icon="➕")
    # 3. Link to an update page
    st.page_link("pages/3_⚙️_Update Account.py", label="Update account info", icon="⚙️")

    # 4. Link to an delete page
    st.page_link("pages/4_🗑️_Delete Account.py", label="Delete account", icon="🗑️")

except Exception as e:
    st.write(f"<h5 style='text-align: center; color: red;'>⚠️ {type(e).__name__}: {e}</h5>", unsafe_allow_html = True)