import serial
import time
import subprocess

def get_ladis_h3k_status(serial_connection):
    for i in range(3):
        try:
            serial_connection.write(b'Q1\r')
            response = serial_connection.readline()
            status = response.decode().strip()
            return dict(zip(["输入电压","输入异常电压","输出电压","输出电流百分比",
                            "输入频率","电池电压","温度","状态"],status[1:].split()))
        except:
            print("Failed to get LADIS H3K UPS status. Retrying...")
            time.sleep(5)
    else:
        raise Exception("Failed to get LADIS H3K UPS status.")

def shutdown():
    # 执行关机命令
    shutdown_command = "shutdown -h now" 
    subprocess.call(shutdown_command, shell=True)

def parse_ups_status(ups_status_binary_str):
    ups_status = {
        "ac_failure": ups_status_binary_str[0] == '1',
        "bat_low": ups_status_binary_str[1] == '1',
        "bypass_inv": ups_status_binary_str[2] == '1',
        "fault": ups_status_binary_str[3] == '1',
        "ups_type": 'backup' if ups_status_binary_str[4] == '1' else 'online',
        "system_testing": ups_status_binary_str[5] == '1',
        "system_off": ups_status_binary_str[6] == '1',
        "warning_tone_on": ups_status_binary_str[7] == '1',
    }

    return ups_status

def main():
    serial_port = '/dev/ttyUSB0'
    baud_rate = 2400
    
    try:
        with serial.Serial(serial_port, baud_rate, timeout=1) as ser:
            time.sleep(1)  # 等待串口初始化完成
            status = get_ladis_h3k_status(ser)
            print(f"LADIS H3K UPS status: {status}")
            if status['状态'][0] == '1':
                print("关机")
                shutdown()
            else:
                print("市电正常")
    except serial.SerialException as e:
        print(f"Error: {str(e)}")
        print("Failed to communicate with the LADIS H3K UPS. Please check your serial connection and port.")

if __name__ == "__main__":
    main()
