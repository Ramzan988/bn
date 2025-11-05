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
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Headers */
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        color: #6C0345;
        text-align: center;
        padding: 2rem 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        background: linear-gradient(135deg, #6C0345 0%, #DC143C 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .sub-header {
        font-size: 1.8rem;
        font-weight: 600;
        color: #F7C566;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    /* Cards */
    .book-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #6C0345;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .book-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(108, 3, 69, 0.2);
    }
    
    .stat-card {
        background: linear-gradient(135deg, #6C0345 0%, #DC143C 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 8px 16px rgba(108, 3, 69, 0.3);
        transition: transform 0.3s ease;
    }
    
    .stat-card:hover {
        transform: scale(1.05);
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #6C0345 0%, #DC143C 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(108, 3, 69, 0.3);
    }
    
    /* Input Fields */
    .stTextInput>div>div>input {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 0.75rem;
        transition: border-color 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #6C0345;
        box-shadow: 0 0 0 2px rgba(108, 3, 69, 0.1);
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #6C0345 0%, #DC143C 100%);
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
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Dataframe */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 10px;
        font-weight: 600;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: white;
        border-radius: 10px 10px 0 0;
        padding: 1rem 2rem;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6C0345 0%, #DC143C 100%);
        color: white;
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
        color: #6C0345;
    }
    
    /* Selectbox */
    .stSelectbox > label {
        font-weight: 600;
        color: #6C0345;
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
                {'id': 'ADMIN001', 'username': 'admin', 'password': 'admin123', 'name': 'Administrator',
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
    # Hero section with gradient
    st.markdown("""
        <div style='background: linear-gradient(135deg, #6C0345 0%, #DC143C 100%); 
                    padding: 4rem 2rem; border-radius: 20px; margin-bottom: 3rem;
                    box-shadow: 0 10px 30px rgba(108, 3, 69, 0.3);'>
            <h1 style='color: white; text-align: center; font-size: 4rem; margin: 0; 
                       text-shadow: 2px 2px 4px rgba(0,0,0,0.2);'>
                📚 BookFlow LMS
            </h1>
            <p style='color: #F7C566; text-align: center; font-size: 1.5rem; margin: 1rem 0 0 0;
                      text-shadow: 1px 1px 2px rgba(0,0,0,0.2);'>
                Modern Library Management System
            </p>
            <p style='color: white; text-align: center; font-size: 1rem; margin: 0.5rem 0 0 0; opacity: 0.9;'>
                Borrow, Return, and Manage Books with Ease
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Login card with shadow
        st.markdown("""
            <div style='background: white; padding: 2.5rem; border-radius: 20px; 
                        box-shadow: 0 10px 30px rgba(0,0,0,0.1);'>
                <h2 style='color: #6C0345; text-align: center; margin: 0 0 2rem 0;'>
                    🔐 Welcome Back!
                </h2>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        role = st.radio("**Select Your Role:**", ["Student", "Teacher", "Admin"], horizontal=True)
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
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Demo credentials in styled box
        st.markdown("""
            <div style='background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); 
                        padding: 1.5rem; border-radius: 15px; border-left: 4px solid #2196F3;
                        margin-top: 2rem;'>
                <h4 style='color: #1976d2; margin: 0 0 1rem 0;'>💡 Demo Credentials</h4>
                <p style='margin: 0.5rem 0; color: #0d47a1;'><strong>Student:</strong> sairam / sairam123</p>
                <p style='margin: 0.5rem 0; color: #0d47a1;'><strong>Teacher:</strong> prof_bohra / teacher123</p>
                <p style='margin: 0.5rem 0; color: #0d47a1;'><strong>Admin:</strong> admin / admin123</p>
            </div>
        """, unsafe_allow_html=True)

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
    # Header with gradient
    st.markdown("""
        <div style='background: linear-gradient(135deg, #6C0345 0%, #DC143C 100%); 
                    padding: 2rem; border-radius: 15px; margin-bottom: 2rem;'>
            <h1 style='color: white; text-align: center; margin: 0;'>📚 Book Catalog</h1>
            <p style='color: #F7C566; text-align: center; margin: 0.5rem 0 0 0;'>
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
        
        # Create card with gradient border
        st.markdown(f"""
            <div style='background: white; padding: 1.5rem; border-radius: 15px; 
                        margin: 1rem 0; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                        border-left: 5px solid {status_color};
                        transition: transform 0.3s ease;'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <div style='flex: 1;'>
                        <h3 style='color: #6C0345; margin: 0 0 0.5rem 0;'>📖 {book['title']}</h3>
                        <p style='color: #6c757d; margin: 0 0 0.5rem 0;'>✍️ by {book['author']}</p>
                        <p style='color: #6c757d; margin: 0; font-size: 0.9rem;'>🆔 {book['id']}</p>
                    </div>
                    <div style='text-align: center; padding: 0 2rem;'>
                        <div style='background: {status_color}; color: white; padding: 0.5rem 1rem; 
                                    border-radius: 10px; font-weight: 600;'>
                            {status_icon} {status_text}
                        </div>
                        <p style='margin: 0.5rem 0 0 0; font-size: 1.2rem; font-weight: 600; color: #6C0345;'>
                            {book['available']}/{book['copies']}
                        </p>
                        <p style='margin: 0; font-size: 0.8rem; color: #6c757d;'>Available/Total</p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Action buttons
        col1, col2, col3, col4 = st.columns([2, 2, 2, 6])
        
        with col1:
            if st.button(f"📥 Borrow", key=f"borrow_{book['id']}", use_container_width=True):
                borrow_book(book)
        
        with col2:
            if st.button(f"👥 Who Has?", key=f"who_{book['id']}", use_container_width=True):
                show_borrowers(book)
        
        with col3:
            if st.button(f"ℹ️ Details", key=f"details_{book['id']}", use_container_width=True):
                st.info(f"**Book Details:**\n\n📖 Title: {book['title']}\n✍️ Author: {book['author']}\n🆔 ID: {book['id']}\n📚 Total Copies: {book['copies']}\n✅ Available: {book['available']}")
        
        st.markdown("<br>", unsafe_allow_html=True)

def borrow_book(book):
    """Borrow a book"""
    if book['available'] <= 0:
        st.error(f"❌ '{book['title']}' is not available!")
        return
    
    # Check if user already has this book
    active_borrows = [t for t in st.session_state.app.transactions 
                     if t['user_id'] == st.session_state.user['id'] 
                     and t['book_id'] == book['id'] 
                     and t['status'] == 'borrowed']
    
    if active_borrows:
        st.error("❌ You already have this book!")
        return
    
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
    
    st.success(f"✅ Book borrowed successfully! Due date: {due_date}")
    st.balloons()
    st.rerun()

def show_borrowers(book):
    """Show who has borrowed the book"""
    borrowers = [t for t in st.session_state.app.transactions 
                if t['book_id'] == book['id'] and t['status'] == 'borrowed']
    
    if not borrowers:
        st.info(f"✅ '{book['title']}' is currently available! You can borrow it directly.")
        return
    
    st.markdown(f"### 👥 Who Has '{book['title']}'?")
    st.info(f"💡 Currently borrowed by {len(borrowers)} user(s). You can contact them to request early return.")
    
    for trans in borrowers:
        # Find user
        user = None
        for role in ['students', 'teachers']:
            user = next((u for u in st.session_state.app.users.get(role, []) if u['id'] == trans['user_id']), None)
            if user:
                break
        
        with st.expander(f"👤 {trans['user_name']} (ID: {trans['user_id']})"):
            st.write(f"**📅 Due Date:** {trans['due_date']}")
            
            if user:
                st.markdown("**📞 Contact Information:**")
                if user.get('contact', 'Not provided') != 'Not provided':
                    st.write(f"📱 Phone: {user['contact']}")
                if user.get('email', 'Not provided') != 'Not provided':
                    st.write(f"📧 Email: {user['email']}")
                if user.get('contact') == 'Not provided' and user.get('email') == 'Not provided':
                    st.caption("Contact info not available")

def my_transactions_page():
    """Display user's transactions"""
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
    
    if days_late > 0:
        trans['fine'] = days_late * 10
    
    # Update book availability
    book_list = st.session_state.app.books['student_books'] if st.session_state.role != 'teacher' else st.session_state.app.books['teacher_books']
    book = next((b for b in book_list if b['id'] == trans['book_id']), None)
    if book:
        book['available'] += 1
    
    st.session_state.app.save_data()
    st.success("✅ Book returned successfully!")
    if trans['fine'] > 0:
        st.warning(f"⚠️ Late return fine: ₹{trans['fine']}")
    st.rerun()

def admin_dashboard():
    """Admin dashboard"""
    # Header with gradient
    st.markdown("""
        <div style='background: linear-gradient(135deg, #6C0345 0%, #DC143C 100%); 
                    padding: 2rem; border-radius: 15px; margin-bottom: 2rem;'>
            <h1 style='color: white; text-align: center; margin: 0;'>📊 Admin Dashboard</h1>
            <p style='color: #F7C566; text-align: center; margin: 0.5rem 0 0 0;'>
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
                        padding: 1.5rem; border-radius: 15px; text-align: center;
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                <h3 style='color: white; margin: 0; font-size: 2.5rem;'>{total_users}</h3>
                <p style='color: white; margin: 0.5rem 0 0 0; font-size: 1rem; opacity: 0.9;'>👥 Total Users</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                        padding: 1.5rem; border-radius: 15px; text-align: center;
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                <h3 style='color: white; margin: 0; font-size: 2.5rem;'>{total_books}</h3>
                <p style='color: white; margin: 0.5rem 0 0 0; font-size: 1rem; opacity: 0.9;'>📚 Total Books</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                        padding: 1.5rem; border-radius: 15px; text-align: center;
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                <h3 style='color: white; margin: 0; font-size: 2.5rem;'>{active_borrows}</h3>
                <p style='color: white; margin: 0.5rem 0 0 0; font-size: 1rem; opacity: 0.9;'>📖 Active Borrows</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); 
                        padding: 1.5rem; border-radius: 15px; text-align: center;
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                <h3 style='color: white; margin: 0; font-size: 2.5rem;'>₹{total_fines}</h3>
                <p style='color: white; margin: 0.5rem 0 0 0; font-size: 1rem; opacity: 0.9;'>💰 Total Fines</p>
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
    
    all_users = []
    for role in ['students', 'teachers']:
        for user in st.session_state.app.users.get(role, []):
            all_users.append({**user, 'role': role})
    
    if all_users:
        # Display users in cards
        for user in all_users:
            with st.expander(f"👤 {user['name']} ({user['id']})"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Username:** {user['username']}")
                    st.write(f"**Role:** {user['role'].title()}")
                with col2:
                    st.write(f"**Contact:** {user.get('contact', 'Not provided')}")
                    st.write(f"**Email:** {user.get('email', 'Not provided')}")
    else:
        st.info("No users found")

def view_all_transactions():
    """View all transactions"""
    st.markdown("### 📈 All Transactions")
    
    if st.session_state.app.transactions:
        # Display transactions
        for trans in st.session_state.app.transactions:
            status_color = "#28a745" if trans['status'] == 'returned' else "#ffc107"
            st.markdown(f"""
                <div style='background: white; padding: 1rem; border-radius: 10px; 
                            margin: 0.5rem 0; border-left: 4px solid {status_color};'>
                    <strong>{trans['user_name']}</strong> - {trans['book_title']}<br>
                    <small>Borrowed: {trans['borrow_date']} | Due: {trans['due_date']} | Status: {trans['status'].title()}</small>
                    {f"<br><span style='color: #dc3545;'>Fine: ₹{trans['fine']}</span>" if trans['fine'] > 0 else ""}
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
        else:
            login_page()
        return
    
    # Logged in - Show sidebar
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.user['name']}")
        st.caption(f"Role: {st.session_state.role.title()}")
        st.caption(f"ID: {st.session_state.user['id']}")
        st.divider()
        
        if st.session_state.role == 'admin':
            menu = st.radio("Navigation", ["📊 Dashboard", "📚 Books", "🚪 Logout"])
        else:
            menu = st.radio("Navigation", ["📚 View Books", "📊 My Transactions", "🚪 Logout"])
        
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
