# Autoswat.ch

> Generate color swatch images on the fly.

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

## Steps Left

1.  Add unit tests for the basic routes (root and `/<hex_value>`).
    - [x] basic html layout (favicon, internal links),
    - [x] differently structured hex values,
    - [ ] html color codes,
    - [x] useful error pages (400, 404).
2.  [ ] Add programatic configuration and tests for app config.
3.  [ ] Create a production build with Docker.
4.  [ ] Deploy that build to Digital Ocean and test.
5.  [ ] Create a deploy pipeline that runs:
    - **GitHub** (_push to master_) → <br>
      **Docker Hub** (_build & store image_) → <br>
      **CircleCI** (_run tests_) → <br>
      **Digital Ocean droplet** (_update production_)
6.  Use the pipeline for further TDD of features:
    1. [ ] Add redis for caching and e2e tests.
    2. [ ] Add `/<mode>/<color_value>` route with tests.
    3. [ ] Add JSON responses when requested via headers.
    4. [ ] Add URL query params for size, format, request=json
    5. [ ] Add URL query params for border.
    6. [ ] Add URL query params for text.
    7. [ ] Add URL query params for font and alignment.
