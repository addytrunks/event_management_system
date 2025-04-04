import streamlit as st
import pymysql
import bcrypt
import datetime

# Set page configuration and apply custom styling
st.set_page_config(
    page_title="Event Management System",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def apply_custom_css():
    st.markdown("""
    <style>
        /* Main styles */
        .stApp {
            background-color: #f0f5ff;
        }
        
        /* Headers */
        h1, h2, h3 {
            color: #1e3a8a;
            font-family: 'Segoe UI', sans-serif;
        }
        
        h1 {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 1.5rem;
        }
        
        h3 {
            font-size: 1.5rem;
            margin-top: 1rem;
        }
        
        /* Card styling */
        .card {
            background-color: white;
            border-radius: 10px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 1rem;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
        }
        
        /* Status indicators */
        .status-pending {
            color: #f59e0b;
            background-color: rgba(245, 158, 11, 0.1);
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-weight: 500;
        }
        
        .status-confirmed {
            color: #10b981;
            background-color: rgba(16, 185, 129, 0.1);
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-weight: 500;
        }
        
        .status-rejected {
            color: #ef4444;
            background-color: rgba(239, 68, 68, 0.1);
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-weight: 500;
        }
        
        /* Button styling */
        .stButton>button {
            border-radius: 20px;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .primary-btn>button {
            background-color: #1e40af;
            color: white;
        }
        
        .primary-btn>button:hover {
            background-color: #1e3a8a;
            box-shadow: 0 4px 8px rgba(30, 64, 175, 0.3);
        }
        
        .secondary-btn>button {
            background-color: #f9fafb;
            color: #1e3a8a;
            border: 1px solid #1e3a8a;
        }
        
        .secondary-btn>button:hover {
            background-color: #f0f5ff;
        }
        
        .danger-btn>button {
            background-color: #ef4444;
            color: white;
        }
        
        .danger-btn>button:hover {
            background-color: #dc2626;
            box-shadow: 0 4px 8px rgba(239, 68, 68, 0.3);
        }
        
        /* Sidebar */
        .css-1d391kg {
            background-color: #1e3a8a;
        }
        
        .sidebar .sidebar-content {
            background-color: #1e3a8a;
            color: white;
        }
        
        /* Data display styling */
        .data-row {
            display: flex;
            margin-bottom: 0.5rem;
        }
        
        .data-label {
            font-weight: 500;
            color: #6b7280;
            width: 120px;
        }
        
        .data-value {
            color: #1f2937;
        }
        
        /* Divider */
        hr {
            margin-top: 1rem;
            margin-bottom: 1rem;
            border: 0;
            border-top: 1px solid #e5e7eb;
        }
        
        /* Form styling */
        .stTextInput>div>div>input, .stNumberInput>div>div>input, .stDateInput>div>div>input {
            border-radius: 8px;
            border: 1px solid #d1d5db;
            padding: 0.5rem;
        }
        
        .stTextInput>div>div>input:focus, .stNumberInput>div>div>input:focus, .stDateInput>div>div>input:focus {
            border-color: #1e3a8a;
            box-shadow: 0 0 0 2px rgba(30, 64, 175, 0.2);
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 4rem;
            white-space: nowrap;
            font-size: 1rem;
            color: #6b7280;
            font-weight: 500;
        }
        
        .stTabs [aria-selected="true"] {
            color: #1e3a8a;
            font-weight: 600;
        }
        
        /* Custom badge */
        .badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.875rem;
            font-weight: 500;
            margin-right: 0.5rem;
        }
        
        .badge-primary {
            background-color: #dbeafe;
            color: #1e40af;
        }
        
        .badge-success {
            background-color: #d1fae5;
            color: #065f46;
        }
        
        .badge-warning {
            background-color: #fef3c7;
            color: #92400e;
        }
        
        .badge-danger {
            background-color: #fee2e2;
            color: #b91c1c;
        }
        
        /* Price display */
        .price-display {
            font-size: 1.5rem;
            font-weight: 700;
            color: #1e3a8a;
        }
        
        /* Select box styling */
        .stSelectbox>div>div>div {
            background-color: white;
            border-radius: 8px;
            border: 1px solid #d1d5db;
        }
        
        /* Progress bar */
        .stProgress > div > div > div > div {
            background-color: #1e3a8a;
        }
        
        /* Header decorations */
        .decorated-header {
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #1e3a8a;
            margin-bottom: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)

# Database Connection
def connect_db():
    return pymysql.connect(
        host="localhost",
        user="root",  # Change this to your MySQL username
        password="adhithya1234",  # Change this to your MySQL password
        database="event_management"
    )

# Hash Password
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Verify Password
def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

# User Login
def login(user_type):
    st.markdown(f'<h2 class="decorated-header">{user_type} Login</h2>', unsafe_allow_html=True)
    
    with st.container():
        # Create a card-like effect for the login form
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Login image or graphic could go here
            st.markdown(
                """
                <div style="display: flex; justify-content: center; align-items: center; height: 100%;">
                    <span style="font-size: 5rem; color: #1e3a8a;">🔐</span>
                </div>
                <div style="text-align: center; margin-top: 1rem;">
                    <p style="color: #6b7280; font-size: 1.2rem;">Welcome back!</p>
                </div>
                """, 
                unsafe_allow_html=True
            )
        
        with col2:
            email = st.text_input("Email Address", placeholder="Enter your email")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            col_btn1, col_btn2 = st.columns([1, 1])
            with col_btn1:
                st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
                login_btn = st.button("Login")
                st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    if login_btn:
        try:
            print("Trying to connect to DB")
            db = connect_db()
            print("DB connected")
            cursor = db.cursor(pymysql.cursors.DictCursor)
            table = "Organizer" if user_type == "Organizer" else "Customer"
            cursor.execute(f"SELECT * FROM {table} WHERE email = %s", (email,))
            user = cursor.fetchone()
            db.close()
            
            if user and verify_password(password, user['password']):
                st.session_state["logged_in"] = True
                st.session_state["user_type"] = user_type
                st.session_state["user_id"] = user["organizer_id"] if user_type == "Organizer" else user["customer_id"]
                st.session_state["user_name"] = user['first_name']
                
                # Success message with animation
                st.markdown(
                    """
                    <div style="display: flex; justify-content: center; align-items: center; margin: 2rem 0;">
                        <div style="background-color: #d1fae5; border-radius: 8px; padding: 1rem; text-align: center;">
                            <span style="font-size: 3rem;">✅</span>
                            <p style="color: #065f46; font-weight: 600; margin-top: 0.5rem;">Login Successful!</p>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                st.rerun()
            else:
                st.markdown(
                    """
                    <div style="background-color: #fee2e2; border-radius: 8px; padding: 1rem; margin-top: 1rem;">
                        <p style="color: #b91c1c; margin: 0;">❌ Invalid email or password. Please try again.</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        except Exception as e:
            st.error(f"Connection error: {str(e)}")

# User Registration
def register(user_type):
    st.markdown(f'<h2 class="decorated-header">{user_type} Registration</h2>', unsafe_allow_html=True)
    
    # Create a card-like effect for the registration form
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        first_name = st.text_input("First Name", placeholder="Enter your first name")
        last_name = st.text_input("Last Name", placeholder="Enter your last name")
        email = st.text_input("Email Address", placeholder="Enter your email")
    
    with col2:
        password = st.text_input("Password", type="password", placeholder="Create a password")
        phone_no = st.text_input("Phone Number", placeholder="Enter your phone number")
        
        # Empty space to align the register button
        st.write("")
    
    col_btn1, col_btn2, col_btn3 = st.columns([2, 2, 1])
    with col_btn1:
        st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
        register_btn = st.button("Register")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if register_btn:
        if not first_name or not last_name or not email or not password or not phone_no:
            st.markdown(
                """
                <div style="background-color: #fee2e2; border-radius: 8px; padding: 1rem; margin-top: 1rem;">
                    <p style="color: #b91c1c; margin: 0;">❌ Please fill in all fields to complete registration.</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            return
            
        db = connect_db()
        cursor = db.cursor()
        table = "Organizer" if user_type == "Organizer" else "Customer"
        hashed_pw = hash_password(password)
        try:
            cursor.execute(f"INSERT INTO {table} (first_name, last_name, email, password, phone_no) VALUES (%s, %s, %s, %s, %s)",
                           (first_name, last_name, email, hashed_pw, phone_no))
            db.commit()
            
            # Success message with animation
            st.markdown(
                """
                <div style="display: flex; justify-content: center; align-items: center; margin: 2rem 0;">
                    <div style="background-color: #d1fae5; border-radius: 8px; padding: 1rem; text-align: center;">
                        <span style="font-size: 3rem;">🎉</span>
                        <p style="color: #065f46; font-weight: 600; margin-top: 0.5rem;">Registration Successful!</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Auto-redirect to login
            st.session_state['show_login'] = True
            st.rerun()
        except Exception as e:
            st.markdown(
                f"""
                <div style="background-color: #fee2e2; border-radius: 8px; padding: 1rem; margin-top: 1rem;">
                    <p style="color: #b91c1c; margin: 0;">❌ Registration failed: {str(e)}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        db.close()

# Check if user is logged in
def is_authenticated():
    return "logged_in" in st.session_state and st.session_state["logged_in"]

# Check if user is of certain type
def is_user_type(user_type):
    return is_authenticated() and st.session_state["user_type"] == user_type

# Organizer: Manage Halls
def manage_halls():
    if not is_user_type("Organizer"):
        st.markdown(
            """
            <div style="background-color: #fee2e2; border-radius: 8px; padding: 1rem; margin: 2rem 0;">
                <p style="color: #b91c1c; font-weight: 500; margin: 0;">⚠️ Access denied. Please login as an Organizer.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        return
    
    st.markdown('<h2 class="decorated-header">Manage Your Venues</h2>', unsafe_allow_html=True)
    
    # Create tabs for better organization
    tab1, tab2 = st.tabs(["📋 Your Halls", "➕ Add New Hall"])
    
    with tab1:
        if "hall_updated_success" in st.session_state:
            st.markdown(
                f"""
                <div style="background-color: #d1fae5; border-radius: 8px; padding: 1rem; margin-top: 1rem;">
                    <p style="color: #065f46; font-weight: 500; margin: 0;">{st.session_state['hall_updated_success']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            del st.session_state["hall_updated_success"]
        db = connect_db()
        cursor = db.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM Hall WHERE organizer_id = %s", (st.session_state["user_id"],))
        halls = cursor.fetchall()
        
        if not halls:
            st.markdown(
                """
                <div style="background-color: #dbeafe; border-radius: 8px; padding: 1.5rem; margin: 1rem 0; text-align: center;">
                    <span style="font-size: 3rem;">🏛️</span>
                    <p style="color: #1e40af; font-weight: 500; margin-top: 1rem;">You haven't added any halls yet.</p>
                    <p style="color: #1e40af;">Use the 'Add New Hall' tab to get started.</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        # Display halls in a modern card format
        for i, hall in enumerate(halls):
            st.markdown(f'<div class="card">', unsafe_allow_html=True)
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                st.markdown(f'<h3 style="margin-top: 0;">{hall["address"]}</h3>', unsafe_allow_html=True)
                
                # Display hall description
                if hall["hall_description"]:
                    st.markdown("**Description**:",unsafe_allow_html=True)
                    st.markdown(
                        f"""
                        <div style="font-size: 0.9rem; color: #555; margin-bottom: 0.8rem; background: #f9fafb; padding: 0.8rem; border-radius: 5px; background: #f3f4f6;">
                            {hall["hall_description"]}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                st.markdown(
                    f"""
                    <div class="data-row">
                        <div class="data-label">Price:</div>
                        <div class="data-value price-display">₹{hall['hall_price_per_day']}</div>
                    </div>
                    <div class="data-row">
                        <div class="data-label">Capacity:</div>
                        <div class="data-value"><span class="badge badge-primary">{hall['hall_accommodation']} people</span></div>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )

            
            with col2:
                # Visual indicator of hall status
                st.markdown(
                    """
                    <div style="display: flex; align-items: center; height: 100%;">
                        <div style="background-color: #f0f9ff; border-radius: 8px; padding: 1rem; text-align: center; width: 100%;">
                            <span style="font-size: 2rem;">🏛️</span>
                            <p style="color: #1e40af; margin: 0.5rem 0 0 0;">Ready for bookings</p>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            with col3:
                st.markdown('<div style="display: flex; flex-direction: column; height: 100%; justify-content: center;">', unsafe_allow_html=True)
                
                # Edit button
                st.markdown('<div class="primary-btn" style="margin-bottom: 0.5rem;">', unsafe_allow_html=True)
                if st.button("Edit", key=f"edit_{hall['hall_id']}"):
                    st.session_state["editing_hall"] = hall
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Delete button
                st.markdown('<div class="danger-btn">', unsafe_allow_html=True)
                if st.button("Delete", key=f"delete_{hall['hall_id']}"):
                    st.session_state[f"confirm_delete_{hall['hall_id']}"] = True
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Confirmation dialog for deletion
            if st.session_state.get(f"confirm_delete_{hall['hall_id']}", False):
                st.markdown(
                    f"""
                    <div style="background-color: #fef3c7; border-radius: 8px; padding: 1rem; margin-top: 1rem;">
                        <p style="color: #92400e; font-weight: 500;">⚠️ Are you sure you want to delete the hall at {hall['address']}?</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                col3, col4 = st.columns(2)
                with col3:
                    st.markdown('<div class="danger-btn">', unsafe_allow_html=True)
                    if st.button("Yes, Delete", key=f"confirm_yes_{hall['hall_id']}"):
                        cursor.execute("DELETE FROM Hall WHERE hall_id = %s", (hall['hall_id'],))
                        db.commit()
                        
                        st.markdown(
                            f"""
                            <div style="background-color: #fee2e2; border-radius: 8px; padding: 1rem; margin-top: 1rem;">
                                <p style="color: #b91c1c; font-weight: 500; margin: 0;">Hall at {hall['address']} has been deleted.</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        
                        # Clear the confirmation state
                        del st.session_state[f"confirm_delete_{hall['hall_id']}"]
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col4:
                    st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
                    if st.button("Cancel", key=f"confirm_no_{hall['hall_id']}"):
                        # Clear the confirmation state
                        del st.session_state[f"confirm_delete_{hall['hall_id']}"]
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Edit form if a hall is being edited
        if "editing_hall" in st.session_state:
            hall = st.session_state["editing_hall"]
            
            st.markdown(
                f"""
                <div class="card" style="border: 2px solid #1e3a8a;">
                    <h3 style="margin-top: 0;">Edit Hall: {hall['address']}</h3>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            with st.form(key=f"edit_form_{hall['hall_id']}"):
                new_address = st.text_input("Address", value=hall['address'])
                
                col1, col2 = st.columns(2)
                with col1:
                    new_price = st.number_input("Price Per Day (₹)", min_value=1000, value=int(hall['hall_price_per_day']))
                with col2:
                    new_capacity = st.number_input("Accommodation (people)", min_value=10, value=int(hall['hall_accommodation']))
                
                new_description = st.text_area("Description", value=hall['hall_description'], placeholder="Enter a brief description of the hall")
                
                col5, col6 = st.columns(2)
                with col5:
                    st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
                    update_btn = st.form_submit_button("Update Hall")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col6:
                    st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
                    cancel_btn = st.form_submit_button("Cancel")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                if update_btn:
                    if st.session_state.get(f"confirm_update_{hall['hall_id']}", False):
                        cursor.execute(
                            "UPDATE Hall SET address = %s, hall_price_per_day = %s, hall_accommodation = %s, hall_description = %s WHERE hall_id = %s",
                            (new_address, new_price, new_capacity, new_description,hall['hall_id'])
                        )
                        db.commit()
                        
                        st.session_state["hall_updated_success"] = f"✅ Hall at {new_address} has been updated successfully!"
                        del st.session_state["editing_hall"]
                        if f"confirm_update_{hall['hall_id']}" in st.session_state:
                            del st.session_state[f"confirm_update_{hall['hall_id']}"]
                        st.rerun()
                    else:
                        st.session_state[f"confirm_update_{hall['hall_id']}"] = True
                        
                        st.markdown(
                            """
                            <div style="background-color: #fef3c7; border-radius: 8px; padding: 1rem; margin-top: 1rem;">
                                <p style="color: #92400e; font-weight: 500; margin: 0;">⚠️ Please confirm your changes by clicking 'Update Hall' again.</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        
                        st.rerun()
                
                if cancel_btn:
                    # Clear the editing state
                    del st.session_state["editing_hall"]
                    if f"confirm_update_{hall['hall_id']}" in st.session_state:
                        del st.session_state[f"confirm_update_{hall['hall_id']}"]
                    st.rerun()
            
        db.close()
    
    with tab2:
        if "hall_added_success" in st.session_state:
            st.markdown(
                f"""
                <div style="background-color: #d1fae5; border-radius: 8px; padding: 1rem; margin-top: 1rem;">
                    <p style="color: #065f46; font-weight: 500; margin: 0;">{st.session_state['hall_added_success']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            del st.session_state["hall_added_success"]

        st.markdown(
            """
            <div class="card">
                <h3 style="margin-top: 0;">Add a New Hall</h3>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        with st.form("add_hall"):
            address = st.text_input("Address", placeholder="Enter the venue address")
            
            col1, col2 = st.columns(2)
            with col1:
                price = st.number_input("Price Per Day (₹)", min_value=1000, placeholder="Enter price per day")
            with col2:
                capacity = st.number_input("Accommodation (people)", min_value=10, placeholder="Enter max capacity")

            st.text("Hall Description (optional):")
            hall_description = st.text_area("Description", placeholder="Enter a brief description of the hall")
            st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
            submit_btn = st.form_submit_button("Add Hall")
            st.markdown('</div>', unsafe_allow_html=True)
            
            if submit_btn:
                if not address:
                    st.markdown(
                        """
                        <div style="background-color: #fee2e2; border-radius: 8px; padding: 1rem; margin-top: 1rem;">
                            <p style="color: #b91c1c; margin: 0;">❌ Please enter an address for the hall.</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    db = connect_db()
                    cursor = db.cursor()
                    cursor.execute("INSERT INTO Hall (organizer_id, hall_price_per_day, address, hall_accommodation,hall_description) VALUES (%s, %s, %s, %s, %s)",
                                (st.session_state["user_id"], price, address, capacity, hall_description))
                    db.commit()
                    db.close()

                    # ✅ Store success message in session state before rerunning
                    st.session_state["hall_added_success"] = f"✅ Hall at {address} has been added successfully! You can now receive bookings for this venue."
                    
                    st.rerun()  # Refresh the page

# Organizer: Manage Bookings
def manage_bookings():
    if not is_user_type("Organizer"):
        st.markdown(
            """
            <div style="background-color: #fee2e2; border-radius: 8px; padding: 1rem; margin: 2rem 0;">
                <p style="color: #b91c1c; font-weight: 500; margin: 0;">⚠️ Access denied. Please login as an Organizer.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        return
    
    st.markdown('<h2 class="decorated-header">Manage Bookings</h2>', unsafe_allow_html=True)
    
    # Create tabs for better organization
    tabs = st.tabs(["⏳ Pending Requests", "✅ Confirmed Bookings", "❌ Rejected Bookings"])
    
    db = connect_db()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    
    cursor.execute("SELECT hall_id FROM Hall WHERE organizer_id = %s", (st.session_state["user_id"],))
    halls = cursor.fetchall()
    
    if not halls:
        st.markdown(
            """
            <div style="background-color: #dbeafe; border-radius: 8px; padding: 1.5rem; margin: 1rem 0; text-align: center;">
                <span style="font-size: 3rem;">🏛️</span>
                <p style="color: #1e40af; font-weight: 500; margin-top: 1rem;">You don't have any halls yet. Add halls first to receive bookings.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        db.close()
        return
    
    # Get all halls owned by this organizer
    hall_ids = [hall['hall_id'] for hall in halls]
    
    # Pending Bookings Tab
    with tabs[0]:
        cursor.execute("""
            SELECT b.*, h.address, h.hall_price_per_day, c.first_name, c.last_name, c.phone_no, c.email
            FROM Booking b
            JOIN Hall h ON b.hall_id = h.hall_id
            JOIN Customer c ON b.customer_id = c.customer_id
            WHERE h.organizer_id = %s AND b.is_confirmed = False AND b.is_rejected = 0
            ORDER BY b.booking_date
        """, (st.session_state["user_id"],))
        
        pending_bookings = cursor.fetchall()
        
        if not pending_bookings:
            st.markdown(
                """
                <div style="background-color: #dbeafe; border-radius: 8px; padding: 1rem; margin: 1rem 0; text-align: center;">
                    <p style="color: #1e40af; font-weight: 500; margin: 0;">No pending booking requests at this time.</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        for booking in pending_bookings:
            with st.container():
                st.markdown(
                    f"""
                    <div class="card">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <h3>{booking['address']}</h3>
                            <span class="badge badge-warning">Pending</span>
                        </div>
                        <div style="display: grid; grid-template-columns: 3fr 1fr; gap: 1rem;">
                            <div>
                                <div class="data-row">
                                    <div class="data-label">Date:</div>
                                    <div class="data-value">{booking['booking_date']}</div>
                                </div>
                                <div class="data-row">
                                    <div class="data-label">Duration:</div>
                                    <div class="data-value">{booking['duration']} days</div>
                                </div>
                                <div class="data-row">
                                    <div class="data-label">Total Cost:</div>
                                    <div class="data-value price-display">₹{booking['total_cost']}</div>
                                </div>
                                <div class="data-row">
                                    <div class="data-label">Customer:</div>
                                    <div class="data-value">{booking['first_name']} {booking['last_name']}</div>
                                </div>
                                <div class="data-row">
                                    <div class="data-label">Contact:</div>
                                    <div class="data-value">{booking['phone_no']} | {booking['email']}</div>
                                </div>
                            </div>
                            <div>
                    """,
                    unsafe_allow_html=True
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
                    if st.button("Confirm", key=f"confirm_{booking['booking_id']}"):
                        cursor.execute("UPDATE Booking SET is_confirmed = 1 WHERE booking_id = %s", (booking['booking_id'],))
                        db.commit()
                        st.success(f"Booking confirmed! Customer {booking['first_name']} {booking['last_name']} will be notified.")
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col2:
                    st.markdown('<div class="danger-btn">', unsafe_allow_html=True)
                    if st.button("Reject", key=f"reject_{booking['booking_id']}"):
                        st.session_state[f"rejecting_{booking['booking_id']}"] = True
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown('</div></div>', unsafe_allow_html=True)
                
                # If rejection is triggered, show reason input
                if st.session_state.get(f"rejecting_{booking['booking_id']}", False):
                    st.markdown(
                        """
                        <div style="background-color: #fef3c7; border-radius: 8px; padding: 1rem; margin: 1rem 0;">
                            <p style="color: #92400e; font-weight: 500;">Are you sure you want to reject this booking request?</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                    rejection_reason = st.text_area("Provide a reason for rejection:", key=f"reason_{booking['booking_id']}")
                    
                    col3, col4 = st.columns(2)
                    with col3:
                        st.markdown('<div class="danger-btn">', unsafe_allow_html=True)
                        if st.button("Yes, Reject", key=f"confirm_reject_{booking['booking_id']}"):
                            if not rejection_reason.strip():
                                st.error("Please provide a reason for rejection.")
                            else:
                                cursor.execute("UPDATE Booking SET is_rejected = 1, rejection_reason = %s WHERE booking_id = %s", 
                                               (rejection_reason, booking['booking_id']))
                                db.commit()
                                st.warning(f"Booking rejected. Customer {booking['first_name']} {booking['last_name']} will be notified.")
                                del st.session_state[f"rejecting_{booking['booking_id']}"]
                                st.rerun()
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with col4:
                        st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
                        if st.button("Cancel", key=f"cancel_reject_{booking['booking_id']}"):
                            del st.session_state[f"rejecting_{booking['booking_id']}"]
                            st.rerun()
                        st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)

    # Confirmed Bookings Tab
    with tabs[1]:
        # Step 1: Delete expired confirmed bookings
        cursor.execute("""
            DELETE FROM Booking 
            WHERE is_confirmed = 1 
            AND is_rejected = 0
            AND DATE_ADD(booking_date, INTERVAL duration DAY) < CURDATE()
        """)
        db.commit()  # Apply deletion changes

        # Step 2: Fetch remaining confirmed bookings
        cursor.execute("""
            SELECT b.*, h.address, h.hall_price_per_day, c.first_name, c.last_name, c.phone_no, c.email
            FROM Booking b
            JOIN Hall h ON b.hall_id = h.hall_id
            JOIN Customer c ON b.customer_id = c.customer_id
            WHERE h.organizer_id = %s 
            AND b.is_confirmed = 1 
            AND b.is_rejected = 0
            ORDER BY b.booking_date
        """, (st.session_state["user_id"],))
        
        confirmed_bookings = cursor.fetchall()
        
        if not confirmed_bookings:
            st.markdown(
                """
                <div style="background-color: #dbeafe; border-radius: 8px; padding: 1rem; margin: 1rem 0; text-align: center;">
                    <p style="color: #1e40af; font-weight: 500; margin: 0;">No confirmed bookings at this time.</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        for booking in confirmed_bookings:
            with st.container():
                st.markdown(
                    f"""
                    <div class="card">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <h3>{booking['address']}</h3>
                            <span class="badge badge-success">Confirmed</span>
                        </div>
                        <div style="display: grid; grid-template-columns: 3fr 1fr; gap: 1rem;">
                            <div>
                                <div class="data-row">
                                    <div class="data-label">Date:</div>
                                    <div class="data-value">{booking['booking_date']}</div>
                                </div>
                                <div class="data-row">
                                    <div class="data-label">Duration:</div>
                                    <div class="data-value">{booking['duration']} days</div>
                                </div>
                                <div class="data-row">
                                    <div class="data-label">Total Cost:</div>
                                    <div class="data-value price-display">₹{booking['total_cost']}</div>
                                </div>
                                <div class="data-row">
                                    <div class="data-label">Customer:</div>
                                    <div class="data-value">{booking['first_name']} {booking['last_name']}</div>
                                </div>
                                <div class="data-row">
                                    <div class="data-label">Contact:</div>
                                    <div class="data-value">{booking['phone_no']} | {booking['email']}</div>
                                </div>
                            </div>
                            <div>
                    """,
                    unsafe_allow_html=True
                )
                
                st.markdown('<div class="danger-btn">', unsafe_allow_html=True)
                if st.button("Cancel Booking", key=f"cancel_{booking['booking_id']}"):
                    # Show confirmation dialog
                    st.session_state[f"cancelling_{booking['booking_id']}"] = True
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Cancellation confirmation
                if st.session_state.get(f"cancelling_{booking['booking_id']}", False):
                    st.markdown(
                        """
                        <div style="background-color: #fee2e2; border-radius: 8px; padding: 1rem; margin: 1rem 0;">
                            <p style="color: #b91c1c; font-weight: 500;">Are you sure you want to cancel this confirmed booking?</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                    cancellation_reason = st.text_area("Provide a reason for cancellation:", key=f"cancel_reason_{booking['booking_id']}")
                    
                    col5, col6 = st.columns(2)
                    with col5:
                        st.markdown('<div class="danger-btn">', unsafe_allow_html=True)
                        if st.button("Yes, Cancel", key=f"confirm_cancel_{booking['booking_id']}"):
                            if not cancellation_reason.strip():
                                st.error("Please provide a reason for cancellation.")
                            else:
                                cursor.execute("UPDATE Booking SET is_rejected = 1, rejection_reason = %s WHERE booking_id = %s", 
                                               (cancellation_reason, booking['booking_id']))
                                db.commit()
                                st.error(f"Booking cancelled. Customer {booking['first_name']} {booking['last_name']} will be notified.")
                                del st.session_state[f"cancelling_{booking['booking_id']}"]
                                st.rerun()
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with col6:
                        st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
                        if st.button("Keep Booking", key=f"keep_booking_{booking['booking_id']}"):
                            del st.session_state[f"cancelling_{booking['booking_id']}"]
                            st.rerun()
                        st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown('</div></div></div>', unsafe_allow_html=True)
  
    # Rejected Bookings Tab
    with tabs[2]:
        cursor.execute("""
            SELECT b.*, h.address, h.hall_price_per_day, c.first_name, c.last_name, c.phone_no, c.email, b.rejection_reason
            FROM Booking b
            JOIN Hall h ON b.hall_id = h.hall_id
            JOIN Customer c ON b.customer_id = c.customer_id
            WHERE h.organizer_id = %s AND b.is_rejected = 1
            ORDER BY b.booking_date DESC
        """, (st.session_state["user_id"],))
        
        rejected_bookings = cursor.fetchall()
        
        if not rejected_bookings:
            st.markdown(
                """
                <div style="background-color: #dbeafe; border-radius: 8px; padding: 1rem; margin: 1rem 0; text-align: center;">
                    <p style="color: #1e40af; font-weight: 500; margin: 0;">No rejected bookings in your history.</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        for booking in rejected_bookings:
            with st.container():
                st.markdown(
                    f"""
                    <div class="card">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <h3>{booking['address']}</h3>
                            <span class="badge badge-danger">Rejected</span>
                        </div>
                        <div>
                            <div class="data-row">
                                <div class="data-label">Date:</div>
                                <div class="data-value">{booking['booking_date']}</div>
                            </div>
                            <div class="data-row">
                                <div class="data-label">Duration:</div>
                                <div class="data-value">{booking['duration']} days</div>
                            </div>
                            <div class="data-row">
                                <div class="data-label">Total Cost:</div>
                                <div class="data-value price-display">₹{booking['total_cost']}</div>
                            </div>
                            <div class="data-row">
                                <div class="data-label">Customer:</div>
                                <div class="data-value">{booking['first_name']} {booking['last_name']}</div>
                            </div>
                            <div class="data-row">
                                <div class="data-label">Contact:</div>
                                <div class="data-value">{booking['phone_no']} | {booking['email']}</div>
                            </div>
                            <div style="margin-top: 1rem; padding: 0.75rem; background-color: #fee2e2; border-radius: 8px;">
                                <p style="font-weight: 500; color: #b91c1c; margin: 0;">Reason for rejection:</p>
                                <p style="margin-top: 0.5rem; margin-bottom: 0;">{booking['rejection_reason'] or 'Not provided'}</p>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    
    # Add a dashboard summary at the top
    st.markdown(
        """
        <script>
            // Add this script to the top of the page
            document.addEventListener('DOMContentLoaded', function() {
                const tabs = document.querySelectorAll('[data-baseweb="tab"]');
                if (tabs.length > 0) {
                    tabs.forEach(tab => {
                        tab.style.transition = 'all 0.3s ease';
                    });
                }
            });
        </script>
        """,
        unsafe_allow_html=True
    )
    
    db.close()
 
# Customer: Browse and Book Venues               
def browse_and_book():
    if not is_user_type("Customer"):
        st.markdown(
            """
            <div style="background-color: #fee2e2; border-radius: 8px; padding: 1rem; margin: 2rem 0;">
                <p style="color: #b91c1c; font-weight: 500; margin: 0;">⚠️ Access denied. Please login as a Customer.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        return
    
    if st.session_state.get('customer_booking_request', False):
        st.markdown(
                    f"""
                    <div style="background-color: #d1fae5; border-radius: 8px; padding: 1rem; margin-top: 1rem; text-align: center;">
                        <span style="font-size: 3rem;">🎉</span>
                        <h4 style="margin: 0.5rem 0; color: #065f46;">Booking Requested!</h4>
                        <p style="color: #065f46; margin: 0;">{st.session_state.get('customer_booking_request')}</p>
                        <p style="color: #065f46; margin: 0.5rem 0 0 0;">You'll be notified when they confirm your booking.</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        del st.session_state['customer_booking_request']
    
    st.markdown('<h2 class="decorated-header">Browse Venues</h2>', unsafe_allow_html=True)
    
    db = connect_db()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("""
        SELECT h.*, o.first_name, o.last_name, o.phone_no 
        FROM Hall h
        JOIN Organizer o ON h.organizer_id = o.organizer_id
    """)
    halls = cursor.fetchall()
    
    if not halls:
        st.markdown(
            """
            <div style="background-color: #dbeafe; border-radius: 8px; padding: 1.5rem; margin: 1rem 0; text-align: center;">
                <span style="font-size: 3rem;">🏛️</span>
                <p style="color: #1e40af; font-weight: 500; margin-top: 1rem;">No venues are available for booking at the moment.</p>
                <p style="color: #1e40af;">Please check back later.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Display halls in a modern card format
    for hall in halls:
        st.markdown(f'<div class="card">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            st.markdown(f'<h3 style="margin-top: 0;">{hall["address"]}</h3>', unsafe_allow_html=True)
            
            if hall["hall_description"]:
                    st.markdown("**Description**:",unsafe_allow_html=True)
                    st.markdown(
                        f"""
                        <div style="font-size: 0.9rem; color: #555; margin-bottom: 0.8rem; background: #f9fafb; padding: 0.8rem; border-radius: 5px; background: #f3f4f6;">
                            {hall["hall_description"]}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            
            st.markdown(
                f"""
                <div class="data-row">
                    <div class="data-label">Price:</div>
                    <div class="data-value price-display">₹{hall['hall_price_per_day']}</div>
                </div>
                <div class="data-row">
                    <div class="data-label">Capacity:</div>
                    <div class="data-value"><span class="badge badge-primary">{hall['hall_accommodation']} people</span></div>
                </div>
                <div class="data-row">
                    <div class="data-label">Organizer:</div>
                    <div class="data-value">{hall['first_name']} {hall['last_name']}</div>
                </div>
                <div class="data-row">
                    <div class="data-label">Contact:</div>
                    <div class="data-value">{hall['phone_no']}</div>
                </div>
                """, 
                unsafe_allow_html=True
            )
        
        with col2:
            # Visual representation of the hall
            st.markdown(
                """
                <div style="display: flex; align-items: center; height: 100%;">
                    <div style="background-color: #f0f9ff; border-radius: 8px; padding: 1rem; text-align: center; width: 100%;">
                        <span style="font-size: 2.5rem;">🏛️</span>
                        <p style="color: #1e40af; margin: 0.5rem 0 0 0;">Available for booking</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col3:
            st.markdown('<div style="display: flex; flex-direction: column; height: 100%; justify-content: center;">', unsafe_allow_html=True)
            st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
            if st.button(f"Book Now", key=f"book_{hall['hall_id']}"):
                st.session_state["booking_hall"] = hall
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Booking form if a hall is selected for booking
    if "booking_hall" in st.session_state:
        hall = st.session_state["booking_hall"]
        
        st.markdown(
            f"""
            <div class="card" style="border: 2px solid #1e3a8a; margin-top: 2rem;">
                <h3 style="margin-top: 0;">Book Venue: {hall['address']}</h3>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        with st.form(f"booking_form_{hall['hall_id']}"):
            st.markdown('<div class="card">', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                date = st.date_input("Booking Date", min_value=datetime.date.today())
            with col2:
                duration = st.number_input("Duration (days)", min_value=1, value=1)
            
            # Price negotiation with visual feedback
            price_negotiated = st.slider("Negotiate Price (₹)", 
                                        min_value=int(hall['hall_price_per_day']-hall['hall_price_per_day']*0.1), 
                                        max_value=int(hall['hall_price_per_day']), 
                                        value=int(hall['hall_price_per_day']))
            
            # Calculate total and show visual summary
            total_cost = duration * price_negotiated
            st.markdown(
                f"""
                <div style="background-color: #f0f9ff; border-radius: 8px; padding: 1rem; margin: 1rem 0;">
                    <h4 style="margin-top: 0; color: #1e40af;">Booking Summary</h4>
                    <div class="data-row">
                        <div class="data-label">Venue:</div>
                        <div class="data-value">{hall['address']}</div>
                    </div>
                    <div class="data-row">
                        <div class="data-label">Date:</div>
                        <div class="data-value">{date}</div>
                    </div>
                    <div class="data-row">
                        <div class="data-label">Duration:</div>
                        <div class="data-value">{duration} day{'s' if duration > 1 else ''}</div>
                    </div>
                    <div class="data-row">
                        <div class="data-label">Price per Day:</div>
                        <div class="data-value">₹{price_negotiated}</div>
                    </div>
                    <div class="data-row" style="margin-top: 0.5rem; border-top: 1px solid #dbeafe; padding-top: 0.5rem;">
                        <div class="data-label">Total Cost:</div>
                        <div class="price-display">₹{total_cost}</div>
                    </div>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            col3, col4 = st.columns(2)
            with col3:
                st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
                submit_btn = st.form_submit_button("Confirm Booking")
                st.markdown('</div>', unsafe_allow_html=True)
            with col4:
                st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
                cancel_btn = st.form_submit_button("Cancel")
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            if submit_btn:
                cursor.execute("INSERT INTO Booking (customer_id, hall_id, booking_date, duration, is_confirmed, total_cost) VALUES (%s, %s, %s, %s, %s, %s)",
                            (st.session_state["user_id"], hall['hall_id'], date, duration, False, total_cost))
                db.commit()
                st.session_state["customer_booking_request"] = f"Your request for {hall['address']} has been sent to the organizer."
                
                del st.session_state["booking_hall"]
                st.rerun()
            
            if cancel_btn:
                del st.session_state["booking_hall"]
                st.rerun()
    
    db.close()

# Customer: View Bookings
def view_bookings():
    if not is_user_type("Customer"):
        st.markdown(
            """
            <div style="background-color: #fee2e2; border-radius: 8px; padding: 1rem; margin: 2rem 0;">
                <p style="color: #b91c1c; font-weight: 500; margin: 0;">⚠️ Access denied. Please login as a Customer.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        return

    st.markdown('<h2 class="decorated-header">Your Bookings</h2>', unsafe_allow_html=True)

    # Create tabs for better organization
    tabs = st.tabs(["⏳ Pending Bookings", "✅ Confirmed Bookings", "❌ Rejected Bookings"])
    db = connect_db()
    cursor = db.cursor(pymysql.cursors.DictCursor)

    # Pending Bookings Tab
    with tabs[0]:
        cursor.execute("""
            SELECT b.*, h.address, h.hall_price_per_day, h.hall_accommodation, 
                   o.first_name as organizer_first_name, o.last_name as organizer_last_name, 
                   o.phone_no as organizer_phone
            FROM Booking b
            JOIN Hall h ON b.hall_id = h.hall_id
            JOIN Organizer o ON h.organizer_id = o.organizer_id
            WHERE b.customer_id = %s AND b.is_confirmed = False AND b.is_rejected = 0
            ORDER BY b.booking_date DESC
        """, (st.session_state["user_id"],))

        pending_bookings = cursor.fetchall()

        if not pending_bookings:
            st.markdown(
                """
                <div style="background-color: #dbeafe; border-radius: 8px; padding: 1.5rem; margin: 1rem 0; text-align: center;">
                    <span style="font-size: 3rem;">⏳</span>
                    <p style="color: #1e40af; font-weight: 500; margin-top: 1rem;">You don't have any pending bookings.</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        for booking in pending_bookings:
            st.markdown(f'<div class="card">', unsafe_allow_html=True)
            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown(
                    f"""
                    <h3 style="margin-top: 0; display: flex; align-items: center;">
                        {booking['address']} 
                        <span class="status-pending" style="margin-left: 0.75rem;">⏳ Pending</span>
                    </h3>
                    
                    <div class="data-row">
                        <div class="data-label">Date:</div>
                        <div class="data-value">{booking['booking_date'].strftime('%d %b %Y')}</div>
                    </div>
                    <div class="data-row">
                        <div class="data-label">Duration:</div>
                        <div class="data-value">{booking['duration']} day{'s' if booking['duration'] > 1 else ''}</div>
                    </div>
                    <div class="data-row">
                        <div class="data-label">Total Cost:</div>
                        <div class="data-value price-display">₹{booking['total_cost']}</div>
                    </div>
                    <div class="data-row">
                        <div class="data-label">Organizer:</div>
                        <div class="data-value">{booking['organizer_first_name']} {booking['organizer_last_name']}</div>
                    </div>
                    <div class="data-row">
                        <div class="data-label">Contact:</div>
                        <div class="data-value">{booking['organizer_phone']}</div>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )

            with col2:
                st.markdown('<div style="display: flex; flex-direction: column; height: 100%; justify-content: center;">', unsafe_allow_html=True)
                st.markdown('<div class="danger-btn">', unsafe_allow_html=True)
                if st.button("Cancel Booking", key=f"cancel_{booking['booking_id']}"):
                    st.session_state[f"confirm_cancel_{booking['booking_id']}"] = True
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            # Confirmation dialog for cancellation
            if st.session_state.get(f"confirm_cancel_{booking['booking_id']}", False):
                st.markdown(
                    f"""
                    <div style="background-color: #fef3c7; border-radius: 8px; padding: 1rem; margin-top: 1rem;">
                        <p style="color: #92400e; font-weight: 500;">⚠️ Are you sure you want to cancel your booking for {booking['address']}?</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                col3, col4 = st.columns(2)
                with col3:
                    st.markdown('<div class="danger-btn">', unsafe_allow_html=True)
                    if st.button("Yes, Cancel", key=f"confirm_yes_{booking['booking_id']}"):
                        cursor.execute("DELETE FROM Booking WHERE booking_id = %s", (booking['booking_id'],))
                        db.commit()
                        
                        st.markdown(
                            f"""
                            <div style="background-color: #fee2e2; border-radius: 8px; padding: 1rem; margin-top: 1rem;">
                                <p style="color: #b91c1c; font-weight: 500; margin: 0;">Booking for {booking['address']} has been cancelled.</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        
                        del st.session_state[f"confirm_cancel_{booking['booking_id']}"]
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col4:
                    st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
                    if st.button("Keep Booking", key=f"confirm_no_{booking['booking_id']}"):
                        del st.session_state[f"confirm_cancel_{booking['booking_id']}"]
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

    # Confirmed Bookings Tab
    with tabs[1]:
        cursor.execute("""
            SELECT b.*, h.address, h.hall_price_per_day, h.hall_accommodation, 
                   o.first_name as organizer_first_name, o.last_name as organizer_last_name, 
                   o.phone_no as organizer_phone
            FROM Booking b
            JOIN Hall h ON b.hall_id = h.hall_id
            JOIN Organizer o ON h.organizer_id = o.organizer_id
            WHERE b.customer_id = %s AND b.is_confirmed = True AND b.is_rejected = 0
            ORDER BY b.booking_date DESC
        """, (st.session_state["user_id"],))

        confirmed_bookings = cursor.fetchall()

        if not confirmed_bookings:
            st.markdown(
                """
                <div style="background-color: #dbeafe; border-radius: 8px; padding: 1.5rem; margin: 1rem 0; text-align: center;">
                    <span style="font-size: 3rem;">✅</span>
                    <p style="color: #1e40af; font-weight: 500; margin-top: 1rem;">You don't have any confirmed bookings.</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        for booking in confirmed_bookings:
            st.markdown(f'<div class="card">', unsafe_allow_html=True)
            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown(
                    f"""
                    <h3 style="margin-top: 0; display: flex; align-items: center;">
                        {booking['address']} 
                        <span class="status-confirmed" style="margin-left: 0.75rem;">✅ Confirmed</span>
                    </h3>
                    
                    <div class="data-row">
                        <div class="data-label">Date:</div>
                        <div class="data-value">{booking['booking_date'].strftime('%d %b %Y')}</div>
                    </div>
                    <div class="data-row">
                        <div class="data-label">Duration:</div>
                        <div class="data-value">{booking['duration']} day{'s' if booking['duration'] > 1 else ''}</div>
                    </div>
                    <div class="data-row">
                        <div class="data-label">Total Cost:</div>
                        <div class="data-value price-display">₹{booking['total_cost']}</div>
                    </div>
                    <div class="data-row">
                        <div class="data-label">Organizer:</div>
                        <div class="data-value">{booking['organizer_first_name']} {booking['organizer_last_name']}</div>
                    </div>
                    <div class="data-row">
                        <div class="data-label">Contact:</div>
                        <div class="data-value">{booking['organizer_phone']}</div>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )

            with col2:
                st.markdown(
                    """
                    <div style="display: flex; align-items: center; height: 100%;">
                        <div style="background-color: #d1fae5; border-radius: 8px; padding: 1rem; text-align: center; width: 100%;">
                            <span style="font-size: 2rem;">📝</span>
                            <p style="color: #065f46; margin: 0.5rem 0 0 0;">Ready to Go!</p>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            st.markdown('</div>', unsafe_allow_html=True)

    # Rejected Bookings Tab
    with tabs[2]:
        cursor.execute("""
            SELECT b.*, h.address, h.hall_price_per_day, h.hall_accommodation, 
                   o.first_name as organizer_first_name, o.last_name as organizer_last_name, 
                   o.phone_no as organizer_phone
            FROM Booking b
            JOIN Hall h ON b.hall_id = h.hall_id
            JOIN Organizer o ON h.organizer_id = o.organizer_id
            WHERE b.customer_id = %s AND b.is_rejected = 1
            ORDER BY b.booking_date DESC
        """, (st.session_state["user_id"],))

        rejected_bookings = cursor.fetchall()

        if not rejected_bookings:
            st.markdown(
                """
                <div style="background-color: #dbeafe; border-radius: 8px; padding: 1.5rem; margin: 1rem 0; text-align: center;">
                    <span style="font-size: 3rem;">❌</span>
                    <p style="color: #1e40af; font-weight: 500; margin-top: 1rem;">You don't have any rejected bookings.</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        for booking in rejected_bookings:
            if st.session_state.get(f"renegotiate_{booking['booking_id']}", False):
                with st.form(key=f"renegotiation_form_{booking['booking_id']}"):
                    st.markdown(
                        f"""
                        <div style="background-color: #fef3c7; border-radius: 8px; padding: 1rem; margin-top: 1rem;">
                            <p style="color: #92400e; font-weight: 500;">📌 Re-Negotiation for <strong>{booking['address']}</strong></p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    new_date = st.date_input("Select a new date", value=booking["booking_date"])
                    new_duration = st.number_input("Enter Duration (days)", min_value=1, max_value=30, value=booking["duration"])
                    new_price = st.number_input("Propose a new price", min_value=1, value=booking["total_cost"])


                    col1, col2 = st.columns(2)
                    with col1:
                        submitted = st.form_submit_button("Submit Request")
                    with col2:
                        cancel = st.form_submit_button("Cancel")

                if submitted:
                    cursor.execute(
                        """
                        UPDATE Booking 
                        SET booking_date = %s, duration = %s, total_cost = %s, is_rejected = 0
                        WHERE booking_id = %s
                        """,
                        (new_date, new_duration, new_price, booking['booking_id'])
                    )
                    db.commit()

                    st.success("✅ Your request has been submitted successfully!")
                    del st.session_state[f"renegotiate_{booking['booking_id']}"]
                    st.rerun()

                if cancel:
                    del st.session_state[f"renegotiate_{booking['booking_id']}"]
                    st.rerun()
            
            st.markdown(f'<div class="card">', unsafe_allow_html=True)
            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown(
                    f"""
                    <h3 style="margin-top: 0; display: flex; align-items: center;">
                        {booking['address']} 
                        <span class="status-rejected" style="margin-left: 0.75rem;">❌ Rejected</span>
                    </h3>
                    
                    <div class="data-row">
                        <div class="data-label">Date:</div>
                        <div class="data-value">{booking['booking_date'].strftime('%d %b %Y')}</div>
                    </div>
                    <div class="data-row">
                        <div class="data-label">Duration:</div>
                        <div class="data-value">{booking['duration']} day{'s' if booking['duration'] > 1 else ''}</div>
                    </div>
                    <div class="data-row">
                        <div class="data-label">Total Cost:</div>
                        <div class="data-value price-display">₹{booking['total_cost']}</div>
                    </div>
                    <div class="data-row">
                        <div class="data-label">Organizer:</div>
                        <div class="data-value">{booking['organizer_first_name']} {booking['organizer_last_name']}</div>
                    </div>
                    <div class="data-row">
                        <div class="data-label">Contact:</div>
                        <div class="data-value">{booking['organizer_phone']}</div>
                    </div>
                    
                    <div style="margin-top: 1rem; padding: 0.75rem; background-color: rgba(239, 68, 68, 0.05); border-radius: 8px; border-left: 3px solid #ef4444;">
                        <p style="margin: 0; color: #b91c1c; font-style: italic;">This booking was rejected by the organizer. You can try booking a different date or venue.</p>
                        <p style="margin-top: 0.5rem; margin-bottom: 0;">{booking['rejection_reason'] or 'Not provided'}</p>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )

            with col2:
                st.markdown('<div style="display: flex; flex-direction: column; height: 100%; justify-content: center;">', unsafe_allow_html=True)
                st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
                
                if st.button("Book Again", key=f"book_again_{booking['booking_id']}"):
                    st.session_state[f"renegotiate_{booking['booking_id']}"] = True

                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            
            st.markdown('</div>', unsafe_allow_html=True)

    db.close()
     
# Main Streamlit App
def main():
    apply_custom_css()
    
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    
    if is_authenticated():
        st.markdown(
            f"""
            <div class='user-info'>
                Logged in as: <b>{st.session_state.get('user_name', '')}</b> ({st.session_state['user_type']})
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    menu = ["🏠 Home"]
    if not is_authenticated():
        menu.extend(["🔑 Login", "📝 Register"])
    else:
        if st.session_state["user_type"] == "Organizer":
            menu.extend(["🏛 Manage Halls", "📅 Manage Bookings"])
        else:
            menu.extend(["🔍 Browse & Book", "📜 View Bookings"])
        menu.append("🚪 Logout")
    
    choice = st.selectbox("Navigation", menu, key="nav_menu")
    
    if choice == "🏠 Home":
        st.markdown(
            """
            <h1 class='welcome-title'>🎉 Welcome to the Event Management System! 🎉</h1>
            """,
            unsafe_allow_html=True,
        )
        if not is_authenticated():
            st.markdown(
                """
                <div class='login-prompt'>
                    Please <b>login</b> or <b>register</b> to continue.
                </div>
                """,
                unsafe_allow_html=True,
            )
        elif st.session_state["user_type"] == "Organizer":
            st.write("Use the menu to:")
            st.write("- Manage your halls")
            st.write("- View and confirm booking requests from customers")
        else:
            st.write("Use the menu to:")
            st.write("- Browse and book event halls")
            st.write("- View and manage your bookings")
    elif choice == "🔑 Login":
        user_type = st.selectbox("Login as", ["Customer", "Organizer"])
        login(user_type)
    elif choice == "📝 Register":
        user_type = st.selectbox("Register as", ["Customer", "Organizer"])
        register(user_type)
    elif choice == "🏛 Manage Halls":
        manage_halls()
    elif choice == "📅 Manage Bookings":
        manage_bookings()
    elif choice == "🔍 Browse & Book":
        browse_and_book()
    elif choice == "📜 View Bookings":
        view_bookings()
    elif choice == "🚪 Logout":
        st.session_state.clear()
        st.success("You have successfully logged out. Thank you for using the Event Management System!")
        st.rerun()

if __name__ == "__main__":
    main()