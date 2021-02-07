from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QCoreApplication
import time
import os
from PIL import Image
import huffman
import sys
import send
import recv
fail = False  # 错误信息标志
ok = True  # 正确信息标志
encode = 0
decode = 1
mainpath = os.getcwd()  # 获取当前路径
os.environ['PATH'] += os.pathsep + \
    mainpath + '\\source\\Graphviz\\bin'  # 创建虚拟环境变量 使得绘图工具成功使用


def show_error_message(self):  # 报错
    QMessageBox.about(self, "错误", "输入不合法")


def show_hint(self, str):  # 信息提示
    QMessageBox.about(self, "提示", str)


def show_code(self, code):  # 输出编码译码结果
    if code == '':
        show_error_message(self)
    else:
        out_code = ''
        index = 0
        l = len(code)
        code = code.replace("\n", "")
        while l-index > 50:
            out_code += (str(code[index:index+50]+'\n'))  # 每50个字符换行
            index += 50
        out_code += str(code[index:])
        QMessageBox.about(self, "编码/译码结果", out_code)


def show_huffman_tree(directory):  # 打开哈夫曼树图片
    if Image.open(directory).show() == False:
        return fail


def set_save_filename(save_filename, flag):  # 初始化文件保存名称
    if save_filename == "":  # 如果没有输入保存文件名称则由程序设置保存名称
        if flag == 0:
            save_filename = 'encoding'+'_' + \
                str(time.strftime('%Y%m%d%H%M%S'))
        else:
            save_filename = 'decoding'+'_' + \
                str(time.strftime('%Y%m%d%H%M%S'))
    return save_filename


def set_save_directory(save_directory, flag):  # 初始化文件保存路径
    if save_directory == '':  # 如果没有输入保存路径则由程序设置保存路径
        if flag == 0:
            save_directory = 'encoding_file'
        else:
            save_directory = 'decoding_file'
    return save_directory


class Ui_mainWindow(QWidget):  # 主窗口
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(600, 300, 700, 500)
        self.setWindowTitle('Huffman')
        self.setWindowIcon(QIcon(mainpath+'\\source\\luffy.jpg'))
        self.setStyleSheet(
            "QWidget{background-color:#F0FFFF }QPushButton{background:#B0E0E6}QPushButton:hover{background:#E0FFFF}")
        self.encoding = QPushButton('编码', self)
        self.decoding = QPushButton('译码', self)
        self.recv = QPushButton('打开服务器')
        self.recv.clicked.connect(recv.recv_file)
        self.clear = QPushButton('清空默认路径数据', self)
        self.clear.clicked.connect(self.clear_cache)
        self.quit = QPushButton('退出', self)
        self.quit.clicked.connect(QCoreApplication.instance().quit)
        layout = QGridLayout()
        layout.addWidget(self.encoding, 0, 0, 1, 2)
        layout.addWidget(self.decoding, 0, 2, 1, 2)
        layout.addWidget(self.recv, 1, 1, 1, 2)
        layout.addWidget(self.clear, 2, 1, 1, 2)
        layout.addWidget(self.quit, 3, 1, 1, 2)
        self.setLayout(layout)

    def clear_cache(self):  # 清除默认条件下建造的文件
        os.system('rd/s/q '+mainpath+'\\decoding_file')
        os.system('rd/s/q '+mainpath+'\\encoding_file')


class Encoding_Window(QWidget):  # 编码选择窗口
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(600, 300, 700, 500)
        self.setWindowTitle('Huffman_Encoding')
        self.setWindowIcon(QIcon(mainpath+'\\source\\luffy.jpg'))
        self.setStyleSheet(
            "QWidget{background-color:#F0FFFF }QPushButton{background:#B0E0E6}QPushButton:hover{background:#E0FFFF}")
        self.encoding_btn1 = QPushButton('输入字符和权值获取编码规范', self)
        self.encoding_btn2 = QPushButton('输入字符串获得编码结果', self)
        self.encoding_btn3 = QPushButton('输入字符权值文件获取编码规范', self)
        self.encoding_btn4 = QPushButton('输入字符串文件获得编码结果', self)
        self.quit = QPushButton('退出', self)
        self.quit.clicked.connect(QCoreApplication.instance().quit)
        self.back = QPushButton('返回', self)
        layout = QGridLayout()
        layout.addWidget(self.encoding_btn1, 0, 1)
        layout.addWidget(self.encoding_btn2, 1, 1)
        layout.addWidget(self.encoding_btn3, 2, 1)
        layout.addWidget(self.encoding_btn4, 3, 1)
        layout.addWidget(self.back, 4, 0)
        layout.addWidget(self.quit, 4, 2)
        self.setLayout(layout)


class Encoding_Window_1(QWidget):  # 编码子窗口
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(600, 300, 700, 500)
        self.setWindowTitle('Huffman_Encoding_1')
        self.setWindowIcon(QIcon(mainpath+'\\source\\luffy.jpg'))
        self.setStyleSheet(
            "QWidget{background-color:#F0FFFF }QPushButton{background:#B0E0E6}QPushButton:hover{background:#E0FFFF}")
        self.char_and_weight = ''
        self.save_filename = ''
        self.save_directory = ''
        self.label_1 = QLabel(self)
        self.label_1.setText("请输入字符和权值(格式a 11)用空格隔开:")
        self.textEdit = QTextEdit()
        self.btn_1 = QPushButton('确认编码')
        self.btn_1.clicked.connect(self.get_text)
        self.btn_1.clicked.connect(self.encoding)
        self.label_2 = QLabel(self)
        self.label_2.setText('请输入保存文件名称:')
        self.lineEdit_1 = QLineEdit()
        self.btn_2 = QPushButton('确认保存文件名称')
        self.btn_2.clicked.connect(self.setfilename)
        self.lineEdit_2 = QLineEdit()
        self.btn_3 = QPushButton('选择文件保存路径')
        self.btn_3.clicked.connect(self.setdirecory)
        self.btn_4 = QPushButton('显示赫夫曼树')
        self.btn_4.clicked.connect(lambda: show_huffman_tree(self.save_directory+'/'+self.save_filename +
                                                             '/'+self.save_filename+'_'+'picture.png')
                                   if os.path.exists(self.save_directory+'/'+self.save_filename +
                                                     '/'+self.save_filename+'_'+'picture.png') else show_error_message(self)
                                   )  # 显示哈夫曼树
        self.clear = QPushButton('清空')
        self.clear.clicked.connect(self.clear_cache)
        self.send = QPushButton('发送文件')
        self.send.clicked.connect(lambda: send.send_file(
            self.save_directory+'/'+self.save_filename, self.save_filename)
            if (self.save_directory != '' and self.save_filename != '') else show_error_message(self))
        self.quit = QPushButton('退出', self)
        self.quit.clicked.connect(QCoreApplication.instance().quit)
        self.back = QPushButton('返回', self)
        self.back.clicked.connect(self.clear_cache)
        layout = QGridLayout()
        layout.addWidget(self.label_1, 0, 2)
        layout.addWidget(self.textEdit, 1, 0, 2, 5)
        layout.addWidget(self.label_2, 3, 0, 1, 1)
        layout.addWidget(self.lineEdit_1, 3, 1, 1, 3)
        layout.addWidget(self.btn_2, 3, 4, 1, 1)
        layout.addWidget(self.lineEdit_2, 5, 0, 1, 3)
        layout.addWidget(self.btn_3, 5, 3, 1, 2)
        layout.addWidget(self.btn_1, 6, 0, 1, 5)
        layout.addWidget(self.btn_4, 7, 0, 1, 5)
        layout.addWidget(self.clear, 8, 0, 1, 5)
        layout.addWidget(self.send, 9, 0, 1, 5)
        layout.addWidget(self.back, 10, 0, 1, 2)
        layout.addWidget(self.quit, 10, 3, 1, 2)
        self.setLayout(layout)

    def get_text(self):
        text = str(self.textEdit.toPlainText())  # 获取text中的输入的字符权重信息
        self.char_and_weight = text

    def setfilename(self):
        line = str(self.lineEdit_1.text())  # 获取line中设定的文件名称
        self.save_filename = line

    def setdirecory(self):
        save_directory = QFileDialog.getExistingDirectory(
            self, '选择文件路径')  # 获取文件保存路径
        self.save_directory = save_directory
        self.lineEdit_2.setText(save_directory)  # 在line中显示路径

    def encoding(self):
        self.save_filename = set_save_filename(
            self.save_filename, encode)  # 设置保存名称
        self.save_directory = set_save_directory(
            self.save_directory, encode)  # 设置保存路径
        if self.char_and_weight == '':
            show_error_message(self)
        else:
            flag = huffman.Encoding_1(str(self.char_and_weight),
                                      str(self.save_filename), str(self.save_directory))
            if flag == fail:
                show_error_message(self)

    def clear_cache(self):  # 清空缓存
        self.char_and_weight = ''
        self.save_filename = ''
        self.save_directory = ''
        self.textEdit.clear()
        self.lineEdit_1.clear()
        self.lineEdit_2.clear()


class Encoding_Window_2(QWidget):  # 编码子窗口
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(600, 300, 700, 500)
        self.setWindowTitle('Huffman_Encoding_2')
        self.setWindowIcon(QIcon(mainpath+'\\source\\luffy.jpg'))
        self.setStyleSheet(
            "QWidget{background-color:#F0FFFF }QPushButton{background:#B0E0E6}QPushButton:hover{background:#E0FFFF}")
        self.str = ''
        self.save_filename = ''
        self.save_directory = ''
        self.encode_table_directory = ''
        self.encode_table_filename = ''
        self.code = ''
        self.label_1 = QLabel(self)
        self.label_1.setText("请输入字符串:")
        self.textEdit = QTextEdit()
        self.label_2 = QLabel(self)
        self.label_2.setText('请输入保存文件名称:')
        self.lineEdit_1 = QLineEdit()
        self.btn_2 = QPushButton('确认保存文件名称')
        self.btn_2.clicked.connect(self.setfilename)
        self.lineEdit_2 = QLineEdit()
        self.btn_3 = QPushButton('选择已有编码规范(文件夹)')
        self.btn_3.clicked.connect(self.openencodefile)
        self.lineEdit_3 = QLineEdit()
        self.btn_4 = QPushButton('选择文件保存路径')
        self.btn_4.clicked.connect(self.setdirecory)
        self.btn_1 = QPushButton('确认编码')
        self.btn_1.clicked.connect(self.get_text)
        self.btn_1.clicked.connect(self.encoding)
        self.btn_5 = QPushButton('显示赫夫曼树')
        self.btn_5.clicked.connect(self.show_huffman)
        self.btn_6 = QPushButton('显示编码结果')
        self.btn_6.clicked.connect(lambda: show_code(self, self.code))
        self.send = QPushButton('发送文件')
        self.send.clicked.connect(lambda: send.send_file(
            self.save_directory+'/'+self.save_filename, self.save_filename)
            if (self.save_directory != '' and self.save_filename != '') else show_error_message(self))
        self.claer = QPushButton('清空')
        self.claer.clicked.connect(self.clear_cache)
        self.quit = QPushButton('退出', self)
        self.quit.clicked.connect(QCoreApplication.instance().quit)
        self.back = QPushButton('返回', self)
        self.back.clicked.connect(self.clear_cache)
        layout = QGridLayout()
        layout.addWidget(self.label_1, 0, 2)
        layout.addWidget(self.textEdit, 1, 0, 2, 5)
        layout.addWidget(self.label_2, 3, 0, 1, 1)
        layout.addWidget(self.lineEdit_1, 3, 1, 1, 3)
        layout.addWidget(self.btn_2, 3, 4, 1, 1)
        layout.addWidget(self.lineEdit_2, 4, 0, 1, 3)
        layout.addWidget(self.btn_3, 4, 3, 1, 2)
        layout.addWidget(self.lineEdit_3, 5, 0, 1, 3)
        layout.addWidget(self.btn_4, 5, 3, 1, 2)
        layout.addWidget(self.btn_1, 6, 0, 1, 5)
        layout.addWidget(self.btn_5, 7, 0, 1, 5)
        layout.addWidget(self.btn_6, 8, 0, 1, 5)
        layout.addWidget(self.send, 9, 0, 1, 5)
        layout.addWidget(self.claer, 10, 0, 1, 5)
        layout.addWidget(self.back, 11, 0, 1, 2)
        layout.addWidget(self.quit, 11, 3, 1, 2)
        self.setLayout(layout)

    def get_text(self):
        text = self.textEdit.toPlainText()  # 获取text中输入的字符串
        self.str = text

    def setfilename(self):
        line = self.lineEdit_1.text()  # 获取line中输入的保存文件名称
        self.save_filename = line

    def openencodefile(self):
        encode_file = QFileDialog.getExistingDirectory(
            self, '选择文件路径')  # 获取编码规范的路径
        if encode_file != '':
            self.lineEdit_2.setText(encode_file)
            self.encode_table_directory = encode_file
            pos = len(encode_file)-1
            while encode_file[pos] != '/':
                pos -= 1
            # 提取出编码规范文件的名称
            self.encode_table_filename = encode_file[pos+1:len(encode_file)]

    def setdirecory(self):  # =
        save_directory = QFileDialog.getExistingDirectory(
            self, '选择文件路径')  # 获取文件保存路径
        self.save_directory = save_directory
        self.lineEdit_3.setText(save_directory)  # 在line中显示路径

    def encoding(self):
        self.save_filename = set_save_filename(self.save_filename, encode)
        self.save_directory = set_save_directory(self.save_directory, encode)
        if self.str == '':
            show_error_message(self)
        else:
            if self.encode_table_directory == '':  # 判断是否有编码规范
                encode_file = fail
            else:
                encode_file = ok
            flag = huffman.Encoding_2(str(self.str), str(
                self.save_filename), str(self.save_directory), str(self.encode_table_directory), str(self.encode_table_filename), encode_file)
            if flag == fail:
                show_error_message(self)
            else:
                f = open(self.save_directory+'/'+self.save_filename +
                         '/'+self.save_filename + '_code.txt', 'r+', encoding='utf-8')  # 保存编码结果
                self.code = f.read()
                f.close()

    def show_huffman(self):
        if (self.encode_table_directory == '' and
                os.path.exists(self.save_directory+'/'+self.save_filename + '/'+self.save_filename+'_'+'picture.png')):
            show_huffman_tree(self.save_directory+'/'+self.save_filename +
                              '/'+self.save_filename+'_'+'picture.png')  # 打开生成的哈夫曼树
        elif os.path.exists(self.encode_table_directory+'/'
                            '/'+self.encode_table_filename+'_'+'picture.png'):
            show_huffman_tree(self.encode_table_directory +
                              '/'+self.encode_table_filename+'_'+'picture.png')  # 打开编码规范的哈夫曼树 在已有编码规范下编码不生成哈夫曼树
        else:
            show_error_message(self)

    def clear_cache(self):  # 清除缓存
        self.str = ''
        self.save_filename = ''
        self.save_directory = ''
        self.encode_table_directory = ''
        self.encode_table_filename = ''
        self.code = ''
        self.textEdit.clear()
        self.lineEdit_1.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()


class Encoding_Window_3(QWidget):  # 编码子窗口
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(600, 300, 700, 500)
        self.setWindowTitle('Huffman_Encoding_3')
        self.setWindowIcon(QIcon(mainpath+'\\source\\luffy.jpg'))
        self.setStyleSheet(
            "QWidget{background-color:#F0FFFF }QPushButton{background:#B0E0E6}QPushButton:hover{background:#E0FFFF}")
        self.char_and_weight_directory = ''
        self.save_filename = ''
        self.save_directory = ''
        self.label_1 = QLabel(self)
        self.label_1.setText('文件中的内容需要是频度表 如(A 12) !')
        self.lineEdit_1 = QLineEdit()
        self.btn_1 = QPushButton('选择待编码文件')
        self.btn_1.clicked.connect(self.openfile)
        self.btn_2 = QPushButton('确认编码')
        self.btn_2.clicked.connect(self.encoding)
        self.label_2 = QLabel(self)
        self.label_2.setText('请输入保存文件名称:')
        self.lineEdit_2 = QLineEdit()
        self.btn_3 = QPushButton('确认保存文件名称')
        self.btn_3.clicked.connect(self.setfilename)
        self.lineEdit_3 = QLineEdit()
        self.btn_4 = QPushButton('选择文件保存路径')
        self.btn_4.clicked.connect(self.setdirecory)
        self.btn_5 = QPushButton('显示赫夫曼树')
        self.btn_5.clicked.connect(lambda: show_huffman_tree(self.save_directory+'/'+self.save_filename +
                                                             '/'+self.save_filename+'_'+'picture.png')
                                   if os.path.exists(self.save_directory+'/'+self.save_filename +
                                                     '/'+self.save_filename+'_'+'picture.png') else show_error_message(self))  # 显示哈夫曼树
        self.send = QPushButton('发送文件')
        self.send.clicked.connect(lambda: send.send_file(
            self.save_directory+'/'+self.save_filename, self.save_filename)
            if (self.save_directory != '' and self.save_filename != '') else show_error_message(self))
        self.clear = QPushButton('清空')
        self.clear.clicked.connect(self.clear_cache)
        self.quit = QPushButton('退出', self)
        self.quit.clicked.connect(QCoreApplication.instance().quit)
        self.back = QPushButton('返回', self)
        self.back.clicked.connect(self.clear_cache)
        layout = QGridLayout()
        layout.addWidget(self.label_1, 0, 2)
        layout.addWidget(self.lineEdit_1, 1, 0, 1, 3)
        layout.addWidget(self.btn_1, 1, 3, 1, 2)
        layout.addWidget(self.label_2, 2, 0, 1, 1)
        layout.addWidget(self.lineEdit_2, 2, 1, 1, 3)
        layout.addWidget(self.btn_3, 2, 4, 1, 1)
        layout.addWidget(self.lineEdit_3, 4, 0, 1, 3)
        layout.addWidget(self.btn_4, 4, 3, 1, 2)
        layout.addWidget(self.btn_2, 5, 0, 1, 5)
        layout.addWidget(self.btn_5, 6, 0, 1, 5)
        layout.addWidget(self.send, 7, 0, 1, 5)
        layout.addWidget(self.clear, 8, 0, 1, 5)
        layout.addWidget(self.back, 9, 0, 1, 2)
        layout.addWidget(self.quit, 9, 3, 1, 2)
        self.setLayout(layout)

    def openfile(self):
        openfile_name = QFileDialog.getOpenFileName(
            self, '选择文件', '', '文本文档(*.txt)')  # 打开txt文件
        self.lineEdit_1.setText(openfile_name[0])  # 显示获取文件路径
        self.char_and_weight_directory = openfile_name[0]

    def setfilename(self):
        line = self.lineEdit_2.text()  # 从line中获取输入的保存文件名称
        self.save_filename = line

    def setdirecory(self):
        save_directory = QFileDialog.getExistingDirectory(
            self, '选择文件路径')  # 获取文件保存路径
        self.lineEdit_3.setText(save_directory)  # 在line中显示路径
        self.save_directory = self.save_directory

    def encoding(self):
        self.save_filename = set_save_filename(self.save_filename, encode)
        self.save_directory = set_save_directory(self.save_directory, encode)
        if self.char_and_weight_directory == None:
            show_error_message(self)
        else:
            flag = huffman.Encoding_3(str(self.char_and_weight_directory),
                                      str(self.save_filename), str(self.save_directory))
            if flag == fail:
                show_error_message(self)

    def clear_cache(self):  # 清除缓存
        self.char_and_weight_directory = ''
        self.save_filename = ''
        self.save_directory = ''
        self.lineEdit_1.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()


class Encoding_Window_4(QWidget):  # 编码子窗口
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(600, 300, 700, 500)
        self.setWindowTitle('Huffman_Encoding_4')
        self.setWindowIcon(QIcon(mainpath+'\\source\\luffy.jpg'))
        self.setStyleSheet(
            "QWidget{background-color:#F0FFFF}QPushButton{background:#B0E0E6}QPushButton:hover{background:#E0FFFF}")
        self.str_directory = ''
        self.save_filename = ''
        self.save_directory = ''
        self.encode_table_directory = ''
        self.encode_table_filename = ''
        self.code = ''
        self.label_1 = QLabel(self)
        self.label_1.setText('文件中的内容需要是字符串!')
        self.lineEdit_1 = QLineEdit()
        self.btn_1 = QPushButton('选择待编码文件')
        self.btn_1.clicked.connect(self.setencodefile)
        self.label_2 = QLabel(self)
        self.label_2.setText('请输入保存文件名称:')
        self.lineEdit_2 = QLineEdit()
        self.btn_2 = QPushButton('确认保存文件名称')
        self.btn_2.clicked.connect(self.setfilename)
        self.lineEdit_3 = QLineEdit()
        self.btn_3 = QPushButton('选择已有编码规范')
        self.btn_3.clicked.connect(self.openencodefile)
        self.lineEdit_4 = QLineEdit()
        self.btn_4 = QPushButton('选择文件保存路径')
        self.btn_4.clicked.connect(self.setdirecory)
        self.btn_5 = QPushButton('确认编码')
        self.btn_5.clicked.connect(self.encoding)
        self.btn_6 = QPushButton('显示赫夫曼树')
        self.btn_6.clicked.connect(self.show_huffman)
        self.btn_7 = QPushButton('显示编码结果')
        self.btn_7.clicked.connect(lambda: show_code(self, self.code))
        self.send = QPushButton('发送文件')
        self.send.clicked.connect(lambda: send.send_file(
            self.save_directory+'/'+self.save_filename, self.save_filename)
            if (self.save_directory != '' and self.save_filename != '') else show_error_message(self))
        self.clear = QPushButton('清空')
        self.clear.clicked.connect(self.clear_cache)
        self.quit = QPushButton('退出', self)
        self.quit.clicked.connect(QCoreApplication.instance().quit)
        self.back = QPushButton('返回', self)
        self.back.clicked.connect(self.clear_cache)
        layout = QGridLayout()
        layout.addWidget(self.label_1, 0, 2)
        layout.addWidget(self.lineEdit_1, 1, 0, 1, 3)
        layout.addWidget(self.btn_1, 1, 3, 1, 2)
        layout.addWidget(self.label_2, 3, 0, 1, 1)
        layout.addWidget(self.lineEdit_2, 3, 1, 1, 3)
        layout.addWidget(self.btn_2, 3, 4, 1, 1)
        layout.addWidget(self.lineEdit_3, 4, 0, 1, 3)
        layout.addWidget(self.btn_3, 4, 3, 1, 2)
        layout.addWidget(self.lineEdit_4, 5, 0, 1, 3)
        layout.addWidget(self.btn_4, 5, 3, 1, 2)
        layout.addWidget(self.btn_5, 6, 0, 1, 5)
        layout.addWidget(self.btn_6, 7, 0, 1, 5)
        layout.addWidget(self.btn_7, 8, 0, 1, 5)
        layout.addWidget(self.send, 9, 0, 1, 5)
        layout.addWidget(self.clear, 10, 0, 1, 5)
        layout.addWidget(self.back, 11, 0, 1, 2)
        layout.addWidget(self.quit, 11, 3, 1, 2)
        self.setLayout(layout)

    def openencodefile(self):
        encode_file = QFileDialog.getExistingDirectory(
            self, '选择文件路径')  # 获取编码规范的文件路径
        if encode_file != '':
            self.lineEdit_3.setText(encode_file)
            self.encode_table_directory = encode_file
            pos = len(encode_file)-1
            while encode_file[pos] != '/':
                pos -= 1
            # 提取出编码规范文件的名称
            self.encode_table_filename = encode_file[pos+1:len(encode_file)]

    def setencodefile(self):
        openfile_name = QFileDialog.getOpenFileName(
            self, '选择文件', '', '文本文档(*.txt)')  # 代开待编译的txt文件
        self.lineEdit_1.setText(openfile_name[0])  # 在line中显示文件路径
        self.str_directory = openfile_name[0]

    def setfilename(self):
        line = self.lineEdit_2.text()  # 从line中获取保存文件名称
        self.save_filename = line

    def setdirecory(self):
        save_directory = QFileDialog.getExistingDirectory(
            self, '选择文件路径')  # 获取文件保存路径
        self.lineEdit_4.setText(save_directory)  # 在line中显示路径
        self.save_directory = save_directory

    def encoding(self):
        self.save_filename = set_save_filename(self.save_filename, encode)
        self.save_directory = set_save_directory(self.save_directory, encode)
        if self.str_directory == '':
            show_error_message(self)
        else:
            if self.encode_table_directory == '':
                encode_file = fail
            else:
                encode_file = ok
            flag = huffman.Encoding_4(str(self.str_directory), str(
                self.save_filename), str(self.save_directory), str(self.encode_table_directory), str(self.encode_table_filename), encode_file)
            if flag == fail:
                show_error_message(self)
            else:
                f = open(self.save_directory+'/'+self.save_filename +
                         '/'+self.save_filename + '_code.txt', 'r+', encoding='utf-8')
                self.code = f.read()
                f.close()

    def show_huffman(self):
        print(self.encode_table_directory+'/'
              + self.encode_table_filename+'_'+'picture.png')
        if (self.encode_table_directory == '' and
                os.path.exists(self.save_directory+'/'+self.save_filename + '/'+self.save_filename+'_'+'picture.png')):
            show_huffman_tree(self.save_directory+'/'+self.save_filename +
                              '/'+self.save_filename+'_'+'picture.png')  # 打开哈夫曼树树图片
        elif os.path.exists(self.encode_table_directory+'/'
                            '/'+self.encode_table_filename+'_'+'picture.png'):
            show_huffman_tree(self.encode_table_directory +
                              '/'+self.encode_table_filename+'_'+'picture.png')  # 打开编码规范的哈夫曼树 在已有编码规范下编码不生成哈夫曼树
        else:
            show_error_message(self)

    def clear_cache(self):
        self.str_directory = ''
        self.save_filename = ''
        self.save_directory = ''
        self.encode_table_directory = ''
        self.code = ''
        self.lineEdit_1.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.lineEdit_4.clear()


class Decoding_Window(QWidget):  # 译码选择窗口
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(600, 300, 700, 500)
        self.setWindowTitle('Huffman_Decoding')
        self.setWindowIcon(QIcon(mainpath+'\\source\\luffy.jpg'))
        self.setStyleSheet(
            "QWidget{background-color:#F0FFFF }QPushButton{background:#B0E0E6}QPushButton:hover{background:#E0FFFF}")
        self.decoding_btn1 = QPushButton('输入译码表和代码获得信息', self)
        self.decoding_btn2 = QPushButton('输入译码表文件和代码文件获得信息', self)
        self.decoding_btn3 = QPushButton('输入译码表文件和代码获得信息', self)
        self.quit = QPushButton('退出', self)
        self.quit.clicked.connect(QCoreApplication.instance().quit)
        self.back = QPushButton('返回', self)
        layout = QGridLayout()
        layout.addWidget(self.decoding_btn1, 0, 1)
        layout.addWidget(self.decoding_btn2, 1, 1)
        layout.addWidget(self.decoding_btn3, 2, 1)
        layout.addWidget(self.back, 3, 0)
        layout.addWidget(self.quit, 3, 2)
        self.setLayout(layout)


class Decoding_Window_1(QWidget):  # 译码子窗口
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):  # TODO 译码操作
        self.setGeometry(600, 300, 700, 500)
        self.setWindowTitle('Huffman_Decoding_1')
        self.setWindowIcon(QIcon(mainpath+'\\source\\luffy.jpg'))
        self.setStyleSheet(
            "QWidget{background-color:#F0FFFF }QPushButton{background:#B0E0E6}QPushButton:hover{background:#E0FFFF}")
        self.codetochar = ''
        self.code = ''
        self.save_filename = ''
        self.save_directory = ''
        self.str = ''
        self.label_1 = QLabel(self)
        self.label_1.setText("请输入译码表(格式 01 a)用空格隔开:")
        self.textEdit_1 = QTextEdit()
        self.btn_1 = QPushButton('确认')
        self.btn_1.clicked.connect(self.get_text_1)
        self.label_2 = QLabel(self)
        self.label_2.setText("请输入代码:")
        self.textEdit_2 = QTextEdit()
        self.btn_2 = QPushButton('确认')
        self.btn_2.clicked.connect(self.get_text_2)
        self.lineEdit_1 = QLineEdit()
        self.btn_3 = QPushButton('确认保存文件名称')
        self.btn_3.clicked.connect(self.setfilename)
        self.lineEdit_2 = QLineEdit()
        self.btn_4 = QPushButton('选择文件保存路径')
        self.btn_4.clicked.connect(self.setdirecory)
        self.btn_5 = QPushButton('确认译码并显示译码结果')
        self.btn_5.clicked.connect(self.decoding)
        self.clear = QPushButton('清空')
        self.clear.clicked.connect(self.clear_cache)
        self.quit = QPushButton('退出', self)
        self.quit.clicked.connect(QCoreApplication.instance().quit)
        self.back = QPushButton('返回', self)
        self.back.clicked.connect(self.clear_cache)
        layout = QGridLayout()
        layout.addWidget(self.label_1, 0, 2)
        layout.addWidget(self.textEdit_1, 1, 0, 1, 3)
        layout.addWidget(self.btn_1, 1, 3, 1, 2)
        layout.addWidget(self.label_2, 4, 0)
        layout.addWidget(self.textEdit_2, 5, 0, 1, 3)
        layout.addWidget(self.btn_2, 5, 3, 1, 2)
        layout.addWidget(self.lineEdit_1, 6, 0, 1, 3)
        layout.addWidget(self.btn_3, 6, 3, 1, 2)
        layout.addWidget(self.lineEdit_2, 7, 0, 1, 3)
        layout.addWidget(self.btn_4, 7, 3, 1, 2)
        layout.addWidget(self.btn_5, 9, 0, 1, 5)
        layout.addWidget(self.clear, 11, 0, 1, 5)
        layout.addWidget(self.back, 12, 0, 1, 2)
        layout.addWidget(self.quit, 12, 3, 1, 2)
        self.setLayout(layout)

    def get_text_1(self):
        text = self.textEdit_1.toPlainText()  # 从text中获取译码表
        self.codetochar = text

    def get_text_2(self):
        text = self.textEdit_2.toPlainText()  # 从text中获取代码
        self.code = text

    def setfilename(self):
        line = self.lineEdit_1.text()  # 从line中获取保存文件名称
        self.save_filename = line

    def setdirecory(self):
        save_directory = QFileDialog.getExistingDirectory(
            self, '选择文件路径')  # 获取文件保存路径
        self.lineEdit_2.setText(save_directory)  # 在line中显示路径
        self.save_directory = save_directory

    def decoding(self):
        self.save_filename = set_save_filename(self.save_filename, decode)
        self.save_directory = set_save_directory(self.save_directory, decode)
        if self.codetochar == None or self.code == None:
            show_error_message(self)
        else:
            print(self.codetochar)
            ans = huffman.Decoding_1(str(self.codetochar), str(self.code),
                                     str(self.save_filename), str(self.save_directory))
            if ans == fail:
                show_error_message(self)
            else:
                self.str = ans
                show_code(self, self.str)  # 显示译码结果

    def clear_cache(self):  # 清除缓存
        self.codetochar = ''
        self.decode = ''
        self.save_filename = ''
        self.save_directory = ''
        self.str = ''
        self.textEdit_1.clear()
        self.textEdit_2.clear()
        self.lineEdit_1.clear()
        self.lineEdit_2.clear()


class Decoding_Window_2(QWidget):  # 译码子窗口
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):  # TODO 译码操作
        self.setGeometry(600, 300, 700, 300)
        self.setWindowTitle('Huffman_Decoding_2')
        self.setWindowIcon(QIcon(mainpath+'\\source\\luffy.jpg'))
        self.setStyleSheet(
            "QWidget{background-color:#F0FFFF }QPushButton{background:#B0E0E6}QPushButton:hover{background:#E0FFFF}")
        self.decode_table_directory = ''
        self.decode_table_filename = ''
        self.code_directory = ''
        self.save_filename = ''
        self.save_directory = ''
        self.str = ''
        self.lineEdit_1 = QLineEdit()
        self.btn_1 = QPushButton('选择已有的编码规范(文件夹)')
        self.btn_1.clicked.connect(self.openfile_1)
        self.lineEdit_2 = QLineEdit()
        self.btn_2 = QPushButton('选择代码文件')
        self.btn_2.clicked.connect(self.openfile_2)
        self.lineEdit_3 = QLineEdit()
        self.btn_3 = QPushButton('确认保存文件名称')
        self.btn_3.clicked.connect(self.setfilename)
        self.lineEdit_4 = QLineEdit()
        self.btn_4 = QPushButton('选择文件保存路径')
        self.btn_4.clicked.connect(self.setdirecory)
        self.btn_5 = QPushButton('确认译码并显示译码结果')
        self.btn_5.clicked.connect(self.decoding)
        self.clear = QPushButton('清空')
        self.clear.clicked.connect(self.clear_cache)
        self.quit = QPushButton('退出', self)
        self.quit.clicked.connect(QCoreApplication.instance().quit)
        self.back = QPushButton('返回', self)
        self.back.clicked.connect(self.clear_cache)
        layout = QGridLayout()
        layout.addWidget(self.lineEdit_1, 0, 0, 1, 3)
        layout.addWidget(self.btn_1, 0, 3, 1, 2)
        layout.addWidget(self.lineEdit_2, 1, 0, 1, 3)
        layout.addWidget(self.btn_2, 1, 3, 1, 2)
        layout.addWidget(self.lineEdit_3, 2, 0, 1, 3)
        layout.addWidget(self.btn_3, 2, 3, 1, 2)
        layout.addWidget(self.lineEdit_4, 3, 0, 1, 3)
        layout.addWidget(self.btn_4, 3, 3, 1, 2)
        layout.addWidget(self.btn_5, 4, 0, 1, 5)
        layout.addWidget(self.clear, 6, 0, 1, 5)
        layout.addWidget(self.back, 7, 0, 1, 2)
        layout.addWidget(self.quit, 7, 3, 1, 2)
        self.setLayout(layout)

    def openfile_1(self):
        decode_file = QFileDialog.getExistingDirectory(
            self, '选择文件路径')  # 获取编码规范路径
        if decode_file != '':
            self.lineEdit_1.setText(decode_file)
            self.decode_table_directory = decode_file
            pos = len(decode_file)-1
            while decode_file[pos] != '/':
                pos -= 1
            # 提取编码规范名称
            self.decode_table_filename = decode_file[pos+1:len(decode_file)]

    def openfile_2(self):
        openfile_name = QFileDialog.getOpenFileName(
            self, '选择文件', '', '文本文档(*.txt)')  # 打开代码文件
        self.lineEdit_2.setText(openfile_name[0])  # 在line中显示路径
        self.code_directory = openfile_name[0]

    def setfilename(self):
        line = self.lineEdit_3.text()  # 从line中获取保存文件名称
        self.save_filename = line

    def setdirecory(self):
        save_directory = QFileDialog.getExistingDirectory(
            self, '选择文件路径')  # 获取文件保存路径
        self.lineEdit_4.setText(save_directory)  # 在line中显示路径
        self.save_directory = save_directory

    def decoding(self):
        self.save_filename = set_save_filename(self.save_filename, decode)
        self.save_directory = set_save_directory(self.save_directory, decode)
        if self.decode_table_directory == '' or self.code_directory == '':
            show_error_message(self)
        else:
            ans = huffman.Decoding_2(str(self.decode_table_directory+'/'+self.decode_table_filename+'_decode_table.txt'),
                                     str(self.code_directory), str(self.save_filename), str(self.save_directory))
            if ans == fail:
                show_error_message(self)
            else:
                self.str = ans
                show_code(self, self.str)  # 显示译码结果

    def clear_cache(self):  # 清除缓存
        self.decode_table_directory = ''
        self.decode_table_filename = ''
        self.code_directory = ''
        self.save_filename = ''
        self.save_directory = ''
        self.str = ''
        self.lineEdit_1.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.lineEdit_4.clear()


class Decoding_Window_3(QWidget):  # 译码子窗口
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(600, 300, 700, 300)
        self.setWindowTitle('Huffman_Decoding_3')
        self.setWindowIcon(QIcon(mainpath+'\\source\\luffy.jpg'))
        self.setStyleSheet(
            "QWidget{background-color:#F0FFFF }QPushButton{background:#B0E0E6}QPushButton:hover{background:#E0FFFF}")
        self.decode_table_directory = ''
        self.decode_table_filename = ''
        self.code = ''
        self.save_filename = ''
        self.save_directory = ''
        self.str = ''
        self.lineEdit_1 = QLineEdit()
        self.btn_1 = QPushButton('选择已有的编码规范(文件夹)')
        self.btn_1.clicked.connect(self.openfile_1)
        self.label_2 = QLabel(self)
        self.label_2.setText("请输入代码:")
        self.textEdit_1 = QTextEdit()
        self.btn_2 = QPushButton('确认')
        self.btn_2.clicked.connect(self.get_text_1)
        self.lineEdit_2 = QLineEdit()
        self.btn_3 = QPushButton('确认保存文件名称')
        self.btn_3.clicked.connect(self.setfilename)
        self.lineEdit_3 = QLineEdit()
        self.btn_4 = QPushButton('选择文件保存路径')
        self.btn_4.clicked.connect(self.setdirecory)
        self.btn_5 = QPushButton('确认译码并显示译码结果')
        self.btn_5.clicked.connect(self.decoding)
        self.clear = QPushButton('清空')
        self.clear.clicked.connect(self.clear_cache)
        self.quit = QPushButton('退出', self)
        self.quit.clicked.connect(QCoreApplication.instance().quit)
        self.back = QPushButton('返回', self)
        self.back.clicked.connect(self.clear_cache)
        layout = QGridLayout()
        layout.addWidget(self.lineEdit_1, 0, 0, 1, 3)
        layout.addWidget(self.btn_1, 0, 3, 1, 2)
        layout.addWidget(self.label_2, 1, 0)
        layout.addWidget(self.textEdit_1, 2, 0, 1, 3)
        layout.addWidget(self.btn_2, 2, 3, 1, 2)
        layout.addWidget(self.lineEdit_2, 3, 0, 1, 3)
        layout.addWidget(self.btn_3, 3, 3, 1, 2)
        layout.addWidget(self.lineEdit_3, 4, 0, 1, 3)
        layout.addWidget(self.btn_4, 4, 3, 1, 2)
        layout.addWidget(self.btn_5, 5, 0, 1, 5)
        layout.addWidget(self.clear, 6, 0, 1, 5)
        layout.addWidget(self.back, 7, 0, 1, 2)
        layout.addWidget(self.quit, 7, 3, 1, 2)
        self.setLayout(layout)

    def openfile_1(self):
        decode_file = QFileDialog.getExistingDirectory(
            self, '选择文件路径')  # 获取编码规范路径
        if decode_file != '':
            self.lineEdit_1.setText(decode_file)
            self.decode_table_directory = decode_file
            pos = len(decode_file)-1
            while decode_file[pos] != '/':
                pos -= 1
            # 提取编码规范名称
            self.decode_table_filename = decode_file[pos+1:len(decode_file)]

    def get_text_1(self):
        text = self.textEdit_1.toPlainText()  # 从text中获取代码
        self.code = text

    def setfilename(self):
        line = self.lineEdit_2.text()  # 从line中获取保存名称
        self.save_filename = line

    def setdirecory(self):
        save_directory = QFileDialog.getExistingDirectory(
            self, '选择文件路径')  # 获取文件保存路径
        self.lineEdit_3.setText(save_directory)  # 在line中显示路径
        self.save_directory = save_directory

    def decoding(self):
        self.save_filename = set_save_filename(self.save_filename, decode)
        self.save_directory = set_save_directory(self.save_directory, decode)
        if self.decode_table_directory == '' or self.code == '':
            show_error_message(self)
        else:
            ans = huffman.Decoding_3(str(self.decode_table_directory+'/'+self.decode_table_filename+'_decode_table.txt'),
                                     str(self.code), str(self.save_filename), str(self.save_directory))
            if ans == fail:
                show_error_message(self)
            else:
                self.str = ans
                show_code(self, self.str)  # 显示译码结果

    def clear_cache(self):  # 清除缓存
        self.decode_table_directory = ''
        self.decode_table_filename = ''
        self.code = ''
        self.save_filename = ''
        self.save_directory = ''
        self.str = ''
        self.textEdit_1.clear()
        self.lineEdit_1.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()


def main():
    app = QApplication(sys.argv)  # 运行主循环，必须调用此函数才能开始事件处理
    ui_mainwindow = Ui_mainWindow()
    encoding_window = Encoding_Window()
    encoding_window_1 = Encoding_Window_1()
    encoding_window_2 = Encoding_Window_2()
    encoding_window_3 = Encoding_Window_3()
    encoding_window_4 = Encoding_Window_4()
    decoding_window = Decoding_Window()
    decoding_window_1 = Decoding_Window_1()
    decoding_window_2 = Decoding_Window_2()
    decoding_window_3 = Decoding_Window_3()

    ui_mainwindow.show()
    show_hint(ui_mainwindow, "本程序如果没有修改保存路径和文件名称将在同一个文件中操作")
    ui_mainwindow.encoding.clicked.connect(encoding_window.show)
    ui_mainwindow.encoding.clicked.connect(ui_mainwindow.hide)
    ui_mainwindow.decoding.clicked.connect(decoding_window.show)
    ui_mainwindow.decoding.clicked.connect(ui_mainwindow.hide)

    encoding_window.back.clicked.connect(ui_mainwindow.show)
    encoding_window.back.clicked.connect(encoding_window.hide)
    encoding_window.encoding_btn1.clicked.connect(encoding_window_1.show)
    encoding_window.encoding_btn1.clicked.connect(encoding_window.hide)
    encoding_window.encoding_btn2.clicked.connect(encoding_window_2.show)
    encoding_window.encoding_btn2.clicked.connect(encoding_window.hide)
    encoding_window.encoding_btn2.clicked.connect(
        lambda: show_hint(encoding_window_2, '在选择编码表的选项中若不选择编码表则重新编码。'))
    encoding_window.encoding_btn3.clicked.connect(encoding_window_3.show)
    encoding_window.encoding_btn3.clicked.connect(encoding_window.hide)
    encoding_window.encoding_btn4.clicked.connect(encoding_window_4.show)
    encoding_window.encoding_btn4.clicked.connect(encoding_window.hide)
    encoding_window.encoding_btn4.clicked.connect(
        lambda: show_hint(encoding_window_4, '在选择编码表的选项中若不选择编码表则重新编码。'))

    encoding_window_1.back.clicked.connect(encoding_window.show)
    encoding_window_1.back.clicked.connect(encoding_window_1.hide)
    encoding_window_2.back.clicked.connect(encoding_window.show)
    encoding_window_2.back.clicked.connect(encoding_window_2.hide)
    encoding_window_3.back.clicked.connect(encoding_window.show)
    encoding_window_3.back.clicked.connect(encoding_window_3.hide)
    encoding_window_4.back.clicked.connect(encoding_window.show)
    encoding_window_4.back.clicked.connect(encoding_window_4.hide)

    decoding_window.back.clicked.connect(ui_mainwindow.show)
    decoding_window.back.clicked.connect(decoding_window.hide)
    decoding_window.decoding_btn1.clicked.connect(decoding_window_1.show)
    decoding_window.decoding_btn1.clicked.connect(decoding_window.hide)
    decoding_window.decoding_btn2.clicked.connect(decoding_window_2.show)
    decoding_window.decoding_btn2.clicked.connect(decoding_window.hide)
    decoding_window.decoding_btn3.clicked.connect(decoding_window_3.show)
    decoding_window.decoding_btn3.clicked.connect(decoding_window.hide)

    decoding_window_1.back.clicked.connect(decoding_window.show)
    decoding_window_1.back.clicked.connect(decoding_window_1.hide)
    decoding_window_2.back.clicked.connect(decoding_window.show)
    decoding_window_2.back.clicked.connect(decoding_window_2.hide)
    decoding_window_3.back.clicked.connect(decoding_window.show)
    decoding_window_3.back.clicked.connect(decoding_window_3.hide)

    sys.exit(app.exec_())  # 结束程序


if __name__ == "__main__":
    main()
