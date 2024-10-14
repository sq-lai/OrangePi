import sys
import os
import serial
import threading
import mysql.connector
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QSizePolicy
from PyQt5.QtGui import QPixmap, QImage
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
import matplotlib.pyplot as plt
import datetime

######################################################################################
# 阿里云链接配置#
######################################################################################

# 设备证书（ProductKey、DeviceName和DeviceSecret），三元组
productKey = 'k1h6wbBlprP'
deviceName = 'test'
deviceSecret = '63A6EBA0E16301B60FB1F89C7690B4B2F286DB6E'

# ClientId Username和 Password 签名模式下的设置方法，参考文档 https://help.aliyun.com/document_detail/73742.html?spm=a2c4g.11186623.6.614.c92e3d45d80aqG
# MQTT - 合成connect报文中使用的 ClientID、Username、Password
mqttClientId = deviceName + '|securemode=2,signmethod=hmacsha1,timestamp=1719387126564|'
mqttUsername = deviceName + '&' + productKey
content = 'clientId' + deviceName + 'deviceName' + deviceName + 'productKey' + productKey
mqttPassword = hmac.new(deviceSecret.encode(), content.encode(), sha1).hexdigest()
mqttPassword = '63A6EBA0E16301B60FB1F89C7690B4B2F286DB6E'
# 接入的服务器地址
regionId = 'cn-shanghai'
# MQTT 接入点域名
brokerUrl = productKey + '.iot-as-mqtt.' + regionId + '.aliyuncs.com'

# Topic，post，客户端向服务器上报消息
topic_post = '/sys/' + productKey + '/' + deviceName + '/thing/event/property/post'
# Topic，set，服务器向客户端下发消息
topic_set = '/sys/' + productKey + '/' + deviceName + '/thing/service/property/set'

# 物模型名称的前缀（去除后缀的数字）
modelName = 'PowerSwitch_'

# 创建MQTT客户端对象
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

# MQTT成功连接到服务器的回调处理函数
def on_connect(client, userdata, flags, rc):
    print('Connected with result code ' + str(rc))
    # 与MQTT服务器连接成功，之后订阅主题
    client.subscribe(topic_post, qos=0)
    client.subscribe(topic_set, qos=0)
    # 向服务器发布测试消息
    client.publish(topic_post, payload='test msg', qos=0)

# MQTT接收到服务器消息的回调处理函数
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
    # ssl设置，并且port=8883
    # client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS, ciphers=None)
    try:
        client.connect(brokerUrl, 1883, 60)
    except Exception as e:
        print(f'阿里云物联网平台MQTT服务器连接错误，请检查设备证书三元组、及接入点的域名！ Error: {e}')
    client.loop_forever()


#######################################################################################
# 数据库配置与链接 #
#######################################################################################
# MySQL数据库连接
try:
    db_conn = mysql.connector.connect(
        host="localhost",  # 替换为您的MySQL服务器地址
        user="root",        # 替换为您的用户名
        password="password",  # 替换为您的密码
        database="sensor_data_db"  # 替换为您的数据库名称
    )
    cursor = db_conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sensor_data (
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        voltage REAL,
        current REAL,
        power_consumption REAL,
        humidity REAL,
        temperature REAL,
        smoke_concentration REAL
    )
    ''')
    db_conn.commit()
    print("Connected to MySQL database and ensured table exists.")
except mysql.connector.Error as err:
    print(f"Error: {err}")
    sys.exit(1)


######################################################################################
# 主界面类函数，核心程序#
######################################################################################

# 主窗口类
class MainWindow(QMainWindow, Ui_mainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        print('Initializing MainWindow...')  # Debug log
        self.setupUi(self)  # 初始化UI
        print('UI setup completed.')  # Debug log
        
        # 设置GPIO的引触模式
        GPIO.setmode(GPIO.BOARD)
        print('GPIO mode set to BOARD.')  # Debug log

        # 设置485的输出模式
        GPIO.setup(7, GPIO.OUT)
        GPIO.output(7, GPIO.LOW)
        print('GPIO pin 7 set to OUTPUT and LOW.')  # Debug log

        # 初始化背景图标签
        self.background_label = QLabel(self)
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        self.background_label.setScaledContents(True)
        self.background_label.lower()  # 确保背景图在所有控件之后
        print('Background label initialized.')  # Debug log

        # 设置初始背景图
        self.set_background_image('images/wew.png')

        # 设置QLCDNumber的位数，防止接收数据太大不显示
        self.lcdNumber11.setDigitCount(9)
        self.lcdNumber111.setDigitCount(9)
        self.lcdNumber1.setDigitCount(9)
        self.lcdNumber22.setDigitCount(9)
        self.lcdNumber222.setDigitCount(9)
        self.lcdNumber2.setDigitCount(9)
        print('LCD Number digit counts set.')  # Debug log

        # 初始化电压、电流、用电量、湿度、温度、烟雾浓度
        self.voltage = 0
        self.current = 0
        self.power_consumption = 0
        self.alarm = 0
        self.power_switch = 0
        self.Humidity = 0
        self.Temperature = 0
        self.Smoke_Concentration = 0
        self.Smoke_alarm = 0 # 云端还没有这个参数传入
        print('Initial sensor values set to 0.')  # Debug log

        # 新增的电力压缩模块
        self.label_4.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label_8.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        print('Label size policies set to Expanding.')  # Debug log
        
        # 存储日常功率数据
        self.power_data = []  # 存储当前24小时内的所有功率变化点
        self.daily_average_power = {}  # 记录最近30天的平均功率

        # 打开串口
        try:
            self.serial_port = serial.Serial('/dev/ttyS1', baudrate=19200, timeout=1)
            print("Serial port opened successfully")  # 打印串口打开成功信息
        except Exception as e:
            print(f"Failed to open serial port: {e}")  # 打印串口打开失败信息
            return

        self.start_receiving()  # 开始接收串口数据
        print('Started receiving serial data.')  # Debug log
        self.showMaximized()  # 最大化显示窗口
        print('Main window maximized.')  # Debug log

    def set_background_image(self, image_path):
        print(f'Setting background image: {image_path}')  # Debug log
        abs_image_path = os.path.join(os.getcwd(), image_path).replace("\\", "/")
        if not os.path.exists(abs_image_path):
            print(f"Image not found: {abs_image_path}")  # 打印图片未找到信息
        else:
            pixmap = QPixmap(abs_image_path)
            if pixmap.isNull():
                print(f"Failed to load image: {abs_image_path}")  # 打印加载图片失败信息
            else:
                self.background_label.setPixmap(pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
                self.background_label.setGeometry(0, 0, self.width(), self.height())
                self.update()
                print(f'Background image set successfully.')  # Debug log

    # 处理窗口大小改变事件
    def resizeEvent(self, event):
        print('Resizing window...')  # Debug log
        self.background_label.setGeometry(0, 0, self.width(), self.height())  # 调整背景图大小
        pixmap = self.background_label.pixmap()
        if pixmap:
            self.background_label.setPixmap(pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
            print('Background label resized.')  # Debug log

    # 开始接收串口数据
    def start_receiving(self):
        print('Starting thread to receive data from serial port...')  # Debug log
        self.thread = threading.Thread(target=self.receive_data)
        self.thread.daemon = True
        self.thread.start()

    # 接收串口数据
    def receive_data(self):
        buffer = b""
        while True:
            if self.serial_port.in_waiting > 0:
                buffer += self.serial_port.read(self.serial_port.in_waiting)
                print(f"Buffer: {buffer.hex()}")  # 打印接收到的数据

                # 确保缓存区包含一个完整的数据帧
                while len(buffer) >= 17:
                    start_index = buffer.find(b'\x68')
                    if start_index != -1 and len(buffer) >= start_index + 17:
                        if buffer[start_index + 16] == 0x16:
                            packet = buffer[start_index:start_index + 17]
                            buffer = buffer[start_index + 17:]
                            print(f"Packet found: {packet.hex()}")  # 打印找到的数据包信息
                            self.process_packet(packet)
                        else:
                            buffer = buffer[start_index + 1:]
                            print('Invalid packet found, moving to next byte...')  # Debug log
                    else:
                        print('Incomplete packet, waiting for more data...')  # Debug log
                        break

    # 处理接收到的数据包
    def process_packet(self, packet):
        data = packet.hex()
        print(f"Received packet data: {data}")  # 打印接收到的数据

        if len(data) == 34 and data.startswith('68') and data.endswith('16'):
            sign_flag = data[20:22]  # 标志位在第21和22个字符
            value_data = data[22:30]  # 数据部分从第23到第30个字符

            print(f"Sign flag: {sign_flag}, Value data (hex): {value_data}")  # 打印标志位和数据部分

            try:
                value = int(value_data, 16)  # 将16进制转换为10进制
                print(f"Value (decimal): {value}")  # 打印转换后的10进制值
                if sign_flag == '03':  # 电压
                    self.voltage = value
                    print(f"Updating voltage to: {value}")
                    self.update_lcd(self.lcdNumber11, value)
                elif sign_flag == '04':  # 电流
                    self.current = value
                    print(f"Updating current to: {value}")
                    self.update_lcd(self.lcdNumber111, value)
                elif sign_flag == '05':  # 用电量
                    self.power_consumption = value
                    print(f"Updating power consumption to: {value}")
                    self.update_lcd(self.lcdNumber1, value)
                    self.update_power_graphs(value)  # 更新功率曲线图，实时记录变化
                elif sign_flag == '06':  # 湿度
                    self.Humidity = value
                    print(f"Updating humidity to: {value}")
                    self.update_lcd(self.lcdNumber22, value)
                elif sign_flag == '07':  # 温度
                    self.Temperature = value
                    print(f"Updating temperature to: {value}")
                    self.update_lcd(self.lcdNumber2, value)
                elif sign_flag == '08':  # 烟雾浓度
                    self.Smoke_Concentration = value
                    print(f"Updating smoke concentration to: {value}")
                    self.update_lcd(self.lcdNumber222, value)    
                self.update_checkbox()
                self.send_data_to_cloud()
                self.save_to_database()  # 将数据保存到数据库
            except ValueError as e:
                print(f"Error parsing value: {e}")  # 打印解析值错误信息

    # 将数据保存到数据库
    def save_to_database(self):
        try:
            print("Saving data to database...")
            cursor.execute('''
                INSERT INTO sensor_data (voltage, current, power_consumption, humidity, temperature, smoke_concentration)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (self.voltage, self.current, self.power_consumption, self.Humidity, self.Temperature, self.Smoke_Concentration))
            db_conn.commit()
            print("Data saved to database successfully.")
        except mysql.connector.Error as err:
            print(f"Failed to save data to database: {err}")

    # 更新LCD显示
    def update_lcd(self, lcd, value):
        if lcd:
            print(f"Updating LCD with value: {value}")  # 打印更新LCD信息
            QMetaObject.invokeMethod(lcd, "display", Qt.QueuedConnection, Q_ARG(int, value))

    # 更新复选框
    def update_checkbox(self):
        print("Updating checkboxes based on current sensor data...")
        if self.power_consumption > 0:
            self.checkBox1.setChecked(True)
            self.power_switch = 1
            print("Power switch checkbox is checked.")
        else:
            self.checkBox1.setChecked(False)
            self.power_switch = 0
            print("Power switch checkbox is unchecked.")

        if self.power_consumption > 1000:
            self.alarm = 1
            self.checkBox11.setChecked(True)
            print("Alarm checkbox is checked.")
        else:
            self.alarm = 0
            self.checkBox11.setChecked(False)
            print("Alarm checkbox is unchecked.")
        
        if self.Smoke_Concentration > 50:
            self.Smoke_alarm = 1
            self.checkBox2.setChecked(True)
            print("Smoke alarm checkbox is checked.")
        else:
            self.Smoke_alarm = 0
            self.checkBox2.setChecked(False)
            print("Smoke alarm checkbox is unchecked.")

    # 发送数据到云端
    def send_data_to_cloud(self):
        print("Preparing data to send to cloud...")
        
        switchPost = {
            "params": {
                "Watt": self.power_consumption,
                "Alarm_all": 0,
                "Alarm": self.alarm,
                "Current": self.current,
                "Humidity":self.Humidity,
                "Temperature":self.Temperature,
                "Smoke_Concentration":self.Smoke_Concentration,
                "Voltage": self.voltage,
                "PowerSwitch_1": self.power_switch
            },
            "version": "1.0.0"
        }
        payload = json.dumps(switchPost)
        try:
            client.publish(topic_post, payload=payload, qos=0)  # 发布消息到MQTT主题
            print(f"Sent data to cloud: {payload}")  # 打印发送的数据
        except Exception as e:
            print(f"Sent data to cloud: {payload}")  # 打印发送的数据

    # 更新功率曲线图
    def update_power_graphs(self, power_value):
        print(f"Updating power graphs with power value: {power_value}")

        
        # 实时追加新采集到的功率值
        self.power_data.append(power_value)

        # 重绘当前功率曲线
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(range(len(self.power_data)), self.power_data, marker='o')
        ax.set_title('Power Consumption for Today (Real-time)')
        ax.set_xlabel('Data Point Index')
        ax.set_ylabel('Power (W)')
        plt.tight_layout()
        self.display_plot(fig, self.label_8)
        print('Power graph for today updated.')  # Debug log

        # 更新、计算平均功率
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        if today not in self.daily_average_power:
            self.daily_average_power[today] = []
        self.daily_average_power[today].append(power_value)

        # 计算最新的平均功率
        average_power = {date: sum(values) / len(values) for date, values in self.daily_average_power.items()}
        dates = list(average_power.keys())
        averages = list(average_power.values())

        # 重绘30天平均功率曲线
        fig2, ax2 = plt.subplots(figsize=(10, 5))
        ax2.plot(dates, averages, marker='o')
        ax2.set_title('Average Power Consumption Over 30 Days')
        ax2.set_xlabel('Date')
        ax2.set_ylabel('Average Power (W)')
        ax2.set_xticks(dates)
        ax2.set_xticks(range(len(dates)))
        ax2.set_xticklabels(dates, rotation=45)
        plt.tight_layout()
        self.display_plot(fig2, self.label_4)
        print('30-day average power graph updated.')  # Debug log

    def display_plot(self, figure, label):
        # 将matplotlib图形嵌入到指定的QLabel中
        print('Displaying plot in QLabel...')  # Debug log
        figure.canvas.draw()  # 绘制图形

        # 获取图形的QPixmap
        width, height = figure.canvas.get_width_height()
        image = figure.canvas.buffer_rgba()  # 获取图形的RGBA数据
        qimage = QImage(image, width, height, QImage.Format_RGBA8888)  # 使用RGBA格式创建QImage

        # 设置标签的pixmap
        pixmap = QPixmap.fromImage(qimage)  # 转换为QPixmap
        label.setPixmap(pixmap.scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        plt.close(figure)  # 关闭当前图形，以便下次使用
        print('Plot displayed and figure closed.')  # Debug log

##########################################################################################################
# 主程序入口#
##########################################################################################################
def main():
    print('Starting application...')  # Debug log
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    # 建立线程t1：mqtt连接阿里云物联网平台
    # 主线程跑界面和数据处理，子线程跑云端连接
    print("Starting MQTT connection thread...")
    t1 = threading.Thread(target=mqtt_connect_aliyun_iot_platform, )
    t1.start()
    print('MQTT connection thread started.')  # Debug log
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()