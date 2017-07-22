# Autoswat.ch

#### ***Generate color swatch images on the fly!***

### Versioning

The current codebase version is stored in `VERSION`, and matches the
Docker image tag we want to use along with the code. It can be entered 
on every command below individually, or we can export it into the
environment:

```bash
export BUILD_VERSION=$(cat VERSION | xargs echo -n)
```

> **Note:** the name of this env var is important, as it's hardcoded
> into the Docker Compose files!

### Building an Image

This package relies on Docker to contain and manage the Python
environment. To use it, we need a working image locally. Either pull
the image from Docker Hub or build it.

Pull from Docker Hub:

```bash
docker pull "hews/autoswatch:$BUILD_VERSION"
```

Build locally:

```bash
docker build -t "hews/autoswatch:$BUILD_VERSION" .
```

### Getting Started

To begin a development environment, use:

```bash
# Necessary to export $BUILD_VERSION first!
docker-compose -f docker/compose.development.yml up
```

This runs the build in two separate containers: one is a dev server,
and the other runs a test guard ([sniffer][sniffer]). Both mount the
app files, and their logging overlaps.

### Running Unit Tests (as in CI)

```bash
docker run -e ENV=test --rm "hews/autoswatch:$BUILD_VERSION"
```

### Running a Production Server

```bash
# Necessary to export $BUILD_VERSION first!
docker-compose -f docker/compose.production.yml up
```

---

## Steps Left

1.  Add unit tests for the basic routes (root and `/<hex_value>`).
    - [x] basic html layout (favicon, internal links),
    - [x] differently structured hex values,
    - [x] useful error pages (400, 404).
2.  [x] Add programatic configuration and tests for app config.
    - [x] Create a canonical version that is updated everywhere,
      including in the Docker image, and maybe that can bust caches?
3.  [x] Create a production build with Docker.
4.  [ ] Deploy that build to Digital Ocean and test.
5.  [ ] Create a deploy pipeline that runs:
    - **GitHub** (_push to master_) → <br>
      **Docker Hub** (_build & store image_) → <br>
      **CircleCI** (_run tests_) → <br>
      **Digital Ocean droplet** (_update production_)
6.  Use the pipeline for further TDD of features:
    1. [ ] Add redis for caching and e2e tests. This includes adding
       very long caching data to the requests.
    2. [ ] Add `/<named_color>` route for named colors.
    3. [ ] Add `/(color)|rgb|rgba|cmyk|hsl/<color_value>` routes with 
       tests.
    4. [ ] Add JSON responses when requested via headers.
    5. [ ] Add URL query params for size, format, request=json
    6. [ ] Add URL query params for border.
    7. [ ] Add URL query params for text.
    8. [ ] Add URL query params for font and alignment.

<!-- LINKS -->

[sniffer]: https://pypi.python.org/pypi/sniffer
