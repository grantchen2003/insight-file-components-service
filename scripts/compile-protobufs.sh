#!/bin/bash

cd ../file_segment_service/protobufs

python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. *.proto

# Add "from . " to all lines that match "import *_pb2"
files=$(find . -name '*_pb2_grpc.py')

for file in $files; do
    sed -i -e 's/import \([^ ]*\)_pb2/from . import \1_pb2/' "$file"
done