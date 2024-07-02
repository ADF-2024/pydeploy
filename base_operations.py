import base64
import paramiko
import io

from ftplib import FTP
from ftp_operations import connect_ftp, clean_ftp, upload_ftp, check_connection_ftp
from config import load_config, get_or_create_target, save_config, add_connection
from encryption import encrypt_value, decrypt_value, derive_key

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def check_connection(target=None):
    config = load_config()
    
    if target is None:
        target = get_or_create_target(config)
        if target is None:
            return

    if target not in config['targets']:
        print(f"Target {target} not found in config.")
        return

    target_config = config['targets'][target]
    
    if 'local_path' not in target_config:
        print("Error: 'local_path' not found in configuration.")
        return

    local_path = target_config['local_path']

    if 'password' in target_config:
        password = base64.b64decode(target_config['password']).decode()
    elif 'private_key' in target_config:
        private_key = base64.b64decode(target_config['private_key']).decode()

    print(f"Checking connection to {target}...")

    try:
        if target_config['type'] == 'ftp':
            ftp = connect_ftp(target_config['host'], target_config['username'], password)
            if check_connection_ftp(ftp, target_config['remote_path']):
                print(f"FTP connection to {target} successful!")
                print(f"Changed to remote directory: {target_config['remote_path']}")
            ftp.quit()
        elif target_config['type'] == 'sftp':
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            if 'password' in target_config:
                ssh.connect(target_config['host'], username=target_config['username'], password=password)
            else:
                private_key = paramiko.RSAKey.from_private_key(io.StringIO(private_key))
                ssh.connect(target_config['host'], username=target_config['username'], pkey=private_key)
            
            with ssh.open_sftp() as sftp:
                sftp.chdir(target_config['remote_path'])
                print(f"SFTP connection to {target} successful!")
                print(f"Changed to remote directory: {target_config['remote_path']}")
            ssh.close()
    except Exception as e:
        print(f"Connection to {target} failed: {str(e)}")
    else:
        print("Connection check completed successfully.")

def clean(target):
    config = load_config()
    
    if target not in config['targets']:
        print(f"Target {target} not found in config.")
        return

    target_config = config['targets'][target]
    
    if 'password' in target_config:
        password = base64.b64decode(target_config['password']).decode()
    elif 'private_key' in target_config:
        private_key = base64.b64decode(target_config['private_key']).decode()

    print(f"Cleaning {target}...")

    try:
        if target_config['type'] == 'ftp':
            ftp = connect_ftp(target_config['host'], target_config['username'], password)
            clean_ftp(ftp, target_config['remote_path'], config.get('exclude_from_clean', []))
            ftp.quit()
        elif target_config['type'] == 'sftp':
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            if 'password' in target_config:
                ssh.connect(target_config['host'], username=target_config['username'], password=password)
            else:
                private_key = paramiko.RSAKey.from_private_key(io.StringIO(private_key))
                ssh.connect(target_config['host'], username=target_config['username'], pkey=private_key)
            
            with ssh.open_sftp() as sftp:
                clean_sftp(sftp, target_config['remote_path'], config.get('exclude_from_clean', []))
            ssh.close()
        print(f"Cleaning of {target} completed successfully.")
    except Exception as e:
        print(f"Cleaning of {target} failed: {str(e)}")

def deploy(target=None):
    config = load_config()
    
    if target is None:
        target = get_or_create_target(config)
        if target is None:
            return

    if target not in config['targets']:
        print(f"Target {target} not found in config.")
        return

    target_config = config['targets'][target]
    
    if 'password' in target_config:
        password = base64.b64decode(target_config['password']).decode()
    elif 'private_key' in target_config:
        private_key = base64.b64decode(target_config['private_key']).decode()

    print(f"Deploying to {target}...")

    try:
        if target_config['type'] == 'ftp':
            ftp = connect_ftp(target_config['host'], target_config['username'], password)
            if check_connection_ftp(ftp, target_config['remote_path']):
                if config.get('clean_before_deploy', False):
                    clean_ftp(ftp, target_config['remote_path'], config.get('exclude_from_clean', []))
                upload_ftp(ftp, target_config['local_path'], target_config['remote_path'])
                ftp.quit()
        elif target_config['type'] == 'sftp':
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            if 'password' in target_config:
                ssh.connect(target_config['host'], username=target_config['username'], password=password)
            else:
                private_key = paramiko.RSAKey.from_private_key(io.StringIO(private_key))
                ssh.connect(target_config['host'], username=target_config['username'], pkey=private_key)
            
            with ssh.open_sftp() as sftp:
                if config.get('clean_before_deploy', False):
                    clean_sftp(sftp, target_config['remote_path'], config.get('exclude_from_clean', []))
                upload_sftp(sftp, target_config['local_path'], target_config['remote_path'])
            ssh.close()
        print(f"Deployment to {target} completed successfully.")
    except Exception as e:
        print(f"Deployment to {target} failed: {str(e)}")

