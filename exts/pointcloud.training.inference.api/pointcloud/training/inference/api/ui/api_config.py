import omni.ui as ui
import omni
import logging
from pointcloud.training.inference.api.utils.helper_functions import *
from pointcloud.training.inference.api.infrastructure.clients.training_client import TrainingClient

class ApiConfig:
    api_url = None
    port = None
    def __init__(self, name: str, url:str, port:int):
        self.name = name
        self.url : str = url
        self.port : int = port

class APIConfigUI:
    def __init__(self, logger:logging):
        self.endpoints : dict = {}
        self.list_new_configs : dict = {}
        self.list_configs : dict = {}
        self.list_config_names : List[str] = []
        self.client : TrainingClient = TrainingClient(logger=logger)
        
    def build_ui(self):
        def send_config():
            option = register_option(configs_ui, self.list_config_names)
            config = self.list_configs.get(option)
            url = config["url"]
            port = config["port"]
            self.client.change_url_port(url = url, port = port)

        def show_configs():
            manager = omni.kit.app.get_app().get_extension_manager()
            ext_id = manager.get_enabled_extension_id("pointcloud.training.inference.api")
            ext_path = manager.get_extension_dict(ext_id)["path"]
            with open(os.path.join(ext_path, "config/clients.json"), "r") as f: 
                json_data = json.load(f)
                self.endpoints = json_data["endpoints"]

                for config in json_data["api_connectors"]:
                        url = json_data["api_connectors"][config]["url"]
                        port = json_data["api_connectors"][config]["port"]
                        self.list_config_names.append(config)

                        new_config = ApiConfig(name = config, url=url, port=port)
                        self.list_configs.update({new_config.name :{"url": new_config.url, "port" : new_config.port}})
            return self.list_configs
    
        def save_config():
            self.list_new_configs = {}
            name = name_ui.model.get_value_as_string()
            url= url_ui.model.get_value_as_string()
            port= port_ui.model.get_value_as_int()
            if name and url and port:
                new_config = ApiConfig(name = name, url=url, port=port)
                self.list_config_names.append(name)
                self.list_new_configs.update({new_config.name :{"url": new_config.url, "port" : new_config.port}})
                self.list_configs.update({new_config.name :{"url": new_config.url, "port" : new_config.port}})
                #Remove old contents of ui.ComboBox
                items = configs_ui.model.get_item_children()
                for item in items:
                    configs_ui.model.remove_item(item)
                #Retrieve new training names available by sending a get request from the client
                for name in self.list_configs:
                    #Update ComboBox
                    configs_ui.model.append_child_item(None, ui.SimpleStringModel(name)) 

                write_config(self.list_new_configs)
                
        def write_config(list_configs : dict):
            manager = omni.kit.app.get_app().get_extension_manager()
            ext_id = manager.get_enabled_extension_id("pointcloud.training.inference.api")
            ext_path = manager.get_extension_dict(ext_id)["path"]

            with open(os.path.join(ext_path, "config/clients.json"), 'r+') as file:
                # First we load existing data into a dict.
                file_data = json.load(file)
                # Join new_data with file_data inside emp_details
                file_data["api_connectors"].update(list_configs)
                # Sets file's current position at offset.
                file.seek(0)
                # convert back to json.
                json.dump(file_data, file, indent=4)   

        with ui.VStack(height = 30):
            
            with ui.HStack(width = 800):
                ui.Label("Name of config")
                name_ui = ui.StringField()
            ui.Separator(height=20)

            with ui.HStack(width = 800):
                ui.Label("Enter api url")
                url_ui = ui.StringField()
            ui.Separator(height=20)

            with ui.HStack(width = 800):
                ui.Label("Enter port number")
                port_ui = ui.StringField()
            ui.Button("Add config", clicked_fn = save_config)
            with ui.HStack(width=700):
                ui.Label("Select config")
                configs_ui : ui.ComboBox = ui.ComboBox(0, *show_configs())
            ui.Button("Use this config", clicked_fn = send_config)