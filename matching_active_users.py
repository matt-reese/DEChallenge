import configparser
from datetime import datetime
import mysql.connector
import os
import pandas
import requests

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read(
        os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.cfg'))

    runtime_start = datetime.now()

    cnx = mysql.connector.connect(user=config['env']['username']
                                  , password=config['env']['password']
                                  , host='REDACTED'
                                  , port='REDACTED'
                                  , database='data_engineer')
    cursor = cnx.cursor(buffered=True)

    response = requests.get('http://REDACTED.com/users')
    total_pages = int(response.json()['total_pages'])

    db_query_results = []
    merged_results = pandas.DataFrame()

    for i in range(1, total_pages):
        resp = requests.get(f'http://REDACTED.com/users?page={i}')
        user_info = resp.json()['users']
        api_data = pandas.DataFrame(user_info).astype({'last_active_date': 'datetime64'})
        api_data = api_data.rename(columns={'practice_location': 'location'})

        lastnames = api_data.lastname.unique().tolist()
        lastnames_string = ', '.join(['%s'] * len(lastnames))

        db_query = """
                   SELECT user.*, user_practice.location
                   FROM user
                   INNER JOIN user_practice ON user_practice.id = user.practice_id
                   WHERE lastname IN (%s)
                   """
        cursor.execute(db_query % lastnames_string, tuple(lastnames))

        for result in cursor:
            db_query_results.append(result)

        db_table = pandas.DataFrame(db_query_results, columns=['id', 'practice_id', 'firstname', 'lastname',
            'classification', 'specialty', 'platform_registered_on', 'last_active_date', 'location'])
        merged = pandas.merge(api_data, db_table, on=['firstname', 'lastname', 'location'], suffixes=('_api', '_db'))
        merged_results = merged_results.append(merged)

    cursor.close()
    cnx.close()

    new_merged_results = merged_results[['firstname', 'lastname', 'location', 'last_active_date_api', 'last_active_date_db',
        'user_type_classification', 'classification']]

    runtime = datetime.now() - runtime_start
    minutes = (runtime.total_seconds() % 3600) // 60
    seconds = runtime.total_seconds() % 60

    if os.path.exists('./output.txt'):
        os.remove('./output.txt')

    file = open('./output.txt', 'x')
    file.write(f'Elapsed time: {minutes} minutes, {seconds} seconds\n\n')
    file.write(f'Total matches: {new_merged_results.shape[0]}\n\n')
    file.write(f'Sample output:\n {new_merged_results[0:10].to_json(orient="records", date_format="iso")}\n\n')
    file.write('SQL DDL: \
                \n CREATE TABLE matching_active_users ( \
                \n     firstname varchar(50) \
                \n     , lastname varchar(50) \
                \n     , location varchar(50) \
                \n     , last_active_date_api date \
                \n     , last_active_date_db date \
                \n     , user_type_classification varchar(50) \
                \n     , classification varchar(50) \
                \n )')
    file.close()
