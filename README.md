# Dobby VPN Admin Interface

## Installation

### Prerequisites

- **git**
- **python**
- **pip** (Python package installer)

### Installation Steps

```bash
git clone https://github.com/DobbyVPN/DobbyVPN-server-admin.git
cd DobbyVPN-server-admin
pip install -r requirements.txt
python3 main.py
```

## Usage

`main.py` python script is a terminal app, that runs user cycle, waiting for one of the next commands:

* Add user to all added VPNs
* Remove user from all add VPNs
* List of all keys for every added VPN
* Add VPN interface
* Get list of added VPN interfaces

When we run VPN user management command (for example: `add`), we are doing next steps:
1. Make SSH connection with every added VPN
1. For each VPN machine run user management script. VPN machine expected to be Dobby VPN server, that uses [DobbyVPN-server repository](https://github.com/DobbyVPN/DobbyVPN-server) on the `~/DobbyVPN-server/` path, where our user management script is being run
1. Redirect STDIN and STDOUT of user managemnt script to our admin STDOUT
