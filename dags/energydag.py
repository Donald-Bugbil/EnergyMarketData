import boto3
import os
import io
import pandas as pd
import csv
import pendulum
from airflow.decorators import dag, task
import logging
from database_configuration.database_config import database_initialize
from aws.aws_config import ACCESS_KEY, SECRET_KEY, BUCKET_NAME

task_logger=logging.getLogger('airflow.task')

@dag(
    schedule='@daily',
    start_date=pendulum.datetime(2025, 8, 5, tz='UTC'),
    catchup=True,
    tags=['energy_etl']
)

#function for the workflow
def energy_worflow():
    """
    This worlflow extract raw data from s3 bucket and then clean and transform it and finally loaded to rds
    """

    #This first task initiate connection with the database
    @task()
    def database_initialization():
        try:
            database_initialize()
            task_logger.info(f"database is connected successfully:{True}" )
            return True
        except Exception as e:
            task_logger.error(f"error connecting to database:{e}")
            return None
        
    #This task pulls raw data from aws S3 bucket "extract"
    @task()
    def extract():
        try:
            session=boto3.Session(aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
            Client=session.client('s3')
            response=Client.get_object(Bucket=BUCKET_NAME, Key='20250728 Open Electricity.csv')['Body'].read()
            Byte_format=io.BytesIO(response)
            data_frame=pd.read_csv(Byte_format,low_memory=False)
            task_logger.info(data_frame)
            return data_frame
        except Exception as e:
            task_logger.warning(f'Can not connect to s3')
            return None
        
    @task()
    def transform(data_frame):
        new_data_frame=data_frame

        # Convert the 'date' column to datetime format
        new_data_frame['date']=pd.to_datetime(new_data_frame['date']) 
        
        # Round all numeric columns to 2 decimal places
        new_data_frame = new_data_frame.round(2)
        return new_data_frame
        
    starting_database=database_initialization()
    extraction=extract()
    transformation=transform(extraction)
energy_worflow()
        
   
