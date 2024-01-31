te#!/bin/bash

pandoc "$1" \
  -V geometry:a4paper \
  -V geometry:left=3cm \
  -V geometry:right=2cm \
  -V geometry:top=3cm \
  -V geometry:bottom=2cm \
  -o "$2"