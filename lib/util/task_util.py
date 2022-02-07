import time
import traceback
import asyncio
import threading
import lib.util.util as util

class TaskItem:
    def __init__(self, fn, *args, **kwargs):
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.on_done = util.CallBackList()
        self.on_error = util.CallBackList()
    
    def exec(self):
        result = None
        try:
            result = self.fn(*self.args, **self.kwargs)
        except Exception as e:
            self.on_error.fire(e, traceback.format_exc())
        finally:
            self.on_done.fire(self, result)

    def __repr__(self):
        return f'<TaskItem>({self.fn.__name__})'

class Task:
    def __init__(self, name):
        self.name = name
        self.item_count = 0
        self.items = util.Queue()

    def add(self, item):
        self.item_count += 1
        self.items.put(item)

    def get(self):
        return self.items.get()

    def add_on_item_done(self, fn):
        self.items.items[0].on_done.append(fn)

    @classmethod
    def from_single_item(cls, name, fn, *args, **kwargs):
        item = TaskItem(fn, *args, **kwargs)
        task = cls(name)
        task.add(item)
        return task

class TaskWorker:
    def __init__(self, name, limit = 4, meta = {}, error_action = 0):
        """error_action: 0:continue 1:skip task 2:skip worker"""
        self.name = name
        self.meta = meta
        self.on_task_item_done = util.CallBackList()
        self.on_task_done = util.CallBackList()
        self.on_task_start = util.CallBackList()
        self.on_worker_done = util.CallBackList()
        self.on_task_item_error = util.CallBackList()
        self.limit = limit
        self.task_count = 0
        self.tasks = util.Queue()
        self.current_items = []
        self.current_task:Task = None
        self.current_atasks = []
        self.error_action = error_action

    def get_processed_item_count(self):
        if (self.current_task != None):
            return self.current_task.item_count - (len(self.current_items) + len(self.current_task.items))

    def get_done_task_count(self):
        """Note: Current processing task counted as done"""
        return self.task_count - len(self.tasks)

    def add(self, task):
        self.task_count += 1
        self.tasks.put(task)

    def run_item(self, item):
        self.current_items.append(item)
        item.on_done.append(self.task_item_done)
        item.on_error.append(self.task_item_error)
        #asyncio.create_task(item.exec())
        threading.Thread(target=item.exec, daemon=True).start()

    def start_task(self):
        self.current_task = self.tasks.get()
        # print('task', self.current_task.name, 'started', len(self.current_task.items))
        while (len(self.current_items) < self.limit and len(self.current_task.items) > 0):
            self.run_item(self.current_task.get())
        self.on_task_start.fire(self.current_task)
        # print(self.current_items)

    def task_item_error(self, exception, traceback_str):
        self.on_task_item_error.fire(self, exception, traceback_str)
        if (self.error_action == 1):
            # print('Task canceled')
            # self.current_items = []
            self.current_task.items.clear()
        elif (self.error_action == 2):
            # self.current_items = []
            self.current_task.items.clear()
            self.tasks.clear()

    def task_item_done(self, task_item, result):
        self.current_items.remove(task_item)
        self.on_task_item_done.fire(task_item, result)
        # print('item done')
        if (len(self.current_items) == 0):
            # print('task done')
            self.on_task_done.fire(self.current_task)
            # print('next task')
            if (len(self.tasks) > 0): self.start_task()
            else: self.on_worker_done.fire(self)
        if (len(self.current_task.items) > 0):
            self.run_item(self.current_task.get())

class TaskWorkerQueue:
    def __init__(self, auto_start = True):
        self.workers = util.Queue()
        self.current_worker = None
        self.auto_start = auto_start
        self.on_task_update = util.CallBackList()
        self.on_worker_done = util.CallBackList()
        self.on_worker_error = util.CallBackList()

    def get_worker_list(self):
        if (self.current_worker != None):
            return [self.current_worker] + self.workers
        else:
            return self.workers
    
    def get_worker_count(self):
        return len(self.workers) + (1 if self.current_worker != None else 0)

    def add(self, worker):
        self.workers.put(worker)
        if (self.auto_start and self.current_worker == None):
            self.start_worker()

    def start_worker(self):
        worker:TaskWorker = self.workers.get()
        worker.on_worker_done.append(self.worker_done)
        worker.on_task_item_done.append(self.task_item_done)
        worker.on_task_item_error.append(self.worker_error)
        self.current_worker = worker
        worker.start_task()

    def task_item_done(self, item, result = None):
        self.on_task_update.fire(self.current_worker, item, result)

    def worker_done(self, worker):
        if (len(self.workers) > 0):
            self.start_worker()
        else:
            self.current_worker = None
        self.on_worker_done.fire(worker)

    def worker_error(self, worker, exception, traceback_str):
        self.on_worker_error.fire(worker, exception, traceback_str)

worker_queue = TaskWorkerQueue()

def get_queue_stat() -> dict:
    res = {}
    res['count'] = worker_queue.get_worker_count()
    res['tasks'] = []
    ls = worker_queue.get_worker_list()
    for q in ls:
        dt = {}
        dt['id'] = f'{q.meta["category"].lower()}-{q.meta["id"]}'
        if ('operation' in q.meta): dt['id'] += f'-{q.meta["operation"]}'
        dt['category'] = q.meta['category']
        if (q.current_task != None):
            dt['name'] = q.current_task.name
            dt['count'] = q.current_task.item_count
            dt['progress_all'] = q.get_done_task_count()
            dt['progress'] = q.get_processed_item_count()
        else:
            dt['name'] = 'Awating...'
            dt['count'] = 1
            dt['progress_all'] = 0
            dt['progress'] = 0
        dt['name_all'] = q.name
        dt['count_all'] = q.task_count
        res['tasks'].append(dt)

    return res

#q_worker = QueueWorker(name=stream.name, dequeue_on_done = True, meta={'id':id})
#for vid in ls:
    #if (vid.type in [1,2]):
        #q_worker.enqueue(WorkerTask(process_video, None, vid=vid))
#worker_queue.enqueue(q_worker)

class DQueue:
    def __init__(self):
        self.data = []
    
    def enqueue(self, data):
        self.data.append(data)
    
    def dequeue(self):
        if (len(self.data) <= 0): return None
        return self.data.pop(0)

    def limit(self, limit):
        if (len(self.data) > limit):
            count = len(self.data) - limit
            self.data = self.data[count:]

class Preloader:
    def __init__(self, range:int = 1, cache:int = 4):
        self.meta = {}
        self.cache = cache
        self.range = range
        self.enum = 0
        self.data = util.Queue()

    # need override
    def is_loaded(self, page, enum) -> bool:
        return False
    
    def check_page_loaded(self, enum):
        for page in self.data:
            if (self.is_loaded(page, enum)): return page
        return None

    def do_limit(self):
        if (len(self.data) > self.cache):
            count = len(self.data) - self.cache
            self.data = util.Queue(self.data[count:])

    # optional override
    def on_receive_data(self, data):
        self.data.put(data)
        self.do_limit()

    def do_request(self, enum):
        pg = self.check_page_loaded(enum)
        if (pg == None):
            data = self.run_request(enum)
            self.on_receive_data(data)
            return data
        return pg

    # optional override (default to check all meta keys)
    def is_meta_diff(self, mt):
        return self.meta != mt

    # need override
    def do_next(self, enum, i):
        pass
    
    # need override
    def do_previous(self, enum, i):
        pass
    
    # need override
    def has_next(self, enum, i):
        return False

    # need override
    def has_previous(self, enum, i):
        return False

    # need override (the main funtion to run)
    def run_request(self, enum):
        return None

    def clear_data(self):
        self.data.clear()

    # (optionally) need to be called from your real get function (or you just call this with the right meta data)
    def do_get(self, enum, meta, preload_other = True):
        if (self.is_meta_diff(meta)):
            self.meta = meta
            self.data.clear()
        result = self.do_request(enum)
        if (preload_other):
            for i in range(1, self.range + 1):
                if (self.has_next(enum, i)): threading.Thread(target=self.do_next, args=(enum, i), daemon=True).start()
                if (self.has_previous(enum, i)): threading.Thread(target=self.do_previous, args=(enum, i), daemon=True).start()
        return result

class PagePreLoader:
    def __init__(self, range:int = 1, cache:int = 4):
        self.per_page = 0
        self.request = None
        self.range = range
        self.cache = cache
        self.page_count = 1
        self.page = 1
        self.page_data = DQueue()

    def check_page_loaded(self, page, per_page):
        for pg in self.page_data.data:
            if (page == pg.page_num and per_page == pg.per_page): return pg
        return None

    async def do_request(self, page, perpage):
        pg = self.check_page_loaded(page, per_page)
        if (pg == None):
            data = await self.request(page, per_page)
            self.receive_data(data)
            return data
        return pg

    def receive_data(self, data):
        self.page_count = data.page_count
        self.page_data.enqueue(data)
        self.page_data.limit(self.cache)
    
    async def get(self, page, per_page):
        self.page = page
        self.per_page = per_page
        result = await self.do_request(page, self.per_page)
        for i in range(1,self.range + 1):
            if (self.page + i <= self.page_count): self.do_request(self.page + i, self.per_page)
            if (self.page - i >= 1): self.do_request(self.page - i, self.per_page)
        return result

