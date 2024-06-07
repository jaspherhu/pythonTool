import tkinter as tk
import socket
import threading
import datetime
from tkinter import messagebox
from tkinter import filedialog
import logging
import os
import subprocess
import json
import pickle
import socket  
import errno

# 设置日志记录
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

col1 = 20
col1_1 = 150
col2 = 300
col3 = 600


class UDPListenerApp:
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.stop_listening()
            self.root.destroy()
    
    def __init__(self, root):
        super().__init__()
        self.root = root

        self.root.title("UDP Listener and Sender")
        root.geometry('1000x500')
        self.menubar = tk.Menu(root)
        root.config(menu=self.menubar)  # 将菜单栏添加到根窗口

        # UI Elements 初始化，使用grid布局
        self.init_ui()

        # UDP variables
        self.server_socket = None
        self.listen_thread = None
        self.stop_event = threading.Event()
        self.is_listening = False

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)  # 添加这行代码来处理窗口关闭事件

    def init_ui(self):
        # 创建菜单栏
        # 文件菜单
        file_menu = tk.Menu(self.menubar, tearoff=0)
        self.filename = 0
        file_menu.add_command(label="log path folder", command=self.open_folder)  # 添加“打开”选项
        file_menu.add_command(label="open log folder", command=self.open_log_folder)
        file_menu.add_command(label="exit app", command=self.on_closing)  # 添加“打开”选项

        self.menubar.add_cascade(label="文件", menu=file_menu)
        self.menubar.add_command(label="退出", command=self.on_closing)
        
        #输入端口号
        #tk.Label(self.root, text="Port:").grid(row=1, column=0)
        tk.Label(self.root, text="Listening Port Input:").place(y=5, x=col1)
        self.port_var = tk.StringVar()  # 用于存储端口号的StringVar
        self.port_entry = tk.Entry(self.root, textvariable=self.port_var)  # 使用Entry控件并绑定到port_var
        self.port_entry.place(y=5, x=col1_1)
        #self.port_entry.grid(row=1, column=1)
        
        #点击按钮
        self.start_button = tk.Button(self.root, text="Start Listening", command=self.start_listening, width=15)
        self.start_button.place(y=65, x=col1)
        #self.start_button.grid(row=2, column=0)
        self.stop_button = tk.Button(self.root, text="Stop Listening", command=self.stop_listening, state='disabled', width=15)
        self.stop_button.place(y=65, x=col1_1)
        #self.stop_button.grid(row=2, column=1)

        #输入发送数据
        #tk.Label(self.root, text="Data to Send:").grid(row=3, column=0)
        self.send_button = tk.Button(self.root, text="Send Data", command=self.send_data, width=15)
        self.send_button.place(y=155, x=col1)
        #self.send_button.grid(row=3, column=0)

        self.send_var = tk.StringVar()
        self.send_entry = tk.Entry(self.root, textvariable=self.send_var, width=35)  # 使用Entry控件并绑定到port_var
        self.send_entry.place(y=125, x=col1)
        #self.send_entry.grid(row=4, column=0, columnspan=2)
        
        #显示接收数据
        #self.rcv_var = tk.StringVar()
        #tk.Label(self.root, text="Rscv:").grid(row=1, column=4)
        tk.Label(self.root, text="Rscv Date:").place(y=5, x=col2)
        self.rcve_area = tk.Text(self.root, height=20, width=50)
        #self.rcve_area.grid(row=2, column=4)
        self.rcve_area.place(y=25, x=col2)
        

        #显示发送历史
        #tk.Label(self.root, text="His Rscv:").grid(row=3, column=4)
        tk.Label(self.root, text="History Send Date:").place(y=305, x=col2)
        self.history_send = tk.Text(self.root, height=10, width=50)
        #self.history_send.grid(row=4, column=4)
        self.history_send.place(y=325, x=col2)

    def open_folder(self):
        self.filename = filedialog.askdirectory()
        #self.filename = filedialog.askopenfilename(title="选择文件", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
        if self.filename:
            print(f"选定的文件夹：{self.filename}")

    def open_log_folder(self):
        if self.filename:
            #log_dir = self.filename
            #打开失败,不知道为啥
            log_dir = "{}".format(self.filename)
        else:
            log_dir = os.getcwd()  # 获取当前工作目录
        
        print("folder path is:",log_dir)
        # 根据不同的操作系统使用不同的命令
        if os.name == 'posix':  # Unix-like systems (Linux, macOS)
            subprocess.run(['open', '-a', 'Finder', log_dir])  # macOS
            # 或者
            # subprocess.run(['xdg-open', log_dir])  # Linux
        elif os.name == 'nt':  # Windows
            subprocess.run(['explorer', log_dir])  # 打开资源管理器

    def start_listening(self):
        port = self.port_var.get()  # 从StringVar获取端口号
        if not port.isdigit() or int(port) < 1 or int(port) > 65535:
            tk.messagebox.showerror("Error", "Invalid port number!{port}")  # 使用消息框展示错误
            #print("port is:",port)
            return

        if self.is_listening:
            self.is_listening = False
            self.stop_event.set()
            self.server_socket.close()
            tk.messagebox.showinfo("Info", "Already listening. Stop it first.")
            return

        try:
            if self.listen_thread.is_alive():
                self.stop_event.set()#抛出一个异常来让线程停止监听
                self.server_socket.close()
                self.server_socket = None
                self.listen_thread.join() #暂停执行
                tk.messagebox.showinfo("Info", "Wait last listening Close.")
        except:
            pass

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind(('0.0.0.0', int(port)))

        self.is_listening = True
        self.listen_thread = threading.Thread(target=self.listen_for_data)
        self.listen_thread.start()

        if self.listen_thread.is_alive():
            self.start_button.config(state='disabled')
            self.stop_button.config(state='normal')

    def stop_listening(self):
        self.stop_event.set()#抛出一个异常来让线程停止监听
        
        if self.server_socket:
            self.server_socket.close()
            self.server_socket = None

        # 等待当前接收循环完成--但是接收函数是一个阻塞函数
        if self.listen_thread and self.listen_thread.is_alive():
            self.listen_thread.join() #暂停执行
        
        if self.listen_thread and self.listen_thread.is_alive():
            tk.messagebox.showinfo("Info", "listening thread kill failed.")

        self.is_listening = False
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')

    def listen_for_data(self):
        #self.server_socket.settimeout(1)  # 设置超时时间为5秒
        self.server_socket.setblocking(False) 
        
        while not self.stop_event.is_set():
            try:
                data, addr = self.server_socket.recvfrom(1024)
                if data:
                    self.handle_received_data(data)
                else:
                    pass
            #except self.server_socket.timeout:
                #logging.info("Data receive timed out, continuing to listen...")
                #pass #放过了
            except socket.error as e: 
                if e.errno == errno.EWOULDBLOCK or e.errno == errno.EAGAIN: 
                    # 没有数据可读，继续执行或稍后再试  
                    #print("No data to receive")  
                    pass
                else:  
                    logging.error(f"Error receiving data: {e}")
                    # 其他非预期异常，可能需要更深入的调查
                    self.stop_event.set()  # 停止监听
                    raise
                    #return
    
    def paser_func_find_cmd(self, byte_data):
        len = 4 #cmd在aaf5后面的第几个数字,
        cmd_data = byte_data[len:len+4] #cmd占有2个字节的话就是4个数字
        cmd_hex = bytes.fromhex(cmd_data.decode()) 
        # 将字节串转换为十六进制
        cmd = int.from_bytes(cmd_hex, byteorder='little')
        return cmd
    
    def paser_func_find_len(self, byte_data):
        len = 0 #cmd在aaf5后面的第几个数字,
        len_data = byte_data[len:len+4] #cmd占有2个字节的话就是4个数字
        len_hex = bytes.fromhex(len_data.decode()) 
        # 将字节串转换为十六进制
        len = int.from_bytes(len_hex, byteorder='little')
        return len
    
    def paser_func_find_seqnum(self, byte_data):
        len = 8 #cmd在aaf5后面的第几个数字,
        seq_data = byte_data[len:len+4] #cmd占有2个字节的话就是4个数字
        seq_hex = bytes.fromhex(seq_data.decode()) 
        # 将字节串转换为十六进制
        seqnum = int.from_bytes(seq_hex, byteorder='little')
        return seqnum
    
    def paser_func_find_type(self, byte_data):
        len = 12 #cmd在aaf5后面的第几个数字,
        type_data = byte_data[len:len+2] #cmd占有2个字节的话就是4个数字
        type_hex = bytes.fromhex(type_data.decode()) 
        # 将字节串转换为十六进制
        hd_type = int.from_bytes(type_hex, byteorder='little')
        return hd_type
    
    def paser_func_find_adr(self, byte_data):
        len = 14 #cmd在aaf5后面的第几个数字,
        adr_data = byte_data[len:len+2] #cmd占有2个字节的话就是4个数字
        adr_hex = bytes.fromhex(adr_data.decode()) 
        # 将字节串转换为十六进制
        hd_adr = int.from_bytes(adr_hex, byteorder='little')
        return hd_adr
    def paser_func_find_gunseq(self, byte_data):
        len = 16 #cmd在aaf5后面的第几个数字,
        gun_data = byte_data[len:len+2] #cmd占有2个字节的话就是4个数字
        gun_hex = bytes.fromhex(gun_data.decode()) 
        # 将字节串转换为十六进制
        hd_gun = int.from_bytes(gun_hex, byteorder='little')
        return hd_gun
    
    def parse_data(self, data):
        #去掉里面的空格
        data = data.replace(b' ', b'')  
        #这个则是十六进制非字符
        #target_hex = b'\xaa\xf5'
        # 原始的字节串，包含十六进制字符 
        target_hex = b'aaf5' #被坑了啊
        # 查找目标十六进制数在字符串中的位置
        position = data.find(target_hex)
        if position == -1:
            position = data.find(b'AAF5')

        # 如果找到了目标序列，则提取其后面的所有字符
        if position != -1 and position != -1:
            byte_data = data[position + len(target_hex):]
            print("在 aaf5 后面的内容:", byte_data)  # 打印为十六进制字符串
        else:
            print("未找到 aaf5 序列",data)
            return

        cmd = self.paser_func_find_cmd(byte_data)
        #cmd = 112
        print("cmd:",cmd)

        len_total = 0
        
        if cmd:
            # 指定你的 JSON 文件路径
            file_path = './cmd_jason/{}.jason'.format(cmd)
        else:
            return

        items_title = {}    #报文中有很多个item
        #parsed_data_list = []  # 更改为列表以保存每个解析结果
        #先把cmd入栈表单
        items_title["cmd"] = cmd
        items_title["len"] = self.paser_func_find_len(byte_data)
        items_title["seq"] = self.paser_func_find_seqnum(byte_data)
        items_title["hd_type"] = self.paser_func_find_type(byte_data)
        items_title["hd_adr"] = self.paser_func_find_adr(byte_data)
        items_title["hd_gun"] = self.paser_func_find_gunseq(byte_data)
        items_title["body"] = []

        byte_data = byte_data[18:]   #头部的结构：长度(2字节) + cmd(2字节) + seq(2字节) + type(1字节) + adr(1字节) + gun(1字节)

        # 使用 'with' 语句打开并读取JSON文件
        with open(file_path, 'r', encoding='utf-8') as file:
            data_jason = json.load(file)

        # 遍历列表中的每个字典
        for cmd_dict in data_jason:
            # 字典中的键和值可以根据你的具体数据来访问
            date_hex = 0            #报文格式中间态
            items_content = {}
            # 使用 for 循环和 items() 方法遍历字典
            for key, value in cmd_dict.items():
                items_content[key] = value
                #print(key,value) 

                if key == "len":
                        lens = (value*2)#(cmd_dict[key]*2)
                        date_hex = byte_data[len_total:len_total + lens]
                        items_content["date_hex"] = date_hex.decode('utf-8') 
                        date_hex = bytes.fromhex(date_hex.decode())  #转化为2字节的数据
                        len_total += lens #他每次取得是一个数字
                    
                elif key == "type":
                    if cmd_dict[key] == "BIN":
                        # 将字节串转换为十六进制
                        items_content["date_parse"] = int.from_bytes(date_hex, byteorder='little') 
                    elif cmd_dict[key] == "STR":
                        # 将字节串解码为ASCII字符串  
                        items_content["date_parse"] = date_hex.decode('utf-8')  
                    else:
                        items_content["date_parse"] = "jason解析文件无标记类型(BIN/STRING)"
                        pass

            items_title["body"].append(items_content)  # 将报文每一个字段解析成一个字典当成一个键值
            #print(items_title["body"])   
        return items_title
    
    def save_to_json(self, parsed_data):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H")
        if self.filename:
            log_dir = f"{self.filename}/{timestamp}"
        else:
            log_dir = f"./{timestamp}"

        log_path = f"{log_dir}/udp_data.json"
        # 创建日志文件所在的目录，如果不存在的话
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        with open(log_path, 'a') as json_file:  #追加写入a,股覆盖w
            json.dump(parsed_data, json_file, ensure_ascii=False, indent=4)
            json_file.write('\n')  # 在写入数据后添加换行符


    def handle_received_data(self, data):
        self.rcve_area.insert(tk.END, f"Received: {data.decode('utf-8')}\n")

        # Parse and save data to log file  
        #parsed_data = self.encode_utf8_data(data)  
        parsed_data = data
        self.save_to_log(parsed_data)  

        # 解析数据
        jason_data = self.parse_data(data)

        # 保存数据到JSON文件
        self.save_to_json(jason_data)
        

    def send_data(self):
        if not self.is_listening:
            tk.messagebox.showerror("Error", "No UDP service is listening. Please start listening first.")
            logging.error(f"Error sending data: : Service is not in listening mode.")
            return

        #data_to_send = self.send_data_entry.get()  # 使用get方法获取Entry中的文本
        data_to_send = self.send_var.get()
        dest_ip = '127.0.0.1'
        dest_port = int(self.port_entry.get())
        #dest_port = int(self.port_var.get())

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as send_socket:
            send_socket.sendto(data_to_send.encode('utf-8'), (dest_ip, dest_port))

        self.history_send.insert(tk.END, f"Sent: {data_to_send}\n")  # 在Text控件中插入发送的数据

    def encode_utf8_data(self, data):  
        # Implement your data parsing logic here  
        # For demonstration, we'll just return the received string  
        return data.decode('utf-8')  

    def save_to_log(self, parsed_data):

        _data = parsed_data.decode('utf-8')
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H")
        if self.filename:
            log_dir = '{}/{}'.format(self.filename,timestamp) 
        else:
            log_dir = './{}'.format(timestamp)

        log_path = '{}/udp_log.txt'.format(log_dir)
        #print("path is:",log_path)

        # 创建日志文件所在的目录，如果不存在的话
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        
        with open(log_path, 'a') as log_file: 
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
            log_file.write(f"[{timestamp}] {_data}\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = UDPListenerApp(root)
    root.mainloop()