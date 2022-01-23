import sqlite3
from sqlite3 import Error

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'rename Comment model'

    def handle(self, *args, **options):
        def sql_connection():
            try:
                return sqlite3.connect('db.sqlite3')
            except Error:
                print(Error)

        def sql_table(con):
            cursor = con.cursor()
            cursor.execute(
                'ALTER TABLE "reviews_comments" RENAME TO "reviews_comment"'
            )
            con.commit()

        con = sql_connection()
        sql_table(con)
