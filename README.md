# Leonida Session Lab

**Open two tabs and move one player.** The second tab follows the same shared arena, giving you a small, inspectable example of multiplayer state.

## Try it with two players

```sh
python server.py
```

Open [the local lobby](http://127.0.0.1:8765) in two tabs. Join with a different name in each, click a new position in one tab and watch the marker move in both. Python’s standard library serves the client and the API.

## Follow one move through the server

| Request | What happens |
|---|---|
| `POST /join` | Creates a player and returns a session token to that client. |
| `POST /move` | Updates the named session’s coordinates in the 0–100 arena. |
| `GET /state` | Returns the names and positions visible to the clients. |

The browser sends updates twice per second. After a client stops sending updates, the server removes it on the next request once 120 seconds have elapsed. The demo binds to the loopback interface and runs independently of GTA VI and GTA Online.

---

[Explore the GTA VI project collection](https://github.com/Berserk-hub150/gta6-resource-index) · Independent fan project. Grand Theft Auto is a trademark of its respective owners.
