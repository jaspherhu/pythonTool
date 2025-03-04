import unittest
from unittest.mock import patch, MagicMock
import os
import struct
import zlib
from fileTransUartA02 import SerialTool, FRAME_TYPE_HAND, FRAME_TYPE_INFO, FRAME_TYPE_DATA, FRAME_TYPE_END, FRAME_TYPE_ACK_08, FRAME_TYPE_ACK_02, FRAME_TYPE_ACK_06, FRAME_TYPE_ACK_04, FRAME_TYPE_ACK_08
import tkinter as tk

class TestFileTransUART(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()  # 创建一个虚拟的 Tk 根窗口
        self.app = SerialTool(self.root)
        self.app.is_open = True  # 确保串口打开状态
        self.app.serial_port = MagicMock()
        # self.app.self.serial_port # 将app里面的串口映射到这儿来
        self.app.default_directory = os.path.dirname(__file__)
        # 确保默认目录存在
        if not os.path.exists(self.app.default_directory):
            os.makedirs(self.app.default_directory)

    def tearDown(self):
        self.app.close_serial()
        self.root.destroy()  # 销毁虚拟的 Tk 根窗口

    @patch('fileTransUartA02.open', new_callable=MagicMock)
    def test_send_file(self, mock_open):
        file_path = os.path.join(self.app.default_directory, "test_send_file.bin")
        file_data = b"test data"
        with open(file_path, "wb") as f:
            f.write(file_data)

        # 模拟接收 ACK 帧 0x02
        ack_frame_02 = self.app.create_frame(FRAME_TYPE_ACK_02, b"")
        self.app.process_data(ack_frame_02)  

        # 模拟接收 ACK 帧 0x04
        ack_frame_04 = self.app.create_frame(FRAME_TYPE_ACK_04, b"")
        self.app.process_data(ack_frame_04)

        # 模拟接收 ACK 帧 0x06
        ack_frame_06 = self.app.create_frame(FRAME_TYPE_ACK_06, b"")
        self.app.process_data(ack_frame_06)
        
        # 模拟接收 ACK 帧 0x08
        ack_frame_08 = self.app.create_frame(FRAME_TYPE_ACK_08, b"")
        self.app.process_data(ack_frame_08)

        # 主动发送01帧
        self.app.send_file_protocol(file_path, file_data)

        # 检查发送的帧
        frames = [call[0][0] for call in self.app.serial_port.write.call_args_list]
        # 检查帧数量
        self.assertEqual(len(frames), 4)  # 1 HAND, 1 INFO, 1 DATA, 1 END

        # 检查 HAND 帧
        hand_frame = frames[0]
        self.assertEqual(hand_frame[:2], b'\xaa\xf5')
        self.assertEqual(hand_frame[-1], 0x5a)
        self.assertEqual(hand_frame[2], FRAME_TYPE_HAND)

        # 检查 INFO 帧
        info_frame = frames[1]
        self.assertEqual(info_frame[:2], b'\xaa\xf5')
        self.assertEqual(info_frame[-1], 0x5a)
        self.assertEqual(info_frame[2], FRAME_TYPE_INFO)

        file_name = os.path.basename(file_path).ljust(32, '\0')  # 使用单个字符的字符串
        file_format = os.path.splitext(os.path.basename(file_path))[1][1:].ljust(32, '\0')  # 使用单个字符的字符串
        file_name_encoded = file_name.encode('utf-8')
        file_format_encoded = file_format.encode('utf-8')
        file_size = struct.pack('<I', len(file_data))
        self.assertEqual(info_frame[5:5+32], file_name_encoded)
        self.assertEqual(info_frame[37:37+32], file_format_encoded)
        self.assertEqual(info_frame[69:73], file_size)

        # 检查 DATA 帧
        data_frame = frames[2]
        self.assertEqual(data_frame[:2], b'\xaa\xf5')
        self.assertEqual(data_frame[-1], 0x5a)
        self.assertEqual(data_frame[2], FRAME_TYPE_DATA)
        self.assertEqual(data_frame[5:5+len(file_data)], file_data)

        # 检查 END 帧
        end_frame = frames[3]
        self.assertEqual(end_frame[:2], b'\xaa\xf5')
        self.assertEqual(end_frame[-1], 0x5a)
        self.assertEqual(end_frame[2], FRAME_TYPE_END)
        file_crc = zlib.crc32(file_data) & 0xFFFF
        self.assertEqual(end_frame[5:7], struct.pack('<H', file_crc))

        os.remove(file_path)

    @patch('fileTransUartA02.open', new_callable=MagicMock)
    def test_receive_file(self, mock_open):

        return
    
        file_name = "test_receive_file.bin"
        file_format = "bin"
        file_size = 1024
        file_data = b"test data" * 32
        file_crc = zlib.crc32(file_data) & 0xFFFF

        # 模拟接收 HAND 帧
        hand_frame = self.app.create_frame(FRAME_TYPE_HAND, b'\xaa')
        self.app.process_data(hand_frame)

        # 模拟接收 ACK 帧 0x02
        ack_frame_02 = self.app.create_frame(FRAME_TYPE_ACK_02, b"")
        self.app.process_data(ack_frame_02)

        # 模拟接收 INFO 帧
        file_info = file_name.ljust(32, '\0').encode('utf-8') + file_format.ljust(32, '\0').encode('utf-8') + struct.pack('<I', file_size)
        info_frame = self.app.create_frame(FRAME_TYPE_INFO, file_info)
        self.app.process_data(info_frame)

        # 模拟接收 ACK 帧 0x04
        ack_frame_04 = self.app.create_frame(FRAME_TYPE_ACK_04, b"")
        self.app.process_data(ack_frame_04)

        # 模拟接收 DATA 帧
        # 要给被调用的路径赋值
        self.app.default_directory = r"D:/pythonTool/06 flieTransUart"
        self.app.file_transfer_file_path = os.path.join(self.app.default_directory, file_name)
        self.app.file_transfer_file = open(self.app.file_transfer_file_path, "wb")

        data_frame = self.app.create_frame(FRAME_TYPE_DATA, file_data)
        self.app.process_data(data_frame)

        # 模拟接收 ACK 帧 0x06
        ack_frame_06 = self.app.create_frame(FRAME_TYPE_ACK_06, b"")
        self.app.process_data(ack_frame_06)

        # 模拟接收 END 帕
        end_frame = self.app.create_frame(FRAME_TYPE_END, struct.pack('<H', file_crc))
        self.app.process_data(end_frame)

        # 模拟接收 ACK 帕 0x08
        ack_frame_08 = self.app.create_frame(FRAME_TYPE_ACK_08, b"")
        self.app.process_data(ack_frame_08)

        # 检查保存的文件
        saved_file_path = os.path.join(self.app.default_directory, file_name)
        with open(saved_file_path, "rb") as f:
            saved_file_data = f.read()
        self.assertEqual(saved_file_data, file_data)

        os.remove(saved_file_path)

if __name__ == '__main__':
    unittest.main()