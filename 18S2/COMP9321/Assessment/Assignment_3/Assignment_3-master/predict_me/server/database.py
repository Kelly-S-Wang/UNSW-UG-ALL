import psycopg2, re

class Database:

    def __init__(self, database_name, csv_path):
        self.connection = psycopg2.connect("dbname='{}' user='postgres' password='root'".format(database_name))
        self.connection.autocommit = False
        self.path = csv_path
        print('Connected to PSQL database ({}) successfully.'.format(database_name))

    def save_to_csv(self):
        with self.connection.cursor() as cursor:
            cursor.execute('''COPY users(username, email, password) TO \'{}/users.csv\' DELIMITER \',\' CSV HEADER'''.format(self.path))
        print('Successfully save to csv.')
        self.connection.commit()