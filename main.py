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