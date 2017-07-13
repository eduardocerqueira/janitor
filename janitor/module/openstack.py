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

import libcloud.security
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
from os import getenv

libcloud.security.VERIFY_SSL_CERT = False


class Credentials(object):
    def __init__(self, openrc=None):
        self.openrc_path = openrc
        self.osp_username = getenv("OS_USERNAME")
        self.osp_password = getenv("OS_PASSWORD")
        self.osp_tenant = getenv("OS_TENANT_NAME")
        self.osp_auth_url = getenv("OS_AUTH_URL")
        self.osp_auth_version = '3.x_password'
        self.osp_service_type = 'compute'
        self.osp_service_region = getenv("OS_REGION_NAME")

        # file overrides env variable
        if self.openrc_path:
            openrc = self.read_openrc()
            self.osp_username = openrc["OS_USERNAME"]
            self.osp_password = openrc["OS_PASSWORD"]
            self.osp_tenant = openrc["OS_TENANT_NAME"]
            self.osp_auth_url = openrc["OS_AUTH_URL"]
            self.osp_service_region = openrc["OS_REGION_NAME"]

        if not self.osp_username:
            raise Exception("Missing OS_USERNAME")

        if not self.osp_password:
            raise Exception("Missing OS_PASSWORD")

        if not self.osp_tenant:
            raise Exception("Missing OS_TENANT_NAME")

        if not self.osp_auth_url:
            raise Exception("Missing OS_AUTH_URL")

        if not self.osp_service_region:
            raise Exception("Missing OS_REGION_NAME")

    def read_openrc(self):
        openrc = {}
        with open(self.openrc_path) as fdata:
            lines = fdata.readlines()
            for line in lines:
                if line.startswith('export'):
                    # string formating
                    kv = line.replace("export", "").replace("\"", "").\
                    strip().split("=")
                    if "/v2.0" in kv[1]:
                        kv[1] = kv[1].replace("/v2.0", "")
                    openrc[kv[0]] = kv[1]
            return openrc


class Openstack(object):
    def __init__(self, openrc=None):
        self.creds = Credentials(openrc)
        openstack = get_driver(Provider.OPENSTACK)
        self.driver = openstack(self.creds.osp_username,
                                self.creds.osp_password,
                                ex_force_auth_version=\
                                self.creds.osp_auth_version,
                                ex_force_auth_url=\
                                self.creds.osp_auth_url,
                                ex_force_service_type=\
                                self.creds.osp_service_type,
                                ex_force_service_region=\
                                self.creds.osp_service_region,
                                ex_tenant_name=self.creds.osp_tenant)

    def get_all_instances(self):
        """Retrieve list of all instances"""
        return self.driver.list_nodes()

    def delete_instance(self, vm):
        """delete openstack instance"""
        return self.driver.destroy_node(vm)



