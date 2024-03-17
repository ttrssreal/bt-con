#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p python3

import os, re
import subprocess as subp

config_file = "/home/{}/.config/bt-con/map".format(os.environ["USER"])
name_map = {}
options = None

lines = open(config_file, "r").readlines()
for i, line in enumerate(lines):
    try:
        line = line.strip()
        if not line:
            continue
        if re.match("^#", line):
            continue
        key, value = line.split()
        key = bytes(key, "utf-8").decode("unicode_escape").encode("utf-8")
        name_map[key] = value
    except Exception as e: print(e); options = "Failed to parse config line:{}".format(i+1).encode()

p = subp.Popen(["dmenu"], stdout=subp.PIPE, stdin=subp.PIPE, stderr=subp.PIPE)
options = b"\n".join(name_map.keys()) if not options else options
stdout_data = p.communicate(input=options)[0]

selection = stdout_data.removesuffix(b"\n")

subp.run(["bluetoothctl", "connect", name_map[selection]])