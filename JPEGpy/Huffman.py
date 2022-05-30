class node(object):
    def __init__(self,value = None,left = None,right = None,father = None):
        self.value = value
        self.left = left
        self.right = right
        self.father = father

    def build_father(left,right):
        n = node(value = left.value + right.value,left = left,right = right)
        left.father = right.father = n
        return n

    def encode(n):
        if n.father == None:
            return b''
        if n.father.left == n:
            return node.encode(n.father) + b'0'
        else:
            return node.encode(n.father) + b'1'

class tree(object):

    def __init__(self):
        #数据初始化
        self.node_dict = {}
        self.count_dict = {}
        self.ec_dict = {}
        self.nodes = []
        self.inverse_dict = {}

    #哈夫曼树构建
    def build_tree(self, l):
        if len(l) == 1:
            return l
        sorts = sorted(l,key = lambda x:x.value,reverse = False)
        n = node.build_father(sorts[0],sorts[1])
        sorts.pop(0)
        sorts.pop(0)
        sorts.append(n)
        return self.build_tree(sorts)

    def encode(self, echo):
        for x in self.node_dict.keys():
            self.ec_dict[x] = node.encode(self.node_dict[x])
            if echo == True:
                print(x)
                print(self.ec_dict[x])

    def encodefile(self, inputfile):

        print("Starting encode...")
        f = open(inputfile,"rb")
        bytes_width = 1
        i = 0

        f.seek(0,2)
        count = f.tell() / bytes_width
        print(count)
        nodes = []
        buff = [b''] * int(count)
        f.seek(0)

        #计算字符频率,并将单个字符构建成单一节点
        while i < count:
            buff[i] = f.read(bytes_width)
            if self.count_dict.get(buff[i],     -1) == -1:
                self.count_dict[buff[i]] = 0
            self.count_dict[buff[i]] = self.count_dict[buff[i]] + 1
            i = i + 1
        print("Read OK")
        print(self.count_dict) #输出权值字典,可注释掉
        for x in self.count_dict.keys():
            self.node_dict[x] = node(self.count_dict[x])
            nodes.append(self.node_dict[x])

        f.close()
        tree = self.build_tree(nodes)
        self.encode(False)
        print("Encode OK")

        head = sorted(self.count_dict.items(),key = lambda x:x[1] ,reverse = True)	#对所有根节点进行排序
        bit_width = 1
        print("head:",head[0][1])
        if head[0][1] > 255:
            bit_width = 2
            if head[0][1] > 65535:
                bit_width = 3
                if head[0][1] > 16777215:
                    bit_width = 4
        print("bit_width:",bit_width)
        i = 0
        raw = 0b1
        last = 0
        name = inputfile.split('.')
        o = open(name[0]+"_.txt" , 'wb')
        name = inputfile.split('/')
        o.write((name[len(name)-1] + '\n').encode(encoding="utf-8"))#写出原文件名
        o.write(int.to_bytes(len(self.ec_dict) ,2 ,byteorder = 'big'))#写出结点数量
        o.write(int.to_bytes(bit_width ,1 ,byteorder = 'big'))#写出编码表字节宽度
        for x in self.ec_dict.keys():#编码文件头
            o.write(x)
            o.write(int.to_bytes(self.count_dict[x] ,bit_width ,byteorder = 'big'))

        print('head OK')
        while i < count:
            for x in self.ec_dict[buff[i]]:
                raw = raw << 1
                if x == 49:
                    raw = raw | 1
                if raw.bit_length() == 9:
                    raw = raw & (~(1 << 8))
                    o.write(int.to_bytes(raw ,1 , byteorder = 'big'))
                    o.flush()
                    raw = 0b1
                    tem = int(i  /len(buff) * 100)
                    if tem > last:
                        # print("encode:", tem ,'%')
                        last = tem
            i = i + 1

        if raw.bit_length() > 1:
            raw = raw << (8 - (raw.bit_length() - 1))
            raw = raw & (~(1 << raw.bit_length() - 1))
            o.write(int.to_bytes(raw ,1 , byteorder = 'big'))
        o.close()
        print("File encode successful.")

    def decodefile(self, inputfile):

        print("Starting decode...")
        count = 0
        raw = 0
        last = 0
        f = open(inputfile ,'rb')
        f.seek(0,2)
        eof = f.tell()
        f.seek(0)
        name = inputfile.split('/')
        outputfile = inputfile.replace(name[len(name)-1], f.readline().decode(encoding="utf-8"))
        o = open(outputfile.replace('\n','') ,'wb')
        count = int.from_bytes(f.read(2), byteorder = 'big')
        bit_width = int.from_bytes(f.read(1), byteorder = 'big')
        i = 0
        de_dict = {}
        while i < count:
            key = f.read(1)
            value = int.from_bytes(f.read(bit_width), byteorder = 'big')
            de_dict[key] = value
            i = i + 1
        for x in de_dict.keys():
            self.node_dict[x] = node(de_dict[x])
            self.nodes.append(self.node_dict[x])
        tree = self.build_tree(self.nodes)#重建哈夫曼树
        self.encode(False)#建立编码表
        for x in self.ec_dict.keys():#反向字典构建
            self.inverse_dict[self.ec_dict[x]] = x
        i = f.tell()
        data = b''
        while i < eof:#开始解压数据
            raw = int.from_bytes(f.read(1), byteorder = 'big')
            # print("raw:",raw)
            i = i + 1
            j = 8
            while j > 0:
                if (raw >> (j - 1)) & 1 == 1:
                    data = data + b'1'
                    raw = raw & (~(1 << (j - 1)))
                else:
                    data = data + b'0'
                    raw = raw & (~(1 << (j - 1)))
                if self.inverse_dict.get(data, 0) != 0:
                    o.write(self.inverse_dict[data])
                    o.flush()
                    #print("decode",data,":",inverse_dict[data])
                    data = b''
                j = j - 1
            tem = int(i / eof * 100)
            if tem > last:
                # print("decode:", tem,'%')#输出解压进度
                last = tem
            raw = 0

        f.close()
        o.close()
        print("File decode successful.")

if __name__ == '__main__':

    temptree = tree()
    temptree.encodefile("lenna1.txt")
    temptree.encodefile("lenna5.txt")
    temptree.encodefile("lenna10.txt")
    temptree.encodefile("lenna20.txt")