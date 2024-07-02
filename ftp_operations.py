from ftplib import FTP
import os
import ftplib

def connect_ftp(host, username, password):
    ftp = FTP(host)
    ftp.login(username, password)
    return ftp

def clean_ftp(ftp, remote_path, exclude_list):
    print(f"Starting clean operation in {remote_path}")
    original_dir = ftp.pwd()
    ftp.cwd(remote_path)
    
    files = ftp.nlst()
    
    for item in files:
        if item not in exclude_list and item not in ('.', '..'):
            try:
                ftp.delete(item)
                print(f"Deleted file: {item}")
            except ftplib.error_perm as e:
                if str(e).startswith('550'):  # 550 is the error code for "file unavailable" (usually means it's a directory)
                    delete_directory_ftp(ftp, item)
                else:
                    print(f"Failed to delete {item}: {str(e)}")
    
    ftp.cwd(original_dir)
    print("FTP clean operation completed.")

def delete_directory_ftp(ftp, directory):
    print(f"Attempting to delete directory: {directory}")
    original_dir = ftp.pwd()
    
    try:
        ftp.cwd(directory)
        sub_items = ftp.nlst()
        
        for item in sub_items:
            if item not in ('.', '..'):
                try:
                    ftp.delete(item)
                    print(f"Deleted file in directory: {item}")
                except ftplib.error_perm as e:
                    if str(e).startswith('550'):
                        delete_directory_ftp(ftp, item)
                    else:
                        print(f"Failed to delete {item} in directory {directory}: {str(e)}")
        
        ftp.cwd(original_dir)
        ftp.rmd(directory)
        print(f"Deleted directory: {directory}")
    except ftplib.error_perm as e:
        print(f"Failed to delete directory {directory}: {str(e)}")
        ftp.cwd(original_dir)

def upload_ftp(ftp, local_path, remote_path):
    for root, dirs, files in os.walk(local_path):
        for filename in files:
            local_file = os.path.join(root, filename)
            relative_path = os.path.relpath(local_file, local_path)
            remote_file = os.path.join(remote_path, relative_path).replace("\\", "/")
            
            remote_dir = os.path.dirname(remote_file)
            if not directory_exists_ftp(ftp, remote_dir):
                create_remote_directory_ftp(ftp, remote_dir)
            
            try:
                with open(local_file, 'rb') as file:
                    ftp.storbinary(f'STOR {remote_file}', file)
                print(f"Uploaded: {remote_file}")
            except Exception as e:
                print(f"Failed to upload {local_file}: {str(e)}")

def directory_exists_ftp(ftp, dir):
    file_list = []
    ftp.retrlines('LIST', file_list.append)
    for f in file_list:
        if dir in f.split()[-1]:
            return True
    return False

def create_remote_directory_ftp(ftp, remote_dir):
    dirs = remote_dir.split('/')
    path = ''
    for dir in dirs:
        if dir:
            path += f'/{dir}'
            if not directory_exists_ftp(ftp, path):
                ftp.mkd(path)

def check_connection_ftp(ftp, remote_path):
    try:
        ftp.cwd(remote_path)
        print(f"Successfully connected and changed to directory: {remote_path}")
        return True
    except Exception as e:
        print(f"Failed to connect or change directory: {str(e)}")
        return False

def clean_sftp(sftp, remote_path, exclude_list):
    print(f"Starting clean operation in {remote_path}")
    for item in sftp.listdir(remote_path):
        if item not in exclude_list and item not in ('.', '..'):
            try:
                sftp.remove(f"{remote_path}/{item}")
                print(f"Deleted file: {item}")
            except IOError:
                delete_directory_sftp(sftp, f"{remote_path}/{item}")

    print("SFTP clean operation completed.")

def delete_directory_sftp(sftp, directory):
    print(f"Attempting to delete directory: {directory}")
    for item in sftp.listdir(directory):
        if item not in ('.', '..'):
            try:
                sftp.remove(f"{directory}/{item}")
                print(f"Deleted file in directory: {item}")
            except IOError:
                delete_directory_sftp(sftp, f"{directory}/{item}")
    sftp.rmdir(directory)
    print(f"Deleted directory: {directory}")

def upload_sftp(sftp, local_path, remote_path):
    for root, dirs, files in os.walk(local_path):
        for filename in files:
            local_file = os.path.join(root, filename)
            relative_path = os.path.relpath(local_file, local_path)
            remote_file = os.path.join(remote_path, relative_path).replace("\\", "/")
            
            remote_dir = os.path.dirname(remote_file)
            create_remote_directory_sftp(sftp, remote_dir)
            
            sftp.put(local_file, remote_file)
            print(f"Uploaded: {remote_file}")

def create_remote_directory_sftp(sftp, remote_dir):
    dirs = remote_dir.split('/')
    path = ''
    for dir in dirs:
        if dir:
            path += f'/{dir}'
            try:
                sftp.chdir(path)
            except IOError:
                sftp.mkdir(path)
                sftp.chdir(path)
