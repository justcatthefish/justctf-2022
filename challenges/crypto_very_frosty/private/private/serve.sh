#!/bin/bash
socat -t960 -T960 -d -d TCP4-LISTEN:4445,reuseaddr,fork EXEC:"./src/handle_connection.sh"
