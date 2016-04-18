"""
Send a single email
"""
from cp_lib.app_base import CradlepointAppBase


def send_one_email(app_base):
    """

    :param CradlepointAppBase app_base: the prepared resources: logger, cs_client, settings, etc
    :return:
    """
    # logger.debug("Settings({})".format(sets))

    if "send_email" not in app_base.settings:
        raise ValueError("settings.ini requires [send_email] section")

    local_settings = dict()
    # we default to GMAIL, assume this is for testing
    local_settings['smtp_url'] = app_base.settings["send_email"].get("smtp_url", 'smtp.gmail.com')
    local_settings['smtp_port'] = int(app_base.settings["send_email"].get("smtp_port", 587))

    for value in ('username', 'password', 'email_to', 'email_from'):
        if value not in app_base.settings["send_email"]:
            raise ValueError("settings [send_email] section requires {} value".format(value))
        # assume all are 'strings' - no need for INT
        local_settings[value] = app_base.settings["send_email"][value]

    subject = app_base.settings["send_email"].get("subject", "test-Subject")
    body = app_base.settings["send_email"].get("body", "test-body")

    app_base.logger.debug("Send Email To:({})".format(local_settings['email_to']))
    result = _do_send_email(local_settings, subject, body)

    app_base.logger.debug("result({})".format(result))

    return result


def _do_send_email(sets, subject, body):
    """

    :param dict sets: the various settings
    :param str subject: the subject line text
    :param str body: the body text
    :return:
    """
    import smtplib

    email = smtplib.SMTP(sets['smtp_url'], sets['smtp_port'])
    email.ehlo()
    email.starttls()
    email.login(sets['username'], sets['password'])

    email_body = '\r\n'.join(['TO: %s' % sets['email_to'], 'FROM: %s' % sets['email_from'],
                              'SUBJECT: %s' % subject, '', body])

    # try:
    email.sendmail(sets['email_from'], [sets['email_to']], email_body)

    # except:
    #     logging.error("Email send failed!")

    email.quit()
    return 0


if __name__ == "__main__":
    import sys

    my_app = CradlepointAppBase("network/send_email")

    _result = send_one_email(my_app)

    my_app.logger.info("Exiting, status code is {}".format(_result))

    sys.exit(_result)
