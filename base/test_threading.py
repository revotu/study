import threading, time


def loop():
    print 'thread %s is running...' % threading.current_thread().name
    for i in range(5):
        print 'thread %s >>> %s' % (threading.current_thread().name, i)
        time.sleep(1)
    print 'thread %s ended.' % threading.current_thread().name


print 'thread %s is running...' % threading.current_thread().name
t = threading.Thread(target=loop, name='LoopThread')
t.start()
t.join()
print 'thread %s ended.' % threading.current_thread().name