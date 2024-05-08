#!/usr/bin/env bash

# Generate the binaries 
mkdir -p mddb
bin/comm.datalayer/ubuntu22-gcc-x64/release/mddb_compiler -in metadata.csv -out ./mddb/metadata.mddb

