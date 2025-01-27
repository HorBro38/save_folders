#### The default name that wil display on folders.  If your game supports renaming the protagonist, you may want to make this equal to that variable, or any number of other options.  If two names are detected that are the same, we will append the date and time of the first save made to help differentiate them.  You can modify the save screen to allow for this to be changed as well, just make sure the variable is always SF_RN_NAME

default SF_RN_NAME = "Default"

#### Defaulting this variable will make it so we generate a new one on each game start.  We also have a persistent variable that tracks all of the names for the folders so that players can update them if they wish

default SF_RN_SEED = SF_RN_GEN()
default persistent.SF_RN_NAMES = [ ]

init python:

    DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    #### This function generates a random string 25 digits long

    def SF_RN_GEN():

        import random
        n = random.SystemRandom().getrandbits(128)
        rv = ""
        for i in range(25):
            rv += DIGITS[n % 36]
            n //= 36
        return rv

    #### This will add the random number to the save's JSON for later correlation as well as the name to display for the save folder

    def jsoncallback(d):
        d["SF_RN_SEED"] = str(SF_RN_SEED)
        d["SF_RN_NAME"] = str(SF_RN_NAME)

    #### This is a function you can use to get a list of all saves as well as their variables for correlation

    def SF_GET_JSON():

        from datetime import datetime

        slots = renpy.loadsave.location.list()
        slots.sort()
        rv = [ ]

        for s in slots:
            c = renpy.loadsave.get_cache(s)
            if c is not None:
                json = c.get_json()
                if json is not None:
                    RN_SEED = json.get("SF_RN_SEED", "")
                    RN_NAME = json.get("SF_RN_NAME", "Unassigned")
                    RN_TIME = json.get("_ctime", "January 1, 1970")
                else:
                    RN_SEED = ""
                    RN_NAME = ""
                    RN_TIME = ""

                #### This will prevent multiple copies of the same seed from showing up in the selection box

                if [x for x in rv if x[1] == RN_SEED]:
                    pass
                else:
                    rv.append([s, RN_SEED])

                #### This code sets the names to the persistent variable that tracks them, and again only makes sure one copy is there.  It will add the time to duplicate names to help clarify which is which

                if [x for x in persistent.SF_RN_NAMES if x[0] == RN_SEED]:
                    pass
                else:
                    if [x for x in persistent.SF_RN_NAMES if x[1] == RN_NAME]:
                        persistent.SF_RN_NAMES.append([RN_SEED, RN_NAME+" - "+str(datetime.fromtimestamp(RN_TIME))])
                    else:
                        persistent.SF_RN_NAMES.append([RN_SEED, RN_NAME])
        return rv

    #### This function gets us the name to display in the list

    def SF_GET_NAME(i):
        rv = next((x for x in persistent.SF_RN_NAMES if x[0] == i), "None")
        return rv

    config.save_json_callbacks.append(jsoncallback)


#### This is a take on the existing save and load screens included with Ren'py.  You will want to remove the existing ones, or move these where you want to use them.  We continue to use the load/save screens to reduce the number of changes needed elsewhere.  The first bit of logic here is to select the folder you want to load from, and can be customized as you see fit

screen load():

    tag menu

    use game_menu(_("Select Folder")):
        fixed:
            order_reverse True
            vbox:
                for i in SF_GET_JSON():
                    textbutton SF_GET_NAME(i[1])[1] action ShowMenu("load_post", SF_GET_NAME(i[1]))

#### This acts as the default load screen, just post seed selection

screen load_post(x):

    tag menu

    use file_slots(_("Load"),x)

#### Since saves will always go to their folder, we can move directly to the file_slots screen

screen save():

    tag menu

    use file_slots(_("Save"), SF_RN_SEED)

#### This is the main file_slots screen from the default Ren'py, with some extra logic to only show the saves that match the currently selected seed and to allow the player to rename the folder if they want

screen file_slots(title,x):

    default page_name_value = FilePageNameInputValue(pattern=_("Page {}"), auto=_("Automatic saves"), quick=_("Quick saves"))
    python:
        if x:
            SF_NAME = DictInputValue(x,1,default=False)
        else:
            SF_NAME = None

    use game_menu(title):

        fixed:

            ## This ensures the input will get the enter event before any of the
            ## buttons do.
            order_reverse True

            vbox:
                xalign 0.5
                style "page_label"

                ## The Folder name.  Click on this will allow a user to rename the folder if they wish

                if SF_NAME:
                    button:
                       xalign 0.5
                       key_events True
                       action SF_NAME.Toggle()

                       input:
                           style "page_label_text"
                           value SF_NAME
                           action SF_NAME.Toggle()

                ## The page name, which can be edited by clicking on a button.
                button:
                    xalign 0.5
                    key_events True
                    action page_name_value.Toggle()

                    input:
                        style "page_label_text"
                        value page_name_value

            ## The grid of file slots.
            grid gui.file_slot_cols gui.file_slot_rows:
                style_prefix "slot"

                xalign 0.5
                yalign 0.5

                spacing gui.slot_spacing

                for i in range(gui.file_slot_cols * gui.file_slot_rows):

                    $ slot = i + 1

                    button:
                        action FileAction(str(slot)+(x[0] if x else ""))

                        has vbox

                        add FileScreenshot(str(slot)+(x[0] if x else "")) xalign 0.5

                        text FileTime(str(slot)+(x[0] if x else ""), format=_("{#file_time}%A, %B %d %Y, %H:%M"), empty=_("empty slot")):
                            style "slot_time_text"

                        text FileSaveName(str(slot)+(x[0] if x else "")):
                            style "slot_name_text"

                        key "save_delete" action FileDelete(str(slot)+(x[0] if x else ""))

            ## Buttons to access other pages.
            vbox:
                style_prefix "page"

                xalign 0.5
                yalign 1.0

                hbox:
                    xalign 0.5

                    spacing gui.page_spacing

                    textbutton _("<") action FilePagePrevious()
                    key "save_page_prev" action FilePagePrevious()

                    if config.has_autosave:
                        textbutton _("{#auto_page}A") action FilePage("auto")

                    if config.has_quicksave:
                        textbutton _("{#quick_page}Q") action FilePage("quick")

                    ## range(1, 10) gives the numbers from 1 to 9.
                    for page in range(1, 10):
                        textbutton "[page]" action FilePage(page)

                    textbutton _(">") action FilePageNext()
                    key "save_page_next" action FilePageNext()

                if config.has_sync:
                    if CurrentScreenName() == "save":
                        textbutton _("Upload Sync"):
                            action UploadSync()
                            xalign 0.5
                    else:
                        textbutton _("Download Sync"):
                            action DownloadSync()
                            xalign 0.5


style page_label is gui_label
style page_label_text is gui_label_text
style page_button is gui_button
style page_button_text is gui_button_text

style slot_button is gui_button
style slot_button_text is gui_button_text
style slot_time_text is slot_button_text
style slot_name_text is slot_button_text

style page_label:
    xpadding 75
    ypadding 5

style page_label_text:
    textalign 0.5
    layout "subtitle"
    hover_color gui.hover_color

style page_button:
    properties gui.button_properties("page_button")

style page_button_text:
    properties gui.text_properties("page_button")

style slot_button:
    properties gui.button_properties("slot_button")

style slot_button_text:
    properties gui.text_properties("slot_button")