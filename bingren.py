import hmac
from hashlib import sha1
import time
from paho.mqtt.client import MQTT_LOG_INFO, MQTT_LOG_NOTICE, MQTT_LOG_WARNING, MQTT_LOG_ERR, MQTT_LOG_DEBUG
from paho.mqtt import client as mqtt
import json
import random
import threading

'''
# 原文链接 - 我的博客，更多内容可查看我的主页。
# MQTT接入阿里云物联网平台Demo，使用一机一密的方式
# 运行时，需安装 paho.mqtt
# 在PyCharm 的 File - Settings - Projectxxx - Python Interpreter 中，搜索并安装 paho.mqtt
# 需要根据个人设备进行改动的仅5项：productKey、deviceName、deviceSecret、regionId、modelName
'''

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

# 下发的设置报文示例：{"method":"thing.service.property.set","id":"1227667605","params":{"PowerSwitch_1":1},"version":"1.0.0"}
# json合成上报开关状态的报文
def json_switch_set(num, status):
    switch_info = {}
    switch_data = json.loads(json.dumps(switch_info))
    switch_data['method'] = '/thing/event/property/post'
    switch_data['id'] = random.randint(100000000,999999999) # 随机数即可，用于让服务器区分开报文
    switch_status = {modelName + num : status}
    switch_data['params'] = switch_status
    return json.dumps(switch_data, ensure_ascii=False)

# 开关的状态，0/1
onoff = 0

# 建立mqtt连接对象
#mqtt.CallbackAPIVersion.VERSION1出现问题删除下，运行文件；再添加这个代码运行下就可以了
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, mqttClientId, protocol=mqtt.MQTTv311, clean_session=True)

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

def publish_loop():
    while 1:
        time.sleep(5)
        # global onoff
        # onoff = 1-onoff
        # switchPost = json_switch_set('1', onoff)
        switchPost = '{"params":{"Watt":180,"Alarm_all":0,"Alarm":0,"Current":45,"Voltage":80,"PowerSwitch_1":1},"version":"1.0.0"}'

        client.publish(topic_post, payload=switchPost, qos=0)

if __name__ == '__main__':
    # 建立线程t1：mqtt连接阿里云物联网平台
    # 建立线程t2：定时向阿里云发布消息：5s为间隔，变化开关状态
    t1 = threading.Thread(target=mqtt_connect_aliyun_iot_platform, )
    t2 = threading.Thread(target=publish_loop, )
    t1.start()
    t2.start()
