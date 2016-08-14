#ring benchmark for asyncoro

import asyncoro
import sys
KILLME = object()

def client_proc(me, N, coro=None):
    nexto = yield coro.receive()
    i = yield coro.receive()
    while i != KILLME and i < N:
        #print("cor {} - received {}".format(me, i))
        nexto.send(i + 1)
        i = yield coro.receive()
    nexto.send(KILLME)

def kick(n, coro=None):
    yield coro.resume()
    cors = [asyncoro.Coro(client_proc, i, n) for i in range(503)]
    for i in range(503):
        cors[i].send(cors[(i + 1) % 503])
    cors[0].send(0)

if __name__ == '__main__':
    n = int(sys.argv[1])
    asyncoro.Coro(kick, n)
