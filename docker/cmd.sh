#!/bin/bash
set -e

RED="\033[0;31m"
YLW="\033[1;33m"
GRN="\033[0;32m"
GRY="\033[0;37m"
CYN="\033[0;36m"
END="\033[0m"

docker_print() {
  echo -e "${GRY}[docker/cmd.sh]>${END} $@"
}

if   [ "$ENV" = "production" ]; then
  docker_print "Loading application in production environment…"
  docker_print "${GRN}Starting production server:${END}"

  # NOTES:
  #   - wsgi-disable-file-wrapper solves an io error caused by sending
  #     a bytes buffer to send_file.

  # QUESTIONS:
  #   - Do not understand manage-script-name or why to use it, but in
  #     multiple example docs.
  #   - Ports should be changed, and maybe aligned with development,
  #     etc?
  #   - What about: --master --processes 4 --threads 2 ?
  #   - Can we proxy to a Unix socket instead of TCP?
  #
  exec uwsgi --uwsgi-socket  :5000     \
             --stats  0.0.0.0:5001     \
             --mount  /=autoswatch:app \
             --manage-script-name      \
             --wsgi-disable-file-wrapper

elif [ "$ENV" = "test" ]; then
  docker_print "Loading application in test environment…"
  docker_print "Running tests:"

  exec nosetests

elif [ "$ENV" = "test-guard" ]; then
  docker_print "Loading application in test environment…"
  docker_print "Running test guard:"

  exec sniffer

else
  docker_print "Loading application in development environment…"
  docker_print "Starting dev server:"

  exec flask run --host=0.0.0.0

fi
