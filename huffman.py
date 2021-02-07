from graphviz import *  # 绘制哈夫曼树工具
import os

fail = False  # 错误信息标志
ok = True  # 正确信息标志
encode = 0
decode = 1
mainpath = os.getcwd()  # 获取当前路径


def mkdir(path):  # 建立路径
    path = path.strip()  # 去除首位空格
    path = path.rstrip("\\")  # 去除尾部 \ 符号
    isExists = os.path.exists(path)
    if not isExists:  # 不存在时创建路径
        os.makedirs(path)  # 穿件文件夹
        desktop = open(path + '\\desktop.ini', 'w+',
                       encoding='utf-8')  # 船舰desktop.ini文件
        desktop.write(
            '''[.ShellClassInfo]
IconResource='''+mainpath+'''\\source\\roger.ico, 0
[ViewState]
Mode=
Vid=
FolderType=Generic
'''
        )  # 自定义文件夹图标与文件加以区分因为本程序是以这文件夹为整体作为导出
        os.system('attrib +h '+path+'\\desktop.ini')  # 命令行操作隐藏desktop.ini
        os.system('attrib +s '+path)  # 刷新是该文件生效
        return True
    else:
        return False


class Node(object):  # 哈夫曼树的节点
    def __init__(self, char=None, weight=None):
        self._char = char  # 节点代表的字符
        self._weight = weight  # 节点的权值
        self._code = ''  # 节点编码
        self._left = None  # 左子树
        self._right = None  # 右子树


class HuffmanTree(object):  # HuffmanTree类 存储哈夫曼树

    def __init__(self, char_weights=None, str=None):  # 初始化
        self.nodes = [Node(part[0], part[1])
                      for part in char_weights]  # 初始化节点
        self.str = str  # 被编码字符穿
        self.codetochar = {}  # 码转字符字典
        self.chartocode = {}  # 字符转码字典
        self.create_huffman_tree()
        if self.root._left == None and self.root._right == None:  # 当只有一个节点时的建树
            self.encoding(self.root, '0')
        else:
            self.encoding(self.root, '')  # 多个节点的建树
        self.make_dic(self.root)  # 建立字符转码 码转字符的字典
        if self.str != None:  # 对于字符串输入进行编码
            self.code = self.coding(self.str)  # 编码结果

    def create_huffman_tree(self):  # 建立哈夫曼树
        while len(self.nodes) != 1:  # 判断是否结束
            self.nodes.sort(key=lambda node: node._weight,
                            reverse=False)  # 通过weight排序 升序
            min = Node(weight=(self.nodes[0]._weight+self.nodes[1]._weight))
            # 最小的两个weight建立新的新的节点
            min._left = self.nodes.pop(0)
            min._right = self.nodes.pop(0)
            # 接上左右孩子，并从现有的节点中删去
            self.nodes.append(min)  # 加上新的节点
        self.root = self.nodes[0]  # 选定根节点

    def encoding(self, node, code):  # 编码操作为每个节点编写哈夫曼码
        if node._char != None:  # 给节点附上编码
            node._code = code
        if node._char == None:  # 绘图是用code作为name 如果code 不赋值会导致判断都从一个根结点出来 防止绘图出现问题
            node._code = 'none'+code
        if node._left != None:  # 进行递归
            temp = code+'0'  # 左边加'0'
            self.encoding(node._left, temp)
        if node._right != None:  # 进行递归
            temp = code+'1'  # 右边加'1'
            self.encoding(node._right, temp)

    def make_dic(self, node):  # 递归建立字典
        if node._char != None:
            self.codetochar[node._code] = node._char  # 建立码转字符字典
            self.chartocode[node._char] = node._code  # 建立字符转码字典
        if node._left != None:  # 进行递归
            self.make_dic(node._left)
        if node._right != None:  # 进行递归
            self.make_dic(node._right)

    def coding(self, str):  # 对str进行编码
        code = ''
        for i in range(len(str)):
            code += self.chartocode[str[i]]  # 在字典中查找
        return code


class draw_HuffmanTree(object):  # 利用graphviz绘制哈夫曼树
    def __init__(self, huffman_tree):  # 初始化
        # 保存为png格式
        self.dot = Digraph(comment='HuffmanTree', format='png')
        self.create_nodes(huffman_tree.root)
        self.link_nodes(huffman_tree.root)

    def create_nodes(self, node):  # 递归建立节点
        self.dot.node(str(node._code), str(
            node._char)+str(':')+str(node._weight), color='red', fontname='Microsoft YaHei')  # 设定节点类型 格式位 字符：权值
        if node._left != None:  # 进行递归
            self.create_nodes(node._left)
        if node._right != None:  # 进行递归
            self.create_nodes(node._right)

    def link_nodes(self, node):  # 递归建立边连接节点
        if node._left != None:  # 左边的边上写 0进行递归
            self.dot.edge(str(node._code), str(
                node._left._code), '0', color='green')
            self.link_nodes(node._left)
        if node._right != None:  # 右边的边上写1进行递归
            self.dot.edge(str(node._code), str(
                node._right._code), '1', color='green')
            self.link_nodes(node._right)

    def export(self, directory):  # 导出图片
        # 由于graphviz为第三方插件 使用pyinstaller进行打包不会包含 所以采取使用命令行的操作导出图片
        dotfile = open(directory, 'w+', encoding='utf-8')  # 先将dot资料写入一个文件中
        dotfile.write(self.dot.source)
        dotfile.close()
        com = 'dot '+directory + ' -T png -o ' + directory+'.png'  # 使用命令导出为png图片
        os.system(com)


def Encoding_1(char_and_weight, save_filename, save_directory):  # 进行第一种情况的编码
    char_weights = char_and_weight_to_char_weights(
        str(char_and_weight))    # 将输入的字符和权值组成tuple放在list中
    if char_weights == fail:  # 判断输入是否有误
        return fail
    else:
        return encoding_without_table(
            char_weights, save_filename, save_directory, fail)  # 进行没有编码规范的编码 制作编码规范


def Encoding_2(string, save_filename, save_directory, encode_table_directory, encode_table_filename, encode_file):  # 进行第二种情况的编码
    if encode_file == fail:  # 判断是否已经有编码规范
        char_weights = str_to_char_weights(
            str(string))  # 将输入的字符串组成tuple放在list中
        return encoding_without_table(char_weights, save_filename,
                                      save_directory, ok, string)  # 进行没有编码规范的编码 建立一个编码规范 输出代码 编码表 树
    else:
        # 判断输入的编码规范是否存在或符合规定
        if os.path.exists(encode_table_directory+'/'+encode_table_filename+'_decode_table.txt'):
            return encoding_with_table(save_directory, save_filename,
                                       encode_table_directory+'/'+encode_table_filename+'_decode_table.txt', string)  # 进行有编码规范的编码 输出代码
        else:
            return fail


def Encoding_3(char_and_weight_directory, save_filename, save_directory):  # 进行第三种情况编码
    f = open(char_and_weight_directory, 'r+', encoding='utf-8')  # 打开文件
    char_and_weight = f.read()  # 从文件中读入字符与权重数值
    f.close()  # 关闭文件
    char_weights = char_and_weight_to_char_weights(
        char_and_weight)  # 将输入的字符和权值组成tuple放在list中
    if char_weights == fail:
        return fail
    # 进行没有编码规范的编码 制作编码规范
    return encoding_without_table(char_weights, save_filename, save_directory, fail)


def Encoding_4(str_directory, save_filename, save_directory, encode_table_directory, encode_table_filename, encode_file):  # 进行第四种情况编码
    f = open(str_directory, 'r+', encoding='utf-8')  # 打开文件
    string = f.read()  # 从文件中读入字符串
    f.close()  # 关闭文件
    if encode_file == fail:  # 判断是否已经有编码规范
        char_weights = str_to_char_weights(
            str(string))  # 将输入的字符串组成tuple放在list中
        return encoding_without_table(char_weights, save_filename,
                                      save_directory, ok, string)  # 进行没有编码规范的编码 建立一个编码规范 输出代码 编码表 树
    else:
        # 判断输入的编码规范是否存在或符合规定
        if os.path.exists(encode_table_directory+'/'+encode_table_filename+'_decode_table.txt'):
            return encoding_with_table(save_directory, save_filename,
                                       encode_table_directory+'/'+encode_table_filename+'_decode_table.txt', string)  # 进行有编码规范的编码 输出代码
        else:
            return fail


def encoding_without_table(char_weights, save_filename, save_directory, flag, string=None):  # 没有编码规范下编码
    if flag == ok:  # 判断输入情况
        huffman_tree = HuffmanTree(char_weights, string)  # 初始化类
    else:
        huffman_tree = HuffmanTree(char_weights)  # 初始化类
    huffman_tree.create_huffman_tree()  # 建树
    directory = save_directory+'/'+save_filename  # 设置路径
    mkdir(directory)  # 创造路径
    decode_table = open(directory+'/'+save_filename +
                        '_decode_table.txt', 'w+', encoding='utf-8')  # 代开文件或者新建文件
    decode_dic = set_decode_table(huffman_tree.codetochar)  # 编写译码表
    decode_table.write(decode_dic)  # 写入文件
    decode_table.close()  # 关闭文件
    if flag == ok:  # 当有字符串输入时要输出编写后的代码
        code_file = open(directory+'/'+save_filename +
                         '_code.txt', 'w+', encoding='utf-8')  # 打开文件或者新建文件
        write_code(code_file, str(huffman_tree.code))  # 将输入的字符转换为代码并且写入文件
        code_file.close()  # 关闭文件
    huffman_tree_picture = draw_HuffmanTree(huffman_tree)  # 绘制哈夫曼树
    huffman_tree_picture.export(
        directory+'/'+save_filename+'_'+'picture')  # 导出哈夫曼树文件
    return ok


def encoding_with_table(save_directory, save_filename, encode_table_directory, string):  # 有编码规范下编码
    directory = save_directory+'/'+save_filename  # 设置路径
    mkdir(directory)  # 创造路径
    f = open(encode_table_directory, 'r+',
             encoding='utf-8')  # 打开文件
    codetochar = f.read()  # 从文件中读入编码规范S
    f.close()  # 关闭文件
    encode_table = make_dic(codetochar, encode)  # 制作字典
    print(encode_table)
    code = ''  # 初始化编码结果
    for i in range(len(string)):
        if string[i] in encode_table:  # 在字典中查找对应的代码
            code += encode_table[string[i]]  # 添加到结果中
        else:
            return fail
    code_file = open(directory+'/'+save_filename +
                     '_code.txt', 'w+', encoding='utf-8')  # 打开文件或者新建文件
    write_code(code_file, str(code))  # 将代码写入文件
    code_file.close()  # 关闭文件
    return ok


def write_code(code_file, code):  # 控制代码输出格式
    l = len(code)
    index = 0
    while l-index > 50:
        code_file.write(str(code[index:index+50]+'\n'))  # 每50个字符换行
        index += 50
    code_file.write(str(code[index:l]))  # 写入文件中


def Decoding_1(codetochar, code, save_filename, save_directory):  # 进行第一种情况译码
    decode_table = make_dic(codetochar, decode)  # 建立字典
    code = code.replace("\n", "")  # 控制代码格式将换行符删除
    flag = check_code(code)  # 判断代码是否符合规范
    if decode_table == fail or flag == fail:
        return fail
    else:
        # 返回译码结果
        return decoding(decode_table, code, save_filename, save_directory)


def Decoding_2(codetochar_directory, code_directory, save_filename, save_directory):  # 进行第二种情况译码
    if os.path.exists(codetochar_directory):  # 判断路径是否存在
        f = open(codetochar_directory, 'r+', encoding='utf-8')  # 打开文件
        codetochar = f.read()  # 从文件中读入译码表
        f.close()  # 关闭文件
    else:
        return fail
    decode_table = make_dic(codetochar, decode)  # 创造路径
    code = ''
    flag = ok
    if os.path.exists(code_directory):  # 判断路径是否存在
        f = open(code_directory, 'r+', encoding='utf-8')  # 打开文件
        code = f.read()  # 从文件中读入
        f.close()  # 关闭文件
        code = code.replace("\n", "")  # 控制代码格式将换行符删除
        flag = check_code(code)  # 判断代码是否符合规范
    if decode_table == fail or flag == fail:
        return fail
    else:
        # 返回译码结果
        return decoding(decode_table, code, save_filename, save_directory)


def Decoding_3(codetochar_directory, code, save_filename, save_directory):  # 进行第三种情况译码
    if os.path.exists(codetochar_directory):  # 判读路径是否存在
        f = open(codetochar_directory, 'r+', encoding='utf-8')  # 打开文件
        codetochar = f.read()  # 从文件中读入
        f.close()  # 关闭文件
    else:
        return fail
    decode_table = make_dic(codetochar, decode)  # 建立字典
    code = code.replace("\n", "")  # 控制代码格式将换行符删除
    flag = check_code(code)  # 判断代码是否符合规范
    if decode_table == fail and flag == fail:
        return fail
    else:
        # 返回译码结果
        return decoding(decode_table, code, save_filename, save_directory)


def decoding(decode_table, code, save_filename, save_directory):  # 译码操作
    string = decodes(decode_table, code)  # 获得译码结果
    if string == fail:
        return fail
    directory = save_directory+'/'+save_filename  # 设置路径
    mkdir(directory)  # 创造路径
    decode_ans = open(directory+'/'+save_filename +
                      '_decode_ans.txt', 'w+', encoding='utf-8')  # 打开文件或者新建文件
    decode_ans.write(string)  # 写入结果
    decode_ans.close()  # 关闭文件
    return string  # 返回译码结果


def check_code(code):  # 判断代码是否符合规范
    i = 0
    while i < len(code):
        if code[i] != '1' and code[i] != '0':  # 哈夫曼的编码结果只有0或1 换行符已被去除
            return fail
        i += 1
    return ok


def decodes(decode_table, code):  # 译码操作
    i = 0
    j = 0
    ans = ''
    while i < len(code) and j < len(code):
        j += 1
        if(code[i:j] in decode_table):  # 判断当前片段是否在字典中能被匹配到
            ans += decode_table[code[i:j]]  # 添加到结果
            i = j
        elif j == len(code):
            return fail
    return ans


def set_decode_table(decode_dic):  # 建立译码表用于编码后的文件保存
    decode_list = ''  # 初始化
    for key in decode_dic:
        decode_list += key+' '+decode_dic[key]+' '  # 将每个key和其对应的添加到结果
    return decode_list


def char_and_weight_to_char_weights(char_and_weight):  # 字符权重组成tuple建立list
    char_weights = []  # 初始化
    i = 0
    while i <= len(char_and_weight)-1:
        flag = ok
        # 空格为分隔符
        # 将判断下标是否合法放在判断具体内容是否合法前面避免下标越界的问题
        if i+1 >= len(char_and_weight) or char_and_weight[i+1] != ' ':
            return fail
        j = i+2
        while j < len(char_and_weight):
            # 权重为数值因此在这个字符后和上个字符前只会有数字和最多一个'.'
            if ((char_and_weight[j] < '0' or char_and_weight[j] > '9') and char_and_weight[j] != '.' and char_and_weight[j] != ' ') or \
                    (char_and_weight[j] == '.' and flag == fail):
                return fail
            if char_and_weight[j] == '.':
                flag = fail
            if char_and_weight[j] != ' ':  # 遇到不是空格则j+1 为空格则当前权重或频率已经读完了
                j += 1
            else:
                break
        for part in char_weights:
            if part[0] == char_and_weight[i]:  # 判读是否有重复
                return fail
        if i+2 == j:
            return fail
        temp = (char_and_weight[i], float(char_and_weight[i+2:j]))  # 组成tuple
        char_weights.append(temp)  # 添加到list
        i = j+1
    return char_weights


def str_to_char_weights(str):  # 字符权重组成tuple建立list
    char_weights = []  # 初始化list
    dic = {}  # 初始化dic
    for i in range(len(str)):
        if str[i] in dic:
            dic[str[i]] += 1  # 已存在的+1
        else:
            dic[str[i]] = 1  # 未存在为1
    for key in dic:  # 遍历所有字典
        temp = (key, dic[key])  # 将键与值组成tuple
        char_weights.append(temp)  # 添加到list
    return char_weights


def make_dic(codetochar, flag):  # 建立译码字典
    dic = {}  # 初始化字典
    i = 0
    while i < len(codetochar):
        j = i
        if codetochar[i] == ' ':
            return fail
        while j < len(codetochar):  # 空格为分隔符
            if codetochar[j] == ' ':
                break
            elif codetochar[j] == '0' or codetochar[j] == '1':
                j += 1
            else:
                return fail
        if j == len(codetochar)-1:
            return fail
        key = codetochar[i:j]
        j += 1

        if flag == decode:
            dic[key] = codetochar[j]  # 建立译码字典
        else:
            dic[codetochar[j]] = key  # 建立编码字典
        if j+1 < len(codetochar)-1 and codetochar[j+1] != ' ':
            return fail
        i = j+2
    return dic
