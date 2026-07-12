#!/usr/bin/env python3
import copy, click, yaml
from rich.console import Console
from rich.table import Table

console = Console()

SERVICE_TEMPLATES = {
    "api": {
        "build": {"context": "./api", "dockerfile": "Dockerfile"},
        "ports": ["8000:8000"],
        "environment": {"APP_ENV": "production"},
        "networks": ["backend"],
        "healthcheck": {"test": ["CMD", "curl", "-f", "http://localhost:8000/health"], "interval": "30s", "timeout": "10s", "retries": 3},
        "restart": "unless-stopped",
    },
    "web": {
        "image": "nginx:alpine",
        "ports": ["80:80"],
        "networks": ["frontend"],
        "depends_on": {"api": {"condition": "service_healthy"}},
        "restart": "unless-stopped",
    },
    "db": {
        "image": "postgres:16-alpine",
        "environment": {"POSTGRES_DB": "app", "POSTGRES_USER": "postgres", "POSTGRES_PASSWORD": "postgres"},
        "volumes": ["pgdata:/var/lib/postgresql/data"],
        "networks": ["backend"],
        "healthcheck": {"test": ["CMD-SHELL", "pg_isready -U postgres"], "interval": "10s", "timeout": "5s", "retries": 5},
        "restart": "unless-stopped",
    },
    "cache": {
        "image": "redis:7-alpine",
        "command": "redis-server --maxmemory 256mb --maxmemory-policy allkeys-lru",
        "volumes": ["redisdata:/data"],
        "networks": ["backend"],
        "healthcheck": {"test": ["CMD", "redis-cli", "ping"], "interval": "10s", "timeout": "5s", "retries": 5},
        "restart": "unless-stopped",
    },
    "redis": "cache",
    "worker": {
        "build": {"context": "./worker", "dockerfile": "Dockerfile"},
        "environment": {"REDIS_URL": "redis://cache:6379/0"},
        "networks": ["backend"],
        "restart": "unless-stopped",
    },
    "monitor": {
        "image": "prom/prometheus:latest",
        "ports": ["9090:9090"],
        "volumes": ["./prometheus.yml:/etc/prometheus/prometheus.yml:ro", "promdata:/prometheus"],
        "networks": ["monitoring"],
        "restart": "unless-stopped",
    },
}

def resolve(name):
    t = SERVICE_TEMPLATES.get(name)
    return SERVICE_TEMPLATES[t] if t == "cache" else t

def generate_compose(services, project="app", port=8000):
    compose = {"version": "3.9", "services": {}, "volumes": {}, "networks": {}}
    nets, vols = set(), set()
    for svc in services:
        tmpl = resolve(svc)
        if not tmpl:
            console.print(f"[yellow]Unknown: {svc}[/yellow]")
            continue
        svc_def = copy.deepcopy(tmpl)
        if svc == "api":
            svc_def["ports"] = [f"{port}:{port}"]
        for n in svc_def.get("networks", []): nets.add(n)
        for v in svc_def.get("volumes", []):
            if isinstance(v, str) and ":" in v and not v.startswith("./"):
                vol_name = v.split(":")[0]
                if vol_name not in ("", "."):
                    vols.add(vol_name)
        compose["services"][svc] = svc_def
    for n in nets: compose["networks"][n] = {"driver": "bridge"}
    for v in vols: compose["volumes"][v] = None
    return compose

@click.group()
def cli():
    pass

@cli.command()
@click.argument("services", nargs=-1)
@click.option("-o", "--output", default="docker-compose.yml")
@click.option("-p", "--project", default="app")
@click.option("--port", default=8000)
def create(services, output, project, port):
    if not services:
        console.print("[red]No services specified[/red]")
        return
    compose = generate_compose(list(services), project, port)
    with open(output, "w") as f:
        yaml.dump(compose, f, default_flow_style=False, sort_keys=False)
    console.print(f"[green]Generated {output}: {', '.join(services)}[/green]")

@cli.command("list-services")
def list_services():
    table = Table(title="Available Services")
    table.add_column("Service", style="cyan")
    table.add_column("Description", style="white")
    for svc, desc in {"api": "FastAPI backend", "web": "Nginx proxy", "db": "PostgreSQL", "cache": "Redis", "worker": "Background worker", "monitor": "Prometheus"}.items():
        table.add_row(svc, desc)
    console.print(table)

if __name__ == "__main__":
    cli()
