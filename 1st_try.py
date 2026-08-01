import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# --- Page Setup ---
st.title("Welcome to FINXHORIZON")
st.write("---")

# Name Input
name = st.text_input("Hello Sir/Madam, may I know your full name?")

# Submit Button
if st.button("Submit Form"):
    if name:
        try:
            # 1. API-এর সাথে কানেক্ট করা
            scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
            
            # নিচে 'secret_key.json' এর জায়গায় আপনার ডাউনলোড করা আসল json ফাইলটির নাম দিন
            creds = Credentials.from_service_account_file("finxhorizon-form-ec743c08434a.json", scopes=scope)
            client = gspread.authorize(creds)
            
            # 2. গুগল শিট ওপেন করা (আপনার শিটের নাম 'Client_Test' না হলে সেটা বদলে দিন)
            sheet = client.open("Client_Test").sheet1
            
            # 3. শিটে ডেটা পাঠানো (একটি নতুন Row-তে নাম সেভ হবে)
            sheet.append_row([name])
            
            first_name = name.split()[0]
            st.success(f"Thank You {first_name} Sir, your data is saved in Google Sheets!")
            st.balloons()
            
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Doya kore apnar nam likhun!")