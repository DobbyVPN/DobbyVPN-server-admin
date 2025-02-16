# Dobby VPN Admin Interface

## Installation

### Prerequisites

- **Git**
- **Python 3.12+**
- [**UV**](https://github.com/astral-sh/uv)

### Installation Steps

#### Download UV

```bash
# Install uv on macOS and Linux.
curl -LsSf https://astral.sh/uv/install.sh | sh
# Install uv on macOS and Linux.
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Download repository

```bash
git clone https://github.com/DobbyVPN/DobbyVPN-server-admin.git
cd DobbyVPN-server-admin
```

### Run admin

Simply run

```bash
./admin.py
```

## Usage

`admin.py` python script is a terminal app, that runs user cycle, waiting for one of the next commands:

* Add user to all VPNs
* Remove user from all VPNs
* List of all keys for every VPN
* Add VPN server
* List VPN servers
