import threading
import time
import traceback


class WorkerTask:
    def __init__(self, task, callback = None, error_callback = None, **kargs):
        self.task = task
        self.kargs = kargs
        self.done = False
        self.callback = callback
        self.error_callback = error_callback

    def exec(self):
        try:
            self.task(**self.kargs)
            if (self.callback != None): self.callback(self)
        except Exception as e:
            if (self.callback != None): self.error_callback(self, e , traceback.format_exc())
            else: 
                print('Unhadled error: ')
                print(traceback.format_exc())
        self.done = True

class QueueWorker:
    def __init__(self, limit = 4, name='<task>', dequeue_on_done = False, all_done_callback = None, task_done_callback = None, error_callback = None, meta = {}):
        self.current = []
        self.queue = []
        self.limit = limit
        self.started = False
        self.done = False
        self.total_task = 0
        self.dequeue_on_done = dequeue_on_done
        self.all_done_callback = all_done_callback
        self.task_done_callback = task_done_callback
        self.error_callback = error_callback
        self.name = name
        self.meta = meta

    def taskdone(self, task):
        self.current.remove(task)
        self.dequeue()
        if (self.task_done_callback != None): self.task_done_callback(self, task)
        if (len(self.queue) == 0 and len(self.current) == 0):
            self.done = True
            if (self.all_done_callback != None): self.all_done_callback(self)

    def taskerror(self, task, e, trc):
        self.queue.clear()
        self.current.clear()
        self.done = True
        if (self.error_callback != None): self.error_callback(self, e, trc)
        else:
            print(f'Unhandled error in task {self.name!r}:')
            print(trc)

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
        task.error_callback = self.taskerror
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
    def __init__(self, on_task_update = None, on_task_done = None, on_task_error = None):
        self.queue = []
        self.on_task_update = on_task_update
        self.on_task_done = on_task_done
        self.on_task_error = on_task_error

    def enqueue(self, worker:QueueWorker):
        print(f'[QueueWorker] {worker.name}: Enqueued')
        self.queue.append(worker)
        if (len(self.queue) == 1):
            print(f'[QueueWorker] {self.queue[0].name}: Started')
            # len == 1 because this one only wanted to startup the first one in queue if emty (otherwise it would call start on the first one again and fuck thing up) and the next one will start automatically
            self.queue[0].all_done_callback = self.dequeue
            self.queue[0].task_done_callback = self.task_done
            self.queue[0].error_callback = self.task_error
            self.queue[0].start()
            if (self.on_task_update != None): self.on_task_update(worker)

    def task_done(self, worker, task):
        if (self.on_task_update != None): self.on_task_update(worker)

    def task_error(self, worker, e, trace):
        if (len(self.queue) > 0):
            res = self.queue[0]
            self.queue.remove(res)
        print(f'[QueueWorker] {worker.name}: Error: {e}')
        print(trace)
        if (len(self.queue) > 0):
            self.queue[0].all_done_callback = self.dequeue
            self.queue[0].task_done_callback = self.task_done
            self.queue[0].error_callback = self.task_error
            self.queue[0].start()
            print(f'[QueueWorker] {self.queue[0].name}: Started')
        else:
            print(f'[QueueWorker]: All done')
            if (self.on_task_update != None): self.on_task_update(worker)
        if (self.on_task_error != None): self.on_task_error(worker, e, trace)


    def dequeue(self, worker = None):
        if (len(self.queue) <= 0): return None
        res = self.queue[0]
        self.queue.remove(res)
        print(f'[QueueWorker] {res.name}: Done')
        if (len(self.queue) > 0):
            self.queue[0].all_done_callback = self.dequeue
            self.queue[0].task_done_callback = self.task_done
            self.queue[0].start()
            print(f'[QueueWorker] {self.queue[0].name}: Started')
        else:
            print(f'[QueueWorker]: All done')
            if (self.on_task_update != None): self.on_task_update(worker)
        if (self.on_task_done != None): self.on_task_done(worker)
        return res

task_queue = TaskQueue()

def get_queue_stat() -> dict:
    res = {}
    res['count'] = len(task_queue.queue)
    res['tasks'] = []
    for q in task_queue.queue:
        dt = {}
        dt['id'] = f'{q.meta["category"]}-{q.meta["id"]}'
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
