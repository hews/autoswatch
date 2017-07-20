#!/bin/bash
set -e

RED="\033[0;31m"
YLW="\033[1;33m"
GRN="\033[0;32m"
CYN="\033[0;36m"
END="\033[0m"

docker_print() {
  echo -e "${CYN}[docker/cmd.sh]>${END} $@"
}

if   [ "$ENV" = 'production' ]; then
  docker_print "Loading application in production environment…"
  docker_print "${YLW}WARNING: Not implemented yet.${END}"
  docker_print ""
  docker_print "Loading application in development environment…"
  docker_print "Starting dev server:"

  export ENV FLASK_APP="autoswatch" FLASK_DEBUG="true"
  exec flask run --host=0.0.0.0

elif [ "$ENV" = 'test' ]; then
  docker_print "Loading application in test environment…"
  docker_print "Running tests:"

  exec nosetests

elif [ "$ENV" = 'test-guard' ]; then
  docker_print "Loading application in test environment…"
  docker_print "Running test guard:"

  exec sniffer

else
  docker_print "Loading application in development environment…"
  docker_print "Starting dev server:"

  export ENV FLASK_APP="autoswatch" FLASK_DEBUG="true"
  exec flask run --host=0.0.0.0

fi
