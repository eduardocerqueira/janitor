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

from os import getenv, getcwd
from os.path import exists, join, dirname


ROOT = dirname(getcwd())
print ROOT

def get_openstack_creds():

    ops_creds = getenv("OPENSTACK_CREDS")
    if ops_creds:
        print "Using %s" % ops_creds
        return ops_creds
    # root and workspace folder
    elif exists(join(ROOT, 'test-openrc.sh')):
        ops_creds = join(ROOT, 'test-openrc.sh')
        print "Using %s" % ops_creds
        return ops_creds
    # tests folder
    elif exists(join(ROOT, 'tests/test-openrc.sh')):
        ops_creds = join(ROOT, 'tests/test-openrc.sh')
        print "Using %s" % ops_creds
        return ops_creds
    # janitor folder
    elif exists(join(ROOT, 'janitor/tests/test-openrc.sh')):
        ops_creds = join(ROOT, 'janitor/tests/test-openrc.sh')
        print "Using %s" % ops_creds
        return ops_creds
    else:
        raise Exception("missing Openstack credentials")

OPENSTACK_CREDS_PATH = get_openstack_creds()
