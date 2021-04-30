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

from fnmatch import fnmatch
from os.path import exists
from .util import file_mgmt
from .history import History


class Clean(object):
    """ """

    def __init__(self, vms, wlist_path, volumes, driver):
        self.vm_list = vms
        self.wlist_path = wlist_path
        self.volumes = volumes
        self.wlist_data = self.read_whitelist()
        self.driver = driver

    def read_whitelist(self):
        """ """
        if not exists(self.wlist_path):
            raise Exception(f"File {self.wlist_path} not found")

        wlist = file_mgmt('r', file_path=self.wlist_path)
        return wlist.split()

    def run(self):
        """ """
        # Get full name of vms in whitelist and to keep running
        to_keep = []
        to_keep_names = []
        for vm in self.vm_list:
            for wlisted in self.wlist_data:
                if fnmatch(vm['name'], wlisted):
                    to_keep.append(vm)
                    to_keep_names.append(vm['name'])

        # delete vm not in the whitelist
        deleted = []
        for vm in self.vm_list:
            if vm['name'] not in to_keep_names:
                try:
                    if self.driver.delete_instance(vm):
                        deleted.append(vm)
                    else:
                        print(f"Could not delete vm {vm['name']}")
                except Exception as ex:
                    print(ex)

        # delete zoombies floating ips
        ips_deleted = []
        zombie_ips = self.driver.get_zoombies_floating_ips()
        try:
            for ip in zombie_ips:
                if self.driver.delete_floating_ip(ip['id']):
                    ips_deleted.append(ip)
                else:
                    print(f"Could not delete ip {ip}")
        except Exception as ex:
            print(ex)

        # delete volumes
        vols_deleted = []
        for vol in self.volumes:
            # extra verification for not attached volumes
            try:
                if len(vol.attachments) == 0:
                    self.driver.cinder.volumes.delete(vol.id)
                    vols_deleted.append(vol.id)
            except Exception as ex:
                print(ex)

        # history
        history = History(to_keep, deleted, ips_deleted, vols_deleted)
        history.print_report()
        history.update_history()
