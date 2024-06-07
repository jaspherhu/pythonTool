import tkinter as tk
from tkinter import messagebox
import bluetooth

class BluetoothSpeedTestApp:
    def __init__(self, master):
        self.master = master
        master.title("Bluetooth Speed Test")

        # 创建一个标签和按钮
        self.label = tk.Label(master, text="Enter the MAC address of the Bluetooth device:")
        self.label.pack()

        self.entry = tk.Entry(master)
        self.entry.pack()

        self.connect_button = tk.Button(master, text="Connect", command=self.connect_device)
        self.connect_button.pack()

        self.send_button = tk.Button(master, text="Send Data", command=self.send_data)
        self.send_button.pack()

        self.speed_label = tk.Label(master, text="Speed: ")
        self.speed_label.pack()

        self.connected = False

    def connect_device(self):
        mac_address = self.entry.get()
        if not mac_address:
            messagebox.showerror("Error", "Please enter a MAC address.")
            return

        try:
            self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            self.sock.connect((mac_address, 1))
            self.connected = True
            messagebox.showinfo("Success", "Connected to device.")
        except bluetooth.btcommon.BluetoothError as e:
            messagebox.showerror("Error", f"Connection failed: {e}")

    def send_data(self):
        if not self.connected:
            messagebox.showerror("Error", "Not connected to any device.")
            return

        data = "Hello World"
        start_time = time.time()
        self.sock.send(data)
        response = self.sock.recv(1024)
        end_time = time.time()

        duration = end_time - start_time
        speed = len(data) / duration / 1024.0  # in KB/s
        self.speed_label.config(text=f"Speed: {speed:.2f} KB/s")

root = tk.Tk()
my_gui = BluetoothSpeedTestApp(root)
root.mainloop()