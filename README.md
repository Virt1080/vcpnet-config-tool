# VCPnet Config Tool

A web UI for managing network services and devices, with capabilities to test connectivity via SSH and HTTP.

## Features

- CRUD operations for service/device entries
- Predefined service types (Proxmox, Router, Switch, Web Service, LXC, Pi-hole, OpenWrt, VPN, Proxy, SSO, Wifi, Custom)
- Test SSH connectivity
- Test HTTP/HTTPS connectivity
- SQLite database for storage
- Responsive UI with Bootstrap 5

## Setup

1. Clone the repository (or copy the files to a directory).
2. Ensure you have Python 3.12+ installed.
3. It is recommended to use a virtual environment:

   ```bash
   uv venv
   source .venv/bin/activate
   ```

4. Install dependencies:

   ```bash
   uv pip install -r requirements.txt
   ```

5. Run the application:

   ```bash
   uv uvicorn main:app --reload
   ```

   Or, if you prefer:

   ```bash
   .venv/bin/uvicorn main:app --reload
   ```

6. Open your browser at http://localhost:8000.

## Usage

- Navigate to the dashboard to see all services.
- Click "Add Service" to create a new service entry.
- Fill in the form with the service details.
- Use the "Test SSH" and "Test HTTP" buttons to verify connectivity.
- Edit or delete services as needed.

## Notes

- Passwords are stored in plain text in the database. This is intended for personal use in a trusted environment. For production, consider encrypting sensitive fields.
- The tool does not implement authentication; it is assumed to be used in a secure environment.

## Project Structure

- `main.py`: FastAPI application entrypoint.
- `models.py`: SQLModel definitions.
- `database.py`: Database setup.
- `crud.py`: CRUD operations.
- `ssh_utils.py`: SSH connection testing.
- `http_utils.py`: HTTP connection testing.
- `templates/`: Jinja2 HTML templates.
- `static/`: CSS and JavaScript files.
- `requirements.txt`: Python dependencies.
- `.gitignore`: Git ignore file.

## License

This project is open source and available under the MIT License.