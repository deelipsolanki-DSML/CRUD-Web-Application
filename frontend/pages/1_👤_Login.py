import streamlit as st
import requests as req
import pandas as pd
import time


if not st.session_state.get("login", False):  #if not logged in
    st.title("Login to your account", text_alignment='center')
    st.divider()
    st.write("<h4>Enter your credentials</h4>",unsafe_allow_html = True)
    st.space("small")

    col1, col2 = st.columns(2)
    with col1:
        id = st.text_input("User ID", icon = "🪪")
    with col2:
        pwd = st.text_input("password", icon="🔑")

    but = st.button("login", icon = "👤")

    if but:  #after button is pressed
        payload = {
        "id": id,
        "pwd": pwd
                    }
        
        try:
            response = req.post('http://127.0.0.1:8000/fetch', json = payload)  #fetch api

            if not id or not pwd:  #catch empty string
                st.write(f"<h4 style='text-align: center; color: red;'>please enter your id and password</h4", unsafe_allow_html=True)
                st.session_state.login = False
                
            elif response.status_code == 200:
                st.session_state.login = True
                st.success("login successfull")
                st.session_state.payload = payload
                st.session_state.data = response.json()['data'][0]

            elif response.status_code in [401, 503]:  #incorrect id/pass
                st.session_state.login = False
                st.subheader(f"status code: {response.status_code}", text_alignment='center')
                st.write(f"<h4 style='text-align: center; color: red;'> {response.json()['detail']} </h4", unsafe_allow_html=True)
            

            else:
                st.session_state.login = False
                st.write(f"<h4 style='text-align: center; color: red;'> {response.json()['detail'][0]['loc'][1]}: {response.json()['detail'][0]['msg']} </h4", unsafe_allow_html=True)
    
        except Exception as e:
            st.write(f"<h5 style='text-align: center; color: red;'>{type(e).__name__}: {e}</h5>", unsafe_allow_html = True)

if st.session_state.get("login", False):  #if logged in
    st.space("small")
    st.write(f"<h3 style='text-align: center; color: DodgerBlue;'>Your are logged into your account</h3>", unsafe_allow_html = True)
    st.space("small")
    st.write("Details")
    df = pd.DataFrame([st.session_state.data], columns=["ID", "Password", "Name", "Email", "DOB", "Balance ($)", "Age"])
    st.table(df.style.format({"Balance ($)": "{:,}"}))

    st.space("small")
    if st.button("⏻ **logout**"):
        st.session_state.login = False
        st.warning("Logged out successfully")
        time.sleep(2)
        st.rerun()
