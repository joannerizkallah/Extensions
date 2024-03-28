class TrainingInfo:
    def __init__(self, **kwargs):

        for key, value in kwargs.items():
            setattr(self,key,value)
        # uuid : str = None
        # gpu_id : int = None
        # container_id : str = None
        # training_name : str = None
        # container_name : str = None
        # training_config_file_path : str = None
        # dataset_config_file_path : str = None
        # status : str = None
        # status_message : str = None
        # results_ready : bool = None
        # progress : int = None
        # start_time: str = None
        # end_time : str = None

        def get_uuid(self):
            return self.uuid
        
        def get_gpu_id(self):
            return self.gpu_id
        
        def get_training_name(self):
            return self.training_name
        
        def get_status():
            return self.status
        
        def get_status_message():
            return self.status_message
        
        def get_results_ready():
            return self.results_ready
        
        def get_progress():
            return self.progress
        
        def get_start_time():
            return self.start_time
        
        def get_end_time():
            return self.end_time