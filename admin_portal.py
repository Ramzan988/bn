import streamlit as st

from security_utils import ensure_password_fields, hash_password

__all__ = [
    "admin_login_page",
    "admin_dashboard",
]


def admin_login_page():
    """Admin-only login page"""
    # Header with purple/red gradient like public page - compact
    st.markdown(
        """
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
    """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown(
            """
            <div style='background: #1e1e1e; padding: 0.8rem; border-radius: 8px; 
                        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
                        border: 1px solid #333333;'>
                <h2 style='color: #ffffff; text-align: center; margin: 0; font-size: 1.1rem;'>
                    🛡️ Administrator Login
                </h2>
            </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown("<div style='margin: 0.5rem 0;'></div>", unsafe_allow_html=True)

        username = st.text_input(
            "**Admin Username**", placeholder="Enter admin username", key="admin_username"
        )
        password = st.text_input(
            "**Admin Password**",
            type="password",
            placeholder="Enter admin password",
            key="admin_password",
        )

        st.markdown("<br>", unsafe_allow_html=True)

        col_a, col_b = st.columns(2)

        with col_a:
            if st.button("🔐 Admin Login", use_container_width=True, type="primary"):
                if username and password:
                    user = st.session_state.app.verify_login(username, password, "admin")
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.user = user
                        st.session_state.role = "admin"
                        st.success(f"✅ Welcome, Administrator {user['name']}!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid admin credentials! Access denied.")
                else:
                    st.warning("⚠️ Please enter both username and password")

        with col_b:
            if st.button("← Back to Login", use_container_width=True):
                st.session_state.page = "login"
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        # Security warning
        st.warning(
            "⚠️ **Security Notice:** This area is restricted to authorized administrators only. Unauthorized access attempts are logged."
        )


def admin_dashboard():
    """Admin dashboard"""
    # Header with gradient - compact
    st.markdown(
        """
        <div style='background: linear-gradient(135deg, #6C0345 0%, #DC143C 100%); 
                    padding: 0.6rem; border-radius: 8px; margin-bottom: 0.8rem;'>
            <h2 style='color: white; text-align: center; margin: 0; font-size: 1.2rem;'>📊 Admin Dashboard</h2>
            <p style='color: #F7C566; text-align: center; margin: 0.2rem 0 0 0; font-size: 0.75rem;'>
                Complete library overview and management
            </p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    # Statistics with enhanced cards
    col1, col2, col3, col4 = st.columns(4)

    total_users = len(st.session_state.app.users.get("students", [])) + len(
        st.session_state.app.users.get("teachers", [])
    )
    total_books = len(st.session_state.app.books["student_books"]) + len(
        st.session_state.app.books["teacher_books"]
    )
    active_borrows = len([t for t in st.session_state.app.transactions if t["status"] == "borrowed"])
    total_fines = sum(t["fine"] for t in st.session_state.app.transactions)

    with col1:
        st.markdown(
            f"""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 0.8rem; border-radius: 8px; text-align: center;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 0.5rem;'>
                <h3 style='color: white; margin: 0; font-size: 1.5rem;'>{total_users}</h3>
                <p style='color: white; margin: 0.3rem 0 0 0; font-size: 0.8rem; opacity: 0.9;'>👥 Users</p>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                        padding: 0.8rem; border-radius: 8px; text-align: center;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 0.5rem;'>
                <h3 style='color: white; margin: 0; font-size: 1.5rem;'>{total_books}</h3>
                <p style='color: white; margin: 0.3rem 0 0 0; font-size: 0.8rem; opacity: 0.9;'>📚 Books</p>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
            <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                        padding: 0.8rem; border-radius: 8px; text-align: center;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 0.5rem;'>
                <h3 style='color: white; margin: 0; font-size: 1.5rem;'>{active_borrows}</h3>
                <p style='color: white; margin: 0.3rem 0 0 0; font-size: 0.8rem; opacity: 0.9;'>📖 Borrows</p>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            f"""
            <div style='background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); 
                        padding: 0.8rem; border-radius: 8px; text-align: center;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 0.5rem;'>
                <h3 style='color: white; margin: 0; font-size: 1.5rem;'>₹{total_fines}</h3>
                <p style='color: white; margin: 0.3rem 0 0 0; font-size: 0.8rem; opacity: 0.9;'>💰 Fines</p>
            </div>
        """,
            unsafe_allow_html=True,
        )

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
                    "id": book_id.upper(),
                    "title": title,
                    "author": author,
                    "copies": copies,
                    "available": copies,
                }

                book_list = (
                    st.session_state.app.books["student_books"]
                    if category == "Student"
                    else st.session_state.app.books["teacher_books"]
                )
                book_list.append(new_book)
                st.session_state.app.save_data()
                st.success("✅ Book added successfully!")
                st.rerun()
            else:
                st.error("❌ All fields required!")

    # List all books
    st.markdown("### 📖 All Books")
    all_books = st.session_state.app.books["student_books"] + st.session_state.app.books["teacher_books"]

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
                    active = [
                        t
                        for t in st.session_state.app.transactions
                        if t["book_id"] == book["id"] and t["status"] == "borrowed"
                    ]
                    if active:
                        st.error("Cannot delete - book is borrowed!")
                    else:
                        # Remove book
                        st.session_state.app.books["student_books"] = [
                            b for b in st.session_state.app.books["student_books"] if b["id"] != book["id"]
                        ]
                        st.session_state.app.books["teacher_books"] = [
                            b for b in st.session_state.app.books["teacher_books"] if b["id"] != book["id"]
                        ]
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
                role_key = "students" if new_role == "Student" else "teachers"
                existing = any(
                    u["username"] == new_username or u["id"] == new_id
                    for role in ["students", "teachers"]
                    for u in st.session_state.app.users.get(role, [])
                )

                if existing:
                    st.error("❌ Username or ID already exists!")
                else:
                    password_hash, password_salt = hash_password(new_password)
                    new_user = {
                        "id": new_id.upper(),
                        "name": new_name,
                        "username": new_username,
                        "password_hash": password_hash,
                        "password_salt": password_salt,
                        "contact": new_contact,
                        "email": new_email,
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
    for role in ["students", "teachers"]:
        for user in st.session_state.app.users.get(role, []):
            all_users.append({**user, "role": role})

    if all_users:
        st.markdown(
            f"**Total Users:** {len(all_users)} (Students: {len(st.session_state.app.users.get('students', []))}, Teachers: {len(st.session_state.app.users.get('teachers', []))})"
        )
        st.divider()

        # Display users in dark cards
        for idx, user in enumerate(all_users):
            st.markdown(
                f"""
                <div style='background: #1e1e1e; padding: 1rem; border-radius: 10px; 
                            margin: 0.5rem 0; border-left: 4px solid #6C0345;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.3);'>
                    <p style='color: #ffffff; margin: 0; font-weight: 600; font-size: 1.1rem;'>👤 {user['name']}</p>
                    <p style='color: #b0b0b0; margin: 0.3rem 0 0 0; font-size: 0.9rem;'>
                        🆔 {user['id']} | 👨‍💼 {user['role'].title()} | 📧 {user.get('email', 'N/A')} | 📱 {user.get('contact', 'N/A')}
                    </p>
                </div>
            """,
                unsafe_allow_html=True,
            )

            col1, col2, col3 = st.columns([1, 1, 3])
            with col1:
                if st.button("✏️ Edit", key=f"edit_user_{idx}", use_container_width=True):
                    st.session_state[f"editing_user_{idx}"] = True
                    st.rerun()
            with col2:
                if st.button("🗑️ Delete", key=f"delete_user_{idx}", use_container_width=True):
                    # Check for active borrows
                    active_borrows = [
                        t
                        for t in st.session_state.app.transactions
                        if t["user_id"] == user["id"] and t["status"] == "borrowed"
                    ]
                    if active_borrows:
                        st.error(
                            f"❌ Cannot delete! {user['name']} has {len(active_borrows)} active borrow(s)"
                        )
                    else:
                        st.session_state.app.users[user["role"]] = [
                            u for u in st.session_state.app.users[user["role"]] if u["id"] != user["id"]
                        ]
                        st.session_state.app.save_data()
                        st.success(f"✅ User {user['name']} deleted!")
                        st.rerun()

            # Edit form
            if st.session_state.get(f"editing_user_{idx}", False):
                with st.expander(f"✏️ Edit {user['name']}", expanded=True):
                    col_a, col_b = st.columns(2)
                    with col_a:
                        edit_name = st.text_input(
                            "Name", value=user["name"], key=f"edit_name_{idx}"
                        )
                        edit_username = st.text_input(
                            "Username", value=user["username"], key=f"edit_username_{idx}"
                        )
                        edit_password = st.text_input(
                            "Password",
                            type="password",
                            key=f"edit_password_{idx}",
                        )
                    with col_b:
                        edit_contact = st.text_input(
                            "Contact", value=user.get("contact", ""), key=f"edit_contact_{idx}"
                        )
                        edit_email = st.text_input(
                            "Email", value=user.get("email", ""), key=f"edit_email_{idx}"
                        )

                    col_save, col_cancel = st.columns(2)
                    with col_save:
                        if st.button("💾 Save Changes", key=f"save_{idx}", use_container_width=True):
                            # Update user
                            for u in st.session_state.app.users[user["role"]]:
                                if u["id"] == user["id"]:
                                    u["name"] = edit_name
                                    u["username"] = edit_username
                                    if edit_password:
                                        password_hash, password_salt = hash_password(edit_password)
                                        u["password_hash"] = password_hash
                                        u["password_salt"] = password_salt
                                    ensure_password_fields(u)
                                    u["contact"] = edit_contact
                                    u["email"] = edit_email
                                    break
                            st.session_state.app.save_data()
                            st.session_state[f"editing_user_{idx}"] = False
                            st.success("✅ User updated successfully!")
                            st.rerun()
                    with col_cancel:
                        if st.button("❌ Cancel", key=f"cancel_{idx}", use_container_width=True):
                            st.session_state[f"editing_user_{idx}"] = False
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
            status_color = "#28a745" if trans["status"] == "returned" else "#ffc107"
            st.markdown(
                f"""
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
            """,
                unsafe_allow_html=True,
            )
    else:
        st.info("No transactions yet")
