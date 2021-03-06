import os
import yaml as ym
from App import Routines as routines


class ExternalConfigs:
    def __init__(self):

        stream = open(r"config.yaml", "r")
        configs = ym.safe_load(stream)
        conf = configs["configs"]
        notify = configs["claim_notification"]

        # ================== SYSTEM CONFIGS ==================
        self.TimeForStartHeroWork = float(conf["time_for_start_hero_work"])
        self.SafeResetGamePage = float(conf["safe_reset_game_page"])
        self.ConnectionScreen = float(conf["connection_screen"])
        self.Starting_hero = float(conf["starting_hero"])
        self.DefaultDelay = float(conf["default_delay"])
        self.LoopingDelay = float(conf["looping_delay"])
        self.MouseDelay = float(conf["mouse_delays"])
        self.Attempts = int(conf["attempts"])
        self.Update_map = int(conf["update_map"])
        self.CheckPixelSpeed = int(conf["pixel_speed"])
        self.ResetLogsOnStart = bool(conf["reset_logs_on_start"])

        # ================== NOTIFICATIONS ==================
        self.ResendNotifyTimeout = float(notify["time_re_send"])
        self.EnableNotification = bool(notify["enable"])
        self.EmailToSend = str(notify["email_to_send"])
        self.AmountBCoin = int(notify["amount_bcoin"])

    if not os.path.exists("config.yaml"):
        file = """
    # time in seconds
    configs:
        # default 1 second / default system activity delay
        default_delay: 1.0
        
        # default 1.5 seconds / activate heroes from the list
        starting_hero: 1.5
        
        # default 1.0 / looping execution time delay
        looping_delay: 1.0
        
        # default 20.0 / delay for error checking on initial connection screen
        connection_screen: 20.0
        
        # recommended 0.2
        mouse_delays: 0.2
        
        # count seconds multiplies for update map / default = 20
        update_map: 20
        
        # default: True [False | True] / reset application operation logs
        reset_logs_on_start: True
        
        # default: 10 / recommended to increase the value in cases of slow computer
        attempts: 10
        
        # default: 2 / Recommended to use below 4 to avoid bad application functionality.
        pixel_speed: 2
        
        # default: 500 / time in seconds for start hero work
        time_for_start_hero_work: 500
        
        # default 3600 (1 hour) / time limit in seconds to reset the game page as a way to prevent possible
        # map transition bugs
        safe_reset_game_page: 3600
          
    # configuration to notify the user that it is now possible to claim
    claim_notification:

        # default: False [False | True] / configuration activity status
        enable: False
        
        # default: empty / Email where notification will be sent
        email_to_send: "empty"
        
        # default 40 / value that will be recognized to notify the user
        amount_bcoin: 40
        
        # default 7200 (2 hour) / timeout to resend the notification to the user
        time_re_send: 7200
        """
        try:
            arq = open(r"config.yaml", "w")
            arq.write(file)
            arq.close()
        except Exception as ex:
            routines.save_logs(f"external configs open failed >> {ex}")

