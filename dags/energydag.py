import boto3
import os
import io
import pandas as pd
import csv
import pendulum
from airflow.decorators import dag, task
import logging
from database_configuration.database_config import database_initialize, engine
from aws.aws_config import ACCESS_KEY, SECRET_KEY, BUCKET_NAME
from schema.Schema import Session, Electric

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
    
    @task()
    def load(transformed_data, database_state):

        # prepare a list to store Electric model instances to insert into the DB    
        data_to_insert=[]

        def create_object(row):
            electric=Electric(
                date=row['date'],
                battery_charging_mv=row['Battery (Charging) -  MW'],
                pumps_mv=row['Pumps -  MW'],
                coal_brown_mv=row['Coal (Brown) -  MW'],
                coal_black_mv=row['Coal (Black) -  MW'],
                bioenergy_biomass_mv=row['Bioenergy (Biomass) -  MW'],
                distillate_mv=row['Distillate -  MW'],
                gas_steam_mv=row['Gas (Steam) -  MW'],
                gas_ccgt_mv=row['Gas (CCGT) -  MW'],
                gas_ocgt_mv=row['Gas (OCGT) -  MW'],
                gas_reciprocating_mw=row['Gas (Reciprocating) -  MW'],
                gas_waste_coal_mine_mw=row['Gas (Waste Coal Mine) -  MW'],
                battery_discharging_mw=row['Battery (Discharging) -  MW'],
                hydro_mw=row['Hydro -  MW'],
                wind_mw=row['Wind -  MW'], 
                solar_utility_mw=row['Solar (Utility) -  MW'],
                solar_rooftop_mw=row['Solar (Rooftop) -  MW'],
                coal_brown_emissions_vol_tco2e=row['Coal (Brown) Emissions Vol - tCO₂e'],
                coal_black_emissions_vol_tco2e=row['Coal (Black) Emissions Vol - tCO₂e'],
                bioenergy_biomass_emissions_vol_tco2e=row['Bioenergy (Biomass) Emissions Vol - tCO₂e'],
                distillate_emissions_vol_tco2e=row['Distillate Emissions Vol - tCO₂e'],
                gas_steam_emissions_vol_tco2e=row['Gas (Steam) Emissions Vol - tCO₂e'],
                gas_ccgt_emissions_vol_tco2e=row['Gas (CCGT) Emissions Vol - tCO₂e'],
                gas_ocgt_emissions_vol_tco2e=row['Gas (OCGT) Emissions Vol - tCO₂e'],
                gas_reciprocating_emissions_vol_tco2e=row['Gas (Reciprocating) Emissions Vol - tCO₂e'],
                gas_waste_coal_mine_emissions_vol_tco2e=row['Gas (Waste Coal Mine) Emissions Vol - tCO₂e'],
                emissions_intensity_kgco2e_per_mwh=row['Emissions Intensity - kgCO₂e/MWh'],
                price_aud_per_mwh=row['Price - AUD/MWh']

            )
            
            # add the object to the list for bulk insert
            data_to_insert.append(electric)

        # check if database is ready before attempting to load data
        if database_state is True:
            try:
                data_to_load=transformed_data
                task_logger.info(data_to_load)
                task_logger.info(f"transformed data is ready to load")

                # apply the create_object function to each row in the dataframe
                data_to_load.apply(lambda row:create_object(row), axis=1)
                
                # insert all Electric objects into the database
                with Session(engine) as session:
                    session.add_all(data_to_insert)
                    session.commit()
                    return "Loading is complete"

            except Exception as e:
                task_logger.warning(f"Not able to establish coonection with database")
                return "Stop and check database connection"
            
        else:
            task_logger.warning(f"database not initiazed skip loading")
            return "Skipped load due to database error"
    """
     Run the full data pipeline(ETL) step-by-step:
    1. initialize the database
    2. Extract raw data
    3. Transform the extracted data
    4. Load the transformed data into the database
    """      
    starting_database=database_initialization()
    extraction=extract()
    transformation=transform(extraction)
    loading=load(transformation, starting_database)

# Trigger the entire energy data workflow
energy_worflow()

        
   
