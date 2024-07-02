import os
import yaml

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

CONFIG_FILE = 'config.yaml'

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            config = yaml.safe_load(file)
    else:
        config = {}
    
    # Ensure 'targets' key exists
    if 'targets' not in config:
        config['targets'] = {}
    
    return config

def get_or_create_target(config):
    if not config.get('targets'):
        print("No targets found in the configuration.")
        print("Let's add a new connection.")
        add_connection()
        config = load_config()  # Reload the config after adding a new connection
    
    if len(config['targets']) == 1:
        return next(iter(config['targets']))
    elif len(config['targets']) > 1:
        print("Multiple targets found. Please specify a target.")
        for target in config['targets']:
            print(f"- {target}")
        return None
    else:
        print("No targets found. This shouldn't happen. Please check your configuration.")
        return None


def save_config(config):
    with open(CONFIG_FILE, 'w') as file:
        yaml.dump(config, file)

def add_connection():
    config = load_config()
    
    target = input("Enter target name (e.g., prod, dev): ")
    conn_type = input("Enter connection type (ftp/sftp): ").lower()
    
    if conn_type not in ['ftp', 'sftp']:
        print("Invalid connection type. Please enter 'ftp' or 'sftp'.")
        return

    host = input("Enter host: ")
    username = input("Enter username: ")
    
    if conn_type == 'ftp':
        password = input("Enter password: ")
    else:  # sftp
        use_password = input("Use password for SFTP? (y/n): ").lower() == 'y'
        if use_password:
            password = input("Enter password: ")
        else:
            private_key_path = input("Enter path to private key: ")
            with open(private_key_path, 'r') as key_file:
                private_key = key_file.read()

    remote_path = input("Enter remote path: ")
    
    # Get encryption password
    encryption_password = input("Enter a password to encrypt sensitive data: ")
    salt = os.urandom(16)
    key = derive_key(encryption_password, salt)

    target_config = {
        'type': conn_type,
        'host': host,
        'username': username,
        'remote_path': remote_path,
        'salt': base64.b64encode(salt).decode()
    }

    if conn_type == 'ftp' or (conn_type == 'sftp' and use_password):
        target_config['password'] = encrypt_value(password, key)
    else:
        target_config['private_key'] = encrypt_value(private_key, key)

    config['targets'][target] = target_config
    save_config(config)
    print(f"Connection for {target} has been added and encrypted.")

