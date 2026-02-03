# Crypto Real-Time Price Tracker

[![CI](https://github.com/YOUR_USERNAME/YOUR_REPO/workflows/CI%20-%20Continuous%20Integration/badge.svg)](https://github.com/YOUR_USERNAME/YOUR_REPO/actions)
[![CD](https://github.com/YOUR_USERNAME/YOUR_REPO/workflows/CD%20-%20Continuous%20Deployment/badge.svg)](https://github.com/YOUR_USERNAME/YOUR_REPO/actions)
[![codecov](https://codecov.io/gh/YOUR_USERNAME/YOUR_REPO/branch/main/graph/badge.svg)](https://codecov.io/gh/YOUR_USERNAME/YOUR_REPO)

A real-time cryptocurrency price tracker with support for ALL Binance coins. Features live WebSocket updates, autocomplete search, and multi-currency support (USD/VND).

## Features

- 🔴 **Real-time Updates**: WebSocket connection for live price updates
- 🔍 **Smart Search**: Autocomplete search for all Binance coins
- 💱 **Multi-Currency**: Toggle between USD and VND
- 📊 **24H Stats**: View 24-hour high/low prices
- 🎨 **Modern UI**: Clean, dark-themed interface
- 🚀 **All Binance Coins**: Support for 1000+ cryptocurrencies

## Screenshots

![Crypto Tracker Screenshot](screenshot.png)

## Installation

### Requirements

- Python 3.8 or higher
- tkinter (usually comes with Python)

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

Run the application:

```bash
python crypto_tracker_simple.py
```

### Quick Start

1. Enter a coin code (e.g., BTC, ETH, DOGE) or use the search
2. Click "Load Coin" or press Enter
3. Click "START" to begin real-time tracking
4. Toggle between USD/VND as needed
5. Click "STOP" to pause tracking

## Development

### Running Tests

```bash
pytest
```

### Code Quality

```bash
# Linting
flake8 .

# Security scan
bandit -r .
safety check
```

## Docker

Build and run with Docker:

```bash
# Build image
docker build -t crypto-tracker .

# Run container (requires X11 forwarding for GUI)
docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix crypto-tracker
```

## CI/CD

This project uses GitHub Actions for CI/CD:

- **CI (Continuous Integration)**: Runs on every push/PR
  - Tests on multiple OS (Ubuntu, Windows, macOS)
  - Python versions: 3.8, 3.9, 3.10, 3.11
  - Code linting and security scanning
  - Code coverage reporting

- **CD (Continuous Deployment)**: Runs on main branch pushes and tags
  - Builds executables for all platforms
  - Creates GitHub releases
  - Builds and pushes Docker images

### Setup CI/CD

1. Fork/clone this repository
2. Enable GitHub Actions in your repository settings
3. (Optional) Add secrets for Docker deployment:
   - `DOCKER_USERNAME`: Your Docker Hub username
   - `DOCKER_PASSWORD`: Your Docker Hub password

## Building Executable

Create standalone executable:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name CryptoTracker crypto_tracker_simple.py
```

The executable will be in the `dist/` folder.

## API

This project uses:
- **Binance WebSocket API**: Real-time price updates
- **Binance REST API**: Exchange info and coin listing

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is for informational purposes only. Cryptocurrency trading carries risk. Always do your own research before making investment decisions.

## Support

If you find this project helpful, please give it a ⭐️!

## Contact

- GitHub: [@YOUR_USERNAME](https://github.com/YOUR_USERNAME)
- Email: your.email@example.com

## Changelog

### v1.0.0 (2026-01-30)
- Initial release
- Support for all Binance coins
- Real-time WebSocket updates
- Autocomplete search
- USD/VND currency support
- 24H high/low statistics
