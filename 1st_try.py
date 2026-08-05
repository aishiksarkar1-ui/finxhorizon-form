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
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        [
            "Personal Info", 
            "Spouse Details",
            "Child Details",
            "Dependent Member",
            "Future Expenses Projection", 
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
            format_func=lambda x: "Select age" if x is None else str(x),
            key="p_age"
        )
    
        # পেশা ইনপুট
        profession = st.radio(
            "Kindly select your profession:",
            ('Business', 'Service(Govt. / Pvt.)', 'Self Employed', 'Non Earning member'),
            index=None,
            key="p_prof"
        )
    
        # আয় ইনপুট (পেশার ওপর ভিত্তি করে)
        if profession in ["Business", "Self Employed", "Service(Govt. / Pvt.)"]:
            income = st.number_input("What is your approximate monthly income?", min_value=0, step=1000, key="p_inc")
        else:
            income = 0
    
        # খরচ ইনপুট
        expenses = st.number_input("What is your approximate monthly household expenses?", min_value=0, step=1000, key="p_exp")
    
        # বিবাহিত কি না
        married = st.radio(
            "Are you married?",
            ('YES', 'NO'),
            index=None,
            key="p_married"
        )

        # --- ভ্যালিডেশন লজিক (Smart Disabled Button) ---
        # চেক করা হচ্ছে: বয়স, পেশা এবং বিবাহিত কি না এই ৩টি ফিল্ড সিলেক্ট করা হয়েছে কি না
        is_valid = bool((age is not None) and (profession is not None) and (married is not None))
        
        # সব ফিলাপ না হলে ওয়ার্নিং মেসেজ দেখাবে
        if not is_valid:
            st.warning("⚠️ Please fill in your age, profession, and marital status to enable the Next button.")
    
        # --------------------------------------
        #  Next বাটনে পরের ট্যাব এ যাওয়া
        # --------------------------------------
        # disabled=not is_valid এর কারণে ফর্ম সম্পূর্ণ না হলে বাটন কাজ করবে না
        if st.button("Next", key="btn_tab1_next", disabled=not is_valid, on_click=switch_tab, args=("Spouse Details",)):
            # ডেটাগুলো মেমোরিতে সেভ করা হচ্ছে
            st.session_state.age = age
            st.session_state.profession = profession
            st.session_state.income = income
            st.session_state.expenses = expenses
            st.session_state.married = married
            
            st.success("Personal information saved! Moving to the next step...")


    



   # 2nd ট্যাব এর ডিজাইন
    #____________________________________



    
    with tab2:
        st.subheader("Spouse Details")
        
        # যদি বিবাহিত হয়
        if st.session_state.get('married') == 'YES':
            st.info("Information of spouse")

            # নাম ইনপুট
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

            # --- ভ্যালিডেশন লজিক (Smart Disabled Button) ---
            # চেক করা হচ্ছে: নাম ফাঁকা নয়, বয়স সিলেক্ট করা হয়েছে, পেশা সিলেক্ট করা হয়েছে এবং সন্তান আছে কি না জানানো হয়েছে।
            is_valid = bool(spouse_name and (spouse_age is not None) and (spouse_profession is not None) and (child is not None))
            
            # সব ফিলাপ না হলে ওয়ার্নিং মেসেজ দেখাবে
            if not is_valid:
                st.warning("⚠️ Please fill in all spouse details to enable the Next button.")
       
            # ----------------------------------------------------
            # Next বাটনে Child Details ট্যাবে যাওয়ার ব্যবস্থা
            # ----------------------------------------------------
            # disabled=not is_valid এর কারণে ফর্ম সম্পূর্ণ না হলে বাটন কাজ করবে না
            if st.button("Next", key="btn_tab2_next", disabled=not is_valid, on_click=switch_tab, args=("Child Details",)):
                # ডেটাগুলো মেমোরিতে সেভ করা হচ্ছে
                st.session_state.spouse_name = spouse_name
                st.session_state.spouse_age = spouse_age
                st.session_state.spouse_profession = spouse_profession
                st.session_state.spouse_income = spouse_income
                st.session_state.spouse_expenses = spouse_expenses
                st.session_state.child = child
                
                st.success("Spouse information saved! Moving to the next step...")
        
        # যদি অবিবাহিত হয়
        elif st.session_state.get('married') == 'NO':
            st.info("Since you are unmarried, this section is not applicable.")
            # অবিবাহিত হলে স্পাউস সেকশন স্কিপ করে সরাসরি Child Details পেজে চলে যাবে
            if st.button("Skip to Next Step", key="btn_tab2_skip", on_click=switch_tab, args=("Child Details",)):
                pass
                
        else:
            st.warning("Please fill the Personal Info tab first.")



    


  # 3rd ট্যাব এর ডিজাইন
    #____________________________________



    
   
    with tab3:
        st.subheader("Child & Dependent Details")
        
        # --- ১. বাচ্চাদের তথ্যের অংশ ---
        if st.session_state.get('child') == 'YES':
            # কতজন সন্তান সেটা জানার ইনপুট
            num_children = st.number_input("How many children do you have?", min_value=1, max_value=10, step=1, key="num_child")
            children_data = []
            
            st.write("---")
            # লুপ চালিয়ে ডাইনামিক টেবিল/কলাম তৈরি করা
            for i in range(num_children):
                st.markdown(f"**Child {i+1} Details:**")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    c_name = st.text_input("Name", key=f"c_name_{i}")
                with col2:
                    c_gender = st.selectbox("Gender", ['MALE', 'FEMALE', 'OTHER'], index=None, key=f"c_gender_{i}")
                with col3:
                    c_age = st.selectbox("Age", [None] + list(range(0, 51)), format_func=lambda x: "Select age" if x is None else f"{x} Years", key=f"c_age_{i}")
                
                children_data.append({"Name": c_name, "Gender": c_gender, "Age": c_age})
                st.write("")
                
        elif st.session_state.get('child') == 'NO':
            st.info("Since you do not have children, child details are not applicable.")
            children_data = []
            
        elif st.session_state.get('married') == 'NO':
             st.info("Since you are unmarried, child details are not applicable.")
             children_data = []
             
        else:
             children_data = []
             st.warning("Please fill the Spouse Details tab first.")

        # --- ২. Dependent Member এর প্রশ্ন (সবার জন্য) ---
        st.write("---")
        dependent = st.radio(
            "Do you have any member in your family who is completely dependent on your income?",
            ('YES', 'NO'),
            index=None,
            key="has_dependent"
        )
        
        # --- ৩. Next বাটন এবং ডাইনামিক রুট লজিক ---
        
        # dependent 'YES' হলে 4th ট্যাব (Dependent Member) এ যাবে, নাহলে 5th ট্যাব (Income & Expenses) এ যাবে
        target_tab = "Dependent Member" if dependent == 'YES' else "Future Expenses Projection"
        
        # ভ্যালিডেশন চেক (সব ফিলাপ করা হয়েছে কি না)
        all_filled = True
        if st.session_state.get('child') == 'YES':
            # চেক করছে বাচ্চাদের নাম, জেন্ডার এবং বয়স দেওয়া হয়েছে কি না
            all_filled = all(child["Name"] and child["Gender"] and child["Age"] is not None for child in children_data)
        
        # ফর্ম তখনই valid হবে যখন বাচ্চাদের তথ্য (যদি থাকে) এবং Dependent এর রেডিও বাটন সিলেক্ট করা হবে
        is_valid = all_filled and (dependent is not None)
        
        if not is_valid:
            st.warning("⚠️ Please fill in all details and answer the dependent question to enable the Next button.")

        # স্মার্ট Next বাটন: ফর্ম পূরণ না হওয়া পর্যন্ত বাটনটি disabled (হালকা রঙ) থাকবে
        if st.button("Next", key="btn_tab3_next", disabled=not is_valid, on_click=switch_tab, args=(target_tab,)):
            # ডেটাগুলো মেমোরিতে সেভ করা হচ্ছে
            if st.session_state.get('child') == 'YES':
                st.session_state.children_data = children_data
            st.session_state.dependent = dependent
            
            st.success("Details saved successfully! Moving to the next step...")



# 4th ট্যাব এর ডিজাইন (Dependent Member)
    #____________________________________
    with tab4:
        st.subheader("Dependent Member Details")
        
        # যদি ৩য় ট্যাবে Dependent থাকার কথা 'YES' বলে থাকে
        if st.session_state.get('dependent') == 'YES':
            st.info("Please provide the details of your dependent family members below:")
            
            # কতজন নির্ভরশীল সদস্য সেটা জানার ইনপুট
            num_dependents = st.number_input(
                "HOW MANY DEPENDENT MEMBERS ARE THERE IN YOUR FAMILY?", 
                min_value=1, max_value=10, step=1, key="num_dep"
            )
            
            # ডেটা সেভ রাখার জন্য একটি ফাঁকা লিস্ট
            dependents_data = []
            
            st.write("---") 
            
            # লুপ চালিয়ে ডাইনামিক টেবিল/কলাম তৈরি করা
            for i in range(num_dependents):
                st.markdown(f"**Dependent Member {i+1}:**")
                
                # এবার ৪টি কলাম তৈরি করা হলো (Name, Gender, Age, Relation)
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    d_name = st.text_input("Name", key=f"d_name_{i}")
                
                with col2:
                    d_gender = st.selectbox("Gender", ['MALE', 'FEMALE', 'OTHER'], index=None, key=f"d_gender_{i}")
                
                with col3:
                    # বয়স (০ থেকে ১০০ বছর পর্যন্ত)
                    d_age = st.selectbox(
                        "Age", 
                        [None] + list(range(0, 101)), 
                        format_func=lambda x: "Select age" if x is None else f"{x} Years",
                        key=f"d_age_{i}"
                    )
                    
                with col4:
                    # সম্পর্ক (Relation)
                    d_relation = st.selectbox(
                        "Relation", 
                        ['FATHER', 'MOTHER', 'BROTHER', 'SISTER', 'OTHER'], 
                        index=None, 
                        key=f"d_rel_{i}"
                    )
                
                # ইউজারের দেওয়া ডেটা লিস্টে যোগ করা হচ্ছে
                dependents_data.append({
                    "Name": d_name,
                    "Gender": d_gender,
                    "Age": d_age,
                    "Relation": d_relation
                })
                
                st.write("") # ফর্মের মাঝখানে ফাঁকা জায়গা
            
            # --- ভ্যালিডেশন লজিক (Smart Disabled Button) ---
            # চেক করা হচ্ছে সব সদস্যের নাম, জেন্ডার, বয়স এবং সম্পর্ক দেওয়া হয়েছে কি না
            is_valid = all(dep["Name"] and dep["Gender"] and (dep["Age"] is not None) and dep["Relation"] for dep in dependents_data)
            
            if not is_valid:
                st.warning("⚠️ Please fill in the Name, Gender, Age, and Relation for all dependent members to enable the Next button.")
                
            # ----------------------------------------------------
            # Next বাটনে Income & Expenses ট্যাবে যাওয়ার ব্যবস্থা
            # ----------------------------------------------------
            if st.button("Next", key="btn_tab4_next", disabled=not is_valid, on_click=switch_tab, args=("Future Expenses Projection",)):
                st.session_state.dependents_data = dependents_data
                st.success("Dependent members' details saved successfully! Moving to the next step...")
                
        # যদি ৩য় ট্যাবে Dependent থাকার কথা 'NO' বলে থাকে
        elif st.session_state.get('dependent') == 'NO':
            st.info("Since you do not have any dependent family members, this section is not applicable.")
            if st.button("Skip to Income & Expenses", key="btn_tab4_skip", on_click=switch_tab, args=("Future Expenses Projection",)):
                pass
                
        else:
            st.warning("Please complete the Child & Dependent Details tab first.")






# 5th ট্যাব এর ডিজাইন (Future Expenses Projection & Goal Planning)
    #____________________________________
    with tab5:
        st.subheader("Future Expenses Projection")

        # ১. লোকেশন ইনপুট
        location = st.selectbox(
            "Where do you live?",
            ["Village", "Semi-village", "Small City", "City", "Megacity"],
            index=None,
            key="location_type"
        )

        st.write("---")

        if location:
            # ২. টোটাল মেম্বার ক্যালকুলেশন
            user_count = 1
            spouse_count = 1 if st.session_state.get('married') == 'YES' else 0
            
            child_data = st.session_state.get('children_data', [])
            child_count = len(child_data) if st.session_state.get('child') == 'YES' else 0
            
            dep_data = st.session_state.get('dependents_data', [])
            dep_count = len(dep_data) if st.session_state.get('dependent') == 'YES' else 0

            total_member = user_count + spouse_count + child_count + dep_count

            # ৩. টোটাল এক্সপেন্স ক্যালকুলেশন
            user_exp = st.session_state.get('expenses', 0)
            spouse_exp = st.session_state.get('spouse_expenses', 0)
            total_expense = user_exp + spouse_exp

            # 4. Expense Per Head
            exp_per_head = total_expense / total_member if total_member > 0 else 0

            # 5. Lifestyle Status Logic
            levels = ["Basic", "Modest", "Standard", "Comfortable", "Upper_Middle class", "Affluent", "Luxury", "Elite"]
            lvl = 0 

            if location == "Village":
                if exp_per_head <= 5000: lvl = 0
                elif exp_per_head <= 10000: lvl = 1
                elif exp_per_head <= 15000: lvl = 2
                elif exp_per_head <= 20000: lvl = 3
                elif exp_per_head <= 30000: lvl = 4
                elif exp_per_head <= 50000: lvl = 5
                elif exp_per_head <= 75000: lvl = 6
                else: lvl = 7
            elif location == "Semi-village":
                if exp_per_head <= 8000: lvl = 0
                elif exp_per_head <= 12000: lvl = 1
                elif exp_per_head <= 20000: lvl = 2
                elif exp_per_head <= 35000: lvl = 3
                elif exp_per_head <= 50000: lvl = 4
                elif exp_per_head <= 75000: lvl = 5
                elif exp_per_head <= 100000: lvl = 6
                else: lvl = 7
            elif location == "Small City":
                if exp_per_head <= 10000: lvl = 0
                elif exp_per_head <= 15000: lvl = 1
                elif exp_per_head <= 22000: lvl = 2
                elif exp_per_head <= 40000: lvl = 3
                elif exp_per_head <= 60000: lvl = 4
                elif exp_per_head <= 100000: lvl = 5
                elif exp_per_head <= 120000: lvl = 6
                else: lvl = 7
            elif location == "City":
                if exp_per_head <= 12000: lvl = 0
                elif exp_per_head <= 18000: lvl = 1
                elif exp_per_head <= 25000: lvl = 2
                elif exp_per_head <= 50000: lvl = 3
                elif exp_per_head <= 80000: lvl = 4
                elif exp_per_head <= 110000: lvl = 5
                elif exp_per_head <= 130000: lvl = 6
                else: lvl = 7
            elif location == "Megacity":
                if exp_per_head <= 15000: lvl = 0
                elif exp_per_head <= 20000: lvl = 1
                elif exp_per_head <= 22000: lvl = 2
                elif exp_per_head <= 30000: lvl = 3
                elif exp_per_head <= 60000: lvl = 4
                elif exp_per_head <= 100000: lvl = 5
                elif exp_per_head <= 150000: lvl = 6
                else: lvl = 7

            style_status = levels[lvl]

            st.info(f"📊 **Calculation:** Total Members: **{total_member}** | Total Family Expense: **₹{total_expense:,.2f}** | Per Head Expense: **₹{exp_per_head:,.2f}**")
            st.success(f"As per your expenses, your default lifestyle status is: **{style_status.upper()}**")

            st.write("---")

            # ==============================================================
            # ৬. Customized Goal List 
            # ==============================================================
            st.markdown("### 🎯 Customized Goal List")
            final_goals_list = []

            # ----------------------------------------------------
            # CASE 1: অবিবাহিত (Married = "NO") হলে
            # ----------------------------------------------------
            if st.session_state.get('married') == 'NO':
                st.info("Since you are unmarried, here is your customized recommended goal list:")
                
                st.markdown("#### 📌 Recommended Goals")
                st.write("*(These are selected by default. You can untick any goal if you don't want it.)*")
                
                col1, col2 = st.columns(2)
                with col1:
                    g_retire = st.checkbox("Retirement Fund", value=True, key="u_retire")
                    g_insure = st.checkbox("Insurance Fund", value=True, key="u_insure")
                    g_emerg = st.checkbox("Contingency/Emergency Fund", value=True, key="u_emerg")
                    
                with col2:
                    g_marriage = st.checkbox("Marriage", value=True, key="u_marriage")
                    g_vacation = st.checkbox("Vacation", value=True, key="u_vacation")
                    g_child_plan = st.checkbox("Child Planning", value=True, key="u_child_plan")
                    
                    num_planned_child = 0
                    child_goals_status = {}
                    
                    if g_child_plan:
                        num_planned_child = st.number_input("How many children do you plan to have?", min_value=1, max_value=10, value=1, step=1, key="u_plan_child_qty")
                        for i in range(1, num_planned_child + 1):
                            st.markdown(f"**🔹 For Child {i}:**")
                            child_goals_status[f"c{i}_edu"] = st.checkbox(f"Child {i} Education", value=True, key=f"u_chk_c{i}_edu")
                            child_goals_status[f"c{i}_mar"] = st.checkbox(f"Child {i} Marriage", value=True, key=f"u_chk_c{i}_mar")

                st.write("---")
                
                st.markdown("#### ➕ Additional Goals")
                st.write("*(Tick to add a goal, and adjust the quantity using + / -)*")
                
                additional_goals = ["House", "Car", "World Tour", "Lavish Accessories", "Business Set up fund", "Gadgets"]
                selected_additional_goals = {}
                
                add_cols = st.columns(3)
                for idx, goal_name in enumerate(additional_goals):
                    col = add_cols[idx % 3]
                    with col:
                        is_checked = st.checkbox(goal_name, value=False, key=f"u_chk_{goal_name}")
                        if is_checked:
                            qty = st.number_input(f"Qty", min_value=1, value=1, step=1, key=f"u_qty_{goal_name}")
                            selected_additional_goals[goal_name] = qty

                if g_retire: final_goals_list.append("Retirement Fund")
                if g_insure: final_goals_list.append("Insurance Fund")
                if g_emerg: final_goals_list.append("Contingency/Emergency Fund")
                if g_marriage: final_goals_list.append("Marriage")
                if g_vacation: final_goals_list.append("Vacation")
                
                if g_child_plan and num_planned_child > 0:
                    for i in range(1, num_planned_child + 1):
                        if child_goals_status[f"c{i}_edu"]: final_goals_list.append(f"Child {i} Education")
                        if child_goals_status[f"c{i}_mar"]: final_goals_list.append(f"Child {i} Marriage")
                
                for goal, qty in selected_additional_goals.items():
                    if qty == 1: final_goals_list.append(goal)
                    else:
                        for i in range(1, qty + 1): final_goals_list.append(f"{goal} {i}")
            
            # ----------------------------------------------------
            # CASE 2: বিবাহিত (Married = "YES") হলে
            # ----------------------------------------------------
            elif st.session_state.get('married') == 'YES':
                st.info("Since you are married, here is your customized recommended goal list:")
                
                st.markdown("#### 📌 Recommended Goals")
                st.write("*(These are selected by default. You can untick any goal if you don't want it.)*")
                
                col1, col2 = st.columns(2)
                with col1:
                    m_retire = st.checkbox("Retirement Fund", value=True, key="m_retire")
                    m_insure = st.checkbox("Insurance Fund", value=True, key="m_insure")
                    m_emerg = st.checkbox("Contingency/Emergency Fund", value=True, key="m_emerg")
                
                with col2:
                    m_vacation = st.checkbox("Vacation", value=True, key="m_vacation")
                    
                    has_child = st.session_state.get('child') == 'YES'
                    m_child_plan = False
                    num_planned_child = 0
                    planned_child_status = {}
                    
                    if not has_child:
                        m_child_plan = st.checkbox("Child Planning", value=True, key="m_child_plan")
                        if m_child_plan:
                            num_planned_child = st.number_input("How many children do you plan to have?", min_value=1, max_value=10, value=1, step=1, key="m_plan_child_qty")
                            for i in range(1, num_planned_child + 1):
                                st.markdown(f"**🔹 For Future Child {i}:**")
                                planned_child_status[f"fc{i}_edu"] = st.checkbox(f"Future Child {i} Education", value=True, key=f"m_chk_fc{i}_edu")
                                planned_child_status[f"fc{i}_mar"] = st.checkbox(f"Future Child {i} Marriage", value=True, key=f"m_chk_fc{i}_mar")

                existing_child_status = {}
                if has_child:
                    st.write("---")
                    st.markdown("#### 👶 Existing Children Goals")
                    kids = st.session_state.get('children_data', [])
                    for i, kid in enumerate(kids):
                        kid_name = kid['Name'] if kid['Name'] else f"Child {i+1}"
                        st.markdown(f"**🔹 For {kid_name}:**")
                        existing_child_status[f"{kid_name}_edu"] = st.checkbox(f"Education Expense for {kid_name}", value=True, key=f"m_chk_ex_{i}_edu")
                        existing_child_status[f"{kid_name}_mar"] = st.checkbox(f"Marriage Expense for {kid_name}", value=True, key=f"m_chk_ex_{i}_mar")
                
                st.write("---")
                st.markdown("#### ➕ Additional Goals")
                
                additional_goals = ["House", "Car", "World Tour", "Lavish Accessories", "Business Set up fund", "Gadgets"]
                
                if has_child:
                    additional_goals.insert(0, "Additional Child Planning")
                    
                selected_additional_goals = {}
                add_cols = st.columns(3)
                for idx, goal_name in enumerate(additional_goals):
                    col = add_cols[idx % 3]
                    with col:
                        is_checked = st.checkbox(goal_name, value=False, key=f"m_add_{idx}")
                        if is_checked:
                            qty = st.number_input(f"Qty", min_value=1, value=1, step=1, key=f"m_qty_{idx}")
                            selected_additional_goals[goal_name] = qty

                if m_retire: final_goals_list.append("Retirement Fund")
                if m_insure: final_goals_list.append("Insurance Fund")
                if m_emerg: final_goals_list.append("Contingency/Emergency Fund")
                if m_vacation: final_goals_list.append("Vacation")
                
                if not has_child and m_child_plan and num_planned_child > 0:
                    for i in range(1, num_planned_child + 1):
                        if planned_child_status[f"fc{i}_edu"]: final_goals_list.append(f"Future Child {i} Education")
                        if planned_child_status[f"fc{i}_mar"]: final_goals_list.append(f"Future Child {i} Marriage")
                
                if has_child:
                    for i, kid in enumerate(st.session_state.get('children_data', [])):
                        kid_name = kid['Name'] if kid['Name'] else f"Child {i+1}"
                        if existing_child_status[f"{kid_name}_edu"]: final_goals_list.append(f"Education Expense for {kid_name}")
                        if existing_child_status[f"{kid_name}_mar"]: final_goals_list.append(f"Marriage Expense for {kid_name}")
                
                for goal, qty in selected_additional_goals.items():
                    if goal == "Additional Child Planning":
                        for i in range(1, qty + 1):
                            final_goals_list.append(f"Additional Child {i} Education")
                            final_goals_list.append(f"Additional Child {i} Marriage")
                    elif qty == 1: 
                        final_goals_list.append(goal)
                    else:
                        for i in range(1, qty + 1): final_goals_list.append(f"{goal} {i}")

           # ==============================================================
            # ৭. ৬-কলামের টেবিল তৈরি (Present Value সহ)
            # ==============================================================
            if len(final_goals_list) > 0:
                st.write("---")
                st.markdown("### 📋 Your Customized Goal Table")
                
                # --- Col 2 এর ডিফল্ট ভ্যালু ক্যালকুলেশনের জন্য আয় এবং খরচ ---
                total_monthly_income = st.session_state.get('income', 0) + st.session_state.get('spouse_income', 0)
                annual_income = total_monthly_income * 12
                annual_expense = total_expense * 12  # total_expense উপরে আগেই ক্যালকুলেট করা আছে
                
                # টেবিলের হেডার
                h1, h2, h3, h4, h5, h6 = st.columns(6)
                h1.markdown("**Goal Name**")
                h2.markdown("**Present Value (₹)**") # Col 2 এর নাম দিলাম
                h3.markdown("**Col 3**")
                h4.markdown("**Col 4**")
                h5.markdown("**Col 5**")
                h6.markdown("**Col 6**")
                st.markdown("---")
                
                # ইউজারের এডিট করা ভ্যালুগুলো সেভ রাখার জন্য
                goal_present_values = {}
                
                for i, goal in enumerate(final_goals_list):
                    c1, c2, c3, c4, c5, c6 = st.columns(6)
                    
                    with c1: 
                        st.write(f"🎯 **{goal}**")
                        
                    with c2: 
                        # আপনার দেওয়া লজিক অনুযায়ী ডিফল্ট ভ্যালু সেট করা
                        default_val = 0.0
                        
                        if goal == "Retirement Fund":
                            # (total expense * 70%) / 7.5% 
                            default_val = (annual_expense * 0.70) / 0.075
                        elif goal == "Insurance Fund":
                            # anual income * 15
                            default_val = float(annual_income * 15)
                        elif goal == "Contingency/Emergency Fund":
                            # anual income * 3
                            default_val = float(annual_income * 3)
                        
                        # number_input দেওয়া হলো যাতে ক্লায়েন্ট ভ্যালু দেখতে ও এডিট করতে পারে
                        pv_value = st.number_input(
                            f"PV for {goal}", # লেবেল
                            value=float(default_val), 
                            min_value=0.0, 
                            step=1000.0, 
                            key=f"pv_{i}",
                            label_visibility="collapsed" # টেবিলের সুন্দর লুকের জন্য লেবেল হাইড করা হয়েছে
                        )
                        # এডিট করা ভ্যালুটি ডিকশনারিতে সেভ করে রাখা হচ্ছে
                        goal_present_values[goal] = pv_value
                        
                    with c3: st.write("-")
                    with c4: st.write("-")
                    with c5: st.write("-")
                    with c6: st.write("-")

            # ==============================================================
            # ৮. Upgrade / Downgrade Section (টেবিলের পরে)
            # ==============================================================
            st.write("---")
            st.markdown("### Do you want to upgrade or downgrade your lifestyle?")
            st.markdown("*According to your choice, your future expenses will be changed...*")

            options = ["Keep Same (0)"]
            if lvl > 0:
                options.insert(0, "Downgrade (-1 Level)")
            if lvl < 7:
                options.append("Upgrade (+1 Level)")

            lifestyle_change = st.radio(
                "Select an option:",
                options,
                index=options.index("Keep Same (0)"),
                key="lifestyle_change"
            )

            st.write("---")
            
            # ----------------------------------------------------
            # Next বাটন
            # ----------------------------------------------------
            if st.button("Next", key="btn_tab5_next", on_click=switch_tab, args=("Final Goals",)):
                # ডেটাগুলো মেমোরিতে সেভ করা হচ্ছে
                st.session_state.location = location
                st.session_state.current_lifestyle_level = lvl
                st.session_state.current_lifestyle_status = style_status
                st.session_state.lifestyle_change_choice = lifestyle_change
                st.session_state.final_goals_list = final_goals_list
                st.session_state.goal_present_values = goal_present_values # নতুন ডেটা মেমোরিতে সেভ হলো
                
                st.success("Lifestyle & Goals projection saved! Moving to Final Goals...")

        else:
            st.warning("⚠️ Please select your location to see your lifestyle calculation and enable the Next button.")
