import pyautogui as pag
from time import sleep
from App import MappingScreen as mp
from App.Objects.bombcolors import BombColors
from App.Objects.externalConfigs import ExternalConfigs
from App import Routines as routines


get_bomb_area = (100, 110)  # get the application area (no color)


def metamask_icon():
    b_color = BombColors()
    config = ExternalConfigs()
    success = False
    for _try in range(0, config.Attempts, 1):
        x, y = get_bomb_area
        rgb = b_color.MetamaskIcon
        for r, g, b in rgb:
            if mp.get_position_by_color(r, g, b, x, y):
                success = True
                break
        if success:
            break
        sleep(config.LoopingDelay)
    return success


# =============================================================================================================


def treasure_chest_btn():
    b_color = BombColors()
    config = ExternalConfigs()
    success = False
    for _try in range(0, config.Attempts, 1):
        x, y = get_bomb_area
        r, g, b = b_color.TreasureChest
        if mp.get_position_by_color(r, g, b, x, y):
            success = True
            break
        sleep(config.LoopingDelay)
    return success

# =============================================================================================================


def next_error_or_start_btn():  # locates the application's default button (orange color)
    b_color = BombColors()
    config = ExternalConfigs()
    success = False
    for _try in range(0, config.Attempts, 1):
        r, g, b = b_color.DefaultButton
        x, y = get_bomb_area
        if mp.get_position_by_color(r, g, b, x, y):
            current_pos = pag.position()
            pag.moveTo(current_pos.x + 20, current_pos.y + 5)
            success = True
            break
        sleep(config.LoopingDelay)
    return success

# =============================================================================================================


def map_btn():  # look for the button to enter the map (wine color)
    b_color = BombColors()
    config = ExternalConfigs()
    success = False
    for _try in range(0, config.Attempts, 1):
        x, y = get_bomb_area
        r, g, b = b_color.TreasureIcon
        if mp.get_position_by_color(r, g, b, x, y):
            success = True
            break
        sleep(config.LoopingDelay)
    return success

# =============================================================================================================


def close_btn():  # look for the close window button (red color)
    b_color = BombColors()
    config = ExternalConfigs()
    success = False
    for _try in range(0, config.Attempts, 1):
        x, y = get_bomb_area
        r, g, b = b_color.CloseButton
        if mp.get_position_by_color(r, g, b, x, y):
            success = True
            break
        sleep(config.LoopingDelay)
    return success

# =============================================================================================================


def back_btn():  # search for the back button (light green)
    b_color = BombColors()
    config = ExternalConfigs()
    success = False
    for _try in range(0, config.Attempts, 1):
        for color in b_color.BackBtn:
            x, y = get_bomb_area
            r, g, b = color
            if mp.get_position_by_color(r, g, b, x, y):
                success = True
                break
        if success:
            break
        sleep(config.LoopingDelay)
    return success

# =============================================================================================================


def champion_selected_btn(x, y):
    b_color = BombColors()
    config = ExternalConfigs()
    success = False
    for _try in range(0, config.Attempts, 1):
        colors = b_color.ChampionSelected
        for color in colors:
            if mp.get_position_by_color(color[0], color[1], color[2], x, y):
                success = True
                break
        if success:
            break
        sleep(config.LoopingDelay)
    return success

# =============================================================================================================


def work_on_btn(current_pos_x, current_pos_y):  # check if current hero is already at work
    b_color = BombColors()
    for btn in b_color.WorkButtonOn:
        r, g, b = btn
        return mp.get_position_by_color(r, g, b, current_pos_x, current_pos_y, 350, 30)

# =============================================================================================================


def loading_screen():  # check if the screen is loading
    b_color = BombColors()
    config = ExternalConfigs()
    x, y = get_bomb_area
    while True:
        r, g, b = b_color.LoadScreenHeroList
        waiting = mp.get_position_by_color(r, g, b, x, y)
        if not waiting:
            break
        else:
            sleep(config.DefaultDelay)

# =============================================================================================================


def heroes_icon_btn():  # find hero icon on home screen
    b_color = BombColors()
    config = ExternalConfigs()
    success = False
    for _try in range(0, config.Attempts, 1):
        x, y = get_bomb_area
        r, g, b = b_color.HeroesIcon
        if mp.get_position_by_color(r, g, b, x, y):
            success = True
            break
        sleep(config.LoopingDelay)
    return success

# =============================================================================================================


def work_off_btn(x, y, no_param=False):
    """
    if the Param parameter is checked, the "X" and "Y" will be ignored and will use
     the current position retrieved in the method
    """
    success = False
    b_color = BombColors()
    config = ExternalConfigs()
    if no_param:
        current_pos = pag.position()
        r, g, b = b_color.WorkButtonOff
        if mp.get_position_by_color(r, g, b, current_pos.x, current_pos.y, 250, 15):
            pag.click()
            routines.save_logs("starting hero")
            sleep(config.Starting_hero)
            success = True
    else:
        for _try in range(0, config.Attempts, 1):
            r, g, b = b_color.WorkButtonOff
            if mp.get_position_by_color(r, g, b, x, y):
                success = True
                break
            sleep(config.DefaultDelay)
    return success

# =============================================================================================================


def any_work_btn(x, y):
    b_color = BombColors()
    config = ExternalConfigs()
    success = False
    for _try in range(0, config.Attempts, 1):

        r, g, b = b_color.WorkButtonOff
        if mp.get_position_by_color(r, g, b, x, y):
            success = True
            break
        for btn in b_color.WorkButtonOn:
            r1, g1, b1 = btn
            if mp.get_position_by_color(r1, g1, b1, x, y):
                success = True
                break
        if success:
            break
    return success

# =============================================================================================================


def coin_btn(x=0, y=0):
    success = False
    config = ExternalConfigs()
    b_color = BombColors()

    if x == 0 and y == 0:
        x, y = get_bomb_area

    for _try in range(0, config.Attempts, 1):
        r, g, b = b_color.CoinIcon
        if mp.get_position_by_color(r, g, b, x, y):
            success = True
            break
    return success

# =============================================================================================================


def green_health_bar(start_pos_x, start_pos_y):  # check the current champion's life situation
    b_color = BombColors()
    rested = False
    max_wid = 300
    max_hei = 70
    for color in b_color.GreenHealthsBar:
        r, g, b = color
        if mp.get_position_by_color(r, g, b, start_pos_x, start_pos_y, max_wid, max_hei):
            rested = True
            break
    return rested

# =============================================================================================================


def sign_metamask_btn(attempts=0):  # finds the metamask subscribe button
    b_color = BombColors()
    config = ExternalConfigs()
    success = False

    if attempts == 0:
        attempts = config.Attempts

    for _try in range(0, attempts, 1):
        x, y = get_bomb_area
        r, g, b = b_color.SignButton
        if mp.get_position_by_color(r, g, b, x, y):
            current_pos = pag.position()
            pag.moveTo(current_pos.x + 200, current_pos.y, config.MouseDelay)
            x, y = pag.position()

            y -= 20
            pag.moveTo(x, y, config.MouseDelay)
            if mp.get_position_by_color(r, g, b, x, y):
                x, y = pag.position()
                pag.moveTo(x, y + 15, config.MouseDelay)
                success = True
        if success:
            break
        sleep(config.LoopingDelay)
    return success

# =============================================================================================================
