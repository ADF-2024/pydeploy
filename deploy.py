import os

from ftp_operations import connect_ftp, clean_ftp, upload_ftp, check_connection_ftp
from base_operations import deploy, clean, check_connection

import sys

def print_usage():
    print("Usage:")
    print("  py deploy.py                       - Deploy using default target")
    print("  py deploy.py <target>              - Deploy to specific target")
    print("  py deploy.py add                   - Add a new connection")
    print("  py deploy.py --check [<target>]    - Check connection (optional: specific target)")
    print("  py deploy.py --clean <target>      - Clean target")
    print("  py deploy.py <target> --clean      - Clean specific target")
    print("  py deploy.py <target> --check      - Check connection for specific target")
    print("  py deploy.py --help                - Show this help message")

def main():
    if len(sys.argv) == 1:
        deploy()
    elif sys.argv[1] == 'add':
        add_connection()
    elif sys.argv[1] == '--check':
        if len(sys.argv) > 2:
            check_connection(sys.argv[2])
        else:
            check_connection()
    elif sys.argv[1] == '--clean':
        if len(sys.argv) > 2:
            clean(sys.argv[2])
        else:
            print("Please specify a target for cleaning.")
            print_usage()
    elif sys.argv[1] == '--help':
        print_usage()
    else:
        target = sys.argv[1]
        if len(sys.argv) > 2:
            if sys.argv[2] == '--clean':
                clean(target)
            elif sys.argv[2] == '--check':
                check_connection(target)
            else:
                print(f"Unknown command: {sys.argv[2]}")
                print_usage()
        else:
            deploy(target)

if __name__ == "__main__":
    main()