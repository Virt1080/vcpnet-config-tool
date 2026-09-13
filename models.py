"""
SQLModel models for VCPnet Config Tool - Restructured for Network Management
"""

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime


class ManagementService(SQLModel, table=True):
    """Management layer services like DNS, Traefik, Headscale, etc."""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)  # e.g., "Pi-hole", "Traefik", "Headscale"
    service_type: str = Field(index=True)  # dns, proxy, vpn_controller, vpn_gateway, etc.
    hostname: str = ""
    ip_address: str = ""
    port: Optional[int] = None
    username: str = ""
    password: str = ""  # If empty, will attempt SSH key authentication
    api_endpoint: str = ""  # For API-based configuration
    ssh_command: str = ""  # Command to run via SSH for testing/config
    config_file_path: str = ""  # Path to config file on the device
    config_method: str = ""  # ssh, api, direct_file
    notes: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class KnownSystem(SQLModel, table=True):
    """Template for known hardware/software/firmware"""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)  # e.g., "Raspberry Pi 4", "Dell R750", "Ubuntu 22.04 LTS"
    category: str = Field(index=True)  # hardware, software, firmware
    vendor: str = ""  # e.g., "Raspberry Pi Foundation", "Dell", "Canonical"
    model_number: str = ""  # Specific model identifier
    default_username: str = ""  # Default username for this system
    default_password: str = ""  # Default password (if applicable)
    ssh_port: int = Field(default=22)  # Default SSH port
    config_notes: str = ""  # Special configuration notes
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class MasterTemplate(SQLModel, table=True):
    """Master template for IP/hostname/port/LXC CTID allocation rules"""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)  # Template name
    description: str = ""

    # IP address pattern (with {client_number} placeholder)
    ip_pattern: str = Field(default="192.168.{client_number}.{device_id}")  # e.g., "192.168.{client_number}.10"

    # Hostname pattern (with placeholders)
    hostname_pattern: str = Field(default="{device_name}-{home_abbrev}")  # e.g., "Router-ABBV"

    # LXC CTID pattern (if applicable)
    lxc_ctid_pattern: Optional[str] = None  # e.g., "10{client_number}" for LXCs

    # Port mappings (service_type -> port pattern or fixed port)
    # Stored as JSON string for flexibility: {"web_service": 80, "proxy": 8080, "dns": 53}
    port_mappings: str = Field(default='{}')

    # Default values for fields
    default_username: str = ""
    default_password: str = ""

    # MAC address generation settings
    mac_vendor_prefix: str = Field(default="00:16:3e")  # Locally administered prefix
    mac_method: str = Field(default="ip_based")  # ip_based, hostname_hash, sequential

    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Network(SQLModel, table=True):
    """Represents a managed network (home network or client network)"""
    id: Optional[int] = Field(default=None, primary_key=True)
    client_name: str = Field(index=True)  # Client identifier
    client_number: int = Field(index=True, unique=True)  # Used for subnet calculation: 192.168.X.X
    client_address: str = ""  # Physical address or location
    home_name: str = ""  # e.g., "VirtiCORP Home"
    home_name_abbrev: str = Field(index=True)  # e.g., "VCP"
    tailnet_domain: str = Field(index=True, unique=True)  # e.g., "VCPnet"

    # Feature flags (what services are enabled in this network)
    feature_dns: bool = Field(default=True)
    feature_proxy: bool = Field(default=True)
    feature_vpn: bool = Field(default=True)
    feature_monitoring: bool = Field(default=False)
    feature_backup: bool = Field(default=False)

    notes: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to devices in this network
    devices: List["Device"] = Relationship(back_populates="network")


class Device(SQLModel, table=True):
    """Represents an actual device in a network"""
    id: Optional[int] = Field(default=None, primary_key=True)
    network_id: Optional[int] = Field(default=None, foreign_key="network.id")
    name: str = Field(index=True)  # e.g., "Router", "Pi-hole", "Proxmox"

    # Device classification
    service_type: str = Field(index=True)  # router, dns, proxy, vpn, etc.
    known_system_id: Optional[int] = Field(default=None, foreign_key="knownsystem.id")  # Reference to KnownSystem template

    # Network addressing (calculated from master template and network client_number)
    hostname: str = ""
    ip_address: str = ""
    mac_address: str = Field(index=True, unique=True)  # MAC address - must be unique across all networks
    lxc_ctid: Optional[int] = None  # For LXC containers

    # Connection details
    port: Optional[int] = None
    username: str = ""
    password: str = ""  # If empty, will attempt SSH key authentication

    # Configuration status
    config_status: str = Field(default="not_loaded")  # not_loaded, config_mismatch, config_ok, applying
    config_applied_at: Optional[datetime] = None
    config_checked_at: Optional[datetime] = None

    # Installation tracking
    installed_at: Optional[datetime] = None
    installation_method: str = ""  # community_script, manual, etc.
    installation_script_url: str = ""  # Link to or content of installation script used

    notes: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    network: Optional[Network] = Relationship(back_populates="devices")
    known_system: Optional[KnownSystem] = Relationship()


# Legacy model for backward compatibility during migration
class ServiceDevice(SQLModel, table=True):
    """Legacy model - kept for migration purposes"""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    service_type: str = Field(index=True)  # e.g., proxmox, router, switch, web_service, lxc, pi_hole, openwrt, vpn, proxy, sso, wifi, custom
    hostname: str = ""
    ip_address: str = ""
    port: Optional[int] = None
    username: str = ""
    password: str = ""  # If empty, will attempt SSH key authentication via ssh-agent or default keys
    notes: str = ""
    ssh_command: str = ""  # Command to run via SSH when testing (e.g., "uname -a")