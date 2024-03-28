import requests
from requests import RequestException, Response
import logging
from logging import Logger
import time
import json
import os
from typing import List
from pathlib import Path
#from circuitbreaker import CircuitBreaker, CircuitBreakerMonitor, CircuitBreakerError
from pointcloud.training.inference.api.domain.exceptions.infrastructure_api_client_exception import *
from pointcloud.training.inference.api.infrastructure.parameter_control import *

import omni.kit.app

class TrainingClient:
    url = None
    api_url = None
    port = None
    endpoints = None

    def __init__(self):
        self.endpoints = None
        self.logger : Logger = logging.getLogger(name = "Pointcloud Training Inference API Logger")
        logging.basicConfig(filename = "logs/client_logging.log", encoding = 'utf-8', level = logging.DEBUG)
        self.logger.debug("Initializing Pointcloud Training Inference API Client")
        
        manager = omni.kit.app.get_app().get_extension_manager()
        ext_id = manager.get_enabled_extension_id("pointcloud.training.inference.api")
        ext_path = manager.get_extension_dict(ext_id)["path"]
        self.MAX_RETRIES = 6

        with open(os.path.join(ext_path, "config/clients.json"), "r") as f: 
            json_data = json.load(f)
            self.endpoints = json_data["endpoints"]

            for config in json_data["api_connectors"]:
                if config == "default":
                    self.url = json_data["api_connectors"][config]["url"]
                    self.port = json_data["api_connectors"][config]["port"]
                break
        self.api_url = self.url + ":" + str(self.port)

    def _request_external_api_health(self) -> bool:
        self.logger.debug("Checking API health")
        try:
            request = requests.get(url = os.path.join(self.api_url, self.endpoints["health_endpoint"])) 
            return request
        except RequestException as e:
            raise e
        except Exception as ex:
            raise ex
        
        
    def check_external_api_health(self) -> bool:
        for i in range(10):
            try:
                request = self._request_external_api_health()
                if request:
                    return True
                time.sleep(2)
            except:
                pass
        raise AppException(additional_info="Please check API port")
    
    def _get_external_call(self, url, request_body: dict, retry_count:int = 0) -> Response:
        try:
            self.logger.debug(f"Sending GET Request to Pointcloud Training Inference API on url: {url}")
            response = requests.get(url = url, params= request_body)
            return response
        except requests.exceptions.ConnectionError as e:
            self.logger.error(f"GET Request to Pointcloud Training Inference API on url: {url} failed; error: {e}")
            
            if retry_count < self.MAX_RETRIES:
                self.logger.debug(f"Retrying GET Request to Pointcloud Training Inference API url: {url}")
                time.sleep(2)
                return self._get_external_call(url = url, retry_count= retry_count+1)
            raise e
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error while trying to communicate with Pointcloud Training Inference API GET Request URL: {url}; Request Body: {request_body}; Exception Occured {e.__str__()}")
            raise e
        
    def _patch_external_call(self, url, request_body: dict, retry_count: int = 0) -> Response:
        try:
            self.logger.debug(f"Trying PATCH Request to Pointcloud Training Inference API on URL : {url}")
            response = requests.patch(url = url, params = request_body)
            return response
        except requests.exceptions.ConnectionError as e:
            self.logger.error(f"PATCH Request to Pointcloud Training Inference API on URL: {url} failed; error: {e}")

            if retry_count < self.MAX_RETRIES:
                self.logger.debug(f"Retrying PATCH Request to Pointcloud Training Inference API on URL: {url}")
                time.sleep(2)
                return self._post_external_call(url=url, request_body=request_body, retry_count=retry_count+1)
            raise e
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error while communicating with Pointcloud Training Inference API PATCH Request URL: {url}; Request Body: {request_body}; Exception Occured {e.__str__()}")
            raise e

    def _delete_external_call(self, url, request_body: dict, retry_count : int = 0) -> Response:
        try:
            self.logger.debug(f"Trying DELETE Request to Pointcloud Training Inference API on url: {url}")
            response = requests.delete(url = url, params = request_body)
            return response
        except requests.exceptions.RequestException as e:
            self.logger.error(f"DELETE Request to Pointcloud Training Inference API on URL: {url} failed; error: {e}")

            if retry_count < self.MAX_RETRIES:
                self.logger.debug(f"Retrying DELETE Request to Pointcloud Training Inference API on URL: {url}")
                time.sleep(2)
                return self._delete_external_call(url=url, request_body=request_body, retry_count=retry_count+1)
            raise e
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error while trying to communicate with Pointcloud Training Inference API DELETE Request on URL: {url}, Request Body: {request_body}; Exception Occured {e.__str__()}")
            raise e
        
    # endpoints
        
    def train_endpoint(self, params : TrainingParams) -> Response:
        self.logger.debug(f"POINTCLOUD TRAINING INFERENCE API Communication: Training Model")

        url: str = os.path.join(self.api_url, self.endpoints["train_endpoint"])
        params = dict(params)
        response = self._get_external_call(url = url, request_body=params)

        if response.status_code == 200:
            self.logger.debug(f"Pointcloud Training Inference API GET Request successful: {response.text}")
            return response
        else:
            self.logger.error(f"Pointcloud Training Inference API GET Request {url} failed! {response.text}")
            raise AppException(additional_info= response.text)
        
    def test_endpoint(self, params : TestParams) -> Response:
        self.logger.debug(f"POINTCLOUD TRAINING INFERENCE API Communication: Test Model")

        url: str = os.path.join(self.api_url, self.endpoints["test_endpoint"])
        params = dict(params)
        response : Response= self._get_external_call(url = url, request_body=params)

        if response.status_code != 200:
            self.logger.error(f"Pointcloud Training Inference API GET Request {url} failed! {response.text}")
            raise AppException(additional_info=response.text)
        return response
    
    def infer_endpoint(self, params : InferParams) -> Response:
        self.logger.debug(f"POINTCLOUD TRAINING INFERENCE API Communication: Test Model")

        url: str = os.path.join(self.api_url, self.endpoints["infer_endpoint"])
        #params.point_cloud_path = self.
        params = dict(params)
        response = self._get_external_call(url = url, request_body=params)

        if response.status_code != 200:
            self.logger.error(f"Pointcloud Training Inference API GET Request {url} failed! {response.text}")
            raise AppException(additional_info= "") #response.text
        return response
    
    def stop_endpoint(self, params : StopParams) -> Response:
        self.logger.debug(f"POINTCLOUD TRAINING INFERENCE API Communication: Test Model")

        url: str = os.path.join(str(self.api_url), self.endpoints["stop_training_endpoint"])
        params = dict(params)
        response = self._delete_external_call(url = url, request_body=params)

        if response.status_code != 200:
            self.logger.error(f"Pointcloud Training Inference API GET Request {url} failed! {response.text}")
            raise AppException(additional_info=response.text)
        return response
    
    def rename_endpoint(self, params : RenameParams) -> Response:
        self.logger.debug(f"POINTCLOUD TRAINING INFERENCE API Communication: Test Model")

        url: str = os.path.join(str(self.api_url), self.endpoints["rename_training_endpoint"])
        params = dict(params)
        response = self._patch_external_call(url = url, request_body=params)

        if response.status_code != 200:
            self.logger.error(f"Pointcloud Training Inference API GET Request {url} failed! {response.text}")
            raise AppException(additional_info=response.text)
        return response
    
    def status_endpoint(self) -> Response:
        self.logger.debug(f"POINTCLOUD TRAINING INFERENCE API Communication: Test Model")

        url: str = os.path.join(str(self.api_url), self.endpoints["status_endpoint"])
        response = self._get_external_call(url = url, request_body=None)

        if response.status_code != 200:
            self.logger.error(f"Pointcloud Training Inference API GET Request {url} failed! {response.text}")
            raise AppException(additional_info=response.text)
        return response    

    def status_uuid_endpoint(self, params : StatusUuidParams) -> Response:
        self.logger.debug(f"POINTCLOUD TRAINING INFERENCE API Communication: Test Model")

        url: str = os.path.join(str(self.api_url), self.endpoints["status_uuid_endpoint"]) + "/" + params.uuid
        params = dict(params)
        response = self._get_external_call(url = url, request_body=params)

        if response.status_code != 200:
            self.logger.error(f"Pointcloud Training Inference API GET Request {url} failed! {response.text}")
            raise AppException(additional_info=response.text)
        return response
        
    # helper endpoints
    def get_available_gpu(self):
        response = requests.get(os.path.join(self.api_url,self.endpoints["gpus_endpoint"]))
        if response.status_code != 200:
            self.logger.error(f'Pointcloud Training Inference API GET Request {self.endpoints["gpus_endpoint"]} failed! {response.text}')
            raise AppException(additional_info=response.text)
        gpus = response.json()
        gpus_list = []
        for gpu in gpus:
            gpus_list.append(gpu)
        return gpus_list

    def get_files_endpoint(self, url : str):
        configs = []
        response = self._get_external_call(url = url, request_body=None)
        if response.status_code == 200:
            configs_json = json.loads(response.text)
        else:
            raise AppException(additional_info=response.text)

        for i in range(len(configs_json)):
            configs.append(configs_json[i])

        return configs

    def find_clean_datasets_available(self):
        datasets = []
        response = self._get_external_call(url= os.path.join(str(self.api_url),str(self.endpoints["dataset_endpoint"])), request_body=None)
        self.logger.debug(os.path.join(str(self.api_url),self.endpoints["dataset_endpoint"]))
        if response.status_code == 200:
            self.logger.debug(f"Pointcloud Training Inference API GET Request successful: {response.text}")
            datasets_json = json.loads(response.text)
        else:
            self.logger.error(f"Pointcloud Training Inference API GET Request failed! {response.text}")
            raise AppException(additional_info=response.text)
        
        for i in range(len(datasets_json)):
            datasets.append(datasets_json[i]["name"])

        return datasets

    def find_dataset_configs(self):
        dataset_configs = self.get_files_endpoint(os.path.join(self.api_url, self.endpoints["dataset_config_files_endpoint"]))

        return dataset_configs

    def find_training_configs(self):
        training_configs = self.get_files_endpoint(os.path.join(self.api_url, self.endpoints["training_config_files_endpoint"]))

        return training_configs

    def retrieve_available_trains(self):
        response = self._get_external_call(url = os.path.join(self.api_url, self.endpoints["status_endpoint"]), request_body=None)
        if response.status_code == 200:
            self.logger.debug(f"Pointcloud Training Inference API GET Request successful: {response.text}")
        else:
            self.logger.error(f"Pointcloud Training Inference API GET Request failed! {response.text}")
            raise AppException(additional_info=response.text)
        json_data = json.loads(response.text)
        uuids = []
        training_names = []
        available_training_names = []
        available_training_uuids = []
        for train in json_data:
            uuids.append(train["uuid"])
            training_names.append(train["training_name"])
            if train["progress"] == 100:
                available_training_uuids.append(train["uuid"])
                available_training_names.append(train["training_name"])
            
        return {"uuid": uuids, "training_names" : training_names, "available_training_names": available_training_names}
    
    def change_url_port(self, url: str, port: int):
        self.api_url = url + ":" + str(port)

    def retrieve_pcd_inference_files(self) -> List:
        return self.get_files_endpoint(os.path.join(self.api_url,self.endpoints["list_pcd_inference_files_endpoint"]))