from App import Routines as routines


def define_cache(key):
    try:
        arq = open(r"cache\key_cache.txt", "w")
        arq.write(key)
        arq.close()
    except Exception as ex:
        routines.save_logs(f"creating cache for key failed >> {ex}")

# =====================================================================================================


def delete_cache():
    try:
        arq = open(r"cache\key_cache.txt", "r")
        key = arq.read()
        arq.close()
        if key:
            arq.truncate()
    except Exception as ex:
        routines.save_logs(f"cache read failure >> {ex}")

# =====================================================================================================
