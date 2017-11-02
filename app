#!/bin/bash
gunicorn -c ./gunicorn.py 'run:create_app()'

