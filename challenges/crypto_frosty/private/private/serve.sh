#!/bin/bash
socat -t240 -T240 -d -d TCP4-LISTEN:4444,reuseaddr,fork EXEC:"./src/handle_connection.sh"
