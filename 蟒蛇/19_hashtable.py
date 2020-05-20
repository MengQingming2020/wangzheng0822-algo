#散列表：数组，线性探测法

class Slot(object):
    def __init__(self, key, value, removed = None):
        self.key = key          #特征值
        self.value = value      #存储的数据
        self.removed = removed  #标记是否为已删除节点

class HashTable(object):
    def __init__(self):
        self.__load_factor = 0.75       #装载因子
        self.__default_capacity = 8     #散列表默认长度
        self.table = [None] * self.__default_capacity   #初始化散列表
        self.use = 0       #散列表已使用的索引数量

    def add(self, key, value):
        index = self.hash(key)
        #如果该索引未使用，直接插入Slot
        if self.table[index] == None:
            self.table[index] = Slot(key, value)
            self.use += 1
            if self.use >= len(self.table) * self.__load_factor:
                self.resize()

        #如果key相同，更新value
        elif self.table[index].key == key:
            self.table[index].value = value
            self.removed = None

        #如果位置被占用，向后线性探测空闲位置
        else:
            for i in range(index+1,len(self.table)):
                if self.table[i] == None:
                    self.table[i] = Slot(key, value)
                    self.use += 1
                    if self.use >= len(self.table) * self.__load_factor:
                        self.resize()
                    return True

            #若尾部没有空闲位置，则从头开始找
            for j in range(index):
                if self.table[j] == None:
                    self.table[j] = Slot(key, value)
                    self.use += 1
                    if self.use >= len(self.table) * self.__load_factor:
                        self.resize()
                    return True

    #并不真的移除Slot,而是将Slot.removed属性标记为True
    def remove(self, key):
        index = self.hash(key)

        #如果对应索引为空，返回True
        if self.table[index] == None:
            return True
        
        #如果对应的索引存储的是要移除的节点，将Slot.removed属性标记为True，并返回value
        elif self.table[index].key == key:
            self.table[index].removed = True
            return self.table[index].value

        #如果位置被占用，继续线性探测
        else:
            for i in range(index+1, len(self.table)):
                if self.table[i] == None:
                    return True
                if self.table[i].key == key:
                    self.table[i].removed = True
                    return self.table[i].value
            for j in range(index):
                if self.table[j] == None:
                    return True
                if self.table[j].key == key:
                    self.table[j].removed = True
                    return self.table[j].value

    #查找操作
    def find(self, key):
        index = self.hash(key)
        if self.table[index] == None:
            return None
        elif self.table[index].key == key:
            if self.table[index].removed == None:
                return self.table[index].value
            else:
                return None
        else:
            for i in range(index+1, len(self.table)):
                if self.table[i] == None:
                    return None
                if self.table[i].key == key:
                    if self.table[i].removed == None:
                        return self.table[i].value
                    else:
                        return None
            for j in range(index):
                if self.table[j] == None:
                    return None
                if self.table[j].key == key:
                    if self.table[j].removed == None:
                        return self.table[j].value
                    else:
                        return None

    #哈希函数
    def hash(self, key):
        return abs(hash(key)) % len(self.table)

    #动态扩容
    def resize(self):
        old_table = self.table
        self.table = [None] * (len(old_table) << 1)
        self.use = 0
        for slot in old_table:
            if slot == None:
                continue
            self.add(slot.key, slot.value)

    #打印散列表
    def print_all(self):
        for slot in self.table:
            if slot == None or slot.removed == True:
                print('None',end=' / ')
            else:
                print(slot.key, slot.value, end=' / ')
        

if __name__ == '__main__':
    h = HashTable()
    h.add(0, 100)
    h.add(7, 107)
    h.add(5, 105)
    h.print_all()
    print('\n')
    ''' 0 100 / None / None / None / None / 5 105 / None / 7 107 /'''

    h.add(0, 77)
    h.print_all()
    print('\n')
    ''' 0 77 / None / None / None / None / 5 105 / None / 7 107 / '''

    print('find',h.find(7))
    print('remove',h.remove(5))
    h.print_all()
    print('\n')
    '''
    find 107
    remove 105
    0 77 / None / None / None / None / None / None / 7 107 / 
    '''
    
    h.add(13, 113)
    h.add(37, 137)
    h.add(77, 177)
    h.print_all()
    '''0 77 / None / None / None / None / 37 137 / 5 105 / 7 107 / None / None / None / None / None / 77 177 / 13 113 / None /'''
