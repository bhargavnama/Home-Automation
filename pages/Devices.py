import streamlit as st
from typing import List, Dict
from src.web.auth import ensure_supabase, get_or_fetch_user_id, get_current_user_email
from src.services.device_service import DeviceService

st.set_page_config(page_title="Devices", page_icon="🔧", layout="wide")

ensure_supabase()

if "authenticated" not in st.session_state or not st.session_state.authenticated:
	st.warning("Please sign in from the Home page.")
	st.page_link("streamlit_app.py", label="← Back to Home", icon="🏠")
	st.stop()

st.title("My Devices")

user_id = get_or_fetch_user_id()
if user_id is None:
	st.error("No app user profile found for email: " + str(get_current_user_email()))
	st.stop()

service = DeviceService()

@st.cache_data(ttl=10)
def load_devices(uid: int) -> List[Dict]:
	return service.by_user(uid)

def refresh():
	load_devices.clear()

with st.expander("Add a new device", expanded=False):
	with st.form("create_device_form", clear_on_submit=True):
		col_a, col_b, col_c, col_d = st.columns(4)
		with col_a:
			type_name = st.selectbox("Type", options=["Light", "Thermostat", "Camera", "Other"], index=0)
		with col_b:
			name = st.text_input("Name", placeholder="e.g., Living Room Light")
		with col_c:
			location = st.text_input("Location", placeholder="e.g., Living Room")
		with col_d:
			status = st.checkbox("Turn on", value=True)
		submitted_new = st.form_submit_button("Create Device", type="primary")
		if submitted_new:
			created = service.create(type_name, name, status, location, user_id)
			if created:
				st.success(f"Created device: {created.get('name')} (ID: {created.get('device_id')})")
				refresh()
				st.rerun()
			else:
				st.error("Failed to create device. Please check inputs and try again.")

with st.spinner("Loading devices..."):
	devices = load_devices(user_id) or []

if not devices:
	st.info("No devices found. Add devices for your account to manage them here.")
else:
	for device in devices:
		with st.container(border=True):
			header = f"{device.get('name', 'Device')} ({device.get('type_name', 'Unknown')})"
			cols = st.columns([3,1,1,2])
			with cols[0]:
				st.subheader(header)
				st.caption(f"Location: {device.get('location', 'N/A')}")
				st.caption(f"Status: {'ON' if device.get('status') else 'OFF'}")
			with cols[1]:
				if st.button("Turn ON", key=f"on_{device['device_id']}"):
					service.control_on(device["device_id"])  # DAO should persist state
					refresh()
					st.rerun()
			with cols[2]:
				if st.button("Turn OFF", key=f"off_{device['device_id']}"):
					service.control_off(device["device_id"])  # DAO should persist state
					refresh()
					st.rerun()
			with cols[3]:
				st.json({k: v for k, v in device.items() if k not in {"status"}})
