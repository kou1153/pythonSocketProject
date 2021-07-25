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

# insert_weather(connection, 'Hồ Chí Minh', '2021-07-25', 'có nắng', '37')
# insert_weather(connection, 'Hồ Chí Minh', '2021-06-15', 'nhiều mây', '36')
# insert_weather(connection, 'Hồ Chí Minh', '2021-06-16', 'mưa rào', '32')
# insert_weather(connection, 'Hồ Chí Minh', '2021-06-17', 'nắng nhẹ', '33')
# insert_weather(connection, 'Hồ Chí Minh', '2021-06-18', 'trời trong', '37')
# insert_weather(connection, 'Hồ Chí Minh', '2021-06-19', 'có gió', '35')
# insert_weather(connection, 'Hồ Chí Minh', '2021-06-20', 'mưa rải rác', '35')
# insert_weather(connection, 'Hồ Chí Minh', '2021-06-21', 'có mây', '35')
# insert_weather(connection, 'Hồ Chí Minh', '2021-06-22', 'có nắng', '36')
# insert_weather(connection, 'Hồ Chí Minh', '2021-06-23', 'nắng nhẹ', '32')
# insert_weather(connection, 'Hồ Chí Minh', '2021-06-24', 'nhiều mây', '33')
# insert_weather(connection, 'Hồ Chí Minh', '2021-06-25', 'có nắng', '35')
# insert_weather(connection, 'Hồ Chí Minh', '2021-06-26', 'mưa rào', '35')
# insert_weather(connection, 'Hồ Chí Minh', '2021-06-27', 'nắng nhẹ', '35')
# insert_weather(connection, 'Hồ Chí Minh', '2021-06-28', 'nhiều mây', '33')
# insert_weather(connection, 'Hồ Chí Minh', '2021-06-29', 'có nắng', '32')
# insert_weather(connection, 'Hồ Chí Minh', '2021-06-30', 'mưa rào', '35')
# insert_weather(connection, 'Hồ Chí Minh', '2021-07-01', 'có nắng', '35')
# insert_weather(connection, 'Hồ Chí Minh', '2021-07-02', 'nắng nhẹ', '35')
# insert_weather(connection, 'Hồ Chí Minh', '2021-07-03', 'có nắng', '36')
# insert_weather(connection, 'Hồ Chí Minh', '2021-07-04', 'trời trong', '32')
# insert_weather(connection, 'Hồ Chí Minh', '2021-07-05', 'nhiều mây', '33')
# insert_weather(connection, 'Hồ Chí Minh', '2021-07-06', 'nắng nhẹ', '35')
# insert_weather(connection, 'Hồ Chí Minh', '2021-07-07', 'có nắng', '35')
# insert_weather(connection, 'Hồ Chí Minh', '2021-07-08', 'nắng nhẹ', '35')
# insert_weather(connection, 'Hồ Chí Minh', '2021-07-09', 'nhiều mây', '33')
# insert_weather(connection, 'Hồ Chí Minh', '2021-07-10', 'mưa rào', '32')

# insert_weather(connection, 'Hà Nội', '2021-06-14', 'nắng nhẹ', '37')
# insert_weather(connection, 'Hà Nội', '2021-06-15', 'mưa rào', '36')
# insert_weather(connection, 'Hà Nội', '2021-06-16', 'nhiều mây', '32')
# insert_weather(connection, 'Hà Nội', '2021-06-17', 'nắng nhẹ', '33')
# insert_weather(connection, 'Hà Nội', '2021-06-18', 'mưa rào', '37')
# insert_weather(connection, 'Hà Nội', '2021-06-19', 'nhiều mây', '35')
# insert_weather(connection, 'Hà Nội', '2021-06-20', 'có nắng', '35')
# insert_weather(connection, 'Hà Nội', '2021-06-21', 'mưa rào', '35')
# insert_weather(connection, 'Hà Nội', '2021-06-22', 'có nắng', '36')
# insert_weather(connection, 'Hà Nội', '2021-06-23', 'trời trong', '32')
# insert_weather(connection, 'Hà Nội', '2021-06-24', 'nắng nhẹ', '33')
# insert_weather(connection, 'Hà Nội', '2021-06-25', 'mưa rào', '35')
# insert_weather(connection, 'Hà Nội', '2021-06-26', 'trời trong', '35')
# insert_weather(connection, 'Hà Nội', '2021-06-27', 'có nắng', '35')
# insert_weather(connection, 'Hà Nội', '2021-06-28', 'nắng nhẹ', '33')
# insert_weather(connection, 'Hà Nội', '2021-06-29', 'trời trong', '32')
# insert_weather(connection, 'Hà Nội', '2021-06-30', 'mưa rào', '37')
# insert_weather(connection, 'Hà Nội', '2021-07-01', 'nhiều mây', '35')
# insert_weather(connection, 'Hà Nội', '2021-07-02', 'có nắng', '37')
# insert_weather(connection, 'Hà Nội', '2021-07-03', 'mưa rào', '36')
# insert_weather(connection, 'Hà Nội', '2021-07-04', 'nhiều mây', '32')
# insert_weather(connection, 'Hà Nội', '2021-07-05', 'có nắng', '33')
# insert_weather(connection, 'Hà Nội', '2021-07-06', 'trời trong', '37')
# insert_weather(connection, 'Hà Nội', '2021-07-07', 'mưa rào', '35')
# insert_weather(connection, 'Hà Nội', '2021-07-08', 'nhiều mây', '35')
# insert_weather(connection, 'Hà Nội', '2021-07-09', 'nắng nhẹ', '33')

# insert_weather(connection, 'Hải Phòng', '2021-06-14', 'nhiều mây', '37')
# insert_weather(connection, 'Hải Phòng', '2021-06-15', 'nắng nhẹ', '36')
# insert_weather(connection, 'Hải Phòng', '2021-06-16', 'nhiều mây', '32')
# insert_weather(connection, 'Hải Phòng', '2021-06-17', 'nắng nhẹ', '33')
# insert_weather(connection, 'Hải Phòng', '2021-06-18', 'mưa rào', '37')
# insert_weather(connection, 'Hải Phòng', '2021-06-19', 'nắng nhẹ', '35')
# insert_weather(connection, 'Hải Phòng', '2021-06-20', 'nhiều mây', '35')
# insert_weather(connection, 'Hải Phòng', '2021-06-21', 'mưa rào', '35')
# insert_weather(connection, 'Hải Phòng', '2021-06-22', 'nắng nhẹ', '36')
# insert_weather(connection, 'Hải Phòng', '2021-06-23', 'mưa rào', '32')
# insert_weather(connection, 'Hải Phòng', '2021-06-24', 'trời trong', '33')
# insert_weather(connection, 'Hải Phòng', '2021-06-25', 'nhiều mây', '35')
# insert_weather(connection, 'Hải Phòng', '2021-06-26', 'mưa rào', '35')
# insert_weather(connection, 'Hải Phòng', '2021-06-27', 'có nắng', '35')
# insert_weather(connection, 'Hải Phòng', '2021-06-28', 'trời trong', '33')
# insert_weather(connection, 'Hải Phòng', '2021-06-29', 'có nắng', '32')
# insert_weather(connection, 'Hải Phòng', '2021-06-30', 'nắng nhẹ', '35')
# insert_weather(connection, 'Hải Phòng', '2021-07-01', 'mưa rào', '35')
# insert_weather(connection, 'Hải Phòng', '2021-07-02', 'nắng nhẹ', '35')
# insert_weather(connection, 'Hải Phòng', '2021-07-03', 'nhiều mây', '36')
# insert_weather(connection, 'Hải Phòng', '2021-07-04', 'có nắng', '32')
# insert_weather(connection, 'Hải Phòng', '2021-07-05', 'trời trong', '33')
# insert_weather(connection, 'Hải Phòng', '2021-07-06', 'nắng nhẹ', '35')
# insert_weather(connection, 'Hải Phòng', '2021-07-07', 'có nắng', '35')
# insert_weather(connection, 'Hải Phòng', '2021-07-08', 'nhiều mây', '35')
# insert_weather(connection, 'Hải Phòng', '2021-07-09', 'trời trong', '33')
# insert_weather(connection, 'Hải Phòng', '2021-07-10', 'có nắng', '32')

# insert_weather(connection, 'Đà Nẵng', '2021-06-14', 'có nắng', '37')
# insert_weather(connection, 'Đà Nẵng', '2021-06-15', 'nắng nhẹ', '36')
# insert_weather(connection, 'Đà Nẵng', '2021-06-16', 'trời trong', '32')
# insert_weather(connection, 'Đà Nẵng', '2021-06-17', 'mưa rào', '33')
# insert_weather(connection, 'Đà Nẵng', '2021-06-18', 'nắng nhẹ', '37')
# insert_weather(connection, 'Đà Nẵng', '2021-06-19', 'trời trong', '35')
# insert_weather(connection, 'Đà Nẵng', '2021-06-20', 'mưa rào', '35')
# insert_weather(connection, 'Đà Nẵng', '2021-06-21', 'nắng nhẹ', '35')
# insert_weather(connection, 'Đà Nẵng', '2021-06-22', 'có nắng', '36')
# insert_weather(connection, 'Đà Nẵng', '2021-06-23', 'trời trong', '32')
# insert_weather(connection, 'Đà Nẵng', '2021-06-24', 'có nắng', '33')
# insert_weather(connection, 'Đà Nẵng', '2021-06-25', 'mưa rào', '35')
# insert_weather(connection, 'Đà Nẵng', '2021-06-26', 'nắng nhẹ', '35')
# insert_weather(connection, 'Đà Nẵng', '2021-06-27', 'trời trong', '35')
# insert_weather(connection, 'Đà Nẵng', '2021-06-28', 'mưa rào', '33')
# insert_weather(connection, 'Đà Nẵng', '2021-06-29', 'nhiều mây', '32')
# insert_weather(connection, 'Đà Nẵng', '2021-06-30', 'có nắng', '35')
# insert_weather(connection, 'Đà Nẵng', '2021-07-01', 'mưa rào', '35')
# insert_weather(connection, 'Đà Nẵng', '2021-07-02', 'trời trong', '35')
# insert_weather(connection, 'Đà Nẵng', '2021-07-03', 'nắng nhẹ', '36')
# insert_weather(connection, 'Đà Nẵng', '2021-07-04', 'có nắng', '32')
# insert_weather(connection, 'Đà Nẵng', '2021-07-05', 'có nắng', '33')
# insert_weather(connection, 'Đà Nẵng', '2021-07-06', 'mưa rào', '35')
# insert_weather(connection, 'Đà Nẵng', '2021-07-07', 'trời trong', '35')
# insert_weather(connection, 'Đà Nẵng', '2021-07-08', 'nắng nhẹ', '35')
# insert_weather(connection, 'Đà Nẵng', '2021-07-09', 'mưa rào', '33')
# insert_weather(connection, 'Đà Nẵng', '2021-07-10', 'có nắng', '32')