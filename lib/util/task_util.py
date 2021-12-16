import threading
import time


class WorkerTask:
    def __init__(self, task, callback = None, **kargs):
        self.task = task
        self.kargs = kargs
        self.done = False
        self.callback = callback

    def exec(self):
        self.task(**self.kargs)
        self.done = True
        if (self.callback != None): self.callback(self)

class QueueWorker:
    def __init__(self, limit = 4, name='<task>', dequeue_on_done = False, all_done_callback = None, task_done_callback = None, meta = {}):
        self.current = []
        self.queue = []
        self.limit = limit
        self.started = False
        self.done = False
        self.total_task = 0
        self.dequeue_on_done = dequeue_on_done
        self.all_done_callback = all_done_callback
        self.task_done_callback = task_done_callback
        self.name = name
        self.meta = meta

    def taskdone(self, task):
        self.current.remove(task)
        self.dequeue()
        if (self.task_done_callback != None): self.task_done_callback(task)
        if (len(self.queue) == 0 and len(self.current) == 0):
            self.done = True
            if (self.all_done_callback != None): self.all_done_callback(self)

    def dequeue(self):
        if len(self.queue) > 0:
            task = self.queue[0]
            self.current.append(task)
            self.queue.remove(task)
            t = threading.Thread(target=task.exec)
            t.daemon = True
            t.start()
            return task
        return None

    def enqueue(self, task):
        if (self.started):
            raise Exception('Queue already started')
        if (self.dequeue_on_done): task.callback = self.taskdone
        self.queue.append(task)

    def get_total_task(self):
        if (self.started):
            return self.total_task
        self.total_task = len(self.queue)
        return self.total_task

    def start(self):
        if (self.started or len(self.queue) == 0):
            return
        self.started = True
        self.total_task = len(self.queue)
        while (len(self.current) != self.limit and len(self.queue) > 0):
            self.dequeue()

    def wait(self):
        while (not self.done):
            time.sleep(0.1)

class TaskQueue:
    def __init__(self, on_task_update = None):
        self.queue = []
        self.on_task_update = on_task_update

    def enqueue(self, o:QueueWorker):
        print(f'[QueueWorker] {o.name}: Enqueued')
        self.queue.append(o)
        if (len(self.queue) == 1):
            print(f'[QueueWorker] {self.queue[0].name}: Started')
            # len == 1 because this one only wanted to startup the first one in queue if emty (otherwise it would call start on the first one again and fuck thing up) and the next one will start automatically
            self.queue[0].all_done_callback = self.dequeue
            self.queue[0].task_done_callback = self.task_done
            self.queue[0].start()

    def task_done(self, task):
        if (self.on_task_update != None): self.on_task_update()

    def dequeue(self, worker):
        if (len(self.queue) <= 0): return None
        res = self.queue[0]
        print(f'[QueueWorker] {res.name}: Done')
        self.queue.remove(res)
        if (len(self.queue) > 0):
            self.queue[0].all_done_callback = self.dequeue
            self.queue[0].task_done_callback = self.task_done
            self.queue[0].start()
            print(f'[QueueWorker] {self.queue[0].name}: Started')
        else:
            print(f'[QueueWorker]: All done')
        return res

task_queue = TaskQueue()

def get_queue_stat() -> dict:
    res = {}
    res['count'] = len(task_queue.queue)
    res['tasks'] = []
    for q in task_queue.queue:
        dt = {}
        mid = q.meta['id']
        dt['id'] = f'process-{mid}'
        dt['category'] = q.meta['category']
        dt['name'] = q.name
        dt['count'] = q.get_total_task()
        dt['progress'] = dt['count'] - len(q.queue)
        res['tasks'].append(dt)

    return res

#q_worker = QueueWorker(name=stream.name, dequeue_on_done = True, meta={'id':id})
#for vid in ls:
    #if (vid.type in [1,2]):
        #q_worker.enqueue(WorkerTask(process_video, None, vid=vid))
#worker_queue.enqueue(q_worker)
