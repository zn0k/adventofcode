#!/usr/bin/env python3

import sys

with open(sys.argv[1], "r") as f: 
  lines = [l.strip() for l in f.readlines()]
