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

class History(object):
    def __init__(self, keep, deleted):
        self.keep = keep
        self.deleted = deleted
        self.report = self.create_report()

    def update_history(self):
        """append latest report to history file"""
        return True

    def print_history(self):
        """print history file"""
        return True

    def print_report(self):
        """print current report"""
        print self.report

    def create_report(self):
        """
        create a simple report based on: when, what and who
        """
        report = PrettyTable(['TIMESTAMP', 'ACTION', 'NAME', 'PUBLIC IP',
                              'IMAGE', 'CREATED AT (UTC)'])
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for vm in self.deleted:
            report.add_row([now, 'deleted', vm.name,
                            vm.public_ips, vm.image, vm.created_at])

        for vm in self.keep:
            report.add_row([now, 'in whitelist',
                            vm.name, vm.public_ips, vm.image, vm.created_at])

        return report
