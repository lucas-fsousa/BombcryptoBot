import os
import pyautogui as pag
from zipfile import ZipFile
from time import sleep
from time import time


last_notification_time = time()


def __safe_close_app__():
    from App import Routines as routines
    routines.close_app()

# ====================================================================================================


def __connect_wallet__():
    """
    checks if there is already an open connection with the metamask,
    the connection is processed and then a new attempt is made connection to metamask
    :return: success (bool)
    """
    from App.Objects.externalConfigs import ExternalConfigs
    from App import Routines as routines
    from App import Find as find

    config = ExternalConfigs()
    success = False
    try:
        # checks if have popup to sign
        routines.save_logs("initiating attempts to connect the wallet")
        if find.sign_metamask_btn(attempts=2):
            routines.save_logs(f"there is already an authentication in progress. Canceling!")
            pag.click()
            sleep(config.DefaultDelay)

        routines.reset_page()  # reset current page (ctrl + f5)
        routines.save_logs("starting try connect")
        if find.next_error_or_start_btn():
            pag.click()
            sleep(5)  # fixed! no remove
            routines.save_logs("starting try sign metamask")
        if find.metamask_icon():
            pos = pag.position()
            pag.moveTo(pos.x + 20, pos.y)
            pag.click()
            sleep(config.DefaultDelay)
            if find.sign_metamask_btn():
                routines.save_logs("successfully connected on the wallet")
                pag.click()
                sleep(config.DefaultDelay)
                success = True
    except Exception as ex:
        routines.save_logs(f"internal error on try connect wallet >>> {ex}")
    finally:
        return success

# =======================================================================================================


def __checks_if_successfully_login__():
    from App import Routines as routines
    from App import Find as find

    success = True
    try:
        routines.save_logs("checking server connection status")
        if find.next_error_or_start_btn():
            routines.save_logs("an unexpected event was found. Returning to authentication module")
            success = False
            pag.click()
    finally:
        return success

# =======================================================================================================


def __validate_resources__():
    from App.Objects.externalConfigs import ExternalConfigs
    from App import Routines as routines
    from App import Cache as cache

    config = ExternalConfigs()
    # check if the folders already exist on the system
    if not os.path.exists("logs"):
        os.mkdir("logs")

    if not os.path.exists("cache"):
        os.mkdir("cache")

    routines.save_logs("validating resources")
    # if not os.path.exists("Tesseract-OCR"):
    #     try:
    #         # download the necessary resource
    #         if not os.path.exists("Tesseract-OCR.zip"):
    #             data.download_dependencies()
    #
    #         # extract the zip file
    #         routines.save_logs("extracting files")
    #         zp = ZipFile('Tesseract-OCR.zip', 'r')
    #         zp.extractall()
    #         zp.close()
    #         os.remove(r"Tesseract-OCR.zip")
    #     except Exception as ex:
    #         routines.save_logs(f"failed to extract zip files >> {ex}")

    # reset logs on start
    if config.ResetLogsOnStart:
        file = open(r"logs\bombcrypto.log", "w")
        file.write("")
        file.close()

    if cache.read_cache():
        return True

    if routines.insert_and_validate_key():
        return True
    else:
        return False

# =======================================================================================================


def __management__():
    """
    This method is responsible for controlling the application during the
    execution of the maps and also performs some routine activities such as anti afk
    to avoid expulsion from the server due to inactivity and activation of heroes that are on temporary rest.

    :return: boolean
    :params: no params
    """
    from App.Objects.externalConfigs import ExternalConfigs
    from App import Routines as routines
    from App import Find as find

    config = ExternalConfigs()
    success = True
    next_notify_time = time()
    safe_reset_game_page = time().__add__(config.SafeResetGamePage)
    try:
        while success:
            routines.save_logs("starting search for hero list")
            if find.heroes_icon_btn():  # look for the hero list icon to enter
                routines.save_logs("successfully located list")
                pag.click()
                sleep(config.DefaultDelay)
                success = hero_work()
            else:
                routines.save_logs("Heroes list not located.")
                success = False

            if success:  # checks if it is possible to identify a map
                routines.save_logs("waiting for the map")
                if not find.map_btn():
                    success = False
                    routines.save_logs("no map found")
                else:
                    pag.click()
                    sleep(config.DefaultDelay)

            if success:
                routines.save_logs("opening the map and preparing to explode boxes!")
                success = map_control()

            # if success:
            #     # checks if it is necessary to send claim notification to the user
            #     if time() > next_notify_time and config.EnableNotification:
            #         if find.treasure_chest_btn():
            #             pag.click()
            #             sleep(5)
            #             find.close_btn()
            #             send = routines.send_notification()
            #             sleep(5)
            #             find.close_btn()
            #             pag.click()
            #
            #             if send:  # checks if the notification was successfully sent to the user
            #                 # defines when a new notification will be sent to the user
            #                 next_notify_time = time().__add__(config.ResendNotifyTimeout)
            if success:
                if find.back_btn():
                    pag.click()
                else:
                    success = False

            if time() > safe_reset_game_page:
                routines.save_logs("timeout for page reset reached. Safe reset module activated.")
                success = False
    except Exception as ex:
        routines.save_logs(f"internal error on try start works >>> {ex}")
    finally:
        return success

# =======================================================================================================


def map_control():
    from App.Objects.externalConfigs import ExternalConfigs
    from App import Routines as routines
    from App import Find as find

    config = ExternalConfigs()
    success = True
    time_end_hero_work = time().__add__(config.TimeForStartHeroWork)
    update_hero_count_time = 0
    routines.save_logs("waiting for error or new map initialization")
    while time() < time_end_hero_work:
        if find.next_error_or_start_btn():
            pag.click()
            sleep(15)

            # found another button / means it's on the home page
            if not find.back_btn():
                routines.save_logs("Wops. An error was found.")
                success = False
                return success
            else:
                routines.save_logs("Let's go to the next map!")
                continue
        else:
            # anti afk
            if update_hero_count_time % 3 == 0:
                routines.anti_afk()

        update_hero_count_time += 1
        sleep(config.DefaultDelay)

        # responsible for updating the map to avoid bugs in heroes
        if update_hero_count_time == config.Update_map:
            update_hero_count_time = 0
            if routines.update_map():
                routines.save_logs("updating heroes on the map...")
            else:
                routines.save_logs("Failed to perform map update.")
                success = False

        if not success:
            break
    return success

# =======================================================================================================


def hero_work():
    """
    Method responsible for putting the heroes to work if they are rested. It involves using other methods.
    :return: success (bool)
    """
    from App import Routines as routines
    from App.Objects.externalConfigs import ExternalConfigs
    from App import Find as find

    config = ExternalConfigs()
    success = False
    try:
        find.loading_screen()  # wait for load screen
        pos = routines.scroll_list_heroes(repetition=4, speed=0.1)
        pag.moveTo(pos.x - 300, pos.y + 140)
        temp_x, temp_y = pag.position()

        safe_break = 0
        while not find.any_work_btn(temp_x, temp_y) and safe_break <= 5:
            temp_y = temp_y - 40
            safe_break += 1

        # ============= configure the start mouse position ==============
        current_pos = pag.position()
        safe_position = current_pos = pag.position(current_pos.x - 250, current_pos.y + 30)
        pag.moveTo(current_pos.x, current_pos.y, config.MouseDelay)
        count = 0
        safe_break = 0
        all_working = False

        # looping will run until all heroes are working
        routines.save_logs(f"making sure the hero is rested")
        while not all_working:
            # checks if there was forced stop
            if safe_break == 110:
                routines.save_logs("safe break active")
                success = True
                break

            current_pos = pag.position()  # keep the current position
            if find.green_health_bar(safe_position.x, current_pos.y):  # check the hero's rest state
                find.work_off_btn(0, 0, True)  # check if it is possible to activate the selected hero

            else:
                count += 1
                routines.control_flow_hero_list(current_pos.x, current_pos.y)

                # helps control screen scroll
                if count == 22:
                    # reset the controls
                    routines.scroll_list_heroes(repetition=1, speed=0.05, reverse=True)
                    routines.control_flow_hero_list(safe_position.x, safe_position.y, reset=True)
                    count = 0

            all_working_check = pag.position()
            # checks if the current hero is already working. If the return is true, the looping ends.
            all_working = find.work_on_btn(all_working_check.x, all_working_check.y)
            safe_break += 1

        # makes some attempts to locate the heroes screen close button
        if find.close_btn():
            pag.click()
            success = True
    except Exception as ex:
        routines.save_logs(f"error starting job {ex}")
    finally:
        return success
