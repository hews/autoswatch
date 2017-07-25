# Autoswat.ch

![](http://autoswat.ch/hex/ff0033)
![](http://autoswat.ch/hex/ff9955)
![](http://autoswat.ch/hex/ffffe0)
![](http://autoswat.ch/hex/90ee90)
![](http://autoswat.ch/hex/add8e6)
![](http://autoswat.ch/hex/cc99cc)
![](http://autoswat.ch/hex/ee82ee)
![](http://autoswat.ch/hex/ffc0cb)
![](http://autoswat.ch/hex/d2b48c)
![](http://autoswat.ch/hex/fffff0)
![](http://autoswat.ch/hex/c0c0c0)

#### ***Generate color swatch images on the fly!***

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

## Acquire a Server

### Creating a Virtual Server in the Cloud with DigitalOcean

For this example we will use DigitalOcean. The steps below will create
a working [droplet][droplet] that is provisioned for Docker by using
Docker Machine. 

> Note: You could also create a provisioned droplet using the DigitalOcean
> console, and then simply send Docker commands by using Docker Machine
> with the [`generic` driver][g-driver], or deploy the code with
> GitHub, SSH in and run the commands local to the droplet.

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
# console and SSH into it, like:
$ ssh "root@${DROPLET_IP}"
$ …

# Let's deploy to it! 
```

## Deploy

### Using Docker Machine and Docker Compose (v3)

**TODO:** expand upon:

- [`jwilders/nginx-proxy`][np-repo]
- [`jrcs/docker-letsencrypt-nginx-proxy-companion`][le-repo]
- [`jwilder/docker-gen`][dg-repo]
- [compose v3](https://docs.docker.com/compose/compose-file/)
- *swarm mode and app replicas…*   
   From jwilder's description of his automated Nginx reverse-proxy container:
 
   > While this works well for containers running on a single host, 
   > generating configs for remote hosts requires [service discovery][jw1]. 
   > Take a look at [docker service discovery][jw2] for a solution to that 
   > problem.

```bash
# First, we need to set some more env vars that tell the Docker CLI 
# client to send it's commands to the new droplet instead of localhost.
$ eval $(docker-machine env "${DROPLET_NAME}")

# "Autobots, transform and roll out!"
$ VIRTUAL_HOST=autoswat.ch         # … or whatever host/IP (or localhost) you are using.
$ LETSENCRYPT_EMAIL=XXXXX@XXXXX.ly # … or whatever email you want to use.
$ LETSENCRYPT_DEBUG="true"         # … to enable debug logging in the Let's Encrypt container.
$ docker-compose -f docker/compose.production.yml up -d

# Check in from time-to-time:
$ docker logs nginx_proxy
$ docker logs autoswatch
$ docker logs letsencrypt

# That's it! Visit the site! And finally, reset the environment so that
# Docker commands are sent to localhost only:
$ eval $(docke-machine env -u)
```

---

## Steps Left

0.  Harden and complete the production app creation/deploy:
    - [ ] Check, can I remove `vhost` and `nginx_html` volumes from 
          `letsencrypt` service?
    - [ ] Add non-root user to SSH in with (and other provisioning).
    - [x] Add SSL cert to machine via Let's Encrypt.
    - [x] Set restart policies on the containers.
    - ~~[ ] Ensure ufw configured and on?~~ (Seems like it, but should test again.)
    - ~~[ ] Allow scaling of the `autoswatch` container (dynamic port 
          binding), all proxied by the same `nginx-proxy` container.~~
          (Not dealing with swarm mode for now.)
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

<!-- LINKS -->

[sniffer]:   https://pypi.python.org/pypi/sniffer
[droplet]:   https://www.digitalocean.com/products/compute/
[doctl]:     https://github.com/digitalocean/doctl
[machine]:   https://docs.docker.com/machine/reference/
[do-driver]: https://docs.docker.com/machine/drivers/digital-ocean/
[g-driver]:  https://docs.docker.com/machine/drivers/generic/
[le-repo]:   https://github.com/JrCs/docker-letsencrypt-nginx-proxy-companion
[np-repo]:   https://github.com/jwilder/nginx-proxy
[dg-repo]:   https://github.com/jwilder/docker-gen
[jw1]:       http://jasonwilder.com/blog/2014/02/04/service-discovery-in-the-cloud/
[jw2]:       http://jasonwilder.com/blog/2014/07/15/docker-service-discovery




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

Starting nginx_proxy ... 
Starting nginx_proxy ... done
Creating letsencrypt ... 
Creating letsencrypt ... done
Attaching to autoswatch, nginx_proxy, letsencrypt
nginx_proxy    | forego     | starting dockergen.1 on port 5000
nginx_proxy    | forego     | starting nginx.1 on port 5100
nginx_proxy    | dockergen.1 | 2017/07/25 20:08:48 Generated '/etc/nginx/conf.d/default.conf' from 2 containers
nginx_proxy    | (&c, more of this stuff…)
nginx_proxy    | dockergen.1 | 2017/07/25 20:08:49 Received event start for container 38db2f9fdc3d
letsencrypt    | Creating Diffie-Hellman group (can take several minutes...)
letsencrypt    | Generating DH parameters, 2048 bit long safe prime, generator 2
letsencrypt    | This is going to take a long time
autoswatch     | [docker/cmd.sh]> Loading application in production environment…
autoswatch     | [docker/cmd.sh]> Starting production server:
autoswatch     | *** Starting uWSGI 2.0.15 (64bit) on [Tue Jul 25 20:08:33 2017] ***
autoswatch     | (&c, lots more of this stuff…)
(wait a long time)
letsencrypt    | ...........+.........................+*... (&c for a few hundred lines…)
letsencrypt    | Sleep for 3600s
letsencrypt    | 2017/07/25 20:11:59 Generated '/app/letsencrypt_service_data' from 2 containers
letsencrypt    | 2017/07/25 20:11:59 Running '/app/update_certs'
letsencrypt    | 2017/07/25 20:11:59 Watching docker events
letsencrypt    | Reloading nginx proxy...
letsencrypt    | 2017/07/25 20:11:59 Contents of /app/letsencrypt_service_data did not change. Skipping notification '/app/update_certs'
letsencrypt    | 2017/07/25 20:11:59 Generated '/etc/nginx/conf.d/default.conf' from 2 containers
letsencrypt    | 2017/07/25 20:11:59 [notice] 32#32: signal process started
letsencrypt    | Creating/renewal autoswat.ch certificates... (autoswat.ch)
letsencrypt    | 2017-07-25 20:11:59,898:INFO:simp_le:1211: Generating new account key
letsencrypt    | 2017-07-25 20:12:01,770:INFO:requests.packages.urllib3.connectionpool:756: Starting new HTTPS connection (1): acme-v01.api.letsencrypt.org
letsencrypt    | 2017-07-25 20:12:02,884:INFO:requests.packages.urllib3.connectionpool:756: Starting new HTTPS connection (1): letsencrypt.org
nginx_proxy    | dockergen.1 | 2017/07/25 20:08:49 Contents of /etc/nginx/conf.d/default.conf did not change. Skipping notification 'nginx -s reload'
letsencrypt    | 2017-07-25 20:12:04,412:INFO:requests.packages.urllib3.connectionpool:207: Starting new HTTP connection (1): autoswat.ch
letsencrypt    | 2017-07-25 20:12:04,500:INFO:simp_le:1305: autoswat.ch was successfully self-verified
nginx_proxy    | nginx.1    | autoswat.ch 10.12.0.2 - - [25/Jul/2017:20:12:04 +0000] "GET /.well-known/acme-challenge/hxsrqcghk3hrgb7KnMIZgNKg_T3-mUwmDnd2cJybNa4 HTTP/1.1" 200 87 "-" "python-requests/2.8.1"
letsencrypt    | 2017-07-25 20:12:04,710:INFO:simp_le:1313: Generating new certificate private key
letsencrypt    | 2017-07-25 20:12:07,575:INFO:simp_le:391: Saving account_key.json
letsencrypt    | 2017-07-25 20:12:07,576:INFO:simp_le:391: Saving key.pem
letsencrypt    | 2017-07-25 20:12:07,576:INFO:simp_le:391: Saving chain.pem
letsencrypt    | 2017-07-25 20:12:07,577:INFO:simp_le:391: Saving fullchain.pem
letsencrypt    | 2017-07-25 20:12:07,578:INFO:simp_le:391: Saving cert.pem
letsencrypt    | Reloading nginx proxy...
letsencrypt    | 2017/07/25 20:12:07 Generated '/etc/nginx/conf.d/default.conf' from 2 containers
letsencrypt    | 2017/07/25 20:12:07 [notice] 42#42: signal process started
nginx_proxy    | nginx.1    | autoswat.ch 66.133.109.36 - - [25/Jul/2017:20:12:04 +0000] "GET /.well-known/acme-challenge/hxsrqcghk3hrgb7KnMIZgNKg_T3-mUwmDnd2cJybNa4 HTTP/1.1" 200 87 "-" "Mozilla/5.0 (compatible; Let's Encrypt validation server; +https://www.letsencrypt.org)"
-->
