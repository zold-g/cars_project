import streamlit
import pandas
import streamlit.web.cli as stcli
import os,sys
import streamlit as st
import pandas as pd
#import seaborn as sns 
#from tkinter import filedialog
#import shutil
import datetime
import os
#from st_on_hover_tabs import on_hover_tabs
#from waitress import serve
#import ctypes
#import importlib_metadata
import streamlit as st
import pandas as pd
import datetime
import sqlite3
import pyodbc
import os
import subprocess
from setuptools import setup, find_packages
from cx_Freeze import setup, Executable
import streamlit.runtime.scriptrunner.magic_funcs
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
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
import asyncio
import asyncodbc
import asyncio





def resolve_path(path):
    resolved_path = os.path.abspath(os.path.join(os.getcwd(), path))
    return resolved_path

if __name__ == "__main__":
    sys.argv = [
        "streamlit",
        "run",
        resolve_path("car2.py"),
        "--global.developmentMode=false",
    ]
    sys.exit(stcli.main())

    try:
        subprocess.run(sys.argv, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running Streamlit: {e}")
        sys.exit(1)
