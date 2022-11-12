#!/bin/bash
nslookup www.google.com 203.28.128.1 | awk -F ': ' 'NR==6{ print $2 }'
