def log_debug(message):
    log("debug", message)

def log_error(message):
    log("error", message)

def log_info(message):
    log("info ", message)

def log(type, message):
    print("[{}] {}".format(type.upper(), message), flush=True)
