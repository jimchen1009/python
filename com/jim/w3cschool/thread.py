#!/usr/bin/python3
import queue
import threading
import time

exitFlag = 0
threadLock = threading.Lock()


class DemoThread(threading.Thread):
    def __init__(self, thread_id, name, que):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.que = que

    def run(self):
        print("开始线程:" + self.name)
        process_data(self.name, 5, self.que)
        print("退出线程：" + self.name)


def process_data(name, delay, que):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            data = que.get()
            print("%s processing %s" % (name, data))
            queueLock.release()
        else:
            queueLock.release()
        time.sleep(1)


threadList = ["No-1", "No-2", "No-3"]
nameList = ["One", "Two", "Three", "Four", "Five"]
queueLock = threading.Lock()
workQueue = queue.Queue(10)
threads = []
threadID = 1

# 创建新线程
for tName in threadList:
    thread = DemoThread(threadID, tName, workQueue)
    thread.start()
    threads.append(thread)
    threadID += 1


# 填充队列
queueLock.acquire()
for word in nameList:
    workQueue.put(word)
queueLock.release()


# 等待队列清空
while not workQueue.empty():
    pass

# 通知线程是时候退出
exitFlag = 1

for thread in threads:
    thread.join()

print("退出主线程")
