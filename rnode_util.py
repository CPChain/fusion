"""

Join and Quit RNode

"""
import logging
import argparse
import sys

from cpc_fusion import Web3
from cpc_fusion.default_contracts import RNode

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger()

cf = Web3(Web3.HTTPProvider('https://civilian.cpchain.io'))
rnode = RNode(cf)

def join_rnode(args):
    rnode.join(keystorePath=args.keystore)

def quit_rnode(args):
    rnode.quit(keystorePath=args.keystore)

def check_rnode(args):
    if args.addr:
        if rnode.is_rnode(args.addr):
            log.info('This address is RNode')
        else:
            log.info('This address is not RNode')
        return
    log.info('RNode version: %d', rnode.supported_version)
    log.info('RNode locked period: %d min', rnode.period / 60)
    log.info('RNode threshold: %d CPC', cf.fromWei(rnode.threshold, 'ether'))
    log.info('RNodes count: %d', rnode.rnodes_num)

parser = argparse.ArgumentParser()

subparsers = parser.add_subparsers(help="sub-command help")

rnode_parser = subparsers.add_parser('rnode', help="RNode contract")
rnode_sub_parser = rnode_parser.add_subparsers(help='rnode sub-command')

query_rnode_parser = rnode_sub_parser.add_parser('check', help='check parameters for rnode contracts')
query_rnode_parser.add_argument('--addr', type=str, help='Check whether this address is RNode')
query_rnode_parser.set_defaults(func=check_rnode)

join_rnode_parser = rnode_sub_parser.add_parser('join', help='Join RNode')
join_rnode_parser.add_argument('--keystore', type=str, help='Path of the keystore file')
join_rnode_parser.set_defaults(func=join_rnode)

quit_rnode_parser = rnode_sub_parser.add_parser('quit', help='Quit RNode')
quit_rnode_parser.add_argument('--keystore', type=str, help='Path of the keystore file')
quit_rnode_parser.set_defaults(func=quit_rnode)

args = parser.parse_args()
args.func(args)
