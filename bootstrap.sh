#! /usr/bin/env bash

set -ex

# Compile i18n translations
pybabel compile -d lark_bot_demo/translations

exec gunicorn \
  --worker-class "gevent" \
  --bind="[::]:5000" \
  "lark_bot_demo:create_app()"
