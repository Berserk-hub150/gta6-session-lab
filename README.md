# Session Lab

A standalone multiplayer lobby prototype for experimenting with session state outside GTA VI.

## Quick start

```sh
python server.py
```

Open http://127.0.0.1:8765 in two tabs, choose names and click the arena.

## Using your own material

The local server is the shared authority for normalized positions. Clients send updates twice per second; inactive clients expire after 120 seconds. It has no connection to GTA Online, GTA VI or a game networking protocol.

Independent fan project. Grand Theft Auto is a trademark of its respective owners.
