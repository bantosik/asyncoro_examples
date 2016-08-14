import sys
import asyncoro.disasyncoro as asyncoro

def worker_proc(n, coro=None):
    toprocess = yield coro.receive()
    while toprocess != 'end':
        print('worker {} process: {}'.format(n, toprocess))
        toprocess = yield coro.receive()
    print('ending')

def server_proc(coro=None):
    coro.set_daemon()
    coro.register('server_coro')
    workers = {}
    while True:
        args = yield coro.receive()
        if(args[0] == 'create'):
            cmd, wid, sender = args
            c = asyncoro.Coro(worker_proc, wid)
            workers[wid] = c
            sender.send(('server', ('newworker', wid, c)))
        elif(args[0] == 'list'):
            cmd, sender = args
            sender.send(('server', ('listresp', workers)))


server = asyncoro.Coro(server_proc)
while True:
    cmd = sys.stdin.readline().strip().lower()
    if cmd == 'quit' or cmd == 'exit':
        break