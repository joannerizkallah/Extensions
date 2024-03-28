import json
import omni
import omni.ui as ui
import os
from pointcloud.training.inference.api.infrastructure.clients.training_client import TrainingClient

#Used to register selected option in ui.ComboBox
def register_option(ui_model : ui.ComboBox, options : list):
    value_model = ui_model.model.get_item_value_model()
    current_index = value_model.as_int
    option = options[current_index]
    return option

def present_output(response_txt : str) -> str:
    """
    Present output of response in a clean way
    """
    json_data = json.loads(response_txt)
    output = ""
    for train in json_data:
        output += f"{train}: {json_data[train]}"
        output += "\t"

    return output

#Obtain the glyph used for refresh
def get_reset_glyph() -> ui:
    return ui.get_custom_glyph_code("${glyphs}/menu_refresh.svg")

#used to refresh gpu ids in ui
def refresh_gpu_id(gpu_ui : ui, client: TrainingClient):
    #Remove old contents of ui.ComboBox
    items = gpu_ui.model.get_item_children()
    for item in items:
        gpu_ui.model.remove_item(item)
    #Retrieve new training names available by sending a get request from the client
    available = client.get_available_gpu()
    for id in available:
        #Update ComboBox
        gpu_ui.model.append_child_item(None, ui.SimpleIntModel(int(id)))

#used to refresh training names
def refresh_trainings(ui_entity : ui, client: TrainingClient, key: str):
    #Remove old contents of ui.ComboBox
    items = ui_entity.model.get_item_children()
    for item in items:
        ui_entity.model.remove_item(item)
    #Retrieve new training names available by sending a get request from the client
    available = client.retrieve_available_trains()[key]
    for name in available:
        #Update ComboBox
        ui_entity.model.append_child_item(None, ui.SimpleStringModel(name))

#used to refresh either training configs or dataset configs 
def refresh_file_paths(ui_entity : ui, retrieve_fn : callable):
    #Remove old contents of ui.ComboBox
    items = ui_entity.model.get_item_children()
    for item in items:
        ui_entity.model.remove_item(item)
    #Retrieve new training names available by sending a get request from the client
    available= retrieve_fn()
    for name in available:
        #Update ComboBox
        ui_entity.model.append_child_item(None, ui.SimpleStringModel(name)) 

