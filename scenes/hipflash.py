from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
import time

import random
import threading
import math

ECAY_TIME = 10.0
PULSE_DELAY = 0.15
PULSE_LENGTH = 0.5


class Scene(object):
    def __init__(self):
        self.client_id = 'janky_hipflash'
        self.host = 'a37oq57ebfrpmi.iot.us-east-2.amazonaws.com'
        self.root_ca_path = '/etc/awsiot/root-CA.crt'
        self.private_key_path = '/etc/awsiot/jankypi.private.key'
        self.certificate_path = '/etc/awsiot/jankypi.cert.pem'
        self.init_aws_mqqt()
        self.flash_start = None

    def init_aws_mqqt(self):
        awsclient = AWSIoTMQTTClient(self.client_id)
        awsclient.configureEndpoint(self.host, 8883)
        awsclient.configureCredentials(self.root_ca_path, self.private_key_path, self.certificate_path)
        awsclient.connect()
        awsclient.subscribe('janky',1, self.mqtt_callback)
    
    def mqtt_callback(self, client, userdata, message):
        self.flash_start = time.time()
    
    def render_to(self, renderer, moment):
        self.moment = moment
        if self.flash_time is None:
            return
        for i in range(0,60):
            renderer.set_pixel(i, (255, 255, 255))
    
    @property
    def flash_time(self):
        if self.flash_start is None:
            return None
        ftime = time.time() - self.flash_start
        if ftime > 1.0:
            self.flash_start = None
            return None
        return ftime
    


 

if __name__ == '__main__':
    s= Scene()
    while True:
        time.sleep(1)
        print s.flash_time
        print 'waiting..\n'


