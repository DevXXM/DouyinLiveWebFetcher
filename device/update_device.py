# -*- coding:utf-8 -*-
from __future__ import print_function
import requests
import json
import os
import zipfile
import shutil
import psutil
import time

# 获取本地版本号和版本名
def get_local_version():
    if os.path.exists('version.json'):
        with open('version.json', 'r') as f:
            data = json.load(f)
            return data.get('version_num', 0), data.get('version_name', '')
    return 0, ''

# 获取设备ID
def get_device_id():
    if os.path.exists('uuid.txt'):
        with open('uuid.txt', 'r') as f:
            return f.read().strip()
    return ''

# 获取最新固件信息
def get_latest_firmware(device_id):
    url = 'http://danmu.mmdoc.cn/api/login?device_id=%s' % device_id
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('data', {}).get('firmware')
    return None

# 下载固件
def download_firmware(url):
    response = requests.get(url)
    if response.status_code == 200:
        if not os.path.exists('firmware'):
            os.makedirs('firmware')
        filename = url.split('/')[-1]
        with open(os.path.join('firmware', filename), 'wb') as f:
            f.write(response.content)
        return filename
    return None

# 解压固件
def unzip_firmware(filename):
    extract_folder = os.path.splitext(filename)[0]
    extract_path = os.path.join('firmware', extract_folder)
    with zipfile.ZipFile(os.path.join('firmware', filename), 'r') as zip_ref:
        zip_ref.extractall(extract_path)

    code_path = os.path.join(extract_path, 'code')
    if not os.path.exists('code'):
        os.makedirs('code')
    for item in os.listdir(extract_path):
        item_path = os.path.join(extract_path, item)
        if os.path.isfile(item_path):
            shutil.copy(item_path, os.path.join('code', item))

# 运行程序
def run_program():
    # 检查是否有其他 run.py 进程正在运行
    for proc in psutil.process_iter():
        try:
            if proc.name() == 'python' and 'run.py' in ' '.join(proc.cmdline()):
                print('Another run.py process is running, waiting for it to finish...')
                proc.wait()
        except psutil.Error:
            pass

    os.system('python ' + os.path.join('code', 'run.py'))

# 主程序
def main():
    device_id = get_device_id()
    if not device_id:
        print('Error: Device ID not found.')
        return

    local_version_num, local_version_name = get_local_version()
    latest_firmware = get_latest_firmware(device_id)

    if latest_firmware and latest_firmware['version_num'] > local_version_num:
        download_url = latest_firmware['download_url']
        firmware_filename = download_firmware(download_url)
        if firmware_filename:
            unzip_firmware(firmware_filename)
            with open('version.json', 'w') as f:
                json.dump({'version_num': latest_firmware['version_num'], 'version_name': latest_firmware['version_name']}, f)
            run_program()

if __name__ == '__main__':
    main()