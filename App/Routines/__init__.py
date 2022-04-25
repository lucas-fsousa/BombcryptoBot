import os
import keyboard as kb
import pyautogui as pag
import pytesseract as ptc
import cv2
from cv2 import cv2
from time import sleep
from datetime import datetime as dt
from App import MappingScreen as mp
from App import Cache as cache
from App import Find as find
from App.Objects.mail import Email
from App.Objects.externalConfigs import ExternalConfigs

ptc.pytesseract.tesseract_cmd = r"Tesseract-OCR/tesseract.exe"


def scroll_list_heroes(reverse=False, repetition=1, speed=0.5):
    """
    responsible for scrolling the list of heroes from a specific point to another point
    :param reverse: defines the course that the scroll will be applied to (bool)
    :param repetition: number of times the method will be repeated (int)
    :param speed: speed at which the scroll is performed (float)
    :return: None
    """
    config = ExternalConfigs()
    pos = None
    for c in range(0, repetition, 1):
        for attempts in range(0, 5, 1):
            sleep(0.2)
            mp.get_center_screen()

            if not reverse:
                pag.moveTo(pag.position().x - 100, pag.position().y + 130, speed)
                pos = pag.position()
                pag.drag(0, - 250, 1)
                break
            else:
                pag.moveTo(pag.position().x - 150, pag.position().y - 50, speed)
                pag.drag(0, 205, 4)
                pos = pag.position()
                break
        sleep(config.DefaultDelay)
    return pos

# ===================================================================================================


def save_logs(message):  # keeps the logs of actions performed during the application's execution
    dt_hr = f"{dt.now().date()} - {dt.now().time().hour}:{dt.now().time().minute}:{dt.now().time().second}"
    print(f"{dt_hr} >>> {message}")
    arq = open(r"logs\bombcrypto.log", "a")
    arq.write(f"{dt_hr} >>>\t{message}\n")
    arq.close()

# ===================================================================================================


def anti_afk():
    if find.treasure_chest_btn():
        pag.click()

    sleep(5)
    if find.close_btn():
        pag.click()

# ===================================================================================================


def update_map():
    success = False
    if find.back_btn():
        pag.click()
        sleep(5)
        if find.map_btn():
            pag.click()
            sleep(5)
            success = True
    return success

# ===================================================================================================


def close_app():  # force the application to terminate
    while True:
        if kb.is_pressed(["Esc"]):
            save_logs("exiting...")
            os.system(r"taskkill /f /t /im bcrypto_bot.exe && exit")

# ===================================================================================================


def reset_page():  # refresh browser page
    """
    responsible for applying a common page reset (Ctrl+f5)
    :return: None
    """
    save_logs("updating the page...")
    mp.get_center_screen()
    pag.keyDown("ctrl")
    pag.press(["f5"])
    pag.keyUp("Ctrl")
    sleep(10)
    pag.keyDown("ctrl")
    pag.keyUp("Ctrl")

# ===================================================================================================


def control_flow_hero_list(position_x, position_y, reset=False):
    """
    method responsible for controlling the location of the mouse pointer,
    which reduces the value of Y by 30 whenever invoked

    :param position_x: current position of x (int)
    :param position_y: current position of y (int)
    :param reset: responsible for checking if it is necessary to reset the flow in the list of heroes (bool)
    :return: None
    """
    # Controls the cursor position and sets the position on the next item
    pag.moveTo(position_x, (position_y - 15))
    # hero list scroll control
    if reset:
        move = pag.position(position_x, position_y)
        pag.moveTo(move.x, move.y)

# ===================================================================================================


def read_text_from_image(x, y, w, h, name=""):
    """
    reads an image with definitions included by the user, the position of y and x
    must be informed and the size of the image that will be read from the points of
    x and y, must also be informed the name that will be assigned to the image. The
    image will be properly changed to black and white colors before it is saved in the defined folder
    :param x: position x (int)
    :param y: position y (int)
    :param w: represents the width of the screen that will be read after the point X
    :param h: represents the height of the screen that will be read after the point Y
    :param name: imagem name for read (str)
    :return: success (bool)
    :rtype:
    """
    success = False
    try:
        name = name + ".jpg"

        sc = pag.screenshot(region=(x, y, w, h))
        sc.save(name)
        img = cv2.imread(name)
        img = cv2.cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        img = cv2.cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV or cv2.THRESH_OTSU)[1]
        cv2.imwrite(name, img)

        matches = tes_read_list(name)

        if matches >= 5:
            success = True
    except Exception as ex:
        save_logs(f"crash while handling images>> {ex}")
    return success

# ===================================================================================================


def tes_read_list(name_image):
    """
    reads images using tesseract and checks the number of matches found during the checks
    :param name_image: the name of an image to be read (str)
    :return: Matches (int)
    """
    matches = 0
    config = ExternalConfigs()
    try:
        img = cv2.imread(name_image)
        whitelist = '-c tessedit_char_whitelist=0123456789,'
        list_tes_string_read = (
            f"{ptc.image_to_string(img, lang='fil', config=f'--psm 12 --oem 1 {whitelist}')}".strip(),
            f"{ptc.image_to_string(img, lang='afr', config=f'--psm 12 --oem 1 {whitelist}')}".strip(),
            f"{ptc.image_to_string(img, lang='cat', config=f'--psm 12 --oem 1 {whitelist}')}".strip(),
            f"{ptc.image_to_string(img, lang='eng', config=f'--psm 12 --oem 1 {whitelist}')}".strip(),
            f"{ptc.image_to_string(img, lang='epo', config=f'--psm 12 --oem 1 {whitelist}')}".strip(),
            f"{ptc.image_to_string(img, lang='uzb', config=f'--psm 12 --oem 1 {whitelist}')}".strip(),
            f"{ptc.image_to_string(img, lang='yor', config=f'--psm 12 --oem 1 {whitelist}')}".strip()
        )

        for item in list_tes_string_read:
            item = item.split(',')[0]
            if item == '':
                continue

            if int(item) >= config.AmountBCoin:
                matches += 1

    except Exception as ex:
        save_logs(f"failed while listing tesseract items list >> {ex}")
    finally:
        return matches

# ===================================================================================================


def send_notification():  # checks if it is necessary to send notification to the user
    """
    controls the reading of an image for character extraction
    and checks if the settings allow the user to be notified
    :return: boolean
    """
    success = False
    pos = pag.position()
    pag.moveTo((pos.x - 550), (pos.y + 60))
    pos = pag.position()
    find.coin_btn(pos.x, pos.y)
    pos = pag.position()

    if read_text_from_image((pos.x - 70), (pos.y + 50), 250, 70, "coin-icon"):
        em = Email()
        config = ExternalConfigs()
        if config.EmailToSend != "empty":
            if em.send_mail(em.DefaultSubject, config.EmailToSend, em.DefaultMessage):
                save_logs("Notified user")
                success = True
            else:
                save_logs("failed to notify user")
        else:
            save_logs("The user will not be notified. Notification email filled in incorrectly. [EMPTY]")
    return success

# ===================================================================================================

