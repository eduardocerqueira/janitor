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
from util import file_mgmt
from history import History

class Clean(object):
    """ """
    def __init__(self, vms, wlist_path, driver):
        self.vm_list = vms
        self.wlist_path = wlist_path
        self.wlist_data = self.read_whitelist()
        self.driver = driver

    def read_whitelist(self):
        """ """
        if not exists(self.wlist_path):
            raise Exception("File %s not found" % self.wlist_path)

        wlist = file_mgmt('r', file_path=self.wlist_path)
        return wlist.split()


    def match_whitelist(self):
        """ """
        print "ok"

    def run(self):
        """ """
        # Get full name of vms in whitelist and to keep running
        to_keep = []
        to_keep_names = []
        for vm in self.vm_list:
            for wlisted in self.wlist_data:
                if fnmatch(vm.name, wlisted):
                    to_keep.append(vm)
                    to_keep_names.append(vm.name)

        # delete vm not in the whitelist
        deleted = []
        for vm in self.vm_list:
            if vm.name not in to_keep_names:
                if self.driver.delete_instance(vm):
                    deleted.append(vm)
                else:
                    print "Could not delete vm %s" % vm.name

        # history
        history = History(to_keep, deleted)
        history.print_report()

