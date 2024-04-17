import os
import fcntl
import sys
import psutil  # 导入psutil模块

# 检测是否有其他实例在运行
lock_file = "run.lock"
if os.path.exists(lock_file):
    # 如果锁文件存在，则检查对应进程是否存在
    with open(lock_file, "r") as file:
        pid = int(file.read())
    if not psutil.pid_exists(pid):
        os.remove(lock_file)
    else:
        print("其他实例正在运行，程序退出")
        sys.exit(0)

# 创建锁文件
with open(lock_file, "w") as file:
    file.write(str(os.getpid()))

# 脚本未在运行，进行初始化
import json
import time
import requests
import paho.mqtt.client as mqtt
from queue import Queue, Empty
from threading import Thread
import RPi.GPIO as GPIO

# 设置GPIO模式为BCM编码方式
GPIO.setmode(GPIO.BCM)

# 定义舵机控制引脚
servo_pin = 22

# 设置舵机引脚为输出模式
GPIO.setup(servo_pin, GPIO.OUT)

# 创建 PWM 对象，频率设置为50Hz
pwm = GPIO.PWM(servo_pin, 50)

# 启动 PWM
pwm.start(0)

# MQTT 服务器信息
mqtt_host = ""
mqtt_port = ""
sub_topic = ""

# 全局变量
device_id = ""
login_success = False
client_id = "client_" + str(int(time.time() * 1000))
mqtt_client = mqtt.Client(client_id=client_id)
mqtt_queue = Queue()

running = True

def login_device():
    global device_id, mqtt_host, mqtt_port, sub_topic, login_success
    while not login_success and running:
        try:
            with open("/script/uuid.txt", "r") as file:
                device_id = file.read().strip()
            response = requests.get("http://danmu.mmdoc.cn/api/device/login?device_id=" + device_id)
            data = response.json()
            if data["status"] == 0:
                mqtt_host = data["data"]["host"]
                mqtt_port = str(data["data"]["port"])  # 将端口转换为字符串类型
                sub_topic = data["data"]["sub_topic"]
                login_success = True
                print("登录成功")
            else:
                print("登录失败，2秒后重试")
                time.sleep(2)
        except Exception as e:
            print("登录失败，2秒后重试:", e)
            time.sleep(2)

def on_connect(client, userdata, flags, rc):
    print("连接到MQTT服务器")
    client.subscribe(sub_topic)

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload)
        mqtt_queue.put(data)
    except Exception as e:
        print("消息解析失败:", e)

def servo_action(angle, delay):
    # 限制角度在 0 到 180 度之间
    angle = max(0, min(angle, 180))
    # 计算 PWM 的占空比
    duty = angle / 18 + 2
    # 设置舵机转动到指定角度
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    # 等待一段时间
    time.sleep(delay / 1000.0)
    # 停止 PWM 信号
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(0)

def process_message():
    while running:
        try:
            data = mqtt_queue.get(timeout=1)
            if data["type"] == 1:
                # 调用继电器动作的方法
                pass
            elif data["type"] == 2:
                angle_str = data.get("angle", "")
                if angle_str:
                    angle = int(angle_str)
                else:
                    continue  # 跳过空角度字段的数据
                times = int(data["times"])
                delay = int(data["delay"])
                for _ in range(times):
                    servo_action(angle, delay)
                    servo_action(0, delay)  # 恢复到位置0
        except Empty:
            # 当队列为空时，不执行任何动作，等待新消息
            continue

def mqtt_reconnect():
    global mqtt_port
    while running:
        try:
            if mqtt_port == "":
                print("未设置 MQTT 端口，1秒后重试")
                time.sleep(1)
                continue

            mqtt_client.connect(mqtt_host, int(mqtt_port), 60)
            mqtt_client.loop_start()  # 在新线程中处理MQTT连接和消息循环
            break  # 连接成功后退出循环
        except Exception as e:
            print("MQTT连接失败，1秒后重试:", e)
            time.sleep(1)

def init_servo():
    # 将舵机转到初始位置（例如0度）
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(2)  # 将占空比设置为0度对应的占空比
    time.sleep(0.5)  # 等待舵机稳定
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(0)
    time.sleep(0.5)  # 再次等待舵机稳定

if __name__ == "__main__":
    try:
        init_servo()  # 初始化舵机位置

        login_thread = Thread(target=login_device)
        login_thread.start()

        process_thread = Thread(target=process_message)
        process_thread.start()

        while not login_success:
            time.sleep(1)

        mqtt_client.on_connect = on_connect
        mqtt_client.on_message = on_message

        mqtt_reconnect_thread = Thread(target=mqtt_reconnect)
        mqtt_reconnect_thread.start()

        while running:
            time.sleep(1)
    except KeyboardInterrupt:
        running = False
        mqtt_client.disconnect()
        print("程序已停止")
        # 删除锁文件
        os.remove(lock_file)
        # 等待线程结束
        login_thread.join()
        process_thread.join()
    finally:
        pwm.stop()
        GPIO.cleanup()
