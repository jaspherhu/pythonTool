# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from tkinter import ttk
import serial
import serial.tools.list_ports
import threading
import time
from datetime import datetime
import configparser
import os
import zipfile
import struct
import binascii
import zlib  # 添加 zlib 库

# 定义帧ID宏
FRAME_TYPE_HAND = 0x01
FRAME_TYPE_INFO = 0x03
FRAME_TYPE_DATA = 0x05
FRAME_TYPE_END = 0x07

FRAME_TYPE_ACK_02 = 0x02
FRAME_TYPE_ACK_04 = 0x04
FRAME_TYPE_ACK_06 = 0x06
FRAME_TYPE_ACK_08 = 0x08

class SerialTool:
    def __init__(self, root):
        self.root = root
        self.root.title("串口通信工具")
        self.serial_port = None
        self.is_open = False
        self.default_directory = ""  # 默认文件目录
        self.config_file = "config.ini"
        # 初始化变量
        self.port_var = tk.StringVar()
        self.baudrate_var = tk.StringVar(value="115200")
        self.databits_var = tk.StringVar(value="8")
        self.stopbits_var = tk.StringVar(value="1")
        self.parity_var = tk.StringVar(value="N")
        self.load_config()
        self.create_menu()
        self.create_widgets()
        self.rcv_ack02 = 0
        self.rcv_ack04 = 0
        self.rcv_ack06 = 0
        self.rcv_ack08 = 0
        self.file_transfer_state = None
        self.file_transfer_data = b""
        self.frame_number = 0
        self.file_transfer_crc = 0
        self.file_transfer_size = 0
        self.file_transfer_received_size = 0
        self.file_transfer_start_time = time.time()
        self.file_transfer_timeout = 1000  # 1000 ms
        self.file_transfer_file_path = ""
        self.file_transfer_file = None
        self.chunk_size = 1024  # 定义 chunk_size

    def create_menu(self):
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="设置文件目录", command=self.set_default_directory)
        menubar.add_cascade(label="文件", menu=file_menu)
        self.root.config(menu=menubar)

    def create_widgets(self):
        # 串口配置区域
        config_frame = tk.LabelFrame(self.root, text="串口配置")
        config_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        tk.Label(config_frame, text="端口:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.port_combobox = ttk.Combobox(config_frame, textvariable=self.port_var, state="readonly", width=20, font=('Helvetica', 10))
        self.port_combobox.grid(row=0, column=1, padx=5, pady=2, sticky="ew")

        tk.Label(config_frame, text="波特率:").grid(row=1, column=0, padx=5, pady=2, sticky="w")
        tk.Entry(config_frame, textvariable=self.baudrate_var, width=20).grid(row=1, column=1, padx=5, pady=2, sticky="ew")

        tk.Label(config_frame, text="数据位:").grid(row=2, column=0, padx=5, pady=2, sticky="w")
        tk.Entry(config_frame, textvariable=self.databits_var, width=20).grid(row=2, column=1, padx=5, pady=2, sticky="ew")

        tk.Label(config_frame, text="停止位:").grid(row=3, column=0, padx=5, pady=2, sticky="w")
        tk.Entry(config_frame, textvariable=self.stopbits_var, width=20).grid(row=3, column=1, padx=5, pady=2, sticky="ew")

        tk.Label(config_frame, text="校验位:").grid(row=4, column=0, padx=5, pady=2, sticky="w")
        tk.Entry(config_frame, textvariable=self.parity_var, width=20).grid(row=4, column=1, padx=5, pady=2, sticky="ew")

        tk.Button(config_frame, text="打开串口", command=self.toggle_serial).grid(row=5, column=0, padx=5, pady=5, sticky="ew")
        tk.Button(config_frame, text="关闭串口", command=self.close_serial).grid(row=5, column=1, padx=5, pady=5, sticky="ew")

        # 数据发送区域
        send_frame = tk.LabelFrame(self.root, text="数据发送")
        send_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.send_data_var = tk.StringVar()
        tk.Entry(send_frame, textvariable=self.send_data_var, width=40).grid(row=0, column=0, padx=5, pady=2, sticky="ew")
        tk.Button(send_frame, text="发送", command=self.send_data).grid(row=0, column=1, padx=5, pady=2, sticky="ew")

        tk.Button(send_frame, text="文件发送", command=self.send_file).grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        # 数据接收区域
        receive_frame = tk.LabelFrame(self.root, text="数据接收")
        receive_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.receive_text = scrolledtext.ScrolledText(receive_frame, width=60, height=10, state="disabled")
        self.receive_text.grid(row=0, column=0, padx=5, pady=2, sticky="ew")

        self.receive_file_var = tk.BooleanVar(value=False)
        tk.Checkbutton(receive_frame, text="允许接收文件", variable=self.receive_file_var).grid(row=1, column=0, padx=5, pady=2, sticky="w")

        # 历史记录区域
        history_frame = tk.LabelFrame(self.root, text="历史记录")
        history_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")  # 添加 nsew 以支持扩展

        self.history_text = scrolledtext.ScrolledText(history_frame, width=80, height=10, state="disabled")  # 增加宽度
        self.history_text.grid(row=0, column=0, padx=5, pady=2, sticky="nsew")  # 添加 nsew 以支持扩展

        # 设置列权重
        self.root.grid_columnconfigure(0, weight=1)  # 主窗口列权重
        history_frame.grid_columnconfigure(0, weight=1)  # 历史记录区域列权重

    def refresh_ports(self):
        ports = [f"{port.device} - {port.description}" for port in serial.tools.list_ports.comports()]
        self.port_combobox["values"] = ports
        if ports:
            self.port_var.set(ports[0])

    def toggle_serial(self):
        if not self.is_open:
            port_name = self.port_var.get().split(' - ')[0]  # 提取端口名称
            if port_name not in [port.device for port in serial.tools.list_ports.comports()]:
                self.update_history("错误", f"串口设备 {port_name} 未找到")
                return
            try:
                self.serial_port = serial.Serial(
                    port=port_name,
                    baudrate=int(self.baudrate_var.get()),
                    bytesize=int(self.databits_var.get()),
                    stopbits=float(self.stopbits_var.get()),
                    parity=self.parity_var.get()
                )
                self.is_open = True
                threading.Thread(target=self.read_data, daemon=True).start()
                self.update_history("提示", "串口已打开")  # 替换消息框为历史记录打印
            except Exception as e:
                self.update_history("错误", f"无法打开串口: {e}")  # 替换消息框为历史记录打印
        else:
            self.serial_port.close()
            self.is_open = False
            self.update_history("提示", "串口已关闭")  # 替换消息框为历史记录打印

    def close_serial(self):
        if self.is_open:
            self.serial_port.close()
            self.is_open = False
            # messagebox.showinfo("提示", "串口已关闭")  # 显示串口已关闭的消息框
            self.update_history("提示", "串口已关闭")  # 替换消息框为历史记录打印
        else:
            messagebox.showwarning("警告", "串口未打开")  # 显示串口未打开的警告消息框

    def send_data(self):
        if self.is_open:
            data = self.send_data_var.get().encode()
            self.serial_port.write(data)
            self.update_history("发送", data.decode())
        else:
            messagebox.showwarning("警告", "请先打开串口")  # 显示请先打开串口的警告消息框

    def send_file(self):
        if self.is_open:
            initial_dir = self.default_directory if self.default_directory else None
            file_path = filedialog.askopenfilename(initialdir=initial_dir)
            if file_path:
                with open(file_path, "rb") as f:
                    data = f.read()
                    # 使用线程处理文件发送--不然被阻塞死了
                    threading.Thread(target=self.send_file_protocol, args=(file_path, data), daemon=True).start()
        else:
            messagebox.showwarning("警告", "请先打开串口")  # 显示请先打开串口的警告消息框

    def send_file_protocol(self, file_path, file_data):
        # 重置确认标志
        self.rcv_ack02 = 0
        self.rcv_ack04 = 0
        self.rcv_ack06 = 0
        self.rcv_ack08 = 0

        # 发送帧类型为 0x01 的帧
        frame = self.create_frame(0x01, b'\xaa')
        self.serial_port.write(frame)
        self.file_transfer_state = None #
        self.update_history("发送帧类型 0x01", "")

        # 等待确认帧 0x02 -- 一直卡在while里面导致无法接收到02帧
        start_time = time.time()
        while time.time() - start_time < 5:
            if self.rcv_ack02 == 1:
                break
            
            time.sleep(0.1)
            self.serial_port.write(frame)
        else:
            # messagebox.showerror("错误", "握手01超时")
            self.update_history("错误", "握手01超时")
            return

        # 发送文件信息帧
        file_name = os.path.basename(file_path)
        file_format = os.path.splitext(file_name)[1][1:]  # 去掉点号
        file_size = len(file_data)
        file_info = file_name.ljust(32, '\0').encode('utf-8') + file_format.ljust(32, '\0').encode('utf-8') + struct.pack('<I', file_size)
        frame = self.create_frame(FRAME_TYPE_INFO, file_info)
        self.serial_port.write(frame)
        self.update_history("发送文件信息帧", f"文件名: {file_name}, 格式: {file_format}, 大小: {file_size} bytes")

        # 等待确认帧 0x04
        start_time = time.time()
        while time.time() - start_time < 5:
            if self.rcv_ack04 == 1:
                break

            time.sleep(0.1)
            self.serial_port.write(frame)
        else:
            # messagebox.showerror("错误", "发送文件信息帧超时")
            self.update_history("错误", "发送文件信息帧超时")
            return

        # 发送文件数据帧
        f_nums_bak = -1
        chunk_size = 1024  # 每帧发送1024字节
        total_chunks = (file_size + chunk_size - 1) // chunk_size

        # for i in range(total_chunks):
        # self.frame_number = total_chunks 时候就是从机全部接收完成时候
        while self.frame_number < total_chunks:
            # 检查从机多久没有更新了
            if f_nums_bak != self.frame_number:
                start_time = time.time()
                f_nums_bak = self.frame_number

            i = self.frame_number + 1
            chunk = file_data[i * chunk_size:(i + 1) * chunk_size]
            frame_data = struct.pack('<I', i) + chunk  # 当前帧号 + 文件数据
            frame = self.create_frame(FRAME_TYPE_DATA, frame_data)
            self.serial_port.write(frame)
            self.update_history(f"发送文件数据帧 {i+1}/{total_chunks}", f"{len(chunk)} bytes")
            # time.sleep(0.01)

            # 每5s检测一次06报文收到了没--如果很久没有收到从机回复报文-暂停发送了
            if time.time() - start_time > 5:
                time.sleep(1) #延迟系统发送周期,等待从机恢复
                self.update_history("错误", f"发送文件数据帧 {i+1}/{total_chunks} 超时")
            else:
                if self.rcv_ack06 == 1:
                    self.rcv_ack06 = 0  # 重置确认标志    

        # 发送结束帧
        file_crc = zlib.crc32(file_data) & 0xFFFF  # 使用 zlib 库计算 CRC16
        frame = self.create_frame(FRAME_TYPE_END, struct.pack('<H', file_crc))
        self.serial_port.write(frame)
        self.update_history("发送文件结束帧", f"CRC: {file_crc}")

        # 等待确认帧 0x08
        start_time = time.time()
        while time.time() - start_time < 1:
            if self.rcv_ack08 == 1:
                break

            time.sleep(0.1)
            self.serial_port.write(frame)
        else:
            # messagebox.showerror("错误", "发送文件结束帧超时")
            self.update_history("错误", "发送文件结束帧超时")
            return

        self.update_history("提示", "文件发送成功")  # 替换消息框为历史记录打印

    def read_data(self):
        while self.is_open:
            if self.serial_port.in_waiting > 0:
                data = self.serial_port.read(self.serial_port.in_waiting)
                self.process_data(data)
                self.update_receive(data)
            time.sleep(0.1)

    def calculate_crc(self, data):
        # 计算CRC16-RTU
        # crc = zlib.crc32(data) & 0xFFFF
        crc = 0
        for byte in data:
            crc ^= byte

        return crc

    def create_frame(self, frame_type, data):
        header = b'\xaa\xf5'
        length = struct.pack('<H', len(data))
        crc = self.calculate_crc(header + bytes([frame_type]) + length + data)  # 使用新的CRC计算函数
        # self.update_history("CRC 发送校验", f"接收到的 CRC: {crc}, 计算的 CRC: {header + bytes([frame_type]) + length + data}")
        footer = b'\x5a'
        # self.update_history("创建帧", f"header: {header}, length: {length}, data: {data}, crc: {crc}, footer: {footer}")
        return header + bytes([frame_type]) + length + data + struct.pack('<H', crc) + footer

    def process_data(self, data):
        buffer = self.file_transfer_data + data
        self.file_transfer_data = b""
        
        while len(buffer) >= 8:  # 修改最小帧长度为8字节
            if buffer[:2] != b'\xaa\xf5' or buffer[-1] != 0x5a:
                buffer = buffer[1:]  # 移除无效字节
                continue

            frame_type = buffer[2]
            length = struct.unpack('<H', buffer[3:5])[0]    

            if length > 0:
                if len(buffer) < 8 + length:
                    self.file_transfer_data = buffer    # 缓存未完整帧
                    break
            else:
                self.file_transfer_data = b""

            frame_data = buffer[5:5 + length]
            crc_received = struct.unpack('<H', buffer[5+length:5+length+2])[0]
            crc_calculated = self.calculate_crc(buffer[:5+length])  # 使用新的CRC计算函数

            if crc_received != crc_calculated:
                self.update_history("CRC 校验失败", f"接收到的 CRC: {crc_received}, 计算的 CRC: {crc_calculated}")
                buffer = buffer[1:]  # 移除无效帧
                continue

            if time.time() - self.file_transfer_start_time > 30 & frame_type > FRAME_TYPE_HAND:
                self.update_history("错误", "接收方确认失败")
                self.file_transfer_file.close()

            if frame_type == FRAME_TYPE_HAND:
                if self.receive_file_var.get():
                    self.send_ack(FRAME_TYPE_ACK_02)
                    self.file_transfer_start_time = time.time()
            elif frame_type == FRAME_TYPE_ACK_02:
                self.rcv_ack02 = 1
                self.file_transfer_state = FRAME_TYPE_ACK_02
                self.update_history("接收确认帧 0x02", "")
            elif frame_type == FRAME_TYPE_INFO:
                if self.receive_file_var.get():
                    try:
                        file_name = frame_data[:32].rstrip(b'\0').decode('utf-8', errors='ignore')  # 修改：添加 errors='ignore'
                        file_format = frame_data[32:64].rstrip(b'\0').decode('utf-8', errors='ignore')  # 修改：添加 errors='ignore'
                        file_size = struct.unpack('<I', frame_data[64:68])[0]
                        if self.file_transfer_size > 0:
                            self.update_history("文件信息异常-长度为0", f"文件名: {file_name}, 格式: {file_format}, 大小: {file_size} bytes 数据: {frame_data}")
                            return
                        
                        self.file_transfer_size = file_size
                        self.file_transfer_received_size = 0
                        self.file_transfer_crc = 0
                        self.file_transfer_start_time = time.time()
                        self.file_transfer_file_path = os.path.join(self.default_directory, file_name)
                        self.file_transfer_file = open(self.file_transfer_file_path, "wb")
                        self.send_ack(FRAME_TYPE_ACK_04)
                        self.update_history("接收文件信息帧", f"文件名: {file_name}, 格式: {file_format}, 大小: {file_size} bytes")
                        self.file_transfer_state = FRAME_TYPE_ACK_04  # 新增赋值
                    except Exception as e:
                        self.update_history("错误", f"处理文件信息帧失败: {e}")
                        buffer = buffer[1:]  # 移除无效帧
                        continue
            elif frame_type == FRAME_TYPE_ACK_04:
                self.rcv_ack04 = 1
                self.file_transfer_state = FRAME_TYPE_ACK_04
            elif frame_type == FRAME_TYPE_DATA:
                self.frame_number = struct.unpack('<I', frame_data[:4])[0]
                chunk = frame_data[4:]
                self.file_transfer_data += chunk
                self.file_transfer_received_size += len(chunk)
                self.file_transfer_crc = zlib.crc32(self.file_transfer_data) & 0xFFFF  # 使用 zlib 库计算 CRC16
                self.file_transfer_start_time = time.time()

                # 发送确认帧 0x06--告诉主机我接收到了frame_number这一帧,不要乱发
                progress_percent = int((self.file_transfer_received_size / self.file_transfer_size) * 100)
                ack_data = struct.pack('<I', self.frame_number) + struct.pack('<H', progress_percent)
                self.send_ack_with_data(FRAME_TYPE_ACK_06, ack_data)
                self.update_history(f"接收文件数据帧 {self.frame_number+1}/{(self.file_transfer_size + self.chunk_size - 1) // self.chunk_size}", f"{len(chunk)} bytes, 进度: {progress_percent}%")

                if self.file_transfer_received_size >= self.file_transfer_size:
                    self.file_transfer_file.write(self.file_transfer_data)
                    self.file_transfer_file.close()

                    self.send_ack(FRAME_TYPE_ACK_06)

                    self.update_history("接收文件数据帧", f"接收大小: {self.file_transfer_received_size} bytes, CRC: {self.file_transfer_crc}")
                    self.save_received_file()
                    self.file_transfer_state = None

            elif frame_type == FRAME_TYPE_ACK_06:
                self.rcv_ack06 = 1
                self.file_transfer_state = FRAME_TYPE_ACK_06 
                self.update_history("接收确认帧 0x06", "")
            elif frame_type == FRAME_TYPE_END:
                received_crc = struct.unpack('<H', frame_data)[0]
                if received_crc == self.file_transfer_crc:
                    self.update_history("接收文件结束帧", f"CRC 匹配: {received_crc}")
                    # messagebox.showinfo("提示", "文件接收成功")
                    self.send_ack(FRAME_TYPE_ACK_08)
                    self.file_transfer_state = FRAME_TYPE_ACK_08  # 新增赋值
                else:
                    self.update_history("接收文件结束帧", f"CRC 不匹配: {received_crc} != {self.file_transfer_crc}")
                    # messagebox.showerror("错误", "文件接收失败，CRC 不匹配")
                    self.update_history("错误", "文件接收失败，CRC 不匹配")
                self.file_transfer_state = None
            elif frame_type == FRAME_TYPE_ACK_08:
                self.rcv_ack08 = 1
                self.file_transfer_state = FRAME_TYPE_ACK_08
                self.update_history("接收确认帧 0x08", "")
            else:
                self.file_transfer_state = None

            buffer = buffer[8+length+2:]  # 移除已处理帧

    def send_ack(self, ack_code):
        frame = self.create_frame(ack_code, b"")
        self.serial_port.write(frame)
        # self.send_data(frame)
        self.update_history(f"发送确认帧 {ack_code}", "")

    def update_receive(self, data):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 获取当前时间并格式化
        formatted_data = f"[{timestamp}] {data.decode('utf-8', errors='ignore')}\n"  # 格式化接收到的数据
        self.receive_text.config(state="normal")
        self.receive_text.insert(tk.END, formatted_data)  # 使用格式化后的数据
        self.receive_text.config(state="disabled")
        self.receive_text.yview(tk.END)

    def set_default_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.default_directory = directory
            messagebox.showinfo("提示", f"默认文件目录已设置为: {directory}")  # 显示默认文件目录已设置的消息框

    def load_config(self):
        config = configparser.ConfigParser()
        if os.path.exists(self.config_file):
            config.read(self.config_file, encoding="utf-8")
            if "Serial" in config:
                self.port_var.set(config["Serial"].get("port", ""))
                self.baudrate_var.set(config["Serial"].get("baudrate", "9600"))
                self.databits_var.set(config["Serial"].get("databits", "8"))
                self.stopbits_var.set(config["Serial"].get("stopbits", "1"))
                self.parity_var.set(config["Serial"].get("parity", "N"))
            if "File" in config:
                self.default_directory = config["File"].get("default_directory", "")
        else:
            self.save_config()  # 如果配置文件不存在，则创建默认配置

    def save_config(self):
        config = configparser.ConfigParser()
        config["Serial"] = {
            "port": self.port_var.get(),
            "baudrate": self.baudrate_var.get(),
            "databits": self.databits_var.get(),
            "stopbits": self.stopbits_var.get(),
            "parity": self.parity_var.get(),
        }
        config["File"] = {
            "default_directory": self.default_directory,
        }
        with open(self.config_file, "w", encoding="utf-8") as f:
            config.write(f)

    def on_closing(self):
        self.save_config()
        self.root.destroy()

    def save_received_file(self):
        if self.file_transfer_received_size != self.file_transfer_size:
            # messagebox.showerror("错误", "文件接收不完整")
            self.update_history("错误", "文件接收不完整")
            return
        try:
            # messagebox.showinfo("提示", f"文件已保存到: {self.file_transfer_file_path}")
            self.update_history("提示", f"文件已保存到: {self.file_transfer_file_path}")
        except Exception as e:
            # messagebox.showerror("错误", f"保存文件失败: {e}")
            self.update_history("错误", f"保存文件失败: {e}")

    def update_history(self, action, data):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log = f"[{timestamp}] {action}: {data}\n"
        self.history_text.config(state="normal")
        self.history_text.insert(tk.END, log)  # 添加插入位置和日志内容
        self.history_text.config(state="disabled")  # 插入后将状态重新设置为disabled

if __name__ == "__main__":
    root = tk.Tk()
    app = SerialTool(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)  # 添加完整的参数和关闭括号
    root.mainloop()  # 添加主事件循环