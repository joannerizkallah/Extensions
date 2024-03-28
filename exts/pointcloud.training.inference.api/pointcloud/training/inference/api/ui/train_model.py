import omni.ui as ui
import requests
import json
import logging
from pointcloud.training.inference.api.utils.helper_functions import *
from pointcloud.training.inference.api.infrastructure.clients.training_client import TrainingClient
from pointcloud.training.inference.api.infrastructure.parameter_control import TrainingParams

class TrainModel:

    def __init__(self, logger : logging):
        self.client : TrainingClient = TrainingClient(logger=logger)
        self.resume_options : List = ["--", False, True]
        self.params : dict = {
            "training_name" : None,
            "dataset_path" : None,
            "training_config_file_path" : None,
            "dataset_config_file_path" : None,
            "resume_training" : None,
            "gpu_id" : None
        }
        
    def build_ui(self):

        def run_train_endpoint():

            #Assign parameters used in get requests
            self.params["training_name"] = training_name_ui.model.get_value_as_string()
            self.params["gpu_id"] = register_option(gpu_id_ui, self.client.get_available_gpu())
            self.params["dataset_path"] = register_option(dataset_path_ui, self.client.find_clean_datasets_available())
            self.params["training_config_file_path"] = register_option(training_config_file_path_ui, self.client.find_training_configs())
            self.params["dataset_config_file_path"] = register_option(dataset_config_file_path_ui, self.client.find_dataset_configs())
            self.params["resume_training"] = register_option(resume_training_ui, self.resume_options)

            #Utilizing pydantic to pass parameters to client
            api_params : TrainingParams = TrainingParams(**self.params)
            response = self.client.train_endpoint(params = api_params)

            #Change label coloring according to response status code
            if response.status_code == 200:
                training_response_label.text = present_output(response.text)
                training_response_label.style = {"color": ui.color(0, 255, 0)}

            else:
                training_response_label.text = response.text
                training_response_label.style = {"color": ui.color(255, 0, 0)}

        with ui.VStack(height = 60):
            ui.Label("Training name", style={"color": ui.color(200, 162, 200)})
            training_name_ui : ui.StringField = ui.StringField()


            ui.Label("Dataset path relative to datasets/clean/", style = {"color" : ui.color(200, 162, 200)})
            with ui.HStack(height=10, width=1000):
                dataset_path_ui = ui.ComboBox(0, *self.client.find_clean_datasets_available())
                #ui.Button(f"{get_reset_glyph()}", width =20, clicked_fn = refresh_file_paths(dataset_path_ui, self.client.find_clean_datasets_available), tooltip = "Refresh datasets")
                

            ui.Label("Training config file path relative to config_files/training_config/", style = {"color" : ui.color(200,162,200)})
            with ui.HStack(height=10, width=1000):
                training_config_file_path_ui : ui.ComboBox = ui.ComboBox(0, *self.client.find_training_configs())
                ui.Button(f"{get_reset_glyph()}", width =20, clicked_fn = refresh_file_paths(training_config_file_path_ui, self.client.find_training_configs), tooltip = "Refresh training configs")
            

            ui.Label("Dataset config file path relative to config_files/dataset_config/", style = {"color" : ui.color(200,162,200)})
            with ui.HStack(height=10, width=1000):
                dataset_config_file_path_ui : ui.ComboBox = ui.ComboBox(0, *self.client.find_dataset_configs())
                ui.Button(f"{get_reset_glyph()}", width =20, clicked_fn = refresh_file_paths(dataset_config_file_path_ui, self.client.find_dataset_configs), tooltip = "Refresh dataset configs")


            ui.Label("Resume training option", style = {"color" : ui.color(200,162,200)})
            resume_training_ui : ui.ComboBox = ui.ComboBox(0, "--", "False", "True")


            ui.Label("GPU ID", style = {"color" : ui.color(200,162,200)})
            with ui.HStack(height=10, width=1000):
                gpu_id_ui : ui.ComboBox = ui.ComboBox(0, *self.client.get_available_gpu())
                ui.Button(f"{get_reset_glyph()}", width =20, clicked_fn = refresh_gpu_id(gpu_id_ui, self.client), tooltip = "Refresh GPUs")


            ui.Button("Run Training", clicked_fn = run_train_endpoint)
            training_response_label : ui.Label = ui.Label("Training information", style={"color": ui.color(200, 162, 200)})