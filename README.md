# autoswat.ch

Generate color swatch images on the fly.

## Getting Started

To begin a development environment, use:

```bash
docker-compose -f docker/development.yml build
docker-compose -f docker/development.yml up
```

This runs the build as a dev server AND in a container with a test
guard ([sniffer](https://pypi.python.org/pypi/sniffer)). The logging
overlaps.

## Running Tests Alone

```bash
docker-compose -f docker/development.yml build
docker run -e ENV=test --rm hews/autoswatch:0.1.0
```
