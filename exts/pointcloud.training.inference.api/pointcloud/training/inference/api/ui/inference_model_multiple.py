import omni.ui as ui
import logging
import os
from typing import List
from omni.kit.window.filepicker import FilePickerDialog
from pointcloud.training.inference.api.utils.helper_functions import *
from pointcloud.training.inference.api.utils.filepicker_utils import open_file_dialog, click_open_startup
from pointcloud.training.inference.api.infrastructure.parameter_control import InferParams
from pointcloud.training.inference.api.infrastructure.clients.training_client import TrainingClient
import numpy as np

class InferenceMultiple:

    def __init__(self, logger : logging):
        self.client : TrainingClient = TrainingClient(logger=logger)
        self.params : dict = {
            "point_cloud_path": None, 
            "training_name": None
        }
        self.referesh = None
        self.list_pcd : List[str] = []
        self.list_checkboxes :List[ui.CheckBox.model]= []
        self.valid_params : bool = False

    def build_ui(self):


        def register_training_name():
            self.params["training_name"] = register_option(training_name_ui, self.client.retrieve_available_trains()["training_names"])

        
        def infer():
            register_training_name()
            if self.params["training_name"]:
                for box in self.list_checkboxes:
                    if box[0].as_bool:
                        self.list_pcd.append(box[1])
                for pcd in self.list_pcd:
                    self.params["point_cloud_path"] = pcd
                    api_params = InferParams(**self.params)
                    response = self.client.infer_endpoint(params=api_params)
                    if response.status_code == 200:
                        info_label.text = "Inferring"
                        info_label.style = {"color" : ui.color(0,255,0)}
                    else:
                        info_label.text = response.text
                        info_label.style = {"color" : ui.color(255,0,0)}
            else:
                info_label.text = "Make surer to pick a point cloud and a training name"
                info_label.style = {"color" : ui.color(255,0,0)}
        with ui.VStack():

            ui.Label("Training name")
            with ui.HStack(width=600):
                training_name_ui : ui.ComboBox = ui.ComboBox(0, *self.client.retrieve_available_trains()["training_names"])
                ui.Button(f"{get_reset_glyph()}", width =20, clicked_fn = refresh_trainings(training_name_ui, self.client, "training_names"), tooltip = "Refresh names")

            with ui.HStack(height=10, width=1300):
                list_pcd = self.client.retrieve_pcd_inference_files()
            for pcd in list_pcd:
                with ui.VStack():
                    with ui.HStack(width=600):
                        ui.Label(str(pcd))
                        checkbox = ui.CheckBox(width=100)
                        self.list_checkboxes.append([checkbox.model, pcd])
            with ui.VStack():
                ui.Button("Infer", clicked_fn = infer)
                info_label : ui.Label = ui.Label("", style={"color": ui.color(255, 255, 0)})
            with ui.CanvasFrame(height = 70):
                list_pcd_ui : ui.Label = ui.Label("Selected pcds will show here")