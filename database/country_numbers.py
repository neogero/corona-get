import sqlite3
from sqlite3 import Error

def insertOne(conn, country_dict):
    """
    Create a new country_number registry into the country_numbers table
    :param conn:
    :param country_numbers:
    #:return: c id
    """
    cur = conn.cursor() 
    sql = ''' INSERT INTO country_numbers(get_datetime, country_name, cases, deaths, deaths_rate, recovery, recovery_rate, original_last_modification) VALUES(?,?,?,?,?,?,?,?) '''
    
    cur.execute(sql, [country_dict['get_datetime'], country_dict['country_name'], country_dict['cases'], country_dict['deaths'], country_dict['deaths_rate'], country_dict['recovery'], country_dict['recovery_rate'], country_dict['original_last_modification']])
    conn.commit()
    #print(cur.lastrowid)

    return cur.lastrowid