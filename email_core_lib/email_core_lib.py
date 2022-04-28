from omegaconf import DictConfig
from core_lib.core_lib import CoreLib
from core_lib.helpers.config_instances import instantiate_config


class EmailCoreLib(CoreLib):
    def __init__(self, conf: DictConfig):
        super().__init__()
        self.config = conf
        self.mailchimp = instantiate_config(self.config.core_lib.email_core_lib.client)

    def send(self, template_id, params):
        self.mailchimp.send(template_id, params)

