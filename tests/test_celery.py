import os
import unittest
import hydra
from celery import Celery
from dotenv import load_dotenv

from core_lib.data_layers.data.data_helpers import build_url

path = os.path.join(os.path.dirname(__file__), 'test_data')
load_dotenv(dotenv_path=os.path.join(path, '.env'))
hydra.initialize(config_path='test_data', caller_stack_depth=1)
cfg = hydra.compose('config.yaml')

app = Celery(broker=build_url(**cfg.core_lib.email_core_lib.amqp.url))
app.autodiscover_tasks()


class Test(unittest.TestCase):
    def test(self):
        app.send_task('task.send',
                      ['register_complete', {'email': 'shay@objectivelove.com'}])
