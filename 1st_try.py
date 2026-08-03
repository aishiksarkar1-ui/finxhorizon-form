import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import json

# CSS ফাইলটি পড়ে ওয়েবসাইটে যুক্ত করার কোড
try:
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except:
    pass

# --- Page Setup & Session State Initialization ---
st.title("Welcome to FINXHORIZON")
st.write("---")

# পেজ স্টেপ ট্র্যাক করার জন্য সেশন স্টেট ইনিশিয়ালাইজ করা
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'










# ==========================================
# PAGE 1: Welcome & Basic Info Form
# ==========================================




if st.session_state.page == 'welcome':
    st.subheader("Hello, may I know your full name?")

    # Name Input
    name = st.text_input("NAME:", value=st.session_state.get('name', ''))

    # CONTACT INFORMATION
    phone = st.text_input("Phone Number:", value=st.session_state.get('phone', ''))
    email = st.text_input("Email Address:", value=st.session_state.get('email', ''))

    # Gender Input
    gender = st.radio(
        "Kindly select your gender",
        ('MALE', 'FEMALE', 'OTHER'), 
        index=None if 'gender' not in st.session_state else ('MALE', 'FEMALE', 'OTHER').index(st.session_state.gender)
    )

   

    # লাইভ ওয়েলকাম মেসেজ দেখানোর জন্য চেক
    if name and gender:
        first_name = name.split()[0]
        if gender == "MALE":
            st.success(f"Thank You {first_name} Sir, it is a pleasure to have you. Kindly fill the form to proceed further.")
        elif gender == "FEMALE":
            st.success(f"Thank You {first_name} Mam, it is a pleasure to have you. Kindly fill the form to proceed further.")
        else:
            st.success(f"Thank You {first_name}, it is a pleasure to have you. Kindly fill the form to proceed further.")

    # Go to Form Button & Google Sheet Integration
    if st.button("Go to Form"):
        if name and gender and phone and email:
            try:
                # 1. API-এর সাথে কানেক্ট করা (Streamlit Secrets থেকে)
                scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
                secret_dict = json.loads(st.secrets["google_sheets_secret"])
                creds = Credentials.from_service_account_info(secret_dict, scopes=scope)
                client = gspread.authorize(creds)
                
                # 2. গুগল শিট ওপেন করা 
                sheet = client.open("Client_Test").sheet1
                
                # 3. শিটে ডেটা পাঠানো (নাম, জেন্ডার, ফোন, ইমেল একসাথে একটি সারিতে)
                sheet.append_row([name, gender, phone, email])
                
                # ডেটা সেশন স্টেটে সেভ করে রাখা যাতে পরের পেজেও মনে থাকে
                st.session_state.name = name
                st.session_state.gender = gender
                st.session_state.phone = phone
                st.session_state.email = email

                # পেজ পরিবর্তন করে মূল ফর্মে নিয়ে যাওয়া
                st.session_state.page = 'main_form'
                st.rerun()
                
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Doya kore sokol field thikvabe puron korun!")











# ==========================================
# PAGE 2: Main Form (Personal Information)
# ==========================================







elif st.session_state.page == 'main_form':
    st.subheader("Personal Information")
    
    # আগের তথ্যগুলো রিড-অন হিসেবে বা প্রি-ফিল হিসেবে দেখানো
    st.info(f"**Name:** {st.session_state.name}  \n**Phone:** {st.session_state.phone}  \n**Email:** {st.session_state.email}  \n**Gender:** {st.session_state.gender}")
    
    # ----------------------------------------------------
    # ১. স্ক্রিনশটের মতো ফাংশন তৈরি
    # ----------------------------------------------------
    def switch_tab(tab):
        st.session_state.current_tab = tab

    def on_tab_change():
        # ট্যাব পরিবর্তন হলে এই ফাংশন কাজ করবে (এখানে Toast message দেওয়া যেতে পারে)
        pass

    # ----------------------------------------------------
    # ২. স্ক্রিনশটের হুবহু লজিকে st.tabs তৈরি (on_change এবং key সহ)
    # ----------------------------------------------------
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "Personal Info", 
            "Spouse Details",
            "Child Details",
            "Income & Expenses", 
            "Final Goals"
        ], 
        on_change=on_tab_change, 
        key="current_tab"
    )





    # প্রথম ট্যাব এর ডিজাইন
    #____________________________________

    
    with tab1:
        st.subheader("Personal Information")
        # বয়স ইনপুট
        age = st.selectbox(
            "May I know what age are you?", 
            [None] + list(range(18, 101)), 
            format_func=lambda x: "Select age" if x is None else str(x)
        )
    
        # পেশা ইনপুট
        profession = st.radio(
            "Kindly select your profession:",
            ('Business', 'Service(Govt. / Pvt.)', 'Self Employed', 'Non Earning member'),
            index=None 
        )
    
        # আয় ইনপুট (পেশার ওপর ভিত্তি করে)
        if profession in ["Business", "Self Employed", "Service(Govt. / Pvt.)"]:
            income = st.number_input("What is your approximate monthly income?", min_value=0, step=1000)
        else:
            income = 0
    
        # খরচ ইনপুট
        expenses = st.number_input("What is your approximate monthly household expenses?", min_value=0, step=1000)
    
        # বিবাহিত কি না
        married = st.radio(
            "Are you married?",
            ('YES', 'NO'),
            index=None
        )
    
        # --------------------------------------
        #  Next বাটনে পরের ট্যাব এ যাওয়া
        # --------------------------------------
        if st.button("Next", on_click=switch_tab, args=("Spouse Details",)):
            if age and profession and married and income and expenses:
                st.session_state.age = age
                st.session_state.profession = profession
                st.session_state.income = income
                st.session_state.expenses = expenses
                st.session_state.married = married
                
                st.success("Personal information saved! Moving to the next step...")
            else:
                st.warning("Please fill in all the required details before clicking Next!")



    # 2nd ট্যাব এর ডিজাইন
    #____________________________________
    with tab2:
        st.subheader("Spouse Details")
        
        # যদি বিবাহিত হয়
        if st.session_state.get('married') == 'YES':
            st.info("Information of spouse")

            # নাম ইনপুট (key যুক্ত করা হয়েছে)
            spouse_name = st.text_input("Kindly mention your spouse name:", key="sp_name")
            
            # বয়স ইনপুট
            spouse_age = st.selectbox(
                "May I know what is the age of your spouse?", 
                [None] + list(range(18, 101)), 
                format_func=lambda x: "Select age" if x is None else str(x),
                key="sp_age"
            )
        
            # পেশা ইনপুট
            spouse_profession = st.radio(
                "Kindly select your spouse's profession:",
                ('Business', 'Service(Govt. / Pvt.)', 'Self Employed', 'Non Earning member'),
                index=None,
                key="sp_prof"
            )
        
            # আয় ইনপুট (পেশার ওপর ভিত্তি করে)
            if spouse_profession in ["Business", "Self Employed", "Service(Govt. / Pvt.)"]:
                spouse_income = st.number_input("What is your spouse's approximate monthly income?", min_value=0, step=1000, key="sp_inc")
            else:
                spouse_income = 0
        
            # খরচ ইনপুট
            spouse_expenses = st.number_input("What is your spouse's approximate monthly household expenses?", min_value=0, step=1000, key="sp_exp")
        
            # সন্তান আছে কি না
            child = st.radio(
                "Do you have children?",
                ('YES', 'NO'),
                index=None,
                key="sp_child"
            )
       
            # ----------------------------------------------------
            # Next বাটনে Child Details ট্যাবে যাওয়ার ব্যবস্থা
            # ----------------------------------------------------
            if st.button("Next", key="btn_tab2_next", on_click=switch_tab, args=("Child Details",)):
                if spouse_name and spouse_age and spouse_profession and child:
                    # ডেটাগুলো মেমোরিতে সেভ করা হচ্ছে
                    st.session_state.spouse_name = spouse_name
                    st.session_state.spouse_age = spouse_age
                    st.session_state.spouse_profession = spouse_profession
                    st.session_state.spouse_income = spouse_income
                    st.session_state.spouse_expenses = spouse_expenses
                    st.session_state.child = child
                    
                    st.success("Spouse information saved! Moving to the next step...")
                else:
                    st.warning("Please fill in all the required details before clicking Next!")
        
        # যদি অবিবাহিত হয়
        elif st.session_state.get('married') == 'NO':
            st.info("Since you are unmarried, this section is not applicable.")
            # অবিবাহিত হলে স্পাউস এবং চাইল্ড সেকশন স্কিপ করে সরাসরি ইনকাম পেজে চলে যাবে
            if st.button("Skip to Income & Expenses", key="btn_tab2_skip", on_click=switch_tab, args=("Income & Expenses",)):
                pass
                
        else:
            st.warning("Please fill the Personal Info tab first.")


    # 3rd ট্যাব এর ডিজাইন
    #____________________________________
    with tab3:
        st.subheader("Child Details")
        
        if st.session_state.get('child') == 'YES':
            st.write("Child information form will go here...")
            
            # এখানে আপাতত টেস্ট করার জন্য একটি নেক্সট বাটন দেওয়া হলো
            if st.button("Next", key="btn_tab3_next", on_click=switch_tab, args=("Income & Expenses",)):
                pass
                
        elif st.session_state.get('child') == 'NO':
            st.info("Since you do not have children, this section is not applicable.")
            if st.button("Skip to Next Step", key="btn_tab3_skip", on_click=switch_tab, args=("Income & Expenses",)):
                pass
                
        elif st.session_state.get('married') == 'NO':
             st.info("Since you are unmarried, this section is not applicable.")
             
        else:
            st.warning("Please fill the Spouse Details tab first.")
   
    
