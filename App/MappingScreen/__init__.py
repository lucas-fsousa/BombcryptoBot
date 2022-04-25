
# hover over center of home screen
def get_center_screen():
    import pyautogui as pag
    pag.moveTo((pag.size().width / 2), (pag.size().height / 2))

# =============================================================================================================


# generic instruction to find an RGB color pattern that matches input values
def get_position_by_color(r, g, b, start_pos_x, start_pos_y, end_width=0, end_heigth=0):
    from App.Objects.externalConfigs import ExternalConfigs
    from App import Routines as routines
    import pyautogui as pag

    config = ExternalConfigs()
    ok = False
    try:
        sc = pag.screenshot()
        wid, hei = sc.size
        if end_width > 0 and end_heigth > 0:
            wid = start_pos_x + end_width
            hei = start_pos_y + end_heigth
        else:
            wid = wid - 70  # ignore 65px at end screen width
            hei = hei - 70  # ignore 65px at end screen heigth
        for x in range(start_pos_x, wid, config.CheckPixelSpeed):
            for y in range(start_pos_y, hei, config.CheckPixelSpeed):
                r_temp, g_temp, b_temp = sc.getpixel((x, y))
                if r == r_temp and g == g_temp and b == b_temp:
                    pag.moveTo(x, y, config.MouseDelay)
                    ok = True
                    break
            if ok:
                break
        return ok
    except Exception as ex:
        routines.save_logs(f"unexpected error while fetching image: {ex}")
        get_center_screen()
        return ok

# =============================================================================================================


def get_minor_screen(x, y, wid, hei):
    import pyautogui as pag
    sc = pag.screenshot(region=(x, y, wid, hei))
    pag.moveTo(x, y)
    return sc

# =============================================================================================================


