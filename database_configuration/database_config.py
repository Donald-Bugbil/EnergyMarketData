import os
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from dotenv import load_dotenv
from schema.Schema import Base

load_dotenv()


DRIVERNAME=os.environ['DRIVERNAME']
POSTGRES_PASSWORD=os.environ['POSTGRES_PASSWORD']
POSTGRES_USER=os.environ['POSTGRES_USER']
POSTGRES_DB=os.environ['POSTGRES_DB']
POSTGRES_HOST=os.environ['POSTGRES_HOST']
POSTGRES_PORT=os.environ['POSTGRES_PORT']

#Establishing database configuration
database_configuration=URL.create(drivername=DRIVERNAME,
                                  username=POSTGRES_USER,
                                  password=POSTGRES_PASSWORD,
                                  host=POSTGRES_HOST,
                                  port=POSTGRES_PORT,
                                  database=POSTGRES_DB
                                  )
#starting the engine
engine=create_engine(database_configuration)

#initializing the database
def database_initialize():
    return Base.metadata.create_all(engine)