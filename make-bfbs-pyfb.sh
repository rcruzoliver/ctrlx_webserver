#!/usr/bin/env bash

# Generate the binaries 
mkdir -p bfbs
bin/oss.flatbuffers/ubuntu22-gcc-x64/release/flatc -o bfbs/ -b --schema flatbuffers/robotActualValues.fbs

# Generate the python libraries
bin/oss.flatbuffers/ubuntu22-gcc-x64/release/flatc --python flatbuffers/robotActualValues.fbs 

