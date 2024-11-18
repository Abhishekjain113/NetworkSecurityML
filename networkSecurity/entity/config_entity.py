from datetime import datetime
from networkSecurity.constant import training_pipleine
import os 
import sys

class TrainingPipelineConfig:
    def __init__(self,timestamp=datetime.now()):
        timestamp=timestamp.strftime("%m,%d,%H,%M,%S")
        self.pipeline_name=training_pipleine.PIPELINE_NAME
        self.artifacts_name=training_pipleine.ARTIFACT_DIR
        self.artifacts_dir=os.path.join(self.artifacts_name,timestamp)
        self.timestamp: str=timestamp



class DataIngestionConfig:
    def __init__(self,training_pipleine_config:TrainingPipelineConfig):
        self.data_ingestion_dir:str=os.path.join(
            training_pipleine_config.artifacts_dir,
            training_pipleine.DATA_INGESTION_DIR_NAME
        )
        self.feature_store_file_path: str = os.path.join(
                self.data_ingestion_dir, training_pipleine.DATA_INGESTION_FEATURE_STORE_DIR, training_pipleine.FILE_NAME
            )
        self.training_file_path: str = os.path.join(
                self.data_ingestion_dir, training_pipleine.DATA_INGESTION_INGESTED_DIR, training_pipleine.TRAIN_FILE_NAME
            )
        self.testing_file_path: str = os.path.join(
                self.data_ingestion_dir, training_pipleine.DATA_INGESTION_INGESTED_DIR, training_pipleine.TEST_FILE_NAME
            )
        
        self.train_test_split_ration:float=training_pipleine.DATA_INGESTION_TRAIN_TEST_SPLIT_RATION
        self.collection_name:str=training_pipleine.DATA_INGESTION_COLLECTION_NAME
        self.database_name:str=training_pipleine.DATA_INGESTION_DATABASE_NAME



        
        
