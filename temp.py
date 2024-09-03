import sys
import os
import serial
import threading
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QMetaObject, Q_ARG
from UI.power_moniter import Ui_mainWindow
import OPi.GPIO as GPIO
import hmac
from hashlib import sha1
import time
from paho.mqtt.client import MQTT_LOG_INFO, MQTT_LOG_NOTICE, MQTT_LOG_WARNING, MQTT_LOG_ERR, MQTT_LOG_DEBUG
from paho.mqtt import client as mqtt
import json
import random

# ����GPIO������ģʽ
GPIO.setmode(GPIO.BOARD)

# �豸֤�飨ProductKey��DeviceName��DeviceSecret������Ԫ��
productKey = 'k1h6wbBlprP'
deviceName = 'test'
deviceSecret = '63A6EBA0E16301B60FB1F89C7690B4B2F286DB6E'

# ClientId Username�� Password ǩ��ģʽ�µ����÷������ο��ĵ� https://help.aliyun.com/document_detail/73742.html?spm=a2c4g.11186623.6.614.c92e3d45d80aqG
# MQTT - �ϳ�connect������ʹ�õ� ClientID��Username��Password
mqttClientId = deviceName + '|securemode=2,signmethod=hmacsha1,timestamp=1719387126564|'
mqttUsername = deviceName + '&' + productKey
content = 'clientId' + deviceName + 'deviceName' + deviceName + 'productKey' + productKey
mqttPassword = hmac.new(deviceSecret.encode(), content.encode(), sha1).hexdigest()
mqttPassword = '63A6EBA0E16301B60FB1F89C7690B4B2F286DB6E'
# ����ķ�������ַ
regionId = 'cn-shanghai'
# MQTT ���������
brokerUrl = productKey + '.iot-as-mqtt.' + regionId + '.aliyuncs.com'

# Topic��post���ͻ�����������ϱ���Ϣ
topic_post = '/sys/' + productKey + '/' + deviceName + '/thing/event/property/post'
# Topic��set����������ͻ����·���Ϣ
topic_set = '/sys/' + productKey + '/' + deviceName + '/thing/service/property/set'

# ��ģ�����Ƶ�ǰ׺��ȥ����׺�����֣�
modelName = 'PowerSwitch_'

# ����MQTT�ͻ��˶���
client = mqtt.Client(client_id=mqttClientId, protocol=mqtt.MQTTv311, clean_session=True)

def on_log(client, userdata, level, buf):
    if level == MQTT_LOG_INFO:
        head = 'INFO'
    elif level == MQTT_LOG_NOTICE:
        head = 'NOTICE'
    elif level == MQTT_LOG_WARNING:
        head = 'WARN'
    elif level == MQTT_LOG_ERR:
        head = 'ERR'
    elif level == MQTT_LOG_DEBUG:
        head = 'DEBUG'
    else:
        head = level
    print('%s: %s' % (head, buf))

# MQTT�ɹ����ӵ��������Ļص�������
def on_connect(client, userdata, flags, rc):
    print('Connected with result code ' + str(rc))
    # ��MQTT���������ӳɹ���֮��������
    client.subscribe(topic_post, qos=0)
    client.subscribe(topic_set, qos=0)
    # �����������������Ϣ
    client.publish(topic_post, payload='test msg', qos=0)

# MQTT���յ���������Ϣ�Ļص�������
def on_message(client, userdata, msg):
    print('recv:', msg.topic + ' ' + str(msg.payload))

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected disconnection %s' % rc)

def mqtt_connect_aliyun_iot_platform():
    client.on_log = on_log
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.username_pw_set(mqttUsername, mqttPassword)
    print('clientId:', mqttClientId)
    print('userName:', mqttUsername)
    print('password:', mqttPassword)
    print('brokerUrl:', brokerUrl)
    # ssl���ã�����port=8883
    # client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS, ciphers=None)
    try:
        client.connect(brokerUrl, 1883, 60)
    except:
        print('������������ƽ̨MQTT���������Ӵ��������豸֤����Ԫ�顢��������������')
    client.loop_forever()

# ��������
class MainWindow(QMainWindow, Ui_mainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)  # ��ʼ��UI

        # ����485�����ģʽ
        GPIO.setup(7, GPIO.OUT)
        GPIO.output(7, GPIO.LOW)

        # ��ʼ������ͼ��ǩ
        self.background_label = QLabel(self)
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        self.background_label.setScaledContents(True)
        self.background_label.lower()  # ȷ������ͼ�����пؼ�֮��

        # ���ó�ʼ����ͼ
        self.set_background_image('images/wew.png')

        # ����QLCDNumber��λ������ֹ��������̫����ʾ
        self.lcdNumber11.setDigitCount(9)
        self.lcdNumber111.setDigitCount(9)
        self.lcdNumber1.setDigitCount(9)
        self.lcdNumber22.setDigitCount(9)
        self.lcdNumber222.setDigitCount(9)
        self.lcdNumber2.setDigitCount(9)
        self.lcdNumber33.setDigitCount(9)
        self.lcdNumber333.setDigitCount(9)
        self.lcdNumber3.setDigitCount(9)
        
        # ��ʼ����ѹ���������õ���
        self.voltage = 0
        self.current = 0
        self.power_consumption = 0
        
        # �򿪴���
        try:
            self.serial_port = serial.Serial('/dev/ttyS1', baudrate=115200, timeout=1)
            print("Serial port opened successfully")  # ��ӡ���ڴ򿪳ɹ���Ϣ
        except Exception as e:
            print(f"Failed to open serial port: {e}")  # ��ӡ���ڴ�ʧ����Ϣ
            return

        self.start_receiving()  # ��ʼ���մ�������
        self.showMaximized()  # �����ʾ����

    def set_background_image(self, image_path):
        abs_image_path = os.path.join(os.getcwd(), image_path).replace("\\", "/")
        if not os.path.exists(abs_image_path):
            print(f"Image not found: {abs_image_path}")  # ��ӡͼƬδ�ҵ���Ϣ
        else:
            pixmap = QPixmap(abs_image_path)
            if pixmap.isNull():
                print(f"Failed to load image: {abs_image_path}")  # ��ӡ����ͼƬʧ����Ϣ
            else:
                self.background_label.setPixmap(pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
                self.background_label.setGeometry(0, 0, self.width(), self.height())
                self.update()

    # �����ڴ�С�ı��¼�
    def resizeEvent(self, event):
        self.background_label.setGeometry(0, 0, self.width(), self.height())  # ��������ͼ��С
        pixmap = self.background_label.pixmap()
        if pixmap:
            self.background_label.setPixmap(pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))

    # ��ʼ���մ�������
    def start_receiving(self):
        self.thread = threading.Thread(target=self.receive_data)
        self.thread.daemon = True
        self.thread.start()

    # ���մ�������
    def receive_data(self):
        buffer = b""
        while True:
            if self.serial_port.in_waiting > 0:
                buffer += self.serial_port.read(self.serial_port.in_waiting)
                print(f"Buffer: {buffer.hex()}")  # ��ӡ���յ�������

                # ȷ������������һ������������֡
                while len(buffer) >= 17:
                    start_index = buffer.find(b'\x68')
                    if start_index != -1 and len(buffer) >= start_index + 17:
                        if buffer[start_index + 16] == 0x16:
                            packet = buffer[start_index:start_index + 17]
                            buffer = buffer[start_index + 17:]
                            print(f"Packet found: {packet.hex()}")  # ��ӡ�ҵ������ݰ���Ϣ
                            self.process_packet(packet)
                        else:
                            buffer = buffer[start_index + 1:]
                    else:
                        break

    # ������յ������ݰ�
    def process_packet(self, packet):
        data = packet.hex()
        print(f"Received packet data: {data}")  # ��ӡ���յ������ݰ���Ϣ

        if len(data) == 34 and data.startswith('68') and data.endswith('16'):
            sign_flag = data[20:22]  # ��־λ�ڵ�21��22���ַ�
            value_data = data[22:30]  # ���ݲ��ִӵ�23����30���ַ�

            print(f"Sign flag: {sign_flag}, Value data (hex): {value_data}")  # ��ӡ��־λ�����ݲ���

            try:
                value = int(value_data, 16)  # ��16����ת��Ϊ10����
                print(f"Value (decimal): {value}")  # ��ӡת�����10����ֵ
                if sign_flag == '03':  # ��ѹ
                    self.voltage = value
                    self.update_lcd(self.lcdNumber11, value)
                elif sign_flag == '04':  # ����
                    self.current = value
                    self.update_lcd(self.lcdNumber111, value)
                elif sign_flag == '05':  # �õ���
                    self.power_consumption = value
                    self.update_lcd(self.lcdNumber1, value)
                self.update_checkbox()
                self.send_data_to_cloud()
            except ValueError as e:
                print(f"Error parsing value: {e}")  # ��ӡ����ֵ������Ϣ

    # ����LCD��ʾ
    def update_lcd(self, lcd, value):
        if lcd:
            print(f"Updating LCD with value: {value}")  # ��ӡ����LCD��Ϣ
            QMetaObject.invokeMethod(lcd, "display", Qt.QueuedConnection, Q_ARG(int, value))

    # ���¸�ѡ��
    def update_checkbox(self):
        if self.power_consumption > 0:
            self.checkBox1.setChecked(True)
            self.power_switch = 1
        else:
            self.checkBox1.setChecked(False)
            self.power_switch = 0

    # �������ݵ��ƶ�
    def send_data_to_cloud(self):
        switchPost = {
            "params": {
                "Watt": self.power_consumption,
                "Alarm_all": 0,
                "Alarm": 0,
                "Current": self.current,
                "Voltage": self.voltage,
                "PowerSwitch_1": self.power_switch
            },
            "version": "1.0.0"
        }
        payload = json.dumps(switchPost)
        client.publish(topic_post, payload=payload, qos=0)  # ������Ϣ��MQTT����
        print(f"Sent data to cloud: {payload}")  # ��ӡ���͵�����

# ���������
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    # �����߳�t1��mqtt���Ӱ�����������ƽ̨
    t1 = threading.Thread(target=mqtt_connect_aliyun_iot_platform, )
    t1.start()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
