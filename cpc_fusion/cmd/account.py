"""

Create account

"""

from argparse import _SubParsersAction
import getpass
import os
import json
from cpc_fusion import Web3


def green_str(s):
    return f'\033[32m{s}\033[0m'


def red_str(s):
    return f'\033[31m{s}\033[0m'


def pair_output(left, right):
    print(green_str(left), right)


def create(output_dir, password):
    cf = Web3('https://civilian.cpchain.io')
    account = cf.cpc.account.create()
    pair_output('Address of your wallet:', account.address)
    keystore = account.encrypt(password)
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    if not os.path.isdir(output_dir):
        raise Exception('output_dir is not a directory')
    file_name = os.path.join(output_dir, f'{account.address}.json')
    with open(file_name, 'w') as f:
        json.dump(keystore, f)
    pair_output('Your keystore is stored in', file_name)


def gen_account(args):
    password = getpass.getpass(green_str('Please set the password of your keystore:'))
    re_input = getpass.getpass(green_str('Please input again:'))
    if password != re_input:
        print(red_str('Passwords do not match!!'))
        return
    create(args.output_dir, password)


def get_account_parser(subParsers: _SubParsersAction):
    account_parser = subParsers.add_parser('account', help="Account operations")
    account_sub_parser = account_parser.add_subparsers(help='Account sub-command')

    create_parser = account_sub_parser.add_parser('create', help='create an account')
    create_parser.add_argument('--output-dir', default="keystore",
                               type=str, help='Specify the output directory')
    create_parser.set_defaults(func=gen_account)
    return create_parser


if __name__ == '__main__':
    gen_account('keystore')
