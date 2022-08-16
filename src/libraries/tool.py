import time

def hash(userid: int):
    days = int(time.strftime("%d", time.localtime(time.time()))) + 31 * int(time.strftime("%m", time.localtime(time.time()))) + 77
    return (days * userid) >> 8