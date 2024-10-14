import sys
import os
import serial
import threading
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel,QSizePolicy, QVBoxLayout, QWidget
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
    except:
        print('阿里云物联网平台MQTT服务器连接错误，请检查设备证书三元组、及接入点的域名！')
    client.loop_forever()



######################################################################################
# 主界面类函数，核心程序#
######################################################################################
# 主窗口类
class MainWindow(QMainWindow, Ui_mainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)  # 初始化UI

        
        # 设置GPIO的引脚模式
        GPIO.setmode(GPIO.BOARD)

        # 设置485的输出模式
        GPIO.setup(7, GPIO.OUT)
        GPIO.output(7, GPIO.LOW)

        # 初始化背景图标签
        self.background_label = QLabel(self)
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        self.background_label.setScaledContents(True)
        self.background_label.lower()  # 确保背景图在所有控件之后

        # 设置初始背景图
        self.set_background_image('images/wew.png')

        # 设置QLCDNumber的位数，防止接收数据太大不显示
        self.lcdNumber11.setDigitCount(9)
        self.lcdNumber111.setDigitCount(9)
        self.lcdNumber1.setDigitCount(9)
        self.lcdNumber22.setDigitCount(9)
        self.lcdNumber222.setDigitCount(9)
        self.lcdNumber2.setDigitCount(9)

        # 初始化电压、电流、用电量、湿度、温度、烟雾浓度
        self.voltage = 0
        self.current = 0
        self.power_consumption = 0
        self.alarm = 0
        self.power_switch = 0
        self.Humidity = 0
        self.Temperature = 0
        self.Smoke_Concentration = 0
        self.Smoke_alarm = 0 #云端还没有这个参数传入


        # 新增的画图变量
        self.power_data = {}  # 用于存储每天的用电量，字典形式：天是键，这一天24个小时的用电量存入数组中作为值。键值对形式
        self.daily_power = []  # 存储当天24小时的用电量
        self.days_data_file = 'power_data.txt'
        self.hourly_record_interval = 3600  # 每小时记录一次数据，单位为秒
        self.next_record_time = time.time()  # 下次记录时间
        # 在初始化函数中设置QLabel的大小策略,加了显示的图片才会随窗口变大而变大
        self.label_4.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label_8.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # 打开串口
        try:
            self.serial_port = serial.Serial('/dev/ttyS1', baudrate=19200, timeout=1)
            print("Serial port opened successfully")  # 打印串口打开成功信息
        except Exception as e:
            print(f"Failed to open serial port: {e}")  # 打印串口打开失败信息
            return

        self.start_receiving()  # 开始接收串口数据
        self.showMaximized()  # 最大化显示窗口

    def set_background_image(self, image_path):
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

    # 处理窗口大小改变事件
    def resizeEvent(self, event):
        self.background_label.setGeometry(0, 0, self.width(), self.height())  # 调整背景图大小
        pixmap = self.background_label.pixmap()
        if pixmap:
            self.background_label.setPixmap(pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))

    # 开始接收串口数据
    def start_receiving(self):
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
                    else:
                        break

    # 处理接收到的数据包
    def process_packet(self, packet):
        data = packet.hex()
        print(f"Received packet data: {data}")  # 打印接收到的数据包信息

        if len(data) == 34 and data.startswith('68') and data.endswith('16'):
            sign_flag = data[20:22]  # 标志位在第21和22个字符
            value_data = data[22:30]  # 数据部分从第23到第30个字符

            print(f"Sign flag: {sign_flag}, Value data (hex): {value_data}")  # 打印标志位和数据部分

            try:
                value = int(value_data, 16)  # 将16进制转换为10进制
                print(f"Value (decimal): {value}")  # 打印转换后的10进制值
                if sign_flag == '03':  # 电压
                    self.voltage = value
                    self.update_lcd(self.lcdNumber11, value)
                elif sign_flag == '04':  # 电流
                    self.current = value
                    self.update_lcd(self.lcdNumber111, value)
                elif sign_flag == '05':  # 用电量
                    self.power_consumption = value
                    self.update_lcd(self.lcdNumber1, value)
                    self.log_power_data(value)  # 记录用电量
                    self.update_graphs()  # 更新图形
                elif sign_flag == '06':  # 湿度
                    self.Humidity = value
                    self.update_lcd(self.lcdNumber22, value)
                elif sign_flag == '07':  # 温度
                    self.Temperature = value
                    self.update_lcd(self.lcdNumber2, value)
                elif sign_flag == '08':  # 烟雾浓度
                    self.Smoke_Concentration = value
                    self.update_lcd(self.lcdNumber222, value)    
                self.update_checkbox()
                self.send_data_to_cloud()
            except ValueError as e:
                print(f"Error parsing value: {e}")  # 打印解析值错误信息


    #txt文件存入信息
    def log_power_data(self, value):
        current_time = time.time()

        # 每小时记录一次
        if current_time >= self.next_record_time:
            now = datetime.datetime.now()
            hour = now.strftime('%H')  # 获取当前小时
            today = now.strftime('%Y-%m-%d')  # 获取当天日期

            if today not in self.power_data:
                self.power_data[today] = [0] * 24  # 初始化为24个0的列表

            # 记录当前小时的值
            self.power_data[today][int(hour)] = value  # 将当前小时的用电量记录到相应的位置

            # 保存数据到文件
            with open(self.days_data_file, 'w') as f:
                for date, values in self.power_data.items():
                    if len(values) > 24:  # 每天存储24次数据
                        values = values[-24:]
                    f.write(f"{date}: {','.join(map(str, values))}\n")  # 将每个小时的用电量写入文件

            # 删除过期数据
            if len(self.power_data) > 30:
                oldest_date = min(self.power_data.keys())
                del self.power_data[oldest_date]

            # 更新下一个记录时间
            self.next_record_time = current_time + self.hourly_record_interval

    #实时更新图片曲线
    def update_graphs(self):
        # 计算每天的平均功率
        average_power = {date: sum(values) / len(values) for date, values in self.power_data.items() if values}
        dates = list(average_power.keys())
        averages = list(average_power.values())

        # 创建新的 Figure 对象
        fig1, ax1 = plt.subplots(figsize=(10, 5))
        ax1.plot(dates, averages, marker='o')
        ax1.set_title('Average Power Consumption Over 30 Days')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Average Power (W)')
        ax1.set_xticks(dates)
        ax1.set_xticklabels(dates, rotation=45)
        plt.tight_layout()

        # 在 label_4 上显示图形
        self.display_plot(fig1  , self.label_4)


        # 绘制当天24小时的功率变化图
        current_day = datetime.datetime.now().strftime('%Y-%m-%d')
        if current_day in self.power_data:
            # 获取当天的功率数据
            hourly_power = self.power_data[current_day]

            fig2, ax2 = plt.subplots(figsize=(10, 5))
            ax2.plot(range(24), hourly_power, marker='o')  # x轴为小时，y轴为用电量
            ax2.set_title('Power Consumption for Today (24h)')
            ax2.set_xlabel('Hour')
            ax2.set_ylabel('Power (W)')
            ax2.set_xticks(range(24))  # 设置x轴为0-23
            ax2.set_xticklabels(range(24))  # x轴标签为0-23小时
            plt.tight_layout()


            # 在 label_8 上显示图形
            self.display_plot(fig2, self.label_8)


    def display_plot(self, figure, label):
        # 将matplotlib图形嵌入到指定的QLabel中
        figure.canvas.draw()  # 绘制图形

        # 获取图形的QPixmap
        width, height = figure.canvas.get_width_height()
        image = figure.canvas.buffer_rgba()  # 获取图形的RGBA数据
        qimage = QImage(image, width, height, QImage.Format_RGBA8888)  # 使用RGBA格式创建QImage

        # 设置标签的pixmap
        pixmap = QPixmap.fromImage(qimage)  # 转换为QPixmap
        pixmap = QPixmap.fromImage(qimage)  # 转换为QPixmap
        label.setPixmap(pixmap.scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        plt.close(figure)  # 关闭当前图形，以便下次使用 # 清除当前图形，以便下次使用


    # 更新LCD显示
    def update_lcd(self, lcd, value):
        if lcd:
            print(f"Updating LCD with value: {value}")  # 打印更新LCD信息
            QMetaObject.invokeMethod(lcd, "display", Qt.QueuedConnection, Q_ARG(int, value))

    # 更新复选框
    def update_checkbox(self):
        if self.power_consumption > 0:
            self.checkBox1.setChecked(True)
            self.power_switch = 1
        else:
            self.checkBox1.setChecked(False)
            self.power_switch = 0

        if self.power_consumption > 1000:
            self.alarm = 1
            self.checkBox11.setChecked(True)
        else:
            self.alarm = 0
            self.checkBox11.setChecked(False)
        
        if self.Smoke_Concentration > 50:
            self.Smoke_alarm = 1
            self.checkBox2.setChecked(True)
        else:
            self.Smoke_alarm= 0
            self.checkBox2.setChecked(False)   
        #气体的还没开发，需要定下规则  



    # 发送数据到云端
    def send_data_to_cloud(self):
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
        client.publish(topic_post, payload=payload, qos=0)  # 发布消息到MQTT主题
        print(f"Sent data to cloud: {payload}")  # 打印发送的数据


##########################################################################################################
# 主程序入口#
##########################################################################################################
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    # 建立线程t1：mqtt连接阿里云物联网平台
    #主线程跑界面和数据处理，子线程跑云端链接
    t1 = threading.Thread(target=mqtt_connect_aliyun_iot_platform, )
    t1.start()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
