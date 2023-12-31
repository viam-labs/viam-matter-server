#!/usr/bin/env bash

SUDO=sudo

if ! command -v $SUDO; then
    echo "no sudo on this system, proceeding as current user"
    SUDO=""
fi

if command -v apt-get; then
    if dpkg -l python3-venv; then
        echo "python3-venv is install, skipping setup"
    else
        if ! apt info python3-venv; then
            echo "package info not found, trying apt update"
            $SUDO apt-get -qq update
        fi
        $SUDO apt-get install -qqy python3-venv
    fi
else
    echo "Skipping tool installation because your platform is missing apt-get"
    echo "If you see failures below, install the equivalent of python3-venv for your system"
fi

source .env
if [ ! -d "${VIRTUAL_ENV:=.venv}" ]; then
    echo "creating virtualenv at $VIRTUAL_ENV"
    python3 -m venv $VIRTUAL_ENV
fi
if [ ! -f .installed ]; then
    echo "installling dependencies from wheel"
    package="$(ls dist/ | grep whl)"
    $VIRTUAL_ENV/bin/pip install ./dist/$package[prod]

    if [ $? -eq 0 ]; then
        touch .installed
    fi
fi

# CHIP storage relies on /data directory existing on device
if [ ! -d /data ]; then
    mkdir /data
fi