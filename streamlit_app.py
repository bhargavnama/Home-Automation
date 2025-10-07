import streamlit as st
from src.web.auth import ensure_supabase, sign_in_with_email_password, sign_out, get_current_user_email, get_or_fetch_user_id

st.set_page_config(page_title="Home Automation", page_icon="💡", layout="wide")

ensure_supabase()

if "authenticated" not in st.session_state:
	st.session_state.authenticated = False

st.title("Home Automation Console")

if not st.session_state.authenticated:
	col1, col2 = st.columns([1, 1])
	
	with col1:
		st.subheader("Sign In")
		with st.form("login_form", clear_on_submit=False):
			email = st.text_input("Email", key="login_email")
			password = st.text_input("Password", type="password", key="login_password")
			submitted = st.form_submit_button("Sign in", type="primary")
			if submitted:
				ok, err = sign_in_with_email_password(email, password)
				if ok:
					st.success("Signed in successfully")
					st.session_state.authenticated = True
					st.session_state.email = get_current_user_email()
					st.rerun()
				else:
					st.error(err or "Login failed")
	
	with col2:
		st.subheader("New User?")
		st.markdown("Create a new account to start managing your smart home devices.")
		st.page_link("pages/Signup.py", label="Create Account", icon="👤")
		
		st.markdown("---")
		st.markdown("**Features you'll get:**")
		st.markdown("• Device management")
		st.markdown("• Real-time monitoring")
		st.markdown("• Smart automation")
		st.markdown("• Secure cloud storage")
else:
	col1, col2 = st.columns([1,1])
	with col1:
		st.markdown("**Status**: ✅ Authenticated")
		st.markdown(f"**Email**: {get_current_user_email()}")
		user_id = get_or_fetch_user_id()
		if user_id is not None:
			st.markdown(f"**User ID**: {user_id}")
		else:
			st.warning("No user profile found in DB for this email.")
	with col2:
		if st.button("Sign out"):
			sign_out()
			st.session_state.authenticated = False
			st.experimental_set_query_params()
			st.rerun()

	st.divider()
	st.markdown("Go to the Devices page from the left sidebar: `Devices`.\n\nAlternatively, use the link below.")
	st.page_link("pages/Devices.py", label="→ Manage Devices", icon="🔧")
