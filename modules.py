import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog
import tkinter.ttk as ttk
import random
import sys
import os
#import win32com.client
import threading
import json
import zipfile
import re
import base64
import datetime
import time
from bs4 import BeautifulSoup
import re
import string
from bs4 import BeautifulSoup

import xlsxwriter

#from docx import Document
#from docx.shared import Inches, Pt, RGBColor
#from docx.enum.text import WD_ALIGN_PARAGRAPH
#from docx.oxml.ns import qn
#from docx.oxml import OxmlElement

#import plotly.express as px
import pandas as pd

from PIL import ImageTk, Image
from PyQt6.QtWidgets import QMessageBox

import requests
# To ignore SSL errors, the SLL will be disabled as Helix ALM REST API is configured to work on localhost. If not,
# SLL must be enabled and verified for any request to ensure that connection is secure
from urllib3.exceptions import InsecureRequestWarning
# Ignores SSL errors
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)