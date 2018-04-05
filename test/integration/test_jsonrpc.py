import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from wantd import WantDaemon
from want_config import WantConfig


def test_wantd():
    config_text = WantConfig.slurp_config_file(config.want_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'0000025bdd1e5be1a4a0b51e27e50fd3b33fd44662bafe8fdd6b492e7a970d26'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'0000053e7d8b8f6378294376c4e3bc40206dcad982aaad2e714b2c762baf0a92'

    creds = WantConfig.get_rpc_creds(config_text, network)
    wantd = WantDaemon(**creds)
    assert wantd.rpc_command is not None

    assert hasattr(wantd, 'rpc_connection')

    # Want testnet block 0 hash == 00000bafbc94add76cb75e2ec92894837288a481e5c005f6563d91623bf8bc2c
    # test commands without arguments
    info = wantd.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert wantd.rpc_command('getblockhash', 0) == genesis_hash
