from omegaconf import DictConfig
from core_lib.core_lib import CoreLib
from email_core_lib.client.mailchimp_client import MailChimpClient


class EmailCoreLib(CoreLib):
    def __init__(self, conf: DictConfig):
        super().__init__()
        self.config = conf
        self.mailchimp = MailChimpClient(self.config.core_lib.email_core_lib.client.token)

    def send(self, template_id, params):
        self.mailchimp.send(template_id, params)

