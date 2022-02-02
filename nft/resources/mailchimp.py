import mailchimp_transactional as MailchimpTransactional
from mailchimp_transactional.api_client import ApiClientError

mailchimp = MailchimpTransactional.Client('XplG1hxLlF0J_TjVrJtRdA')

class TransactionalEmailManager:
    @staticmethod
    def send_message(message_text, to):
        message = {
            "from_email": "no-reply@blackpearl-nft.com",
            "subject": "Hello world",
            "text": message_text,
            "to": [
              {
                "email": to,
                "type": "to"
              }
            ]
        }
        try:
            mailchimp.messages.send({"message": message})
        except ApiClientError:
            return False



