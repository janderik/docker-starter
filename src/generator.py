#!/usr/bin/env python3
"""
Docker Starter - Template Generator

Generate Docker Compose configurations from templates.
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any


class TemplateGenerator:
    """Generate Docker Compose configurations."""
    
    TEMPLATES_DIR = Path(__file__).parent.parent / 'templates'
    
    TEMPLATES = {
        'nginx-proxy': {
            'services': {
                'nginx': {
                    'image': 'nginx:alpine',
                    'ports': ['80:80', '443:443'],
                    'volumes': ['./nginx.conf:/etc/nginx/nginx.conf:ro']
                }
            }
        },
        'postgres': {
            'services': {
                'postgres': {
                    'image': 'postgres:15-alpine',
                    'environment': {
                        'POSTGRES_DB': 'mydb',
                        'POSTGRES_USER': 'user',
                        'POSTGRES_PASSWORD': 'password'
                    },
                    'ports': ['5432:5432'],
                    'volumes': ['postgres_data:/var/lib/postgresql/data']
                }
            },
            'volumes': {
                'postgres_data': {}
            }
        },
        'redis': {
            'services': {
                'redis': {
                    'image': 'redis:7-alpine',
                    'ports': ['6379:6379'],
                    'volumes': ['redis_data:/data']
                }
            },
            'volumes': {
                'redis_data': {}
            }
        },
        'mongodb': {
            'services': {
                'mongo': {
                    'image': 'mongo:6',
                    'ports': ['27017:27017'],
                    'environment': {
                        'MONGO_INITDB_ROOT_USERNAME': 'admin',
                        'MONGO_INITDB_ROOT_PASSWORD': 'password'
                    },
                    'volumes': ['mongo_data:/data/db']
                }
            },
            'volumes': {
                'mongo_data': {}
            }
        },
        'prometheus-grafana': {
            'services': {
                'prometheus': {
                    'image': 'prom/prometheus:latest',
                    'ports': ['9090:9090'],
                    'volumes': ['./prometheus.yml:/etc/prometheus/prometheus.yml']
                },
                'grafana': {
                    'image': 'grafana/grafana:latest',
                    'ports': ['3000:3000'],
                    'environment': {
                        'GF_SECURITY_ADMIN_PASSWORD': 'admin'
                    }
                }
            }
        },
    }
    
    def list_templates(self) -> List[str]:
        """List available templates."""
        return list(self.TEMPLATES.keys())
    
    def create(self, template_name: str, output_dir: str = '.') -> str:
        """
        Create a Docker Compose file from a template.
        
        Args:
            template_name: Name of the template.
            output_dir: Output directory.
            
        Returns:
            Path to the created file.
        """
        if template_name not in self.TEMPLATES:
            raise ValueError(f"Template not found: {template_name}")
        
        template = self.TEMPLATES[template_name]
        
        output_path = Path(output_dir) / template_name
        output_path.mkdir(parents=True, exist_ok=True)
        
        compose_file = output_path / 'docker-compose.yml'
        
        # Generate docker-compose.yml
        import yaml
        
        with open(compose_file, 'w') as f:
            yaml.dump(template, f, default_flow_style=False)
        
        return str(compose_file)


if __name__ == '__main__':
    import sys
    
    generator = TemplateGenerator()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python generator.py list          - List templates")
        print("  python generator.py create <name> - Create from template")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'list':
        print("Available templates:")
        for name in generator.list_templates():
            print(f"  - {name}")
    
    elif command == 'create':
        if len(sys.argv) < 3:
            print("Please specify template name")
            sys.exit(1)
        
        template_name = sys.argv[2]
        output = generator.create(template_name)
        print(f"Created: {output}")
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
