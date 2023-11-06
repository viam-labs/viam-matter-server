#!/usr/bin/env bash
cd `dirname $0`

source .env
./setup.sh

exec "${PYTHON:-python3}" -m src.main $@