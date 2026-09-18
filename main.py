"""
Main application entrypoint for VCPnet Config Tool
"""
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import Session

from database import engine
from models import *
from crud import *
from mac_utils import generate_mac_address

app = FastAPI(title="VCPnet Config Tool", version="1.0.0")


@app.on_event("startup")
def on_startup():
    """Create database tables on startup"""
    from database import create_db_and_tables
    create_db_and_tables()


@app.get("/")
def root():
    """Root endpoint"""
    return {"message": "VCPnet Config Tool API", "version": "1.0.0"}


@app.get("/api/device/{device_id}/calculate-mac")
def api_calculate_mac(device_id: int):
    """Calculate MAC address for a device based on master template rules"""
    with Session(engine) as session:
        device = get_device(session, device_id)
        if not device:
            raise HTTPException(status_code=404, detail="Device not found")

        network = get_network(session, device.network_id) if device.network_id else None
        master_template = get_active_master_template(session)

        if not master_template:
            raise HTTPException(status_code=400, detail="No active master template")

        # Calculate MAC based on method using utility function
        mac_address = generate_mac_address(
            ip_address=device.ip_address if device.ip_address else None,
            hostname=device.hostname if device.hostname else None,
            master_template_method=master_template.mac_method,
            vendor_prefix=master_template.mac_vendor_prefix
        )

        return JSONResponse(content={"mac_address": mac_address})


# Additional API routes would go here for CRUD operations on various entities
# These would typically be imported from routers or defined directly