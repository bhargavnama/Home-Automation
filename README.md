# Home-Automation

Prerequisites
- Python 3.10+
- A Supabase project with tables: users, devices, device_types, device_settings, device_logs, home_controller
- .env containing SUPABASE_URL and SUPABASE_KEY

Setup
1. Create .env with your Supabase creds
2. Install deps: pip install supabase python-dotenv
3. Run CLI: python -m src.client.cli --help

CLI examples
- Create device: python -m src.client.cli create-device Light "Living Light" LivingRoom 1 --on
- List devices: python -m src.client.cli list-devices 1
- Turn on: python -m src.client.cli on 10
- Turn off: python -m src.client.cli off 10

Project structure
- src/config.py: Supabase client
- src/dao/: DAOs for users, devices, home_controller
- src/devices/: OOP device classes (SmartDevice, Light, Thermostat, Camera)
- src/services/: Orchestration services for devices and controller
- src/client/cli.py: Minimal CLI 

## Streamlit Web App

1. Create a `.env` file in project root with:

```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_or_service_key
```

2. Install dependencies:

```
pip install -r requirements.txt
```

3. Run the app from the project root:

```
streamlit run streamlit_app.py
```

4. Use the left sidebar to open `Devices` after signing in. Your Supabase Auth email should exist in the `users` table for device mapping. 