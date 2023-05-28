import psycopg2
from django.core.management.base import BaseCommand
from geopy.distance import geodesic
from decouple import config
import csv

class Command(BaseCommand):
    '''Команда для загрузки локаций из файла uszips.csv в базу данных'''
    help = 'Загрузка локация из uszips.csv в бд'

    def handle(self, *args, **options):
        with open('uszips.csv', 'r') as file:
            csv_data = csv.reader(file)
            next(csv_data)

            conn = psycopg2.connect(database=config('DB_NAME'), 
                                    user=config('DB_USER'), 
                                    password=config('DB_PASSWORD'), 
                                    host=config('DB_HOST'), 
                                    port=config('DB_PORT'))
            cur = conn.cursor()

            for row in csv_data:
                zip = row[0]
                lat = row[1]
                lng = row[2]
                city = row[3]
                state_name = row[5]

                cur.execute("INSERT INTO cargo_location (zip, lat, lng, city, state_name) VALUES (%s, %s, %s, %s, %s)", 
                            (zip, lat, lng, city, state_name))

            conn.commit()
            cur.close()
            conn.close()
