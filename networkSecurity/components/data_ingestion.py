import os
import sys
import numpy as np
import pandas as pd
import pymongo

from typing import List
from sklearn.model_selection import train_test_split

from networkSecurity.Exception.exception import NetworkSecurityException
from networkSecurity.entity.config_entity import DataIngestionConfig
from networkSecurity.entity.artifact_entity import DataIngestionArtifacts
from networkSecurity.logging.logger import logging

from dotenv import load_dotenv

# Load environment variables
load_dotenv()
MONGO_URL = os.getenv('MONGO_URL')


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_collection_as_dataframe(self):
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name

        # Test MongoDB connection
            logging.info(f"Connecting to MongoDB at {MONGO_URL}")
            self.mongo_client = pymongo.MongoClient(MONGO_URL)
            self.mongo_client.server_info()  # Forces connection test
            logging.info("Successfully connected to MongoDB")

        # Fetch collection data
            collection = self.mongo_client[database_name][collection_name]
            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df = df.drop(columns=['_id'], axis=1)
            df = df.replace({'na': np.nan})
            return df
        except Exception as e:
            logging.error(f"Failed to connect to MongoDB: {e}")
            raise NetworkSecurityException(e, sys)


    def split_data_as_train_test(self, dataframe: pd.DataFrame):
        """Splits the DataFrame into train and test sets and saves them as CSV files."""
        try:
            train_set, test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ration
            )
            logging.info('Performed train-test split on the dataframe')

            # Ensure directory exists
            dir_path = os.path.dirname(self.data_ingestion_config.testing_file_path)
            os.makedirs(dir_path, exist_ok=True)

            # Save train and test datasets
            train_set.to_csv(
                self.data_ingestion_config.training_file_path, index=False, header=True
            )
            test_set.to_csv(
                self.data_ingestion_config.testing_file_path, index=False, header=True
            )
            logging.info('Train and test file paths created successfully')
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_data_into_feature_store(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """Exports the DataFrame to the feature store."""
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)

            # Save the DataFrame to the feature store
            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            logging.info(f"Data successfully exported to feature store: {feature_store_file_path}")
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_ingestion(self) -> DataIngestionArtifacts:
        """Orchestrates the entire data ingestion process."""
        try:
            # Fetch data from MongoDB collection
            dataframe = self.export_collection_as_dataframe()
            logging.info(f"Dataframe shape after fetching from MongoDB: {dataframe.shape}")

            # Export data to feature store
            dataframe = self.export_data_into_feature_store(dataframe)

            # Perform train-test split
            self.split_data_as_train_test(dataframe)

            # Create and return artifact object
            data_ingestion_artifacts = DataIngestionArtifacts(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )
            logging.info("Data ingestion completed successfully")
            return data_ingestion_artifacts
        except Exception as e:
            raise NetworkSecurityException(e, sys)
