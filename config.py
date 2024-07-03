import os
import yaml
import base64

CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'config.yaml')

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            config = yaml.safe_load(file)
    else:
        config = {}
    
    if 'targets' not in config:
        config['targets'] = {}
    
    return config

def get_or_create_target(config):
    if not config.get('targets'):
        print("No targets found in the configuration.")
        print("Let's add a new connection.")
        add_connection()
        return None
    else:
        target = next(iter(config['targets']))
        local_path = os.path.join(os.path.dirname(__file__), config['targets'][target]['local_path'])
        print(f"Evaluated local path: {local_path}")
        return target
    
    if len(config['targets']) == 1:
        target = next(iter(config['targets']))
        local_path = os.path.join(os.path.dirname(__file__), config['targets'][target]['local_path'])
        print(f"Evaluated local path: {local_path}")
        return target
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
    remote_path = input("Enter remote path (default: /): ") or '/'

    local_path = input("Enter local path (default: ../dist): ") or '../dist'

    base_dir = os.path.dirname(__file__)
    target_config = {
        'local_path': os.path.relpath(local_path, base_dir),
        'local_path': local_path,
        'type': conn_type,
        'host': host,
        'username': username,
        'remote_path': remote_path,
    }

    if conn_type == 'ftp':
        password = input("Enter password: ")
        target_config['password'] = base64.b64encode(password.encode()).decode()
    else:  # sftp
        use_password = input("Use password for SFTP? (y/n): ").lower() == 'y'
        if use_password:
            password = input("Enter password: ")
            target_config['password'] = base64.b64encode(password.encode()).decode()
        else:
            private_key_path = input("Enter path to private key: ")
            with open(private_key_path, 'r') as key_file:
                private_key = key_file.read()
            target_config['private_key'] = base64.b64encode(private_key.encode()).decode()

    config['targets'][target] = target_config
    config['exclude_from_clean'] = ['.htaccess', '.htpasswd']
    save_config(config)
    print(f"Connection for {target} has been added with base64 encoding.")
