from typing import Optional, Tuple
import re
import bcrypt
import streamlit as st
from src.config import get_supabase
from src.dao.user_dao import User


def ensure_supabase():
	if "supabase" not in st.session_state:
		st.session_state.supabase = get_supabase()


def sign_up_with_email_password(email: str, password: str, name: str, phone: str = "", city: str = "") -> Tuple[bool, Optional[str]]:
	try:
		ensure_supabase()
		if not email or not password or not name:
			return False, "Email, password, and name are required"
		# Normalize inputs
		email = email.strip().lower()
		name = name.strip()
		phone = phone.strip() if phone else ""
		city = city.strip() if city else ""
		# Strict email format check (no consecutive dots, proper domain)
		EMAIL_REGEX = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
		if not re.match(EMAIL_REGEX, email):
			return False, "Invalid email address"

		
		# Check if user already exists
		user_dao = User()
		existing_user = user_dao.get_user_by_email(email)
		if existing_user:
			return False, "An account with this email already exists"
		
		# Sign up with Supabase Auth
		response = st.session_state.supabase.auth.sign_up({
			"email": email,
			"password": password,
		})
		
		if response.user:
			# Create user profile in the users table with hashed password for app-side reference
			password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
			created_user = user_dao.create_user(name=name, email=email, phone=phone, city=city, password_hash=password_hash)
			if created_user:
				# Store user_id in session state for immediate access
				st.session_state.user_id = created_user.get("user_id")
				return True, None
			else:
				return False, "Failed to create user profile"
		else:
			return False, "Failed to create account"
			
	except Exception as exc:
		error_msg = str(exc)
		# Provide more specific error messages
		if "duplicate key" in error_msg.lower() or "already exists" in error_msg.lower():
			return False, "An account with this email already exists"
		elif "database" in error_msg.lower():
			return False, f"Database error: {error_msg}"
		else:
			return False, f"Signup failed: {error_msg}"


def sign_in_with_email_password(email: str, password: str) -> Tuple[bool, Optional[str]]:
	try:
		ensure_supabase()
		if not email or not password:
			return False, "Email and password are required"
		# Normalize inputs
		email = email.strip().lower()
		st.session_state.supabase.auth.sign_in_with_password({
			"email": email,
			"password": password,
		})
		# Cache user email and user_id for app usage
		st.session_state.email = get_current_user_email() or email
		try:
			dao = User()
			row = dao.get_user_by_email(email)
			if row and "user_id" in row:
				st.session_state.user_id = row["user_id"]
		except Exception:
			pass
		return True, None
	except Exception as exc:
		msg = str(exc)
		if "invalid" in msg.lower() and "email" in msg.lower():
			return False, "Invalid email address"
		return False, msg


def sign_out():
	ensure_supabase()
	try:
		st.session_state.supabase.auth.sign_out()
	except Exception:
		pass
	for key in ["authenticated", "email", "user_id"]:
		if key in st.session_state:
			del st.session_state[key]


def get_current_user_email() -> Optional[str]:
	ensure_supabase()
	try:
		session = st.session_state.supabase.auth.get_session()
		if session and getattr(session, "user", None) and getattr(session.user, "email", None):
			return session.user.email
		# Fallback to cached email if session has no email
		return st.session_state.get("email")
	except Exception:
		return st.session_state.get("email")


def get_or_fetch_user_id() -> Optional[int]:
	if "user_id" in st.session_state and st.session_state.user_id is not None:
		return st.session_state.user_id

	email = get_current_user_email()
	if not email:
		return None

	try:
		dao = User()
		row = dao.get_user_by_email(email)
		if row and "user_id" in row:
			st.session_state.user_id = row["user_id"]
			return st.session_state.user_id
	except Exception:
		return None
	return None


def debug_attempt_signup(email: str, password: str) -> Tuple[bool, str]:
	"""
	Attempts a raw Supabase signup and returns (ok, message) with detailed error info.
	This is intended for troubleshooting only and should not be exposed in production.
	"""
	try:
		ensure_supabase()
		norm_email = (email or "").strip().lower()
		st.write({"normalized_email": repr(norm_email)})
		resp = st.session_state.supabase.auth.sign_up({
			"email": norm_email,
			"password": password,
		})
		if getattr(resp, "user", None):
			return True, "Signup succeeded"
		return False, f"Signup returned no user: {resp}"
	except Exception as exc:
		return False, f"Exception: {repr(exc)}"
