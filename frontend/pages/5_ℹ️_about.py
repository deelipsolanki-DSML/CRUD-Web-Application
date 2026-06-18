import streamlit as st

st.title("About this website")
st.space("small")

st.write('''##### This interface has been build using streamlit, and the API that performs CRUD operations on sqlite3 database in backend is built using FastAPI.
         
         Here you can:

         📌 create your account
         📌 login using your id and password
         📌 update your info
         📌 delete your account
         ''')
