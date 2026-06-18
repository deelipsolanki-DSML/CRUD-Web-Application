from time import strftime
import streamlit as st
import requests as req
import pandas as pd

st.title("Update your account info", text_alignment='center')
st.divider()


if st.session_state.get("login", False):

    data_dict = st.session_state.data

    df = pd.DataFrame(
        [data_dict],
        columns=["ID", "Password", "Name", "Email", "DOB", "Balance ($)", "Age"]
    )

    st.write("<h5>User Details</h5>",unsafe_allow_html = True)
    st.table(df.style.format({"Balance ($)": "{:,}"}))
    st.divider()

    name, mail_id, balance, dob = None, None, None, None  #initialize to all None
    
    st.write("<h4>update fields</h4>",unsafe_allow_html = True)
    cols = st.columns(2)

    with cols[0]:
        n = st.checkbox("Name")
        if n:
            name = st.text_input("Name", value= data_dict[2])  #default name
        eid = st.checkbox("Email ID")
        if eid:
            mail_id = st.text_input("E-mail ID", value= data_dict[3]) #default mail id
    with cols[1]:
        bl = st.checkbox("Balance")
        if bl:
            balance = st.number_input("Balance",value= float(data_dict[5]))  #default balance
        dateofb = st.checkbox("Date of birth")
        if dateofb:
            dob = st.date_input("Date of brith", min_value="1950-01-01", value = data_dict[4])  #default dob

    but_ud = st.button("🗘 Update")
    st.space("small")

    payload2 = {
        "id_pass":st.session_state.payload,
        "up_inp": {
            "name": name,
            "mail_id": mail_id,
            "balance": balance,
            "dob": dob.strftime("%Y-%m-%d") if dob else None
        }
    }
    checkbox_list = [n, eid, bl, dateofb]
    any_update = [True for x in checkbox_list if x != False]  #check if any checkbox ticked for update

    if but_ud and any_update:
        try:
            resp2 = req.put('http://127.0.0.1:8000/update', json = payload2)

            if resp2.status_code == 200:
                st.success("updated successfully !")
                st.session_state.refresh = True  # to refresh login data after update
                
                #get new data and update it for login page
                response_login = req.post('http://127.0.0.1:8000/fetch', json = st.session_state.payload)
                if response_login.status_code == 200:
                    st.session_state.data = response_login.json()['data'][0]
                else:
                    st.session_state.login = False  # logout if cannot fetch updated info
                
            elif resp2.status_code == 404:
                st.subheader(f"status code: {resp2.status_code}", text_alignment='center')
                st.write(f"<h4 style='text-align: center; color: red;'> {resp2.json()['detail']} </h4", unsafe_allow_html=True)
            else:
                st.write(f"<h4 style='text-align: center; color: red;'> {resp2.json()['detail'][0]['loc'][2]}: {resp2.json()['detail'][0]['msg']} </h4", unsafe_allow_html=True)

        except Exception as e:
            st.write(f"<h5 style='text-align: center; color: red;'>{type(e).__name__}: {e}</h5>", unsafe_allow_html = True)


else:
    st.write(f"<h4 style='text-align: center; color: DodgerBlue;'>login to your account first</h4", unsafe_allow_html=True)
