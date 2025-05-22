import logging

from omegaconf import DictConfig
from core_lib.core_lib import CoreLib
from core_lib.helpers.config_instances import instantiate_config


class EmailCoreLib(CoreLib):
    def __init__(self, conf: DictConfig):
        super().__init__()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.config = conf
        self.mail_client = instantiate_config(self.config.core_lib.email_core_lib.client)

    def send(self, template_id, params, sender_info):
        self.logger.info(f'send email. template_id: {template_id}, params: {params}, sender_info: {sender_info}')
        self.mail_client.send(template_id, params, sender_info)
