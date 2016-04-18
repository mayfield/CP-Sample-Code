"""Router SDK Demo Application."""

import time
import CSClient
import smtplib
import socket
import serial

message = "think globally, act locally."


class LogLister(object):
    """class that dumps a log"""

    DEV = '/dev/ttyUSB0'
    MIPS = 57600
    ARM = 115200

    def __init__(self):
        self.serial = serial.Serial()
        self.serial.port = self.DEV
        self.serial.baudrate = self.MIPS
        self.serial.bytesize = 8
        self.serial.parity = 'N'
        self.serial.stopbits = 1

    def dump(self):
        if not self.serial.isOpen():
            self.serial.open()

        self.serial.write(b'log\r\n')
        time.sleep(0.5)

        out = ''
        resp = self.serial.readline()
        while resp != b'':
            out += resp.decode()
            resp = self.serial.readline()

        self.serial.close()

        return out


class Email(object):
    """Email class to send emails"""

    USER = "nrf2016cp@gmail.com"
    PASS = "new387week"

    SERVER = "smtp.gmail.com"
    PORT = 587

    def __init__(self, user=None, password=None):
        self.user = user or self.USER
        self.password = password or self.PASS
        self.msg = ''
        self.from_addr = 'test1@test.org'
        self.to_addr = 'test2@test.org'
        self.server = self.SERVER
        self.port = self.PORT

    def message(self, subject, from_addr, to_addr, body):
        self.from_addr = from_addr
        self.to_addr = to_addr

        template = 'Content-Type: text/plain; charset="us-ascii"\n"\
            "MIME-Version: 1.0\nContent-Transfer-Encoding: 7bit\n"\
            "Subject: {}\nFrom: {}\nTo: {}\n\n{}'

        self.msg = template.format(subject, from_addr, to_addr, body)

    def send(self, server=None, port=None):
        if server:
            self.server = server

        if port:
            self.port = port

        try:
            host = socket.gethostname()
            mail_server = smtplib.SMTP(self.server, self.port, host)
            mail_server.ehlo()
            mail_server.starttls()
            mail_server.ehlo()

            mail_server.login(self.user, self.password)
            mail_server.sendmail(self.from_addr, self.to_addr, self.msg)

            mail_server.quit()
        except Exception as e:
            pass


class GPIO(object):
    """A class that represents a GPIO pin."""

    LOW = 0
    HIGH = 1

    def __init__(self, client, name, initial_state=LOW):
        """GPIO class initialization."""
        self.client = client
        self.name = name
        self.state = initial_state
        self.set(self.state)

    def get(self):
        """Request and return the state of the GPIO pin."""
        self.state = self.client.get('/status/gpio/%s' % self.name)
        return self.state

    def set(self, state):
        """Set the state of the GPIO pin."""
        self.state = state
        self.client.put('/control/gpio', {self.name: self.state})

    def toggle(self):
        """Toggle the state of the GPIO pin."""
        self.set(self.LOW if self.state else self.HIGH)
        return self.state


class MorseCode(object):
    """A morse code implementation."""

    CODE = {
        'A': '.-',
        'B': '-...',
        'C': '-.-.',
        'D': '-..',
        'E': '.',
        'F': '..-.',
        'G': '--.',
        'H': '....',
        'I': '..',
        'J': '.---',
        'K': '-.-',
        'L': '.-..',
        'M': '--',
        'N': '-.',
        'O': '---',
        'P': '.--.',
        'Q': '--.-',
        'R': '.-.',
        'S': '...',
        'T': '-',
        'U': '..-',
        'V': '...-',
        'W': '.--',
        'X': '-..-',
        'Y': '-.--',
        'Z': '--..',
        '0': '-----',
        '1': '.----',
        '2': '..---',
        '3': '...--',
        '4': '....-',
        '5': '.....',
        '6': '-....',
        '7': '--...',
        '8': '---..',
        '9': '----.',
        ',': '--..--',
        '.': '.-.-.-',
        '?': '..--..',
        ';': '-.-.-.',
        ':': '---...',
        "'": '.----.',
        '-': '-....-',
        '/': '-..-.',
        '(': '-.--.-',
        ')': '-.--.-',
        '_': '..--.-',
        ' ': ' ',
    }
    dit = 0.05  # 50 ms
    dah = 3 * dit
    gap = dit
    char_gap = 3 * dit
    word_gap = 7 * dit

    def __init__(self, on_func, off_func):
        """Initialize the MorseCode class."""
        self.on = on_func
        self.off = off_func

    def send(self, message):
        """Send a message as morse code."""
        for ch in message:
            try:
                self.render(ch)
            except:
                pass

    def render(self, char):
        """Render a character in morse code."""
        code = self.CODE[char.upper()]
        if code == ' ':
            time.sleep(self.word_gap)
        else:
            time.sleep(self.char_gap)
            for bit in code:
                if bit == '.':
                    self.on()
                    time.sleep(self.dit)
                    self.off()
                elif bit == '-':
                    self.on()
                    time.sleep(self.dah)
                    self.off()
                else:
                    pass
                time.sleep(self.gap)


def run():
    """Application entry point."""
    client = CSClient.CSClient()
    led = GPIO(client, "LED_USB1_G")
    email = Email()
    log = LogLister()
    tm = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
    msg = '%s @ %s' % (message, tm)
    email.message('Hello', 'test@cradlepoint.com', 'nrf2016cp@gmail.com', msg)

    def on():
        """Turn the LED on."""
        led.set(led.HIGH)

    def off():
        """Turn the LED off."""
        led.set(led.LOW)

    morse = MorseCode(on, off)

    iteration = 0
    while True:
        iteration += 1
        if iteration % 10 == 0:
            client.log('RouterSDKDemo', 'Sending alert to ECM.')
            client.alert('RouterSDKDemo', 'Transmitting message: %s' % message)
            client.log('RouterSDKDemo', 'Connected device log %s' % log.dump())

        if iteration % 100 == 0:
            tm = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
            msg = '%s @ %s' % (message, tm)

            email.send()

        client.log('RouterSDKDemo', 'Transmitting message: %s' % message)
        morse.send(message)
        time.sleep(2)


if __name__ == '__main__':
    run()
