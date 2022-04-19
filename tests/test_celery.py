import json
import os
import unittest
from time import sleep
import hydra
from dotenv import load_dotenv

import pika

from core_lib.data_layers.data.data_helpers import build_url

path = os.path.join(os.path.dirname(__file__), 'test_data')
load_dotenv(dotenv_path=os.path.join(path, '.env'))
hydra.initialize(config_path='test_data', caller_stack_depth=1)
cfg = hydra.compose('config.yaml')

connection = pika.BlockingConnection(pika.URLParameters(build_url(**cfg.core_lib.email_core_lib.amqp.url)))
channel = connection.channel()

queue_name = cfg.core_lib.email_core_lib.amqp.queue_name
channel.queue_declare(queue=queue_name, durable=True)


class Test(unittest.TestCase):
    def test(self):
        i = 1
        while i < 100:
            data = {"data": i, "user_id": 2, "msg_type": "SEND_EMAIL"}
            channel.basic_publish(exchange='hello',
                                  routing_key='routing_key',
                                  body=json.dumps(data).encode('utf-8'),
                                  )
            print('.')
            i += 1
            sleep(5)

