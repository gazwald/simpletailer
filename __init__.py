#!/usr/bin/env python3
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import time
from errno import ENOENT


class SimpleTailer():
    def __init__(self, filepath):
        """
        Initialise and seek to the end of the file
        """
        self.handle = None
        if os.path.isfile(filepath):
            self.filepath = filepath
            self.open_handle()
            self.handle.seek(0, os.SEEK_END)
        else:
            raise IOError(ENOENT, 'File not found', filepath)

    def open_handle(self):
        """
        Open the file and record its size
        """
        self.handle = open(self.filepath, 'r')
        self.current_state = os.stat(self.filepath)
        self.size = self.current_state.st_size

    def reopen_handle(self):
        """
        Explicitly close the file and then open it again.
        Don't seek to the end to avoid missing data
        """
        self.handle.close()
        self.open_handle()

    def truncated_check(self):
        """
        Check the file was truncated
        If it was truncated then reopen it
        Otherwise update its size
        """
        self.current_state = os.stat(self.filepath)
        if self.size > self.current_state.st_size:
            self.reopen_handle()
        else:
            self.size = self.current_state.st_size

    def __iter__(self):
        while True:
            try:
                self.truncated_check()
                line = self.handle.readline()

                if line:
                    yield line.strip()
                else:
                    time.sleep(1)
                    continue
            except KeyboardInterrupt:
                raise

    def __exit__(self):
        pass

    def __del__(self):
        if self.handle is not None:
            self.handle.close()
