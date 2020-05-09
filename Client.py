import gi
import json
import os
import pyperclip
import sys
import webbrowser
from io import StringIO

from s2protocol import s2_cli

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

# TODO: resize window when stuff happens
# TODO: clear everything on replay load
# TODO: add about to menu
# TODO: submit
# TODO: licenses for s2protocol

# testing CSS
css = '#comboboxtext1 > box.linked > button.combo > box > cellview {color: #0000FF;}'


class Player():
    def __init__(self, id, name=None, previousList=[], currentList=[], punishment="None"):
        self.id = id
        self.name = name
        self.previousList = previousList
        self.currentList = currentList
        self.punishment = punishment


class FileChooserWindow(gi.repository.Gtk.Window):
    def __init__(self):
        dialog_window = Gtk.Window.__init__(self)
        dialog = Gtk.FileChooserDialog("Please choose a file", dialog_window, Gtk.FileChooserAction.OPEN, (
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK,), )

        self.add_filters(dialog)

        while True:
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                if loadReplayFromFile(dialog.get_filename()) == 0:
                    break
            else:
                break
        dialog.destroy()

    def add_filters(self, dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name("Replays (*.SC2Replay)")
        filter_text.add_pattern("*.SC2Replay")
        dialog.add_filter(filter_text)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files (*)")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)


class Handler:
    def file_load(self, filedialog):
        win = FileChooserWindow()
        win.connect("destroy", Gtk.Window.close)
        resizeToFit()

    def onDestroy(self, *args):
        Gtk.main_quit()

    def gtk_close_window(self, window):
        Gtk.Window.close(window)

    def gtk_main_quit(self, button):
        sys.exit()

    def on_about(self, button):
        window = Gtk.Window.new(Gtk.WindowType.TOPLEVEL)
        popup = Gtk.MessageDialog(window, title='About', flags=Gtk.DialogFlags.MODAL, type=Gtk.MessageType.INFO,
                                  message_format="SC2 Mafia Report Tool v0.5 by Iaotle")
        popup.run()
        popup.destroy()

    def on_combobox_changed(self, button):
        id = Gtk.Buildable.get_name(button)
        button.set_property("name", id)
        colorTheBox(button)
        resizeToFit()

    def on_previous_check(self, button):
        playerIndex = button.get_name().split(".")[1]
        id = builder.get_object("sc2idplayer" + playerIndex).get_text().split("-")[3]
        webbrowser.open(
            'http://www.sc2mafia.com/forum/search.php?q=' + id + "&do=process&contenttype=vBForum_Post&forumchoice%5B%5D=8&childforums=1&exactname=1")

    def on_previous_add(self, button):
        pane = button.get_parent()
        pane = pane.get_parent()
        pane = pane.get_child2()
        pane = pane.get_child()
        pane = pane.get_child()

        pagebuilder = Gtk.Builder()
        pagebuilder.add_from_file("previous.glade")
        pagebuilder.connect_signals(Handler())
        newPrevious = pagebuilder.get_object("prevWindow")
        # newPrevious = Gtk.Button.new()

        pane.pack_end(newPrevious, expand=True, fill=True, padding=5)
        pane.show_all()
        # TODO: resize

    def on_previous_remove(self, button):
        window = button.get_parent().get_parent().get_parent().get_parent().get_parent()
        window.destroy()

    def on_current_add(self, button):
        print("Add Crime to player ", button.get_name())
        print("Add Current Offense to player ", button.get_name())
        pane = button.get_parent()
        pane = pane.get_child2()
        pane = pane.get_child()
        pane = pane.get_child()
        # TODO: use this shit when submitting
        # test = vpane.get_children()
        # print(test)

        pagebuilder = Gtk.Builder()
        pagebuilder.add_from_file("current.glade")
        pagebuilder.connect_signals(Handler())
        newPrevious = pagebuilder.get_object("prevWindow")

        pane.pack_end(newPrevious, expand=True, fill=True, padding=5)
        pane.show_all()

    def on_current_remove(self, button):
        window = button.get_parent().get_parent().get_parent().get_parent()
        print(window)
        window.destroy()

    def on_report_toggled(self, button):
        notebook = builder.get_object("notebook1")
        if button.get_active():
            pagebuilder = Gtk.Builder()
            pagebuilder.add_from_file("page.glade")
            pagebuilder.connect_signals(Handler())
            newPage = pagebuilder.get_object("hbox1")

            id = Gtk.Buildable.get_name(button)[12:]
            number = builder.get_object("label" + id).get_text()
            name = builder.get_object("nameplayer" + id).get_text()
            sc2id = builder.get_object("sc2idplayer" + id).get_text()

            Gtk.Notebook.append_page(notebook, newPage, Gtk.Label.new(number + ". " + name))

            # TODO: unique stuff for later
            pagebuilder.get_object("addCrime").set_property("name", "addCrimePlayer." + id)
            pagebuilder.get_object("checkPrevious").set_property("name", "checkPreviousPlayer." + id)
            pagebuilder.get_object("addPrevious").set_property("name", "addPreviousPlayer." + id)

            pagebuilder.get_object("playername").set_text(name)
            pagebuilder.get_object("playerID").set_text(sc2id)
            notebook.show_all()
        else:
            buttonName = Gtk.Buildable.get_name(button)[12:]
            # TODO: maybe instead of loop we do this more nicely? just a thought
            # TODO: separate if needed
            print("Report button name: ", buttonName)
            for i in range(0, notebook.get_n_pages()):
                page = notebook.get_nth_page(i)
                labelName = notebook.get_tab_label_text(page).split('.')[0]
                if labelName == buttonName:
                    notebook.remove_page(i)
        resizeToFit()
        # TODO: remove the report tab from the notebook

    def on_submit(self, button):
        review = getText(builder.get_object("reviewText"))
        notes = getText(builder.get_object("notesText"))

        playerList = generatePlayerList()

        # ID Verification
        report = '[COLOR="#FFF0f5"][B][U]SC ID VERIFICATION[/U][/B][/COLOR]\n'
        for player in playerList:
            report += player.name + ": " + '[color="#00ff00"]' + player.id + '[/color]\n'
        report += '\n'

        # Review
        report += '[B][U][COLOR="#FFF0F5"]Review[/COLOR][/U][/B]\n' + review + '\n\n'

        # Previous Offenses
        report += '[B][U][COLOR="#FFF0F5"]Previous Offenses[/COLOR][/U][/B]\n'
        for player in playerList:
            offense = player.previousList
            if offense != []:
                for crime in offense:
                    report += player.name + ": " + str(crime) + '\n'  # TODO: multiple offenses
            else:
                report += player.name + ": None" + '\n'
        report += '\n'

        # Player Offenses
        report += '[B][U][COLOR="#FFF0F5"]Player Offenses[/COLOR][/U][/B]\n'
        for player in playerList:
            offense = player.currentList
            if offense != []:
                for crime in offense:
                    report += player.name + ": " + str(crime) + '\n'  # TODO: multiple offenses
            else:
                report += player.name + ": None" + '\n'
        report += '\n'

        # Recommended Action
        report += '[B][U][COLOR="#FFF0F5"]Recommended Action[/COLOR][/U][/B]\n'
        for player in playerList:
            report += player.name + ": " + player.punishment + '\n'
        report += '\n'

        # Notes
        report += '[B][U][COLOR="#FFF0F5"]Additional Notes[/COLOR][/U][/B]\n' + 'Thank you for submitting the report, and helping to keep the Mafia community clean.\n' + notes

        report = addColor(report)
        pyperclip.copy(report)

        # TODO: iterate over notebook, copy to clipboard


def addColor(text):
    # Offenses
    text = text.replace("Role-Quitting", '[color="#00ff00"]Role-Quitting[/color]')
    text = text.replace("Intentional Gamethrowing", '[color="#B22222"]Intentional Gamethrowing[/color]')
    text = text.replace("Reactionary Gamethrowing", '[color="#B22222"]Reactionary Gamethrowing[/color]')
    text = text.replace("Leave Train", '[color="#FFFF00"]Leave Train[/color]')
    text = text.replace("Griefing", '[color="#FF8C00"]Griefing[/color]')
    text = text.replace("Name Abuse", '[color="#FFA500"]Name Abuse[/color]')
    text = text.replace("Cheating/Additional Information", '[color="#DDA0DD"]Cheating/Additional Information[/color]')
    text = text.replace("Hacking", '[color="#ff0000"]Hacking[/color]')
    text = text.replace("Skyping", '[color="#ffff00"]Skyping[/color]')
    text = text.replace("Lag Cheating", '[color="#ffff00"]Lag Cheating[/color]')

    # Punishments
    text = text.replace("On-Hold", '[color="#FFD700"]On-Hold[/color]')

    text = text.replace("WL X2", '[color="#00ff00"]WL X2[/color]')
    text = text.replace("WL X3", '[color="#00ff00"]WL X3[/color]')
    text = text.replace("WL X4", '[color="#00ff00"]WL X4[/color]')
    text = text.replace("WL X6", '[color="#00ff00"]WL X6[/color]')

    text = text.replace("BL X2", '[color="#ff0000"]BL X2[/color]')
    text = text.replace("BL X4", '[color="#ff0000"]BL X4[/color]')
    text = text.replace("Permaban", '[color="#ff0000"]Permaban[/color]')

    text = text.replace("Point Ban", '[color="#ff8800"]Point Ban[/color]')

    # Special stuff
    text = text.replace("Town", '[color="#00ff00"]Town[/color]')
    text = text.replace("Mafia", '[color="#ff0000"]Mafia[/color]')
    text = text.replace("Triad", '[color="#0000ff"]Triad[/color]')
    # text = text.replace("N1", '[color="#00ffff"]N1[/color]') # night + day

    # Town (20 roles)
    text = text.replace("Citizen", '[color="#33CC33"]Citizen[/color]')
    text = text.replace("Mason", '[color="#00ff44"]Mason[/color]')
    text = text.replace('[color="#00ff44"]Mason[/color] Leader', '[color="#22ff77"]Mason Leader[/color]')
    text = text.replace("Mayor", '[color="#44ff44"]Mayor[/color]')
    text = text.replace("Marshall", '[color="#23ef32"]Marshall[/color]')
    text = text.replace("Crier", '[color="#66cc33"]Crier[/color]')
    text = text.replace("Bus Driver", '[color="#55cc11"]Bus Driver[/color]')
    text = text.replace("Spy", '[color="#66aa00"]Spy[/color]')
    text = text.replace("Coroner", '[color="#00dd55"]Coroner[/color]')
    text = text.replace("Jailor", '[color="#66cc00"]Jailor[/color]')
    text = text.replace("Vigilante", '[color="#88cc00"]Vigilante[/color]')
    text = text.replace("Veteran", '[color="#aaff55"]Veteran[/color]')
    text = text.replace("Bodyguard", '[color="#00cc66"]Bodyguard[/color]')
    text = text.replace("Investigator", '[color="#00ff66"]Investigator[/color]')
    text = text.replace("Lookout", '[color="#44ff00"]Lookout[/color]')
    text = text.replace("Detective", '[color="#00ff44"]Detective[/color]')
    text = text.replace("Doctor", '[color="#00ff00"]Doctor[/color]')
    text = text.replace("Sheriff", '[color="#00ff00"]Sheriff[/color]')
    text = text.replace("Escort", '[color="#00ff00"]Escort[/color]')
    text = text.replace("Stump", '[color="#01ff10"]Stump[/color]')

    # Mafia (11 roles)
    text = text.replace("Godfather", '[color="#ff4488"]Godfather[/color]')
    text = text.replace("Consigliere", '[color="#ff5533"]Consigliere[/color]')
    text = text.replace("Janitor", '[color="#ff3333"]Janitor[/color]')
    text = text.replace("Agent", '[color="#ff2244"]Agent[/color]')
    text = text.replace("Kidnapper", '[color="#aa3333"]Kidnapper[/color]')
    text = text.replace("Disguiser", '[color="#dd6644"]Disguiser[/color]')
    text = text.replace("Consort", '[color="#ff0000"]Consort[/color]')
    text = text.replace("Beguiler", '[color="#bb3355"]Beguiler[/color]')
    text = text.replace("Mafioso", '[color="#cc0000"]Mafioso[/color]')
    text = text.replace("Framer", '[color="#dd6600"]Framer[/color]')
    text = text.replace("Blackmailer", '[color="#dd0000"]Blackmailer[/color]')

    # Triad (11 roles)
    text = text.replace("Deceiver", '[color="#6969bb"]Deceiver[/color]')
    text = text.replace("Vanguard", '[color="#697aff"]Vanguard[/color]')
    text = text.replace("Interrogator", '[color="#4a62aa"]Interrogator[/color]')
    text = text.replace("Informant", '[color="#6295dd"]Informant[/color]')
    text = text.replace("Silencer", '[color="#2c58dd"]Silencer[/color]')
    text = text.replace("Incense Master", '[color="#5b84ff"]Incense Master[/color]')
    text = text.replace("Forger", '[color="#2c95dd"]Forger[/color]')
    text = text.replace("Administrator", '[color="#5b99ff"]Administrator[/color]')
    text = text.replace("Liason", '[color="#3366ff"]Liason[/color]')
    text = text.replace("Dragon Head", '[color="#9f8eff"]Dragon Head[/color]')
    text = text.replace("Enforcer", '[color="#2851cc"]Enforcer[/color]')

    # Neutrals (12 roles)
    text = text.replace("Auditor", '[color="#BBCC88"]Auditor[/color]')  # add color
    text = text.replace("Witch", '[color="#6622cc"]Witch[/color]')
    text = text.replace("Cultist", '[color="#bb44aa"]Cultist[/color]')
    text = text.replace("Jester", '[color="#fca8fc"]Jester[/color]')
    text = text.replace('[color="#6622cc"]Witch[/color] [color="#00ff00"]Doctor[/color]',
                        '[color="#aa55ff"]Witch Doctor[/color]')
    text = text.replace("Executioner", '[color="#aaccff"]Executioner[/color]')
    text = text.replace("Amnesiac", '[color="#66ffcc"]Amnesiac[/color]')
    text = text.replace("Survivor", '[color="#ffff00"]Survivor[/color]')
    text = text.replace("Mass Murderer", '[color="#bb4455"]Mass Murderer[/color]')
    text = text.replace("Arsonist", '[color="#ffaa00"]Arsonist[/color]')
    text = text.replace("Serial Killer", '[color="#ff00cc"]Serial Killer[/color]')
    text = text.replace("Judge", '[color="#BB6655"]Judge[/color]')  # add color
    return text


def generatePlayerList():
    playerList = []

    notebook = builder.get_object("notebook1")
    for i in range(0, notebook.get_n_pages()):
        page = notebook.get_nth_page(i)

        leftTab = page.get_children()[0].get_children()[
            0].get_children()  # TODO: add total punishment (2 comboboxtexts)
        verdict = page.get_children()[0].get_children()[1].get_children()[0].get_active_text()
        if verdict is None:
            verdict = "None"
        previousBoxes = \
        page.get_children()[1].get_children()[0].get_children()[0].get_children()[1].get_children()[0].get_children()[
            0].get_children()
        crimeBoxes = \
        page.get_children()[2].get_children()[0].get_children()[0].get_children()[1].get_children()[0].get_children()[
            0].get_children()

        name = leftTab[0].get_text()
        id = leftTab[1].get_text()
        previousList = []
        currentList = []

        # for i in range(0, len(leftTab)):
        #     print(leftTab[i].get_text())
        # TODO: colorize player names for easier readability?

        for i in range(0, len(previousBoxes)):
            link = \
            previousBoxes[i].get_children()[0].get_children()[0].get_children()[0].get_children()[0].get_children()[
                0].get_text()
            crime = \
            previousBoxes[i].get_children()[0].get_children()[1].get_children()[0].get_children()[0].get_children()[
                0].get_active_text()
            punishment = \
            previousBoxes[i].get_children()[0].get_children()[1].get_children()[1].get_children()[0].get_children()[
                0].get_active_text()
            if crime is not None and punishment is not None:
                previousCrime = crime + ": " + punishment
                if link != "":
                    previousCrime += " (" + link + ")"
                previousList += [previousCrime]
            # TODO: combine these two

        for i in range(0, len(crimeBoxes)):
            crime = \
            crimeBoxes[i].get_children()[0].get_children()[0].get_children()[0].get_children()[0].get_children()[
                0].get_active_text()
            punishment = \
            crimeBoxes[i].get_children()[0].get_children()[0].get_children()[1].get_children()[0].get_children()[
                0].get_active_text()
            if crime is not None and punishment is not None:
                currentList += [crime + ": " +
                                punishment]

        playerList += [Player(id, name, previousList, currentList, verdict)]

    return playerList


def resizeToFit():
    _, preferred = window.get_preferred_size()
    window.resize(preferred.width, preferred.height)


def getText(textview):
    buffer = textview.get_buffer()
    startIter, endIter = buffer.get_bounds()
    text = buffer.get_text(startIter, endIter, False)
    return text


def colorTheBox(button):
    role = button.get_active_text()
    cssProvider = Gtk.CssProvider()
    cssString = b"""#""" + bytearray(button.get_name(), 'utf-8') + b""" {background: #303030;}"""
    cssString += b"""#""" + bytearray(button.get_name(),
                                      'utf-8') + b""" > box.linked > button.combo {background: #303030;}"""
    cssString += b"""#""" + bytearray(button.get_name(),
                                      'utf-8') + b""" > box.linked > button.combo > box > cellview {text-shadow: none; color: """
    if role == 'Citizen':
        cssString += b"""#33cc33;}"""
    elif role == 'Mason':
        cssString += b"""#00ff44;}"""
    elif role == 'Mason Leader':
        cssString += b"""#22ff77;}"""
    elif role == 'Mayor':
        cssString += b"""#44ff44;}"""
    elif role == 'Marshall':
        cssString += b"""#23ef32;}"""
    elif role == 'Crier':
        cssString += b"""#66cc33;}"""
    elif role == 'Bus Driver':
        cssString += b"""#55cc11;}"""
    elif role == 'Spy':
        cssString += b"""#66aa00;}"""
    elif role == 'Coroner':
        cssString += b"""#00dd55;}"""
    elif role == 'Jailor':
        cssString += b"""#66cc00;}"""
    elif role == 'Vigilante':
        cssString += b"""#88cc00;}"""
    elif role == 'Veteran':
        cssString += b"""#aaff55;}"""
    elif role == 'Bodyguard':
        cssString += b"""#00cc66;}"""
    elif role == 'Investigator':
        cssString += b"""#00ff66;}"""
    elif role == 'Lookout':
        cssString += b"""#44ff00;}"""
    elif role == 'Detective':
        cssString += b"""#00ff44;}"""
    elif role == 'Doctor':
        cssString += b"""#00ff00;}"""
    elif role == 'Sheriff':
        cssString += b"""#00ff00;}"""
    elif role == 'Escort':
        cssString += b"""#00ff00;}"""
    elif role == 'Stump':
        cssString += b"""#01ff10;}"""
        # Mafia
    elif role == 'Godfather':
        cssString += b"""#ff4488;}"""
    elif role == 'Consigliere':
        cssString += b"""#ff5533;}"""
    elif role == 'Janitor':
        cssString += b"""#ff3333;}"""
    elif role == 'Agent':
        cssString += b"""#ff2244;}"""
    elif role == 'Kidnapper':
        cssString += b"""#aa3333;}"""
    elif role == 'Disguiser':
        cssString += b"""#dd6644;}"""
    elif role == 'Consort':
        cssString += b"""#ff0000;}"""
    elif role == 'Beguiler':
        cssString += b"""#bb3355;}"""
    elif role == 'Mafioso':
        cssString += b"""#cc0000;}"""
    elif role == 'Framer':
        cssString += b"""#dd6600;}"""
    elif role == 'Blackmailer':
        cssString += b"""#dd0000;}"""
        # Triad
    elif role == 'Deceiver':
        cssString += b"""#6969bb;}"""
    elif role == 'Vanguard':
        cssString += b"""#697aff;}"""
    elif role == 'Interrogator':
        cssString += b"""#4a62aa;}"""
    elif role == 'Informant':
        cssString += b"""#6295dd;}"""
    elif role == 'Silencer':
        cssString += b"""#2c58dd;}"""
    elif role == 'Incense Master':
        cssString += b"""#5b84ff;}"""
    elif role == 'Forger':
        cssString += b"""#2c95dd;}"""
    elif role == 'Administrator':
        cssString += b"""#5b99ff;}"""
    elif role == 'Liason':
        cssString += b"""#3366ff;}"""
    elif role == 'Dragon Head':
        cssString += b"""#9f8eff;}"""
    elif role == 'Enforcer':
        cssString += b"""#2851cc;}"""
        # Neutrals
    elif role == 'Auditor':
        cssString += b"""#bbccbb;}"""
    elif role == 'Witch':
        cssString += b"""#6622cc;}"""
    elif role == 'Cultist':
        cssString += b"""#bb44aa;}"""
    elif role == 'Jester':
        cssString += b"""#fca8fc;}"""
    elif role == 'Witch Doctor':
        cssString += b"""#aa55ff;}"""
    elif role == 'Executioner':
        cssString += b"""#aaccff;}"""
    elif role == 'Amnesiac':
        cssString += b"""#66ffcc;}"""
    elif role == 'Survivor':
        cssString += b"""#ffff00;}"""
    elif role == 'Mass Murderer':
        cssString += b"""#bb4455;}"""
    elif role == 'Arsonist':
        cssString += b"""#ffaa00;}"""
    elif role == 'Serial Killer':
        cssString += b"""#ff00cc;}"""
    elif role == 'Judge':
        cssString += b"""#bb6655;}"""
    else:
        cssString += b"""#FFFFFF;}"""

    cssProvider.load_from_data(cssString)
    Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), cssProvider,
                                             Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)


def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    print("Path: ", os.path.join(base_path, relative_path))
    return os.path.join(base_path, relative_path)


def loadReplayFromFile(filepath):
    # TODO: reset everything when loading
    buffer = StringIO()
    try:
        s2_cli.main(buffer, ['--json', '--initdata', filepath])
    except ValueError as err:
        window = Gtk.Window.new(Gtk.WindowType.TOPLEVEL)
        popup = Gtk.MessageDialog(window, title='Replay Error', flags=Gtk.DialogFlags.MODAL, type=Gtk.MessageType.ERROR,
                                  buttons=Gtk.ButtonsType.OK, message_format="ERROR: " + str(err))
        popup.run()
        popup.destroy()
        return err
    (playerlist, IDlist) = parseJSON(buffer)

    for i in range(1, 16):
        builder.get_object("nameplayer" + str(i)).set_text(playerlist[i - 1])
        builder.get_object("sc2idplayer" + str(i)).set_text(IDlist[i - 1])
    return 0


def parseJSON(buffer):
    buffer = buffer.getvalue()
    data = json.loads(buffer)
    playerlist = []
    IDlist = []

    for i in range(0, 15):
        IDlist.append(data["m_syncLobbyState"]["m_lobbyState"]["m_slots"][i]["m_toonHandle"])
        playerlist.append(data["m_syncLobbyState"]["m_userInitialData"][i]["m_name"])

    return playerlist, IDlist


builder = Gtk.Builder()
builder.add_from_file("main.glade")
builder.connect_signals(Handler())
window = builder.get_object("mainWindow")

settings = Gtk.Settings.get_default()
settings.props.gtk_button_images = True

# get number label colors to work:
for i in range(1, 16):
    label = builder.get_object("label" + str(i))
    label.set_property("name", "label")
    label = builder.get_object("nameplayer" + str(i))
    label.set_property("name", "label")
    label = builder.get_object("sc2idplayer" + str(i))
    label.set_property("name", "label")

cssProvider = Gtk.CssProvider()
cssProvider.load_from_path('style.css')  # TODO: resources instead of relative paths
styleContext = Gtk.StyleContext()
Gtk.StyleContext.add_provider_for_screen(
    Gdk.Screen.get_default(),
    cssProvider,
    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

window.show_all()  # TODO: don't show anything until they laod a replay

Gtk.main()
