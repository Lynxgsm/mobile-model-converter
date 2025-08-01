# Mobile Model Converter

A Docker-based environment for mobile model conversion with Python 3.10.0 on Debian.

## Prerequisites

- Docker
- Docker Compose

## Quick Start

### Build and run the container

```bash
# Build and start the container
docker-compose up --build

# Run in detached mode
docker-compose up -d --build

# Stop the container
docker-compose down
```

### Development mode

```bash
# Run with development profile
docker-compose --profile dev up --build
```

### Interactive shell

```bash
# Access the container shell
docker-compose exec mobile-model-converter bash

# Or run a new container instance
docker-compose run --rm mobile-model-converter bash
```

## Container Details

- **Base Image**: Debian Bullseye (slim)
- **Python Version**: 3.10.0
- **Working Directory**: `/app`
- **User**: Non-root user (appuser)

## Volume Mounts

- Current directory → `/app`
- `./models` → `/app/models` (for persistent model storage)

## Ports

- **8000**: Main application port
- **8001**: Development server port (when using dev profile)

## Environment Variables

- `PYTHONPATH=/app`
- `PYTHONUNBUFFERED=1`
- `ENVIRONMENT=development` (in dev profile)

## Customization

### Modify Python dependencies

Edit `requirements.txt` and rebuild:

```bash
docker-compose build --no-cache
```

### Run a specific Python script

Uncomment and modify the command in `docker-compose.yml`:

```yaml
command: ['python3', 'your_script.py']
```

### Add additional system packages

Modify the `RUN apt-get install` section in the `Dockerfile`.

## Troubleshooting

### Check container logs

```bash
docker-compose logs mobile-model-converter
```

### Rebuild without cache

```bash
docker-compose build --no-cache
```

### Clean up Docker resources

```bash
docker system prune -a
```
