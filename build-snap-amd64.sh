#!/usr/bin/env bash
sudo snapcraft clean --destructive-mode
sudo snapcraft --destructive-mode --target-arch=amd64 --enable-experimental-target-arch
