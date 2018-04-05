#!/bin/bash
set -evx

mkdir ~/.wantcore

# safety check
if [ ! -f ~/.wantcore/.want.conf ]; then
  cp share/want.conf.example ~/.wantcore/want.conf
fi
