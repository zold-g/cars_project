import streamlit as st
import pandas as pd
import datetime
from cars import add_vehicle # type: ignore
import pyodbc
import os
from cars import * # type: ignore
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
import pandas as pd
from bs4 import BeautifulSoup
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.lib.colors import HexColor
from io import BytesIO
from reportlab.lib import colors
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet








global server
global database
global username
global password
global connection_string
import re
authorization = None
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

global conn
global cursor
conn = pyodbc.connect(connection_string,autocommit=True)
cursor = conn.cursor()

# login_page function
def check_credentials(username, password):
    global correct_username
    global correct_password
    global authorization
    global status

    current_username = 'admin'
    current_password = '123'
    account_type = 'admin'
    status = 'enabled'
    session = 'active'

    try:
     create_table_query = '''
                              CREATE TABLE dbo.accounts (
                              current_username NVARCHAR(255),current_password NVARCHAR(255),account_type NVARCHAR(255),status NVARCHAR(255),
                              session NVARCHAR(255)
                                                            )
                                                            '''
     insert_query = '''
                         INSERT INTO accounts (
                         current_username,current_password,account_type,status,session
                                                       ) 
                                        VALUES (?,?,?,?,?)
                                                            '''
     cursor.execute(create_table_query)
     cursor.execute(insert_query, (
                         current_username,current_password,account_type,status,session
                                                       ))
     conn.commit()
     select_query = 'SELECT current_username, current_password, account_type, status,session FROM accounts WHERE current_username = ?'
     cursor.execute(select_query ,(username,))
     row = cursor.fetchone()
    except:
          select_query = 'SELECT current_username, current_password, account_type, status,session FROM accounts WHERE current_username = ?'
          cursor.execute(select_query ,(username,))
          row = cursor.fetchone()


    if row is None:
        st.error('يوجد خطأ في اسم المستخدم')  # Username error
        return False
    
    # Extract the data from the row
    correct_username, correct_password, authorization, status, session = row
    
    if password != correct_password:
        st.error('يوجد خطأ في كلمة المرور')  # Password error
        return False
    
    if status != 'enabled':
        st.error('الحساب معطل حالياً')  # Account disabled
        return False
    
    
    #log_it_already(username)
    return True


#create the log table
def create_log():
     try:
          create_table_query = '''
                         CREATE TABLE dbo.userslog (
                         userlo NVARCHAR(255),timelo DATETIME,actionlo NVARCHAR(255)
                                                  )
                                                       '''
          cursor.execute(create_table_query)
          conn.commit()
     except:
          pass


# record user log
def userlog(action):
     current_time = datetime.datetime.now()
     insert_query = '''
          INSERT INTO dbo.userslog (userlo, timelo, actionlo)
          VALUES (?, ?, ?)
               '''

     cursor.execute(insert_query, (correct_username, current_time, action))
     conn.commit()


#record use log
def log_it_already(hostname,username):
     log_info = hostname+'/'+username
     file_name = "E:\python_projects\logfile.txt"
     
     try:
          with open(file_name, 'r') as file:
               content = file.read()

          for line in log_info:
               if line not in content:
                    with open(file_name, 'a') as file:
                         file.write(log_info + "\n")
                         break
               else:
                    pass

     except FileNotFoundError:
          with open(file_name, 'w') as file:
               file.write(log_info+"\n")


#loss the log
def log_out_already(hostname,username):
     log_info = hostname+'/'+username
     file_path = "E:\python_projects\logfile.txt"
     with open(file_path, 'r') as file:
        lines = file.readlines()

     lines = [line for line in lines if log_info not in line]

     with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)



#signout
def log_out():
     
     st.rerun()

# authorization check
def autho():
     global authorization
     if authorization == "admin":
            return 'admin'
     elif authorization == "user":
            return 'user'
     else:
           return 'viewer'
     

# check duplication function
def already_exists_account(current_username):
    selected_query = 'SELECT TOP 1 1 FROM accounts WHERE current_username = ?'
    cursor.execute(selected_query ,(current_username,))
    result = cursor.fetchone()
    conn.commit()
    exists = result is not None
    if exists:
         return False
    else:
         return True

def already_exists_chassis(chassisnum):
    selected_query = 'SELECT TOP 1 1 FROM newcar WHERE chassis_number = ?'
    cursor.execute(selected_query ,(chassisnum,))
    result = cursor.fetchone()
    conn.commit()
    exists = result is not None
    if exists:
         return False
    else:
         return True

# info_page function
def load_data(dataset):
	df = pd.read_csv(dataset)
	return df


# add_vehicle function
def add_execution(*v):
     type_option = str(v[0])
     model_option = str(v[1])
     date_option = str(v[2])
     cylinders_option = str(v[3])
     fuel_option = str(v[4])
     cartype_option = str(v[5])
     governorates_option = str(v[6])
     cargovernorates_option = str(v[7])
     color_option = str(v[8])
     chassis_number = str(v[9])
     letter_carnumber = str(v[10])
     carnumber = str(v[11])
     letter_annualnumber = str(v[12])
     annualnumber = str(v[13])
     receive_type = str(v[14])
     car_folder = str(v[15])
     fromrec = str(v[16])
     notes = str(v[17])
     gearstick = str(v[18])
     registerationtype = str(v[19])
     carnumbertype = str(v[20])
     car_owner = 'لا يوجد'
     if letter_carnumber == 'لا يوجد':
          letter_carnumber = '_'
     

     try:
                    fulcarnumber = letter_carnumber + carnumber
                    fulannualnumber = letter_annualnumber + annualnumber
                    create_table_query = '''
                              CREATE TABLE dbo.newcar (
                              chassis_number NVARCHAR(255),type_option NVARCHAR(255),fulcarnumber NVARCHAR(255),fulannualnumber NVARCHAR(255),
                              model_option NVARCHAR(255),date_option NVARCHAR(255),governorates_option NVARCHAR(255),cargovernorates_option NVARCHAR(255),cylinders_option NVARCHAR(255),
                              fuel_option NVARCHAR(255),color_option NVARCHAR(255),receive_type NVARCHAR(255),
                              current_username NVARCHAR(255), cartype_option NVARCHAR(255), car_owner NVARCHAR(255), car_folder NVARCHAR(255),
                              fromrec NVARCHAR(255),notes NVARCHAR(255),gearstick NVARCHAR(255),registerationtype NVARCHAR(255),carnumbertype NVARCHAR(255)
                                                       )
                                                            '''
                    
                    cursor.execute(create_table_query)
                    conn.commit()
                    
     except:
                    pass
               
     check_position_query = f'''
          SELECT COUNT(*)
          FROM dbo.newcar
          WHERE chassis_number = ?
          '''

     cursor.execute(check_position_query, (chassis_number,))
     chas_exists = cursor.fetchone()[0]
     if chas_exists > 0:
          st.error("المركبة مسجلة مسبقاً")
     
     elif len(chassis_number) < 17:
          st.error("يوجد نقص في رقم الشاصي")

     else:
          if any(item == '' for item in v):
               #st.error("يجب ملئ كافة المعلومات")
               st.write("")
          else:
               try:
                    fulcarnumber = letter_carnumber + carnumber
                    fulannualnumber = letter_annualnumber + annualnumber
                    create_table_query = '''
                              CREATE TABLE dbo.newcar (
                              chassis_number NVARCHAR(255),type_option NVARCHAR(255),fulcarnumber NVARCHAR(255),fulannualnumber NVARCHAR(255),
                              model_option NVARCHAR(255),date_option NVARCHAR(255),governorates_option NVARCHAR(255),cargovernorates_option NVARCHAR(255),cylinders_option NVARCHAR(255),
                              fuel_option NVARCHAR(255),color_option NVARCHAR(255),receive_type NVARCHAR(255),
                              current_username NVARCHAR(255), cartype_option NVARCHAR(255), car_owner NVARCHAR(255), car_folder NVARCHAR(255),
                              fromrec NVARCHAR(255),notes NVARCHAR(255),gearstick NVARCHAR(255),registerationtype NVARCHAR(255),carnumbertype NVARCHAR(255)
                                                       )
                                                            '''
                    insert_query = '''
                              INSERT INTO newcar (
                              chassis_number,type_option,fulcarnumber,fulannualnumber,
                              model_option,date_option,governorates_option,cargovernorates_option,cylinders_option,
                              fuel_option,color_option,receive_type,
                              current_username, cartype_option, car_owner, car_folder, fromrec, notes, gearstick,registerationtype,carnumbertype
                                                       ) 
                                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                                                            '''
                    cursor.execute(create_table_query)
                    conn.commit()
                    cursor.execute(insert_query, (
                              chassis_number,type_option,fulcarnumber,fulannualnumber,
                              model_option,date_option,governorates_option,cargovernorates_option,cylinders_option,
                              fuel_option,color_option,receive_type,
                              correct_username, cartype_option, car_owner, car_folder, fromrec, notes,gearstick,registerationtype,carnumbertype
                                                       ))
                    conn.commit()
                    st.success('تم اضافة المعلومات بنجاح')
               except:
                    fulcarnumber = letter_carnumber + carnumber
                    fulannualnumber = letter_annualnumber + annualnumber
                    insert_query = '''
                              INSERT INTO newcar (
                              chassis_number,type_option,fulcarnumber,fulannualnumber,
                              model_option,date_option,governorates_option,cargovernorates_option,cylinders_option,
                              fuel_option,color_option,receive_type,
                              current_username, cartype_option, car_owner, car_folder, fromrec, notes, gearstick,registerationtype,carnumbertype
                                                       ) 
                                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                                                            '''
                    cursor.execute(insert_query, (
                              chassis_number,type_option,fulcarnumber,fulannualnumber,
                              model_option,date_option,governorates_option,cargovernorates_option,cylinders_option,
                              fuel_option,color_option,receive_type,
                              correct_username, cartype_option, car_owner, car_folder, fromrec, notes, gearstick,registerationtype,carnumbertype
                                                       ))
                    conn.commit()
                    st.success('تم اضافة المعلومات بنجاح')
     
                 

# delete_vehicle function
def delete_execution(chassisnum,delete_type,deleteto):
     if chassisnum == '':
           st.error("يجب ملئ كافة المعلومات")
     else:
           if len(chassisnum) < 17:
               chassis_number = num_to_chassis(chassisnum)
           else:
               chassis_number = chassisnum
           if already_exists_chassis(chassis_number):
                st.error("الرقم غير صحيح")

           else:
                create_table_query = '''
                         IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'cararchiveT')
                         BEGIN
                              CREATE TABLE dbo.cararchiveT (
                                   chassis_number NVARCHAR(255),
                                   type_option NVARCHAR(255),
                                   fulcarnumber NVARCHAR(255),
                                   fulannualnumber NVARCHAR(255),
                                   model_option NVARCHAR(255),
                                   date_option NVARCHAR(255),
                                   governorates_option NVARCHAR(255),
                                   cargovernorates_option NVARCHAR(255),
                                   cylinders_option NVARCHAR(255),
                                   fuel_option NVARCHAR(255),
                                   color_option NVARCHAR(255),
                                   receive_type NVARCHAR(255),
                                   current_username NVARCHAR(255),
                                   cartype_option NVARCHAR(255),
                                   car_owner NVARCHAR(255),
                                   car_folder NVARCHAR(255),
                                   fromrec NVARCHAR(255),
                                   notes NVARCHAR(255),
                                   gearstick NVARCHAR(255),
                                   registerationtype NVARCHAR(255),
                                   carnumbertype NVARCHAR(255),
                                   delete_type NVARCHAR(255),
                                   deleteto NVARCHAR(255)

                              )
                         END
                                                       '''
                insert_query = '''
                                   INSERT INTO dbo.cararchiveT (
                                   chassis_number,
                                   type_option,
                                   fulcarnumber,
                                   fulannualnumber,
                                   model_option,
                                   date_option,
                                   governorates_option,
                                   cargovernorates_option,
                                   cylinders_option,
                                   fuel_option,
                                   color_option,
                                   receive_type,
                                   current_username,
                                   cartype_option,
                                   car_owner,
                                   car_folder,
                                   fromrec,
                                   notes,
                                   gearstick,
                                   registerationtype,
                                   carnumbertype,
                                   delete_type,
                                   deleteto
                              )
                              SELECT
                                   chassis_number,
                                   type_option,
                                   fulcarnumber,
                                   fulannualnumber,
                                   model_option,
                                   date_option,
                                   governorates_option,
                                   cargovernorates_option,
                                   cylinders_option,
                                   fuel_option,
                                   color_option,
                                   receive_type,
                                   current_username,
                                   cartype_option,
                                   car_owner,
                                   car_folder,
                                   fromrec,
                                   notes,
                                   gearstick,
                                   registerationtype,
                                   carnumbertype,
                                   ? AS delete_type,
                                   ? AS deleteto
                              FROM dbo.newcar WHERE chassis_number = ?
                         '''
                cursor.execute(create_table_query)
                conn.commit()
                cursor.execute(insert_query, (delete_type,deleteto,chassis_number))
                conn.commit()
                #--------------------------------
                delete_query = 'DELETE FROM newcar WHERE chassis_number = ?'
                cursor.execute(delete_query, (chassis_number,))
                #delete_query = 'DELETE FROM handover WHERE chassis_number = ?'
                #cursor.execute(delete_query, (chassisnum,))
                #conn.commit()
                st.success('تم حذف المركبة بنجاح')
     
def delete_options():
     option1 = 'اهداء عام'
     option2 = 'شطب'
     option3 = 'وزارة الصناعة'
     option4 = 'بيع'
     option5 = 'تسقيط'
     option6 = 'مسروقة'

     
     try:
          create_table_query = '''
          CREATE TABLE dbo.deleteoptions (
          deletet NVARCHAR(255)
          );'''
          cursor.execute(create_table_query)
          conn.commit()
          id_query = """
          ALTER TABLE deleteoptions
          ADD ID INT IDENTITY(1,1);
          """
          cursor.execute(id_query)
          conn.commit()
          insert_deleteV_query = '''
          INSERT INTO deleteoptions (deletet)
          VALUES (?)
          '''

          cursor.execute(insert_deleteV_query, (option1,))
          cursor.execute(insert_deleteV_query, (option2,))
          select_ID_query = 'SELECT ID FROM deleteoptions WHERE deletet = ?'
          cursor.execute(select_ID_query, (option1,))
          idn = cursor.fetchone()
          conn.commit()
          nid = str(idn[0])
          subdelcol = 'delto'+nid
          add_section_query = """
          ALTER TABLE deleteoptions
          ADD delto NVARCHAR(255);
          """
          cursor.execute(add_section_query)
          conn.commit()
          insert_query = '''
          UPDATE deleteoptions SET delto = ? WHERE ID = ?
          '''
          cursor.execute(insert_query, (subdelcol,nid))
          conn.commit()
          select_ID_query = 'SELECT ID FROM deleteoptions WHERE deletet = ?'
          cursor.execute(select_ID_query, (option2,))
          idn = cursor.fetchone()
          conn.commit()
          nid = str(idn[0])
          subdelcol = 'delto'+nid
          cursor.execute(insert_query, (subdelcol,nid))
          conn.commit()

          select_ID_query = 'SELECT delto FROM deleteoptions WHERE deletet = ?'
          cursor.execute(select_ID_query, (option1,))
          idn = cursor.fetchone()
          conn.commit()

          create_table_query = f'''
                                   CREATE TABLE dbo.{idn[0]} (
                                   delto NVARCHAR(255)
                                                            )
                                                                 '''
          cursor.execute(create_table_query)
          conn.commit()
          insert_subdel_query = f'''
          INSERT INTO dbo.{idn[0]} (delto)
          VALUES (?)
          '''
          cursor.execute(insert_subdel_query, (option3,))
          conn.commit()


          select_ID_query = 'SELECT delto FROM deleteoptions WHERE deletet = ?'
          cursor.execute(select_ID_query, (option2,))
          idn = cursor.fetchone()
          conn.commit()

          create_table_query = f'''
                                   CREATE TABLE dbo.{idn[0]} (
                                   delto NVARCHAR(255)
                                                            )
                                                                 '''
          cursor.execute(create_table_query)
          conn.commit()
          insert_deleteto_query = f'''
          INSERT INTO dbo.{idn[0]} (delto)
          VALUES (?)
          '''
          print(idn[0])
          cursor.execute(insert_deleteto_query, (option4,))
          cursor.execute(insert_deleteto_query, (option5,))
          cursor.execute(insert_deleteto_query, (option6,))
          conn.commit()

          select_query = 'SELECT deletet FROM deleteoptions'
          cursor.execute(select_query)
          rows = cursor.fetchall()
          conn.commit()
          #conn.close()
          cleardata = []
          for row in rows:
               data = row[0]
               #data1 = data[0]
          for i in range(len(rows)):
               data = rows[i]
               cleardata.append(data[0])
          return cleardata
     except:
          select_query = 'SELECT deletet FROM deleteoptions'
          cursor.execute(select_query)
          rows = cursor.fetchall()
          conn.commit()
          #conn.close()
          cleardata = []
          for row in rows:
               data = row[0]
          for i in range(len(rows)):
               data = rows[i]
               cleardata.append(data[0])
          return cleardata



def subdelete(delete_type):
     select_section_query = 'SELECT delto FROM deleteoptions WHERE deletet = ?'
     cursor.execute(select_section_query, (delete_type,))
     idn = cursor.fetchone()
     conn.commit()
     select_query = f'SELECT * FROM dbo.{idn[0]}'
     cursor.execute(select_query)
     rows = cursor.fetchall()
     conn.commit()
     cleardata = []
     for row in rows:
          data = row[0]
     for i in range(len(rows)):
          data = rows[i]
          cleardata.append(data[0])
     return cleardata


#Create new account function
def create_new_account(*v):
     current_username = str(v[0])
     current_password = str(v[1])
     account_type = str(v[2])
     status = 'enabled'
     session = 'notactive'
     if any(item == '' for item in v):
           st.error("يجب ملئ كافة المعلومات")
     else:
           if already_exists_account(current_username):
                try:
                     create_table_query = '''
                              CREATE TABLE dbo.accounts (
                              current_username NVARCHAR(255),current_password NVARCHAR(255),account_type NVARCHAR(255),status NVARCHAR(255)
                                                            )
                                                            '''
                     insert_query = '''
                         INSERT INTO accounts (
                         current_username,current_password,account_type,status
                                                       ) 
                                        VALUES (?,?,?,?)
                                                            '''
                     cursor.execute(create_table_query)
                     cursor.execute(insert_query, (
                         current_username,current_password,account_type,status
                                                       ))
                     conn.commit()
                     st.success('تم انشاء الحساب بنجاح')
                except:
                     insert_query = '''
                         INSERT INTO accounts (
                         current_username,current_password,account_type,status, session
                                                       ) 
                                        VALUES (?,?,?,?,?)
                                                            '''
                     cursor.execute(insert_query, (
                         current_username,current_password,account_type,status, session
                                                       ))
                     conn.commit()
                     st.success('تم انشاء الحساب بنجاح')
           else:
                st.error('الحساب مسجل مسبقاً')


# update account information
def update_account(username,password,account_type):
     if username == '' or password == '':
           st.error("يجب ملئ كافة المعلومات")
     else:
           if already_exists_account(username):
                st.error("الحساب غير مسجل")
           else:

                update_query = '''
                UPDATE accounts
                SET current_username = ?, current_password = ?,account_type = ?  WHERE current_username = ?
                                '''
                cursor.execute(update_query, (
                        username,password,account_type,username,
                                                    ))

                conn.commit()
                st.success('تم تعديل معلومات الحساب')

#disable account
def disable_status(username,password):
     status = 'disabled'
     if username == '' or password == '':
           st.error("يجب ملئ كافة المعلومات")
     else:
           if already_exists_account(username):
                st.error("الحساب غير مسجل")
           else:

                update_query = '''
                UPDATE accounts
                SET status = ?  WHERE current_username = ?
                                '''
                cursor.execute(update_query, (
                        status,username,
                                                    ))
                conn.commit()
                
                st.success('تم تعطيل الحساب')


#enable account
def enable_status(username,password):
     status = 'enabled'
     if username == '' or password == '':
           st.error("يجب ملئ كافة المعلومات")
     else:
           if already_exists_account(username):
                st.error("الحساب غير مسجل")
           else:

                update_query = '''
                UPDATE accounts
                SET status = ?  WHERE current_username = ?
                                '''
                cursor.execute(update_query, (
                        status,username,
                                                    ))
                conn.commit()
                
                st.success('تم تفعيل الحساب')
#cars name options
def typeoption():
     option1 = 'تويوتا'
     option2 = 'مارسدس'
     option3 = 'كورولا'
     option4 = 'كامري'
     option5 = 'هاي لوكس'
     option6 = 'c300'
     option7 = 'c700'
     option8 = 'جامبو'
     
     try:
          create_table_query = '''
          CREATE TABLE dbo.typeoption (
          type NVARCHAR(255)
          );'''
          cursor.execute(create_table_query)
          conn.commit()
          id_query = """
          ALTER TABLE typeoption
          ADD ID INT IDENTITY(1,1);
          """
          cursor.execute(id_query)
          conn.commit()
          insert_department_query = '''
          INSERT INTO typeoption (type)
          VALUES (?)
          '''

          cursor.execute(insert_department_query, (option1,))
          cursor.execute(insert_department_query, (option2,))
          select_ID_query = 'SELECT ID FROM typeoption WHERE type = ?'
          cursor.execute(select_ID_query, (option1,))
          idn = cursor.fetchone()
          conn.commit()
          nid = str(idn[0])
          modelcol = 'model'+nid
          add_section_query = """
          ALTER TABLE typeoption
          ADD model NVARCHAR(255);
          """
          cursor.execute(add_section_query)
          conn.commit()
          insert_query = '''
          UPDATE typeoption SET model = ? WHERE ID = ?
          '''
          cursor.execute(insert_query, (modelcol,nid))
          conn.commit()
          select_ID_query = 'SELECT ID FROM typeoption WHERE type = ?'
          cursor.execute(select_ID_query, (option2,))
          idn = cursor.fetchone()
          conn.commit()
          nid = str(idn[0])
          modelcol = 'model'+nid
          cursor.execute(insert_query, (modelcol,nid))
          conn.commit()

          select_ID_query = 'SELECT model FROM typeoption WHERE type = ?'
          cursor.execute(select_ID_query, (option1,))
          idn = cursor.fetchone()
          conn.commit()

          create_table_query = f'''
                                   CREATE TABLE dbo.{idn[0]} (
                                   model NVARCHAR(255)
                                                            )
                                                                 '''
          cursor.execute(create_table_query)
          conn.commit()
          insert_section_query = f'''
          INSERT INTO dbo.{idn[0]} (model)
          VALUES (?)
          '''
          cursor.execute(insert_section_query, (option3,))
          cursor.execute(insert_section_query, (option4,))
          cursor.execute(insert_section_query, (option5,))
          conn.commit()


          select_ID_query = 'SELECT model FROM typeoption WHERE type = ?'
          cursor.execute(select_ID_query, (option2,))
          idn = cursor.fetchone()
          conn.commit()

          create_table_query = f'''
                                   CREATE TABLE dbo.{idn[0]} (
                                   model NVARCHAR(255)
                                                            )
                                                                 '''
          cursor.execute(create_table_query)
          conn.commit()
          insert_section_query = f'''
          INSERT INTO dbo.{idn[0]} (model)
          VALUES (?)
          '''
          cursor.execute(insert_section_query, (option6,))
          cursor.execute(insert_section_query, (option7,))
          cursor.execute(insert_section_query, (option8,))
          conn.commit()

          select_query = 'SELECT type FROM typeoption'
          cursor.execute(select_query)
          rows = cursor.fetchall()
          conn.commit()
          #conn.close()
          cleardata = []
          for row in rows:
               data = row[0]
               #data1 = data[0]
          for i in range(len(rows)):
               data = rows[i]
               cleardata.append(data[0])
          return cleardata
     except:
          select_query = 'SELECT type FROM typeoption'
          cursor.execute(select_query)
          rows = cursor.fetchall()
          conn.commit()
          #conn.close()
          cleardata = []
          for row in rows:
               data = row[0]
          for i in range(len(rows)):
               data = rows[i]
               cleardata.append(data[0])
          return cleardata

#model options
def modeloption(type_option):
     select_model_query = 'SELECT model FROM typeoption WHERE type = ?'
     cursor.execute(select_model_query, (type_option,))
     idn = cursor.fetchone()
     conn.commit()
     select_query = f'SELECT * FROM dbo.{idn[0]}'
     cursor.execute(select_query)
     rows = cursor.fetchall()
     conn.commit()
     cleardata = []
     for row in rows:
          data = row[0]
     for i in range(len(rows)):
          data = rows[i]
          cleardata.append(data[0])
     return cleardata     

#cylinders options
def cylindersoption():
     option1 = '4'
     option2 = '6'
     option3 = '8'
     option4 = '12'

     try:
          create_table_query = '''
          CREATE TABLE dbo.cylindersoption (
          cylinders NVARCHAR(255)
          );'''
          insert_query = '''
          INSERT INTO cylindersoption (cylinders)
          VALUES (?)
          '''
          cursor.execute(create_table_query)
          cursor.execute(insert_query, (option1,))
          cursor.execute(insert_query, (option2,))
          cursor.execute(insert_query, (option3,))
          cursor.execute(insert_query, (option4,))

          select_query = 'SELECT * FROM cylindersoption'
          cursor.execute(select_query)
          rows = cursor.fetchall()
          conn.commit()
          #conn.close()
          cleardata = []
          for row in rows:
               data = row[0]
               #data1 = data[0]
          for i in range(len(rows)):
               data = rows[i]
               cleardata.append(data[0])
          return cleardata
     except:
          select_query = 'SELECT * FROM cylindersoption'
          cursor.execute(select_query)
          rows = cursor.fetchall()
          conn.commit()
          #conn.close()
          cleardata = []
          for row in rows:
               data = row[0]
          for i in range(len(rows)):
               data = rows[i]
               cleardata.append(data[0])
          return cleardata     


def fueloption():
     option1 = 'كاز'
     option2 = 'بانزين'
     option3 = 'كهرباء'
     option4 = 'هايبرد'

     try:
          create_table_query = '''
          CREATE TABLE dbo.fueloption (
          fuel NVARCHAR(255)
          );'''
          insert_query = '''
          INSERT INTO fueloption (fuel)
          VALUES (?)
          '''
          cursor.execute(create_table_query)
          cursor.execute(insert_query, (option1,))
          cursor.execute(insert_query, (option2,))
          cursor.execute(insert_query, (option3,))
          cursor.execute(insert_query, (option4,))

          select_query = 'SELECT * FROM fueloption'
          cursor.execute(select_query)
          rows = cursor.fetchall()
          conn.commit()
          #conn.close()
          cleardata = []
          for row in rows:
               data = row[0]
               #data1 = data[0]
          for i in range(len(rows)):
               data = rows[i]
               cleardata.append(data[0])
          return cleardata
     except:
          select_query = 'SELECT * FROM fueloption'
          cursor.execute(select_query)
          rows = cursor.fetchall()
          conn.commit()
          #conn.close()
          cleardata = []
          for row in rows:
               data = row[0]
          for i in range(len(rows)):
               data = rows[i]
               cleardata.append(data[0])
          return cleardata


def fromrecoption():
     option1 = 'لا يوجد'
     option2 = 'مجلس محافظة بغداد'
     option3 = 'مجلس محافظة كركوك'

     try:
          create_table_query = '''
          CREATE TABLE dbo.fromreceiving (
          fromrec NVARCHAR(255)
          );'''
          insert_query = '''
          INSERT INTO fromreceiving (fromrec)
          VALUES (?)
          '''
          cursor.execute(create_table_query)
          cursor.execute(insert_query, (option1,))
          cursor.execute(insert_query, (option2,))
          cursor.execute(insert_query, (option3,))

          select_query = 'SELECT * FROM fromreceiving'
          cursor.execute(select_query)
          rows = cursor.fetchall()
          conn.commit()
          #conn.close()
          cleardata = []
          for row in rows:
               data = row[0]
               #data1 = data[0]
          for i in range(len(rows)):
               data = rows[i]
               cleardata.append(data[0])
          return cleardata
     except:
          select_query = 'SELECT * FROM fromreceiving'
          cursor.execute(select_query)
          rows = cursor.fetchall()
          conn.commit()
          #conn.close()
          cleardata = []
          for row in rows:
               data = row[0]
          for i in range(len(rows)):
               data = rows[i]
               cleardata.append(data[0])
          return cleardata


def receive_typeoption():
     option1 = 'اهداء'
     option2 = 'اعارة'
     option3 = 'شركة عامة'

     try:
          create_table_query = '''
          CREATE TABLE dbo.receivetype (
          receive NVARCHAR(255)
          );'''
          insert_query = '''
          INSERT INTO receivetype (receive)
          VALUES (?)
          '''
          cursor.execute(create_table_query)
          cursor.execute(insert_query, (option1,))
          cursor.execute(insert_query, (option2,))
          cursor.execute(insert_query, (option3,))

          select_query = 'SELECT * FROM receivetype'
          cursor.execute(select_query)
          rows = cursor.fetchall()
          conn.commit()
          #conn.close()
          cleardata = []
          for row in rows:
               data = row[0]
               #data1 = data[0]
          for i in range(len(rows)):
               data = rows[i]
               cleardata.append(data[0])
          return cleardata
     except:
          select_query = 'SELECT * FROM receivetype'
          cursor.execute(select_query)
          rows = cursor.fetchall()
          conn.commit()
          #conn.close()
          cleardata = []
          for row in rows:
               data = row[0]
          for i in range(len(rows)):
               data = rows[i]
               cleardata.append(data[0])
          return cleardata


def cartypeoption():
     option1 = 'صالون'
     option2 = 'حمل'
     option3 = 'ستيشن'

     try:
          create_table_query = '''
          CREATE TABLE dbo.cartypeoption (
          cartype NVARCHAR(255)
          );'''
          insert_query = '''
          INSERT INTO cartypeoption (cartype)
          VALUES (?)
          '''
          cursor.execute(create_table_query)
          cursor.execute(insert_query, (option1,))
          cursor.execute(insert_query, (option2,))
          cursor.execute(insert_query, (option3,))

          select_query = 'SELECT * FROM cartypeoption'
          cursor.execute(select_query)
          rows = cursor.fetchall()
          conn.commit()
          #conn.close()
          cleardata = []
          for row in rows:
               data = row[0]
               #data1 = data[0]
          for i in range(len(rows)):
               data = rows[i]
               cleardata.append(data[0])
          return cleardata
     except:
          select_query = 'SELECT * FROM cartypeoption'
          cursor.execute(select_query)
          rows = cursor.fetchall()
          conn.commit()
          #conn.close()
          cleardata = []
          for row in rows:
               data = row[0]
          for i in range(len(rows)):
               data = rows[i]
               cleardata.append(data[0])
          return cleardata

def governoratesoption():
     option1 = 'بغداد'
     option2 = 'البصرة'
     option3 = 'النجف'
     option4 = 'كربلاء'
     option5 = 'سليمانية'
     option6 = 'اربيل'
     option7 = 'دهوك'
     option8 = 'الأنبار'
     option9 = 'نينوى'
     option10 = 'صلاح الدين'
     option11 = 'ديالى'
     option12 = 'كركوك'
     option13 = 'واسط'
     option14 = 'ميسان'
     option15 = 'ذي قار'
     option16 = 'القادسية'
     option17 = 'بابل'
     option18 = 'المثنى'

     try:
          create_table_query = '''
          CREATE TABLE dbo.governoratesoption (
          governorates NVARCHAR(255)
          );'''
          insert_query = '''
          INSERT INTO governoratesoption (governorates)
          VALUES (?)
          '''
          cursor.execute(create_table_query)
          cursor.execute(insert_query, (option1,))
          cursor.execute(insert_query, (option2,))
          cursor.execute(insert_query, (option3,))
          cursor.execute(insert_query, (option4,))
          cursor.execute(insert_query, (option5,))
          cursor.execute(insert_query, (option6,))
          cursor.execute(insert_query, (option7,))
          cursor.execute(insert_query, (option8,))
          cursor.execute(insert_query, (option9,))
          cursor.execute(insert_query, (option10,))
          cursor.execute(insert_query, (option11,))
          cursor.execute(insert_query, (option12,))
          cursor.execute(insert_query, (option13,))
          cursor.execute(insert_query, (option14,))
          cursor.execute(insert_query, (option15,))
          cursor.execute(insert_query, (option16,))
          cursor.execute(insert_query, (option17,))
          cursor.execute(insert_query, (option18,))

          select_query = 'SELECT * FROM governoratesoption'
          cursor.execute(select_query)
          rows = cursor.fetchall()
          conn.commit()
          #conn.close()
          cleardata = []
          for row in rows:
               data = row[0]
               #data1 = data[0]
          for i in range(len(rows)):
               data = rows[i]
               cleardata.append(data[0])
          return cleardata
     except:
          select_query = 'SELECT * FROM governoratesoption'
          cursor.execute(select_query)
          rows = cursor.fetchall()
          conn.commit()
          #conn.close()
          cleardata = []
          for row in rows:
               data = row[0]
          for i in range(len(rows)):
               data = rows[i]
               cleardata.append(data[0])
          return cleardata

def coloroption():
     option1 = 'ابيض'
     option2 = 'اسود'
     option3 = 'اصفر'
     option4 = 'برتقالي'
     option5 = 'اخضر'
     option6 = 'بنفسجي'
     option7 = 'احمر'
     option8 = 'ازرق'
     option9 = 'رمادي'
     option10 = 'بني'
     option11 = 'زهري'

     try:
          create_table_query = '''
          CREATE TABLE dbo.coloroption (
          color NVARCHAR(255)
          );'''
          insert_query = '''
          INSERT INTO coloroption (color)
          VALUES (?)
          '''
          cursor.execute(create_table_query)
          cursor.execute(insert_query, (option1,))
          cursor.execute(insert_query, (option2,))
          cursor.execute(insert_query, (option3,))
          cursor.execute(insert_query, (option4,))
          cursor.execute(insert_query, (option5,))
          cursor.execute(insert_query, (option6,))
          cursor.execute(insert_query, (option7,))
          cursor.execute(insert_query, (option8,))
          cursor.execute(insert_query, (option9,))
          cursor.execute(insert_query, (option10,))
          cursor.execute(insert_query, (option11,))

          select_query = 'SELECT * FROM coloroption'
          cursor.execute(select_query)
          rows = cursor.fetchall()
          conn.commit()
          #conn.close()
          cleardata = []
          for row in rows:
               data = row[0]
               #data1 = data[0]
          for i in range(len(rows)):
               data = rows[i]
               cleardata.append(data[0])
          return cleardata
     except:
          select_query = 'SELECT * FROM coloroption'
          cursor.execute(select_query)
          rows = cursor.fetchall()
          conn.commit()
          #conn.close()
          cleardata = []
          for row in rows:
               data = row[0]
          for i in range(len(rows)):
               data = rows[i]
               cleardata.append(data[0])
          return cleardata

def carlettersoption():
     option1 = 'لا يوجد'
     option2 = 'أ'
     option3 = 'ب'
     option4 = 'ت'
     option5 = 'ث'
     option6 = 'ج'
     option7 = 'ح'
     option8 = 'خ'
     option9 = 'د'
     option10 = 'ذ'
     option11 = 'ر'
     option12 = 'ز'
     option13 = 'س'
     option14 = 'ش'
     option15 = 'ص'
     option16 = 'ض'
     option17 = 'ط'
     option18 = 'ظ'
     option19 = 'ع'
     option20 = 'غ'
     option21 = 'ف'
     option22 = 'ق'
     option23 = 'ك'
     option24 = 'ل'
     option25 = 'م'
     option26 = 'ن'
     option27 = 'ه'
     option28 = 'و'
     option29 = 'ي'
     option30 = "A"
     option31 = "B"
     option32 = "C"
     option33 = "D"
     option34 = "E"
     option35 = "F"
     option36 = "G"
     option37 = "H"
     option38 = "I"
     option39 = "J"
     option40 = "K"
     option41 = "L"
     option42 = "M"
     option43 = "N"
     option44 = "O"
     option45 = "P"
     option46 = "Q"
     option47 = "R"
     option48 = "S"
     option49 = "T"
     option50 = "U"
     option51 = "V"
     option52 = "W"
     option53 = "X"
     option54 = "Y"
     option55 = "Z"

     try:
          create_table_query = '''
          CREATE TABLE dbo.carlettersoption (
          letters NVARCHAR(255)
          );'''
          insert_query = '''
          INSERT INTO carlettersoption (letters)
          VALUES (?)
          '''
          cursor.execute(create_table_query)
          cursor.execute(insert_query, (option1,))
          cursor.execute(insert_query, (option2,))
          cursor.execute(insert_query, (option3,))
          cursor.execute(insert_query, (option4,))
          cursor.execute(insert_query, (option5,))
          cursor.execute(insert_query, (option6,))
          cursor.execute(insert_query, (option7,))
          cursor.execute(insert_query, (option8,))
          cursor.execute(insert_query, (option9,))
          cursor.execute(insert_query, (option10,))
          cursor.execute(insert_query, (option11,))
          cursor.execute(insert_query, (option12,))
          cursor.execute(insert_query, (option13,))
          cursor.execute(insert_query, (option14,))
          cursor.execute(insert_query, (option15,))
          cursor.execute(insert_query, (option16,))
          cursor.execute(insert_query, (option17,))
          cursor.execute(insert_query, (option18,))
          cursor.execute(insert_query, (option19,))
          cursor.execute(insert_query, (option20,))
          cursor.execute(insert_query, (option21,))
          cursor.execute(insert_query, (option22,))
          cursor.execute(insert_query, (option23,))
          cursor.execute(insert_query, (option24,))
          cursor.execute(insert_query, (option25,))
          cursor.execute(insert_query, (option26,))
          cursor.execute(insert_query, (option27,))
          cursor.execute(insert_query, (option28,))
          cursor.execute(insert_query, (option29,))
          cursor.execute(insert_query, (option30,))
          cursor.execute(insert_query, (option31,))
          cursor.execute(insert_query, (option32,))
          cursor.execute(insert_query, (option33,))
          cursor.execute(insert_query, (option34,))
          cursor.execute(insert_query, (option35,))
          cursor.execute(insert_query, (option36,))
          cursor.execute(insert_query, (option37,))
          cursor.execute(insert_query, (option38,))
          cursor.execute(insert_query, (option39,))
          cursor.execute(insert_query, (option40,))
          cursor.execute(insert_query, (option41,))
          cursor.execute(insert_query, (option42,))
          cursor.execute(insert_query, (option43,))
          cursor.execute(insert_query, (option44,))
          cursor.execute(insert_query, (option45,))
          cursor.execute(insert_query, (option46,))
          cursor.execute(insert_query, (option47,))
          cursor.execute(insert_query, (option48,))
          cursor.execute(insert_query, (option49,))
          cursor.execute(insert_query, (option50,))
          cursor.execute(insert_query, (option51,))
          cursor.execute(insert_query, (option52,))
          cursor.execute(insert_query, (option53,))
          cursor.execute(insert_query, (option54,))
          cursor.execute(insert_query, (option55,))


          select_query = 'SELECT * FROM carlettersoption'
          cursor.execute(select_query)
          rows = cursor.fetchall()
          conn.commit()
          #conn.close()
          cleardata = []
          for row in rows:
               data = row[0]
               #data1 = data[0]
          for i in range(len(rows)):
               data = rows[i]
               cleardata.append(data[0])
          return cleardata
     except:
          select_query = 'SELECT * FROM carlettersoption'
          cursor.execute(select_query)
          rows = cursor.fetchall()
          conn.commit()
          #conn.close()
          cleardata = []
          for row in rows:
               data = row[0]
          for i in range(len(rows)):
               data = rows[i]
               cleardata.append(data[0])
          return cleardata
     

#letters options gov
def lettersoption():
     option1 = 'أ'
     option2 = 'ب'
     option3 = 'ت'
     option4 = 'ث'
     option5 = 'ج'
     option6 = 'ح'
     option7 = 'خ'
     option8 = 'د'
     option9 = 'ذ'
     option10 = 'ر'
     option11 = 'ز'
     option12 = 'س'
     option13 = 'ش'
     option14 = 'ص'
     option15 = 'ض'
     option16 = 'ط'
     option17 = 'ظ'
     option18 = 'ع'
     option19 = 'غ'
     option20 = 'ف'
     option21 = 'ق'
     option22 = 'ك'
     option23 = 'ل'
     option24 = 'م'
     option25 = 'ن'
     option26 = 'ه'
     option27 = 'و'
     option28 = 'ي'
     option30 = "A"
     option31 = "B"
     option32 = "C"
     option33 = "D"
     option34 = "E"
     option35 = "F"
     option36 = "G"
     option37 = "H"
     option38 = "I"
     option39 = "J"
     option40 = "K"
     option41 = "L"
     option42 = "M"
     option43 = "N"
     option44 = "O"
     option45 = "P"
     option46 = "Q"
     option47 = "R"
     option48 = "S"
     option49 = "T"
     option50 = "U"
     option51 = "V"
     option52 = "W"
     option53 = "X"
     option54 = "Y"
     option55 = "Z"


     try:
          create_table_query = '''
          CREATE TABLE dbo.lettersoption (
          letters NVARCHAR(255)
          );'''
          insert_query = '''
          INSERT INTO lettersoption (letters)
          VALUES (?)
          '''
          cursor.execute(create_table_query)
          cursor.execute(insert_query, (option1,))
          cursor.execute(insert_query, (option2,))
          cursor.execute(insert_query, (option3,))
          cursor.execute(insert_query, (option4,))
          cursor.execute(insert_query, (option5,))
          cursor.execute(insert_query, (option6,))
          cursor.execute(insert_query, (option7,))
          cursor.execute(insert_query, (option8,))
          cursor.execute(insert_query, (option9,))
          cursor.execute(insert_query, (option10,))
          cursor.execute(insert_query, (option11,))
          cursor.execute(insert_query, (option12,))
          cursor.execute(insert_query, (option13,))
          cursor.execute(insert_query, (option14,))
          cursor.execute(insert_query, (option15,))
          cursor.execute(insert_query, (option16,))
          cursor.execute(insert_query, (option17,))
          cursor.execute(insert_query, (option18,))
          cursor.execute(insert_query, (option19,))
          cursor.execute(insert_query, (option20,))
          cursor.execute(insert_query, (option21,))
          cursor.execute(insert_query, (option22,))
          cursor.execute(insert_query, (option23,))
          cursor.execute(insert_query, (option24,))
          cursor.execute(insert_query, (option25,))
          cursor.execute(insert_query, (option26,))
          cursor.execute(insert_query, (option27,))
          cursor.execute(insert_query, (option28,))
          cursor.execute(insert_query, (option30,))
          cursor.execute(insert_query, (option31,))
          cursor.execute(insert_query, (option32,))
          cursor.execute(insert_query, (option33,))
          cursor.execute(insert_query, (option34,))
          cursor.execute(insert_query, (option35,))
          cursor.execute(insert_query, (option36,))
          cursor.execute(insert_query, (option37,))
          cursor.execute(insert_query, (option38,))
          cursor.execute(insert_query, (option39,))
          cursor.execute(insert_query, (option40,))
          cursor.execute(insert_query, (option41,))
          cursor.execute(insert_query, (option42,))
          cursor.execute(insert_query, (option43,))
          cursor.execute(insert_query, (option44,))
          cursor.execute(insert_query, (option45,))
          cursor.execute(insert_query, (option46,))
          cursor.execute(insert_query, (option47,))
          cursor.execute(insert_query, (option48,))
          cursor.execute(insert_query, (option49,))
          cursor.execute(insert_query, (option50,))
          cursor.execute(insert_query, (option51,))
          cursor.execute(insert_query, (option52,))
          cursor.execute(insert_query, (option53,))
          cursor.execute(insert_query, (option54,))
          cursor.execute(insert_query, (option55,))


          select_query = 'SELECT * FROM lettersoption'
          cursor.execute(select_query)
          rows = cursor.fetchall()
          conn.commit()
          #conn.close()
          cleardata = []
          for row in rows:
               data = row[0]
               #data1 = data[0]
          for i in range(len(rows)):
               data = rows[i]
               cleardata.append(data[0])
          return cleardata
     except:
          select_query = 'SELECT * FROM lettersoption'
          cursor.execute(select_query)
          rows = cursor.fetchall()
          conn.commit()
          #conn.close()
          cleardata = []
          for row in rows:
               data = row[0]
          for i in range(len(rows)):
               data = rows[i]
               cleardata.append(data[0])
          return cleardata


def positionoption():
     option1 = 'مبرمج'
     option2 = 'معاون مبرمج'
     option3 = 'معاون محاسب'

     try:
          create_table_query = '''
          CREATE TABLE dbo.position (
          account NVARCHAR(255)
          );'''
          insert_query = '''
          INSERT INTO position (account)
          VALUES (?)
          '''
          cursor.execute(create_table_query)
          cursor.execute(insert_query, (option1,))
          cursor.execute(insert_query, (option2,))
          cursor.execute(insert_query, (option3,))
          conn.commit()
          select_query = 'SELECT * FROM position'
          cursor.execute(select_query)
          rows = cursor.fetchall()
          conn.commit()
          #conn.close()
          cleardata = []
          for row in rows:
               data = row[0]
               #data1 = data[0]
          for i in range(len(rows)):
               data = rows[i]
               cleardata.append(data[0])
          return cleardata
     except:
          select_query = 'SELECT * FROM position'
          cursor.execute(select_query)
          rows = cursor.fetchall()
          conn.commit()
          #conn.close()
          cleardata = []
          for row in rows:
               data = row[0]
          for i in range(len(rows)):
               data = rows[i]
               cleardata.append(data[0])
          return cleardata


def accountty():
     option1 = 'admin'
     option2 = 'user'
     option3 = 'viewer'

     try:
          create_table_query = '''
          CREATE TABLE dbo.accountty (
          account NVARCHAR(255)
          );'''
          insert_query = '''
          INSERT INTO accountty (account)
          VALUES (?)
          '''
          cursor.execute(create_table_query)
          cursor.execute(insert_query, (option1,))
          cursor.execute(insert_query, (option2,))
          cursor.execute(insert_query, (option3,))
          conn.commit()
          select_query = 'SELECT * FROM accountty'
          cursor.execute(select_query)
          rows = cursor.fetchall()
          conn.commit()
          #conn.close()
          cleardata = []
          for row in rows:
               data = row[0]
               #data1 = data[0]
          for i in range(len(rows)):
               data = rows[i]
               cleardata.append(data[0])
          return cleardata
     except:
          select_query = 'SELECT * FROM accountty'
          cursor.execute(select_query)
          rows = cursor.fetchall()
          conn.commit()
          #conn.close()
          cleardata = []
          for row in rows:
               data = row[0]
          for i in range(len(rows)):
               data = rows[i]
               cleardata.append(data[0])
          return cleardata

def malfunctionsoptions():
     option1 = 'كسر في المرآة'
     option2 = 'عطل في مكيف الهواء'
     option3 = 'عطل في طوافة الوقود'
     option4 = 'مشكلة في البطارية'
     option5 = 'المكابح'
     option6 = 'الصمامات أو الأجزاء الداخلية'
     option7 = 'ثقوب في الأطارات'
     #table_name = 'malfunctionsoptions'
     
     #conn = pyodbc.connect(connection_string)
     #cursor = conn.cursor()
     try:
          create_table_query = '''
          CREATE TABLE dbo.malfunctionsoptions (
          malfunctions NVARCHAR(255)
          );'''
          insert_query = '''
          INSERT INTO malfunctionsoptions (malfunctions)
          VALUES (?)
          '''
          cursor.execute(create_table_query)
          cursor.execute(insert_query, (option1,))
          cursor.execute(insert_query, (option2,))
          cursor.execute(insert_query, (option3,))
          cursor.execute(insert_query, (option4,))
          cursor.execute(insert_query, (option5,))
          cursor.execute(insert_query, (option6,))
          cursor.execute(insert_query, (option7,))
          select_query = 'SELECT * FROM malfunctionsoptions'
          cursor.execute(select_query)
          rows = cursor.fetchall()
          conn.commit()
          #conn.close()
          cleardata = []
          for row in rows:
               data = row[0]
               #data1 = data[0]
          for i in range(len(rows)):
               data = rows[i]
               cleardata.append(data[0])
          return cleardata
     except:
          select_query = 'SELECT * FROM malfunctionsoptions'
          cursor.execute(select_query)
          rows = cursor.fetchall()
          conn.commit()
          #conn.close()
          cleardata = []
          for row in rows:
               data = row[0]
          for i in range(len(rows)):
               data = rows[i]
               cleardata.append(data[0])
          return cleardata
     

def registerationtypeoption():
     option1 = 'خصوصي'
     option2 = 'اجرة'
     option3 = 'حمل'
     option4 = 'حكومي'
     option5 = 'انشائية'
     option6 = 'مؤقت'
     #table_name = 'malfunctionsoptions'
     
     #conn = pyodbc.connect(connection_string)
     #cursor = conn.cursor()
     try:
          create_table_query = '''
          CREATE TABLE dbo.registerationt (
          registeration NVARCHAR(255)
          );'''
          insert_query = '''
          INSERT INTO registerationt (registeration)
          VALUES (?)
          '''
          cursor.execute(create_table_query)
          cursor.execute(insert_query, (option1,))
          cursor.execute(insert_query, (option2,))
          cursor.execute(insert_query, (option3,))
          cursor.execute(insert_query, (option4,))
          cursor.execute(insert_query, (option5,))
          cursor.execute(insert_query, (option6,))
          select_query = 'SELECT * FROM registerationt'
          cursor.execute(select_query)
          rows = cursor.fetchall()
          conn.commit()
          #conn.close()
          cleardata = []
          for row in rows:
               data = row[0]
               #data1 = data[0]
          for i in range(len(rows)):
               data = rows[i]
               cleardata.append(data[0])
          return cleardata
     except:
          select_query = 'SELECT * FROM registerationt'
          cursor.execute(select_query)
          rows = cursor.fetchall()
          conn.commit()
          #conn.close()
          cleardata = []
          for row in rows:
               data = row[0]
          for i in range(len(rows)):
               data = rows[i]
               cleardata.append(data[0])
          return cleardata

#handover_vehicle
def departmentoptions():
     option1 = 'الأدارية والمالية'
     option2 = 'مكتب رئيس الهيئة'
     option3 = 'تكنولوجيا المعلومات'
     option4 = 'التدقيق'
     
     try:
          create_table_query = '''
          CREATE TABLE dbo.departmentoptions (
          department NVARCHAR(255)
          );'''
          cursor.execute(create_table_query)
          conn.commit()
          id_query = """
          ALTER TABLE departmentoptions
          ADD ID INT IDENTITY(1,1);
          """
          cursor.execute(id_query)
          conn.commit()
          insert_department_query = '''
          INSERT INTO departmentoptions (department)
          VALUES (?)
          '''

          cursor.execute(insert_department_query, (option1,))
          cursor.execute(insert_department_query, (option2,))
          select_ID_query = 'SELECT ID FROM departmentoptions WHERE department = ?'
          cursor.execute(select_ID_query, (option1,))
          idn = cursor.fetchone()
          conn.commit()
          nid = str(idn[0])
          sectioncol = 'section'+nid
          add_section_query = """
          ALTER TABLE departmentoptions
          ADD Section NVARCHAR(255);
          """
          cursor.execute(add_section_query)
          conn.commit()
          insert_query = '''
          UPDATE departmentoptions SET Section = ? WHERE ID = ?
          '''
          cursor.execute(insert_query, (sectioncol,nid))
          conn.commit()
          select_ID_query = 'SELECT ID FROM departmentoptions WHERE department = ?'
          cursor.execute(select_ID_query, (option2,))
          idn = cursor.fetchone()
          conn.commit()
          nid = str(idn[0])
          sectioncol = 'section'+nid
          cursor.execute(insert_query, (sectioncol,nid))
          conn.commit()

          select_ID_query = 'SELECT Section FROM departmentoptions WHERE department = ?'
          cursor.execute(select_ID_query, (option1,))
          idn = cursor.fetchone()
          conn.commit()

          create_table_query = f'''
                                   CREATE TABLE dbo.{idn[0]} (
                                   section NVARCHAR(255)
                                                            )
                                                                 '''
          cursor.execute(create_table_query)
          conn.commit()
          insert_section_query = f'''
          INSERT INTO dbo.{idn[0]} (section)
          VALUES (?)
          '''
          cursor.execute(insert_section_query, (option3,))
          conn.commit()


          select_ID_query = 'SELECT Section FROM departmentoptions WHERE department = ?'
          cursor.execute(select_ID_query, (option2,))
          idn = cursor.fetchone()
          conn.commit()

          create_table_query = f'''
                                   CREATE TABLE dbo.{idn[0]} (
                                   section NVARCHAR(255)
                                                            )
                                                                 '''
          cursor.execute(create_table_query)
          conn.commit()
          insert_section_query = f'''
          INSERT INTO dbo.{idn[0]} (section)
          VALUES (?)
          '''
          cursor.execute(insert_section_query, (option4,))
          conn.commit()

          select_query = 'SELECT department FROM departmentoptions'
          cursor.execute(select_query)
          rows = cursor.fetchall()
          conn.commit()
          #conn.close()
          cleardata = []
          for row in rows:
               data = row[0]
               #data1 = data[0]
          for i in range(len(rows)):
               data = rows[i]
               cleardata.append(data[0])
          return cleardata
     except:
          select_query = 'SELECT department FROM departmentoptions'
          cursor.execute(select_query)
          rows = cursor.fetchall()
          conn.commit()
          #conn.close()
          cleardata = []
          for row in rows:
               data = row[0]
          for i in range(len(rows)):
               data = rows[i]
               cleardata.append(data[0])
          return cleardata


#handover_vehicle
def sectionoptions(department):
     select_section_query = 'SELECT Section FROM departmentoptions WHERE department = ?'
     cursor.execute(select_section_query, (department,))
     idn = cursor.fetchone()
     conn.commit()
     select_query = f'SELECT * FROM dbo.{idn[0]}'
     cursor.execute(select_query)
     rows = cursor.fetchall()
     conn.commit()
     cleardata = []
     for row in rows:
          data = row[0]
     for i in range(len(rows)):
          data = rows[i]
          cleardata.append(data[0])
     return cleardata


#fetch for edit
def malfuneditbutton(malfunctions):
     select_query = f'SELECT * FROM dbo.{malfunctions}'
     cursor.execute(select_query)
     rows = cursor.fetchall()
     conn.commit()
     cleardata = []
     for row in rows:
          data = row[0]
     for i in range(len(rows)):
          data = rows[i]
          cleardata.append(data[0])
     return cleardata



#get chassis number
def num_to_chassis(id_number):
     select_query = 'SELECT chassis_number FROM newcar WHERE fulcarnumber = ?'
     cursor.execute(select_query ,(id_number,))
     row = cursor.fetchone()
     conn.commit()
     row = str(row).replace("('", "").replace("',)", "")
     if row is None:
          st.error('يوجد خطأ في رقم المركبة')
     else:
          return row


#archive table when we handover the vehicle to a new owner
def handover_archive(current_car_owner,malfunctionsarc,chassis_number):
     create_table_query = '''
                         IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'handoverarchive')
                         BEGIN
                              CREATE TABLE dbo.handoverarchive (
                                   chassis_number NVARCHAR(255),
                                   current_car_owner NVARCHAR(255),
                                   position NVARCHAR(255),
                                   document_number NVARCHAR(255),
                                   document_date NVARCHAR(255),
                                   recivie_date NVARCHAR(255),
                                   allocations NVARCHAR(255),
                                   malfuntable NVARCHAR(255),
                                   vehicle_meter INT,
                                   department NVARCHAR(255),
                                   section NVARCHAR(255)
                              )
                         END
                                                       '''
     insert_query = '''
                                   INSERT INTO dbo.handoverarchive (
                                   chassis_number,
                                   current_car_owner,
                                   position,
                                   document_number,
                                   document_date,
                                   recivie_date,
                                   allocations,
                                   malfuntable,
                                   vehicle_meter,
                                   department,
                                   section
                              )
                              SELECT
                                   chassis_number,
                                   ? AS current_car_owner,
                                   position,
                                   document_number,
                                   document_date,
                                   recivie_date,
                                   allocations,
                                   ? AS malfuntable,
                                   vehicle_meter,
                                   department,
                                   section
                              FROM dbo.handover WHERE current_car_owner = ?
                         '''
     cursor.execute(create_table_query)
     conn.commit()
     cursor.execute(insert_query, (current_car_owner, malfunctionsarc, current_car_owner))
     conn.commit()
     delete_query = '''
                    DELETE FROM dbo.handover
                    WHERE chassis_number = ? AND current_car_owner = ?
                    '''
     cursor.execute(delete_query, (chassis_number,current_car_owner))
     conn.commit()

     new_chassis = 'cust'+str(chassis_number)

     create_malar_table_query = f'''
                         IF NOT EXISTS (SELECT * FROM sys.tables WHERE object_id = OBJECT_ID(N'dbo.{malfunctionsarc}') AND type in (N'U'))
                         BEGIN
                              CREATE TABLE dbo.{malfunctionsarc} (
                                   malfunctions NVARCHAR(255),
                                   current_car_owner NVARCHAR(255)
                              )
                         END
                                                       '''
     insert_query =f'''
                                   INSERT INTO dbo.{malfunctionsarc} (
                                   malfunctions,
                                   current_car_owner
                              )
                              SELECT
                                   malfunctions,
                                   current_car_owner
                              FROM dbo.{new_chassis} WHERE current_car_owner = ?
                         '''
     cursor.execute(create_malar_table_query)
     conn.commit()
     cursor.execute(insert_query, (current_car_owner,))
     conn.commit()
     delete_query =f'''
                    DELETE FROM dbo.{new_chassis}
                    WHERE current_car_owner = ?
                    '''
     cursor.execute(delete_query, (current_car_owner,))
     conn.commit()
     # we can reach the malfunctions by chassis number to reach the table name and current_car_owner to and took 
     # all of the malfunctions from the malfunctions to the malfunctionsarc



#update the car owner in newcar table
def owner_update(current_car_owner,chassis_number):
     selected_query = 'SELECT car_owner FROM newcar WHERE chassis_number = ?'
     cursor.execute(selected_query ,(chassis_number,))
     result = cursor.fetchone()
     conn.commit()
     result = str(result).replace("('", "").replace("',)", "")
     malfunctionsarc = 'custar'+str(chassis_number)

     if result != 'لا يوجد':
          if current_car_owner != result:
               update_query = '''
                UPDATE newcar
                SET car_owner = ? WHERE chassis_number = ?
                                '''
               cursor.execute(update_query, (
                        current_car_owner,chassis_number
                                                    ))
               conn.commit()
               handover_archive(result,malfunctionsarc,chassis_number)
          else:
               pass
     
     else:
          if current_car_owner != result:
               update_query = '''
                UPDATE newcar
                SET car_owner = ? WHERE chassis_number = ?
                                '''
               cursor.execute(update_query, (
                        current_car_owner,chassis_number
                                                    ))
               conn.commit()
               handover_archive(result,malfunctionsarc,chassis_number)
          else:
               pass


# the malfunctions by owner
def owner_malfunctions(malfuntable,malfunctions,current_car_owner):
     try:
          create_table_query = f'''
                         CREATE TABLE dbo.{malfuntable} (
                         malfunctions NVARCHAR(255),current_car_owner NVARCHAR(255)
                                                  )
                                                       '''
          cursor.execute(create_table_query)
          conn.commit()
          insert_query = f'''
                              INSERT INTO dbo.{malfuntable} (malfunctions, current_car_owner)
                              VALUES (?, ?)
                         '''
          if malfunctions == 'لا يوجد':
               pass
          else:
               for mal in malfunctions:
                    cursor.execute(insert_query, (mal, current_car_owner))
                    conn.commit()
     
     except:
          insert_query = f'''
                              INSERT INTO dbo.{malfuntable} (malfunctions, current_car_owner)
                              VALUES (?, ?)
                         '''
          if malfunctions == 'لا يوجد':
               pass
          else:
               for mal in malfunctions:
                    cursor.execute(insert_query, (mal, current_car_owner))
                    conn.commit()


# fuel calculation table
def fuel_cal(chassis_number,current_car_owner,recivie_date,vehicle_meter):
     monpay = 'mon'+str(chassis_number)
     try:
          create_table_query = '''
                              CREATE TABLE dbo.fuel_cal (
                              chassis_number NVARCHAR(255),current_car_owner NVARCHAR(255),
                              recivie_date NVARCHAR(255),vehicle_meter INT,monthpayment NVARCHAR(255)
                                                       )
                                                            '''
          insert_query = '''
                              INSERT INTO fuel_cal (
                              chassis_number,current_car_owner,
                              recivie_date,vehicle_meter,monthpayment
                                                       ) 
                                        VALUES (?,?,?,?,?)
                                                            '''
          cursor.execute(create_table_query)
          conn.commit()
          cursor.execute(insert_query, (
                                        chassis_number,current_car_owner,recivie_date,vehicle_meter,monpay
                                                       ))
          conn.commit()
          create_table_query = f'''
                         CREATE TABLE dbo.{monpay} (
                         payment INT,date NVARCHAR(255)
                                                  )
                                                       '''
          cursor.execute(create_table_query)
          conn.commit()
     except:
          check_query = '''
               SELECT COUNT(*) FROM dbo.fuel_cal 
               WHERE chassis_number = ?
                    '''

          cursor.execute(check_query, (chassis_number,))
          count = cursor.fetchone()[0]
          if count > 0:
               select_query = '''SELECT current_car_owner from fuel_cal WHERE chassis_number = ?'''
               cursor.execute(select_query, (
                                             chassis_number
                                                       ))
               result = cursor.fetchone()
               conn.commit()
               result = str(result).replace("('", "").replace("',)", "")
               if result == current_car_owner:
                    pass
               else:
                    delete_query = '''DELETE FROM dbo.fuel_cal WHERE chassis_number = ?'''
                    cursor.execute(delete_query, (chassis_number,))
                    conn.commit()
                    insert_query = '''
                                        INSERT INTO fuel_cal (
                                        chassis_number,current_car_owner,
                                        recivie_date,vehicle_meter,monthpayment
                                                                 ) 
                                                  VALUES (?,?,?,?,?)
                                                                      '''
                    cursor.execute(insert_query, (
                                                  chassis_number,current_car_owner,recivie_date,vehicle_meter,monpay
                                                            ))
                    conn.commit()
          else:
                    insert_query = '''
                                        INSERT INTO fuel_cal (
                                        chassis_number,current_car_owner,
                                        recivie_date,vehicle_meter,monthpayment
                                                                 ) 
                                                  VALUES (?,?,?,?,?)
                                                                      '''
                    cursor.execute(insert_query, (
                                                  chassis_number,current_car_owner,recivie_date,vehicle_meter,monpay
                                                            ))
                    conn.commit()
               

# haveover_vehicle funcrtion
def handover_exe(*v):
     id_number = str(v[0])
     current_car_owner = str(v[1])
     document_number = str(v[2])
     document_date = str(v[3])
     recivie_date = str(v[4])
     allocations = str(v[5])
     malfunctions = v[6]
     vehicle_meter = int(v[7])
     department = str(v[8])
     section = str(v[9])
     position = str(v[10])
     if malfunctions == '[]':
          malfunctions = 'لا يوجد'
     C = [id_number,current_car_owner,document_number,document_date,recivie_date,allocations,malfunctions,
                        vehicle_meter,department,section,position]
     if any(item == '' for item in C):
           st.error("يجب ملئ كافة المعلومات")
     else:
          id_number = str(v[0])
          current_car_owner = str(v[1])
          document_number = str(v[2])
          document_date = str(v[3])
          recivie_date = str(v[4])
          allocations = str(v[5])
          malfunctions = v[6]
          vehicle_meter = int(v[7])
          department = str(v[8])
          section = str(v[9])
          position = str(v[10])
          if malfunctions == '[]':
               malfunctions = 'لا يوجد'
          if len(id_number) <= 6:
               chassis_number = num_to_chassis(id_number)
          else:
               chassis_number = id_number
          malfuntable = 'cust'+str(chassis_number)

          check_query = '''
               SELECT COUNT(*) FROM dbo.newcar 
               WHERE chassis_number = ?
                    '''

          cursor.execute(check_query, (chassis_number,))
          count = cursor.fetchone()[0]
          if count > 0:
               try:
                    create_table_query = '''
                              CREATE TABLE dbo.handover (
                              chassis_number NVARCHAR(255),current_car_owner NVARCHAR(255),
                              position NVARCHAR(255),document_number NVARCHAR(255),document_date NVARCHAR(255),
                              recivie_date NVARCHAR(255),allocations NVARCHAR(255),malfuntable NVARCHAR(255),
                              vehicle_meter INT,department NVARCHAR(255),section NVARCHAR(255)
                                                       )
                                                            '''
                    insert_query = '''
                              INSERT INTO handover (
                              chassis_number ,current_car_owner ,
                              position ,document_number ,document_date ,
                              recivie_date ,allocations,malfuntable,
                              vehicle_meter,department,section
                                                       ) 
                                        VALUES (?,?,?,?,?,?,?,?,?,?,?)
                                                            '''
                    cursor.execute(create_table_query)
                    conn.commit()
                    cursor.execute(insert_query, (
                                                  chassis_number,current_car_owner,position,document_number,document_date,
                                                  recivie_date,allocations,malfuntable,vehicle_meter,department,section
                                                       ))
                    conn.commit()
                    owner_malfunctions(malfuntable,malfunctions,current_car_owner)
                    owner_update(current_car_owner,chassis_number)
                    if allocations == 'True':
                         fuel_cal(chassis_number,current_car_owner,recivie_date,vehicle_meter)
                    st.success('تم اضافة المعلومات بنجاح')
               except:
                    select_query = '''SELECT current_car_owner from handover WHERE chassis_number = ?'''
                    cursor.execute(select_query, (
                                                  chassis_number
                                                       ))
                    result = cursor.fetchone()
                    conn.commit()
                    result = str(result).replace("('", "").replace("',)", "")
                    if result == current_car_owner:
                         st.error(result)
                         st.error("مالك المركبة مسجل مسبقاً")
                    else:
                         insert_query = '''
                                   INSERT INTO handover (
                                   chassis_number ,current_car_owner ,
                                   position ,document_number ,document_date ,
                                   recivie_date ,allocations,malfuntable,
                                   vehicle_meter,department,section
                                                            ) 
                                             VALUES (?,?,?,?,?,?,?,?,?,?,?)
                                                                 '''
                         cursor.execute(insert_query, (
                                                       chassis_number,current_car_owner,position,document_number,document_date,
                                                       recivie_date,allocations,malfuntable,vehicle_meter,department,section
                                                            ))
                         conn.commit()
                         owner_malfunctions(malfuntable,malfunctions,current_car_owner)
                         owner_update(current_car_owner,chassis_number)
                         try:
                              create_table_query = '''
                              CREATE TABLE dbo.fuel_cal (
                              chassis_number NVARCHAR(255),current_car_owner NVARCHAR(255),
                              recivie_date NVARCHAR(255),vehicle_meter INT,monthpayment NVARCHAR(255)
                                                       )
                                                            '''
                              cursor.execute(create_table_query)
                              conn.commit()
                         except:
                              if allocations == 'True':
                                   fuel_cal(chassis_number,current_car_owner,recivie_date,vehicle_meter)
                              else:
                                   delete_query = '''DELETE FROM dbo.fuel_cal WHERE chassis_number = ?'''
                                   cursor.execute(delete_query, (chassis_number,))
                                   conn.commit()
                         st.success('تم اضافة المعلومات بنجاح')
          else:
               st.error("المركبة غير مسجلة")


# search_vehicle
def search_vehicle_info(search_number):
     st.markdown(
                    """
                    <style>
                    
                    .stButton {
                         display: flex;
                         justify-content: flex-end;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                    )    
     if search_number == '':
          st.error('ادخل رقم المركبة')
     else:
          if len(search_number) <= 6:
               chassis_number = num_to_chassis(search_number)
          else:
               chassis_number = search_number
          check_query = '''
               SELECT COUNT(*) FROM dbo.newcar 
               WHERE chassis_number = ?
                    '''
          cursor.execute(check_query, (chassis_number,))
          count = cursor.fetchone()[0]
          if count > 0:
               fetch_query = "SELECT * FROM newcar WHERE chassis_number = ?"
               cursor.execute(fetch_query, (chassis_number,))
               result = cursor.fetchone()
               car_info_row = list(result)

               try:
                    fetch_handover_query = "SELECT * FROM handover WHERE chassis_number = ?"
                    cursor.execute(fetch_handover_query, (chassis_number,))
                    result = cursor.fetchone()
               except:
                    result = None
               if result is not None:
                    handover_info_row = list(result)
                    try:
                         fetch_malf_query =f"SELECT malfunctions FROM dbo.{handover_info_row[7]} WHERE current_car_owner = ?"
                         cursor.execute(fetch_malf_query, (handover_info_row[1],))
                         result = cursor.fetchall()
                         #malfun_info_row = list(result)
                         if result is not None:
                              malfun_info_row = list(result)
                    except:
                         malfun_info_row = "لا يوجد"
                    
                    if handover_info_row[5] == 'True':
                         alloca = "يوجد تخصيص"
                    else:
                         alloca = "لا يوجد تخصيص"
    
               else:
                    handover_info_row = ['لا يوجد'] * 11
                    malfun_info_row = "لا يوجد"
                    alloca = "لا يوجد تخصيص"
               # def your_function():
               #      destination_dir = f"E://python_projects//{car_info_row[15]}"
               #      os.startfile(destination_dir)
               destination_dir = f"E://python_projects//{car_info_row[15]}"
               os.startfile(destination_dir)
               fircol1, fircol2, fircol3, fircol4 = st.columns([1,1,1,1])
               with fircol4:
                    st.markdown(f"<div style='text-align: right; margin-bottom: 20px; border: 2px solid #FFC300; padding: 5px; border-radius: 5px; color: #green;'>مستلم المركبة الحالي : <span style = 'color: green'>{car_info_row[14]}</span></div>", unsafe_allow_html=True)
               with fircol3:
                    st.markdown(f"<div style='text-align: right; margin-bottom: 20px; border: 2px solid #FFC300; padding: 5px; border-radius: 5px; color: #green;'>العنوان الوظيفي : <span style = 'color: green'>{handover_info_row[2]}</span></div>", unsafe_allow_html=True)     
               with fircol2:
                    st.markdown(f"<div style='text-align: right; margin-bottom: 20px; border: 2px solid #FFC300; padding: 5px; border-radius: 5px; color: #green;'>الدائرة : <span style = 'color: green'>{handover_info_row[9]}</span></div>", unsafe_allow_html=True)
               with fircol1:
                    st.markdown(f"<div style='text-align: right; margin-bottom: 20px; border: 2px solid #FFC300; padding: 5px; border-radius: 5px; color: #green;'>القسم : <span style = 'color: green'>{handover_info_row[10]}</span></div>", unsafe_allow_html=True)
               col1, col2, col3, col4 = st.columns([1,1,1,1])
               with col4:
                    st.markdown(f"<div style='text-align: right; border: 2px solid #FFC300; padding: 5px; border-radius: 5px; color: #green;'>رقم الشاصي : <span style = 'color: green'>{car_info_row[0]}</span></div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='text-align: right; margin-top: 20px; border: 2px solid #FFC300; padding: 5px; border-radius: 5px; color: #green;'>الطراز : <span style = 'color: green'>{car_info_row[4]}</span></div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='text-align: right; margin-top: 20px; border: 2px solid #FFC300; padding: 5px; border-radius: 5px; color: #green;'>عدد الأسطوانات  : <span style = 'color: green'>{car_info_row[8]}</span></div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='text-align: right; margin-top: 20px; border: 2px solid #FFC300; padding: 5px; border-radius: 5px; color: #green;'>مسجل المركبة  : <span style = 'color: green'>{car_info_row[12]}</span></div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='text-align: right; margin-top: 20px; border: 2px solid #FFC300; padding: 5px; border-radius: 5px; color: #green;'>تاريخ الكتاب : <span style = 'color: green'>{handover_info_row[4]}</span></div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='text-align: right; margin-top: 20px; border: 2px solid #FFC300; padding: 5px; border-radius: 5px; color: #green;'>جهة الأستلام : <span style = 'color: green'>{car_info_row[16]}</span></div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='text-align: right; margin-top: 20px; border: 2px solid #FFC300; padding: 5px; border-radius: 5px; color: #green;'>الملاحظات : <span style = 'color: green'>{car_info_row[17]}</span></div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='text-align: right; margin-top: 20px; color: #green'>العوارض : <span style = 'color: green'>{malfun_info_row}</span></div>", unsafe_allow_html=True)            
                    #folder_button = col4.button('عرض الأوليات')              
               with col3:
                    st.markdown(f"<div style='text-align: right; border: 2px solid #FFC300; padding: 5px; border-radius: 5px; color: #green;'>اسم المركبة : <span style = 'color: green'>{car_info_row[1]}</span></div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='text-align: right; margin-top: 20px; border: 2px solid #FFC300; padding: 5px; border-radius: 5px; color: #green;'>الموديل : <span style = 'color: green'>{car_info_row[5]}</span></div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='text-align: right; margin-top: 20px; border: 2px solid #FFC300; padding: 5px; border-radius: 5px; color: #green;'>نوع الوقود : <span style = 'color: green'>{car_info_row[9]}</span></div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='text-align: right; margin-top: 20px; border: 2px solid #FFC300; padding: 5px; border-radius: 5px; color: #green;'>نوع المركبة : <span style = 'color: green'>{car_info_row[13]}</span></div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='text-align: right; margin-top: 20px; border: 2px solid #FFC300; padding: 5px; border-radius: 5px; color: #green;'>تاريخ التسليم : <span style = 'color: green'>{handover_info_row[5]}</span></div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='text-align: right; margin-top: 20px; border: 2px solid #FFC300; padding: 5px; border-radius: 5px; color: #green;'>نوع ناقل الحركة : <span style = 'color: green'>{car_info_row[18]}</span></div>", unsafe_allow_html=True)
               with col2:
                    st.markdown(f"<div style='text-align: right; border: 2px solid #FFC300; padding: 5px; border-radius: 5px; color: #green;'>رقم المركبة : <span style = 'color: green'>{car_info_row[2]}</span></div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='text-align: right; margin-top: 20px; border: 2px solid #FFC300; padding: 5px; border-radius: 5px; color: #green;'>المحافظة : <span style = 'color: green'>{car_info_row[6]}</span></div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='text-align: right; margin-top: 20px; border: 2px solid #FFC300; padding: 5px; border-radius: 5px; color: #green;'>لون المركبة : <span style = 'color: green'>{car_info_row[10]}</span></div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='text-align: right; margin-top: 20px; border: 2px solid #FFC300; padding: 5px; border-radius: 5px; color: #green;'>التخصيص :<span style = 'color: green'>{alloca}</span></div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='text-align: right; margin-top: 20px; border: 2px solid #FFC300; padding: 5px; border-radius: 5px; color: #green;'>رقم السنوية : <span style = 'color: green'>{car_info_row[3]}</span></div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='text-align: right; margin-top: 20px; border: 2px solid #FFC300; padding: 5px; border-radius: 5px; color: #green;'>نوع التسجيل : <span style = 'color: green'>{car_info_row[19]}</span></div>", unsafe_allow_html=True)
               with col1:
                    st.markdown(f"<div style='text-align: right; border: 2px solid #FFC300; padding: 5px; border-radius: 5px; color: #green;'>محافظة المركبة : <span style = 'color: green'>{car_info_row[7]}</span></div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='text-align: right; margin-top: 20px; border: 2px solid #FFC300; padding: 5px; border-radius: 5px; color: #green;'>نوع الاستلام : <span style = 'color: green'>{car_info_row[11]}</span></div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='text-align: right; margin-top: 20px; border: 2px solid #FFC300; padding: 5px; border-radius: 5px; color: #green;'>رقم الكتاب : <span style = 'color: green'>{handover_info_row[3]}</span></div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='text-align: right; margin-top: 20px; border: 2px solid #FFC300; padding: 5px; border-radius: 5px; color: #green;'>عداد المركبة : <span style = 'color: green'>{handover_info_row[8]}</span></div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='text-align: right; margin-top: 20px; border: 2px solid #FFC300; padding: 5px; border-radius: 5px; color: #green;'>رقم الضبارة : <span style = 'color: green'>{car_info_row[15]}</span></div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='text-align: right; margin-top: 20px; border: 2px solid #FFC300; padding: 5px; border-radius: 5px; color: #green;'>نوع لوحة المركبة : <span style = 'color: green'>{car_info_row[20]}</span></div>", unsafe_allow_html=True)

               st.markdown(f"<div style='text-align: right; margin-top: 20px; color: #FFC300'>---------------------------------------------------------------------------------------------------------------------------------------------</div>", unsafe_allow_html=True)

               try:
                    fetch_handoverarchive_query = "SELECT * FROM handoverarchive WHERE chassis_number = ?"
                    cursor.execute(fetch_handoverarchive_query, (chassis_number,))
                    result = cursor.fetchall()
                    handoverarchive_info = list(result)
                    
                    if handoverarchive_info:
                         st.markdown("<div style='text-align: right; margin-top: 20px; color: #green;'>: مستلمي المركبة السابقين</div>", unsafe_allow_html=True)
                         
                         for row in handoverarchive_info:
                              seccol1, seccol2, seccol3, seccol4 = st.columns([1,1,1,1])
                              name = row[1]
                              position = row[2]
                              docunum = row[3]
                              docdate = row[4]
                              reciviedata = row[5]
                              allocation = row[6]
                              meter = row[8]
                              try:
                                   fetch_malf_query =f"SELECT malfunctions FROM dbo.{row[7]} WHERE current_car_owner = ?"
                                   cursor.execute(fetch_malf_query, (name,))
                                   result = cursor.fetchall()
                                   #malfun_info_row = list(result)
                                   if result is not None:
                                        malfun_info_row = list(result)
                              except:
                                   malfun_info_row = "لا يوجد"
                              if allocation == 'True':
                                   alloca = "يوجد تخصيص"
                              else:
                                   alloca = "لا يوجد تخصيص"
                              with seccol4:
                                   st.markdown(f"<div style='text-align: right; margin-top: 20px; border: 2px solid #FFC300; padding: 5px; border-radius: 5px; color: #green;'>الأسم : <span style = 'color: green'>{name}</span></div>", unsafe_allow_html=True)
                                   st.markdown(f"<div style='text-align: right; margin-top: 20px; border: 2px solid #FFC300; padding: 5px; border-radius: 5px; color: #green;'>التخصيص :<span style = 'color: green'>{alloca}</span></div>", unsafe_allow_html=True)
                                   st.markdown(f"<div style='text-align: right; margin-top: 20px; color: #green'>العوارض : <span style = 'color: green'>{malfun_info_row}</span></div>", unsafe_allow_html=True)
                              with seccol3:
                                   st.markdown(f"<div style='text-align: right; margin-top: 20px; border: 2px solid #FFC300; padding: 5px; border-radius: 5px; color: #green;'>العنوان الوظيفي : <span style = 'color: green'>{position}</span></div>", unsafe_allow_html=True)
                                   st.markdown(f"<div style='text-align: right; margin-top: 20px; border: 2px solid #FFC300; padding: 5px; border-radius: 5px; color: #green;'>رقم الكتاب : <span style = 'color: green'>{docunum}</span></div>", unsafe_allow_html=True)
                              with seccol2:
                                   st.markdown(f"<div style='text-align: right; margin-top: 20px; border: 2px solid #FFC300; padding: 5px; border-radius: 5px; color: #green;'>عداد المركبة : <span style = 'color: green'>{meter}</span></div>", unsafe_allow_html=True)
                                   st.markdown(f"<div style='text-align: right; margin-top: 20px; border: 2px solid #FFC300; padding: 5px; border-radius: 5px; color: #green;'>تاريخ الكتاب : <span style = 'color: green'>{docdate}</span></div>", unsafe_allow_html=True)
                              with seccol1:
                                   st.markdown(f"<div style='text-align: right; margin-top: 20px; border: 2px solid #FFC300; padding: 5px; border-radius: 5px; color: #green;'>تاريخ التسليم : <span style = 'color: green'>{reciviedata}</span></div>", unsafe_allow_html=True)
                              st.markdown(f"<div style='text-align: right; margin-top: 20px; color: #FFC300'>---------------------------------------------------------------------------------------------------------------------------------------------</div>", unsafe_allow_html=True)
                    else:
                         st.markdown("<div style='text-align: right; margin-top: 20px; color: #green;'>لا يوجد مستلم سابق للمركبة</div>", unsafe_allow_html=True)
               except:
                    st.markdown("<div style='text-align: right; margin-top: 20px; color: #green;'>لا يوجد مستلم سابق للمركبة</div>", unsafe_allow_html=True)

          else:
               st.error("المركبة غير مسجلة")
          
          




# handover edit function
def editoptions(id_number):
     if id_number == '':
          st.error("ادخل رقم المركبة")
     else:
          if len(id_number) <= 6:
               chassis_number = num_to_chassis(id_number)
          else:
               chassis_number = id_number
          fetch_query = "SELECT * FROM handover WHERE chassis_number = ?"
          cursor.execute(fetch_query, (chassis_number,))
          result = cursor.fetchone()
          row_list = list(result)
          car_owner = row_list[1]
          malf = row_list[6]
          fetch_malfunctions_query = f"SELECT * FROM dbo.{malf} WHERE current_car_owner = ?"
          cursor.execute(fetch_malfunctions_query, (car_owner,))
          result = cursor.fetchone()
          malfuninfo = list(result)
          return row_list,malfuninfo     


#Fuel Committee
def fuel_data():
     fetch_fuel_query = "SELECT * FROM fuel_cal;"
     df = pd.read_sql(fetch_fuel_query, conn)
     return df

#info_ page function
def allcars():
     with conn.cursor() as cursor:
          cursor.execute("""
            IF OBJECT_ID('infoT', 'U') IS NOT NULL
            DROP TABLE infoT;
               """)

    # Create the infoT table without default values
          cursor.execute("""
            CREATE TABLE infoT (
            chassis_number NVARCHAR(255),
            fulcarnumber NVARCHAR(255),
            type_option NVARCHAR(255),
            model_option NVARCHAR(255),
            date_option NVARCHAR(255),
            allocations NVARCHAR(255),
            department NVARCHAR(255),
            section NVARCHAR(255),
            car_owner NVARCHAR(255),
            receive_type NVARCHAR(255),
            fromrec NVARCHAR(255),
            notes NVARCHAR(255),
            gearstick NVARCHAR(255),
            registerationtype NVARCHAR(255),
            carnumbertype NVARCHAR(255)
        );
    """)

          try:
               cursor.execute("""
               INSERT INTO infoT (chassis_number, fulcarnumber, type_option, model_option, date_option, allocations, department, section, car_owner, receive_type, fromrec, notes, gearstick,registerationtype,carnumbertype)
               SELECT 
               n.chassis_number,
               n.fulcarnumber,
               n.type_option,
               n.model_option,
               n.date_option,
               COALESCE(h.allocations, N'لا يوجد') AS allocations,
               COALESCE(h.department, N'لا يوجد') AS department,
               COALESCE(h.section, N'لا يوجد') AS section,
               n.car_owner,
               n.receive_type,
               n.fromrec, 
               n.notes,
               n.gearstick,
               n.registerationtype,
               n.carnumbertype
               FROM newcar n
               LEFT JOIN handover h ON n.chassis_number = h.chassis_number;
               """)

               conn.commit()
          except:
               cursor.execute("""
               INSERT INTO infoT (chassis_number, fulcarnumber, type_option, model_option, date_option, allocations, department, section, car_owner, receive_type,fromrec,notes,gearstick,registerationtype,carnumbertype)
               SELECT 
               n.chassis_number,
               n.fulcarnumber,
               n.type_option,
               n.model_option,
               n.date_option,
               N'لا يوجد' AS allocations,
               N'لا يوجد' AS department,
               N'لا يوجد' AS section,
               n.car_owner,
               n.receive_type,
               n.fromrec, 
               n.notes,
               n.gearstick,
               n.registerationtype,
               n.carnumbertype
               FROM newcar n
               """)

               conn.commit()


     fetch_fuel_query = "SELECT * FROM infoT;"
     df = pd.read_sql(fetch_fuel_query, conn)
     df['allocations'] = df['allocations'].map({'True': 'تخصيص', 'False': 'بدون تخصيص', 'لا يوجد': 'لا يوجد'})    
     return df

def info_to_edit(chassis_number):
     if chassis_number == '':
          pass
     elif already_exists_chassis(chassis_number):
          st.error('المركبة غير مسجلة')
     else:
          select_query = 'SELECT * FROM newcar WHERE chassis_number = ?'
          cursor.execute(select_query, (chassis_number,))
          rows = cursor.fetchall()
          row = rows[0]
          conn.commit()
          split_result = re.match(r'(\D+)(\d+)', row[2])
          character_car = split_result.group(1) 
          number_car = split_result.group(2)    

          split_result = re.match(r'(\D+)(\d+)', row[3])
          character_annual = split_result.group(1) 
          number_annual = split_result.group(2)    

          typeop = typeoption() # type: ignore
          cylindersop = cylindersoption() # type: ignore
          fuelop = fueloption() # type: ignore
          cartypeop = cartypeoption() # type: ignore
          governoratesop = governoratesoption() # type: ignore
          colorop = coloroption() # type: ignore
          carlettersop = carlettersoption() # type: ignore
          lettersop = lettersoption() # type: ignore
          fromrecop = fromrecoption() # type: ignore
          registerationtypeop = registerationtypeoption() # type: ignore
          receive_typeop = receive_typeoption() # type: ignore
          current_year = datetime.datetime.now().year
          start_year = 1899
          year_range = list(range(start_year, current_year + 1))
          year_range.append(1)
          year_string = row[5]
          year_value = int(year_string)
          year_index = year_range.index(year_value)
          if character_car == '_':
               character_car = 'لا يوجد'

          st.markdown(
                    """
                    <style>
                    .stForm {
                         border: none !important;
                         box-shadow: none !important;
                         }
                    .stSelectbox label {
                         text-align: right;
                         display: block;
                         }
                    
                    </style>
                    """,
                    unsafe_allow_html=True
                         )
          fircol1, fircol2 = st.columns(2)
          type_option = fircol2.selectbox("اسم المركبة", typeop, key='type_option',index=typeop.index(row[1]))
          modelop = modeloption(type_option) # type: ignore
          default_model_index = 0  # Fallback default index
          if row[4] in modelop:
               default_model_index = modelop.index(row[4])

          with st.form(key='edit_vehicle_form', clear_on_submit=True):
               st.markdown(
                    """
                    <style>
                    .stForm {
                         border: none !important;
                         box-shadow: none !important;
                         }
                    .stSelectbox label {
                         text-align: right;
                         display: block;
                         }
                    .stTextInput label {
                         text-align: right;
                         display: block;
                         }
                    </style>
                    """,
                    unsafe_allow_html=True
                         )
               col1, col2 = st.columns(2)
               model_option = col2.selectbox("الطراز", modelop, key='model_option',index=default_model_index)
               date_option = col1.selectbox("موديل المركبة",year_range, key='date_option',index=year_index)
               cylinders_option = col2.selectbox("عدد الأسطوانات", cylindersop, key='cylinders_option',index=cylindersop.index(row[8]))
               fuel_option = col1.selectbox("نوع الوقود", fuelop, key='fuel_option',index=fuelop.index(row[9]))
               cartype_option = col2.selectbox("نوع المركبة", cartypeop, key='cartype_option',index=cartypeop.index(row[13]))
               governorates_option = col1.selectbox("اسم المحافظة", governoratesop, key='governorates_option',index=governoratesop.index(row[6]))
               cargovernorates_option = col2.selectbox("محافظة المركبة", governoratesop, key='cargovernorates_option',index=governoratesop.index(row[7]))
               color_option = col1.selectbox("لون المركبة", colorop, key='color_option',index=colorop.index(row[10]))
               registerationtype = col2.selectbox("نوع التسجيل", registerationtypeop, key='registerationtype',index=registerationtypeop.index(row[19]))
               numbertypes = ['الماني','قديم','جديد']
               carnumbertype = col1.radio('نوع لوحة المركبة',numbertypes, key='carnumbertype',index=numbertypes.index(row[20]))
               #second widget with 4 columns
               seccol1, seccol2,seccol3,seccol4=st.columns(4,vertical_alignment="bottom")
               letter_carnumber = seccol1.selectbox("", carlettersop, key='letter_carnumber',index=carlettersop.index(character_car))
               carnumber = seccol2.text_input("رقم المركبة", key='carnumber', value=number_car)
               letter_annualnumber = seccol3.selectbox("", lettersop, key='letter_annualnumber',index=lettersop.index(character_annual))
               annualnumber = seccol4.text_input("رقم السنوية", key='annualnumber', value=number_annual)
               #receives = ['اهداء','اعارة','شركة عامة']
               #receive_type =  st.radio("نوع الأتسلام",receives, key='receive_type',index=receives.index(row[11]))
               thircol1, thircol2,thircol3,thircol4=st.columns(4,vertical_alignment="bottom")
               gears = ['اوتماتيك','يدوي']
               gearstick =  thircol1.radio("نوع ناقل الحركة",gears, key='gearstick',index=gears.index(row[18]))
               receive_type =  thircol4.selectbox("نوع الأتسلام",receive_typeop, key='receive_type',index=receive_typeop.index(row[11]))
               fromrec = thircol3.selectbox("جهة الأهداء او الأعارة",fromrecop,key="fromrec",index=fromrecop.index(row[16]))
               notes = thircol2.text_input("الملاحظات", key='notes',value=row[17])
               variables = [type_option,model_option,date_option,cylinders_option,
                              fuel_option,cartype_option,governorates_option,cargovernorates_option,color_option,
                              chassis_number,letter_carnumber,carnumber,letter_annualnumber,annualnumber, receive_type,
                              fromrec, notes,gearstick,registerationtype,carnumbertype]
               
               forcol1, forcol2, forcol3, forcol4, forcol5, forcol6= st.columns(6)
               st.markdown(
                    """
                    <style>
                    .stFormSubmitButton {
                         display: flex;
                         justify-content: flex-end;
                    }
                    .stButton {
                         display: flex;
                         justify-content: flex-end;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                    )
               submit_button = forcol6.form_submit_button("تعديل")
          st.markdown(
                    """
                    <style>
                    .align-right {
                         text-align: right;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                    )

               
          st.markdown('<div class="align-right">اضافة اوليات للمركبة</div>', unsafe_allow_html=True)
          uploaded_files = st.file_uploader("", type=["pdf"], accept_multiple_files= True)
               
          if submit_button:
               if any(item == '' for item in variables):
                    st.error("يجب ملئ كافة المعلومات")
               else:
                    destination_dir = f"E://python_projects//{row[15]}"

                    if not os.path.exists(destination_dir):
                         os.makedirs(destination_dir)

                    if uploaded_files:
                         for uploaded_file in uploaded_files:
                              # Determine the new file name
                              existing_files = os.listdir(destination_dir)
                              pdf_numbers = []
                              
                              for file in existing_files:
                                   if file.endswith('.pdf'):
                                        try:
                                             number = int(os.path.splitext(file)[0])
                                             pdf_numbers.append(number)
                                        except ValueError:
                                             continue

                              if pdf_numbers:
                                   biggest_number = max(pdf_numbers)
                                   newfile_number = biggest_number + 1
                              else:
                                   newfile_number = 0

                              newfile_name = str(newfile_number) + '.pdf'
                              file_path = os.path.join(destination_dir, newfile_name)
                              
                              # Write the uploaded file
                              with open(file_path, "wb") as f:
                                   f.write(uploaded_file.getbuffer())
                                   
                         # Open the directory after processing all files
                         os.startfile(destination_dir)
                              

                    
               update_execution(*variables)
               st.markdown(
               """
               <style>
               .element-container {
                    display: flex;
                    justify-content: flex-end;
               }
               .stSuccess {
                    text-align: right;
               }
               </style>
               """,
               unsafe_allow_html=True
               )

               # Adjusting the success message container
               st.markdown('<div class="element-container">', unsafe_allow_html=True)
               st.success('تم تعديل المعلومات')
               action = 'edited a vehicle info'
               userlog(action) # type: ignore
               st.markdown('</div>', unsafe_allow_html=True)

def update_execution(*v):
     type_option = str(v[0])
     model_option = str(v[1])
     date_option = str(v[2])
     cylinders_option = str(v[3])
     fuel_option = str(v[4])
     cartype_option = str(v[5])
     governorates_option = str(v[6])
     cargovernorates_option = str(v[7])
     color_option = str(v[8])
     chassis_number = str(v[9])
     letter_carnumber = str(v[10])
     carnumber = str(v[11])
     letter_annualnumber = str(v[12])
     annualnumber = str(v[13])
     receive_type = str(v[14])
     fromrec = str(v[15])
     notes = str(v[16])
     gearstick = str(v[17])
     registerationtype = str(v[18])
     carnumbertype = str(v[19])
     if letter_carnumber == 'لا يوجد':
          letter_carnumber = '_'

     sql_update = """
               UPDATE dbo.newcar
               SET type_option = ?, 
                    model_option = ?, 
                    date_option = ?, 
                    cylinders_option = ?, 
                    fuel_option = ?, 
                    cartype_option = ?, 
                    governorates_option = ?, 
                    cargovernorates_option = ?, 
                    color_option = ?, 
                    fulcarnumber =  ?, 
                    fulannualnumber = ?, 
                    receive_type = ?,
                    fromrec = ?,
                    notes = ?,
                    gearstick = ?,
                    registerationtype = ?,
                    carnumbertype = ?
               WHERE chassis_number = ?
               """
     fulcarnumber = letter_carnumber+carnumber
     fulannualnumber =  letter_annualnumber+annualnumber
    # Execute the update statement
     cursor.execute(sql_update, (type_option, model_option, date_option, cylinders_option,
                                 fuel_option, cartype_option, governorates_option,
                                 cargovernorates_option, color_option, fulcarnumber, fulannualnumber, 
                                 receive_type, fromrec, notes,gearstick,registerationtype,carnumbertype, chassis_number))
     conn.commit()


#add new functions
def addtype(typeoption,modeloption):

     check_query = '''
        SELECT model
        FROM typeoption
        WHERE type = ?
        '''
     cursor.execute(check_query, (typeoption,))
     result = cursor.fetchone()

     if result:
          model = result[0]

          check_model_query = f'''
          SELECT COUNT(*)
          FROM dbo.{model}
          WHERE model = ?
          '''

          cursor.execute(check_model_query, (modeloption,))
          model_exists = cursor.fetchone()[0]

          if model_exists > 0:
               pass
          else:
               insert_section_query = f'''
               INSERT INTO dbo.{model} (model)
               VALUES (?)
               '''
               cursor.execute(insert_section_query, (modeloption,))
               conn.commit()

     else:
          cursor.execute("SELECT COUNT(*) FROM typeoption")
          new_id = cursor.fetchone()[0] + 1
          model = f'model{new_id}'

          cursor.execute("INSERT INTO typeoption (type, model) VALUES (?, ?)",
                    (typeoption, model))
          conn.commit()

          create_table_query = f'''
                                        CREATE TABLE dbo.{model} (
                                        model NVARCHAR(255)
                                                                 )
                                                                      '''
          cursor.execute(create_table_query)
          conn.commit()
          insert_section_query = f'''
               INSERT INTO dbo.{model} (model)
               VALUES (?)
               '''
          cursor.execute(insert_section_query, (modeloption,))
          conn.commit()
    

def adddepar(departmentoption,sectionoption):
     check_query = '''
        SELECT section
        FROM departmentoptions
        WHERE department = ?
        '''
     cursor.execute(check_query, (departmentoption,))
     result = cursor.fetchone()

     if result:
          section = result[0]

          check_section_query = f'''
          SELECT COUNT(*)
          FROM dbo.{section}
          WHERE section = ?
          '''

          cursor.execute(check_section_query, (sectionoption,))
          section_exists = cursor.fetchone()[0]

          if section_exists > 0:
               pass
          else:
               insert_section_query = f'''
               INSERT INTO dbo.{section} (section)
               VALUES (?)
               '''
               cursor.execute(insert_section_query, (sectionoption,))
               conn.commit()

     else:
          cursor.execute("SELECT COUNT(*) FROM departmentoptions")
          new_id = cursor.fetchone()[0] + 1
          section = f'section{new_id}'

          cursor.execute("INSERT INTO departmentoptions (department, section) VALUES (?, ?)",
                    (departmentoption, section))
          conn.commit()

          create_table_query = f'''
                                        CREATE TABLE dbo.{section} (
                                        section NVARCHAR(255)
                                                                 )
                                                                      '''
          cursor.execute(create_table_query)
          conn.commit()
          insert_section_query = f'''
               INSERT INTO dbo.{section} (section)
               VALUES (?)
               '''
          cursor.execute(insert_section_query, (sectionoption,))
          conn.commit()


def addposition(positionoption):
     check_position_query = f'''
          SELECT COUNT(*)
          FROM dbo.position
          WHERE account = ?
          '''

     cursor.execute(check_position_query, (positionoption,))
     pos_exists = cursor.fetchone()[0]
     if pos_exists > 0:
          pass
     else:
          insert_position_query = f'''
               INSERT INTO dbo.position (account)
               VALUES (?)
               '''
          cursor.execute(insert_position_query, (positionoption,))
          conn.commit()


def addmalfunc(malfunctionoption):
     check_malf_query = f'''
          SELECT COUNT(*)
          FROM dbo.malfunctionsoptions
          WHERE malfunctions = ?
          '''

     cursor.execute(check_malf_query, (malfunctionoption,))
     malf_exists = cursor.fetchone()[0]
     if malf_exists > 0:
          pass
     else:
          insert_malf_query = f'''
               INSERT INTO dbo.malfunctionsoptions (malfunctions)
               VALUES (?)
               '''
          cursor.execute(insert_malf_query, (malfunctionoption,))
          conn.commit()


def addregisterty(registertypesoption):
     check_addregistertypes_query = f'''
          SELECT COUNT(*)
          FROM dbo.registerationt
          WHERE registeration = ?
          '''

     cursor.execute(check_addregistertypes_query, (registertypesoption,))
     malf_exists = cursor.fetchone()[0]
     if malf_exists > 0:
          pass
     else:
          insert_addregistertypes_query = f'''
               INSERT INTO dbo.registerationt (registeration)
               VALUES (?)
               '''
          cursor.execute(insert_addregistertypes_query, (registertypesoption,))
          conn.commit()

def addcolor(color):
     check_color_query = f'''
          SELECT COUNT(*)
          FROM dbo.coloroption
          WHERE color = ?
          '''

     cursor.execute(check_color_query, (color,))
     malf_exists = cursor.fetchone()[0]
     if malf_exists > 0:
          pass
     else:
          insert_color_query = f'''
               INSERT INTO dbo.coloroption (color)
               VALUES (?)
               '''
          cursor.execute(insert_color_query, (color,))
          conn.commit()

def addfromrec(fromoption):
     check_rec_query = f'''
          SELECT COUNT(*)
          FROM dbo.fromreceiving
          WHERE fromrec = ?
          '''

     cursor.execute(check_rec_query, (fromoption,))
     malf_exists = cursor.fetchone()[0]
     if malf_exists > 0:
          pass
     else:
          insert_rec_query = f'''
               INSERT INTO dbo.fromreceiving (fromrec)
               VALUES (?)
               '''
          cursor.execute(insert_rec_query, (fromoption,))
          conn.commit()


#pdf report
def create_table_pdf(template_pdf, html_table, infout):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(letter))
    width, height = landscape(letter)  # Page size dimensions (letter)
    
    # Header image
    header_image_path = "E:/python_projects/header2.png"
    header_width = 700
    header_height = 150
    header_x = (width - header_width) / 2
    header_y = height - header_height - 10  # Just below the top margin
    c.drawImage(header_image_path, header_x, header_y, width=header_width, height=header_height)
    
    # Footer image
    footer_image_path = "E:/python_projects/footer2.png"
    footer_width = 700
    footer_height = 70
    footer_x = (width - footer_width) / 2
    footer_y = 10  # 10 units from the bottom of the page
    c.drawImage(footer_image_path, footer_x, footer_y, width=footer_width, height=footer_height)

    # Register font
    pdfmetrics.registerFont(TTFont('TRADITIONAL-ARABIC', 'E:/python_projects/trado.TTF'))

    # Parse the HTML table
    soup = BeautifulSoup(html_table, 'html.parser')
    rows = []
    for row in soup.find_all('tr'):
        cols = row.find_all(['td', 'th'])
        cols = [col.get_text() for col in cols]
        rows.append(cols)

    # Set up the table layout
    padding = 2  # Cell padding
    row_height = 18  # Row height
    x_start = 40
    y_start = height - header_height - 30  # Start Y position after header
    
    # Calculate column widths
    col_widths = [0] * len(rows[0])
    for row in rows:
        for col_num, cell in enumerate(row):
            reshaped_cell = arabic_reshaper.reshape(cell)
            display_cell = get_display(reshaped_cell)
            # Calculate the width of the cell's content
            text_width = c.stringWidth(display_cell, "TRADITIONAL-ARABIC", 10) + 2 * padding
            if text_width > col_widths[col_num]:
                col_widths[col_num] = text_width
          #   if text_width > 70:
          #       col_widths[col_num] = 70
          #       row_height += 10

    current_y_pos = y_start
    for row_num, row in enumerate(rows):
        # Check if we need to create a new page
        if current_y_pos - row_height < footer_y + footer_height:
            c.showPage()  # Start a new page
            # Re-add the header image on the new page
            c.drawImage(header_image_path, header_x, header_y, width=header_width, height=header_height)
            c.drawImage(footer_image_path, footer_x, footer_y, width=footer_width, height=footer_height)
            
            current_y_pos = height - header_height - 30  # Reset Y position for new page

        # Adjust Y position for the row
        y_pos = current_y_pos - row_height  # Row Y position

        # Determine if this is the first row (header row)
        is_header_row = (row_num == 0)

        for col_num, cell in enumerate(row):
            reshaped_cell = arabic_reshaper.reshape(cell)
            display_cell = get_display(reshaped_cell)

            # If it's the header row, set a background color
            if is_header_row:
                c.setFillColor(HexColor("#808080"))  # Set the header background color
                c.setFont("TRADITIONAL-ARABIC", 10)  # Use a bold font for the header text
            else:
                c.setFillColor(HexColor("#FFFFFF"))  # White for other rows
                c.setFont("TRADITIONAL-ARABIC", 10)  # Regular font for data rows

            # Draw the cell border (with adjusted column width)
            c.rect(x_start + sum(col_widths[:col_num]), y_pos, col_widths[col_num], row_height, fill=1)

            # Center the text horizontally and vertically
            text_width = c.stringWidth(display_cell, "TRADITIONAL-ARABIC", 10)
          #   if text_width > 70:
          #        text_width = 70
            x_pos = x_start + sum(col_widths[:col_num]) + (col_widths[col_num] - text_width) / 2  # Centered horizontally
            y_pos_centered = y_pos + (row_height - 8) / 2  # Centered vertically (8 is font size)

            # Draw the text in the cell----------------------------------------
            style = getSampleStyleSheet()['Normal']
            style.fontName = 'TRADITIONAL-ARABIC'
            style.fontSize = 10
            max_width = 300
            style.textColor = colors.black            
          
            
            textw = c.stringWidth(display_cell, "TRADITIONAL-ARABIC", 10) + 2 * padding
            paragraph = Paragraph(display_cell, style)
          #   if textw > 70:
          #       middle_index = len(display_cell) // 2
          #       first_half = display_cell[:middle_index]
          #       second_half = display_cell[middle_index:]
          #       reversed_text = second_half+ " " + first_half

          #       #reversed_text = display_cell[::-1]
          #       paragraph = Paragraph(reversed_text, style)
          #   else:
          #        paragraph = Paragraph(display_cell, style)


            # Use Paragraph to handle text wrapping
            #paragraph = Paragraph(display_cell, style)          
            # Draw the wrapped text as a Paragraph object
            paragraph_width, paragraph_height = paragraph.wrap(max_width, 1000)
            paragraph.drawOn(c, x_pos, y_pos_centered)
            #c.setFillColor(HexColor("#000000"))
            #c.drawString(x_pos, y_pos_centered, display_cell)

        current_y_pos = y_pos  # Update current Y position after printing the row

    # Draw the footer image on the last page
    c.drawImage(footer_image_path, footer_x, footer_y, width=footer_width, height=footer_height)
    
    if current_y_pos - footer_height < footer_y:
            c.showPage()  # Start a new page to accommodate the footer
            # Re-add the header image
            c.drawImage(header_image_path, header_x, header_y, width=header_width, height=header_height)
            current_y_pos = height - header_height - 30  # Reset Y position for new page
        
        # Draw the footer image on the page
    c.drawImage(footer_image_path, footer_x, footer_y, width=footer_width, height=footer_height)

    # Save the PDF
    c.save()
    pdf_data = buffer.getvalue()
    buffer.close()
    return pdf_data

def create_table_pdf2(template_pdf, html_table, infout):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(letter))
    width, height = landscape(letter)  # Page size dimensions (letter)
    
    # Header image
    header_image_path = "E:/python_projects/header2.png"
    header_width = 700
    header_height = 150
    header_x = (width - header_width) / 2
    header_y = height - header_height - 10  # Just below the top margin
    c.drawImage(header_image_path, header_x, header_y, width=header_width, height=header_height)
    
    # Footer image
    footer_image_path = "E:/python_projects/footer2.png"
    footer_width = 700
    footer_height = 70
    footer_x = (width - footer_width) / 2
    footer_y = 10  # 10 units from the bottom of the page
    c.drawImage(footer_image_path, footer_x, footer_y, width=footer_width, height=footer_height)

    # Register font
    pdfmetrics.registerFont(TTFont('TRADITIONAL-ARABIC', 'E:/python_projects/trado.TTF'))

    # Parse the HTML table
    soup = BeautifulSoup(html_table, 'html.parser')
    rows = []
    for row in soup.find_all('tr'):
        cols = row.find_all(['td', 'th'])
        cols = [col.get_text() for col in cols]
        rows.append(cols)

    # Set up the table layout
    padding = 2  # Cell padding
    row_height = 18  # Row height
    x_start = 750
    y_start = height - header_height - 30  # Start Y position after header
    
    # Calculate column widths
    col_widths = [0] * len(rows[0])
    for row in rows:
        for col_num, cell in enumerate(row):
            reshaped_cell = arabic_reshaper.reshape(cell)
            display_cell = get_display(reshaped_cell)
            # Calculate the width of the cell's content
            text_width = c.stringWidth(display_cell, "TRADITIONAL-ARABIC", 10) + 2 * padding
            if text_width > col_widths[col_num]:
                col_widths[col_num] = text_width
          #   if text_width > 70:
          #       col_widths[col_num] = 70
          #       row_height += 10

    current_y_pos = y_start
    for row_num, row in enumerate(rows):
        # Check if we need to create a new page
        if current_y_pos - row_height < footer_y + footer_height:
            c.showPage()  # Start a new page
            # Re-add the header image on the new page
            c.drawImage(header_image_path, header_x, header_y, width=header_width, height=header_height)
            c.drawImage(footer_image_path, footer_x, footer_y, width=footer_width, height=footer_height)
            
            current_y_pos = height - header_height - 30  # Reset Y position for new page

        # Adjust Y position for the row
        y_pos = current_y_pos - row_height  # Row Y position

        # Determine if this is the first row (header row)
        is_header_row = (row_num == 0)

        for col_num, cell in enumerate(row):
            reshaped_cell = arabic_reshaper.reshape(cell)
            display_cell = get_display(reshaped_cell)

            # If it's the header row, set a background color
            if is_header_row:
                c.setFillColor(HexColor("#808080"))  # Set the header background color
                c.setFont("TRADITIONAL-ARABIC", 10)  # Use a bold font for the header text
            else:
                c.setFillColor(HexColor("#FFFFFF"))  # White for other rows
                c.setFont("TRADITIONAL-ARABIC", 10)  # Regular font for data rows

            # Draw the cell border (with adjusted column width)
            #c.rect(x_start + sum(col_widths[:col_num]), y_pos, col_widths[col_num], row_height, fill=1)
            c.rect(x_start - sum(col_widths[:col_num + 1]), y_pos, col_widths[col_num], row_height, fill=1)


            # Center the text horizontally and vertically
            text_width = c.stringWidth(display_cell, "TRADITIONAL-ARABIC", 10)
          #   if text_width > 70:
          #        text_width = 70
            x_pos = x_start - sum(col_widths[:col_num]) - (col_widths[col_num] + text_width) / 2  # Centered horizontally
            y_pos_centered = y_pos + (row_height - 8) / 2  # Centered vertically (8 is font size)

            # Draw the text in the cell----------------------------------------
            style = getSampleStyleSheet()['Normal']
            style.fontName = 'TRADITIONAL-ARABIC'
            style.fontSize = 10
            max_width = 300
            style.textColor = colors.black            
          
            
            textw = c.stringWidth(display_cell, "TRADITIONAL-ARABIC", 10) + 2 * padding
            paragraph = Paragraph(display_cell, style)
          #   if textw > 70:
          #       middle_index = len(display_cell) // 2
          #       first_half = display_cell[:middle_index]
          #       second_half = display_cell[middle_index:]
          #       reversed_text = second_half+ " " + first_half

          #       #reversed_text = display_cell[::-1]
          #       paragraph = Paragraph(reversed_text, style)
          #   else:
          #        paragraph = Paragraph(display_cell, style)


            # Use Paragraph to handle text wrapping
            #paragraph = Paragraph(display_cell, style)          
            # Draw the wrapped text as a Paragraph object
            paragraph_width, paragraph_height = paragraph.wrap(max_width, 1000)
            paragraph.drawOn(c, x_pos, y_pos_centered)
            #c.setFillColor(HexColor("#000000"))
            #c.drawString(x_pos, y_pos_centered, display_cell)

        current_y_pos = y_pos  # Update current Y position after printing the row

    # Draw the footer image on the last page
    c.drawImage(footer_image_path, footer_x, footer_y, width=footer_width, height=footer_height)
    
    if current_y_pos - footer_height < footer_y:
            c.showPage()  # Start a new page to accommodate the footer
            # Re-add the header image
            c.drawImage(header_image_path, header_x, header_y, width=header_width, height=header_height)
            current_y_pos = height - header_height - 30  # Reset Y position for new page
        
        # Draw the footer image on the page
    c.drawImage(footer_image_path, footer_x, footer_y, width=footer_width, height=footer_height)

    # Save the PDF
    c.save()
    pdf_data = buffer.getvalue()
    buffer.close()
    return pdf_data