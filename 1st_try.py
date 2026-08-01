import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import json

# CSS ফাইলটি পড়ে ওয়েবসাইটে যুক্ত করার কোড
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- Page Setup ---
st.title("Welcome to FINXHORIZON")
st.write("---")

st.subheader("1. Personal Details")

# Name Input
name = st.text_input("Hello may I know your full name?")

# Gender Input
gender = st.radio("Kindly select your gender",
    ('MALE', 'FEMALE', 'OTHER'), index=None)

if name:
    if grnder == "MALE":
        first_name = name.split()[0]
        st.success(f"Thank You {first_name} Sir, it will pleasure you chose us to help.\nKindly fill the form to proced further")

    elif grnder == "FEMALE":
        first_name = name.split()[0]
        st.success(f"Thank You {first_name} Mam, it will pleasure you chose us to help.\nKindly fill the form to proced further.") 

    else:
        first_name = name.split()[0]
        st.success(f"Thank You {first_name} , it will pleasure you chose us to help.\nKindly fill the form to proced further.") 

    phone = st.text_input("2) Phone Number:")

# ৩. ইমেইল
    email = st.text_input("3) Email Address:")


    age = st.selectbox("5) Age:", [None] + list(range(18, 101)), format_func=lambda x: "Select age" if x is None else str(x))

    # ৬. পেশা
    profession = st.radio(
        "6) Profession:",
        ('Business', 'Service(Govt. / Pvt.)', 'Self Employed', 'Non Earning member'),
        index=None
    )
    
    # ৭. মাসিক আয় (পেশার ওপর ভিত্তি করে ডাইনামিক)
    income = st.number_input("7) What is your approximate monthly income?", min_value=0, step=1000)
    # ৮. মাসিক খরচ
    expense = st.number_input("8) What is your approximate monthly household expense?", min_value=0, step=1000)

    # ৯. বিবাহিত কি না
    married = st.radio("9) Are you married?", ('YES', 'NO'), index=None)

# Submit Button
if st.button("Submit Form"):
    if name:
        try:
            # 1. API-এর সাথে কানেক্ট করা (Streamlit Secrets থেকে)
            scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
            
            # JSON ফাইল না খুঁজে সরাসরি Streamlit Secrets থেকে চাবি নেওয়া
            secret_dict = json.loads(st.secrets["google_sheets_secret"])
            creds = Credentials.from_service_account_info(secret_dict, scopes=scope)
            client = gspread.authorize(creds)
            
            # 2. গুগল শিট ওপেন করা 
            sheet = client.open("Client_Test").sheet1
            
            # 3. শিটে ডেটা পাঠানো
            sheet.append_row([name])
            
            first_name = name.split()[0]
            st.success(f"Thank You {first_name} Sir, your data is saved in Google Sheets!")
            st.balloons()
            
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Doya kore apnar nam likhun!")
