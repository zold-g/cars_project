import streamlit as st
from thisone import *  # type: ignore
import pandas as pd
import datetime
import os
import uuid
import asyncio


#from st_on_hover_tabs import on_hover_tabs
#import importlib_metadata
#import st_on_hover_tabs

# Check for Streamlit version to include it in the PyInstaller build
# try:
#     version = importlib_metadata.version('streamlit')
# except importlib_metadata.PackageNotFoundError:
#     version = None


#streamlit run e:/python_projects/cars.py
# Login page
def login_page():
    
    st.markdown(
            """
            <style>
    #         .stApp {
    #      background-color: #ffffff; /* Set background color to white */
    #  }
            .stHeading {
            text-align: right;
            }
            .stTextInput label {
            text-align: right;
            display: block;
            }
            .stFormSubmitButton {
            display: flex;
            justify-content: flex-end;
            }
            .stTextInput input {
            text-align: right;
            }
            </style>
            """,
            unsafe_allow_html=True
            )
    #st.title("تسجيل الدخول")

    # create a form for username and password
    placeholder = st.empty()
    with placeholder.form(key='login_form'):
        st.title("تسجيل الدخول")
        username = st.text_input("اسم المستخدم")
        password = st.text_input("كلمة المرور", type="password")#, type="password"
        submit_button = st.form_submit_button("تسجيل")
    if submit_button:
            if check_credentials(username, password): # type: ignore
                placeholder.empty()
                st.session_state.logged_in = True
                main()
        # check the usernames and passwords
        # if submit_button:
        #     if check_credentials(username, password): # type: ignore
        #         placeholder.empty()
        #         st.session_state.logged_in = True

                #newww
                
                #st.session_state.username = username
                #st.session_state.password = password
                # cookie['logged_in'] = True
                # cookie.save()
                # cookie['username'] = username
                # cookie.save()
                # cookie['password'] = password
                # cookie.save()
                

            #else:
             #   st.error("يوجد خطأ في اسم المستخدم او كلمة المرور")



# Title page
def title_page():
    if autho() == 'admin': # type: ignore
        activities = ['🚗  المعلومات','📝  اضافة مركبة','✏️  تعديل المعلومات','🔑  استلام وتسليم المركبات','🔍  بحث','📮  حذف مركبة','⚙️  الأعدادات',' ⛽  لجنة الوقود'
                      ,'💬  اضافة معلومات','🏠  تسجيل الخروج']
        acticon = ['🚗', '📝', '✔','🔑','🔍','delete','⚙','⛽','💬','🏠']
    elif autho() == 'user': # type: ignore
        activities = ['🚗  المعلومات','📝  اضافة مركبة','🔍  بحث',' ⛽  لجنة الوقود','🏠  تسجيل الخروج']
        acticon = ['🚗','📝','🔍','⛽','🏠']
    else:
        activities = ['🚗  المعلومات','🔍  بحث','🏠  تسجيل الخروج']
        acticon = ['🚗','🔍','🏠']

    # the dropdown options
    #activities = ['المعلومات','اضافة مركبة','تعديل المعلومات','حذف مركبة']
    global choices
    #choices = st.sidebar.selectbox("",activities)
    st.markdown('<style>' + open('E:\python_projects/style.css').read() + '</style>', unsafe_allow_html=True)
 
    # with st.sidebar:
    #     activities = on_hover_tabs(tabName=activities,iconName=acticon,
    #                                styles = {'navtab': {'background-color':'#111',
    #                                               'color': '#818181',
    #                                               'font-size': '18px',
    #                                               'transition': '.3s',
    #                                               'white-space': 'nowrap',
    #                                               'text-transform': 'uppercase'},
    #                                    'tabStyle': {':hover :hover': {'color': 'red',
    #                                                                   'cursor': 'pointer'}},
    #                                 #    'tabStyle' : {'list-style-type': 'none',
    #                                 #                  'margin-bottom': '30px',
    #                                 #                  'padding-left': '30px'},
    #                                 #    'iconStyle':{'position':'fixed',
    #                                 #                 'left':'7.5px',
    #                                 #                 'text-align': 'left'},
    #                                    },
    #                          key="1",default_choice=0)
    
    # choices = activities
    st.markdown("""
    <style>
        .stRadio > div > label {
    color: white;
        div[role="listbox"] {
    color: white;
}
}
    </style>
""", unsafe_allow_html=True)

    choices = st.sidebar.radio("",activities)


    if choices == '🚗  المعلومات':
        info_page() 

    if choices == '📝  اضافة مركبة':
        add_vehicle()

    if choices == '✏️  تعديل المعلومات':
        edit_page()
    
    if choices == '🔑  استلام وتسليم المركبات':
        handover_vehicle()
    
    if choices == '🔍  بحث':
        search_vehicle()
    
    if choices == '📮  حذف مركبة':
        delete_vehicle()
    
    if choices == '⚙️  الأعدادات':
        settings()

    if choices == ' ⛽  لجنة الوقود':
        fuel()

    if choices == '💬  اضافة معلومات':
        add_new()

    if choices == '🏠  تسجيل الخروج':
        out()

# Information page
def info_page():
    
    st.markdown(
    """
    <style>
    # .st-emotion-cache-ue6h4q {
    # font-size: 14px;
    # color: rgb(211 214 228);}
    # .st-emotion-cache-1r4qj8v {
    # position: absolute;
    # background: rgb(255, 255, 255);
    # color: rgb(217 220 234);}
    # .h1 {
    # font-family: "Source Sans Pro", sans-serif;
    # font-weight: 700;
    # color: rgb(244 245 250);}
    #  .stApp {
    #      background-color: #0e1117; /* Set background color to white */
    #  }
    .st-emotion-cache-1jicfl2{
        padding : 0rem 1rem 10rem;
    }
    .logo-container {
        display: flex;
        justify-content: space-around;
        align-items: flex-end; /* Align items to the bottom */
        margin-top: 75px; /* Add space above the logos */
        margin-right: 75px; 
    }
    # .stRadio {
    #     display: flex;
    #     justify-content: flex-end;
    # }
    .seclogo-container {
        
        margin-right: 200px; 
    }
    .logo {
        height: 100px;
        margin-top: 300px; /* Set a fixed height */
    }
    

    </style>
    """,
    unsafe_allow_html=True
    )
    st.image("E:/python_projects/caption.png")   
    # Create three columns
    col1, col2, col3 = st.columns([2,2,2])
    
    # Add logos to each column with custom CSS
    # with col1:
    #     st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    #     st.image("E:/python_projects/الخدمات.png", width=220,)  # Adjust the width as needed
    #     st.markdown('</div>', unsafe_allow_html=True)

    # with col2:
    #     st.markdown('<div class="seclogo-container">', unsafe_allow_html=True)
    #     st.image("E:/python_projects/main_logo.png", width=200,)
    #     st.markdown('</div>', unsafe_allow_html=True)

    # with col3:
    #     st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    #     st.image("E:/python_projects/اسم الدائرة.png", width=350)
    #     st.markdown('</div>', unsafe_allow_html=True)
    st.markdown(
            """
            <style>
            .stHeading {
            text-align: right;
            }
            </style>
            """,
            unsafe_allow_html=True
            )
    st.title("المعلومات")
    try:
        cars = allcars() # type: ignore

        #Filters
        department_option = cars['department'].unique()
        section_option = cars['section'].unique()
        car_types = cars['type_option'].unique()
        allocations = ['تخصيص','بدون تخصيص','لا يوجد']
        recivie_type = ['اعارة','اهداء','شركة عامة']  
        date_option = cars['date_option'].unique()
        chassis_option = cars['chassis_number'].unique()
        car_owner = cars['car_owner'].unique()
        gearstick = cars['gearstick'].unique()
        registerationtype = cars['registerationtype'].unique()
        carnumbertype = cars['carnumbertype'].unique()

        # Checkbox for each car type
        custom_css = """
        <style>
            .stMultiSelect label {
                text-align: right;
                display: block;
            }
        </style>
        """
        st.markdown(custom_css, unsafe_allow_html=True)
        fircol1,fircol2 = st.columns(2)
        selected_department = fircol2.multiselect("الدائرة", options=department_option, placeholder = '')
        selected_section = fircol1.multiselect("القسم", options=section_option, placeholder = '')
        selected_types = fircol1.multiselect("نوع المركبة", options=car_types, placeholder = '')
        selected_allocations = fircol2.multiselect("التخصيص", options=allocations, placeholder = '')
        selected_recivie_type = fircol2.multiselect("نوع الشراء", options=recivie_type, placeholder = '')
        seccol1, seccol2=fircol1.columns(2,vertical_alignment="bottom")
        selected_model1 = seccol2.multiselect("موديل المركبة", options=date_option, placeholder = '')
        selected_model2 = seccol1.multiselect("", options=date_option, placeholder = '')
        selected_chassis = fircol2.multiselect("رقم الشاصي", options=chassis_option, placeholder = '')
        selected_car_owner = fircol1.multiselect("مستلم المركبة", options=car_owner, placeholder = '')
        selected_gearstick = fircol2.multiselect("نوع ناقل الحركة", options=gearstick, placeholder = '')
        selected_registerationtype = fircol1.multiselect("نوع التسجيل", options=registerationtype, placeholder = '')
        selected_carnumbertype = fircol2.multiselect("نوع لوحة المركبة", options=carnumbertype, placeholder = '')


        filtered_cars = cars
        # Filter the DataFrame based on selected types
        if selected_department:
            filtered_cars = filtered_cars[filtered_cars['department'].isin(selected_department)]
            filtered_cars.reset_index(drop=True, inplace=True)

        if selected_section:
            filtered_cars = filtered_cars[filtered_cars['section'].isin(selected_section)]
            filtered_cars.reset_index(drop=True, inplace=True)

        if selected_types:
            filtered_cars = filtered_cars[filtered_cars['type_option'].isin(selected_types)]
            filtered_cars.reset_index(drop=True, inplace=True)

        if selected_allocations:
            filtered_cars = filtered_cars[filtered_cars['allocations'].isin(selected_allocations)]
            filtered_cars.reset_index(drop=True, inplace=True)
            #the original allocations from the table is True False and لا يوجد edit it

        if selected_recivie_type:
            filtered_cars = filtered_cars[filtered_cars['receive_type'].isin(selected_recivie_type)]
            filtered_cars.reset_index(drop=True, inplace=True)
        
        if selected_chassis:
            filtered_cars = filtered_cars[filtered_cars['chassis_number'].isin(selected_chassis)]
            filtered_cars.reset_index(drop=True, inplace=True)

        if selected_car_owner:
            filtered_cars = filtered_cars[filtered_cars['car_owner'].isin(selected_car_owner)]
            filtered_cars.reset_index(drop=True, inplace=True)
        
        if selected_gearstick:
            filtered_cars = filtered_cars[filtered_cars['gearstick'].isin(selected_gearstick)]
            filtered_cars.reset_index(drop=True, inplace=True)
        
        if selected_registerationtype:
            filtered_cars = filtered_cars[filtered_cars['registerationtype'].isin(selected_registerationtype)]
            filtered_cars.reset_index(drop=True, inplace=True)
        
        if selected_carnumbertype:
            filtered_cars = filtered_cars[filtered_cars['carnumbertype'].isin(selected_carnumbertype)]
            filtered_cars.reset_index(drop=True, inplace=True)

        if selected_model1 and selected_model2:
            model1 = float(selected_model1[0])
            model2 = float(selected_model2[0])

            # Filter for numbers between selected models
            if model1 == model2:
                filtered_cars = filtered_cars[filtered_cars['date_option'].astype(float) == model1]
                filtered_cars.reset_index(drop=True, inplace=True)
            else:
                # Ensure model1 is less than model2
                lower_bound = min(model1, model2)
                upper_bound = max(model1, model2)
                filtered_cars = filtered_cars[(filtered_cars['date_option'].astype(float) >= lower_bound) & 
                                            (filtered_cars['date_option'].astype(float) <= upper_bound)]
                filtered_cars.reset_index(drop=True, inplace=True)


        
        selected_columns = filtered_cars[['chassis_number', 'fulcarnumber','type_option', 'model_option', 'date_option', 'allocations',
                                        'department', 'section', 'car_owner', 'receive_type','fromrec','gearstick','registerationtype','carnumbertype']]
        selected_columns.columns = [
                    'رقم الشاصي',
                    'رقم المركبة',  
                    'نوع المركبة',  
                    'طراز المركبة',  
                    'موديل المركبة',
                    'التخصيص',
                    'الدائرة',
                    'القسم',
                    'مستلم المركبة',
                    'نوع الأستلام',
                    'جهة الأستلام',
                    'نوع ناقل الحركة',
                    'نوع التسجيل',
                    'نوع لوحة المركبة'
                ]

        filter_option = st.radio("", ('كافة المركبات', 'متسلمين لأكثر من مركبة'))
        if filter_option == 'متسلمين لأكثر من مركبة':
            # Find duplicated car owners
            selected_columns = selected_columns[selected_columns['مستلم المركبة'].duplicated(keep=False)]
            selected_columns.reset_index(drop=True, inplace=True)
        else:
            selected_columns.reset_index(drop=True, inplace=True)
            


        selected_columns.reset_index(inplace=True)
        selected_columns.rename(columns={'index': 'ت'}, inplace=True)
        ordered_columns = ['نوع التسجيل','نوع لوحة المركبة','نوع ناقل الحركة','جهة الأستلام','نوع الأستلام','مستلم المركبة','القسم','الدائرة','التخصيص','موديل المركبة','طراز المركبة', 'نوع المركبة', 'رقم المركبة','رقم الشاصي', 'ت']
        selected_columns = selected_columns[ordered_columns]

        # filter_option = st.radio("", ('كافة المركبات', 'متسلمين لأكثر من مركبة'))

        # if filter_option == 'متسلمين لأكثر من مركبة':
        #     # Find duplicated car owners
        #     duplicated_owners = selected_columns[selected_columns['مستلم المركبة'].duplicated(keep=False)]
        #     filtered_selected_columns = duplicated_owners
        #     filtered_selected_columns.reset_index(drop=True, inplace=True)
        # else:
        #     filtered_selected_columns = selected_columns
        #     filtered_selected_columns.reset_index(drop=True, inplace=True)
        
        filtered_selected_columns = selected_columns
        
        # vehicles number
        num_rows = filtered_selected_columns.shape[0]
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
        
        filtered_selected_columns_reverse = filtered_selected_columns.iloc[:, ::-1]
        html_table_reversed = filtered_selected_columns_reverse.to_html(classes='table table-striped', index=False)
        html_table_reversed = html_table_reversed.replace('<table', '<table style="border: 2px solid #FFC300; border-collapse: collapse;"')


        st.markdown(f'<div class="align-right">عدد المركبات : {num_rows}</div>', unsafe_allow_html=True)
        html_table = filtered_selected_columns.to_html(classes='table table-striped', index=False)
        html_table = html_table.replace('<table', '<table style="border: 2px solid #FFC300; border-collapse: collapse;"')
        custom_css = """
                <style>
                .table th {
                    background-color: #353839;
                    color: white;
                    padding: 8px;
                }
                .table td {
                    text-align: right;
                    padding: 5px; 
                     
                }
                </style>
                """

        st.markdown(custom_css, unsafe_allow_html=True)
        st.markdown(
                f"""
                <div style="display: flex; justify-content: flex-end; width: 100%;">
                    <div style="width: auto; max-height: 300px; overflow-y: auto;">  <!-- Adjust width as needed -->
                        {html_table}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        action = 'loged in'
        create_log() # type: ignore
        userlog(action) # type: ignore
        #printit = st.button('طباعة')
        #dataframe table table-striped
        template_pdf = "temp.pdf"
        infout = "E:\python_projects\infout.pdf"
        pdf_data = create_table_pdf2(filtered_selected_columns, html_table_reversed, infout) # type: ignore
        st.download_button(
            label="طباعة",
            data=pdf_data,
            file_name="تقرير المركبات.pdf",
            mime="application/pdf"
        )
    
        
    
    except:
        action = 'loged in'
        create_log() # type: ignore
        userlog(action) # type: ignore
        st.markdown(
            """
            <div style="text-align: right; color: red;">
                لا توجد اي مركبات مسجلة حالياً
            </div>
            """,
            unsafe_allow_html=True
        )
    
    


#Add new vehicle info
def add_vehicle(*variables):
     st.markdown(
            """
            <style>
    #         .stApp {
    #      background-color: #0e1117; /* Set background color to white */
    #  }
            .stHeading {
            text-align: right;
            }
            .st-emotion-cache-1jicfl2{
                padding : 0rem 1rem 10rem;
            }
            </style>
            """,
            unsafe_allow_html=True
            )
     st.title("اضافة مركبة")
     typeop = typeoption() # type: ignore
     cylindersop = cylindersoption() # type: ignore
     fuelop = fueloption() # type: ignore
     cartypeop = cartypeoption() # type: ignore
     governoratesop = governoratesoption() # type: ignore
     colorop = coloroption() # type: ignore
     carlettersop = carlettersoption() # type: ignore
     lettersop = lettersoption() # type: ignore
     current_year = datetime.datetime.now().year
     fromrecop = fromrecoption() # type: ignore
     registerationtypeop = registerationtypeoption() # type: ignore
     receive_typeop = receive_typeoption() # type: ignore
     start_year = 1950
     year_range = list(range(start_year, current_year + 1))
     year_range.append(1)
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

            .1logo-container {
                
                margin-top: 200px; 
            }
            .2logo-container {
                
                margin-top: 0px;
                margin-bottom: 50px; 
            }
            

            </style>
            """,
            unsafe_allow_html=True
                )
     fircol1, fircol2 = st.columns(2)
     type_option = fircol2.selectbox("اسم المركبة", typeop, key='type_option')
     with fircol1:
         st.empty()  # Push content down
         st.empty()
         logo_col1, logo_col2, logo_col3, logo_col4, logo_col5 = st.columns(5)
         with logo_col1:
            st.image("E:/python_projects/Toyota.png", width=50, use_column_width=False)
         with logo_col2:
            st.markdown('<div class="2logo-container">', unsafe_allow_html=True)
            st.image("E:/python_projects/hyundai.png", width=50, use_column_width=False)
            st.markdown('</div>', unsafe_allow_html=True)
         with logo_col3:
            st.markdown('<div class="2logo-container">', unsafe_allow_html=True)
            st.image("E:/python_projects/bmw.png", width=50, use_column_width=False)
            st.markdown('</div>', unsafe_allow_html=True)
         with logo_col4:
            st.markdown('<div class="2logo-container">', unsafe_allow_html=True)
            st.image("E:/python_projects/mercedes.png", width=50, use_column_width=False)
            st.markdown('</div>', unsafe_allow_html=True)
         with logo_col5:
            st.markdown('<div class="1logo-container">', unsafe_allow_html=True)
            st.image("E:/python_projects/chevrolet.png", width=50, use_column_width=False)
            st.markdown('</div>', unsafe_allow_html=True)
     modelop = modeloption(type_option) # type: ignore
     with st.form(key='add_vehicle_form', clear_on_submit=True):
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
         model_option = col2.selectbox("الطراز", modelop, key='model_option')
         date_option = col1.selectbox("موديل المركبة",year_range, key='date_option',index=len(year_range) - 1)
         cylinders_option = col2.selectbox("عدد الأسطوانات", cylindersop, key='cylinders_option')
         fuel_option = col1.selectbox("نوع الوقود", fuelop, key='fuel_option')
         cartype_option = col2.selectbox("نوع المركبة", cartypeop, key='cartype_option')
         governorates_option = col1.selectbox("اسم المحافظة", governoratesop, key='governorates_option')
         cargovernorates_option = col2.selectbox("محافظة المركبة", governoratesop, key='cargovernorates_option')
         color_option = col1.selectbox("لون المركبة", colorop, key='color_option')
         chassis_number = col2.text_input("رقم الشاصي", key='chassis_number')
         car_folder = col1.text_input("رقم الضبارة", key='car_folder')
         registerationtype = col2.selectbox("نوع التسجيل", registerationtypeop, key='registerationtype')
         numbertypes = ['الماني','قديم','جديد']
         carnumbertype = col1.radio('نوع لوحة المركبة',numbertypes, key='carnumbertype')
         #second widget with 4 columns
         seccol1, seccol2,seccol3,seccol4=st.columns(4,vertical_alignment="bottom")
         letter_carnumber = seccol1.selectbox("", carlettersop, key='letter_carnumber')
         carnumber = seccol2.text_input("رقم المركبة", key='carnumber')
         letter_annualnumber = seccol3.selectbox("", lettersop, key='letter_annualnumber')
         annualnumber = seccol4.text_input("رقم السنوية", key='annualnumber')
         thircol1, thircol2,thircol3,thircol4=st.columns(4,vertical_alignment="bottom")
         receive_type =  thircol4.selectbox("نوع الأتسلام",receive_typeop, key='receive_type')
         fromrec = thircol3.selectbox("جهة الأهداء او الأعارة",fromrecop,key="fromrec")
         notes = thircol2.text_input("الملاحظات", key='notes',value="لا يوجد")
         gearstick =  thircol1.radio("نوع ناقل الحركة",('اوتماتيك','يدوي'), key='gearstick')

         st.markdown(
            """
            <div style="text-align: right; color: red;">
                الخيار رقم (1) هو اختيار افتراضي في حال لم يرغب المستخدم في اضافة اختيار معين حالياً*
            </div>
            """,
            unsafe_allow_html=True
        )
         variables = [type_option,model_option,date_option,cylinders_option,
                      fuel_option,cartype_option,governorates_option,cargovernorates_option,color_option,
                      chassis_number,letter_carnumber,carnumber,letter_annualnumber,annualnumber, receive_type,
                      car_folder,fromrec,notes,gearstick,registerationtype,carnumbertype]
         
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
         submit_button = forcol6.form_submit_button("اضافة")
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

     
     st.markdown('<div class="align-right">اضافة اوليات المركبة</div>', unsafe_allow_html=True)
     uploaded_file = st.file_uploader("", type=["pdf"])
     
     if submit_button:
         if any(item == '' for item in variables):
             st.error("يجب ملئ كافة المعلومات")
         else:
             destination_dir = f"E://python_projects//{car_folder}"
     
             if not os.path.exists(destination_dir):
                 os.makedirs(destination_dir)
                 if uploaded_file is not None:
                     file_path = os.path.join(destination_dir, '0.pdf')
                     with open(file_path, "wb") as f:
                         f.write(uploaded_file.getbuffer())
                     os.startfile(destination_dir)
             else:
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
                    biggest_number = biggest_number + 1
                    newfile = str(biggest_number)
                    if uploaded_file is not None:
                        file_path = os.path.join(destination_dir, newfile+'.pdf')
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        os.startfile(destination_dir)
         

             
             add_execution(*variables) # type: ignore
             action = 'added a vehicle'
             userlog(action) # type: ignore
          
          

def edit_page():
    st.markdown(
            """
            <style>
    #         .stApp {
    #      background-color: #0e1117; /* Set background color to white */
    #  }
            .stHeading {
            text-align: right;
            }
            .st-emotion-cache-1jicfl2{
                padding : 0rem 1rem 10rem;
            }
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
            .stDateInput label {
                text-align: right;
                display: block;
                }
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
    st.title("تعديل المعلومات")
    
    fircol1, fircol2 = st.columns(2)
    chassis_number = fircol2.text_input("رقم الشاصي", key='chassis_number')
    info_edi = info_to_edit(chassis_number) # type: ignore
    


#handover a vehicle
def handover_vehicle(*variables):
    malfunctionsop = malfunctionsoptions() # type: ignore
    departmentop = departmentoptions() # type: ignore
    st.markdown(
            """
            <style>
    #         .stApp {
    #      background-color: #0e1117; /* Set background color to white */
    #  }
            .stSelectbox label {
                text-align: right;
                display: block;
                }
            .st-emotion-cache-1jicfl2{
                padding : 0rem 1rem 10rem;
            }
            .stTextInput label {
                text-align: right;
                display: block;
                }
            .stDateInput label {
                text-align: right;
                display: block;
                }
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
    seccol1, seccol2, seccol3 = st.columns([1,1,1])
    id_number = seccol3.text_input("", placeholder="رقم المركبة او رقم الشاصي", key='id_number')
    department = seccol2.selectbox('اختر الدائرة التي سوف يتم توجيه المركبة اليها', departmentop,key = 'department')
    sectionop = sectionoptions(department) # type: ignore
    positionop = positionoption()  # type: ignore
    with st.form(key='handover_vehicle_form', clear_on_submit=True):
        thircol1, thircol2, thircol3, thircol4 = st.columns([1,1,1,1.5])
        current_car_owner = thircol4.text_input("اسم المتسلم الحالي", key='current_car_owner')
        position = thircol3.selectbox('العنوان الوظيفي', positionop, key = 'position') # type: ignore
        document_number = thircol2.text_input("رقم الكتاب", key='document_number')
        document_date = thircol1.date_input("تاريخ الكتاب", key='document_date')
        recivie_date = thircol4.date_input("تاريخ الأستلام", key='recivie_date')

        st.markdown(
            """
            <style>
    #         .stApp {
    #      background-color: #0e1117; /* Set background color to white */
    #  }
            .streamlit-expanderHeader {
            height: 30px; /* Adjust header height */
            }
            .stMultiSelect {
            max-height: 70px; /* Set max height for the dropdown */
            overflow-y: auto; /* Add scroll if content overflows */
            overflow-x: auto;
            }
            .stMultiSelect label {
            text-align: right;
            display: block;
            }
            .stCheckbox {
            text-align: right;
            display: flex;
            justify-content: flex-end;
            }
            </style>
            """,
            unsafe_allow_html=True
            )

        vehicle_meter = thircol3.text_input('عداد المركبة', placeholder='Km',key='vehicle_meter')
        malfunctions = thircol2.multiselect("العوارض", malfunctionsop, placeholder="اختر العوارض", key='malfunctions')
        section = thircol1.selectbox('القسم', sectionop, index = 0, key = 'section') # type: ignore
        thircol4.markdown("<div style='margin: 26px 0 0 50px; '></div>", unsafe_allow_html=True)
        allocations = thircol4.checkbox("التخصيص", key='allocations')
                    
        variables = [id_number,current_car_owner,document_number,document_date,recivie_date,allocations,malfunctions,
                        vehicle_meter,department,section,position]


        forcol1, forcol2, forcol3, forcol4, forcol5, forcol6= st.columns(6)
        print_button = forcol6.form_submit_button("طباعة")
            #edit_button = forcol1.form_submit_button("تعديل")
        handover_button = forcol5.form_submit_button("تسليم مركبة")
            
        if print_button:
            print('3333')
            #if edit_button:
            #  baseinfo, malf = editoptions(id_number) # type: ignore
            #  new_car_owner = baseinfo[1]
            #  new_document_number = baseinfo[2]
            #  new_document_date = baseinfo[3]
            #  new_recivie_date = baseinfo[4]
            #  new_allocations = baseinfo[5]
            #  #new_malfunctions = baseinfo[6]
            #  #malfuneditbutton(new_malfunctions)
            #  edit1()
            #
            #  print(baseinfo,malf)
            #  print(type(baseinfo),type(malf))
        if handover_button:
            handover_exe(*variables) # type: ignore
            action = 'handedover a vehicle to a new owner'
            userlog(action) # type: ignore
        
        

def edit1():
    st.title("heloooo")


#Fuel Committee
def fuel():
    st.markdown("""
    <style>
    #     .stApp {
    #      background-color: #0e1117; /* Set background color to white */
    #  }
    </style>
""", unsafe_allow_html=True)
    try:
        data = fuel_data() # type: ignore
        selected_columns = data[['chassis_number', 'current_car_owner', 'recivie_date', 'vehicle_meter']]
        selected_columns.columns = [
                'رقم الشاصي',  
                'اسم المالك الحالي',  
                'تاريخ الأستلام',  
                'عداد المركبة',  
            ]
        
        selected_columns.reset_index(inplace=True)
        selected_columns.rename(columns={'index': 'Index'}, inplace=True)
        ordered_columns = ['عداد المركبة', 'تاريخ الأستلام', 'اسم المالك الحالي', 'رقم الشاصي', 'Index']
        selected_columns = selected_columns[ordered_columns]
        html_table = selected_columns.to_html(classes='table table-striped', index=False)
        html_table = html_table.replace('<table', '<table style="border: 2px solid #FFC300; border-collapse: collapse;"')
        
        custom_css = """
            <style>
            .table th {
                background-color: #353839;
                color: white;
                padding: 8px;
            }
            </style>
            """

        st.markdown(custom_css, unsafe_allow_html=True)
        st.markdown(
            f"""
            <div style="display: flex; justify-content: flex-end; width: 100%;">
                <div style="width: auto; max-height: 300px; overflow-y: auto;">  <!-- Adjust width as needed -->
                    {html_table}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        col1, col2, col3, col4 = st.columns([1,1,1,1])
        search_number = col4.text_input("", placeholder="رقم المركبة او رقم الشاصي", key='search_number')

        st.markdown(
        """
        <style>
        button[kind="primary"]{
            background-color: #111421;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            cursor: pointer;
            font-size: 16px;
        }
        button[kind="primary"]:hover{
            background-color: #004080;
        }
        div.stButton {
            display: flex;
            justify-content: flex-end;
        }
        </style>
        """,
        unsafe_allow_html=True
            )
        with col4:
            search_but = st.button("بحث",key = 'search_but',type = "primary")
            if search_but:
                fd()  # THIS IS PINDING FOR A TIME NOW
    except:
        st.error('لا يوجد اي مركبة تحتوي على تخصيص حالياً')
def fd():
    st.write('done')
   

#new_info
def add_new():
    departmentoptions() # type: ignore
    typeoption() # type: ignore
    positionoption() # type: ignore
    malfunctionsoptions() # type: ignore
    fromrecoption() # type: ignore
    registerationtypeoption() # type: ignore
    st.markdown(
            """
            <style>
    #         .stApp {
    #      background-color: #0e1117; /* Set background color to white */
    #  }
            .stHeading {
            text-align: right;
            }
            .st-emotion-cache-1jicfl2{
                padding : 0rem 1rem 10rem;
            }
            .stTextInput label {
            text-align: right;
            display: block;
            }
            .stFormSubmitButton {
            display: flex;
            justify-content: flex-end;
            }
            .stWarning {
            display: flex;
            justify-content: flex-end;
            }
            .stSelectbox label {
            text-align: right;
            display: block;
            }
            </style>
            """,
            unsafe_allow_html=True
            )
    st.title("اضافة معلومات جديدة")
    
    col1,col2 = st.columns(2)
    with col2:
        with st.form(key='newcartype', clear_on_submit=True):
            typeoption1 = st.text_input('اضافة مركبة',key='typeoption')
            modeloption = st.text_input('الطراز',key='model')
            add_car_type = st.form_submit_button('اضافة')
            if add_car_type:
                if not typeoption1 or not modeloption:
                    st.warning('يرجى ملء جميع الحقول!')
                else:
                    addtype(typeoption1,modeloption) # type: ignore
                    st.success('تمت الأضافة')
                    action = 'added new data to the system'
                    userlog(action) # type: ignore
                    
    
    with col1:
        with st.form(key='newdepartment', clear_on_submit=True):
            departmentoption = st.text_input('اضافة دائرة',key='departmentoption')
            sectionoption = st.text_input('القسم',key='sectionoption')
            add_department = st.form_submit_button('اضافة')
            if add_department:
                if not departmentoption or not sectionoption:
                    st.warning('يرجى ملء جميع الحقول!')
                else:
                    adddepar(departmentoption,sectionoption) # type: ignore
                    st.success('تمت الأضافة')
                    action = 'added new data to the system'
                    userlog(action) # type: ignore
    with col2:
        with st.form(key='position', clear_on_submit=True):
            positionoption1 = st.text_input('اضافة عنوان وظيفي',key='positionoption')
            add_position = st.form_submit_button('اضافة')
            if add_position:
                if not positionoption1:
                    st.warning('يرجى ملء جميع الحقول!')
                else:
                    addposition(positionoption1) # type: ignore
                    st.success('تمت الأضافة')
                    action = 'added new data to the system'
                    userlog(action) # type: ignore
    with col1:
        with st.form(key='malfunctions', clear_on_submit=True):
            malfunctionoption = st.text_input('اضافة عوارض',key='malfunctionoption')
            add_malf = st.form_submit_button('اضافة')
            if add_malf:
                if not malfunctionoption:
                    st.warning('يرجى ملء جميع الحقول!')
                else:
                    addmalfunc(malfunctionoption) # type: ignore
                    st.success('تمت الأضافة')
                    action = 'added new data to the system'
                    userlog(action) # type: ignore
    with col2:
        with st.form(key='fromrec', clear_on_submit=True):
            fromoption = st.text_input('اضافة جهة أهداء او أعارة',key='fromoption')
            add_from = st.form_submit_button('اضافة')
            if add_from:
                if not fromoption:
                    st.warning('يرجى ملء جميع الحقول!')
                else:
                    addfromrec(fromoption) # type: ignore
                    st.success('تمت الأضافة')
                    action = 'added new data to the system'
                    userlog(action) # type: ignore
    with col1:
        with st.form(key='registertypes', clear_on_submit=True):
            registertypesoption = st.text_input('اضافة نوع تسجيل',key='registertypesoption')
            add_malf = st.form_submit_button('اضافة')
            if add_malf:
                if not registertypesoption:
                    st.warning('يرجى ملء جميع الحقول!')
                else:
                    addregisterty(registertypesoption) # type: ignore
                    st.success('تمت الأضافة')
                    action = 'added new data to the system'
                    userlog(action) # type: ignore
    with col2:
        with st.form(key='coloroption', clear_on_submit=True):
            color = st.text_input('اضافة لون مركبة',key='coloroptiontype')
            add_malf = st.form_submit_button('اضافة')
            if add_malf:
                if not color:
                    st.warning('يرجى ملء جميع الحقول!')
                else:
                    addcolor(color) # type: ignore
                    st.success('تمت الأضافة')
                    action = 'added new data to the system'
                    userlog(action) # type: ignore
            

#refresh function
def out():
    #  st.session_state.logged_in = False
    #  log_out() # type: ignore
    #newwww
    #cookie.delete("logged_in")
    #cookie.delete("username")
    #cookie.delete("password")
    # st.session_state.logged_in = False
    # cookie['logged_in'] = False
    # cookie.save()
    #del st.session_state.username
    #del st.session_state.username
    #infout = "E:\python_projects\infout.pdf"
    #os.remove(infout)
    action = 'signed out'
    userlog(action) # type: ignore
    st.session_state.logged_in = False
    st.rerun()



#Search page
def search_vehicle():
    st.markdown(
            """
            <style>
    #         .stApp {
    #      background-color: #0e1117; /* Set background color to white */
    #  }
            .stHeading {
            text-align: right;
            }
            .st-emotion-cache-1jicfl2{
                padding : 0rem 1rem 10rem;
            }
            .stButton {
                display: flex;
                justify-content: flex-end;
            }
            </style>
            """,
            unsafe_allow_html=True
            )
    st.title('بحث عن مركبة')
    col1, col2, col3, col4 = st.columns([1,1,1,1])
    search_number = col4.text_input("", placeholder="رقم المركبة او رقم الشاصي", key='search_number')
    search_button = col4.button("بحث", key='search_button')
    if search_button:
        search_vehicle_info(search_number) # type: ignore
        action = 'searched about a vehicle info'
        userlog(action) # type: ignore



#Delete page
def delete_vehicle():
    deleteop = delete_options() # type: ignore
    st.markdown(
            """
            <style>
    #         .stApp {
    #      background-color: #0e1117; /* Set background color to white */
    #  }
            .stHeading {
            text-align: right;
            }
            .st-emotion-cache-1jicfl2{
                padding : 0rem 1rem 10rem;
            }
            .stTextInput label {
            text-align: right;
            display: block;
            }
            .stFormSubmitButton {
            display: flex;
            justify-content: flex-end;
            }
            .stSelectbox label {
            text-align: right;
            display: block;
            }
            </style>
            """,
            unsafe_allow_html=True
            )
    st.title("حذف مركبة")
    
    fircol1,fircol2 = st.columns(2) 
    chassisnum = fircol2.text_input('ادخل رقم الشاصي للمركبة')
    delete_type = fircol1.selectbox('نوع الحذف', deleteop,key = 'delete_type')
    subdelop = subdelete(delete_type) # type: ignore
    with st.form(key='settings_form', clear_on_submit=True):
        deleteto = st.selectbox('جهة الحذف', subdelop, index = 0, key = 'deleteto')
        delete = st.form_submit_button('حذف الركبة')

    if delete:
        delete_execution(chassisnum,delete_type,deleteto) # type: ignore
        action = 'deleted a vehicle from the system'
        userlog(action) # type: ignore

#Settings page
def settings(*variables):   
    st.markdown(
            """
            <style>
    #         .stApp {
    #      background-color: #0e1117; /* Set background color to white */
    #  }
            .stHeading {
            text-align: right;
            }
            .st-emotion-cache-1jicfl2{
                padding : 0rem 1rem 10rem;
            }
            .stTextInput label {
            text-align: right;
            display: block;
            }
            .stFormSubmitButton {
            display: flex;
            justify-content: flex-end;
            }
            .stSelectbox label {
            text-align: right;
            display: block;
            }
            .stTextInput input {
            text-align: right;
            }
            </style>
            """,
            unsafe_allow_html=True
            )
    st.title("أدارة الحسابات")
    accounttype = accountty() # type: ignore
    with st.form(key='settings_form', clear_on_submit=True):
        current_username = st.text_input('اسم المستخدم')
        current_password = st.text_input('كلمة المرور')
        account_type = st.selectbox("نوع الحساب", accounttype, key='account_type')
        col1, col2,col3,col4=st.columns(4,vertical_alignment="center")
        add_account = col4.form_submit_button('اضافة حساب')
        edit_info = col3.form_submit_button('تعديل المعلومات')
        disable_account = col2.form_submit_button('تعطيل الحساب')
        enable_account = col1.form_submit_button('تفعيل الحساب')
        variables = [current_username,current_password,account_type]

    if add_account:
        create_new_account(*variables) # type: ignore
        action = 'added a new account'
        userlog(action) # type: ignore
    if edit_info:
        update_account(current_username,current_password,account_type) # type: ignore
        action = 'edited an account'
        userlog(action) # type: ignore
    if disable_account:
        disable_status(current_username,current_password) # type: ignore
        action = 'disabled an account'
        userlog(action) # type: ignore
    if enable_account:
        enable_status(current_username,current_password) # type: ignore
        action = 'enabled an account'
        userlog(action) # type: ignore


# Main
def main():
    #Check if the user is logged in
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        title_page()
    else:
        login_page()
    

    # if username_cookie and password_cookie :
    #     st.session_state.logged_in = True
    #     #cousername = cookie.get("username")
    #     #copassword = cookie.get("password")
    #     check_credentials(username_cookie, password_cookie) # type: ignore
    
    # if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    #     login_page()
    # else:
    #     title_page()

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    st.markdown("""
    <style>
    #  .stApp {
    #      background-color: #00001a; /* Set background color to white */
    #  }
    
    </style>
    """,
    unsafe_allow_html=True
    )
    main()
