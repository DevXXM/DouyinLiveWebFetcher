# 引入所需的库
import RPi.GPIO as GPIO
import time

# 设置GPIO模式为BCM
GPIO.setmode(GPIO.BCM)

# 定义继电器连接的GPIO引脚
relay_pin = 13  # 请根据实际硬件连接修改引脚号

# 设置GPIO引脚为输出
GPIO.setup(relay_pin, GPIO.OUT)

try:
    while True:
        # 打开继电器
        print("继电器打开")
        GPIO.output(relay_pin, GPIO.HIGH)

        # 等待一段时间
        time.sleep(1)  # 这里等待2秒

        # 关闭继电器
        print("继电器关闭")
        GPIO.output(relay_pin, GPIO.LOW)

        # 等待一段时间
        time.sleep(1)

except KeyboardInterrupt:
    print("程序被用户中断")
finally:
    # 清理GPIO设置
    GPIO.cleanup()
