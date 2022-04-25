DEBUG = False

if DEBUG:
    print("START DEBUG")
    from time import sleep
    from App import Find as find
    sleep(3)
    find.metamask_icon()
    print("END DEBUG")
else:
    # MAIN APPLICATION STARTING
    from time import sleep
    try:
        from App import Main
        Main.__start__()
    except Exception as ex:
        print(f'{ex}')
        sleep(10)
