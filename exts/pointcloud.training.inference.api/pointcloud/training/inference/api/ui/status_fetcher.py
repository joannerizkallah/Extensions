import omni.ui as ui
import json
import logging
import omni.kit.notification_manager as nm
from omni.kit.window.popup_dialog import MessageDialog
from pointcloud.training.inference.api.infrastructure.clients.training_client import TrainingClient
from pointcloud.training.inference.api.utils.training_info import TrainingInfo
class Status:
    def __init__(self, logger : logging):
        self.client : TrainingClient = TrainingClient(logger=logger)
        self.train_counts : int = 0
        self.response_label : ui.Grid = None

    def build_ui(self):

        def get_status():
            #Send GET request directly
            self.train_counts = 0
            response = self.client.status_endpoint()

            if response.status_code == 200:
                json_data = json.loads(response.text)
                output = ""
                for train_data in json_data:
                    train = TrainingInfo(**train_data)
                    self.train_counts+=1

                self.response_label.text = response.text
                #nm.post_notification(output, hide_after_timeout=False, status=nm.NotificationStatus.INFO)
                dialog = MessageDialog(title = "Testing" ,message = output, ok_handler=lambda dialog: print(f"Message acknowledged"))
                self.response_label.style = {"color" : ui.color(0,255,0)}
            else:
                self.response_label.text = response.text
                self.response_label.style = {"color" : ui.color(255,0,0)}

        with ui.HStack(length = 10):
            ui.Button("Get status of trainings", clicked_fn = get_status)
            with ui.ScrollingFrame(height = 60, style = {"alignment" : ui.Alignment.H_CENTER}):
                self.response_label = ui.Label("Status will show here")