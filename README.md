# Docker Starter

[![Docker](https://img.shields.io/badge/Docker-24-blue.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

A collection of Docker Compose templates for common application stacks. Quickly start development environments with pre-configured services.

## Features

- **20+ templates** - Ready-to-use Docker Compose configurations
- **Multiple stacks** - Web servers, databases, message queues, monitoring
- **Easy customization** - Environment variable configuration
- **Production-ready** - Best practices included
- **One-click start** - Simple command to launch any stack

## Available Templates

### Web Servers
- nginx-proxy
- apache-proxy
- caddy

### Databases
- postgres
- mysql
- mongodb
- redis
- elasticsearch

### Full Stacks
- lamp
- mean
- mern
- python-flask-postgres

### Monitoring
- prometheus-grafana
- elk-stack

## Installation

```bash
git clone https://github.com/janderik/docker-starter.git
cd docker-starter
```

## Usage

```bash
# List available templates
python src/generator.py list

# Generate a template
python src/generator.py create nginx-proxy

# Start a stack
docker-compose -f templates/nginx-proxy/docker-compose.yml up -d
```

## Contributing

Contributions are welcome!

## License

MIT License
