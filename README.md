# EmailCoreLib
`EmailCoreLib` uses [Celery](https://docs.celeryq.dev/en/stable/getting-started/introduction.html) and [MailChimp](https://mailchimp.com/) to receive data and send emails.
It uses `Celery` to listen to a queue and receive data over it, and `MailChimp` is used to fire emails using their [Transactional Email](https://mailchimp.com/features/transactional-email/) service.

## Services
- Send Emails using MailChimp
- Starts Celery Worker to handle requests

## Config 
```yaml
core_lib:
  email_core_lib:
    amqp:
      url:
        protocol: amqp
        username: ${oc.env:AMQP_USERNAME}
        password: ${oc.env:AMQP_PASSWORD}
        host: ${oc.env:AMQP_HOST}
        port: ${oc.env:AMQP_PORT}
    client:
      _target_: email_core_lib.client.mailchimp_client.MailChimpClient
      api_key: your_mailchimp_transactional_api_key
```

## celery_main.py
This is the main file that will start the `Celery` worker and initialize the `EmailCoreLib`. As soon as a task is 
dispatched for `task.send` it will use the `MailchimpTransactional` client to send the email.

## EmailCoreLib
```python
class EmailCoreLib(CoreLib):
    def __init__(self, conf: DictConfig):
        super().__init__()
        self.config = conf
        self.mailchimp = instantiate_config(self.config.core_lib.email_core_lib.client)
```
Uses `CoreLib`'s `instantiate_config` that will instantiate the `MailChimpClient` from the config yaml.

## MailChimp Client
This client will be initialized as soon as the `Celery` worker has started and the `EmailCoreLib` is initialized

### Functions
```python
def send(self, template_name: str, params: dict):
```

`template_name` (*str*): Name of the saved template in your MailChimp Transactional account

`params` (*dict*): A `dict` of variables as keys and their values that are saved in the template to be replaced.

## Example
```python
import hydra
from celery import Celery

hydra.initialize(config_path='config_path', caller_stack_depth=1)
cfg = hydra.compose('config.yaml')

app = Celery()
app.config_from_object(cfg.core_lib.email_core_lib.amqp.url)
app.autodiscover_tasks()

app.send_task('task.send',
                ['register_complete', {'email': 'john@example.com', 'plan': 'some plan'}],
                queue='celery')
```
## License
Licenced under [MIT](https://github.com/shay-te/email-core-lib/blob/master/LICENSE_2022_4_19)
