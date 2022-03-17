import sys
import json
import logging

from cpc_fusion import Web3

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger()

def _get_instance(cf, args, has_address=True):
    """ Get instance
    """
    with open(args.abi, 'r', encoding='UTF-8') as fr:
        contract_data = json.load(fr)
    if not has_address:
        contract = cf.cpc.contract(
            abi=contract_data['abi'], bytecode=contract_data['bytecode'])
    else:
        contract = cf.cpc.contract(address=args.address, abi=contract_data['abi'])
    return contract, contract_data['contractName']


def view_funcs(args):
    """
    调用不需要发交易的 view 方法
    """
    with open(args.abi, 'r', encoding='UTF-8') as fr:
        contract_data = json.load(fr)
    abi = contract_data['abi']

    cf = Web3(Web3.HTTPProvider(args.endpoint))
    instance, name = _get_instance(cf, args)
    log.info(f'{name} contract')
    
    name = args.function
    value = args.parameters

    # 参数处理
    constants = [i for i in abi if i.get('name') == name]
    if len(constants) == 0:
        log.error(f"Can't find this configuration: {name}")
        return
    constant = constants[0]
    if value and len(value.split(',')) != len(constant['inputs']):
        log.error(f'Your input {len(value.split(","))} parameters, not equal to {len(constant["inputs"])}')
        return
    inputs = []
    for i in range(len(constant['inputs'])):
        target = constant['inputs'][i]
        val = value.split(',')[i]
        if target['type'] in ['uint', 'uint256']:
            val = int(val)
        inputs.append(val)

    # call
    print(instance.functions[name](*inputs).call())

def builder_view_func_parser(subparsers):
    view_funcs_parser = subparsers.add_parser('view-func', help="Call external view functions")
    view_funcs_parser.add_argument('--address', type=str, help='Address of this contract', required=True)
    view_funcs_parser.add_argument('--abi', type=str, help='Path of the ABI file', required=True)
    view_funcs_parser.add_argument('--function', type=str, help='Function name of the parameter', required=True)
    view_funcs_parser.add_argument('--parameters', type=str, help='Value of the parameter(split by ,)', required=False)
    view_funcs_parser.add_argument('--value', type=float, help="The value(CPC) of the transaction", default=0, required=False)
    view_funcs_parser.add_argument('--endpoint', type=str, help='RPC endpoint of your node', required=False, default="https://civilian.cpchain.io")
    view_funcs_parser.add_argument('--chainID', type=int, help="ChainID of the chain, mainnet: 337(Default), testnet: 41", default=337)
    view_funcs_parser.set_defaults(func=view_funcs)
    return view_funcs_parser
