#!/bin/bash

cd ..

export ENV=dev

nodemon --exec ".venv/Scripts/python -m file_segment_service.main" --ext py
