import omni.ui as ui
import logging
from pointcloud.training.inference.api.utils.helper_functions import *
from pointcloud.training.inference.api.infrastructure.clients.training_client import TrainingClient
from pointcloud.training.inference.api.infrastructure.parameter_control import TestParams

class Test:
    def __init__(self, logger: logging):
        self.client : TrainingClient = TrainingClient(logger=logger)
        self.params : dict = {
            "training_name" : None,
            "dataset_path" : None,
            "dataset_config_file_path" : None,
            "gpu_id" : None
        }
        
    def build_ui(self):
        
        def test():
            #Assign parameters used in GET request
            self.params["dataset_path"] = register_option(dataset_path_ui, self.client.find_clean_datasets_available())
            self.params["dataset_config_file_path"] = register_option(dataset_config_file_path_ui, self.client.find_dataset_configs())
            self.params["training_name"] = register_option(training_name_ui, self.client.retrieve_available_trains()["training_names"])
            self.params["gpu_id"] = register_option(gpu_id_ui, self.client.get_available_gpu())

            #Utilizing pydantic to pass parameters to client
            api_params = TestParams(**self.params)

            #Create GET request
            response = self.client.test_endpoint(params = api_params)

            #Change label coloring according to response status code
            if response.status_code == 200:
                self.response_text.text = f"uuid: {response.text}"
                self.response_text.style = {"color": ui.color(0, 255, 0)}

            else:
                self.response_text.text = f"{response.text}"
                self.response_text.style = {"color": ui.color(255, 0, 0)}

        with ui.VStack(height = 10):

            ui.Label("Training name", style = {"color" : ui.color(200,162,200)})
            with ui.HStack(height=10,width=1000):
                training_name_ui : ui.ComboBox = ui.ComboBox(0, *self.client.retrieve_available_trains()["training_names"])
                ui.Button(f"{get_reset_glyph()}", width =20, clicked_fn = refresh_trainings(training_name_ui, self.client, "training_names"), tooltip = "Refresh names")
            
            ui.Label("Dataset path relative to datasets/clean", style = {"color" : ui.color(200,162,200)})
            with ui.HStack(height=10,width=1000):
                dataset_path_ui : ui.ComboBox = ui.ComboBox(0, *self.client.find_clean_datasets_available())
                ui.Button(f"{get_reset_glyph()}", width =20, clicked_fn = refresh_file_paths(dataset_path_ui, self.client.find_clean_datasets_available), tooltip = "Refresh datasets")

            ui.Label("Dataset config file path relative to config_files/dataset_config", style = {"color" : ui.color(200,162,200)})
            with ui.HStack(height=10,width=1000):
                dataset_config_file_path_ui : ui.ComboBox = ui.ComboBox(0, *self.client.find_dataset_configs())
                ui.Button(f"{get_reset_glyph()}", width =20, clicked_fn = refresh_file_paths(dataset_config_file_path_ui, self.client.find_dataset_configs), tooltip = "Refresh dataset configs")

            ui.Label("GPU id", style = {"color" : ui.color(200,162,200)})
            with ui.HStack(height=10,width=100):
                gpu_id_ui : ui.ComboBox = ui.ComboBox(0, *self.client.get_available_gpu())
                ui.Button(f"{get_reset_glyph()}", width =20, clicked_fn = refresh_gpu_id(gpu_id_ui, self.client), tooltip = "Refresh GPUs")

            ui.Button("Test model on dataset", clicked_fn = test)
            with ui.ScrollingFrame(height = 50):
                self.response_text : ui.Label = ui.Label("Testing results show up here")

