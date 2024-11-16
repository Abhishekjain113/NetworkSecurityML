import os
import sys
import json
import certifi
import pandas as pd
import pymongo
from dotenv import load_dotenv
from networkSecurity.Exception.exception import NetworkSecurityException
from networkSecurity.logging.logger import logging

# Load environment variables
load_dotenv()

# Fetch MongoDB connection URL
MONGO_DB_URL = os.getenv('MOGNO_URL')  # Ensure correct variable name in `.env`
if not MONGO_DB_URL:
    raise ValueError("Environment variable `MONGO_URL` not found or is empty.")
print(f"MONGO_DB_URL: {MONGO_DB_URL}")

# Certificate Authority for secure MongoDB connection
ca = certifi.where()


class NetworkDataExtract:
    def __init__(self):
        try:
            logging.info("NetworkDataExtract object initialized successfully.")
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def cv_to_json_convertor(self, file_path):
        """
        Convert CSV file data to JSON format compatible with MongoDB.
        """
        try:
            logging.info(f"Reading CSV file from path: {file_path}")
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            # Convert DataFrame to JSON format (list of dictionaries)
            record = json.loads(data.to_json(orient='records'))
            logging.info(f"CSV data converted to JSON with {len(record)} records.")
            return record
        except Exception as e:
            logging.error("Error in cv_to_json_convertor method.")
            raise NetworkSecurityException(e, sys)

    def insert_data_mongodb(self, record, db, collection):
        """
        Insert JSON data into MongoDB collection.
        """
        try:
            logging.info(f"Connecting to MongoDB database: {db}, collection: {collection}")
            # Create MongoDB client
            mongo_client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)
            
            # Access the database and collection
            database = mongo_client[db]
            collection_obj = database[collection]
            
            # Insert data into MongoDB
            result = collection_obj.insert_many(record)
            logging.info(f"{len(result.inserted_ids)} records inserted into MongoDB.")
            return len(result.inserted_ids)
        except Exception as e:
            logging.error("Error in insert_data_mongodb method.")
            raise NetworkSecurityException(e, sys)


if __name__ == '__main__':
    # Input data file path
    FILE_PATH = '/home/jainabhi/ML/Network_security/network_data/phisingData.csv'
    DATABASE = 'NWS'
    COLLECTION = 'NetworkData'
    
    try:
        # Create an instance of the class
        network_obj = NetworkDataExtract()
        
        # Convert CSV to JSON
        records = network_obj.cv_to_json_convertor(file_path=FILE_PATH)
        print(f"Records to insert: {len(records)}")
        
        # Insert JSON records into MongoDB
        no_of_records = network_obj.insert_data_mongodb(records, DATABASE, COLLECTION)
        print(f"Number of records inserted: {no_of_records}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")
