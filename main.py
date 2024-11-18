from networkSecurity.components.data_ingestion import DataIngestion
from networkSecurity.logging.logger import logging
from networkSecurity.Exception.exception import NetworkSecurityException
from networkSecurity.entity.config_entity import DataIngestionConfig
from networkSecurity.entity.config_entity import TrainingPipelineConfig
import sys

if __name__=='__main__':
    try:
        trainingPipelineConfig=TrainingPipelineConfig()
        dataingestionconfig=DataIngestionConfig(trainingPipelineConfig)
        data_ingestion=DataIngestion(dataingestionconfig)
        logging.info("Initiate the data ingestion")
        data_ingestionArtifacts=data_ingestion.initiate_data_ingestion()
        print(data_ingestionArtifacts)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
