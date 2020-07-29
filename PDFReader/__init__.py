from flask import Flask
import os

app = Flask(__name__)

app.config['SECRET_KEY']=ldfjsolasfuasdfjsodfusoij4w09r8pswojufsldkfjdf9

from PDFReader import routes