#!python3

from abc import ABC, abstractmethod
import src.misc.config as global_config

class DefaultState(ABC):

    def __init__(self):
        self.ascii_art_obj = None
        self.ascii_art_path = None
        self.application_window_obj = None
        self.application_window_interface = None
        self.environmental_references = global_config

    @abstractmethod
    def toggle_self(self):
        pass
