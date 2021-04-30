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

from prettytable import PrettyTable
from datetime import datetime
from .util import file_mgmt
from os import getenv
from os.path import join, exists


class History(object):
    def __init__(self, keep=None, deleted=None, ips_deleted=None, vols_deleted=None):
        self.keep = keep
        self.deleted = deleted
        self.ips_deleted = ips_deleted
        self.vols_deleted = vols_deleted
        self.report = self.create_report()
        self.history_path = join(getenv('HOME'), ".janitor_history.txt")

    def update_history(self):
        """append latest report to history file"""
        if self.report:
            file_mgmt('w', file_path=self.history_path, content=self.report)

    def print_history(self):
        """print history file"""
        if exists(self.history_path):
            history = file_mgmt('r', file_path=self.history_path)
            print(history)
        else:
            print("no history yet")

    def print_report(self):
        """print current report"""
        if self.report:
            print(self.report)

    def create_report(self):
        """
        create a simple report based on: when, what and who
        """
        # nothing to display
        if not self.keep and not self.deleted and not self.ips_deleted and not self.vols_deleted:
            return None

        # instances/vm report
        vm_report = PrettyTable(['TIMESTAMP', 'ACTION', 'NAME', 'IPs',
                                 'IMAGE', 'CREATED AT (UTC)'])
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for vm in self.deleted:
            vm_report.add_row([now, 'deleted', vm['name'],
                               vm['ips'], vm['image'],
                               vm['created_at']])

        for vm in self.keep:
            vm_report.add_row([now, 'in whitelist', vm['name'],
                               vm['ips'], vm['image'],
                               vm['created_at']])

        # floating ip report
        ip_report = PrettyTable(['TIMESTAMP', 'ACTION', 'FLOATING IP'])
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        for ip in self.ips_deleted:
            ip_report.add_row([now, 'deleted', ip['floating_ip_address']])

        # volumes report
        vol_report = PrettyTable(['TIMESTAMP', 'ACTION', 'VOLUME ID'])
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        for vol in self.vols_deleted:
            vol_report.add_row([now, 'deleted', vol])

        # group all reports
        full_report = None

        if vm_report.rows.__len__() > 0:
            full_report = str(vm_report) + "\n"

        if ip_report.rows.__len__() > 0:
            full_report = full_report + str(ip_report) + "\n\n"

        if vol_report.rows.__len__() > 0:
            full_report = full_report + str(vol_report) + "\n\n"

        return full_report
