#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import click

from janitor.provider.openstack import OpenstackSDK
from janitor.module.clean import Clean
from janitor.module.history import History
from sys import exit


@click.group()
def cli():
    """Janitor clean-up the left-over in your Openstack tenant to know more
    check documentation running: man janitor"""
    pass


@click.command(short_help='clean-up VM and public IP from Openstack tenant')
@click.option('--openrc', multiple=False,
              type=click.Path(), help="path to your openstacksdk openrc file",
              required=False)
@click.option('--whitelist', envvar='WHITELIST', multiple=False,
              type=click.Path(), help="path to your whitelist file to keep",
              required=True)
@click.option('--keystone', multiple=False, type=click.Path(), help="Keystone version: v2 or v3",
              required=True)
def openstack(openrc, whitelist, keystone):
    openstack = OpenstackSDK(openrc, keystone)
    try:
        vms = openstack.get_all_instances()
        volumes = openstack.get_volume(status={'status': 'available'})
    except Exception as ex:
        print(ex)
        exit(1)
    # clean up
    clean = Clean(vms, whitelist, volumes, openstack)
    clean.run()


@click.command(short_help='show janitor history')
def history():
    # History
    history = History()
    history.print_history()


def janitor():
    cli.add_command(openstack)
    cli.add_command(history)
    cli(prog_name='janitor')


if __name__ == "__main__":
    janitor()
