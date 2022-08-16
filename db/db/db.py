from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import urllib
from sqlalchemy import create_engine

server = 'spacebot.database.windows.net' # to specify an alternate port
database = 'spacebot' 
username = 'Javier' 
password = 'Sp4c3bot.2022@'
params = urllib.parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};SERVER=" + server + ";DATABASE=" + database + ";UID=" + username + ";PWD=" + password)
engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
Session = sessionmaker(bind=engine, autoflush=True, autocommit=True)
session = Session()

Base = declarative_base()