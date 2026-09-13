"""
SSH utilities for testing connections and deploying configuration
"""

import paramiko
import socket
import os


def test_ssh_connection(hostname, port, username, password, key_path=None, timeout=10):
    """
    Test SSH connection to a host.
    Returns (success, message) where success is boolean and message is string.
    """
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # If password is empty string, treat as None to allow key auth
        auth_password = password if password != "" else None
        client.connect(
            hostname,
            port=port or 22,
            username=username,
            password=auth_password,
            key_filename=key_path,
            timeout=timeout
        )
        client.close()
        return True, "Connection successful"
    except paramiko.AuthenticationException:
        return False, "Authentication failed"
    except socket.error as e:
        return False, f"Socket error: {str(e)}"
    except Exception as e:
        return False, f"SSH error: {str(e)}"


def run_ssh_command(hostname, port, username, password, command, key_path=None, timeout=10):
    """
    Run a command via SSH and return the output.
    Returns (success, output) where output is stdout+stderr on success, error message on failure.
    """
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        auth_password = password if password != "" else None
        client.connect(
            hostname,
            port=port or 22,
            username=username,
            password=auth_password,
            key_filename=key_path,
            timeout=timeout
        )
        stdin, stdout, stderr = client.exec_command(command)
        exit_status = stdout.channel.recv_exit_status()  # blocking
        output = stdout.read().decode('utf-8', errors='replace')
        error = stderr.read().decode('utf-8', errors='replace')
        client.close()
        if exit_status == 0:
            return True, output + error
        else:
            return False, f"Command exited with status {exit_status}: {output} {error}"
    except paramiko.AuthenticationException:
        return False, "Authentication failed"
    except socket.error as e:
        return False, f"Socket error: {str(e)}"
    except Exception as e:
        return False, f"SSH error: {str(e)}"


def deploy_config_via_ssh(hostname, port, username, password, config_content,
                         target_path, backup=True, key_path=None, timeout=30):
    """
    Deploy configuration file via SSH.
    Returns (success, message) where success is boolean and message is string.
    """
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        auth_password = password if password != "" else None
        client.connect(
            hostname,
            port=port or 22,
            username=username,
            password=auth_password,
            key_filename=key_path,
            timeout=timeout
        )

        # Backup existing file if requested
        if backup:
            backup_cmd = f"if [ -f {target_path} ]; then cp {target_path} {target_path}.bak.$(date +%Y%m%d_%H%M%S); fi"
            stdin, stdout, stderr = client.exec_command(backup_cmd)
            stdout.channel.recv_exit_status()

        # Create directory if it doesn't exist
        dir_path = os.path.dirname(target_path)
        if dir_path:
            mkdir_cmd = f"mkdir -p {dir_path}"
            stdin, stdout, stderr = client.exec_command(mkdir_cmd)
            exit_status = stdout.channel.recv_exit_status()
            if exit_status != 0:
                client.close()
                return False, f"Failed to create directory {dir_path}"

        # Write config content to file using echo and redirection or cat
        # We'll use base64 encoding to avoid issues with special characters
        import base64
        encoded_content = base64.b64encode(config_content.encode('utf-8')).decode('ascii')
        write_cmd = f"echo '{encoded_content}' | base64 -d > {target_path}"
        stdin, stdout, stderr = client.exec_command(write_cmd)
        exit_status = stdout.channel.recv_exit_status()

        if exit_status != 0:
            error_output = stderr.read().decode('utf-8', errors='replace')
            client.close()
            return False, f"Failed to write config file: {error_output}"

        # Verify file was written correctly
        verify_cmd = f"cat {target_path}"
        stdin, stdout, stderr = client.exec_command(verify_cmd)
        exit_status = stdout.channel.recv_exit_status()
        if exit_status == 0:
            written_content = stdout.read().decode('utf-8', errors='replace')
            if written_content.strip() == config_content.strip():
                client.close()
                return True, f"Configuration deployed successfully to {target_path}"
            else:
                client.close()
                return False, "Configuration verification failed - content mismatch"
        else:
            error_output = stderr.read().decode('utf-8', errors='replace')
            client.close()
            return False, f"Failed to verify config file: {error_output}"

    except paramiko.AuthenticationException:
        return False, "Authentication failed"
    except socket.error as e:
        return False, f"Socket error: {str(e)}"
    except Exception as e:
        return False, f"SSH error: {str(e)}"
    finally:
        try:
            client.close()
        except:
            pass