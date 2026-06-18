from time import strftime
import streamlit as st
import requests as req

st.title("Create New Account", text_alignment='center')
st.divider()

if not st.session_state.get("login", False):
    col1, col2 = st.columns(2)

    with col1:
        id = st.text_input("User ID", placeholder="eg. UIDXX", icon = "🪪")  #string
        name = st.text_input("Name", icon="👨🏻‍💼") #string 
        mail_id = st.text_input("E-mail ID", placeholder="example@email.com", icon="✉") #string
    with col2:
        dob = st.date_input("Date of birth 📆", min_value="1950-01-01")  #datetime.date
        balance = st.number_input("Balance", icon = "💲")  #float 0.0
        pwd = st.text_input("Password", icon="🔑")  #string

    l = [id, pwd, name, mail_id]
    missing = [1 for x in l if not x]  #check if any detail is missing
    
    st.space("small")
    but = st.button("Submit", icon="📝")  #submit button

    if but:  #after submit button is pressed
        st.info("details submitted", width=300)
        st.space("small")
        payload = {
            "id": id,
            "pwd": pwd,
            "name": name,
            "mail_id": mail_id,
            "balance": balance,
            "dob": dob.strftime("%Y-%m-%d")
                    }
        if missing:  #catch empty fields
            st.write(f"<h4 style='text-align: center; color: red;'>one or more detail(s) is missing</h4", unsafe_allow_html=True)

        else:      
            try:
                response = req.post('http://127.0.0.1:8000/add_user', json = payload)  #fetch api
                    
                if response.status_code == 201:
                    st.success(title = "Account created successfully", body = "You can now login using your ID and password")

                elif response.status_code == 409:  #user already exists
                    st.subheader(f"status code: {response.status_code}", text_alignment='center')
                    st.warning(title=f"User ID {id} already exists", body="you can login using your credentials")
                
                else: # unprocessable entry
                    st.write(f"<h4 style='text-align: center; color: red;'> {response.json()['detail'][0]['loc'][1]}: {response.json()['detail'][0]['msg']} </h4", unsafe_allow_html=True)
    

            except Exception as e:
                st.write(f"<h5 style='text-align: center; color: red;'>{type(e).__name__}: {e}</h5>", unsafe_allow_html = True)

else:
    st.space("medium")
    st.write(f"<h5 style='text-align: center; color: DodgerBlue;'>Log out to create a new account</h5>", unsafe_allow_html = True)