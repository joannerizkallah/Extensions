import omni.ui as ui
import logging
from pointcloud.training.inference.api.ui.train_model import TrainModel
from pointcloud.training.inference.api.ui.test_model import Test
from pointcloud.training.inference.api.ui.stop_training import StopTraining
from pointcloud.training.inference.api.ui.rename_train_model import RenameTrain
from pointcloud.training.inference.api.ui.status_fetcher import Status
from pointcloud.training.inference.api.ui.status_uuid_fetcher import StatusUUID
from pointcloud.training.inference.api.ui.inference_model_multiple import InferenceMultiple
from pointcloud.training.inference.api.ui.api_config import APIConfigUI
class MainWindow(ui.Window):
    def __init__(self, title: str = None, **kwargs):
        super().__init__(title, **kwargs)
        self.logger: logging = logging.getLogger("Main Logger")
        self.frame.set_build_fn(self._build_window)

    def _build_window(self):
        config_menu = APIConfigUI(self.logger)
        train_model_menu = TrainModel(self.logger)
        inference_multiple_menu = InferenceMultiple(self.logger)
        test_menu = Test(self.logger)
        status_menu = Status(self.logger)
        status_uuid_menu = StatusUUID(self.logger)
        rename_menu = RenameTrain(self.logger)
        stop_training = StopTraining(self.logger)

        with ui.ScrollingFrame():
            with ui.VStack():
                with ui.CollapsableFrame("Configuration", height = 0):
                    with ui.Frame():
                        config_menu.build_ui()
                with ui.CollapsableFrame("Train", height = 0):
                    with ui.Frame():
                        train_model_menu.build_ui()
                with ui.CollapsableFrame("Infer Multiple Pcds", height = 0): 
                        inference_multiple_menu.build_ui()
                with ui.CollapsableFrame("Test", height = 0): 
                    with ui.Frame():
                        test_menu.build_ui()
                with ui.CollapsableFrame("Status", height = 20):
                    with ui.Frame():
                        status_menu.build_ui()
                with ui.CollapsableFrame("Check status of training by uuid", height = 30): 
                    status_uuid_menu.build_ui()
                with ui.CollapsableFrame("Rename", height = 0): 
                    with ui.Frame():
                        rename_menu.build_ui()
                with ui.CollapsableFrame("Stop Training", height = 0): 
                    with ui.Frame():
                        stop_training.build_ui()
                    
    def on_shutdown(self):
        pass