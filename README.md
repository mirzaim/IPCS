# Inverted Pendulum Control Systems (IPCS)

https://github.com/mirzaim/ipcs/assets/14794797/dbb25648-a200-43f2-ba07-b77c07779e93

Welcome to the Inverted Pendulum Control Systems (IPCS) project! This system is designed to simulate and control the dynamics of an inverted pendulum.

### Quick Start

To begin, ensure you have Python 3.9 or above installed on your system.

1. Install the required dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

2. Run the program:
   ```bash
   python3 main.py
   ```

3. Optionally, run the program with a custom configuration:
   ```bash
   python3 main.py <path_to_config_file>

   Example:
   python3 main.py src/configs/default.ini
   ```

### Docker

If you prefer to use Docker, you can run the program with the following commands:

```bash
sudo docker run -v <path_to_output_folder>:/ipcs/out -v <path_to_input_config_file>:/ipcs/configs/default.ini --rm -it mirzaim/ipcs:latest

# Or simply
sudo docker run -v ./out/:/ipcs/out --rm -it mirzaim/ipcs:latest

# For custom configuration
sudo docker run -v ./out/:/ipcs/out -v ./default.ini:/ipcs/configs/default.ini --rm -it mirzaim/ipcs:latest
```
**Notice**: The Docker version doesn't support GUI.

### Installation

For detailed installation instructions and getting started with the project on your own computer, refer to [INSTALL.md](./INSTALL.md).

### Contributing

We welcome contributions from the community! If you're interested in contributing, please check out [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.
