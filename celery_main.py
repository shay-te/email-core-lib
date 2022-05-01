import logging

import hydra
from celery import Celery

from core_lib.data_layers.data.data_helpers import build_url
from email_core_lib.email_core_lib import EmailCoreLib


@hydra.main(config_path='email_core_lib/config', config_name='email_core_lib')
def main(cfg):
    email_core_lib = EmailCoreLib(cfg)
    app = Celery('task', broker=build_url(**cfg.core_lib.email_core_lib.amqp.url))

    @app.task()
    def send(template_id, params):
        email_core_lib.send(template_id, params)

    argv = [
        'worker',
        '--loglevel=INFO',
        '-P',
        'eventlet',
        '--without-gossip',
        '--without-mingle',
        '-Ofair',
        '--pool=solo',
    ]
    app.worker_main(argv)


if __name__ == '__main__':
    main()
