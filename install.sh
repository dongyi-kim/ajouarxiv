#!/usr/bin/env bash
pip install rcssmin --install-option="--without-c-extensions"
pip install rjsmin --install-option="--without-c-extensions"
pip install django-compressor --upgrade
pip install -r requirements.txt
