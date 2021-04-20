#!/usr/bin/env python3

from threading import Semaphore

class MyQueue(object):                                          #Queue obj to handle Semaphore
    def __init__(self, capacity=2048):                          #Init. obj w/ cap
        self.data = []                                          #Create list

        self.available = Semaphore(capacity)                    #Inverted Semaphore
        [self.available.acquire() for _ in range(capacity)]     #Lock for cap of obj

    def put(self, item):                                        #Semaphore Release : Queue put()
        self.available.release()                                #Release current item from semaphore
        self.data += [item]                                     #Update count

    def get(self):                                              #Semaphore Acquire : Queue get()
        self.available.acquire()                                #Acquire current item to put in queue for semaphore
        return self.data.pop(0)                                 #Pop off queue

    def is_empty(self):                                         #Empty check func
        return len(self.data) == 0                              #Empty check
