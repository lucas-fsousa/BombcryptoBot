import smtplib
from os import environ
import email.message
from App import Routines as routines
from App.Objects.externalConfigs import ExternalConfigs


class Email:
    def __init__(self):
        user_profile = environ['USERPROFILE'].split("\\")[2]
        config = ExternalConfigs()
        message = f""" 
            <p>
            Hey, {user_profile}! The BCRYPTO_BOT is delighted to inform you that you have reached the
            <strong>{config.AmountBCoin}</strong>
            BCOINS mark and it is time to claim your winnings at [https://app.bombcrypto.io/]
            </p>        
            <br/>
            <p>
            Ei, {user_profile}! É com enorme prazer que o BCRYPTO_BOT informa que você alcancou a marca de
            <strong>{config.AmountBCoin}</strong>
            BCOINS e está na hora de reinvindicar seus ganhos em [https://app.bombcrypto.io/]
            </p>
            <p><strong>TEAM BCRYPTO BOT</strong></p>
        """

        self.DefaultSubject = "Claim Notification"
        self.DefaultMessage = message

    def send_mail(self, subject, to, msg):
        success = False
        try:

            message = email.message.Message()
            message['Subject'] = subject
            message['To'] = to
            message['From'] = 'bcryptobot.notification@gmail.com'
            password = 'UBOViNgArmOlGEKFUpGmfjppiwQFNjNYiBg'

            message.add_header('Content-Type', 'text/html')
            message.set_payload(msg)

            smtp = smtplib.SMTP('smtp.gmail.com: 587')
            smtp.starttls()
            smtp.login(message['From'], password)
            smtp.sendmail(message['From'], message['To'], message.as_string().encode('utf-8'))

            success = True
        except Exception as ex:
            routines.save_logs(f'Failed to send claim notification to user >> {ex}')
        finally:
            return success

