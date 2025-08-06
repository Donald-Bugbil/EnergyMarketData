import os
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from dotenv import load_dotenv
from schema.Schema import Base

load_dotenv()

ENVIRONMENT=os.environ['ENVIRONMENT']
#development on postgres
if ENVIRONMENT=='development':
    DRIVERNAME=os.environ['DRIVERNAME']
    PASSWORD=os.environ['POSTGRES_PASSWORD']
    USER=os.environ['POSTGRES_USER']
    DATABASE=os.environ['POSTGRES_DB']
    HOST=os.environ['POSTGRES_HOST']
    PORT=os.environ['POSTGRES_PORT']


# #RDS deployment for production purpose
else:
    DRIVERNAME=os.environ['DRIVERNAME']
    HOST=os.environ['AWS_POSTGRES_HOST']
    PORT=os.environ['AWS_POSTGRES_PORT']
    USER=os.environ['AWS_POSTGRES_USER']
    PASSWORD=os.environ['AWS_POSTGRES_PASSWORD']
    DATABASE=os.environ['AWS_POSTGRES_DB']

#Establishing database configuration
database_configuration=URL.create(drivername=DRIVERNAME,
                                  username=USER,
                                  password=PASSWORD,
                                  host=HOST,
                                  port=PORT,
                                  database=DATABASE
                                  )
#starting the engine
engine=create_engine(database_configuration)

#initializing the database
def database_initialize():
    return Base.metadata.create_all(engine)