import hydra
from celery import Celery

from core_lib.data_layers.data.data_helpers import build_url
from email_core_lib.email_core_lib import EmailCoreLib


@hydra.main(config_path='.', config_name='core_lib_config.yaml')
def main(cfg):
    email_core_lib = EmailCoreLib(cfg)
    app = Celery('task', broker=build_url(**cfg.core_lib.email_core_lib.amqp.url))

    @app.task()
    def send(template_id, params, sender_info):
        email_core_lib.send(template_id, params, sender_info)

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
