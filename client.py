import sys
import asyncoro.disasyncoro as asyncoro

def client_fun(msg, server, workers, coro):
    who, rest = msg
    if who == 'client':
        args = rest.split()
        if (args[0] == 'create'):
            server.send(('create', args[1], coro))
        elif (args[0] == 'send'):
            cmd, who, what = args
            workers[who].send(what)
        elif (args[0] == 'list'):
            server.send(('list', coro))
    elif who == 'server':
        cmd = rest[0]
        if(cmd == 'newworker'):
            cmd, wid, worker = rest
            workers[wid] = worker
        elif cmd == 'listresp':
            cmd, newworkers = rest
            workers.clear()
            workers.update(newworkers)

def client_proc(coro=None):
    coro.set_daemon()
    server = yield coro.locate('server_coro')
    workers = {}
    msg = yield coro.receive()
    while True:
        client_fun(msg, server, workers, coro)
        msg = yield coro.receive()

c = asyncoro.Coro(client_proc)

while True:
    cmd = sys.stdin.readline().strip().lower()
    if cmd == 'quit' or cmd == 'exit':
        break
    else:
        c.send(('client', cmd))