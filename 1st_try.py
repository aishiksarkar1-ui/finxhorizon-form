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
            
            # মেমোরি থেকে বাচ্চাদের ডেটা আনা
            saved_children = st.session_state.get('children_data', [])
            default_num_child = len(saved_children) if len(saved_children) > 0 else 1
            
            num_children = st.number_input("How many children do you have?", min_value=1, max_value=10, step=1, value=default_num_child, key="num_child")
            
            # যদি ইউজারের দেওয়া সংখ্যা আগের সেভ করা সংখ্যার চেয়ে বড় হয়, তাহলে লিস্ট বড় করা
            while len(saved_children) < num_children:
                saved_children.append({"Name": "", "Gender": None, "Age": None})
            # যদি ছোট হয়, তাহলে কেটে ফেলা
            saved_children = saved_children[:num_children]
            
            st.write("---")
            
            for i in range(num_children):
                st.markdown(f"**Child {i+1} Details:**")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    saved_children[i]['Name'] = st.text_input(
                        "Name", 
                        value=saved_children[i].get('Name', ""), 
                        key=f"c_name_{i}"
                    )
                with col2:
                    gen_options = ['MALE', 'FEMALE', 'OTHER']
                    c_gen_def = saved_children[i].get('Gender')
                    gen_idx = gen_options.index(c_gen_def) if c_gen_def in gen_options else None
                    
                    saved_children[i]['Gender'] = st.selectbox(
                        "Gender", 
                        gen_options, 
                        index=gen_idx, 
                        key=f"c_gender_{i}"
                    )
                with col3:
                    age_options = [None] + list(range(0, 51))
                    c_age_def = saved_children[i].get('Age')
                    age_idx = age_options.index(c_age_def) if c_age_def in age_options else 0
                    
                    saved_children[i]['Age'] = st.selectbox(
                        "Age", 
                        age_options, 
                        index=age_idx, 
                        format_func=lambda x: "Select age" if x is None else f"{x} Years", 
                        key=f"c_age_{i}"
                    )
                
                st.write("")
            
            # লুপের বাইরে এসে সেশন স্টেটে আপডেট করা
            st.session_state.children_data = saved_children
            children_data = saved_children
                
        elif st.session_state.get('child') == 'NO':
            st.info("Since you do not have children, child details are not applicable.")
            children_data = []
            
        elif st.session_state.get('married') == 'NO':
             st.info("Since you are unmarried, child details are not applicable.")
             children_data = []
             
        else:
             children_data = []
             st.warning("Please fill the Spouse Details tab first.")

        # --- ২. Dependent Member এর প্রশ্ন ---
        st.write("---")
        
        dep_options = ('YES', 'NO')
        saved_dep = st.session_state.get('dependent')
        dep_idx = dep_options.index(saved_dep) if saved_dep in dep_options else None
        
        # অন-চেঞ্জ ফাংশন দিয়ে সরাসরি সেভ
        def update_dependent():
            st.session_state.dependent = st.session_state.has_dependent
            
        dependent = st.radio(
            "Do you have any member in your family who is completely dependent on your income?",
            dep_options,
            index=dep_idx,
            key="has_dependent",
            on_change=update_dependent
        )
        
        # --- ৩. Next বাটন ---
        target_tab = "Dependent Member" if st.session_state.get('dependent') == 'YES' else "Future Expenses Projection"
        
        all_filled = True
        if st.session_state.get('child') == 'YES':
            all_filled = all(child["Name"] and child["Gender"] and child["Age"] is not None for child in children_data)
        
        is_valid = all_filled and (st.session_state.get('dependent') is not None)
        
        if not is_valid:
            st.warning("⚠️ Please fill in all details and answer the dependent question to enable the Next button.")

        if st.button("Next", key="btn_tab3_next", disabled=not is_valid, on_click=switch_tab, args=(target_tab,)):
            st.success("Details saved successfully! Moving to the next step...")


    # 4th ট্যাব এর ডিজাইন (Dependent Member)
    #____________________________________
    with tab4:
        st.subheader("Dependent Member Details")
        
        if st.session_state.get('dependent') == 'YES':
            st.info("Please provide the details of your dependent family members below:")
            
            saved_deps = st.session_state.get('dependents_data', [])
            default_num_dep = len(saved_deps) if len(saved_deps) > 0 else 1
            
            num_dependents = st.number_input(
                "HOW MANY DEPENDENT MEMBERS ARE THERE IN YOUR FAMILY?", 
                min_value=1, max_value=10, step=1, value=default_num_dep, key="num_dep"
            )
            
            while len(saved_deps) < num_dependents:
                saved_deps.append({"Name": "", "Gender": None, "Age": None, "Relation": None})
            saved_deps = saved_deps[:num_dependents]
            
            st.write("---") 
            
            for i in range(num_dependents):
                st.markdown(f"**Dependent Member {i+1}:**")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    saved_deps[i]['Name'] = st.text_input(
                        "Name", 
                        value=saved_deps[i].get('Name', ""), 
                        key=f"d_name_{i}"
                    )
                
                with col2:
                    d_gen_options = ['MALE', 'FEMALE', 'OTHER']
                    d_gen_def = saved_deps[i].get('Gender')
                    d_gen_idx = d_gen_options.index(d_gen_def) if d_gen_def in d_gen_options else None
                    
                    saved_deps[i]['Gender'] = st.selectbox(
                        "Gender", 
                        d_gen_options, 
                        index=d_gen_idx, 
                        key=f"d_gender_{i}"
                    )
                
                with col3:
                    d_age_options = [None] + list(range(0, 101))
                    d_age_def = saved_deps[i].get('Age')
                    d_age_idx = d_age_options.index(d_age_def) if d_age_def in d_age_options else 0
                    
                    saved_deps[i]['Age'] = st.selectbox(
                        "Age", 
                        d_age_options, 
                        index=d_age_idx, 
                        format_func=lambda x: "Select age" if x is None else f"{x} Years", 
                        key=f"d_age_{i}"
                    )
                    
                with col4:
                    rel_options = ['FATHER', 'MOTHER', 'BROTHER', 'SISTER', 'OTHER']
                    d_rel_def = saved_deps[i].get('Relation')
                    rel_idx = rel_options.index(d_rel_def) if d_rel_def in rel_options else None
                    
                    saved_deps[i]['Relation'] = st.selectbox(
                        "Relation", 
                        rel_options, 
                        index=rel_idx, 
                        key=f"d_rel_{i}"
                    )
                
                st.write("")
            
            st.session_state.dependents_data = saved_deps
            
            is_valid = all(dep["Name"] and dep["Gender"] and (dep["Age"] is not None) and dep["Relation"] for dep in saved_deps)
            
            if not is_valid:
                st.warning("⚠️ Please fill in the Name, Gender, Age, and Relation for all dependent members to enable the Next button.")
                
            if st.button("Next", key="btn_tab4_next", disabled=not is_valid, on_click=switch_tab, args=("Future Expenses Projection",)):
                st.success("Dependent members' details saved successfully! Moving to the next step...")
                
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

        # --- ১. লোকেশন ইনপুট ---
        loc_options = ["Village", "Semi-village", "Small City", "City", "Megacity"]
        saved_loc = st.session_state.get('location')
        loc_idx = loc_options.index(saved_loc) if saved_loc in loc_options else None
        
        def update_location():
            st.session_state.location = st.session_state.location_type
            
        location = st.selectbox(
            "Where do you live?",
            loc_options,
            index=loc_idx,
            key="location_type",
            on_change=update_location
        )

        st.write("---")

        if location:
            user_count = 1
            spouse_count = 1 if st.session_state.get('married') == 'YES' else 0
            
            child_data = st.session_state.get('children_data', [])
            child_count = len(child_data) if st.session_state.get('child') == 'YES' else 0
            
            dep_data = st.session_state.get('dependents_data', [])
            dep_count = len(dep_data) if st.session_state.get('dependent') == 'YES' else 0

            total_member = user_count + spouse_count + child_count + dep_count

            user_exp = st.session_state.get('expenses', 0)
            spouse_exp = st.session_state.get('spouse_expenses', 0)
            total_expense = user_exp + spouse_exp

            exp_per_head = total_expense / total_member if total_member > 0 else 0

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
            st.session_state.current_lifestyle_status = style_status

            st.info(f"📊 **Calculation:** Total Members: **{total_member}** | Total Family Expense: **₹ {total_expense:,.2f}** | Per Head Expense: **₹ {exp_per_head:,.2f}**")
            st.success(f"As per your expenses, your default lifestyle status is: **{style_status.upper()}**")

            st.write("---")

            # ==============================================================
            # ৬. Customized Goal List 
            # ==============================================================
            st.markdown("### 🎯 Customized Goal List")
            
            # চেকবক্সগুলোর স্টেট সেভ করার লজিক
            def toggle_goal(goal_key):
                st.session_state[goal_key] = st.session_state[f"chk_{goal_key}"]

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
                    g_retire = st.checkbox("Retirement Fund", value=st.session_state.get('goal_retire', True), key="chk_goal_retire", on_change=toggle_goal, args=('goal_retire',))
                    g_med_emerg = st.checkbox("Medical Emergency Fund", value=st.session_state.get('goal_med_emerg', True), key="chk_goal_med_emerg", on_change=toggle_goal, args=('goal_med_emerg',))
                    g_emerg = st.checkbox("Contingency/Emergency Fund", value=st.session_state.get('goal_emerg', True), key="chk_goal_emerg", on_change=toggle_goal, args=('goal_emerg',))
                    
                with col2:
                    g_marriage = st.checkbox("Marriage", value=st.session_state.get('goal_marriage', True), key="chk_goal_marriage", on_change=toggle_goal, args=('goal_marriage',))
                    g_child_plan = st.checkbox("Child Planning", value=st.session_state.get('goal_child_plan', True), key="chk_goal_child_plan", on_change=toggle_goal, args=('goal_child_plan',))
                    
                    num_planned_child = 0
                    child_goals_status = {}
                    
                    if g_child_plan:
                        num_planned_child = st.number_input("How many children do you plan to have?", min_value=1, max_value=10, value=st.session_state.get('plan_child_qty', 1), step=1, key="plan_child_qty")
                        for i in range(1, num_planned_child + 1):
                            st.markdown(f"**🔹 For Child {i}:**")
                            child_goals_status[f"c{i}_edu"] = st.checkbox(f"Child {i} Education", value=st.session_state.get(f'goal_c{i}_edu', True), key=f"chk_goal_c{i}_edu", on_change=toggle_goal, args=(f'goal_c{i}_edu',))
                            child_goals_status[f"c{i}_mar"] = st.checkbox(f"Child {i} Marriage", value=st.session_state.get(f'goal_c{i}_mar', True), key=f"chk_goal_c{i}_mar", on_change=toggle_goal, args=(f'goal_c{i}_mar',))

                st.write("---")
                
                st.markdown("#### ➕ Additional Goals")
                st.write("*(Tick to add a goal, and adjust the quantity using + / -)*")
                
                additional_goals = ["House", "Car", "Vacation", "Lavish Accessories", "Business Set up fund", "Gadgets"]
                selected_additional_goals = {}
                
                add_cols = st.columns(3)
                for idx, goal_name in enumerate(additional_goals):
                    col = add_cols[idx % 3]
                    with col:
                        is_checked = st.checkbox(goal_name, value=st.session_state.get(f'add_goal_{goal_name}', False), key=f"chk_add_goal_{goal_name}", on_change=toggle_goal, args=(f'add_goal_{goal_name}',))
                        if is_checked:
                            qty = st.number_input(f"Qty", min_value=1, value=st.session_state.get(f'add_qty_{goal_name}', 1), step=1, key=f"add_qty_{goal_name}")
                            selected_additional_goals[goal_name] = qty

                if g_retire: final_goals_list.append("Retirement Fund")
                if g_med_emerg: final_goals_list.append("Medical Emergency Fund")
                if g_emerg: final_goals_list.append("Contingency/Emergency Fund")
                if g_marriage: final_goals_list.append("Marriage")
                
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
                    m_retire = st.checkbox("Retirement Fund", value=st.session_state.get('goal_retire', True), key="chk_goal_retire", on_change=toggle_goal, args=('goal_retire',))
                    m_med_emerg = st.checkbox("Medical Emergency Fund", value=st.session_state.get('goal_med_emerg', True), key="chk_goal_med_emerg", on_change=toggle_goal, args=('goal_med_emerg',))
                    m_emerg = st.checkbox("Contingency/Emergency Fund", value=st.session_state.get('goal_emerg', True), key="chk_goal_emerg", on_change=toggle_goal, args=('goal_emerg',))
                
                with col2:
                    has_child = st.session_state.get('child') == 'YES'
                    m_child_plan = False
                    num_planned_child = 0
                    planned_child_status = {}
                    
                    if not has_child:
                        m_child_plan = st.checkbox("Child Planning", value=st.session_state.get('goal_child_plan', True), key="chk_goal_child_plan", on_change=toggle_goal, args=('goal_child_plan',))
                        if m_child_plan:
                            num_planned_child = st.number_input("How many children do you plan to have?", min_value=1, max_value=10, value=st.session_state.get('plan_child_qty', 1), step=1, key="plan_child_qty")
                            for i in range(1, num_planned_child + 1):
                                st.markdown(f"**🔹 For Future Child {i}:**")
                                planned_child_status[f"fc{i}_edu"] = st.checkbox(f"Future Child {i} Education", value=st.session_state.get(f'goal_fc{i}_edu', True), key=f"chk_goal_fc{i}_edu", on_change=toggle_goal, args=(f'goal_fc{i}_edu',))
                                planned_child_status[f"fc{i}_mar"] = st.checkbox(f"Future Child {i} Marriage", value=st.session_state.get(f'goal_fc{i}_mar', True), key=f"chk_goal_fc{i}_mar", on_change=toggle_goal, args=(f'goal_fc{i}_mar',))

                existing_child_status = {}
                if has_child:
                    st.write("---")
                    st.markdown("#### 👶 Existing Children Goals")
                    kids = st.session_state.get('children_data', [])
                    for i, kid in enumerate(kids):
                        kid_name = kid['Name'] if kid['Name'] else f"Child {i+1}"
                        st.markdown(f"**🔹 For {kid_name}:**")
                        existing_child_status[f"{kid_name}_edu"] = st.checkbox(f"Education Expense for {kid_name}", value=st.session_state.get(f'goal_ex_{i}_edu', True), key=f"chk_goal_ex_{i}_edu", on_change=toggle_goal, args=(f'goal_ex_{i}_edu',))
                        existing_child_status[f"{kid_name}_mar"] = st.checkbox(f"Marriage Expense for {kid_name}", value=st.session_state.get(f'goal_ex_{i}_mar', True), key=f"chk_goal_ex_{i}_mar", on_change=toggle_goal, args=(f'goal_ex_{i}_mar',))
                
                st.write("---")
                st.markdown("#### ➕ Additional Goals")
                
                additional_goals = ["House", "Car", "Vacation", "Lavish Accessories", "Business Set up fund", "Gadgets"]
                
                if has_child:
                    additional_goals.insert(0, "Additional Child Planning")
                    
                selected_additional_goals = {}
                add_cols = st.columns(3)
                for idx, goal_name in enumerate(additional_goals):
                    col = add_cols[idx % 3]
                    with col:
                        is_checked = st.checkbox(goal_name, value=st.session_state.get(f'add_goal_{idx}', False), key=f"chk_add_goal_{idx}", on_change=toggle_goal, args=(f'add_goal_{idx}',))
                        if is_checked:
                            qty = st.number_input(f"Qty", min_value=1, value=st.session_state.get(f'add_qty_{idx}', 1), step=1, key=f"add_qty_{idx}")
                            selected_additional_goals[goal_name] = qty

                if m_retire: final_goals_list.append("Retirement Fund")
                if m_med_emerg: final_goals_list.append("Medical Emergency Fund")
                if m_emerg: final_goals_list.append("Contingency/Emergency Fund")
                
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

            st.session_state.final_goals_list = final_goals_list

            # ==============================================================
            # ৭. ৬-কলামের টেবিল তৈরি 
            # ==============================================================
            if len(final_goals_list) > 0:
                st.write("---")
                st.markdown("### 📋 Your Customized Goal Table")
                
                total_monthly_income = st.session_state.get('income', 0) + st.session_state.get('spouse_income', 0)
                annual_income = total_monthly_income * 12
                annual_expense = total_expense * 12 
                
                user_age = st.session_state.get('age', 30) or 30
                
                kids_dict = {}
                for i, kid in enumerate(st.session_state.get('children_data', [])):
                    k_name = kid.get('Name') if kid.get('Name') else f"Child {i+1}"
                    kids_dict[k_name] = kid
                
                # টেবিলের হেডার
                h1, h2, h3, h4, h5, h6 = st.columns(6)
                h1.markdown("**Goal Name**")
                h2.markdown("**Present Value (₹)**")
                h3.markdown("**Duration (Yrs)**")
                h4.markdown("**Inflation (%)**") 
                h5.markdown("**Future Value (₹)**") 
                h6.markdown("**Col 6**")
                st.markdown("---")
                
                goal_custom_names = st.session_state.get('goal_custom_names', {})
                goal_present_values = st.session_state.get('goal_present_values', {})
                goal_durations = st.session_state.get('goal_durations', {})
                goal_inflations = st.session_state.get('goal_inflations', {})
                goal_future_values = {} 
                
                # ইনপুট সেভ করার লজিক
                def update_goal_data(goal_key, dict_name):
                    if dict_name == 'pv': st.session_state.goal_present_values[goal_key] = st.session_state[f"input_pv_{goal_key}"]
                    elif dict_name == 'dur': st.session_state.goal_durations[goal_key] = st.session_state[f"input_dur_{goal_key}"]
                    elif dict_name == 'inf': st.session_state.goal_inflations[goal_key] = st.session_state[f"input_inf_{goal_key}"]
                    elif dict_name == 'name': st.session_state.goal_custom_names[goal_key] = st.session_state[f"input_name_{goal_key}"]

                for i, goal in enumerate(final_goals_list):
                    c1, c2, c3, c4, c5, c6 = st.columns(6)
                    
                    # ------------------------------------------
                    # Column 2 (Present Value)
                    # ------------------------------------------
                    with c2: 
                        default_val = 0.0
                        
                        if goal == "Retirement Fund":
                            if style_status == "Basic": default_val = (annual_income * 0.40) / 0.09
                            elif style_status == "Modest": default_val = (annual_income * 0.45) / 0.09
                            elif style_status == "Standard": default_val = (annual_income * 0.50) / 0.09
                            elif style_status == "Comfortable": default_val = (annual_income * 0.60) / 0.09
                            elif style_status == "Upper_Middle class": default_val = (annual_income * 0.70) / 0.09
                            elif style_status == "Affluent": default_val = (annual_income * 0.80) / 0.09
                            elif style_status == "Luxury": default_val = (annual_income * 0.90) / 0.09
                            elif style_status == "Elite": default_val = annual_income / 0.09 
                                
                        elif goal == "Medical Emergency Fund":
                            default_val = float(annual_expense * 5)
                            
                        elif goal == "Contingency/Emergency Fund":
                            default_val = float(annual_income * 3)
                            
                        elif "Education" in goal:
                            if style_status == "Basic": default_val = 500000.0      
                            elif style_status == "Modest": default_val = 1000000.0     
                            elif style_status == "Standard": default_val = 1500000.0     
                            elif style_status == "Comfortable": default_val = 2500000.0     
                            elif style_status == "Upper_Middle class": default_val = 4000000.0     
                            elif style_status == "Affluent": default_val = 6500000.0     
                            elif style_status == "Luxury": default_val = 10000000.0    
                            elif style_status == "Elite": default_val = 20000000.0    

                        elif "Marriage" in goal:
                            if style_status == "Basic": default_val = 1000000.0      
                            elif style_status == "Modest": default_val = 1500000.0     
                            elif style_status == "Standard": default_val = 2000000.0     
                            elif style_status == "Comfortable": default_val = 2500000.0     
                            elif style_status == "Upper_Middle class": default_val = 4000000.0     
                            elif style_status == "Affluent": default_val = 6000000.0     
                            elif style_status == "Luxury": default_val = 10000000.0    
                            elif style_status == "Elite": default_val = 25000000.0 
                        
                        # মেমোরি থেকে ভ্যালু আনা
                        current_pv = goal_present_values.get(goal, default_val)
                        
                        pv_value = st.number_input(
                            f"PV for {goal}",
                            value=float(current_pv), 
                            min_value=0.0, 
                            step=1000.0, 
                            format="%0.2f", 
                            key=f"input_pv_{goal}", 
                            label_visibility="collapsed",
                            on_change=update_goal_data,
                            args=(goal, 'pv')
                        )

                        if goal == "Retirement Fund":
                            present_pension = (pv_value * 0.09) / 12
                            st.markdown(f"<div style='font-size:12px; color:gray; margin-top:-10px; margin-bottom:10px;'>Pension: ₹ {present_pension:,.2f} /mo</div>", unsafe_allow_html=True)

                    # ------------------------------------------
                    # Column 3 (Duration)
                    # ------------------------------------------
                    with c3: 
                        default_dur = 0
                        if goal == "Retirement Fund":
                            default_dur = max(0, 60 - user_age)
                        elif goal in ["Medical Emergency Fund", "Contingency/Emergency Fund"]:
                            default_dur = 0
                        elif "Future Child" in goal or "Additional Child" in goal or (goal.startswith("Child ") and st.session_state.get('married') == 'NO'):
                            if "Education" in goal: default_dur = 17
                            elif "Marriage" in goal: default_dur = 24
                        elif goal.startswith("Education Expense for "):
                            k_name = goal.replace("Education Expense for ", "")
                            k_age = kids_dict.get(k_name, {}).get("Age") or 0
                            default_dur = max(0, 17 - k_age)
                        elif goal.startswith("Marriage Expense for "):
                            k_name = goal.replace("Marriage Expense for ", "")
                            kid_info = kids_dict.get(k_name, {})
                            k_age = kid_info.get("Age") or 0
                            k_gender = kid_info.get("Gender", "FEMALE")
                            if k_gender == "MALE": default_dur = max(0, 28 - k_age)
                            else: default_dur = max(0, 24 - k_age)
                        
                        current_dur = goal_durations.get(goal, default_dur)
                        
                        dur_value = st.number_input(
                            f"Dur for {goal}",
                            value=int(current_dur),
                            min_value=0,
                            step=1,
                            key=f"input_dur_{goal}",
                            label_visibility="collapsed",
                            on_change=update_goal_data,
                            args=(goal, 'dur')
                        )

                    # ------------------------------------------
                    # Column 4 (Inflation)
                    # ------------------------------------------
                    with c4:
                        default_inf = 5.0 
                        if "Education" in goal: default_inf = 7.0
                        elif "Medical" in goal: default_inf = 8.0
                            
                        current_inf = goal_inflations.get(goal, default_inf)
                            
                        inf_value = st.number_input(
                            f"Inf for {goal}",
                            value=float(current_inf),
                            min_value=0.0,
                            step=0.5,
                            format="%0.1f", 
                            key=f"input_inf_{goal}",
                            label_visibility="collapsed",
                            on_change=update_goal_data,
                            args=(goal, 'inf')
                        )

                    # ------------------------------------------
                    # Column 5 (Future Value)
                    # ------------------------------------------
                    with c5:
                        fv_value = pv_value * ((1 + (inf_value / 100)) ** dur_value)
                        goal_future_values[goal] = fv_value
                        
                        st.markdown(
                            f"""
                            <div style='background-color: #f3f4f6; border: 1px solid #d1d5db; 
                                        border-radius: 6px; padding: 7px 12px; color: #6b7280; 
                                        font-size: 15px; height: 38px; display: flex; 
                                        align-items: center;'>
                                {fv_value:,.2f}
                            </div>
                            """, 
                            unsafe_allow_html=True
                        )

                        if goal == "Retirement Fund":
                            future_pension = (fv_value * 0.09) / 12
                            st.markdown(f"<div style='font-size:12px; color:#007BFF; font-weight:bold; margin-top:5px; margin-bottom:10px;'>Pension: ₹ {future_pension:,.2f} /mo</div>", unsafe_allow_html=True)

                    # ------------------------------------------
                    # Column 1 (Goal Name Logic Update)
                    # ------------------------------------------
                    with c1: 
                        if "Gadget" in goal:
                            current_name = goal_custom_names.get(goal, goal)
                            custom_name = st.text_input(
                                f"Name for {goal}",
                                value=current_name,
                                key=f"input_name_{goal}",
                                label_visibility="collapsed",
                                on_change=update_goal_data,
                                args=(goal, 'name')
                            )
                        else:
                            st.write(f"🎯 **{goal}**")
                            goal_custom_names[goal] = goal 
                        
                    with c6: st.write("-")
                    
            st.session_state.goal_custom_names = goal_custom_names
            st.session_state.goal_present_values = goal_present_values
            st.session_state.goal_durations = goal_durations
            st.session_state.goal_inflations = goal_inflations
            st.session_state.goal_future_values = goal_future_values

            # ==============================================================
            # ৮. Finalize Goal Button 
            # ==============================================================
            st.write("---")
            
            if st.button("Finalize your goal", type="primary", key="btn_finalize_goals"):
                st.session_state.page = 'timeline_page'
                st.rerun()

        else:
            st.warning("⚠️ Please select your location to see your lifestyle calculation and enable the Next button.")




# ==========================================
# PAGE 3: Timeline & Final Calculation
# ==========================================
elif st.session_state.page == 'timeline_page':
    
    # ব্যাক বাটনটি একদম উপরে রাখা হলো
    if st.button("⬅️ Back to Form"):
        st.session_state.page = 'main_form'
        st.rerun()
        
    st.title("⏳ Your Financial Timeline")
    st.write("---")
    
    st.markdown("### Based on your age and goals, here is your timeline:")
    
    # (এখানে আমরা টাইমলাইনের আসল লজিক বসাবো)
