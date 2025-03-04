def setUp(self):
    self.root = tk.Tk()  # 创建一个虚拟的 Tk 根窗口
    self.app = SerialTool(self.root)
    self.app.is_open = True  # 确保串口打开状态
    self.app.serial_port = MagicMock()
    self.app.default_directory = os.path.dirname(__file__)
