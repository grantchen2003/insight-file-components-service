#!/bin/bash

cd ..

export ENV=dev

nodemon --exec ".venv/Scripts/python -u -m file_components_service.main" --ext py
