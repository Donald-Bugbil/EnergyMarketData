import os
from dotenv import load_dotenv
load_dotenv()

#AWS S3 credentials
SECRET_KEY=os.environ['SECRET_KEY']
ACCESS_KEY=os.environ['ACCESS_KEY']
BUCKET_NAME=os.environ['BUCKET_NAME']