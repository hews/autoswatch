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

### Running a Production Server Locally

```bash
# Necessary to export $BUILD_VERSION & VIRTUAL_HOST first!
VIRTUAL_HOST=localhost
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
# sure they're all there, or add them to a `.env` file first, which is
# loaded by Docker (though env vars in .env are overriden by values
# from the environment).
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
$ VIRTUAL_HOST=autoswat.ch # … or whatever host/IP (or localhost) you are using.
$ docker-compose -f docker/compose.production.yml up -d
$ …

# Check in from time-to-time.
$ docker logs nginx-proxy
$ …
$ docker logs autoswatch
$ …

# That's it! Visit the site! And finally, reset the environment so that 
# Docker commands are sent to localhost only:
$ eval $(docke-machine env -u)
```

---

## Steps Left

0.  Harden and complete the production app creation/deploy:
    - [ ] Set restart policies on the containers.
    - [ ] Allow scaling of autoswatch container (dynamic port binding).
    - [ ] Add non-root user to ssh in with?
    - [x] Ensure ufw configured and on? (Seems like it, but should test again.)
    - [ ] Add SSL cert to machine via Let's Encrypt.
    - [ ] Return IP from original command?
1.  Create a deploy pipeline that runs:
    - [ ] **GitHub** (_push to master_) → <br>
          **Docker Hub** (_build & store image_) → <br>
          **CircleCI** (_run tests_) → <br>
          **Digital Ocean droplet** (_update production_)
2.  Use the pipeline for further TDD of features:
    - [ ] Add redis (for caching) and e2e tests. This includes adding
          very long caching data to the requests.
    - [ ] Add `/<named_color>` route for named colors.
    - [ ] Add `/(color)|rgb|rgba|cmyk|hsl/<color_value>` routes with 
          tests.
    - [ ] Add JSON responses when requested via headers.
    - [ ] Add URL query params for size, format, request=json
    - [ ] Add URL query params for border.
    - [ ] Add URL query params for text.
    - [ ] Add URL query params for font and alignment.

<!--

docker-machine create \
  --driver=generic \
  --generic-ip-address=192.241.220.112 \
  --generic-ssh-key="~/.ssh/id_rsa" \
  autoswatch-docker-sfo1-01

|-----------------------|---------------------|------|
| --generic-engine-port | GENERIC_ENGINE_PORT | 2376 |
| --generic-ip-address  | GENERIC_IP_ADDRESS  | -    |
| --generic-ssh-key     | GENERIC_SSH_KEY     | -    |
| --generic-ssh-user    | GENERIC_SSH_USER    | root |
| --generic-ssh-port    | GENERIC_SSH_PORT    | 22   |

docker-machine create \
  --driver digitalocean \
  --digitalocean-access-token="${DO_API_KEY}" \
  --digitalocean-region=sfo1 \
  --digitalocean-ssh-key-fingerprint="${DO_SSH_FINGERPRINT}" \
  autoswatch-docker-sfo1-02

eval "$(docker-machine env autoswatch-docker-sfo1-02)"

|-------------------------------------|----------------------------------|------------------|
| --digitalocean-access-token         | DIGITALOCEAN_ACCESS_TOKEN        | -                |
| --digitalocean-image                | DIGITALOCEAN_IMAGE               | ubuntu-16-04-x64 |
| --digitalocean-region               | DIGITALOCEAN_REGION              | nyc3             |
| --digitalocean-size                 | DIGITALOCEAN_SIZE                | 512mb            |
| --digitalocean-ipv6                 | DIGITALOCEAN_IPV6                | false            |
| --digitalocean-private-networking   | DIGITALOCEAN_PRIVATE_NETWORKING  | false            |
| --digitalocean-backups              | DIGITALOCEAN_BACKUPS             | false            |
| --digitalocean-userdata             | DIGITALOCEAN_USERDATA            | -                |
| --digitalocean-ssh-user             | DIGITALOCEAN_SSH_USER            | root             |
| --digitalocean-ssh-port             | DIGITALOCEAN_SSH_PORT            | 22               |
| --digitalocean-ssh-key-fingerprint  | DIGITALOCEAN_SSH_KEY_FINGERPRINT | -                |


eval "$(docker-machine env -u)"

-->

<!-- LINKS -->

[sniffer]:   https://pypi.python.org/pypi/sniffer
[droplet]:   https://www.digitalocean.com/products/compute/
[doctl]:     https://github.com/digitalocean/doctl
[machine]:   https://docs.docker.com/machine/reference/
[do-driver]: https://docs.docker.com/machine/drivers/digital-ocean/
