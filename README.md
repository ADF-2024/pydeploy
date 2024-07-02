# Deployment Automation Tool

This project is a deployment automation tool designed to simplify the process of deploying files to remote servers using FTP and SFTP protocols. It provides functionalities to add new connections, check connections, clean remote directories, and deploy files from a local directory to a remote server.

## Features

- **Add Connection**: Add new FTP or SFTP connections with base64 encoded passwords or private keys.
- **Check Connection**: Verify the connection to the remote server.
- **Clean Remote Directory**: Clean the remote directory by deleting files and directories, with an option to exclude certain files.
- **Deploy Files**: Deploy files from a local directory to a remote server, with an option to clean the remote directory before deployment.

## Setup

### Prerequisites

- Python 3.6 or higher
- `pip` (Python package installer)

### Installation

We recommend using [Anaconda](https://www.anaconda.com/products/distribution) to manage your Python environment. Anaconda simplifies package management and deployment.

1. **Install Anaconda**:
    Follow the instructions on the [Anaconda website](https://docs.anaconda.com/anaconda/install/) to download and install Anaconda.

2. **Create a new environment**:
    ```sh
    conda create --name deploy-env python=3.8
    conda activate deploy-env
    ```

3. **Install the required packages**:
    ```sh
    pip install -r requirements.txt
    ```

Alternatively, you can use `pip` directly without Anaconda:

1. **Clone the repository**:
    ```sh
    git clone https://github.com/ADF-2024/pydeploy.git
    cd pydeploy
    ```

2. **Create a virtual environment** (optional but recommended):
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages**:
    ```sh
    pip install -r requirements.txt
    ```

### Configuration

1. **Start the Deploy tool for the first time. It will notice there is no config.yaml and ask
    for your ftp/sftp credentials to create one.**:
    Run the following command and follow the prompts to add a new connection:
    ```sh
    python deploy.py
    ```

    Alternatively, you can copy the `config.yaml.example` to `config.yaml` and create a target on your own. 
    Note that you will need to encrypt the FTP password with base64 manually.
    ```sh
    cp config.yaml.example config.yaml
    ```

### Usage

- **Deploy using the default target**:
    ```sh
    python deploy.py
    ```

- **Deploy to a specific target**:
    ```sh
    python deploy.py <target>
    ```

- **Add a new connection**:
    ```sh
    python deploy.py add
    ```

- **Check connection**:
    ```sh
    python deploy.py --check [<target>]
    ```

- **Clean target**:
    ```sh
    python deploy.py --clean <target>
    ```

- **Show help message**:
    ```sh
    python deploy.py --help
    ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Acknowledgements

- [Paramiko](https://www.paramiko.org/) for SFTP support
- [ftplib](https://docs.python.org/3/library/ftplib.html) for FTP support
- [cryptography](https://cryptography.io/) for encryption support
