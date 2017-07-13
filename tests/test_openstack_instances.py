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

import pytest
from provider.openstack import OpenstackSDK
from helper import OPENSTACK_CREDS_PATH


class TestInstances(object):

    def test_get_all_instances(self):
        openstack = OpenstackSDK(OPENSTACK_CREDS_PATH)
        if openstack.get_all_instances():
            assert True
        else:
            assert False

    def test_get_ip_all_instances(self):
        openstack = OpenstackSDK(OPENSTACK_CREDS_PATH)
        servers = openstack.get_all_instances()
        for server in servers:
            if openstack.get_server_ips(server['obj']):
                assert True
            else:
                assert False

    def test_get_zoombies_floating_ips(self):
        openstack = OpenstackSDK(OPENSTACK_CREDS_PATH)
        ips_zoombies = openstack.get_zoombies_floating_ips()
        if ips_zoombies:
            assert True
        else:
            print "ZERO, it is fine!"
            assert True
