import hydra
from kombu import Consumer, Queue, Exchange
from omegaconf import DictConfig
from core_lib.core_lib import CoreLib
from celery import Celery, bootsteps

from core_lib.data_layers.data.data_helpers import build_url


class EmailCoreLib(CoreLib):
    def __init__(self, conf: DictConfig):
        super().__init__()
        self.config = conf

    class ConsumerStep(bootsteps.ConsumerStep):

        def get_consumers(self, channel):
            return [Consumer(channel,
                             queues=[Queue('hello', Exchange('hello'), 'routing_key')],
                             callbacks=[self.handle_message],
                             accept=['json'])]

        def handle_message(self, body, message):
            print('Received message: {0!r}'.format(body))
            message.ack()


@hydra.main(config_path='./config', config_name='email_core_lib')
def main(cfg):
    email_cl = EmailCoreLib(cfg)
    app = Celery(broker=build_url(**cfg.core_lib.email_core_lib.amqp.url))
    app.steps['consumer'].add(email_cl.ConsumerStep)
    worker = app.Worker()
    worker.start()


if __name__ == '__main__':
    main()
