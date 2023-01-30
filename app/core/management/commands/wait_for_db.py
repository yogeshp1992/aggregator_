"""
Django command to wait for database to be available
"""

import time
from MySQLdb import Error
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for database"""

    def handle(self, *args, **kwargs):
        """ Entrypoint for command """

        self.stdout.write("waiting for database....")
        db_up = False
        while db_up is False:
            try:
                self.check(databases=["default"])
                db_up = True
            except (Error, OperationalError):
                self.stdout.write(
                    "Database unavailable, waiting for 1 second..."
                )
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS("Database available!"))
