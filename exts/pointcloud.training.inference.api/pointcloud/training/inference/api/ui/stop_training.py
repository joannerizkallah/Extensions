import omni.ui as ui
import logging
from pointcloud.training.inference.api.utils.helper_functions import *
from pointcloud.training.inference.api.infrastructure.parameter_control import StopParams
from pointcloud.training.inference.api.infrastructure.clients.training_client import TrainingClient

class StopTraining:

    def __init__(self, logger : logging):
        self.client : TrainingClient = TrainingClient(logger=logger) 
        self.params : dict = {
            "uuid" : None,
            "delete_logs" : None,
        }
        self.delete_options = ["--", False, True]

    def build_ui(self):
        def refresh():
            items = uuid_ui.model.get_item_children()
            for item in items:
                uuid_ui.model.remove_item(item)
            available_trains = self.client.retrieve_available_trains()["uuid"]
            for uuid in available_trains:
                uuid_ui.model.append_child_item(None, ui.SimpleStringModel(uuid))

        def register_uuid():
            self.params["uuid"] = register_option(uuid_ui, self.client.retrieve_available_trains()["uuid"])
            if self.params["uuid"] == "--":
                uuid_label.text = "Enter a uuid!"
                uuid_label.style = {"color" : ui.color(255,0,0)}

        def stop_training():
            self.params["delete_logs"] = register_option(delete_logs_ui, self.delete_options)
            if self.params["delete_logs"] == "--":
                delete_logs_label.text = "Select a valid option"
                delete_logs_label.style = {"color" : ui.color(255,0,0)}
                return
            
            register_uuid()

            api_params = StopParams(**self.params)
            response = self.client.stop_endpoint(params=api_params)

            if response.status_code == 200:
                if self.params["delete_logs"]:
                    stopping_status_label.text = "Logs deleted, training stopped"
                else:
                    stopping_status_label.text = "Logs not deleted, training stopped"
                stopping_status_label.style = {"color" : ui.color(0,255,23)}
            else:
                stopping_status_label.text = response.text
                stopping_status_label.style = {"color" : ui.color(255,0,0)}

        with ui.VStack(height = 12):
            uuid_label = ui.Label("uuid", style={"color": ui.color(200, 162, 200)})
            with ui.HStack(height=10, width=1000):
                uuid_ui : ui.ComboBox = ui.ComboBox(0, *self.client.retrieve_available_trains()["uuid"])
                ui.Button(f"{get_reset_glyph()}", width =20, clicked_fn = refresh, tooltip = "Refresh uuid")
            delete_logs_label : ui.Label = ui.Label("Delete logs", style={"color": ui.color(200, 162, 200)})
            delete_logs_ui : ui.ComboBox = ui.ComboBox(0, "--", "False", "True")

            ui.Button("Stop Training", clicked_fn = stop_training)
            stopping_status_label : ui.Label = ui.Label("Stopping status", style={"color": ui.color(200, 162, 200)})