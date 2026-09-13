"""
HTTP utilities for testing connections and deploying configuration via API
"""

import httpx
import json
from typing import Tuple, Optional, Dict, Any


def test_http_connection(hostname: str, port: int = None, use_https: bool = False, timeout: int = 10) -> Tuple[bool, str]:
    """
    Test HTTP/HTTPS connection to a host.
    Returns (success, message).
    """
    scheme = "https" if use_https else "http"
    host = hostname
    if port:
        host = f"{hostname}:{port}"
    url = f"{scheme}://{host}"

    try:
        # Follow redirects, but we'll just check if we get a response
        response = httpx.get(url, timeout=timeout, follow_redirects=True)
        if response.status_code < 400:
            return True, f"HTTP {response.status_code} OK"
        else:
            return False, f"HTTP {response.status_code} {response.reason_phrase}"
    except httpx.ConnectError:
        return False, "Connection failed"
    except httpx.TimeoutException:
        return False, "Connection timeout"
    except Exception as e:
        return False, f"Error: {str(e)}"


def deploy_config_via_api(hostname: str, port: int = None, use_https: bool = False,
                         api_endpoint: str = "", api_key: str = "",
                         config_data: Dict[str, Any] = None,
                         timeout: int = 30) -> Tuple[bool, str]:
    """
    Deploy configuration via HTTP API (REST endpoint).
    Returns (success, message).
    """
    if not api_endpoint:
        return False, "No API endpoint specified"

    scheme = "https" if use_https else "http"
    host = hostname
    if port:
        host = f"{hostname}:{port}"
    base_url = f"{scheme}://{host}"

    # Ensure endpoint starts with /
    if not api_endpoint.startswith('/'):
        api_endpoint = '/' + api_endpoint

    url = f"{base_url}{api_endpoint}"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    try:
        if config_data is None:
            config_data = {}

        # Try PUT first (update/replace), then POST (create)
        response = httpx.put(
            url,
            json=config_data,
            headers=headers,
            timeout=timeout
        )

        # If PUT not allowed, try POST
        if response.status_code == 405:  # Method Not Allowed
            response = httpx.post(
                url,
                json=config_data,
                headers=headers,
                timeout=timeout
            )

        if response.status_code < 400:
            return True, f"Configuration deployed successfully via API (HTTP {response.status_code})"
        else:
            try:
                error_detail = response.json()
                return False, f"API error {response.status_code}: {error_detail}"
            except:
                return False, f"API error {response.status_code}: {response.text}"

    except httpx.ConnectError:
        return False, "Connection failed"
    except httpx.TimeoutException:
        return False, "Connection timeout"
    except Exception as e:
        return False, f"API error: {str(e)}"


def test_api_connection(hostname: str, port: int = None, use_https: bool = False,
                       api_endpoint: str = "", api_key: str = "",
                       timeout: int = 10) -> Tuple[bool, str]:
    """
    Test HTTP API connection to a host.
    Returns (success, message).
    """
    if not api_endpoint:
        return False, "No API endpoint specified"

    scheme = "https" if use_https else "http"
    host = hostname
    if port:
        host = f"{hostname}:{port}"
    base_url = f"{scheme}://{host}"

    # Ensure endpoint starts with /
    if not api_endpoint.startswith('/'):
        api_endpoint = '/' + api_endpoint

    url = f"{base_url}{api_endpoint}"

    headers = {"Accept": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    try:
        response = httpx.get(url, headers=headers, timeout=timeout)
        if response.status_code < 400:
            return True, f"API connection successful (HTTP {response.status_code})"
        else:
            return False, f"API connection failed (HTTP {response.status_code})"
    except httpx.ConnectError:
        return False, "Connection failed"
    except httpx.TimeoutException:
        return False, "Connection timeout"
    except Exception as e:
        return False, f"Error: {str(e)}"