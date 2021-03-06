import sqlite3
from datetime import date

WEATHER_TABLE = "CREATE TABLE IF NOT EXISTS weather (city_name TEXT NOT NULL, in_day DATE NOT NULL, weather TEXT, temp FLOAT, PRIMARY KEY (city_name, in_day));"

INSERT_WEATHER = "INSERT INTO weather (city_name, in_day, weather, temp) VALUES (?,?,?,?);"
                    
UPDATE_WEATHER= '''UPDATE weather 
                    SET weather = ?,
                        temp = ?,
                        in_day = ?
                    WHERE city_name = ?'''

UPDATE_WEATHER_IN_TIME = '''UPDATE weather 
                            SET weather = ?,
                                temp = ?
                            WHERE city_name = ? AND in_day = ?'''
                            
SHOW_WEATHER = '''SELECT * FROM weather
                WHERE in_day = ?
                '''
                            
SHOW_WEATHER_IN_DAY = '''SELECT * FROM weather
                        WHERE city_name = ? AND in_day = ?
                        '''
                            
SHOW_WEATHER_IN_NEXT_7_DAYS = '''SELECT * FROM weather
                                WHERE city_name = ? 
                                AND (in_day >= (SELECT DATE('now')) 
                                    AND in_day < (SELECT DATE('now', '+7 day')))
                                '''
                                
SHOW_CITIES = '''SELECT DISTINCT city_name
                FROM weather
            '''
            
SHOW_DATES = '''SELECT DISTINCT in_day
                FROM weather
                WHERE city_name = ?
            '''
            
SHOW_ALL = '''SELECT *
                FROM weather
            '''
            
SHOW_CITIES_IN_DATE = '''SELECT DISTINCT city_name
                        FROM weather 
                        WHERE in_day = ?
                        '''
SHOW_NEXT_7_DAYS_FOR_CITY = '''SELECT in_day
                                FROM weather
                                WHERE city_name = ? 
                                AND (in_day >= (SELECT DATE('now')) 
                                    AND in_day < (SELECT DATE('now', '+7 day')))
                            '''

def connect():
    return sqlite3.connect('weather.db')

def create_table_weather(connection):
    with connection:
        connection.execute(WEATHER_TABLE)

def insert_weather(connection, city_name, in_day, weather, temp):
    with connection:
        connection.execute(INSERT_WEATHER, (city_name, in_day, weather, temp))
        
def update_weather(connection, weather, temp, in_day, city_name):
    with connection:
        connection.execute(UPDATE_WEATHER, (weather, temp, in_day, city_name))
                
def update_weather_in_time(connection, weather, temp, city_name, in_day):
    with connection:
        connection.execute(UPDATE_WEATHER_IN_TIME, (weather, temp, city_name, in_day))
        
def show_weather(connection, in_day):
    with connection:
        return connection.execute(SHOW_WEATHER, (in_day, )).fetchall()
    
def show_weather_in_day(connection, city_name, in_day):
    with connection:
        return connection.execute(SHOW_WEATHER_IN_DAY, (city_name, in_day)).fetchall()

def show_weather_in_next_7_days(connection, city_name):
    with connection:
        return connection.execute(SHOW_WEATHER_IN_NEXT_7_DAYS, (city_name, )).fetchall()
    
def show_cities(connection):
    with connection:
        return connection.execute(SHOW_CITIES).fetchall()
    
def show_cities_in_date(connection, in_day):
    with connection:
        return connection.execute(SHOW_CITIES_IN_DATE, (in_day, )).fetchall()
    
def show_dates(connection, city_name):
    with connection:
        return connection.execute(SHOW_DATES, (city_name, )).fetchall()
    
def show_all(connection):
    with connection:
        return connection.execute(SHOW_ALL).fetchall()
    
def show_next_7_dates_for_city(connection, city_name):
    with connection:
        return connection.execute(SHOW_NEXT_7_DAYS_FOR_CITY, (city_name, )).fetchall()
    
    
# connection = connect()

# with connection:
#     connection.execute("DROP TABLE weather")
# create_table_weather(connection)

# insert_weather(connection, 'H??? Ch?? Minh', '2021-07-25', 'c?? n???ng', '37')
# insert_weather(connection, 'H??? Ch?? Minh', '2021-06-15', 'nhi???u m??y', '36')
# insert_weather(connection, 'H??? Ch?? Minh', '2021-06-16', 'm??a r??o', '32')
# insert_weather(connection, 'H??? Ch?? Minh', '2021-06-17', 'n???ng nh???', '33')
# insert_weather(connection, 'H??? Ch?? Minh', '2021-06-18', 'tr???i trong', '37')
# insert_weather(connection, 'H??? Ch?? Minh', '2021-06-19', 'c?? gi??', '35')
# insert_weather(connection, 'H??? Ch?? Minh', '2021-06-20', 'm??a r???i r??c', '35')
# insert_weather(connection, 'H??? Ch?? Minh', '2021-06-21', 'c?? m??y', '35')
# insert_weather(connection, 'H??? Ch?? Minh', '2021-06-22', 'c?? n???ng', '36')
# insert_weather(connection, 'H??? Ch?? Minh', '2021-06-23', 'n???ng nh???', '32')
# insert_weather(connection, 'H??? Ch?? Minh', '2021-06-24', 'nhi???u m??y', '33')
# insert_weather(connection, 'H??? Ch?? Minh', '2021-06-25', 'c?? n???ng', '35')
# insert_weather(connection, 'H??? Ch?? Minh', '2021-06-26', 'm??a r??o', '35')
# insert_weather(connection, 'H??? Ch?? Minh', '2021-06-27', 'n???ng nh???', '35')
# insert_weather(connection, 'H??? Ch?? Minh', '2021-06-28', 'nhi???u m??y', '33')
# insert_weather(connection, 'H??? Ch?? Minh', '2021-06-29', 'c?? n???ng', '32')
# insert_weather(connection, 'H??? Ch?? Minh', '2021-06-30', 'm??a r??o', '35')
# insert_weather(connection, 'H??? Ch?? Minh', '2021-07-01', 'c?? n???ng', '35')
# insert_weather(connection, 'H??? Ch?? Minh', '2021-07-02', 'n???ng nh???', '35')
# insert_weather(connection, 'H??? Ch?? Minh', '2021-07-03', 'c?? n???ng', '36')
# insert_weather(connection, 'H??? Ch?? Minh', '2021-07-04', 'tr???i trong', '32')
# insert_weather(connection, 'H??? Ch?? Minh', '2021-07-05', 'nhi???u m??y', '33')
# insert_weather(connection, 'H??? Ch?? Minh', '2021-07-06', 'n???ng nh???', '35')
# insert_weather(connection, 'H??? Ch?? Minh', '2021-07-07', 'c?? n???ng', '35')
# insert_weather(connection, 'H??? Ch?? Minh', '2021-07-08', 'n???ng nh???', '35')
# insert_weather(connection, 'H??? Ch?? Minh', '2021-07-09', 'nhi???u m??y', '33')
# insert_weather(connection, 'H??? Ch?? Minh', '2021-07-10', 'm??a r??o', '32')

# insert_weather(connection, 'H?? N???i', '2021-06-14', 'n???ng nh???', '37')
# insert_weather(connection, 'H?? N???i', '2021-06-15', 'm??a r??o', '36')
# insert_weather(connection, 'H?? N???i', '2021-06-16', 'nhi???u m??y', '32')
# insert_weather(connection, 'H?? N???i', '2021-06-17', 'n???ng nh???', '33')
# insert_weather(connection, 'H?? N???i', '2021-06-18', 'm??a r??o', '37')
# insert_weather(connection, 'H?? N???i', '2021-06-19', 'nhi???u m??y', '35')
# insert_weather(connection, 'H?? N???i', '2021-06-20', 'c?? n???ng', '35')
# insert_weather(connection, 'H?? N???i', '2021-06-21', 'm??a r??o', '35')
# insert_weather(connection, 'H?? N???i', '2021-06-22', 'c?? n???ng', '36')
# insert_weather(connection, 'H?? N???i', '2021-06-23', 'tr???i trong', '32')
# insert_weather(connection, 'H?? N???i', '2021-06-24', 'n???ng nh???', '33')
# insert_weather(connection, 'H?? N???i', '2021-06-25', 'm??a r??o', '35')
# insert_weather(connection, 'H?? N???i', '2021-06-26', 'tr???i trong', '35')
# insert_weather(connection, 'H?? N???i', '2021-06-27', 'c?? n???ng', '35')
# insert_weather(connection, 'H?? N???i', '2021-06-28', 'n???ng nh???', '33')
# insert_weather(connection, 'H?? N???i', '2021-06-29', 'tr???i trong', '32')
# insert_weather(connection, 'H?? N???i', '2021-06-30', 'm??a r??o', '37')
# insert_weather(connection, 'H?? N???i', '2021-07-01', 'nhi???u m??y', '35')
# insert_weather(connection, 'H?? N???i', '2021-07-02', 'c?? n???ng', '37')
# insert_weather(connection, 'H?? N???i', '2021-07-03', 'm??a r??o', '36')
# insert_weather(connection, 'H?? N???i', '2021-07-04', 'nhi???u m??y', '32')
# insert_weather(connection, 'H?? N???i', '2021-07-05', 'c?? n???ng', '33')
# insert_weather(connection, 'H?? N???i', '2021-07-06', 'tr???i trong', '37')
# insert_weather(connection, 'H?? N???i', '2021-07-07', 'm??a r??o', '35')
# insert_weather(connection, 'H?? N???i', '2021-07-08', 'nhi???u m??y', '35')
# insert_weather(connection, 'H?? N???i', '2021-07-09', 'n???ng nh???', '33')

# insert_weather(connection, 'H???i Ph??ng', '2021-06-14', 'nhi???u m??y', '37')
# insert_weather(connection, 'H???i Ph??ng', '2021-06-15', 'n???ng nh???', '36')
# insert_weather(connection, 'H???i Ph??ng', '2021-06-16', 'nhi???u m??y', '32')
# insert_weather(connection, 'H???i Ph??ng', '2021-06-17', 'n???ng nh???', '33')
# insert_weather(connection, 'H???i Ph??ng', '2021-06-18', 'm??a r??o', '37')
# insert_weather(connection, 'H???i Ph??ng', '2021-06-19', 'n???ng nh???', '35')
# insert_weather(connection, 'H???i Ph??ng', '2021-06-20', 'nhi???u m??y', '35')
# insert_weather(connection, 'H???i Ph??ng', '2021-06-21', 'm??a r??o', '35')
# insert_weather(connection, 'H???i Ph??ng', '2021-06-22', 'n???ng nh???', '36')
# insert_weather(connection, 'H???i Ph??ng', '2021-06-23', 'm??a r??o', '32')
# insert_weather(connection, 'H???i Ph??ng', '2021-06-24', 'tr???i trong', '33')
# insert_weather(connection, 'H???i Ph??ng', '2021-06-25', 'nhi???u m??y', '35')
# insert_weather(connection, 'H???i Ph??ng', '2021-06-26', 'm??a r??o', '35')
# insert_weather(connection, 'H???i Ph??ng', '2021-06-27', 'c?? n???ng', '35')
# insert_weather(connection, 'H???i Ph??ng', '2021-06-28', 'tr???i trong', '33')
# insert_weather(connection, 'H???i Ph??ng', '2021-06-29', 'c?? n???ng', '32')
# insert_weather(connection, 'H???i Ph??ng', '2021-06-30', 'n???ng nh???', '35')
# insert_weather(connection, 'H???i Ph??ng', '2021-07-01', 'm??a r??o', '35')
# insert_weather(connection, 'H???i Ph??ng', '2021-07-02', 'n???ng nh???', '35')
# insert_weather(connection, 'H???i Ph??ng', '2021-07-03', 'nhi???u m??y', '36')
# insert_weather(connection, 'H???i Ph??ng', '2021-07-04', 'c?? n???ng', '32')
# insert_weather(connection, 'H???i Ph??ng', '2021-07-05', 'tr???i trong', '33')
# insert_weather(connection, 'H???i Ph??ng', '2021-07-06', 'n???ng nh???', '35')
# insert_weather(connection, 'H???i Ph??ng', '2021-07-07', 'c?? n???ng', '35')
# insert_weather(connection, 'H???i Ph??ng', '2021-07-08', 'nhi???u m??y', '35')
# insert_weather(connection, 'H???i Ph??ng', '2021-07-09', 'tr???i trong', '33')
# insert_weather(connection, 'H???i Ph??ng', '2021-07-10', 'c?? n???ng', '32')

# insert_weather(connection, '???? N???ng', '2021-06-14', 'c?? n???ng', '37')
# insert_weather(connection, '???? N???ng', '2021-06-15', 'n???ng nh???', '36')
# insert_weather(connection, '???? N???ng', '2021-06-16', 'tr???i trong', '32')
# insert_weather(connection, '???? N???ng', '2021-06-17', 'm??a r??o', '33')
# insert_weather(connection, '???? N???ng', '2021-06-18', 'n???ng nh???', '37')
# insert_weather(connection, '???? N???ng', '2021-06-19', 'tr???i trong', '35')
# insert_weather(connection, '???? N???ng', '2021-06-20', 'm??a r??o', '35')
# insert_weather(connection, '???? N???ng', '2021-06-21', 'n???ng nh???', '35')
# insert_weather(connection, '???? N???ng', '2021-06-22', 'c?? n???ng', '36')
# insert_weather(connection, '???? N???ng', '2021-06-23', 'tr???i trong', '32')
# insert_weather(connection, '???? N???ng', '2021-06-24', 'c?? n???ng', '33')
# insert_weather(connection, '???? N???ng', '2021-06-25', 'm??a r??o', '35')
# insert_weather(connection, '???? N???ng', '2021-06-26', 'n???ng nh???', '35')
# insert_weather(connection, '???? N???ng', '2021-06-27', 'tr???i trong', '35')
# insert_weather(connection, '???? N???ng', '2021-06-28', 'm??a r??o', '33')
# insert_weather(connection, '???? N???ng', '2021-06-29', 'nhi???u m??y', '32')
# insert_weather(connection, '???? N???ng', '2021-06-30', 'c?? n???ng', '35')
# insert_weather(connection, '???? N???ng', '2021-07-01', 'm??a r??o', '35')
# insert_weather(connection, '???? N???ng', '2021-07-02', 'tr???i trong', '35')
# insert_weather(connection, '???? N???ng', '2021-07-03', 'n???ng nh???', '36')
# insert_weather(connection, '???? N???ng', '2021-07-04', 'c?? n???ng', '32')
# insert_weather(connection, '???? N???ng', '2021-07-05', 'c?? n???ng', '33')
# insert_weather(connection, '???? N???ng', '2021-07-06', 'm??a r??o', '35')
# insert_weather(connection, '???? N???ng', '2021-07-07', 'tr???i trong', '35')
# insert_weather(connection, '???? N???ng', '2021-07-08', 'n???ng nh???', '35')
# insert_weather(connection, '???? N???ng', '2021-07-09', 'm??a r??o', '33')
# insert_weather(connection, '???? N???ng', '2021-07-10', 'c?? n???ng', '32')