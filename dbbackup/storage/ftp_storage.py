"""
FTP Storage object.
"""
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import pickle
import os
import tempfile
from shutil import copyfileobj
from .base import BaseStorage, StorageError
from django.conf import settings
from ftplib import FTP

MAX_SPOOLED_SIZE = 10 * 1024 * 1024
FILE_SIZE_LIMIT = 145 * 1024 * 1024

################################
#  FTP Storage Object
################################


class Storage(BaseStorage):
    """ FTP Storage. """
    name = 'FTP'
    FTP_HOST = getattr(settings, 'DBBACKUP_FTP_HOST', None)
    FTP_USER = getattr(settings, 'DBBACKUP_FTP_USER', None)
    FTP_PASSWORD = getattr(settings, 'DBBACKUP_FTP_PASSWORD', None)
    FTP_PATH = getattr(settings, 'DBBACKUP_FTP_PATH', ".")
    FTP_PATH = '/%s/' % FTP_PATH.strip('/')
    FTP_PASSIVE_MODE = getattr(settings, 'DBBACKUP_FTP_PASSIVE_MODE', False)

    def __init__(self, server_name=None):
        self._check_settings()
        self.ftp = FTP(self.FTP_HOST, self.FTP_USER, self.FTP_PASSWORD)
        self.ftp.set_pasv(self.FTP_PASSIVE_MODE)
        BaseStorage.__init__(self)

    def _check_settings(self):
        """ Check we have all the required settings defined. """
        if not self.FTP_HOST:
            raise StorageError('%s storage requires DBBACKUP_FTP_HOST to be defined in settings.' % self.name)

    ###################################
    #  DBBackup Storage Methods
    ###################################

    def backup_dir(self):
        return self.FTP_PATH

    def delete_file(self, filepath):
        """ Delete the specified filepath. """
        self.ftp.delete(filepath)

    def list_directory(self, raw=False):
        """ List all stored backups for the specified. """
        return sorted(self.ftp.nlst(self.FTP_PATH))

    def write_file(self, filehandle, filename):
        """ Write the specified file. """
        filehandle.seek(0)
        backuppath = os.path.join(self.FTP_PATH, filename)
        self.ftp.storbinary('STOR ' + backuppath, filehandle)

    def read_file(self, filepath):
        """ Read the specified file and return it's handle. """
        return self.ftp.retrbinary('RETR ' + filepath)
