import omni.ui as ui
import requests
import logging
from pointcloud.training.inference.api.utils.helper_functions import register_option, get_reset_glyph
from pointcloud.training.inference.api.infrastructure.clients.training_client import TrainingClient
from pointcloud.training.inference.api.infrastructure.parameter_control import RenameParams

class RenameTrain:

    def __init__(self, logger : logging):
        self.client : TrainingClient = TrainingClient(logger=logger)
        self.params : dict = {
            "uuid" : None,
            "new_training_path" : None
        }

        self.response_label : ui.Label = None
    
    def build_ui(self):

        def refresh():
            #Remove old contents of ui.ComboBox
            items = uuid_ui.model.get_item_children()
            for item in items:
                uuid_ui.model.remove_item(item)
            
            #Retrieve new training uuids available by sending a get request from the client
            available_trains = self.client.retrieve_available_trains()["uuid"]
            for uuid in available_trains:
                #Update ComboBox
                uuid_ui.model.append_child_item(None, ui.SimpleStringModel(uuid))

        def change_name():

            #Assign parameters used in PATCH request
            self.params["new_training_path"] = new_training_path_ui.model.get_value_as_string()
            self.params["uuid"] = register_option(uuid_ui, self.client.retrieve_available_trains()["uuid"])

            #Utilizing pydantic to pass parameters to client
            api_params = RenameParams(**self.params)

            #Create PATCH request
            response = self.client.rename_endpoint(params=api_params)

            #Change label coloring according to response status code
            if response.status_code == 200:
                self.response_label.text = f"Successfully renamed training"
                self.response_label.style = {"color" : ui.color(0,255,0)}
            else:
                self.response_label.text = response.text
                self.response_label.style = {"color" : ui.color(255,0,0)}

        with ui.VStack(height = 12):
            with ui.HStack(height = 10, width = 1000):
                ui.Label("Enter uuid")
                uuid_ui : ui.ComboBox = ui.ComboBox(0, *self.client.retrieve_available_trains()["uuid"])

                ui.Button(f"{get_reset_glyph()}", width =20, clicked_fn = refresh, tooltip = "Refresh names")
            with ui.HStack(height = 10, width =1000):
                ui.Label("Enter new training path")
                new_training_path_ui : ui.StringField = ui.StringField()

            self.response_label = ui.Label("")
            ui.Button("Rename Training Logs Directory", clicked_fn = change_name)
