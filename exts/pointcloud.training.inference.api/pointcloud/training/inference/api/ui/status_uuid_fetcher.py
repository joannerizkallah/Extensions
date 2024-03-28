import omni.ui as ui
import logging
import json
from pointcloud.training.inference.api.utils.helper_functions import *
from pointcloud.training.inference.api.infrastructure.clients.training_client import TrainingClient
from pointcloud.training.inference.api.infrastructure.parameter_control import StatusUuidParams

class StatusUUID:
    
    def __init__(self, logger : logging):
        self.client : TrainingClient = TrainingClient(logger=logger)
        self.params : dict = {
             "uuid" : None
        }
        self.response_label : ui.Label = None

    def build_ui(self):

        def refresh():
            items = uuid_ui.model.get_item_children()
            for item in items:
                uuid_ui.model.remove_item(item)
            available_trains = self.client.retrieve_available_trains()["uuid"]
            for uuid in available_trains:
                uuid_ui.model.append_child_item(None, ui.SimpleStringModel(uuid))

        def get_status_uuid():
            self.params["uuid"] = register_option(uuid_ui, self.client.retrieve_available_trains()["uuid"])

            #Retrieve available uuids by sending a GET request. The function returns uuids, and names (that's why [:][0])
            available_uuids = (self.client.retrieve_available_trains())[:][0]

            #Change ui if uuid is not available
            if self.params["uuid"] not in available_uuids:
                 self.response_label.text = "Invalid uuid"
                 self.response_label.style = {"color" : ui.color(255,0,0)}
                 return
            
            #Pydantic to assign parameters for GET request
            api_params = StatusUuidParams(**self.params)

            #Send GET request
            response = self.client.status_uuid_endpoint(api_params)
            
            json_data = json.loads(response.text)
            output = ""
            for element in json_data:
                    output += f"{element}"
                    output += "\n"
            if response.status_code == 200:
                json_data = json.loads(response.text)
                output = ""
                for property in json_data:
                        output += f"{property}: {json_data[property]}\t"
                self.response_label.text = output
                self.response_label.style = {"color" : ui.color(0,255,0)}
            else:
                self.response_label.text = response.text
                self.response_label.style = {"color" : ui.color(255,0,0)}

        with ui.VStack():

            ui.Label("uuid",  style = {"color": ui.color(200,162,200)})
            with ui.HStack(height=10, width=1000):
                uuid_ui : ui.ComboBox = ui.ComboBox(0, *self.client.retrieve_available_trains()["uuid"])
                ui.Button(f"{get_reset_glyph()}", width =20, clicked_fn = refresh, tooltip = "Refresh uuid")
            
            ui.Button("Get status of trainings", clicked_fn = get_status_uuid)
            with ui.VStack():
                with ui.ScrollingFrame(height = 60, style = {"alignment" : ui.Alignment.H_CENTER}):
                    with ui.VStack(height = 10):
                        self.response_label = ui.Label("Status of all trainings will show here")