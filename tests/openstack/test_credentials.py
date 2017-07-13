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
from module.openstack import Openstack
from tests import OPENSTACK_CREDS_PATH


class TestCredentials(object):

    def test_negative_credentials(self):
        try:
            Openstack()
        except:
            assert True

    def test_credentials(self):
        openstack = Openstack(OPENSTACK_CREDS_PATH)
        if openstack:
            assert True
        else:
            assert False

    def test_get_all_instances(self):
        openstack = Openstack(OPENSTACK_CREDS_PATH)
        rs = openstack.get_all_instances()
        if rs:
            assert True
        else:
            assert False
