import streamlit as st
import pandas as pd
import datetime
import pyodbc
import os
#from cars import * # type: ignore
from reportlab.lib.pagesizes import letter
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
import re


'''activities = ['المعلومات','اضافة مركبة','تعديل المعلومات','حذف مركبة']
    choices= st.sidebar.selectbox("Select Activity",activities)        
    if choices == 'المعلومات':
        info_page() 

    if choices == 'اضافة مركبة':
        add_vehicle() '''
#import pandas as pd
#df = pd.read_excel('E:/python_projects/Book1.xlsx') #you could add index_col=0 if there's an index
#first_column_name = df.columns[0]  # Get the name of the first column
#first_column_data = df[first_column_name]
#options = df[first_column_data].dropna().unique().tolist()  # Get unique, non-null values and convert to list

#df = pd.ExcelFile('E:/python_projects/Book1.xlsx').parse('Sheet1') #you could add index_col=0 if there's an index
#sheet = pd.read_excel("E:/python_projects/Book1.xlsx")
#print(sheet['AAA'])

# set a specific option in the select box, radio buttons and textinput
# --------------------------------------------------------------------
'''import streamlit as st

# Define options for the selectbox
options = ['Option 1', 'Option 2', 'Option 3']

# Set the default selected value
default_value = 'Option 2'

# Create the selectbox widget
selected_option = st.selectbox(
    'Choose an option:', 
    options,
    index=options.index(default_value)  # Set the default selection
)

# Display the selected option
st.write(f'You selected: {selected_option}')

import streamlit as st

# Define options for the radio button
options = ['Option 1', 'Option 2', 'Option 3']

# Set the default selected value
default_value = 'Option 2'

# Create the radio button widget
selected_option = st.radio(
    'Choose an option:', 
    options,
    index=options.index(default_value)  # Set the default selection
)

# Display the selected option
st.write(f'You selected: {selected_option}')


import streamlit as st

# Set the default text input value
default_text = 'Default text here'

# Create the text input widget
user_input = st.text_input(
    'Enter some text:', 
    value=default_text  # Set the default text
)

# Display the entered text
st.write(f'You entered: {user_input}')
'''
# --------------------------------------------------------------------

import random
import streamlit as st
import uuid


RERUN_COUNT         = 'rerun_count'
FORM_SUCCESSFUL     = 'form_successful'
USER_TEXT_INPUT_KEY = 'user_text_input_key'
INIT_SESSION_STATE  = 'init_done'

SUCCESS_MESSAGE = ':)'
ERROR_MESSAGE   = ':('


def init_session_state ():
    st.session_state[RERUN_COUNT] = -1
    st.session_state[FORM_SUCCESSFUL] = False
    st.session_state[USER_TEXT_INPUT_KEY] = uuid.uuid4()
    st.session_state[INIT_SESSION_STATE] = True


def user_input_meets_condition (user_input):
    return random.choice( (True, False) )


def main ():
    if INIT_SESSION_STATE not in st.session_state:
        init_session_state()


    # Show success message when user input meets condition.
    if st.session_state[FORM_SUCCESSFUL]:
        st.session_state[FORM_SUCCESSFUL] = False
        st.success(SUCCESS_MESSAGE)


    # Just some debugging output.
    st.session_state[RERUN_COUNT] += 1
    st.markdown(f'Rerun count: **{st.session_state[RERUN_COUNT]}**')


    with st.form(
            key             = 'my-form',
            clear_on_submit = False
    ):
        error_message_placeholder = st.empty()

        user_input = st.text_input(
                        label = 'Write whatever',
                        key   = st.session_state[USER_TEXT_INPUT_KEY]
        )


        if st.form_submit_button():
            if user_input_meets_condition(user_input):
                st.session_state[FORM_SUCCESSFUL] = True

                # Change the user text input key so that a new text input is
                # rendered with its default value as blank (or whatever it's
                # set in the value argument).
                st.session_state[USER_TEXT_INPUT_KEY] = uuid.uuid4()

                # We need to reload so success message shows.
                st.rerun()
            else:
                error_message_placeholder.error(ERROR_MESSAGE)


main()
