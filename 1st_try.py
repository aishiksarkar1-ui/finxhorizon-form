import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import json

# --- Page Setup ---
st.title("Welcome to FINXHORIZON")
st.write("---")

# Name Input
name = st.text_input("Hello Sir/Madam, may I know your full name?")

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
