Configuration
=============

General settings
----------------

DBBACKUP_DATABASES
~~~~~~~~~~~~~~~~~~

List of key entries for ``settings.DATABASES`` which shall be used to
connect and create database backups.

Default: ``list(settings.DATABASES.keys())`` (keys of all entries listed)

DBBACKUP_BACKUP_DIRECTORY
~~~~~~~~~~~~~~~~~~~~~~~~~

Where to store backups. String pointing to django-dbbackup
location module to use when performing a backup.


Default: ``os.getcwd()`` (Current working directory)

DBBACKUP_CLEANUP_KEEP and DBBACKUP_CLEANUP_KEEP_MEDIA
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When issueing ``dbbackup`` and ``mediabackup``, old backup files are
looked for and removed.

Default: ``10`` (days)

DBBACKUP_MEDIA_PATH
~~~~~~~~~~~~~~~~~~~

Default: settings.MEDIA_ROOT

DBBACKUP_DATE_FORMAT
~~~~~~~~~~~~~~~~~~~~

Date format to use for naming files (only currently used in mediabackup).

Default: ``'%Y-%m-%d-%H%M%S'``

DBBACKUP_SERVER_NAME
~~~~~~~~~~~~~~~~~~~~

An optional server name to use when generating the backup filename. This is 
useful to help distinguish between development and production servers. 
By default this value is not used and the servername is not included in the 
generated filename.

Default: ``''``

DBBACKUP_FILENAME_TEMPLATE
~~~~~~~~~~~~~~~~~~~~~~~~~~

**NOT IMPLEMENTED YET**

The template to use when generating the backup filename. By default this is
'{databasename}-{servername}-{datetime}.{extension}'. This setting can
also be made a method which takes the following keyword arguments:

::

    def backup_filename(databasename, servername, timestamp, extension, wildcard):
        pass

This allows you to modify the entire format of the filename based on the
time of day, week, or month. For example, if you want to take advantage
of Amazon S3's automatic expiry feature, you need to prefix your backups
differently based on when you want them to expire.

SEND\_EMAIL
~~~~~~~~~~~

Controls whether or not django-dbbackup sends an error email when an uncaught
exception is received. This is ``True`` by default.

**DBBACKUP\_CLEANUP\_KEEP (optional)** - The number of backups to keep
when specifying the --clean flag. Defaults to keeping 10 + the first
backup of each month.

Database settings
=================

The following databases are supported by this application. You can
customize the commands used for backup and the resulting filenames with
the following settings.

NOTE: The {adminuser} settings below will first check for the variable
ADMINUSER specified on the database, then fall back to USER. This allows
you supplying a different user to perform the admin commands dropdb,
createdb as a different user from the one django uses to connect. If you
need more fine grain control you might consider fully customizing the
admin commands.

Postgresql
----------

DBBACKUP_POSTGRESQL_RESTORE_SINGLE_TRANSACTION
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When doing a restore with postgres, wrap everything in a single transaction
so that errors cause a rollback.

Default: ``True``

DBBACKUP_POSTGIS_SPACIAL_REF
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When on Postgis, using this setting currently disables
``CREATE EXTENSION POSTGIS;``. Ideally, it should run the good old Postgis
templates for version 1.5 of Postgis.


Encrypting your backups
=======================

Considering that you might be putting secured data on external servers and
perhaps untrusted servers where it gets forgotten over time, it's always a
good idea to encrypt backups.

Just remember to keep the encryption keys safe, too!


PGP
---

You can encrypt a backup with the ``--encrypt`` option. The backup is done
using gpg.

::

    python manage.py dbbackup --encrypt

...or when restoring from an encrypted backup:

::

    python manage.py dbrestore --decrypt


Requirements:

-  Install the python package python-gnupg:
   ``pip install python-gnupg``.
-  You need gpg key.
-  Set the setting 'DBBACKUP\_GPG\_RECIPIENT' to the name of the gpg
   key.

**DBBACKUP\_GPG\_ALWAYS\_TRUST (optional)** - The encryption of the
backup file fails if gpg does not trust the public encryption key. The
solution is to set the option 'trust-model' to 'always'. By default this
value is False. Set this to True to enable this option.

**DBBACKUP\_GPG\_RECIPIENT (optional)** - The name of the key that is
used for encryption. This setting is only used when making a backup with
the ``--encrypt`` or ``--decrypt`` option.
