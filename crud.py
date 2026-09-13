"""
CRUD operations for VCPnet Config Tool models
"""

from sqlmodel import Session, select
from models import (
    ServiceDevice,  # Legacy model
    ManagementService,
    KnownSystem,
    MasterTemplate,
    Network,
    Device
)


# ===== LEGACY SERVICE DEVICE (for backward compatibility) =====
def get_services(session: Session):
    return session.exec(select(ServiceDevice)).all()


def create_service(session: Session, service: ServiceDevice):
    session.add(service)
    session.commit()
    session.refresh(service)
    return service


def get_service(session: Session, service_id: int):
    return session.get(ServiceDevice, service_id)


def update_service(session: Session, service: ServiceDevice):
    session.add(service)
    session.commit()
    session.refresh(service)
    return service


def delete_service(session: Session, service: ServiceDevice):
    session.delete(service)
    session.commit()


# ===== MANAGEMENT SERVICE =====
def get_management_services(session: Session):
    return session.exec(select(ManagementService)).all()


def create_management_service(session: Session, service: ManagementService):
    session.add(service)
    session.commit()
    session.refresh(service)
    return service


def get_management_service(session: Session, service_id: int):
    return session.get(ManagementService, service_id)


def update_management_service(session: Session, service: ManagementService):
    session.add(service)
    session.commit()
    session.refresh(service)
    return service


def delete_management_service(session: Session, service: ManagementService):
    session.delete(service)
    session.commit()


# ===== KNOWN SYSTEM =====
def get_known_systems(session: Session):
    return session.exec(select(KnownSystem)).all()


def create_known_system(session: Session, system: KnownSystem):
    session.add(system)
    session.commit()
    session.refresh(system)
    return system


def get_known_system(session: Session, system_id: int):
    return session.get(KnownSystem, system_id)


def update_known_system(session: Session, system: KnownSystem):
    session.add(system)
    session.commit()
    session.refresh(system)
    return system


def delete_known_system(session: Session, system: KnownSystem):
    session.delete(system)
    session.commit()


# ===== MASTER TEMPLATE =====
def get_master_templates(session: Session):
    return session.exec(select(MasterTemplate)).all()


def create_master_template(session: Session, template: MasterTemplate):
    session.add(template)
    session.commit()
    session.refresh(template)
    return template


def get_master_template(session: Session, template_id: int):
    return session.get(MasterTemplate, template_id)


def update_master_template(session: Session, template: MasterTemplate):
    session.add(template)
    session.commit()
    session.refresh(template)
    return template


def delete_master_template(session: Session, template: MasterTemplate):
    session.delete(template)
    session.commit()


def get_active_master_template(session: Session):
    return session.exec(select(MasterTemplate).where(MasterTemplate.is_active == True)).first()


# ===== NETWORK =====
def get_networks(session: Session):
    return session.exec(select(Network)).all()


def create_network(session: Session, network: Network):
    session.add(network)
    session.commit()
    session.refresh(network)
    return network


def get_network(session: Session, network_id: int):
    return session.get(Network, network_id)


def get_network_by_client_number(session: Session, client_number: int):
    return session.exec(select(Network).where(Network.client_number == client_number)).first()


def update_network(session: Session, network: Network):
    session.add(network)
    session.commit()
    session.refresh(network)
    return network


def delete_network(session: Session, network: Network):
    session.delete(network)
    session.commit()


# ===== DEVICE =====
def get_devices(session: Session):
    return session.exec(select(Device)).all()


def get_devices_by_network(session: Session, network_id: int):
    return session.exec(select(Device).where(Device.network_id == network_id)).all()


def create_device(session: Session, device: Device):
    session.add(device)
    session.commit()
    session.refresh(device)
    return device


def get_device(session: Session, device_id: int):
    return session.get(Device, device_id)


def update_device(session: Session, device: Device):
    session.add(device)
    session.commit()
    session.refresh(device)
    return device


def delete_device(session: Session, device: Device):
    session.delete(device)
    session.commit()