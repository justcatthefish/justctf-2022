#!/bin/bash
socat -t240 -T240 -d -d TCP4-LISTEN:4444,reuseaddr,fork EXEC:"timeout 5m python3 task.py",nofork
