#散列表:双向链表法

class Node(object):
    def __init__(self, key, value, pre_node = None, next_node = None, hnext_node = None):
        self.key = key          #用于哈希的特征值
        self.value = value      #存储的数据
        self.pre = pre_node     #双向链表的.pre指针
        self.next = next_node   #双向链表的.next指针
        self.hnext = hnext_node #单向拉链的指针

class HashTable(object):

    def __init__(self):
        self.__load_factor = 0.75    #散列表默认长度
        self.__default_capacity = 8  #装载因子
        self.table = [None] * self.__default_capacity    #初始化散列表数组
        self.size = 0   #实际元素数量
        self.use = 0    #散列表索引数量

        #初始化双向链表，首尾节点作为哨兵
        self.head = Node(None, None)
        self.tail = Node(None, None)   
        self.head.next = self.tail
        self.tail.pre = self.head

    #向散列表中添加数据
    def add(self, key, value):
        index = self.hash(key)  #根据key计算出在散列表中的索引

        #如果散列表该索引位置为None,新建一个Node作为该索引拉链的头节点
        if self.table[index] == None:
            self.table[index] = Node(None, None)

        cur = self.table[index]

        #如果该索引的拉链是一个空链表，将新节点插入拉链的尾部
        if cur.hnext == None:
            new_node = Node(key, value)
            cur.hnext = new_node

            #将新节点插入双向链表的尾部
            new_node.next = self.tail
            self.tail.pre.next = new_node
            new_node.pre = self.tail.pre
            self.tail.pre = new_node
            
            self.size += 1
            self.use += 1

            #如果散列表使用的索引数量超过总量的75%，则进行扩容
            if self.use >= len(self.table) * self.__load_factor:
                self.resize()
        
        else:
            while cur.hnext != None:
                cur = cur.hnext

                #如果key相同，覆盖旧的数据
                if cur.key == key:
                    cur.value = value
                    return
            else:
                #在拉链的尾部，双向链表的尾部添加新节点
                new_node = Node(key, value)
                cur.hnext = new_node
                new_node.next = self.tail
                self.tail.pre.next = new_node
                new_node.pre = self.tail.pre
                self.tail.pre = new_node
                self.size += 1

    #哈希函数
    def hash(self, key):
        return abs(hash(key)) % len(self.table)

    #从散列表中移除key对应数据，并返回value
    def remove(self, key):
        index = self.hash(key)
        cur = self.table[index]
        if cur == None or cur.hnext == None:
            return
        else:
            while cur.hnext != None or cur.hnext.hnext != None: #cur是待删除节点再拉链中的前置节点
                if cur.hnext.key == key:
                    tmp = cur.hnext.value   #临时存储待删除节点的value

                    #先从双向链表中删除，再从拉链中删除
                    cur.hnext.pre.next = cur.hnext.next
                    cur.hnext.next.pre = cur.hnext.pre
                    cur.hnext = cur.hnext.hnext
                    self.size -= 1

                    if self.table[index].hnext == None:
                        self.use -= 1
                    return tmp
                else:
                    cur = cur.hnext

    #动态扩容
    def resize(self):
        old_table = self.table
        self.table = [None] * (len(self.table) << 1)    #申请一个原来两倍大小的数组
        self.use = 0

        #将旧散列表中的数据一次性迁移到新散列表,只改变拉链的索引，双向链表中节点的相对位置保持不变
        node = self.head
        while node.next != self.tail:
            node = node.next
            node.hnext = None   #注意要初始化拉链的指针，昨天忘记这个，致使单向拉链中出现了环

            index = self.hash(node.key)
            if self.table[index] == None:
                self.table[index] = Node(None, None)

            cur = self.table[index]

            #如果该索引的拉链是一个空链表，将节点node插入拉链的尾部
            if cur.hnext == None:
                cur.hnext = node
                self.use += 1
            else:
                while cur.hnext != None:
                    cur = cur.hnext

                    #如果key相同，覆盖旧的数据
                    if cur.key == node.key:
                        cur.value = node.value
                else:
                    #在拉链的尾部添加节点node
                    cur.hnext = node
                            
    #查找key所对应value
    def find(self, key):
        index = self.hash(key)
        cur = self.table[index]
        if cur == None or cur.hnext == None:
            return None
        else:
            while cur.hnext != None:
                cur = cur.hnext
                if cur.key == key:
                    return cur.value
            else:
                return None

    #打印双向链表
    def __repr__(self):
        cur = self.head
        vals = []
        while cur.next != self.tail:
            cur = cur.next
            vals.append(str(cur.value))
        return '-->'.join(vals)

    #用于for...in...语句调用
    def __iter__(self):
        cur = self.head
        while cur.next != self.tail:
            cur = cur.next
            yield cur

    #打印每一个拉链
    def print_all(self):
        for index in range(len(self.table)):
            cur = self.table[index]
            print('index:', index,end='|')
            try:
                while cur.hnext != None:
                    cur = cur.hnext
                    if cur == None:
                        continue
                    print(cur.value,end='-->')
                print('\n')
            except:
                print(None)

if __name__ == '__main__':
    h = HashTable()
    h.add(0, 100)
    h.add(3, 103)
    h.add(7, 107)
    h.add(5, 105)
    h.add(14, 114)
    h.add(15, 115)
    print(h)
    '''
    100-->103-->107-->105-->114-->115
    '''

    h.add(0, 77)
    print(h)
    '''
    77-->103-->107-->105-->114-->115
    '''

    print('find',h.find(7))
    print('remove',h.remove(5))
    h.print_all()
    '''
    find 107
    remove 105
    index: 0|77-->
    index: 1|None
    index: 2|None
    index: 3|103-->
    index: 4|None
    index: 5|
    index: 6|114-->
    index: 7|107-->115-->
    '''

    h.add(13, 113)
    h.add(37, 137)
    h.add(77, 177)
    h.add(50, 150)
    h.add(23, 123)
    h.add(21, 121)
    h.print_all()
    '''
    index: 0|77-->
    index: 1|None
    index: 2|150-->
    index: 3|103-->
    index: 4|None
    index: 5|137-->121-->
    index: 6|None
    index: 7|107-->123-->
    index: 8|None
    index: 9|None
    index: 10|None
    index: 11|None
    index: 12|None
    index: 13|113-->177-->
    index: 14|114-->
    index: 15|115-->
    '''
© 2020 GitHub, Inc.
