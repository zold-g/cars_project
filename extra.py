import sqlite3
import string
import pyodbc
import os
import re




global server
global database
global username
global password
global connection_string

server = 'DESKTOP-M86GGEG'
database = 'carsdatabase'
username = 'sa'
password = '123'

# connection string
connection_string = (
    "DRIVER={SQL Server};"
    "SERVER=DESKTOP-M86GGEG;"
    "DATABASE=carsdatabase;"
    "UID=sa;"
    "PWD=123;"
)

#conn = sqlite3.connect('carsdatabase.db')

#cursor = conn.cursor()

conn = pyodbc.connect(connection_string)
cursor = conn.cursor()
# select query
option1 = 'تويوتا'
option2 = 'مارسدس'

#current_username = 'سعدة'
#current_password = '123'
#account_type = 'admin'
#status = 'enabled'
#create_table_query = '''
#                            CREATE TABLE dbo.accounts (
#                            current_username NVARCHAR(255),current_password NVARCHAR(255),account_type NVARCHAR(255),status NVARCHAR(255)
#                                                        )
#                                                        '''
#insert_query = '''
#                        INSERT INTO accounts (
#                        current_username,current_password,account_type,status
#                                                    ) 
#                                    VALUES (?,?,?,?)
#                                                        '''
#cursor.execute(create_table_query)
#cursor.execute(insert_query, (
#                        current_username,current_password,account_type,status
#                                                    ))








#update query

#update_query = '''
#UPDATE newcar
#SET a = ?, b = ?, c = ?, d = ?
#'''
#cursor.execute(update_query)


# create table query

#create_table_query = '''
#CREATE TABLE IF NOT EXISTS newcar (
#    a TEXT,
#    b TEXT,
#    c TEXT,
#    d TEXT
#)
#'''
#cursor.execute(create_table_query)




#insert querty

#insert_query = '''
#INSERT INTO newcar (a, b, c, d) 
#VALUES (?,?,?,?)
#'''
#cursor.execute(insert_query, (a,b,c,d))



#delete query

#delete_query = 'DELETE FROM accounts WHERE current_username = ?'
#cursor.execute(delete_query, (a,))



#drop table
#cursor.execute('DROP TABLE handover')


#display the database
#cursor.execute('SELECT * from newcar')
#select_query = 'SELECT * FROM malfunctionsoptions'
#rows = cursor.fetchall()
#for row in rows:
#    print(row)


#ceate table query

#car1 = 'admin'
#car2 = 'user'
#car3 = 'viewer'


#create_table_query = '''
#CREATE TABLE IF NOT EXISTS accountty (
#    account TEXT
#)
#'''




#conn.commit()
#conn.close()

chassis_number = '1234567'
#test erea
select_query = 'SELECT * FROM newcar WHERE chassis_number = ?'
cursor.execute(select_query, (chassis_number,))
rows = cursor.fetchall()
row = rows[0]
conn.commit()
print(row[2])
split_result = re.match(r'(\D+)(\d+)', row[2])


character_part = split_result.group(1)  # This will be "د"
number_part = split_result.group(2)      # This will be "11"

print(character_part)  # Output: د
print(number_part)    



conn.commit()
conn.close()



