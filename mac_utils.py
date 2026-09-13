"""
MAC address utilities for VCPnet Config Tool
"""

import random
import hashlib


def generate_mac_address(ip_address: str = None, hostname: str = None,
                        master_template_method: str = "ip_based",
                        vendor_prefix: str = "00:16:3e") -> str:
    """
    Generate MAC address based on available parameters and method.

    Args:
        ip_address: IP address to base MAC on (for ip_based method)
        hostname: Hostname to base MAC on (for hostname_hash method)
        master_template_method: Method to use ("ip_based", "hostname_hash", "sequential", "random")
        vendor_prefix: MAC vendor prefix (first 3 octets) in format XX:XX:XX

    Returns:
        MAC address string in format XX:XX:XX:XX:XX:XX
    """
    # Parse vendor prefix
    try:
        vendor_bytes = [int(x, 16) for x in vendor_prefix.split(':')]
        if len(vendor_bytes) != 3:
            raise ValueError("Invalid vendor prefix format")
    except (ValueError, AttributeError):
        # Default fallback
        vendor_bytes = [0x00, 0x16, 0x3e]

    if master_template_method == "ip_based" and ip_address:
        # IP-based MAC generation (using last 3 octets of IP)
        try:
            ip_parts = [int(x) for x in ip_address.split('.')]
            if len(ip_parts) == 4:
                # Use last 3 octets
                mac_suffix = [ip_parts[1], ip_parts[2], ip_parts[3]]
                mac_bytes = vendor_bytes + mac_suffix
                return ':'.join(f'{b:02x}' for b in mac_bytes)
            else:
                # Invalid IP, fall back to random
                pass
        except (ValueError, IndexError):
            # Invalid IP, fall back to random
            pass

    if master_template_method == "hostname_hash" and hostname:
        # Hostname-based MAC generation
        try:
            hash_obj = hashlib.md5(hostname.encode())
            hash_bytes = hash_obj.digest()[:3]  # First 3 bytes
            mac_bytes = vendor_bytes + list(hash_bytes)
            return ':'.join(f'{b:02x}' for b in mac_bytes)
        except:
            # Hostname hashing failed, fall back to random
            pass

    if master_template_method == "sequential":
        # Sequential MAC generation (simplified - uses timestamp)
        import time
        timestamp = int(time.time()) & 0xFFFFFF  # Last 3 bytes
        mac_bytes = vendor_bytes + [
            (timestamp >> 16) & 0xFF,
            (timestamp >> 8) & 0xFF,
            timestamp & 0xFF
        ]
        return ':'.join(f'{b:02x}' for b in mac_bytes)

    # Default: random with vendor prefix
    random_suffix = [random.randint(0, 255) for _ in range(3)]
    mac_bytes = vendor_bytes + random_suffix
    return ':'.join(f'{b:02x}' for b in mac_bytes)


def is_valid_mac_address(mac: str) -> bool:
    """
    Validate MAC address format.

    Args:
        mac: MAC address string to validate

    Returns:
        True if valid MAC address format, False otherwise
    """
    if not mac or not isinstance(mac, str):
        return False

    parts = mac.split(':')
    if len(parts) != 6:
        return False

    try:
        for part in parts:
            if len(part) != 2:
                return False
            int(part, 16)  # Will raise ValueError if not hex
        return True
    except ValueError:
        return False


def normalize_mac_address(mac: str) -> str:
    """
    Normalize MAC address to lowercase with colon separators.

    Args:
        mac: MAC address string to normalize

    Returns:
        Normalized MAC address string
    """
    if not mac:
        return ""

    # Remove any separators and convert to lowercase
    clean = mac.replace('-', '').replace(':', '').replace('.', '').lower()

    # Add colons every 2 characters
    if len(clean) == 12:
        return ':'.join([clean[i:i+2] for i in range(0, 12, 2)])
    else:
        return mac  # Return as-is if invalid length