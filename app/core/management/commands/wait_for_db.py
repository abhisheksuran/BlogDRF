""" Management command for Django to wait for DB to get up and running first"""

from django.core.management.base import BaseCommand
from psycopg2 import OperationalError as Psycopg2Error
import time
from django.db.utils import OperationalError


class Command(BaseCommand):
    """Django command for wait for db"""

    def handle(self, *args, **kwargs):
        """Command handler"""

        self.stdout.write("Waiting for the database...")
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2Error, OperationalError):
                self.stdout.write("Database Not available, waiting for 1 sec...")
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database Available!'))