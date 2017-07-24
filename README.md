# Autoswat.ch

#### ***Generate color swatch images on the fly!***

![](http://autoswat.ch:5000/hex/fff)
![](http://autoswat.ch:5000/hex/ff0)
![](http://autoswat.ch:5000/hex/f00)
![](http://autoswat.ch:5000/hex/f0f)
![](http://autoswat.ch:5000/hex/00f)
![](http://autoswat.ch:5000/hex/0ff)
![](http://autoswat.ch:5000/hex/000)

![](https://images.microbadger.com/badges/image/hews/autoswatch:0.1.0.svg)
![](https://images.microbadger.com/badges/version/hews/autoswatch:0.1.0.svg)

## Getting Started

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

### Building the Docker Image

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

### Developing

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

## Deploying

Using an example deploy for Digital Ocean, the steps below will create
a working [droplet][droplet] that is running the app by using Docker
Machine to 

Before beginning you should have:

1.  A Digital Ocean account, that has generated an API key and has been
    associated with an SSH public key. Retrieve the API key and the
    SSH key's "fingerprint" when you create them.
2.  [`doctl`][doctl] and `docker-machine` installed.
3.  A floating IP (this is not necessary now, but is helpful).

For all the commands below, remember TIMTOWTDI. Check out the docs for
[`docker-machine`][machine] and its [`digitialocean` driver][do-driver].

```bash
# This can all be done so many ways. Just `env | grep …` first to make 
# sure they're all there.
$ BUILD_VERSION=$(cat VERSION | xargs echo -n)
$ DIGITALOCEAN_ACCESS_TOKEN=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
$ DIGITALOCEAN_SSH_KEY_FINGERPRINT=XX:XX:XX:XX:XX:XX:XX:XX

# Pick any region code you want to create the droplet in. These are
# available when you run `doctl compute region list`; eg 
# blr1 (Bangalore).
$ DIGITALOCEAN_REGION=blr1

# Pick a name for the droplet/docker-machine entry:
$ DROPLET_NAME=autoswatch-blr1-node01
$ docker-machine create --driver digitalocean "${DROPLET_NAME}"
$ …
$ DROPLET_IP=$(docker-machine inspect "${DROPLET_NAME}" -f {{.Driver.IPAddress}})

# Attach a floating IP associated to some domain name, if you wish.
# You can find your floating IPs with `doctl compute floating-ip list`.
$ FLOATING_IP=XXX.XXX.XXX.XXX
$ doctl compute floating-ip-action assign "${FLOATING_IP}" "${DROPLET_IP}"

# Now you should be able to see the new droplet in your DigitalOcean
# console. Let's deploy to it! First, we need to set some more env vars
# that tell Docker to send it's commands to the new droplet instead of
# localhost.
$ eval $(docker-machine env "${DROPLET_NAME}")

# "… transform and roll out!"
$ docker-compose -f docker/compose.production.yml up
$ …

# That's it! Visit the site! And finally, reset the environment so that 
# Docker commands are sent to localhost only:
$ eval $(docke-machine env -u)
```

**TODO:**

Add an Nginx container with Docker Compose, link the two, and set
restart policies.

1. Add non-root user to run the container under.
2. ufw configured and on?
3. Add SSL cert to machine via Let's Encrypt.
4. Return IP from original command.

---

## Steps Left

1.  [x] Deploy build to Digital Ocean and test. 
2.  [ ] Use a container to reverse proxy from nginx with an up-to-date 
    compose file.
3.  [ ] Create a deploy pipeline that runs:
    - **GitHub** (_push to master_) → <br>
      **Docker Hub** (_build & store image_) → <br>
      **CircleCI** (_run tests_) → <br>
      **Digital Ocean droplet** (_update production_)
4.  Use the pipeline for further TDD of features:
    1. [ ] Add redis (for caching) and e2e tests. This includes adding
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

[sniffer]:   https://pypi.python.org/pypi/sniffer
[droplet]:   https://www.digitalocean.com/products/compute/
[doctl]:     https://github.com/digitalocean/doctl
[machine]:   https://docs.docker.com/machine/reference/
[do-driver]: https://docs.docker.com/machine/drivers/digital-ocean/
