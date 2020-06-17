import sys
import argparse
from nubia import Nubia, PluginInterface, Options

from vkb.cli import commands


class VKBCLI(Nubia):
    def _parse_args(self, cli_args=sys.argv):
        args = super()._parse_args(cli_args)
        setattr(args, "verbose", True)
        setattr(args, "stderr", True)
        return args


class VKBPlugin(PluginInterface):
    def get_opts_parser(self, add_help=True):
        opts_parser = argparse.ArgumentParser(
            description="VKB Command Utility",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            add_help=add_help,
        )
        return opts_parser


def main():
    shell = VKBCLI(
        name="vkb",
        command_pkgs=commands,
        plugin=VKBPlugin(),
        options=Options(persistent_history=True),
    )
    sys.exit(shell.run())


if __name__ == "__main__":
    main()
