import logging

from gevent import spawn
from gevent.queue import JoinableQueue

from .fastget import FastGet


class MassGet:
    def __init__(self, urls, dic, threads=10, report_db=False, keepalive=None, each_threads=10):
        self.dic = dic
        self.report_db = report_db
        self.keepalive = keepalive
        self.each_threads = each_threads
        self.queue = JoinableQueue()
        [self.queue.put(x.strip()) for x in urls]
        [spawn(self.worker) for _ in xrange(threads)]
        self.queue.join()

    def worker(self):
        while not self.queue.empty():
            url = self.queue.get()
            try:
                FastGet(url, self.dic, self.each_threads, self.report_db, self.keepalive)
            except Exception as e:
                logging.error(str(e))
            finally:
                self.queue.task_done()
