import streamlit as st
import json
import os
from datetime import datetime, timedelta
import re

# Page config
st.set_page_config(
    page_title="BookFlow - Library Management System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Professional Theme
st.markdown("""
<style>
    /* Main App Styling */
    .stApp {
        background: linear-gradient(135deg, #0f0f0f 0%, #1a1a1a 100%);
        color: #ffffff;
    }
    
    /* Global text color */
    .stMarkdown, .stText, p, span, div {
        color: #e0e0e0 !important;
    }
    
    /* Headers */
    .main-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #6C0345;
        text-align: center;
        padding: 0.5rem 0.3rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        background: linear-gradient(135deg, #6C0345 0%, #DC143C 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .sub-header {
        font-size: 0.85rem;
        font-weight: 500;
        color: #F7C566;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    /* Cards */
    .book-card {
        background: #1e1e1e;
        padding: 0.8rem;
        border-radius: 10px;
        border-left: 4px solid #6C0345;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .book-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 8px rgba(108, 3, 69, 0.4);
        background: #252525;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #6C0345 0%, #DC143C 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 8px rgba(108, 3, 69, 0.3);
        transition: transform 0.3s ease;
    }
    
    .stat-card:hover {
        transform: scale(1.03);
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #6C0345 0%, #DC143C 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        font-size: 0.9rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(108, 3, 69, 0.3);
    }
    
    /* Input Fields */
    .stTextInput>div>div>input, .stSelectbox>div>div>select {
        border-radius: 8px;
        border: 1px solid #444444;
        padding: 0.5rem;
        transition: border-color 0.3s ease;
        background: #2a2a2a !important;
        color: #ffffff !important;
        font-size: 0.9rem;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #6C0345;
        box-shadow: 0 0 0 2px rgba(108, 3, 69, 0.3);
    }
    
    /* Labels */
    .stTextInput>label, .stSelectbox>label, .stRadio>label {
        color: #ffffff !important;
    }
    
    /* Sidebar */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a1a 0%, #0f0f0f 100%) !important;
        border-right: 2px solid #6C0345;
    }
    
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    
    /* Success/Error/Info Boxes */
    .success-box {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border: 2px solid #28a745;
        border-radius: 10px;
        color: #155724;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(40, 167, 69, 0.1);
    }
    
    .error-box {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        border: 2px solid #dc3545;
        border-radius: 10px;
        color: #721c24;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(220, 53, 69, 0.1);
    }
    
    .info-box {
        background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
        border: 2px solid #17a2b8;
        border-radius: 10px;
        color: #0c5460;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(23, 162, 184, 0.1);
    }
    
    .warning-box {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        border: 2px solid #ffc107;
        border-radius: 10px;
        color: #856404;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(255, 193, 7, 0.1);
    }
    
    /* Metrics */
    .stMetric {
        background: #1e1e1e;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
        border: 1px solid #333333;
    }
    
    .stMetric label {
        color: #b0b0b0 !important;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: #ffffff !important;
    }
    
    /* Dataframe */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        background: #1e1e1e;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #2a2a2a;
        border-radius: 10px;
        font-weight: 600;
        color: #ffffff !important;
        border: 1px solid #444444;
    }
    
    .streamlit-expanderContent {
        background: #1e1e1e;
        border: 1px solid #444444;
        border-top: none;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #2a2a2a;
        border-radius: 10px 10px 0 0;
        padding: 0.8rem 1.5rem;
        font-weight: 600;
        color: #b0b0b0;
        border: 1px solid #444444;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #333333;
        color: #ffffff;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6C0345 0%, #DC143C 100%);
        color: white !important;
        border: 1px solid #6C0345;
    }
    
    /* Tab content */
    .stTabs [data-baseweb="tab-panel"] {
        background: transparent;
        padding-top: 1rem;
    }
    
    /* Divider */
    hr {
        margin: 2rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #6C0345, transparent);
    }
    
    /* Container */
    .element-container {
        margin-bottom: 1rem;
    }
    
    /* Radio Buttons */
    .stRadio > label {
        font-weight: 600;
        color: #ffffff !important;
    }
    
    .stRadio [role="radiogroup"] {
        background: #2a2a2a;
        padding: 0.5rem;
        border-radius: 10px;
        border: 1px solid #444444;
    }
    
    .stRadio [data-baseweb="radio"] {
        background: #2a2a2a;
    }
    
    /* Selectbox */
    .stSelectbox > label {
        font-weight: 600;
        color: #ffffff !important;
    }
    
    .stSelectbox [data-baseweb="select"] {
        background: #2a2a2a !important;
    }
    
    /* Containers */
    [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
        background: transparent;
    }
    
    /* Column containers */
    [data-testid="column"] {
        background: transparent;
    }
    
    /* ===== MOBILE RESPONSIVE ===== */
    @media (max-width: 768px) {
        /* Headers */
        .main-header {
            font-size: 2rem !important;
            padding: 1rem 0.5rem !important;
        }
        
        .sub-header {
            font-size: 1.2rem !important;
        }
        
        /* Buttons */
        .stButton>button {
            padding: 0.5rem 1rem !important;
            font-size: 0.9rem !important;
        }
        
        /* Cards */
        .book-card {
            padding: 1rem !important;
            margin: 0.5rem 0 !important;
        }
        
        .stat-card {
            padding: 1rem !important;
            margin: 0.5rem 0 !important;
        }
        
        /* Input Fields */
        .stTextInput>div>div>input {
            padding: 0.5rem !important;
            font-size: 0.9rem !important;
        }
        
        /* Metrics */
        .stMetric {
            padding: 0.5rem !important;
        }
        
        /* Columns - Stack on mobile */
        .row-widget.stHorizontal {
            flex-direction: column !important;
        }
        
        /* Expander */
        .streamlit-expanderHeader {
            font-size: 0.9rem !important;
            padding: 0.5rem !important;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab"] {
            padding: 0.5rem 1rem !important;
            font-size: 0.9rem !important;
        }
        
        /* Sidebar */
        .css-1d391kg {
            padding: 1rem 0.5rem !important;
        }
        
        /* Container spacing */
        .element-container {
            margin-bottom: 0.5rem !important;
        }
        
        /* Radio buttons */
        .stRadio > div {
            flex-direction: column !important;
        }
        
        /* Success/Error boxes */
        .success-box, .error-box, .info-box, .warning-box {
            padding: 1rem !important;
            font-size: 0.9rem !important;
        }
    }
    
    /* Small Mobile (< 480px) */
    @media (max-width: 480px) {
        .main-header {
            font-size: 1.5rem !important;
        }
        
        .sub-header {
            font-size: 1rem !important;
        }
        
        .stButton>button {
            padding: 0.4rem 0.8rem !important;
            font-size: 0.85rem !important;
        }
        
        /* Hide some decorative elements on very small screens */
        .book-card:hover {
            transform: none !important;
        }
    }
    
    /* Tablet (768px - 1024px) */
    @media (min-width: 768px) and (max-width: 1024px) {
        .main-header {
            font-size: 2.5rem !important;
        }
        
        .sub-header {
            font-size: 1.5rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

class BookFlowApp:
    def __init__(self):
        self.data_file = "bookflow_data.json"
        self.load_data()
    
    def load_data(self):
        """Load data from JSON file"""
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                self.users = data.get('users', self.get_default_users())
                self.books = data.get('books', self.get_default_books())
                self.transactions = data.get('transactions', [])
                self.migrate_user_contact_fields()
        except FileNotFoundError:
            self.users = self.get_default_users()
            self.books = self.get_default_books()
            self.transactions = []
            self.save_data()
    
    def migrate_user_contact_fields(self):
        """Add contact and email fields to existing users if missing"""
        updated = False
        for role in ['students', 'teachers', 'admin']:
            if role in self.users:
                for user in self.users[role]:
                    if 'contact' not in user:
                        user['contact'] = 'Not provided'
                        updated = True
                    if 'email' not in user:
                        user['email'] = 'Not provided'
                        updated = True
        if updated:
            self.save_data()
    
    def save_data(self):
        """Save data to JSON file"""
        data = {
            'users': self.users,
            'books': self.books,
            'transactions': self.transactions
        }
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=4)
    
    def get_default_users(self):
        return {
            'students': [
                {'id': 'E25CSEU1187', 'username': 'sairam', 'password': 'sairam123', 'name': 'Sairam R', 
                 'contact': '+91 9876543210', 'email': 'sairam@example.com'},
                {'id': 'B24ECE0045', 'username': 'student2', 'password': 'student123', 'name': 'Student 2',
                 'contact': '+91 9876543211', 'email': 'student2@example.com'}
            ],
            'teachers': [
                {'id': 'T25CSED101', 'username': 'prof_bohra', 'password': 'teacher123', 'name': 'Prof Bohra',
                 'contact': '+91 9876543220', 'email': 'bohra@example.com'},
                {'id': 'P24MATH205', 'username': 'prof_jd', 'password': 'teacher123', 'name': 'Prof JD',
                 'contact': '+91 9876543221', 'email': 'profjd@example.com'}
            ],
            'admin': [
                {'id': 'SHRUTI001', 'username': 'shruti', 'password': 'morningstar123', 'name': 'Administrator',
                 'contact': 'Not provided', 'email': 'Not provided'}
            ]
        }
    
    def get_default_books(self):
        return {
            'student_books': [
                {'id': 'B001', 'title': 'Pride & Prejudice', 'author': 'Jane Austen', 'copies': 3, 'available': 3},
                {'id': 'B002', 'title': 'Crime & Punishment', 'author': 'Dostoevsky', 'copies': 2, 'available': 2},
                {'id': 'B003', 'title': 'One Hundred Years of Solitude', 'author': 'Gabriel García Márquez', 'copies': 2, 'available': 2},
                {'id': 'B004', 'title': '1984', 'author': 'George Orwell', 'copies': 4, 'available': 4},
                {'id': 'B005', 'title': 'The Hunger Games', 'author': 'Suzanne Collins', 'copies': 3, 'available': 3},
            ],
            'teacher_books': [
                {'id': 'T001', 'title': 'R.D. Sharma Mathematics', 'author': 'R.D. Sharma', 'copies': 5, 'available': 5},
                {'id': 'T002', 'title': 'NCERT Science', 'author': 'NCERT', 'copies': 10, 'available': 10},
                {'id': 'T003', 'title': 'Psychology of Prejudice', 'author': 'Various', 'copies': 2, 'available': 2},
            ]
        }
    
    def verify_login(self, username, password, role):
        """Verify user credentials"""
        role_key = 'students' if role == 'student' else 'teachers' if role == 'teacher' else 'admin'
        users = self.users.get(role_key, [])
        
        for user in users:
            if user['username'] == username and user['password'] == password:
                return user
        return None

# Initialize app
if 'app' not in st.session_state:
    st.session_state.app = BookFlowApp()

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.role = None

def logout():
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.role = None
    st.rerun()

def login_page():
    """Display login page"""
    # Hero section with gradient - compact
    st.markdown("""
        <div style='background: linear-gradient(135deg, #6C0345 0%, #DC143C 100%); 
                    padding: 0.8rem 0.5rem; border-radius: 8px; margin-bottom: 1rem;
                    box-shadow: 0 2px 8px rgba(108, 3, 69, 0.3);'>
            <h1 style='color: white; text-align: center; font-size: 1.5rem; margin: 0; 
                       text-shadow: 2px 2px 4px rgba(0,0,0,0.2);'>
                📚 BookFlow LMS
            </h1>
            <p style='color: #F7C566; text-align: center; font-size: 0.8rem; margin: 0.3rem 0 0 0;
                      text-shadow: 1px 1px 2px rgba(0,0,0,0.2);'>
                Modern Library Management System
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Login card with shadow - dark theme
        st.markdown("""
            <div style='background: #1e1e1e; padding: 0.8rem; border-radius: 8px; 
                        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
                        border: 1px solid #333333;'>
                <h2 style='color: #ffffff; text-align: center; margin: 0; font-size: 1.1rem;'>
                    🔐 Welcome Back!
                </h2>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='margin: 0.5rem 0;'></div>", unsafe_allow_html=True)
        
        role = st.radio("**Select Your Role:**", ["Student", "Teacher"], horizontal=True)
        username = st.text_input("**Username**", placeholder="Enter your username", key="login_username")
        password = st.text_input("**Password**", type="password", placeholder="Enter your password", key="login_password")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            if st.button("🚀 Login", use_container_width=True, type="primary"):
                if username and password:
                    user = st.session_state.app.verify_login(username, password, role.lower())
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.user = user
                        st.session_state.role = role.lower()
                        st.success(f"✅ Welcome back, {user['name']}!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials! Please check your username and password.")
                else:
                    st.warning("⚠️ Please enter both username and password")
        
        with col_b:
            if st.button("📝 Create Account", use_container_width=True):
                st.session_state.page = 'register'
                st.rerun()
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Admin login link (hidden at bottom)
        if st.button("🔒 Admin Access", key="admin_link", help="For administrators only"):
            st.session_state.page = 'admin_login'
            st.rerun()

def admin_login_page():
    """Admin-only login page"""
    # Header with purple/red gradient like public page - compact
    st.markdown("""
        <div style='background: linear-gradient(135deg, #6C0345 0%, #DC143C 100%); 
                    padding: 0.8rem 0.5rem; border-radius: 8px; margin-bottom: 1rem;
                    box-shadow: 0 2px 8px rgba(108, 3, 69, 0.3);'>
            <h1 style='color: white; text-align: center; font-size: 1.5rem; margin: 0; 
                       text-shadow: 2px 2px 4px rgba(0,0,0,0.2);'>
                🔒 Admin Portal
            </h1>
            <p style='color: #F7C566; text-align: center; font-size: 0.8rem; margin: 0.3rem 0 0 0;
                      text-shadow: 1px 1px 2px rgba(0,0,0,0.2);'>
                Authorized Personnel Only
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
            <div style='background: #1e1e1e; padding: 0.8rem; border-radius: 8px; 
                        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
                        border: 1px solid #333333;'>
                <h2 style='color: #ffffff; text-align: center; margin: 0; font-size: 1.1rem;'>
                    🛡️ Administrator Login
                </h2>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='margin: 0.5rem 0;'></div>", unsafe_allow_html=True)
        
        username = st.text_input("**Admin Username**", placeholder="Enter admin username", key="admin_username")
        password = st.text_input("**Admin Password**", type="password", placeholder="Enter admin password", key="admin_password")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            if st.button("🔐 Admin Login", use_container_width=True, type="primary"):
                if username and password:
                    user = st.session_state.app.verify_login(username, password, 'admin')
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.user = user
                        st.session_state.role = 'admin'
                        st.success(f"✅ Welcome, Administrator {user['name']}!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid admin credentials! Access denied.")
                else:
                    st.warning("⚠️ Please enter both username and password")
        
        with col_b:
            if st.button("← Back to Login", use_container_width=True):
                st.session_state.page = 'login'
                st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Security warning
        st.warning("⚠️ **Security Notice:** This area is restricted to authorized administrators only. Unauthorized access attempts are logged.")

def register_page():
    """Display registration page"""
    st.markdown('<h1 class="main-header">📝 Register New Account</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        role = st.radio("Select Role:", ["Student", "Teacher"], horizontal=True)
        
        name = st.text_input("Full Name", placeholder="Enter your full name")
        username = st.text_input("Username", placeholder="Choose a username (min 3 chars)")
        password = st.text_input("Password", type="password", placeholder="Choose a password (min 6 chars)")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter password")
        
        if role == "Student":
            st.info("📋 Student ID Format: E25CSEU1187 (Letter + 2digits + 3-4letters + 4digits)")
            user_id = st.text_input("Student ID", placeholder="E25CSEU1187")
        else:
            st.info("📋 Teacher ID Format: T25CSED101 (Letter + 2digits + 4letters + 3digits)")
            user_id = st.text_input("Teacher ID", placeholder="T25CSED101")
        
        contact = st.text_input("Contact Number (Optional)", placeholder="+91 9876543210")
        email = st.text_input("Email (Optional)", placeholder="your.email@example.com")
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            if st.button("✅ Register", use_container_width=True):
                # Validation
                if not all([name, username, password, confirm_password, user_id]):
                    st.error("❌ All required fields must be filled!")
                elif len(username) < 3:
                    st.error("❌ Username must be at least 3 characters!")
                elif len(password) < 6:
                    st.error("❌ Password must be at least 6 characters!")
                elif password != confirm_password:
                    st.error("❌ Passwords do not match!")
                else:
                    # Validate ID format
                    user_id = user_id.upper()
                    if role == "Student":
                        if not re.match(r'^[A-Z]\d{2}[A-Z]{3,4}\d{4}$', user_id):
                            st.error("❌ Invalid Student ID format!")
                            st.stop()
                    else:
                        if not re.match(r'^[A-Z]\d{2}[A-Z]{4}\d{3}$', user_id):
                            st.error("❌ Invalid Teacher ID format!")
                            st.stop()
                    
                    # Check if username or ID exists
                    role_key = 'students' if role == 'Student' else 'teachers'
                    existing_users = st.session_state.app.users.get(role_key, [])
                    
                    if any(u['username'].lower() == username.lower() for u in existing_users):
                        st.error("❌ Username already exists!")
                    elif any(u['id'] == user_id for u in existing_users):
                        st.error("❌ ID already exists!")
                    else:
                        # Create new user
                        new_user = {
                            'id': user_id,
                            'username': username,
                            'password': password,
                            'name': name,
                            'contact': contact if contact else 'Not provided',
                            'email': email if email else 'Not provided'
                        }
                        
                        if role_key not in st.session_state.app.users:
                            st.session_state.app.users[role_key] = []
                        
                        st.session_state.app.users[role_key].append(new_user)
                        st.session_state.app.save_data()
                        
                        st.success(f"✅ Account created successfully! You can now login with username: {username}")
                        st.balloons()
        
        with col_b:
            if st.button("← Back to Login", use_container_width=True):
                st.session_state.page = 'login'
                st.rerun()

def show_books_page():
    """Display books catalog"""
    # Show celebration modals if triggered
    if st.session_state.get('show_borrow_success', False):
        show_borrow_celebration()
    
    if st.session_state.get('show_return_success', False):
        show_return_celebration(st.session_state.get('return_on_time', True))
    
    # Header with gradient - compact version
    st.markdown("""
        <div style='background: linear-gradient(135deg, #6C0345 0%, #DC143C 100%); 
                    padding: 0.6rem; border-radius: 8px; margin-bottom: 0.8rem;'>
            <h2 style='color: white; text-align: center; margin: 0; font-size: 1.2rem;'>📚 Book Catalog</h2>
            <p style='color: #F7C566; text-align: center; margin: 0.2rem 0 0 0; font-size: 0.75rem;'>
                Browse and borrow books from our collection
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Search bar with better styling
    col_search, col_filter = st.columns([3, 1])
    with col_search:
        search = st.text_input("🔍 Search books", placeholder="Search by title or author...", label_visibility="collapsed")
    with col_filter:
        st.write("")  # Spacing
    
    # Get books based on role
    if st.session_state.role == 'teacher':
        book_list = st.session_state.app.books['teacher_books']
    elif st.session_state.role == 'admin':
        book_list = st.session_state.app.books['student_books'] + st.session_state.app.books['teacher_books']
    else:
        book_list = st.session_state.app.books['student_books']
    
    # Filter books
    if search:
        book_list = [b for b in book_list if search.lower() in b['title'].lower() or search.lower() in b['author'].lower()]
    
    if not book_list:
        st.info("📭 No books found matching your search!")
        return
    
    st.markdown(f"<p style='color: #6C0345; font-weight: 600; margin: 1rem 0;'>Found {len(book_list)} book(s)</p>", unsafe_allow_html=True)
    
    # Display books in professional cards
    for book in book_list:
        # Determine availability status
        if book['available'] > 0:
            status_color = "#28a745"
            status_text = "Available"
            status_icon = "✅"
        else:
            status_color = "#dc3545"
            status_text = "Not Available"
            status_icon = "❌"
        
        # Create mobile-responsive dark card
        st.markdown(f"""
            <div style='background: #1e1e1e; padding: 1rem; border-radius: 10px; 
                        margin: 0.5rem 0; box-shadow: 0 2px 4px rgba(0,0,0,0.3);
                        border-left: 4px solid {status_color};
                        transition: all 0.3s ease;'>
                <div style='display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 1rem;'>
                    <div style='flex: 1; min-width: 200px;'>
                        <h3 style='color: #ffffff; margin: 0 0 0.3rem 0; font-size: 1.1rem;'>📖 {book['title']}</h3>
                        <p style='color: #b0b0b0; margin: 0 0 0.2rem 0; font-size: 0.9rem;'>✍️ {book['author']}</p>
                        <p style='color: #888888; margin: 0; font-size: 0.8rem;'>🆔 {book['id']}</p>
                    </div>
                    <div style='text-align: center; padding: 0 1rem; min-width: 100px;'>
                        <div style='background: {status_color}; color: white; padding: 0.4rem 0.8rem; 
                                    border-radius: 8px; font-weight: 600; font-size: 0.85rem;'>
                            {status_icon} {status_text}
                        </div>
                        <p style='margin: 0.4rem 0 0 0; font-size: 1.1rem; font-weight: 600; color: #ffffff;'>
                            {book['available']}/{book['copies']}
                        </p>
                        <p style='margin: 0; font-size: 0.75rem; color: #888888;'>Available</p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Action buttons - responsive layout
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button(f"📥 Borrow", key=f"borrow_{book['id']}", use_container_width=True):
                st.session_state[f"show_borrow_{book['id']}"] = True
        
        with col2:
            if st.button(f"👥 Who Has?", key=f"who_{book['id']}", use_container_width=True):
                st.session_state[f"show_who_{book['id']}"] = True
        
        with col3:
            if st.button(f"ℹ️ Details", key=f"details_{book['id']}", use_container_width=True):
                st.session_state[f"show_details_{book['id']}"] = True
        
        # Show modals if triggered
        if st.session_state.get(f"show_borrow_{book['id']}", False):
            show_borrow_modal(book)
        
        if st.session_state.get(f"show_who_{book['id']}", False):
            show_who_has_modal(book)
        
        if st.session_state.get(f"show_details_{book['id']}", False):
            show_details_modal(book)
        
        st.markdown("<br>", unsafe_allow_html=True)

@st.dialog("📥 Borrow Book")
def show_borrow_modal(book):
    """Show borrow confirmation modal"""
    # Book details in modal
    st.markdown(f"""
        <div style='background: #1e1e1e; padding: 1.5rem; border-radius: 10px; 
                    border-left: 4px solid #6C0345; margin-bottom: 1rem;'>
            <h3 style='color: #ffffff; margin: 0 0 0.5rem 0;'>📖 {book['title']}</h3>
            <p style='color: #b0b0b0; margin: 0;'>✍️ by {book['author']}</p>
            <p style='color: #888888; margin: 0.5rem 0 0 0; font-size: 0.9rem;'>🆔 {book['id']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Check if user already has this book
    already_borrowed = [t for t in st.session_state.app.transactions 
                       if t['user_id'] == st.session_state.user['id'] 
                       and t['book_id'] == book['id'] 
                       and t['status'] == 'borrowed']
    
    if already_borrowed:
        # Show error - already borrowed
        trans = already_borrowed[0]
        st.error(f"""
        ❌ **You Already Have This Book!**
        
        **Current Borrow Details:**
        - 📅 **Borrowed on:** {trans['borrow_date']}
        - ⏰ **Due date:** {trans['due_date']}
        - 📍 **Status:** Active
        
        💡 **Please return this book before borrowing it again!**
        """)
        
        if st.button("Close", use_container_width=True):
            st.session_state[f"show_borrow_{book['id']}"] = False
            st.rerun()
    
    # Availability status
    elif book['available'] > 0:
        st.success(f"✅ **Available:** {book['available']} of {book['copies']} copies")
        
        # Borrow details
        st.info(f"""
        **📅 Borrow Period:** 14 days  
        **📆 Due Date:** {(datetime.now() + timedelta(days=14)).strftime('%d %B %Y')}  
        **⚠️ Late Fee:** ₹10 per day after due date
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Confirm Borrow", use_container_width=True, type="primary"):
                success = borrow_book(book)
                st.session_state[f"show_borrow_{book['id']}"] = False
                if success:
                    st.session_state['show_borrow_success'] = True
                    st.session_state['borrowed_book_title'] = book['title']
                st.rerun()
        with col2:
            if st.button("❌ Cancel", use_container_width=True):
                st.session_state[f"show_borrow_{book['id']}"] = False
                st.rerun()
    else:
        st.error("❌ **Not Available** - All copies are currently borrowed")
        if st.button("Close", use_container_width=True):
            st.session_state[f"show_borrow_{book['id']}"] = False
            st.rerun()

@st.dialog("👥 Who Has This Book?")
def show_who_has_modal(book):
    """Show who has borrowed this book"""
    st.markdown(f"""
        <div style='background: #1e1e1e; padding: 1rem; border-radius: 10px; 
                    border-left: 4px solid #4facfe; margin-bottom: 1rem;'>
            <h4 style='color: #ffffff; margin: 0;'>📖 {book['title']}</h4>
            <p style='color: #b0b0b0; margin: 0.3rem 0 0 0; font-size: 0.9rem;'>by {book['author']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Get borrowers
    borrowers = [t for t in st.session_state.app.transactions 
                 if t['book_id'] == book['id'] and t['status'] == 'borrowed']
    
    if borrowers:
        st.markdown(f"**📊 Currently Borrowed:** {len(borrowers)} of {book['copies']} copies")
        st.divider()
        
        for trans in borrowers:
            # Find user details
            user_details = None
            for role in ['students', 'teachers']:
                user_details = next((u for u in st.session_state.app.users.get(role, []) 
                                   if u['id'] == trans['user_id']), None)
                if user_details:
                    break
            
            if user_details:
                st.markdown(f"""
                    <div style='background: #252525; padding: 1rem; border-radius: 8px; 
                                margin: 0.5rem 0; border-left: 3px solid #ffc107;'>
                        <p style='color: #ffffff; margin: 0; font-weight: 600;'>👤 {trans['user_name']}</p>
                        <p style='color: #b0b0b0; margin: 0.3rem 0 0 0; font-size: 0.85rem;'>
                            📧 {user_details.get('email', 'Not provided')} | 
                            📱 {user_details.get('contact', 'Not provided')}
                        </p>
                        <p style='color: #888888; margin: 0.3rem 0 0 0; font-size: 0.8rem;'>
                            📅 Borrowed: {trans['borrow_date']} | Due: {trans['due_date']}
                        </p>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.info("✅ All copies are available - No one has borrowed this book yet!")
    
    if st.button("Close", use_container_width=True):
        st.session_state[f"show_who_{book['id']}"] = False
        st.rerun()

@st.dialog("ℹ️ Book Details")
def show_details_modal(book):
    """Show complete book details"""
    # Book cover placeholder
    st.markdown("""
        <div style='background: linear-gradient(135deg, #6C0345 0%, #DC143C 100%); 
                    padding: 2rem; border-radius: 10px; text-align: center; margin-bottom: 1rem;'>
            <h1 style='color: white; margin: 0; font-size: 3rem;'>📚</h1>
        </div>
    """, unsafe_allow_html=True)
    
    # Book information
    st.markdown(f"""
        <div style='background: #1e1e1e; padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem;'>
            <h2 style='color: #ffffff; margin: 0 0 1rem 0;'>{book['title']}</h2>
            <p style='color: #b0b0b0; margin: 0.5rem 0;'><strong>✍️ Author:</strong> {book['author']}</p>
            <p style='color: #b0b0b0; margin: 0.5rem 0;'><strong>🆔 Book ID:</strong> {book['id']}</p>
            <p style='color: #b0b0b0; margin: 0.5rem 0;'><strong>📚 Total Copies:</strong> {book['copies']}</p>
            <p style='color: #b0b0b0; margin: 0.5rem 0;'><strong>✅ Available:</strong> {book['available']}</p>
            <p style='color: #b0b0b0; margin: 0.5rem 0;'><strong>📖 Borrowed:</strong> {book['copies'] - book['available']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Availability status
    if book['available'] > 0:
        st.success(f"✅ **Available for borrowing** ({book['available']} copies)")
    else:
        st.error("❌ **Currently unavailable** - All copies are borrowed")
    
    # Borrow info
    st.info("""
    **📋 Borrowing Information:**
    - Borrow period: 14 days
    - Late fee: ₹10 per day
    - Maximum renewals: 2 times
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        if book['available'] > 0:
            if st.button("📥 Borrow This Book", use_container_width=True, type="primary"):
                st.session_state[f"show_details_{book['id']}"] = False
                st.session_state[f"show_borrow_{book['id']}"] = True
                st.rerun()
    with col2:
        if st.button("Close", use_container_width=True):
            st.session_state[f"show_details_{book['id']}"] = False
            st.rerun()

def borrow_book(book):
    """Borrow a book"""
    if book['available'] <= 0:
        st.error(f"❌ '{book['title']}' is not available!")
        return False
    
    # Check if user already has this book
    active_borrows = [t for t in st.session_state.app.transactions 
                     if t['user_id'] == st.session_state.user['id'] 
                     and t['book_id'] == book['id'] 
                     and t['status'] == 'borrowed']
    
    if active_borrows:
        # Show detailed error with due date
        trans = active_borrows[0]
        st.error(f"""
        ❌ **Cannot Borrow - Already Borrowed!**
        
        You already have this book:
        - 📚 **Book:** {book['title']}
        - 📅 **Borrowed on:** {trans['borrow_date']}
        - ⏰ **Due date:** {trans['due_date']}
        
        💡 **Tip:** Please return this book before borrowing it again!
        """)
        return False
    
    # Create transaction
    due_date = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
    transaction = {
        'id': len(st.session_state.app.transactions) + 1,
        'user_id': st.session_state.user['id'],
        'user_name': st.session_state.user['name'],
        'book_id': book['id'],
        'book_title': book['title'],
        'borrow_date': datetime.now().strftime('%Y-%m-%d'),
        'due_date': due_date,
        'return_date': None,
        'status': 'borrowed',
        'fine': 0
    }
    
    st.session_state.app.transactions.append(transaction)
    book['available'] -= 1
    st.session_state.app.save_data()
    st.session_state['borrow_due_date'] = due_date
    
    return True

@st.dialog("🎉 Success!")
def show_borrow_celebration():
    """Show celebration for successful borrow"""
    st.markdown("""
        <div style='text-align: center; padding: 2rem;'>
            <h1 style='font-size: 4rem; margin: 0;'>🎉</h1>
            <h2 style='color: #28a745; margin: 1rem 0;'>Book Borrowed Successfully!</h2>
            <p style='font-size: 1.2rem; color: #ffffff;'>Happy Reading! 📚</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.success(f"""
    ✅ **{st.session_state.get('borrowed_book_title', 'Book')}** is now yours!
    
    📅 **Due Date:** {st.session_state.get('borrow_due_date', 'N/A')}  
    ⏰ **Remember:** Return on time to avoid late fees!
    """)
    
    st.balloons()
    
    if st.button("🎊 Awesome!", use_container_width=True, type="primary"):
        st.session_state['show_borrow_success'] = False
        st.rerun()

@st.dialog("🎊 Returned Successfully!")
def show_return_celebration(on_time=True):
    """Show celebration for successful return"""
    if on_time:
        st.markdown("""
            <div style='text-align: center; padding: 2rem;'>
                <h1 style='font-size: 4rem; margin: 0;'>🎊</h1>
                <h2 style='color: #28a745; margin: 1rem 0;'>Thank You!</h2>
                <p style='font-size: 1.2rem; color: #ffffff;'>Returned on time! 🌟</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.success(f"""
        ✅ **Book returned successfully!**
        
        🌟 **Great job!** You returned the book on time!  
        💚 **No late fees!** Keep up the good work!  
        📚 **Borrow more books** and keep reading!
        """)
        
        st.balloons()
    else:
        st.markdown("""
            <div style='text-align: center; padding: 2rem;'>
                <h1 style='font-size: 4rem; margin: 0;'>📚</h1>
                <h2 style='color: #ffc107; margin: 1rem 0;'>Book Returned</h2>
                <p style='font-size: 1.2rem; color: #ffffff;'>Thank you! ⏰</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.warning(f"""
        ✅ **Book returned successfully!**
        
        ⚠️ **Late Return:** Please check if any fine applies  
        💡 **Next time:** Try to return on time to avoid fees  
        📚 **Keep reading!**
        """)
    
    if st.button("👍 Got it!", use_container_width=True, type="primary"):
        st.session_state['show_return_success'] = False
        st.rerun()

def my_transactions_page():
    """Display user's transactions"""
    # Show celebration modal if triggered
    if st.session_state.get('show_return_success', False):
        show_return_celebration(st.session_state.get('return_on_time', True))
    
    st.markdown("## 📊 My Transactions")
    
    user_trans = [t for t in st.session_state.app.transactions 
                  if t['user_id'] == st.session_state.user['id']]
    
    if not user_trans:
        st.info("📭 No transactions yet!")
        return
    
    # Tabs for active and history
    tab1, tab2 = st.tabs(["📖 Active Borrows", "📜 History"])
    
    with tab1:
        active = [t for t in user_trans if t['status'] == 'borrowed']
        if active:
            for trans in active:
                with st.container():
                    col1, col2, col3 = st.columns([3, 2, 2])
                    
                    with col1:
                        st.markdown(f"**📚 {trans['book_title']}**")
                        st.caption(f"Book ID: {trans['book_id']}")
                    
                    with col2:
                        st.write(f"**Due:** {trans['due_date']}")
                        if trans['fine'] > 0:
                            st.error(f"Fine: ₹{trans['fine']}")
                    
                    with col3:
                        if st.button("↩️ Return", key=f"return_{trans['id']}"):
                            return_book(trans)
                    
                    st.divider()
        else:
            st.info("No active borrows")
    
    with tab2:
        history = [t for t in user_trans if t['status'] == 'returned']
        if history:
            # Display as table
            st.markdown("**Transaction History**")
            for trans in history:
                with st.container():
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.write(f"**{trans['book_title']}**")
                    with col2:
                        st.write(f"Borrowed: {trans['borrow_date']}")
                    with col3:
                        st.write(f"Returned: {trans['return_date']}")
                    with col4:
                        if trans['fine'] > 0:
                            st.error(f"Fine: ₹{trans['fine']}")
                        else:
                            st.success("No fine")
                    st.divider()
        else:
            st.info("No history yet")

def return_book(trans):
    """Return a book"""
    trans['status'] = 'returned'
    trans['return_date'] = datetime.now().strftime('%Y-%m-%d')
    
    # Calculate fine
    due_date = datetime.strptime(trans['due_date'], '%Y-%m-%d')
    return_date = datetime.now()
    days_late = (return_date - due_date).days
    
    on_time = days_late <= 0
    
    if days_late > 0:
        trans['fine'] = days_late * 10
    
    # Update book availability
    book_list = st.session_state.app.books['student_books'] if st.session_state.role != 'teacher' else st.session_state.app.books['teacher_books']
    if st.session_state.role == 'admin':
        book_list = st.session_state.app.books['student_books'] + st.session_state.app.books['teacher_books']
    
    book = next((b for b in book_list if b['id'] == trans['book_id']), None)
    if book:
        book['available'] += 1
    
    st.session_state.app.save_data()
    
    # Trigger celebration modal
    st.session_state['show_return_success'] = True
    st.session_state['return_on_time'] = on_time
    st.rerun()

def admin_dashboard():
    """Admin dashboard"""
    # Header with gradient - compact
    st.markdown("""
        <div style='background: linear-gradient(135deg, #6C0345 0%, #DC143C 100%); 
                    padding: 0.6rem; border-radius: 8px; margin-bottom: 0.8rem;'>
            <h2 style='color: white; text-align: center; margin: 0; font-size: 1.2rem;'>📊 Admin Dashboard</h2>
            <p style='color: #F7C566; text-align: center; margin: 0.2rem 0 0 0; font-size: 0.75rem;'>
                Complete library overview and management
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Statistics with enhanced cards
    col1, col2, col3, col4 = st.columns(4)
    
    total_users = len(st.session_state.app.users.get('students', [])) + len(st.session_state.app.users.get('teachers', []))
    total_books = len(st.session_state.app.books['student_books']) + len(st.session_state.app.books['teacher_books'])
    active_borrows = len([t for t in st.session_state.app.transactions if t['status'] == 'borrowed'])
    total_fines = sum(t['fine'] for t in st.session_state.app.transactions)
    
    with col1:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 0.8rem; border-radius: 8px; text-align: center;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 0.5rem;'>
                <h3 style='color: white; margin: 0; font-size: 1.5rem;'>{total_users}</h3>
                <p style='color: white; margin: 0.3rem 0 0 0; font-size: 0.8rem; opacity: 0.9;'>👥 Users</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                        padding: 0.8rem; border-radius: 8px; text-align: center;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 0.5rem;'>
                <h3 style='color: white; margin: 0; font-size: 1.5rem;'>{total_books}</h3>
                <p style='color: white; margin: 0.3rem 0 0 0; font-size: 0.8rem; opacity: 0.9;'>📚 Books</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                        padding: 0.8rem; border-radius: 8px; text-align: center;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 0.5rem;'>
                <h3 style='color: white; margin: 0; font-size: 1.5rem;'>{active_borrows}</h3>
                <p style='color: white; margin: 0.3rem 0 0 0; font-size: 0.8rem; opacity: 0.9;'>📖 Borrows</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); 
                        padding: 0.8rem; border-radius: 8px; text-align: center;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 0.5rem;'>
                <h3 style='color: white; margin: 0; font-size: 1.5rem;'>₹{total_fines}</h3>
                <p style='color: white; margin: 0.3rem 0 0 0; font-size: 0.8rem; opacity: 0.9;'>💰 Fines</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["📚 Manage Books", "👥 Manage Users", "📈 Transactions"])
    
    with tab1:
        manage_books_admin()
    
    with tab2:
        manage_users_admin()
    
    with tab3:
        view_all_transactions()

def manage_books_admin():
    """Admin book management"""
    st.markdown("### 📚 Book Management")
    
    # Add new book
    with st.expander("➕ Add New Book"):
        col1, col2 = st.columns(2)
        with col1:
            book_id = st.text_input("Book ID", key="new_book_id")
            title = st.text_input("Title", key="new_book_title")
            author = st.text_input("Author", key="new_book_author")
        with col2:
            copies = st.number_input("Copies", min_value=1, value=1, key="new_book_copies")
            category = st.selectbox("Category", ["Student", "Teacher"], key="new_book_cat")
        
        if st.button("💾 Add Book"):
            if all([book_id, title, author]):
                new_book = {
                    'id': book_id.upper(),
                    'title': title,
                    'author': author,
                    'copies': copies,
                    'available': copies
                }
                
                book_list = st.session_state.app.books['student_books'] if category == 'Student' else st.session_state.app.books['teacher_books']
                book_list.append(new_book)
                st.session_state.app.save_data()
                st.success("✅ Book added successfully!")
                st.rerun()
            else:
                st.error("❌ All fields required!")
    
    # List all books
    st.markdown("### 📖 All Books")
    all_books = st.session_state.app.books['student_books'] + st.session_state.app.books['teacher_books']
    
    for book in all_books:
        with st.container():
            col1, col2, col3 = st.columns([3, 2, 1])
            
            with col1:
                st.write(f"**{book['title']}** by {book['author']}")
                st.caption(f"ID: {book['id']}")
            
            with col2:
                st.write(f"Available: {book['available']}/{book['copies']}")
            
            with col3:
                if st.button("🗑️", key=f"del_book_{book['id']}"):
                    # Check if borrowed
                    active = [t for t in st.session_state.app.transactions if t['book_id'] == book['id'] and t['status'] == 'borrowed']
                    if active:
                        st.error("Cannot delete - book is borrowed!")
                    else:
                        # Remove book
                        st.session_state.app.books['student_books'] = [b for b in st.session_state.app.books['student_books'] if b['id'] != book['id']]
                        st.session_state.app.books['teacher_books'] = [b for b in st.session_state.app.books['teacher_books'] if b['id'] != book['id']]
                        st.session_state.app.save_data()
                        st.success("✅ Book deleted!")
                        st.rerun()
            
            st.divider()

def manage_users_admin():
    """Admin user management"""
    st.markdown("### 👥 User Management")
    
    # Add new user section
    with st.expander("➕ Add New User"):
        col1, col2 = st.columns(2)
        with col1:
            new_name = st.text_input("Full Name", key="new_user_name")
            new_username = st.text_input("Username", key="new_user_username")
            new_password = st.text_input("Password", type="password", key="new_user_password")
            new_id = st.text_input("User ID", key="new_user_id")
        with col2:
            new_role = st.selectbox("Role", ["Student", "Teacher"], key="new_user_role")
            new_contact = st.text_input("Contact", key="new_user_contact")
            new_email = st.text_input("Email", key="new_user_email")
        
        if st.button("💾 Add User", use_container_width=True):
            if all([new_name, new_username, new_password, new_id]):
                # Check for duplicates
                role_key = 'students' if new_role == 'Student' else 'teachers'
                existing = any(u['username'] == new_username or u['id'] == new_id 
                             for role in ['students', 'teachers'] 
                             for u in st.session_state.app.users.get(role, []))
                
                if existing:
                    st.error("❌ Username or ID already exists!")
                else:
                    new_user = {
                        'id': new_id.upper(),
                        'name': new_name,
                        'username': new_username,
                        'password': new_password,
                        'contact': new_contact,
                        'email': new_email
                    }
                    st.session_state.app.users[role_key].append(new_user)
                    st.session_state.app.save_data()
                    st.success(f"✅ User {new_name} added successfully!")
                    st.rerun()
            else:
                st.error("❌ Name, Username, Password, and ID are required!")
    
    st.divider()
    
    # List all users with edit/delete
    all_users = []
    for role in ['students', 'teachers']:
        for user in st.session_state.app.users.get(role, []):
            all_users.append({**user, 'role': role})
    
    if all_users:
        st.markdown(f"**Total Users:** {len(all_users)} (Students: {len(st.session_state.app.users.get('students', []))}, Teachers: {len(st.session_state.app.users.get('teachers', []))})")
        st.divider()
        
        # Display users in dark cards
        for idx, user in enumerate(all_users):
            st.markdown(f"""
                <div style='background: #1e1e1e; padding: 1rem; border-radius: 10px; 
                            margin: 0.5rem 0; border-left: 4px solid #6C0345;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.3);'>
                    <p style='color: #ffffff; margin: 0; font-weight: 600; font-size: 1.1rem;'>👤 {user['name']}</p>
                    <p style='color: #b0b0b0; margin: 0.3rem 0 0 0; font-size: 0.9rem;'>
                        🆔 {user['id']} | 👨‍💼 {user['role'].title()} | 📧 {user.get('email', 'N/A')} | 📱 {user.get('contact', 'N/A')}
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 1, 3])
            with col1:
                if st.button("✏️ Edit", key=f"edit_user_{idx}", use_container_width=True):
                    st.session_state[f'editing_user_{idx}'] = True
                    st.rerun()
            with col2:
                if st.button("🗑️ Delete", key=f"delete_user_{idx}", use_container_width=True):
                    # Check for active borrows
                    active_borrows = [t for t in st.session_state.app.transactions 
                                    if t['user_id'] == user['id'] and t['status'] == 'borrowed']
                    if active_borrows:
                        st.error(f"❌ Cannot delete! {user['name']} has {len(active_borrows)} active borrow(s)")
                    else:
                        st.session_state.app.users[user['role']] = [u for u in st.session_state.app.users[user['role']] if u['id'] != user['id']]
                        st.session_state.app.save_data()
                        st.success(f"✅ User {user['name']} deleted!")
                        st.rerun()
            
            # Edit form
            if st.session_state.get(f'editing_user_{idx}', False):
                with st.expander(f"✏️ Edit {user['name']}", expanded=True):
                    col_a, col_b = st.columns(2)
                    with col_a:
                        edit_name = st.text_input("Name", value=user['name'], key=f"edit_name_{idx}")
                        edit_username = st.text_input("Username", value=user['username'], key=f"edit_username_{idx}")
                        edit_password = st.text_input("Password", value=user['password'], type="password", key=f"edit_password_{idx}")
                    with col_b:
                        edit_contact = st.text_input("Contact", value=user.get('contact', ''), key=f"edit_contact_{idx}")
                        edit_email = st.text_input("Email", value=user.get('email', ''), key=f"edit_email_{idx}")
                    
                    col_save, col_cancel = st.columns(2)
                    with col_save:
                        if st.button("💾 Save Changes", key=f"save_{idx}", use_container_width=True):
                            # Update user
                            for u in st.session_state.app.users[user['role']]:
                                if u['id'] == user['id']:
                                    u['name'] = edit_name
                                    u['username'] = edit_username
                                    u['password'] = edit_password
                                    u['contact'] = edit_contact
                                    u['email'] = edit_email
                                    break
                            st.session_state.app.save_data()
                            st.session_state[f'editing_user_{idx}'] = False
                            st.success("✅ User updated successfully!")
                            st.rerun()
                    with col_cancel:
                        if st.button("❌ Cancel", key=f"cancel_{idx}", use_container_width=True):
                            st.session_state[f'editing_user_{idx}'] = False
                            st.rerun()
            
            st.divider()
    else:
        st.info("No users found")

def view_all_transactions():
    """View all transactions"""
    st.markdown("### 📈 All Transactions")
    
    if st.session_state.app.transactions:
        # Display transactions in dark cards
        for trans in st.session_state.app.transactions:
            status_color = "#28a745" if trans['status'] == 'returned' else "#ffc107"
            st.markdown(f"""
                <div style='background: #1e1e1e; padding: 1rem; border-radius: 10px; 
                            margin: 0.5rem 0; border-left: 4px solid {status_color};
                            box-shadow: 0 2px 4px rgba(0,0,0,0.3);'>
                    <p style='color: #ffffff; margin: 0; font-weight: 600;'>{trans['user_name']} - {trans['book_title']}</p>
                    <p style='color: #b0b0b0; margin: 0.3rem 0 0 0; font-size: 0.85rem;'>
                        📅 Borrowed: {trans['borrow_date']} | Due: {trans['due_date']} | 
                        Status: <span style='color: {status_color};'>{trans['status'].title()}</span>
                    </p>
                    {f"<p style='color: #dc3545; margin: 0.3rem 0 0 0; font-weight: 600;'>💰 Fine: ₹{trans['fine']}</p>" if trans['fine'] > 0 else ""}
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No transactions yet")

def main():
    """Main application"""
    
    # Check if page state exists
    if 'page' not in st.session_state:
        st.session_state.page = 'login'
    
    # Not logged in
    if not st.session_state.logged_in:
        if st.session_state.page == 'register':
            register_page()
        elif st.session_state.page == 'admin_login':
            admin_login_page()
        else:
            login_page()
        return
    
    # Logged in - Show sidebar
    with st.sidebar:
        # Compact user info
        st.markdown(f"""
            <div style='background: #1e1e1e; padding: 0.8rem; border-radius: 8px; margin-bottom: 1rem;
                        border-left: 3px solid #6C0345;'>
                <p style='margin: 0; font-size: 1rem; font-weight: 600; color: #ffffff;'>👤 {st.session_state.user['name']}</p>
                <p style='margin: 0.2rem 0 0 0; font-size: 0.8rem; color: #b0b0b0;'>{st.session_state.role.title()} • {st.session_state.user['id']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**Navigation**")
        if st.session_state.role == 'admin':
            menu = st.radio("", ["📊 Dashboard", "📚 Books", "🚪 Logout"], label_visibility="collapsed")
        else:
            menu = st.radio("", ["📚 View Books", "📊 My Transactions", "🚪 Logout"], label_visibility="collapsed")
        
        if menu == "🚪 Logout":
            logout()
    
    # Main content
    if st.session_state.role == 'admin':
        if menu == "📊 Dashboard":
            admin_dashboard()
        elif menu == "📚 Books":
            show_books_page()
    else:
        if menu == "📚 View Books":
            show_books_page()
        elif menu == "📊 My Transactions":
            my_transactions_page()

if __name__ == "__main__":
    main()
