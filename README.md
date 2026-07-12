# Docker Starter

![Docker](https://img.shields.io/badge/Docker-24+-blue.svg) ![Python](https://img.shields.io/badge/Python-3.9+-blue.svg) ![License](https://img.shields.io/badge/License-MIT-yellow.svg)

Ready-to-use Docker templates and a Python generator.

## Templates

| Template | Services |
|----------|----------|
| full-stack | React + FastAPI + PostgreSQL + Redis |
| web-app | Nginx + App + PostgreSQL |
| monitoring | Prometheus + Grafana + Loki |

## Quick Start

```bash
cp -r templates/full-stack my-project
cd my-project && docker compose up -d

# Or generate custom config
pip install -r requirements.txt
python generator.py --services api db cache -o docker-compose.yml
```

## License

MIT
