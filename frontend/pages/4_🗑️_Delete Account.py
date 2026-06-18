import streamlit as st
import requests as req
import pandas as pd


st.title("Delete account", text_alignment='center')
st.divider()

if st.session_state.get("login", False):

    data_dict = st.session_state.data

    df = pd.DataFrame(
        [data_dict],
        columns=["ID", "Password", "Name", "Email", "DOB", "Balance ($)", "Age"]
    )

    st.table(df.style.format({"Balance ($)": "{:,}"}))

    st.warning("this data will be deleted permanently")
    st.divider()

    st.write("<h4>Confirm Deletion</h4>",unsafe_allow_html = True)
    st.write("⚠️ This action will delete your account immidiately")
    but_del = st.button("Delete", icon="🗑️")
    st.space("small")

    if but_del:
     
        try:
            resp2 = req.delete('http://127.0.0.1:8000/delete', json = st.session_state.payload)

            if resp2.status_code == 200:
                st.success("Account deleted successfully !")
                st.session_state.login = False
                
            elif resp2.status_code == 404:
                st.subheader(f"status code: {resp2.status_code}", text_alignment='center')
                st.write(f"<h4 style='text-align: center; color: red;'> {resp2.json()['detail']} </h4", unsafe_allow_html=True)
            else:
                st.write(f"<h4 style='text-align: center; color: red;'> {resp2.json()['detail'][0]['loc'][1]}: {resp2.json()['detail'][0]['msg']} </h4", unsafe_allow_html=True)

        except Exception as e:
            st.write(f"<h5 style='text-align: center; color: red;'>{type(e).__name__}: {e}</h5>", unsafe_allow_html = True)

else:
    st.write(f"<h4 style='text-align: center; color: DodgerBlue;'>login to your account first</h4", unsafe_allow_html=True)