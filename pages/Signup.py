import streamlit as st
from src.web.auth import ensure_supabase, sign_up_with_email_password, debug_attempt_signup

st.set_page_config(page_title="Sign Up - Home Automation", page_icon="👤", layout="wide")

ensure_supabase()

st.title("Create New Account")
st.markdown("Join our Home Automation platform to manage your smart devices.")

# Check if user is already authenticated
if "authenticated" in st.session_state and st.session_state.authenticated:
    st.info("You are already signed in. Go to the main page to access your devices.")
    if st.button("Go to Main Page"):
        st.switch_page("streamlit_app.py")
    st.stop()

# Signup form
with st.form("signup_form", clear_on_submit=False):
    st.subheader("Account Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Full Name *", placeholder="Enter your full name")
        email = st.text_input("Email Address *", placeholder="Enter your email")
        password = st.text_input("Password *", type="password", placeholder="Create a strong password")
    
    with col2:
        phone = st.text_input("Phone Number", placeholder="Enter your phone number (optional)")
        city = st.text_input("City", placeholder="Enter your city (optional)")
        confirm_password = st.text_input("Confirm Password *", type="password", placeholder="Confirm your password")
    
    # Password validation
    password_match = password == confirm_password if password and confirm_password else True
    password_length = len(password) >= 6 if password else True
    
    submitted = st.form_submit_button("Create Account", type="primary")
    
    if submitted:
        # Validation
        if not name or not email or not password:
            st.error("Please fill in all required fields (marked with *)")
        elif not password_match:
            st.error("Passwords do not match")
        elif not password_length:
            st.error("Password must be at least 6 characters long")
        else:
            # Attempt to create account
            with st.spinner("Creating your account..."):
                success, error = sign_up_with_email_password(
                    email=email,
                    password=password,
                    name=name,
                    phone=phone,
                    city=city
                )
                
                if success:
                    st.success("Account created successfully! Please check your email to verify your account.")
                    st.balloons()
                    
                    # Auto sign in after successful signup
                    st.session_state.authenticated = True
                    st.session_state.email = email
                    
                    # Give a moment for the success message to show
                    st.markdown("Redirecting to main page...")
                    st.rerun()
                else:
                    st.error(f"Failed to create account: {error}")

# Troubleshooting expander (dev only)
with st.expander("Troubleshoot Signup (dev)"):
    dbg_email = st.text_input("Debug Email", key="dbg_email")
    dbg_password = st.text_input("Debug Password", type="password", key="dbg_password")
    if st.button("Attempt raw signup"):
        ok, msg = debug_attempt_signup(dbg_email, dbg_password)
        if ok:
            st.success(msg)
        else:
            st.error(msg)

# Additional information
st.divider()
st.markdown("### Already have an account?")
col1, col2 = st.columns(2)
with col1:
    st.page_link("streamlit_app.py", label="Sign In", icon="🔑")
with col2:
    st.page_link("pages/Devices.py", label="View Devices", icon="🔧")

st.markdown("### About Your Account")
st.info("""
- Your email will be used for authentication and device notifications
- Phone number and city are optional but help us provide better service
- You'll receive a verification email after signup
- All your device data is securely stored and encrypted
""")
