#!/usr/bin/env python
from appJar import gui
import webbrowser
import pyperclip
import sys
import os

numPlayers = 0

def rainbowColor(report):
    # Offenses
    report = report.replace("Role-Quitting", '[color="#00ff00"]Role-Quitting[/color]')
    report = report.replace("Intentional Gamethrowing", '[color="#B22222"]Intentional Gamethrowing[/color]')
    report = report.replace("Reactionary Gamethrowing", '[color="#B22222"]Reactionary Gamethrowing[/color]')
    report = report.replace("Leave Train", '[color="#FFFF00"]Leave Train[/color]')
    report = report.replace("Griefing", '[color="#FF8C00"]Griefing[/color]')
    report = report.replace("Name Abuse", '[color="#FFA500"]Name Abuse[/color]')
    report = report.replace("Cheating/Additional Information", '[color="#DDA0DD"]Cheating/Additional Information[/color]')
    report = report.replace("Hacking", '[color="#ff0000"]Hacking[/color]')
    report = report.replace("Skyping", '[color="#ffff00"]Skyping[/color]')
    report = report.replace("Lag Cheating", '[color="#ffff00"]Lag Cheating[/color]')

    # Punishments
    report = report.replace("On-Hold", '[color="#FFD700"]On-Hold[/color]')

    report = report.replace("WL X2", '[color="#00ff00"]WL X2[/color]')
    report = report.replace("WL X3", '[color="#00ff00"]WL X3[/color]')
    report = report.replace("WL X4", '[color="#00ff00"]WL X4[/color]')
    report = report.replace("WL X6", '[color="#00ff00"]WL X6[/color]')

    report = report.replace("BL X2", '[color="#ff0000"]BL X2[/color]')
    report = report.replace("BL X4", '[color="#ff0000"]BL X4[/color]')
    report = report.replace("Permaban", '[color="#ff0000"]Permaban[/color]')

    report = report.replace("Point Ban", '[color="#ff8800"]Point Ban[/color]')

    # Special stuff
    report = report.replace("Town", '[color="#00ff00"]Town[/color]')
    report = report.replace("Mafia", '[color="#ff0000"]Mafia[/color]')
    report = report.replace("Triad", '[color="#0000ff"]Triad[/color]')
    #report = report.replace("N1", '[color="#00ffff"]N1[/color]') # night + day

    # Town (20 roles)
    report = report.replace("Citizen", '[color="#33CC33"]Citizen[/color]')
    report = report.replace("Mason", '[color="#00ff44"]Mason[/color]')
    report = report.replace('[color="#00ff44"]Mason[/color] Leader', '[color="#22ff77"]Mason Leader[/color]')
    report = report.replace("Mayor", '[color="#44ff44"]Mayor[/color]')
    report = report.replace("Marshall", '[color="#23ef32"]Marshall[/color]')
    report = report.replace("Crier", '[color="#66cc33"]Crier[/color]')
    report = report.replace("Bus Driver", '[color="#55cc11"]Bus Driver[/color]')
    report = report.replace("Spy", '[color="#66aa00"]Spy[/color]')
    report = report.replace("Coroner", '[color="#00dd55"]Coroner[/color]')
    report = report.replace("Jailor", '[color="#66cc00"]Jailor[/color]')
    report = report.replace("Vigilante", '[color="#88cc00"]Vigilante[/color]')
    report = report.replace("Veteran", '[color="#aaff55"]Veteran[/color]')
    report = report.replace("Bodyguard", '[color="#00cc66"]Bodyguard[/color]')
    report = report.replace("Investigator", '[color="#00ff66"]Investigator[/color]')
    report = report.replace("Lookout", '[color="#44ff00"]Lookout[/color]')
    report = report.replace("Detective", '[color="#00ff44"]Detective[/color]')
    report = report.replace("Doctor", '[color="#00ff00"]Doctor[/color]')
    report = report.replace("Sheriff", '[color="#00ff00"]Sheriff[/color]')
    report = report.replace("Escort", '[color="#00ff00"]Escort[/color]')
    report = report.replace("Stump", '[color="#01ff10"]Stump[/color]')

    # Mafia (11 roles)
    report = report.replace("Godfather", '[color="#ff4488"]Godfather[/color]')
    report = report.replace("Consigliere", '[color="#ff5533"]Consigliere[/color]')
    report = report.replace("Janitor", '[color="#ff3333"]Janitor[/color]')
    report = report.replace("Agent", '[color="#ff2244"]Agent[/color]')
    report = report.replace("Kidnapper", '[color="#aa3333"]Kidnapper[/color]')
    report = report.replace("Disguiser", '[color="#dd6644"]Disguiser[/color]')
    report = report.replace("Consort", '[color="#ff0000"]Consort[/color]')
    report = report.replace("Beguiler", '[color="#bb3355"]Beguiler[/color]')
    report = report.replace("Mafioso", '[color="#cc0000"]Mafioso[/color]')
    report = report.replace("Framer", '[color="#dd6600"]Framer[/color]')
    report = report.replace("Blackmailer", '[color="#dd0000"]Blackmailer[/color]')

    # Triad (11 roles)
    report = report.replace("Deceiver", '[color="#6969bb"]Deceiver[/color]')
    report = report.replace("Vanguard", '[color="#697aff"]Vanguard[/color]')
    report = report.replace("Interrogator", '[color="#4a62aa"]Interrogator[/color]')
    report = report.replace("Informant", '[color="#6295dd"]Informant[/color]')
    report = report.replace("Silencer", '[color="#2c58dd"]Silencer[/color]')
    report = report.replace("Incense Master", '[color="#5b84ff"]Incense Master[/color]')
    report = report.replace("Forger", '[color="#2c95dd"]Forger[/color]')
    report = report.replace("Administrator", '[color="#5b99ff"]Administrator[/color]')
    report = report.replace("Liason", '[color="#3366ff"]Liason[/color]')
    report = report.replace("Dragon Head", '[color="#9f8eff"]Dragon Head[/color]')
    report = report.replace("Enforcer", '[color="#2851cc"]Enforcer[/color]')

    # Neutrals (12 roles)
    report = report.replace("Auditor", '[color="#BBCC88"]Auditor[/color]') # add color
    report = report.replace("Witch", '[color="#6622cc"]Witch[/color]')
    report = report.replace("Cultist", '[color="#bb44aa"]Cultist[/color]')
    report = report.replace("Jester", '[color="#fca8fc"]Jester[/color]')
    report = report.replace('[color="#6622cc"]Witch[/color] [color="#00ff00"]Doctor[/color]', '[color="#aa55ff"]Witch Doctor[/color]')
    report = report.replace("Executioner", '[color="#aaccff"]Executioner[/color]')
    report = report.replace("Amnesiac", '[color="#66ffcc"]Amnesiac[/color]')
    report = report.replace("Survivor", '[color="#ffff00"]Survivor[/color]')
    report = report.replace("Mass Murderer", '[color="#bb4455"]Mass Murderer[/color]')
    report = report.replace("Arsonist", '[color="#ffaa00"]Arsonist[/color]')
    report = report.replace("Serial Killer", '[color="#ff00c"]Serial Killer[/color]')
    report = report.replace("Judge", '[color="#BB6655"]Judge[/color]') # add color
    return report

def removePlayer(btn):
    global numPlayers
    btn = btn[6:]
    app.removeLabelFrame(btn + ". ID Verification")
    numPlayers -= 1
    if numPlayers > 0:
        app.showButton("delete" + str(numPlayers))
def checkReports(btn):
    btn = btn[5:]
    print("Checking reports for player" + str(btn))
    try:
        id = app.getEntry("SC2ID"+btn).split("-")[3]
        webbrowser.open('http://www.sc2mafia.com/forum/search.php?q=' + id + "&do=process&contenttype=vBForum_Post&forumchoice%5B%5D=8&childforums=1&exactname=1")
    except IndexError:
        app.infoBox("Error", "Invalid SC2 ID!")

def addPlayer():
    global numPlayers
    if numPlayers > 0:
        app.hideButton("delete"+str(numPlayers))
    numPlayers += 1
    app.startLabelFrame(str(numPlayers) + ". ID Verification")
    app.addEntry("player"+str(numPlayers), 0, 0)
    app.setEntryDefault("player"+str(numPlayers), "Name")
    app.addNamedCheckBox("Correct?", "corr"+str(numPlayers), 0, 1)
    app.addEntry("SC2ID"+str(numPlayers), 0, 2)
    app.setEntryDefault("SC2ID"+str(numPlayers), "SC2 ID")
    app.addNamedButton("Check Offenses", "check"+str(numPlayers), checkReports, 0, 3)
    app.addEntry("prevoffense"+str(numPlayers), 0, 4)
    app.setEntryDefault("prevoffense"+str(numPlayers), "Link Prev. Offense")
    app.addOptionBox("offense"+str(numPlayers), ["None", "Role-Quitting", "Griefing", "Lag Cheating", "Leave Train",
                                       "Reactionary Gamethrowing", "Intentional Gamethrowing",
                                       "Cheating/Additional Information", "Hacking", "Skyping", "Name Abuse"], 0, 5)
    app.addOptionBox("punishment"+str(numPlayers), ["None", "On-Hold", "WL X2", "WL X3", "WL X4", "WL X6", "BL X2", "BL X4", "Point Ban", "Permaban"], 0, 6)
    app.addNamedButton("X", "delete"+str(numPlayers), removePlayer, 0, 7)
    app.stopLabelFrame()

def submitReport():
    global numPlayers
    print("This is supposed to submit report")

    # ID Verification
    report = '[COLOR="#FFF0f5"][B][U]SC ID VERIFICATION[/U][/B][/COLOR]\n'
    for i in range(1, numPlayers+1):
        if app.getCheckBox("corr"+str(i)):
            report += app.getEntry("player"+str(i)) + ": " + '[color="#00ff00"]Correct. ' + app.getEntry("SC2ID"+str(i)) + '[/color]\n'
        else:
            report += app.getEntry("player" + str(i)) + ": " + '[color="#ff0000"]Incorrect. ' + app.getEntry("SC2ID" + str(i)) + '[/color]\n'
    report += '\n'

    # Review
    report += '[B][U][COLOR="#FFF0F5"]Review[/COLOR][/U][/B]\n' + app.getTextArea("Review") + '\n\n'

    # Previous Offenses
    report += '[B][U][COLOR="#FFF0F5"]Previous Offenses[/COLOR][/U][/B]\n'
    for i in range(1, numPlayers+1):
        offense = app.getEntry("prevoffense" + str(i))
        if offense != "":
            report += app.getEntry("player" + str(i)) + ": " + offense + '\n'
    report += '\n'

    # Player Offenses
    report += '[B][U][COLOR="#FFF0F5"]Player Offenses[/COLOR][/U][/B]\n'
    for i in range (1, numPlayers+1):
        report += app.getEntry("player"+str(i)) + ": " + app.getOptionBox("offense"+str(i)) + '\n'
    report += '\n'

    # Recommended Action
    report += '[B][U][COLOR="#FFF0F5"]Recommended Action[/COLOR][/U][/B]\n'
    for i in range (1, numPlayers+1):
        report += app.getEntry("player" + str(i)) + ": " + app.getOptionBox("punishment" + str(i)) + '\n'
    report += '\n'

    # Notes
    report += '[B][U][COLOR="#FFF0F5"]Additional Notes[/COLOR][/U][/B]\n' + 'Thank you for submitting the report, and helping to keep the Mafia community clean.\n' + app.getTextArea("Notes")

    report = rainbowColor(report)

    pyperclip.copy(report)

app = gui()

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

#app.setIcon(resource_path("icon/mafia.ico"))
app.setTitle("SC2 Mafia Report Tool")
app.setFont(size=14, family="Consolas")
app.setBg("#202020", override=True, tint=True)
app.setFg("#808e80", override=True)

app.addLabel("title", "                                                            beta v0.350 by Iaotle                                                            ")


app.startLabelFrame("Review")
app.setSticky("ew")
app.addTextArea("Review")
app.stopLabelFrame()
app.startLabelFrame("Notes")
app.setSticky("ew")
app.addTextArea("Notes")
app.addButton("Submit", submitReport, 1, 0)
app.addButton("Add Player", addPlayer, 2, 0)
app.stopLabelFrame()
app.setLabelFrameFg("Review", "#808e80")
app.setLabelFrameBg("Review", "#202020")
app.setLabelFrameFg("Notes", "#808e80")
app.setLabelFrameBg("Notes", "#202020")
app.go()
