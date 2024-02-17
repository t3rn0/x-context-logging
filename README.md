# x-context-logging
Passing context between web services (PoC).

***
Start the server app in terminal 1:
```
$ uvicorn server:app
INFO:     Started server process [6622]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```
Run the client code in terminal 2:
```
$ python client.py
```
Back to the server's stdout in terminal 1:
```
{"time": "2024-02-17T16:01:16.176383+04:00", "level": "INFO", "message": "Inside async GET method.", "extra": {"sync_method": false, "some_var": 4}}
{"time": "2024-02-17T16:01:16.177073+04:00", "level": "INFO", "message": "Inside async GET method.", "extra": {"sync_method": false, "some_var": 3}}
{"time": "2024-02-17T16:01:16.177995+04:00", "level": "INFO", "message": "Inside sync GET method.", "extra": {"sync_method": true, "some_var": 1}}
{"time": "2024-02-17T16:01:16.178401+04:00", "level": "INFO", "message": "Inside sync GET method.", "extra": {"sync_method": true, "some_var": 2}}
INFO:     127.0.0.1:49392 - "GET /root/async HTTP/1.1" 200 OK
INFO:     127.0.0.1:49395 - "GET /root/async HTTP/1.1" 200 OK
INFO:     127.0.0.1:49393 - "GET /root/sync HTTP/1.1" 200 OK
INFO:     127.0.0.1:49394 - "GET /root/sync HTTP/1.1" 200 OK
```
