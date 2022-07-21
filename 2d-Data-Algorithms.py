import sys
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtGui import QPainter, QPen, QPainter, QColor
from PyQt6.QtCore import Qt, QRect,QTimer,QEvent
from PyQt6.QtWidgets import QApplication, QPushButton, QWidget, QVBoxLayout, QVBoxLayout, QComboBox
import random
import time
class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.values = random.sample(range(10, 100),20)
        self.n = 5
        self.m = 5

        #self.pathList=[[0] * self.m] * self.n
        self.pathList=[ [  0, 0,  0, -1, 0 ],
                        [ -1, 0,  0, -1, -1],
                        [  0, 0,  0, -1, 0 ],
                        [ -1, 0,  0,  0, 0 ],
                        [  0, 0, -1,  0, 0 ] ]
        self.visited = [[False]*self.m for _ in range(self.n)]
        self.paths=[]
        #self.paths=random.sample(range(0, self.n*self.m), 2)
        #print(self.paths)
        self.source=[0,0]
        self.destination=(self.n-1,self.m-1)
        
        self.h = 50
        self.w = len(self.values)*self.h
        self.checked=[]
        self.completed=[]
        self.timer = QTimer(interval=1, timeout=self.next_step)

        self.cb = QComboBox()
        self.cb.addItems(["Bubble Sort", "Insertion Sort", "Quick Sort","Shell Sort","Selection Sort","Radix Sort","Pathfind"])
        self.cb.activated.connect(self.selectionchange)
		
        layout = QVBoxLayout()
        layout.addWidget(self.cb)
        self.setLayout(layout)
        self.setGeometry(0,0, self.w, self.w)
        self.setWindowTitle('Drawing text')
        self.show()
    def selectionchange(self,i):
        self.checked=[]
        self.completed=[]
        self.values = random.sample(range(10, 100),20)
        print ("Items in the list are :")
            
        for count in range(self.cb.count()):
            print (self.cb.itemText(count))
        print ("Current index",i,"selection changed ",self.cb.currentText())

        if i==0:
            print('Button 1')        
            self.cb.setDisabled(True)
            self.algorithm=self.bubbleSort(self.values,len(self.values))
            self.timer.start()
            self.cb.setDisabled(False)
            print('Done')
        elif i==1:
            print('Button 2')
            self.cb.setDisabled(True)
            self.algorithm=self.insertionSort(self.values,len(self.values))
            self.timer.start()
            self.cb.setDisabled(False)
            print('Done')
        elif i==2:
            print('Button 3')
            self.cb.setDisabled(True)
            self.algorithm=self.quickSort(self.values,0,len(self.values)-1)
            self.timer.start()
            self.cb.setDisabled(False)
            print('Done')
        elif i==3:
            print('Button 3')
            self.cb.setDisabled(True)
            self.algorithm=self.shellSort(self.values,len(self.values))
            self.timer.start()
            self.cb.setDisabled(False)
            print('Done')
        elif i==4:
            print('Button 4')
            self.cb.setDisabled(True)
            self.algorithm=self.selectionSort(self.values,len(self.values))
            self.timer.start()
            self.cb.setDisabled(False)
            print('Done')
        elif i==5:
            print('Button 5')
            self.cb.setDisabled(True)
            self.algorithm=self.radixSort(self.values,len(self.values))
            self.timer.start()
            self.cb.setDisabled(False)
            print('Done')
        elif i==6:
            print('Button 6')
            self.cb.setDisabled(True)
            self.algorithm=self.pathFind(self.source,self.paths)
            self.timer.start()
            self.cb.setDisabled(False)
            print('Done')

        else:
            print('exit')

    def next_step(self):
        try:
            next(self.algorithm)
            self.update()
            time.sleep(1)
        except StopIteration:
            self.checked=[]
            self.completed=[]
            self.update()
            self.timer.stop()

    def paintEvent(self,event):
        qp = QPainter()
        qp.begin(self)
        i=0
        for item in self.values:
            rect = QRect(i,0,self.h,self.h)
            if (i/self.h in self.completed):
                qp.setBrush(QColor(0,100, 0))
            elif(i/self.h in self.checked):
                qp.setBrush(QColor(255, 165, 0))
            else:
                qp.setBrush(QColor(50, 34, 3))
            qp.drawRect(rect)
            qp.drawText(rect, Qt.AlignmentFlag.AlignCenter, str(item))
            i+=self.h
        #print(self.paths)
        for y in range(self.n):
            for x in range(self.m):
                rect = QRect(x*10,50+(y*10),10,10)
                if ([y,x]==self.source or (y,x)==self.destination):
                    qp.setBrush(QColor(255, 0, 0))
                elif((y,x)in self.paths):
                    qp.setBrush(QColor(255, 165, 0))
                else:
                    qp.setBrush(QColor(50, 34, 3))
                qp.drawRect(rect)
                #qp.drawText(rect, Qt.AlignmentFlag.AlignCenter, str(self.pathList[y][x]))

        qp.end()  
        
    def bubbleSort(self,arr,n):
        for i in range(n-1):
            self.checked=[]
            for j in range(0, n-i-1):
                self.checked.append(j)
                if arr[j] > arr[j + 1]:
                    arr[j],  arr[j + 1] =  arr[j + 1], arr[j]
                    self.completed=[j,j+1]
                    yield

    def insertionSort(self,arr,n):
        for i in range(1, n):
            key_item = arr[i]
            j = i - 1
            self.checked=[i]
            while j >= 0 and arr[j] > key_item:
                
                arr[j + 1] = arr[j]  
                self.checked.append(j)
                j -= 1
            arr[j + 1] = key_item
            yield
            self.completed=[j+1]
            yield

    def partition(self,arr, l, h):
        self.checked=[]
        i = ( l - 1 )
        x = arr[h]
        
        for j in range(l, h):
            if arr[j] <= x:
                i = i + 1
                arr[i], arr[j] = arr[j], arr[i]
                self.checked.append(i)

        arr[i + 1], arr[h] = arr[h], arr[i + 1]
        self.completed=[i+1]
        return (i + 1)
  
    def quickSort(self,arr, l, h):

        size = h - l + 1
        stack = [0] * (size)
        top = -1

        top = top + 1
        stack[top] = l     
        top = top + 1
        stack[top] = h
        
        while top >= 0:
            h = stack[top]
            top = top - 1
            l = stack[top]
            top = top - 1
            p = self.partition( arr, l, h )
            
            if p-1 > l:
                top = top + 1
                stack[top] = l
                yield
                top = top + 1
                stack[top] = p - 1
                yield
                
            if p + 1 < h:
                top = top + 1
                stack[top] = p + 1
                yield
                top = top + 1
                stack[top] = h
                yield
                
        yield
    def selectionSort(self,arr,n):
        for i in range(n):
            min_idx = i
            self.checked=[i]
            for j in range(i+1, n):
                if arr[min_idx] >arr[j]:
                    min_idx = j
                self.checked.append(j)
            self.completed=[i,min_idx]
            yield    
            arr[i],arr[min_idx] = arr[min_idx],arr[i]
            yield
            
            
    def shellSort(self,arr, n):
        h = n // 2
        while h > 0:
            
            for i in range(h, n):
                t = arr[i]
                j = i
                
                while j >= h and arr[j - h] > t:
                    arr[j] = arr[j - h]
                    self.checked.append(j)
                    j -= h
                yield
                arr[j] = t
                self.checked.append(j)
            yield
            
            h = h // 2 
            
    def countingSort(self,arr,n, exp1):
        output = [0] * (n)
        count = [0] * (10)
        for i in range(0, n):
            index = arr[i] // exp1
            count[index % 10] += 1
            
        for i in range(1, 10):
            count[i] += count[i - 1]
    
        i = n - 1
        while i >= 0:
            index = arr[i] // exp1
            output[count[index % 10] - 1] = arr[i]
            count[index % 10] -= 1
            i -= 1
        i = 0
        for i in range(0, len(arr)):
            arr[i] = output[i]
            self.checked.append(i)
            yield
      
    def radixSort(self,arr,n):
        max1 = max(arr)
        exp = 1
        while max1 / exp > 1:
            
            yield from self.countingSort(arr,n, exp)
            self.checked=[]
            exp *= 10
            print(arr)


    def pathFind(self,source,path):
        y,x = source[0],source[1]
        #print(y,x)
        self.visited[y][x]=True
        if source==self.destination:
            print('Done')
            yield
            
        dir = [[0, 1], [0, -1], [1, 0], [-1, 0]]
        
        for i in range(0,4):
            a = y + dir[i][0]
            b = x + dir[i][1]
            #print(a,b)
            
            if a>=0 and b>=0 and a<5 and b<5 and not self.visited[a][b] and self.pathList[a][b]!=-1: 
                #print(visited[a][b])
                path.append((a,b))
                #print(path)
                yield from self.pathFind((a,b),path)
                path.pop()
         
        self.visited[y][x]=False
        print('End')

def main():
    app = QApplication(sys.argv)
    ex = Example()
    
    with open("style.css","r") as file:
        app.setStyleSheet(file.read())
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
