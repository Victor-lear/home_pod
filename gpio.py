# 
# References:
# - https://learn.adafruit.com/welcome-to-adafruit-io/client-library
# - https://github.com/adafruit/Adafruit_IO_Python/blob/master/examples/basics/subscribe.py
# 
# Hardware
# - Raspberry Pi 4 Model B
#   [2GB] https://my.cytron.io/p-raspberry-pi-4-model-b-2gb?tracking=idris
#   [4GB] https://my.cytron.io/p-raspberry-pi-4-model-b-4gb?tracking=idris
#   [8GB] https://my.cytron.io/p-raspberry-pi-4-model-b-8gb-latest?tracking=idris
# - Grove Base Kit for Raspberry Pi
#   https://my.cytron.io/p-grove-base-kit-for-raspberry-pi?tracking=idris
# 
# Install
# - sudo pip3 install adafruit-blinka
# - sudo pip3 install adafruit-io
# 
# Update:
# 28 Feb 2021
# 

# Import standard python modules.
import sys
import requests
# Import blinka python modules.
import board
import digitalio
import RPi.GPIO as GPIO  # 引入 RPi.GPIO 库
import time
import socket

FEED_ID = ['digital','light']
Light_data=0


def socketsub():
    ESP8266_IP = '192.168.2.109'
    ESP8266_PORT = 8888

    # 创建一个TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # 连接到ESP8266
        client_socket.connect((ESP8266_IP, ESP8266_PORT))
        
        # 发送数据
        message = "Button"
        client_socket.sendall(message.encode())
        print("Message sent successfully.")
        
    except Exception as e:
        print("Error:", e)

    finally:
        # 关闭socket连接
        client_socket.close()



def click():
    # 設定使用的 GPIO 針腳
   # IR_LED_GPIO_PIN = 17  # 將 17 替換為你的 GPIO 針腳編號

    # 初始化 GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)

    # 發射紅外線編碼
    try:
        GPIO.output(17, 0)  # 啟動紅外線 LED
        time.sleep(1)  # 延遲一點時間以確保訊號發送完整
        GPIO.output(17, 1)  # 關閉紅外線 LED
    except:
        print("error")
    # 清理 GPIO 資源
    GPIO.output(17, GPIO.HIGH)
    #GPIO.cleanup()
    print("success")
