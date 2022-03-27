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

import locale
import os
import time
from errno import ENOENT
from typing import Optional, TextIO


class SimpleTailer:
    def __init__(self, path: str, encoding: Optional[str] = None):
        self.path: str = path
        self.encoding: str = encoding or locale.getpreferredencoding()

    def _open_handle(self, seek_to_end: bool = False):
        """
        Open the file and record its size
        Optionally seek to the end of the file
        """
        if not self.file_exists:
            raise IOError(ENOENT, "File not found", self.path)

        self.handle: TextIO = open(self.path, "r", encoding=self.encoding)
        self.size: int = self.current_handle_size

        if seek_to_end:
            self._seek_to_end()

    def _close_handle(self):
        self.handle.close()

    def _reopen_handle(self):
        """
        Explicitly close the file and then open it again.
        Don't seek to the end to avoid missing data
        """
        self._close_handle()
        self._open_handle()

    def _seek_to_end(self):
        """
        Seek to the end of the file
        """
        self.handle.seek(0, os.SEEK_END)

    def truncated_check(self):
        """
        Check the file was truncated
        If it was truncated then reopen it
        Otherwise update its size
        """
        if self.size > self.current_handle_size:
            self._reopen_handle()
        else:
            self.size: int = self.current_handle_size

    def __iter__(self):
        """
        Initialise and seek to the end of the file
        Yield lines forever
        """
        self._open_handle(seek_to_end=True)

        while True:
            try:
                self.truncated_check()
                line: str = self.handle.readline()

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
        if self.handle:
            self._close_handle()

    @property
    def current_handle_size(self) -> int:
        current_state: os.stat_result = os.stat(self.path)
        return current_state.st_size

    @property
    def file_exists(self) -> bool:
        if os.path.isfile(self.path):
            return True

        return False
