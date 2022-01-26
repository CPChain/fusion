
from argparse import _SubParsersAction
import pkg_resources
import os
import pathlib

def get_git_revision(base_path):
    git_dir = pathlib.Path(base_path) / '.git'
    with (git_dir / 'HEAD').open('r') as head:
        ref = head.readline().split(' ')[-1].strip()

    with (git_dir / ref).open('r') as git_hash:
        return git_hash.readline().strip()

def find_tag(proj_dir, revision):
    git_dir = pathlib.Path(proj_dir) / '.git'
    tags_dir = git_dir / "refs/tags"
    for tag in os.listdir(tags_dir):
        with (tags_dir / tag).open('r') as r:
            cur = r.readline().strip()
            if cur == revision:
                return tag

# Return the git revision as a string
def git_version():
    try:
        cmd_dir = os.path.dirname(os.path.realpath(__file__))
        src_dir = os.path.dirname(cmd_dir)
        proj_dir = os.path.dirname(src_dir)
        GIT_REVISION = get_git_revision(proj_dir)
        tag = find_tag(proj_dir, GIT_REVISION)
        if tag is not None:
            return tag
    except OSError as e:
        print(e)
        GIT_REVISION = "Unknown"
    return GIT_REVISION

def get_version():
    return pkg_resources.get_distribution("cpc_fusion").version

def print_version(*_args, **_kwargs):
    print(get_version())

def get_version_parser(subParsers: _SubParsersAction):
    version_parser = subParsers.add_parser('version', help="Get version")
    version_parser.set_defaults(func=print_version)
    return version_parser
