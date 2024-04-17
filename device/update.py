import os
import requests
import json
import zipfile
import shutil
import subprocess
import psutil
import time

def check_running():
    # Check if another 'run.py' process is running
    for proc in psutil.process_iter(attrs=['name']):
        if proc.info['name'] == 'python' and 'run.py' in proc.cmdline():
            return True
    return False

def start_run():
    # Start '/script/code/run.py' process
    subprocess.Popen(['python', 'code/run.py'])

def get_local_version():
    if os.path.exists('version.json'):
        with open('version.json', 'r') as f:
            data = json.load(f)
            return data.get('version_num', 0), data.get('version_name', '')
    return 0, ''

def get_device_id():
    if os.path.exists('uuid.txt'):
        with open('uuid.txt', 'r') as f:
            return f.read().strip()
    return ''

def get_latest_firmware(device_id):
    url = f'http://danmu.mmdoc.cn/api/device/version?device_id={device_id}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('data', {}).get('firmware')
    return None

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

def unzip_firmware(filename):
    extract_folder = os.path.splitext(filename)[0]
    extract_path = os.path.join('firmware', extract_folder)
    with zipfile.ZipFile(os.path.join('firmware', filename), 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    code_path = os.path.join(os.path.dirname(__file__), 'code')
    if not os.path.exists(code_path):
        os.makedirs(code_path)
    for item in os.listdir(extract_path):
        item_path = os.path.join(extract_path, item)
        if os.path.isfile(item_path):
            shutil.copy(item_path, os.path.join(code_path, item))

def main():
    device_id = get_device_id()
    if not device_id:
        print('Error: Device ID not found.')
        return

    while True:
        local_version_num, local_version_name = get_local_version()
        latest_firmware = get_latest_firmware(device_id)

        if latest_firmware and latest_firmware['version_num'] > local_version_num:
            download_url = latest_firmware['download_url']
            firmware_filename = download_firmware(download_url)
            if firmware_filename:
                unzip_firmware(firmware_filename)
                with open('version.json', 'w') as f:
                    json.dump({'version_num': latest_firmware['version_num'], 'version_name': latest_firmware['version_name']}, f)

        if not check_running():
            start_run()

        time.sleep(1)

if __name__ == '__main__':
    main()
