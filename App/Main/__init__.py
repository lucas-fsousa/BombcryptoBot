import threading as thd
from time import sleep
from App import Control as control
from App import Routines as routines
from App.Objects.externalConfigs import ExternalConfigs


def __start__():
    sleep(5)
    config = ExternalConfigs()

    routines.save_logs("starting application")
    thd.Thread(target=control.__safe_close_app__).start()
    while True:

        success = control.__connect_wallet__()
        if success:
            sleep(config.ConnectionScreen)
            success = control.__management__()

        if not success:
            routines.save_logs("retry a connection")
            continue

# =============================================================================================================