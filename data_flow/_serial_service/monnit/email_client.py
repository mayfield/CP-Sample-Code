import logging
import smtplib

NRF2016_GMAIL = {
    'user': 'nrf2016cp@gmail.com',
    'pass': 'new387week',
    'smtp': 'smtp.gmail.com',
    'port': 587,
}


def send_email(subject, body):
    """

    :param subject: the subject line text
    :type subject: str
    :param body: the body text
    :type body: str
    :return:
    """
    from notes.lynn_email import LYNN_LINSE_ORG
    # keys are: 'user', 'pass', 'smtp', 'port'

    from monnit.site_config import EMAIL_FROM, EMAIL_TO_LIST

    # data = NRF2016_GMAIL
    data = LYNN_LINSE_ORG

    email = smtplib.SMTP(data['smtp'], data['port'])
    email.ehlo()
    email.starttls()
    email.login(data['user'], data['pass'])

    email_body = '\r\n'.join(['TO: %s' % EMAIL_TO_LIST[0], 'FROM: %s' % EMAIL_FROM,
                              'SUBJECT: %s' % subject, '', body])

    # try:
    logging.info("Sending email to:%s" % EMAIL_TO_LIST[0])
    email.sendmail(EMAIL_FROM, EMAIL_TO_LIST, email_body)
    logging.info("  Email was sent!")

    # except:
    #     logging.error("Email send failed!")

    email.quit()
    return


if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)
    logging.info("Hello - here we go!")

    send_email('Alert: S8892 W broadway Power Status = Lost Power',
               '2016-01-11 17:10:39 UTC Alert: S8892 W broadway Power Status = Lost Power')
