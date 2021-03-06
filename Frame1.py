#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Boa:Frame:Frame1


import re
import binascii
from binascii import hexlify

import wx

#-------------------------------------------------------------------------------

CHARS = {
        'A' : '\x80',
        'B' : '\x81',
        'C' : '\x82',
        'D' : '\x83',
        'E' : '\x84',
        'F' : '\x85',
        'G' : '\x86',
        'H' : '\x87',
        'I' : '\x88',
        'J' : '\x89',
        'K' : '\x8A',
        'L' : '\x8B',
        'M' : '\x8C',
        'N' : '\x8D',
        'O' : '\x8E',
        'P' : '\x8F',
        'Q' : '\x90',
        'R' : '\x91',
        'S' : '\x92',
        'T' : '\x93',
        'U' : '\x94',
        'V' : '\x95',
        'W' : '\x96',
        'X' : '\x97',
        'Y' : '\x98',
        'Z' : '\x99',
        
        'a' : '\x9A',
        'b' : '\x9B',
        'c' : '\x9C',
        'd' : '\x9D',
        'e' : '\x9E',
        'f' : '\x9F',
        'g' : '\xA0',
        'h' : '\xA1',
        'i' : '\xA2',
        'j' : '\xA3',
        'k' : '\xA4',
        'l' : '\xA5',
        'm' : '\xA6',
        'n' : '\xA7',
        'o' : '\xA8',
        'p' : '\xA9',
        'q' : '\xAA',
        'r' : '\xAB',
        's' : '\xAC',
        't' : '\xAD',
        'u' : '\xAE',
        'v' : '\xAF',
        'w' : '\xB0',
        'x' : '\xB1',
        'y' : '\xB2',
        'z' : '\xB3',

        '0' : '\xC1',
        '1' : '\xC2',
        '2' : '\xC3',
        '3' : '\xC4',
        '4' : '\xC5',
        '5' : '\xC6',
        '6' : '\xC7',
        '7' : '\xC8',
        '8' : '\xC9',
        '9' : '\xCA',
        
        ' ' : '\xFF',
}

HEX = {v:k for k,v in CHARS.items()}

SHOOTS_CHAR = {
        '0' : '\x00',
        '1' : '\x01',
        '2' : '\x02',
        '3' : '\x03',
        '4' : '\x04',
        '5' : '\x05',
        '6' : '\x06',
        '7' : '\x07',
        '8' : '\x08',
        '9' : '\x09',
        '10' : '\x0A',
        '11' : '\x0B',
        '12' : '\x0C',
        '13' : '\x0D',
        '14' : '\x0E',
        '15' : '\x0F',
        '16' : '\x16',
        '17' : '\xFF',    
}

SHOOTS_HEX = {v:k for k,v in SHOOTS_CHAR.items()}

START_POWER_HEX = ['\x30', '\x48', '\x50', '\x58', '\x5E', '\x66', '\x6E', '\x80', '\x9A', '\xB4', '\xCA', '\xFF']
MAX_POWER_HEX = ['\x03', '\x04', '\x05', '\x06', '\x07']
SPEED_HEX = ['\x02', '\x01', '\x00']
WEIGHT_HEX = ['\x02', '\x01', '\x00', '\x04', '\x05']
KEEPER_HEX = ['\x03', '\x02', '\x01', '\x00']
ANGRY_HEX = ['\x0D', '\x06', '\x02', '\x01', '\x04', '\x00', '\x05']


SHOOT_NAMES = (
        "DEFORMA LA PELOTA, DIRECTA",
        "TIRA A PUERTA Y SE PARA, AL TOCAR PUEDE IR HACIA TU PROPIA PORTERIA",
        "TIRA RECTO HASTA QUE SE DESVIA LA ULTIMA HORA",
        "VA LENTA Y SE HACE PEQUENYA",
        "REBOTA CON LA PARED PARA SALIR DIRECTA A GOL",
        "PASA DE LARGO DE LA PORTERIA Y DA VUELTAS HASTA IR DIRECTA A PUERTA",
        "SE ELEVA AL FONDO DEL CAMPO VUELVE A LINEA DE GOL Y AL CAER SUELE ENTRAR",
        "HAZE ZIG-ZAG MIENTRAS VA DIRECTO A PORTERIA",
        "SE ELEVA AL CIELO EN BOCA DE GOL Y AL CAER SUELE ENTRAR",
        "ZIG-ZAG MIENTRAS VA DIRECTO A PORTERIA (A LO PLATANO, TEAM 1) CON EFECTO ESTIRADO DE PELOTA (00)",
        "DIRECTO A PORTERIA Y A MITAD DESPARECE, APARECE MAS ADELANTE PARA IR DIRECTA A GOL",
        "TIRO DEL OSITO, PERO PARECE QUE FALLA EL SPRITE (SOLO CHICAS?)",
        "TRAS PEQUENYA 'S' DIRECTA A GOL"
        "REBOTA DE LADO A LADO HASTA SALIR DIRECTA A GOL",
        "TIRO DE REMOLINO MORTAL, DIRECTA A GOL",
        "DIRECTA, LA FICHA SE PONE NARANJA",
        "TIRO ESPECIAL, SE SUSPENDE EL PARTIDO XD",
        "TIRO FAKE, LA POLLA XD",
        "SIN ESPECIAL"
)

FALL_TYPES = {

        "0" : {"HEX" : "\x14", "NAME" : "Original"},
        "1" : {"HEX" : "\x09", "NAME" : "CAEN DE PIE APOYANDOSE"},
        "2" : {"HEX" : "\x0F", "NAME" : "caen de pie"},
        "3" : {"HEX" : "\x12", "NAME" : "DOS BOTES AL RECIBIR GOLPE"},
        "4" : {"HEX" : "\x13", "NAME" : "3 BOTES (2 PEQUEÑOS) Y NO CAEN AL SUELO"},
        "5" : {"HEX" : "\x10", "NAME" : "1 BOTE Y RUEDAN (COMO CUANDO TE CHOCAS CON LA PARED) PERO NO CAEN"},
        "6" : {"HEX" : "\x17", "NAME" : "DOBLE REBANADA Y TRAS UN BOTE"},
        "7" : {"HEX" : "\x1F", "NAME" : "siempre caen de pie, a partir de picaos caen de 1 ostia"},
        "8" : {"HEX" : "\x32", "NAME" : "caen y no se levantan tras un rato como cuando le das el limite de golpes"},
        "9" : {"HEX" : "\x33", "NAME" : "los envia a chodos, quizas como cuando reciben el especial"},
}

#-------------------------------------------------------------------------------
# File

def loadfile(file,action):
    if action == "read":
        rom = open(file,'rb')
    elif action == "write":
        rom = open(file,'r+b')
    
    return rom

def closefile(rom):
    rom.close()
    
#-------------------------------------------------------------------------------
# Time

def loadtime(rom):
    rom.seek(0x01D6C9)
    mins = rom.read(1)
    mins =  ord(mins)
    
    rom.seek(0x01D6D3)
    secs = rom.read(1)
    secs = ord(secs)
    
    return mins , secs

def savetime(rom, mins, secs):
    
    
    rom.seek(0x01D6C9)
    rom.write(convertint(int(mins)))
    
    rom.seek(0x01D6D3)
    rom.write(convertint(int(secs)))
    
#-------------------------------------------------------------------------------
# Charge

def loadcharge(rom):
    rom.seek(0x0190A6)
    charge = rom.read(1)
    charge = ord(charge)
    
    return charge

def savecharge(rom, charge):
    
    rom.seek(0x190A6)
    rom.write(convertint(int(charge)))

#-------------------------------------------------------------------------------
# Music

def loadmusic(rom):

    
    musicHex = ['\x03', '\x0C', '\x0D', '\x0E', '\x0F', '\x10', '\x11']
    music = [0,0,0,0,0]
    rom.seek(0x01D8DC)
    musics = rom.read(5)
    
    i = 0
    for data in musics:
        if data == musicHex[0]:
            music[i] = 0
        elif data == musicHex[1]:
            music[i] = 1
        elif data == musicHex[2]:
            music[i] = 2
        elif data == musicHex[3]:
            music[i] = 3
        elif data == musicHex[4]:
            music[i] = 4
        elif data == musicHex[5]:
            music[i] = 5
        elif data == musicHex[6]:
            music[i] = 6
        i += 1
        
    return music

def savemusic(rom, music):
    
    musicHex = ["\x00", "\x00", "\x00", "\x00", "\x00"]
    
    i = 0
    for data in music:
        if data == 0:
            musicHex[i] = "\x03"
        elif data == 1:
            musicHex[i] = "\x0C"
        elif data == 2:
            musicHex[i] = "\x0D"
        elif data == 3:
            musicHex[i] = "\x0E"
        elif data == 4:
            musicHex[i] = "\x0F"
        elif data == 5:
            musicHex[i] = "\x10"
        elif data == 6:
            musicHex[i] = "\x11"
        
        i += 1
    
    rom.seek(0x1D8DC)
    for i in range(5):
        rom.write(musicHex[i])
    
#-------------------------------------------------------------------------------
# No penalty

def loadnopenalty(rom):
    penalty = "\x18"
    
    enabled = False
    
    rom.seek(0x01B637)
    data = rom.read(1)
    
    if data == penalty:
        enable = False
    else:
        enable = True
    
    return enable

def savenopenalty(rom, enable):
    
    rom.seek(0x01B637)
    
    if enable:
        rom.write("\x17")
    else:
        rom.write("\x18")

#-------------------------------------------------------------------------------

def loadFallType(rom):
    
    rom.seek(0x01932E)
    hexType = rom.read(1)
    type = 0
    
    for key, val in sorted(FALL_TYPES.items()):
        if val["HEX"] == hexType:
            type = key
    
    return int(type)

def saveFallType(rom, type):
    
    hexType = "\x00"
    
    for key, val in sorted(FALL_TYPES.items()):
        if key == str(type):
            hexType = val["HEX"]
    
    rom.seek(0x01932E)
    rom.write(hexType)

#-------------------------------------------------------------------------------

def loadFlyHit(rom):
    
    rom.seek(0x019303)
    heightHex = rom.read(1)
    
    height = int(hexlify(heightHex), 16)
    
    return height

def saveFlyHit(rom, type):
    
    heightHex = convertint(type)
    
    rom.seek(0x019303)
    rom.write(heightHex)

#-------------------------------------------------------------------------------

def loadFlyShoot(rom):
    
    rom.seek(0x01933f)
    heightHex = rom.read(1)
    
    height = int(hexlify(heightHex), 16)
    
    return height

def saveFlyShoot(rom, type):
    
    heightHex = convertint(type)
    
    rom.seek(0x01933f)
    rom.write(heightHex)

#-------------------------------------------------------------------------------
# Teams

class Team(object):
    
    def __init__(self, teamNameOffset, teamStatsOffset, playerNameOffset, playerShootOffset, playersDisplayStatsOffset):
        self.teamNameOffset = teamNameOffset
        self.playerNameOffset = playerNameOffset
        self.playerShootOffset = playerShootOffset
        self.teamStatsOffset = teamStatsOffset
        self.playersDisplayStatsOffset = playersDisplayStatsOffset
        
    def loadteam(self, rom):
        
        # Team name
        
        rom.seek(self.teamNameOffset)
        teamname = rom.read(8)
        
        # Players name
        
        playersname = ['' for i in range(5)]
        
        rom.seek( self.playerNameOffset[0] )
        playersname[0] = rom.read(4)
        
        rom.seek( self.playerNameOffset[1] )
        playersname[1] = rom.read(4)
        
        rom.seek( self.playerNameOffset[2] )
        playersname[2] = rom.read(4)
        
        rom.seek( self.playerNameOffset[3] )
        playersname[3] = rom.read(4)
        
        rom.seek( self.playerNameOffset[4] )
        playersname[4] = rom.read(4)
        
        return teamname, playersname

    def saveteam(self, rom, teamname, players):

        # Team Name
        
        rom.seek(self.teamNameOffset)
        rom.write(teamname)
        
        # Players Name
        
        for i in range(5):
            rom.seek(self.playerNameOffset[i])
            rom.write(players[i])

    def readTeamStats(self, rom):
        
        rom.seek(self.teamStatsOffset)
        teamStats = rom.read(2)
        
        return teamStats
    
    def writeTeamStats(self, rom, attack, defense):
        
        attackHex = convertint(attack)
        defenseHex = convertint(defense)
        
        stats = attackHex + defenseHex
        
        
        rom.seek(self.teamStatsOffset)
        rom.write(stats)
        
    def loadPlayerStats(self, rom, offset):
        
        rom.seek(offset)
        statsHex = rom.read(6)
        
        startPowerPlayer = 0
        maxPowerPlayer = 0
        speedPlayer = 0
        weightPlayer = 0
        keeper = 0
        angryPlayer = 0
        
        
        j = 1
        for hex in START_POWER_HEX:
            if statsHex[0] == hex:
                startPowerPlayer = j
            j += 1
        
        j = 1
        for hex in MAX_POWER_HEX:
            if statsHex[1] == hex:
                maxPowerPlayer = j
            j += 1
        
        j = 1
        for hex in SPEED_HEX:
            if statsHex[2] == hex:
                speedPlayer = j
            j += 1
        
        j = 1
        for hex in WEIGHT_HEX:
            if statsHex[3] == hex:
                weightPlayer = j
            j += 1
        
        j = 1
        for hex in KEEPER_HEX:
            if statsHex[4] == hex:
                keeperPlayer = j
            j += 1
        
        j = 1
        for hex in ANGRY_HEX:
            if statsHex[5] == hex:
                angryPlayer = j
            j += 1
        
        statsInt = [startPowerPlayer, maxPowerPlayer, speedPlayer, weightPlayer, keeperPlayer, angryPlayer]
        
        return statsInt
    
    def writePlayerStats(self, rom, offsets, playerStats):
        
        i = 0
        for offset in offsets:
            
            rom.seek(offset)
            
            statsHex = []
            
            #print("stats Player %d: SP:%d MP:%d S:%d W:%d K:%d A:%d" % ( i, playerStats[i][0]-1, playerStats[i][1]-1, playerStats[i][2]-1, playerStats[i][3]-1, playerStats[i][4]-1, playerStats[i][5]-1))
            
            statsHex.append(START_POWER_HEX[playerStats[i][0]-1])
            statsHex.append(MAX_POWER_HEX[playerStats[i][1]-1])
            statsHex.append(SPEED_HEX[playerStats[i][2]-1])
            statsHex.append(WEIGHT_HEX[playerStats[i][3]-1])
            statsHex.append(KEEPER_HEX[playerStats[i][4]-1])
            statsHex.append(ANGRY_HEX[playerStats[i][5]-1])
            
            
            for hex in statsHex:
                rom.write(hex)
            
            i += 1

    def sShootRead(self, rom):
        
        playerShoot = ['' for i in range(5)]
        playerShootHex = ['' for i in range(5)]
        
        rom.seek( self.playerShootOffset[0] )
        playerShootHex[0] = rom.read(1)
        
        rom.seek( self.playerShootOffset[1] )
        playerShootHex[1] = rom.read(1)
        
        rom.seek( self.playerShootOffset[2] )
        playerShootHex[2] = rom.read(1)
        
        rom.seek( self.playerShootOffset[3] )
        playerShootHex[3] = rom.read(1)
        
        rom.seek( self.playerShootOffset[4] )
        playerShootHex[4] = rom.read(1)
        
        i = 0
        for hex in playerShootHex:
            
            pattern = re.compile(r'(' + '|'.join(SHOOTS_HEX.keys()) + r')')
            result = pattern.sub(lambda x: SHOOTS_HEX[x.group()], hex)
            
            playerShoot[i] = result
            i+=1
        
        return playerShoot

    def sShootWrite(self, rom, index):
        
        pattern = re.compile(r'\b(' + '|'.join(SHOOTS_CHAR.keys()) + r')\b')
        
        result = ''
        
        for c in index:
            hex = pattern.sub(lambda x: SHOOTS_CHAR[x.group()], str(c))
            
            if hex == ' ':
                hex = '\xFF'
            
            result += hex
        
        
        rom.seek(self.playerShootOffset[0])
        rom.write(result[0])
        
        rom.seek(self.playerShootOffset[1])
        rom.write(result[1])
        
        rom.seek(self.playerShootOffset[2])
        rom.write(result[2])
        
        rom.seek(self.playerShootOffset[3])
        rom.write(result[3])
        
        rom.seek(self.playerShootOffset[4])
        rom.write(result[4])
        
    def readDisplayStats(self, rom):
        powStr = ['' for i in range(5)]
        powHex = ['' for i in range(5)]
        spdStr = ['' for i in range(5)]
        spdHex = ['' for i in range(5)]
        defStr = ['' for i in range(5)]
        defHex = ['' for i in range(5)]
        
        for i in range(5):
            rom.seek(self.playersDisplayStatsOffset[i])
            powHex[i] = rom.read(3)
            powStr[i] = hextostr(powHex[i])
        
        for i in range(5):
            rom.seek(self.playersDisplayStatsOffset[i]+3)
            spdHex[i] = rom.read(3)
            spdStr[i] = hextostr(spdHex[i])
        
        for i in range(5):
            rom.seek(self.playersDisplayStatsOffset[i]+6)
            defHex[i] = rom.read(3)
            defStr[i] = hextostr(defHex[i])
        return (powStr, spdStr, defStr)

    def writeDisplayStats(self, rom, displayStats):
               
        for i in range(5):
            rom.seek(self.playersDisplayStatsOffset[i])
            rom.write(strtohex("{0: >3}".format(displayStats[0][i])))

        for i in range(5):
            rom.seek(self.playersDisplayStatsOffset[i]+3)
            rom.write(strtohex("{0: >3}".format(displayStats[1][i])))
            
        for i in range(5):
            rom.seek(self.playersDisplayStatsOffset[i]+6)
            rom.write(strtohex("{0: >3}".format(displayStats[2][i])))

#-------------------------------------------------------------------------------
# utils


def convertint(int_value):
   encoded = format(int_value, 'x')

   length = len(encoded)
   encoded = encoded.zfill(length+length%2)

   return encoded.decode('hex')

def strtohex(string):
    
    string = string.encode('utf8')
    pattern = re.compile(r'\b(' + '|'.join(CHARS.keys()) + r')\b')
    
    result = ''
    
    for c in string:
        hex = pattern.sub(lambda x: CHARS[x.group()], c)
        
        if hex == ' ':
            hex = '\xFF'
        
        result += hex
    
    return result

def hextostr(hex):
    
    pattern = re.compile(r'(' + '|'.join(HEX.keys()) + r')')
    result = pattern.sub(lambda x: HEX[x.group()], hex)    

    return result

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

def create(parent):
    return Frame1(parent)

[wxID_FRAME1, wxID_FRAME1ANGRYSPINTEAM1CTRL1, wxID_FRAME1ANGRYSPINTEAM1CTRL2, 
 wxID_FRAME1ANGRYSPINTEAM1CTRL3, wxID_FRAME1ANGRYSPINTEAM1CTRL4, 
 wxID_FRAME1ANGRYSPINTEAM1CTRL5, wxID_FRAME1ANGRYSPINTEAM2CTRL1, 
 wxID_FRAME1ANGRYSPINTEAM2CTRL2, wxID_FRAME1ANGRYSPINTEAM2CTRL3, 
 wxID_FRAME1ANGRYSPINTEAM2CTRL4, wxID_FRAME1ANGRYSPINTEAM2CTRL5, 
 wxID_FRAME1ANGRYSPINTEAM3CTRL1, wxID_FRAME1ANGRYSPINTEAM3CTRL2, 
 wxID_FRAME1ANGRYSPINTEAM3CTRL3, wxID_FRAME1ANGRYSPINTEAM3CTRL4, 
 wxID_FRAME1ANGRYSPINTEAM3CTRL5, wxID_FRAME1ANGRYSPINTEAM4CTRL1, 
 wxID_FRAME1ANGRYSPINTEAM4CTRL2, wxID_FRAME1ANGRYSPINTEAM4CTRL3, 
 wxID_FRAME1ANGRYSPINTEAM4CTRL4, wxID_FRAME1ANGRYSPINTEAM4CTRL5, 
 wxID_FRAME1ANGRYSPINTEAM5CTRL1, wxID_FRAME1ANGRYSPINTEAM5CTRL2, 
 wxID_FRAME1ANGRYSPINTEAM5CTRL3, wxID_FRAME1ANGRYSPINTEAM5CTRL4, 
 wxID_FRAME1ANGRYSPINTEAM5CTRL5, wxID_FRAME1ANGRYSPINTEAM6CTRL1, 
 wxID_FRAME1ANGRYSPINTEAM6CTRL2, wxID_FRAME1ANGRYSPINTEAM6CTRL3, 
 wxID_FRAME1ANGRYSPINTEAM6CTRL4, wxID_FRAME1ANGRYSPINTEAM6CTRL5, 
 wxID_FRAME1ANGRYSPINTEAM7CTRL1, wxID_FRAME1ANGRYSPINTEAM7CTRL2, 
 wxID_FRAME1ANGRYSPINTEAM7CTRL3, wxID_FRAME1ANGRYSPINTEAM7CTRL4, 
 wxID_FRAME1ANGRYSPINTEAM7CTRL5, wxID_FRAME1ANGRYSPINTEAM8CTRL1, 
 wxID_FRAME1ANGRYSPINTEAM8CTRL2, wxID_FRAME1ANGRYSPINTEAM8CTRL3, 
 wxID_FRAME1ANGRYSPINTEAM8CTRL4, wxID_FRAME1ANGRYSPINTEAM8CTRL5, 
 wxID_FRAME1BUTTON1, wxID_FRAME1BUTTON2, wxID_FRAME1CHECKBOX1, 
 wxID_FRAME1CHOICE1, wxID_FRAME1CHOICE2, wxID_FRAME1CHOICE3, 
 wxID_FRAME1CHOICE4, wxID_FRAME1CHOICE5, wxID_FRAME1DISPLAYDEFTEAM1CTRL1, 
 wxID_FRAME1DISPLAYDEFTEAM1CTRL2, wxID_FRAME1DISPLAYDEFTEAM1CTRL3, 
 wxID_FRAME1DISPLAYDEFTEAM1CTRL4, wxID_FRAME1DISPLAYDEFTEAM1CTRL5, 
 wxID_FRAME1DISPLAYDEFTEAM2CTRL1, wxID_FRAME1DISPLAYDEFTEAM2CTRL2, 
 wxID_FRAME1DISPLAYDEFTEAM2CTRL3, wxID_FRAME1DISPLAYDEFTEAM2CTRL4, 
 wxID_FRAME1DISPLAYDEFTEAM2CTRL5, wxID_FRAME1DISPLAYDEFTEAM3CTRL1, 
 wxID_FRAME1DISPLAYDEFTEAM3CTRL2, wxID_FRAME1DISPLAYDEFTEAM3CTRL3, 
 wxID_FRAME1DISPLAYDEFTEAM3CTRL4, wxID_FRAME1DISPLAYDEFTEAM3CTRL5, 
 wxID_FRAME1DISPLAYDEFTEAM4CTRL1, wxID_FRAME1DISPLAYDEFTEAM4CTRL2, 
 wxID_FRAME1DISPLAYDEFTEAM4CTRL3, wxID_FRAME1DISPLAYDEFTEAM4CTRL4, 
 wxID_FRAME1DISPLAYDEFTEAM4CTRL5, wxID_FRAME1DISPLAYDEFTEAM5CTRL1, 
 wxID_FRAME1DISPLAYDEFTEAM5CTRL2, wxID_FRAME1DISPLAYDEFTEAM5CTRL3, 
 wxID_FRAME1DISPLAYDEFTEAM5CTRL4, wxID_FRAME1DISPLAYDEFTEAM5CTRL5, 
 wxID_FRAME1DISPLAYDEFTEAM6CTRL1, wxID_FRAME1DISPLAYDEFTEAM6CTRL2, 
 wxID_FRAME1DISPLAYDEFTEAM6CTRL3, wxID_FRAME1DISPLAYDEFTEAM6CTRL4, 
 wxID_FRAME1DISPLAYDEFTEAM6CTRL5, wxID_FRAME1DISPLAYDEFTEAM7CTRL1, 
 wxID_FRAME1DISPLAYDEFTEAM7CTRL2, wxID_FRAME1DISPLAYDEFTEAM7CTRL3, 
 wxID_FRAME1DISPLAYDEFTEAM7CTRL4, wxID_FRAME1DISPLAYDEFTEAM7CTRL5, 
 wxID_FRAME1DISPLAYDEFTEAM8CTRL1, wxID_FRAME1DISPLAYDEFTEAM8CTRL2, 
 wxID_FRAME1DISPLAYDEFTEAM8CTRL3, wxID_FRAME1DISPLAYDEFTEAM8CTRL4, 
 wxID_FRAME1DISPLAYDEFTEAM8CTRL5, wxID_FRAME1DISPLAYPOWTEAM1CTRL1, 
 wxID_FRAME1DISPLAYPOWTEAM1CTRL2, wxID_FRAME1DISPLAYPOWTEAM1CTRL3, 
 wxID_FRAME1DISPLAYPOWTEAM1CTRL4, wxID_FRAME1DISPLAYPOWTEAM1CTRL5, 
 wxID_FRAME1DISPLAYPOWTEAM2CTRL1, wxID_FRAME1DISPLAYPOWTEAM2CTRL2, 
 wxID_FRAME1DISPLAYPOWTEAM2CTRL3, wxID_FRAME1DISPLAYPOWTEAM2CTRL4, 
 wxID_FRAME1DISPLAYPOWTEAM2CTRL5, wxID_FRAME1DISPLAYPOWTEAM3CTRL1, 
 wxID_FRAME1DISPLAYPOWTEAM3CTRL2, wxID_FRAME1DISPLAYPOWTEAM3CTRL3, 
 wxID_FRAME1DISPLAYPOWTEAM3CTRL4, wxID_FRAME1DISPLAYPOWTEAM3CTRL5, 
 wxID_FRAME1DISPLAYPOWTEAM4CTRL1, wxID_FRAME1DISPLAYPOWTEAM4CTRL2, 
 wxID_FRAME1DISPLAYPOWTEAM4CTRL3, wxID_FRAME1DISPLAYPOWTEAM4CTRL4, 
 wxID_FRAME1DISPLAYPOWTEAM4CTRL5, wxID_FRAME1DISPLAYPOWTEAM5CTRL1, 
 wxID_FRAME1DISPLAYPOWTEAM5CTRL2, wxID_FRAME1DISPLAYPOWTEAM5CTRL3, 
 wxID_FRAME1DISPLAYPOWTEAM5CTRL4, wxID_FRAME1DISPLAYPOWTEAM5CTRL5, 
 wxID_FRAME1DISPLAYPOWTEAM6CTRL1, wxID_FRAME1DISPLAYPOWTEAM6CTRL2, 
 wxID_FRAME1DISPLAYPOWTEAM6CTRL3, wxID_FRAME1DISPLAYPOWTEAM6CTRL4, 
 wxID_FRAME1DISPLAYPOWTEAM6CTRL5, wxID_FRAME1DISPLAYPOWTEAM7CTRL1, 
 wxID_FRAME1DISPLAYPOWTEAM7CTRL2, wxID_FRAME1DISPLAYPOWTEAM7CTRL3, 
 wxID_FRAME1DISPLAYPOWTEAM7CTRL4, wxID_FRAME1DISPLAYPOWTEAM7CTRL5, 
 wxID_FRAME1DISPLAYPOWTEAM8CTRL1, wxID_FRAME1DISPLAYPOWTEAM8CTRL2, 
 wxID_FRAME1DISPLAYPOWTEAM8CTRL3, wxID_FRAME1DISPLAYPOWTEAM8CTRL4, 
 wxID_FRAME1DISPLAYPOWTEAM8CTRL5, wxID_FRAME1DISPLAYSPDTEAM1CTRL1, 
 wxID_FRAME1DISPLAYSPDTEAM1CTRL2, wxID_FRAME1DISPLAYSPDTEAM1CTRL3, 
 wxID_FRAME1DISPLAYSPDTEAM1CTRL4, wxID_FRAME1DISPLAYSPDTEAM1CTRL5, 
 wxID_FRAME1DISPLAYSPDTEAM2CTRL1, wxID_FRAME1DISPLAYSPDTEAM2CTRL2, 
 wxID_FRAME1DISPLAYSPDTEAM2CTRL3, wxID_FRAME1DISPLAYSPDTEAM2CTRL4, 
 wxID_FRAME1DISPLAYSPDTEAM2CTRL5, wxID_FRAME1DISPLAYSPDTEAM3CTRL1, 
 wxID_FRAME1DISPLAYSPDTEAM3CTRL2, wxID_FRAME1DISPLAYSPDTEAM3CTRL3, 
 wxID_FRAME1DISPLAYSPDTEAM3CTRL4, wxID_FRAME1DISPLAYSPDTEAM3CTRL5, 
 wxID_FRAME1DISPLAYSPDTEAM4CTRL1, wxID_FRAME1DISPLAYSPDTEAM4CTRL2, 
 wxID_FRAME1DISPLAYSPDTEAM4CTRL3, wxID_FRAME1DISPLAYSPDTEAM4CTRL4, 
 wxID_FRAME1DISPLAYSPDTEAM4CTRL5, wxID_FRAME1DISPLAYSPDTEAM5CTRL1, 
 wxID_FRAME1DISPLAYSPDTEAM5CTRL2, wxID_FRAME1DISPLAYSPDTEAM5CTRL3, 
 wxID_FRAME1DISPLAYSPDTEAM5CTRL4, wxID_FRAME1DISPLAYSPDTEAM5CTRL5, 
 wxID_FRAME1DISPLAYSPDTEAM6CTRL1, wxID_FRAME1DISPLAYSPDTEAM6CTRL2, 
 wxID_FRAME1DISPLAYSPDTEAM6CTRL3, wxID_FRAME1DISPLAYSPDTEAM6CTRL4, 
 wxID_FRAME1DISPLAYSPDTEAM6CTRL5, wxID_FRAME1DISPLAYSPDTEAM7CTRL1, 
 wxID_FRAME1DISPLAYSPDTEAM7CTRL2, wxID_FRAME1DISPLAYSPDTEAM7CTRL3, 
 wxID_FRAME1DISPLAYSPDTEAM7CTRL4, wxID_FRAME1DISPLAYSPDTEAM7CTRL5, 
 wxID_FRAME1DISPLAYSPDTEAM8CTRL1, wxID_FRAME1DISPLAYSPDTEAM8CTRL2, 
 wxID_FRAME1DISPLAYSPDTEAM8CTRL3, wxID_FRAME1DISPLAYSPDTEAM8CTRL4, 
 wxID_FRAME1DISPLAYSPDTEAM8CTRL5, wxID_FRAME1FALLTYPECHOICE, 
 wxID_FRAME1FLYHITSPINCTRL, wxID_FRAME1FLYSHOOTSPINCTRL, wxID_FRAME1MINCTRL1, 
 wxID_FRAME1MPOWERSPINTEAM1CTRL1, wxID_FRAME1MPOWERSPINTEAM1CTRL2, 
 wxID_FRAME1MPOWERSPINTEAM1CTRL3, wxID_FRAME1MPOWERSPINTEAM1CTRL4, 
 wxID_FRAME1MPOWERSPINTEAM1CTRL5, wxID_FRAME1MPOWERSPINTEAM2CTRL1, 
 wxID_FRAME1MPOWERSPINTEAM2CTRL2, wxID_FRAME1MPOWERSPINTEAM2CTRL3, 
 wxID_FRAME1MPOWERSPINTEAM2CTRL4, wxID_FRAME1MPOWERSPINTEAM2CTRL5, 
 wxID_FRAME1MPOWERSPINTEAM3CTRL1, wxID_FRAME1MPOWERSPINTEAM3CTRL2, 
 wxID_FRAME1MPOWERSPINTEAM3CTRL3, wxID_FRAME1MPOWERSPINTEAM3CTRL4, 
 wxID_FRAME1MPOWERSPINTEAM3CTRL5, wxID_FRAME1MPOWERSPINTEAM4CTRL1, 
 wxID_FRAME1MPOWERSPINTEAM4CTRL2, wxID_FRAME1MPOWERSPINTEAM4CTRL3, 
 wxID_FRAME1MPOWERSPINTEAM4CTRL4, wxID_FRAME1MPOWERSPINTEAM4CTRL5, 
 wxID_FRAME1MPOWERSPINTEAM5CTRL1, wxID_FRAME1MPOWERSPINTEAM5CTRL2, 
 wxID_FRAME1MPOWERSPINTEAM5CTRL3, wxID_FRAME1MPOWERSPINTEAM5CTRL4, 
 wxID_FRAME1MPOWERSPINTEAM5CTRL5, wxID_FRAME1MPOWERSPINTEAM6CTRL1, 
 wxID_FRAME1MPOWERSPINTEAM6CTRL2, wxID_FRAME1MPOWERSPINTEAM6CTRL3, 
 wxID_FRAME1MPOWERSPINTEAM6CTRL4, wxID_FRAME1MPOWERSPINTEAM6CTRL5, 
 wxID_FRAME1MPOWERSPINTEAM7CTRL1, wxID_FRAME1MPOWERSPINTEAM7CTRL2, 
 wxID_FRAME1MPOWERSPINTEAM7CTRL3, wxID_FRAME1MPOWERSPINTEAM7CTRL4, 
 wxID_FRAME1MPOWERSPINTEAM7CTRL5, wxID_FRAME1MPOWERSPINTEAM8CTRL1, 
 wxID_FRAME1MPOWERSPINTEAM8CTRL2, wxID_FRAME1MPOWERSPINTEAM8CTRL3, 
 wxID_FRAME1MPOWERSPINTEAM8CTRL4, wxID_FRAME1MPOWERSPINTEAM8CTRL5, 
 wxID_FRAME1NOTEBOOK1, wxID_FRAME1PANEL1, wxID_FRAME1PANEL2, 
 wxID_FRAME1PANEL3, wxID_FRAME1PANEL4, wxID_FRAME1PANEL5, wxID_FRAME1PANEL6, 
 wxID_FRAME1PANEL7, wxID_FRAME1PANEL8, wxID_FRAME1PANEL9, wxID_FRAME1SECCTRL1, 
 wxID_FRAME1SHOOTCTRL1, wxID_FRAME1SHOOTTEAM1CHOICE1, 
 wxID_FRAME1SHOOTTEAM1CHOICE2, wxID_FRAME1SHOOTTEAM1CHOICE3, 
 wxID_FRAME1SHOOTTEAM1CHOICE4, wxID_FRAME1SHOOTTEAM1CHOICE5, 
 wxID_FRAME1SHOOTTEAM2CHOICE1, wxID_FRAME1SHOOTTEAM2CHOICE2, 
 wxID_FRAME1SHOOTTEAM2CHOICE3, wxID_FRAME1SHOOTTEAM2CHOICE4, 
 wxID_FRAME1SHOOTTEAM2CHOICE5, wxID_FRAME1SHOOTTEAM3CHOICE1, 
 wxID_FRAME1SHOOTTEAM3CHOICE2, wxID_FRAME1SHOOTTEAM3CHOICE3, 
 wxID_FRAME1SHOOTTEAM3CHOICE4, wxID_FRAME1SHOOTTEAM3CHOICE5, 
 wxID_FRAME1SHOOTTEAM4CHOICE1, wxID_FRAME1SHOOTTEAM4CHOICE2, 
 wxID_FRAME1SHOOTTEAM4CHOICE3, wxID_FRAME1SHOOTTEAM4CHOICE4, 
 wxID_FRAME1SHOOTTEAM4CHOICE5, wxID_FRAME1SHOOTTEAM5CHOICE1, 
 wxID_FRAME1SHOOTTEAM5CHOICE2, wxID_FRAME1SHOOTTEAM5CHOICE3, 
 wxID_FRAME1SHOOTTEAM5CHOICE4, wxID_FRAME1SHOOTTEAM5CHOICE5, 
 wxID_FRAME1SHOOTTEAM6CHOICE1, wxID_FRAME1SHOOTTEAM6CHOICE2, 
 wxID_FRAME1SHOOTTEAM6CHOICE3, wxID_FRAME1SHOOTTEAM6CHOICE4, 
 wxID_FRAME1SHOOTTEAM6CHOICE5, wxID_FRAME1SHOOTTEAM7CHOICE1, 
 wxID_FRAME1SHOOTTEAM7CHOICE2, wxID_FRAME1SHOOTTEAM7CHOICE3, 
 wxID_FRAME1SHOOTTEAM7CHOICE4, wxID_FRAME1SHOOTTEAM7CHOICE5, 
 wxID_FRAME1SHOOTTEAM8CHOICE1, wxID_FRAME1SHOOTTEAM8CHOICE2, 
 wxID_FRAME1SHOOTTEAM8CHOICE3, wxID_FRAME1SHOOTTEAM8CHOICE4, 
 wxID_FRAME1SHOOTTEAM8CHOICE5, wxID_FRAME1SPEEDSPINTEAM1CTRL1, 
 wxID_FRAME1SPEEDSPINTEAM1CTRL2, wxID_FRAME1SPEEDSPINTEAM1CTRL3, 
 wxID_FRAME1SPEEDSPINTEAM1CTRL4, wxID_FRAME1SPEEDSPINTEAM1CTRL5, 
 wxID_FRAME1SPEEDSPINTEAM2CTRL1, wxID_FRAME1SPEEDSPINTEAM2CTRL2, 
 wxID_FRAME1SPEEDSPINTEAM2CTRL3, wxID_FRAME1SPEEDSPINTEAM2CTRL4, 
 wxID_FRAME1SPEEDSPINTEAM2CTRL5, wxID_FRAME1SPEEDSPINTEAM3CTRL1, 
 wxID_FRAME1SPEEDSPINTEAM3CTRL2, wxID_FRAME1SPEEDSPINTEAM3CTRL3, 
 wxID_FRAME1SPEEDSPINTEAM3CTRL4, wxID_FRAME1SPEEDSPINTEAM3CTRL5, 
 wxID_FRAME1SPEEDSPINTEAM4CTRL1, wxID_FRAME1SPEEDSPINTEAM4CTRL2, 
 wxID_FRAME1SPEEDSPINTEAM4CTRL3, wxID_FRAME1SPEEDSPINTEAM4CTRL4, 
 wxID_FRAME1SPEEDSPINTEAM4CTRL5, wxID_FRAME1SPEEDSPINTEAM5CTRL1, 
 wxID_FRAME1SPEEDSPINTEAM5CTRL2, wxID_FRAME1SPEEDSPINTEAM5CTRL3, 
 wxID_FRAME1SPEEDSPINTEAM5CTRL4, wxID_FRAME1SPEEDSPINTEAM5CTRL5, 
 wxID_FRAME1SPEEDSPINTEAM6CTRL1, wxID_FRAME1SPEEDSPINTEAM6CTRL2, 
 wxID_FRAME1SPEEDSPINTEAM6CTRL3, wxID_FRAME1SPEEDSPINTEAM6CTRL4, 
 wxID_FRAME1SPEEDSPINTEAM6CTRL5, wxID_FRAME1SPEEDSPINTEAM7CTRL1, 
 wxID_FRAME1SPEEDSPINTEAM7CTRL2, wxID_FRAME1SPEEDSPINTEAM7CTRL3, 
 wxID_FRAME1SPEEDSPINTEAM7CTRL4, wxID_FRAME1SPEEDSPINTEAM7CTRL5, 
 wxID_FRAME1SPEEDSPINTEAM8CTRL1, wxID_FRAME1SPEEDSPINTEAM8CTRL2, 
 wxID_FRAME1SPEEDSPINTEAM8CTRL3, wxID_FRAME1SPEEDSPINTEAM8CTRL4, 
 wxID_FRAME1SPEEDSPINTEAM8CTRL5, wxID_FRAME1SPOWERSPINTEAM1CTRL1, 
 wxID_FRAME1SPOWERSPINTEAM1CTRL2, wxID_FRAME1SPOWERSPINTEAM1CTRL3, 
 wxID_FRAME1SPOWERSPINTEAM1CTRL4, wxID_FRAME1SPOWERSPINTEAM1CTRL5, 
 wxID_FRAME1SPOWERSPINTEAM2CTRL1, wxID_FRAME1SPOWERSPINTEAM2CTRL2, 
 wxID_FRAME1SPOWERSPINTEAM2CTRL3, wxID_FRAME1SPOWERSPINTEAM2CTRL4, 
 wxID_FRAME1SPOWERSPINTEAM2CTRL5, wxID_FRAME1SPOWERSPINTEAM3CTRL1, 
 wxID_FRAME1SPOWERSPINTEAM3CTRL2, wxID_FRAME1SPOWERSPINTEAM3CTRL3, 
 wxID_FRAME1SPOWERSPINTEAM3CTRL4, wxID_FRAME1SPOWERSPINTEAM3CTRL5, 
 wxID_FRAME1SPOWERSPINTEAM4CTRL1, wxID_FRAME1SPOWERSPINTEAM4CTRL2, 
 wxID_FRAME1SPOWERSPINTEAM4CTRL3, wxID_FRAME1SPOWERSPINTEAM4CTRL4, 
 wxID_FRAME1SPOWERSPINTEAM4CTRL5, wxID_FRAME1SPOWERSPINTEAM5CTRL1, 
 wxID_FRAME1SPOWERSPINTEAM5CTRL2, wxID_FRAME1SPOWERSPINTEAM5CTRL3, 
 wxID_FRAME1SPOWERSPINTEAM5CTRL4, wxID_FRAME1SPOWERSPINTEAM5CTRL5, 
 wxID_FRAME1SPOWERSPINTEAM6CTRL1, wxID_FRAME1SPOWERSPINTEAM6CTRL2, 
 wxID_FRAME1SPOWERSPINTEAM6CTRL3, wxID_FRAME1SPOWERSPINTEAM6CTRL4, 
 wxID_FRAME1SPOWERSPINTEAM6CTRL5, wxID_FRAME1SPOWERSPINTEAM7CTRL1, 
 wxID_FRAME1SPOWERSPINTEAM7CTRL2, wxID_FRAME1SPOWERSPINTEAM7CTRL3, 
 wxID_FRAME1SPOWERSPINTEAM7CTRL4, wxID_FRAME1SPOWERSPINTEAM7CTRL5, 
 wxID_FRAME1SPOWERSPINTEAM8CTRL1, wxID_FRAME1SPOWERSPINTEAM8CTRL2, 
 wxID_FRAME1SPOWERSPINTEAM8CTRL3, wxID_FRAME1SPOWERSPINTEAM8CTRL4, 
 wxID_FRAME1SPOWERSPINTEAM8CTRL5, wxID_FRAME1STATICTEXT1, 
 wxID_FRAME1STATICTEXT10, wxID_FRAME1STATICTEXT100, wxID_FRAME1STATICTEXT101, 
 wxID_FRAME1STATICTEXT102, wxID_FRAME1STATICTEXT103, wxID_FRAME1STATICTEXT104, 
 wxID_FRAME1STATICTEXT105, wxID_FRAME1STATICTEXT106, wxID_FRAME1STATICTEXT107, 
 wxID_FRAME1STATICTEXT108, wxID_FRAME1STATICTEXT109, wxID_FRAME1STATICTEXT11, 
 wxID_FRAME1STATICTEXT110, wxID_FRAME1STATICTEXT111, wxID_FRAME1STATICTEXT112, 
 wxID_FRAME1STATICTEXT113, wxID_FRAME1STATICTEXT114, wxID_FRAME1STATICTEXT115, 
 wxID_FRAME1STATICTEXT116, wxID_FRAME1STATICTEXT117, wxID_FRAME1STATICTEXT118, 
 wxID_FRAME1STATICTEXT119, wxID_FRAME1STATICTEXT12, wxID_FRAME1STATICTEXT120, 
 wxID_FRAME1STATICTEXT121, wxID_FRAME1STATICTEXT13, wxID_FRAME1STATICTEXT14, 
 wxID_FRAME1STATICTEXT15, wxID_FRAME1STATICTEXT2, wxID_FRAME1STATICTEXT21, 
 wxID_FRAME1STATICTEXT22, wxID_FRAME1STATICTEXT23, wxID_FRAME1STATICTEXT24, 
 wxID_FRAME1STATICTEXT25, wxID_FRAME1STATICTEXT26, wxID_FRAME1STATICTEXT27, 
 wxID_FRAME1STATICTEXT28, wxID_FRAME1STATICTEXT29, wxID_FRAME1STATICTEXT3, 
 wxID_FRAME1STATICTEXT30, wxID_FRAME1STATICTEXT31, wxID_FRAME1STATICTEXT32, 
 wxID_FRAME1STATICTEXT33, wxID_FRAME1STATICTEXT34, wxID_FRAME1STATICTEXT35, 
 wxID_FRAME1STATICTEXT36, wxID_FRAME1STATICTEXT37, wxID_FRAME1STATICTEXT38, 
 wxID_FRAME1STATICTEXT39, wxID_FRAME1STATICTEXT4, wxID_FRAME1STATICTEXT40, 
 wxID_FRAME1STATICTEXT41, wxID_FRAME1STATICTEXT42, wxID_FRAME1STATICTEXT43, 
 wxID_FRAME1STATICTEXT44, wxID_FRAME1STATICTEXT45, wxID_FRAME1STATICTEXT46, 
 wxID_FRAME1STATICTEXT47, wxID_FRAME1STATICTEXT48, wxID_FRAME1STATICTEXT49, 
 wxID_FRAME1STATICTEXT5, wxID_FRAME1STATICTEXT50, wxID_FRAME1STATICTEXT51, 
 wxID_FRAME1STATICTEXT52, wxID_FRAME1STATICTEXT53, wxID_FRAME1STATICTEXT54, 
 wxID_FRAME1STATICTEXT56, wxID_FRAME1STATICTEXT57, wxID_FRAME1STATICTEXT58, 
 wxID_FRAME1STATICTEXT59, wxID_FRAME1STATICTEXT6, wxID_FRAME1STATICTEXT60, 
 wxID_FRAME1STATICTEXT61, wxID_FRAME1STATICTEXT62, wxID_FRAME1STATICTEXT63, 
 wxID_FRAME1STATICTEXT64, wxID_FRAME1STATICTEXT65, wxID_FRAME1STATICTEXT66, 
 wxID_FRAME1STATICTEXT67, wxID_FRAME1STATICTEXT68, wxID_FRAME1STATICTEXT69, 
 wxID_FRAME1STATICTEXT7, wxID_FRAME1STATICTEXT70, wxID_FRAME1STATICTEXT71, 
 wxID_FRAME1STATICTEXT72, wxID_FRAME1STATICTEXT73, wxID_FRAME1STATICTEXT74, 
 wxID_FRAME1STATICTEXT75, wxID_FRAME1STATICTEXT76, wxID_FRAME1STATICTEXT77, 
 wxID_FRAME1STATICTEXT78, wxID_FRAME1STATICTEXT79, wxID_FRAME1STATICTEXT8, 
 wxID_FRAME1STATICTEXT80, wxID_FRAME1STATICTEXT81, wxID_FRAME1STATICTEXT82, 
 wxID_FRAME1STATICTEXT83, wxID_FRAME1STATICTEXT84, wxID_FRAME1STATICTEXT85, 
 wxID_FRAME1STATICTEXT86, wxID_FRAME1STATICTEXT87, wxID_FRAME1STATICTEXT88, 
 wxID_FRAME1STATICTEXT89, wxID_FRAME1STATICTEXT9, wxID_FRAME1STATICTEXT90, 
 wxID_FRAME1STATICTEXT91, wxID_FRAME1STATICTEXT92, wxID_FRAME1STATICTEXT93, 
 wxID_FRAME1STATICTEXT94, wxID_FRAME1STATICTEXT95, wxID_FRAME1STATICTEXT96, 
 wxID_FRAME1STATICTEXT97, wxID_FRAME1STATICTEXT98, wxID_FRAME1STATICTEXT99, 
 wxID_FRAME1TEAM1ATTACKSPINCTRL1, wxID_FRAME1TEAM1DEFENSESPINCTRL1, 
 wxID_FRAME1TEAM1PLAYER1CTRL, wxID_FRAME1TEAM1PLAYER2CTRL, 
 wxID_FRAME1TEAM1PLAYER3CTRL, wxID_FRAME1TEAM1PLAYER4CTRL, 
 wxID_FRAME1TEAM1PLAYER5CTRL, wxID_FRAME1TEAM2ATTACKSPINCTRL1, 
 wxID_FRAME1TEAM2DEFENSESPINCTRL1, wxID_FRAME1TEAM2PLAYER1CTRL, 
 wxID_FRAME1TEAM2PLAYER2CTRL, wxID_FRAME1TEAM2PLAYER3CTRL, 
 wxID_FRAME1TEAM2PLAYER4CTRL, wxID_FRAME1TEAM2PLAYER5CTRL, 
 wxID_FRAME1TEAM3ATTACKSPINCTRL1, wxID_FRAME1TEAM3DEFENSESPINCTRL1, 
 wxID_FRAME1TEAM3PLAYER1CTRL, wxID_FRAME1TEAM3PLAYER2CTRL, 
 wxID_FRAME1TEAM3PLAYER3CTRL, wxID_FRAME1TEAM3PLAYER4CTRL, 
 wxID_FRAME1TEAM3PLAYER5CTRL, wxID_FRAME1TEAM4ATTACKSPINCTRL1, 
 wxID_FRAME1TEAM4DEFENSESPINCTRL1, wxID_FRAME1TEAM4PLAYER1CTRL, 
 wxID_FRAME1TEAM4PLAYER2CTRL, wxID_FRAME1TEAM4PLAYER3CTRL, 
 wxID_FRAME1TEAM4PLAYER4CTRL, wxID_FRAME1TEAM4PLAYER5CTRL, 
 wxID_FRAME1TEAM5ATTACKSPINCTRL1, wxID_FRAME1TEAM5DEFENSESPINCTRL1, 
 wxID_FRAME1TEAM5PLAYER1CTRL, wxID_FRAME1TEAM5PLAYER2CTRL, 
 wxID_FRAME1TEAM5PLAYER3CTRL, wxID_FRAME1TEAM5PLAYER4CTRL, 
 wxID_FRAME1TEAM5PLAYER5CTRL, wxID_FRAME1TEAM6ATTACKSPINCTRL1, 
 wxID_FRAME1TEAM6DEFENSESPINCTRL1, wxID_FRAME1TEAM6PLAYER1CTRL, 
 wxID_FRAME1TEAM6PLAYER2CTRL, wxID_FRAME1TEAM6PLAYER3CTRL, 
 wxID_FRAME1TEAM6PLAYER4CTRL, wxID_FRAME1TEAM6PLAYER5CTRL, 
 wxID_FRAME1TEAM7ATTACKSPINCTRL1, wxID_FRAME1TEAM7DEFENSESPINCTRL1, 
 wxID_FRAME1TEAM7PLAYER1CTRL, wxID_FRAME1TEAM7PLAYER2CTRL, 
 wxID_FRAME1TEAM7PLAYER3CTRL, wxID_FRAME1TEAM7PLAYER4CTRL, 
 wxID_FRAME1TEAM7PLAYER5CTRL, wxID_FRAME1TEAM8ATTACKSPINCTRL1, 
 wxID_FRAME1TEAM8DEFENSESPINCTRL1, wxID_FRAME1TEAM8PLAYER1CTRL, 
 wxID_FRAME1TEAM8PLAYER2CTRL, wxID_FRAME1TEAM8PLAYER3CTRL, 
 wxID_FRAME1TEAM8PLAYER4CTRL, wxID_FRAME1TEAM8PLAYER5CTRL, 
 wxID_FRAME1TEAMNAMECTRL1, wxID_FRAME1TEAMNAMECTRL2, wxID_FRAME1TEAMNAMECTRL3, 
 wxID_FRAME1TEAMNAMECTRL4, wxID_FRAME1TEAMNAMECTRL5, wxID_FRAME1TEAMNAMECTRL6, 
 wxID_FRAME1TEAMNAMECTRL7, wxID_FRAME1TEAMNAMECTRL8, 
 wxID_FRAME1WEIGHTSPINTEAM1CTRL1, wxID_FRAME1WEIGHTSPINTEAM1CTRL2, 
 wxID_FRAME1WEIGHTSPINTEAM1CTRL3, wxID_FRAME1WEIGHTSPINTEAM1CTRL4, 
 wxID_FRAME1WEIGHTSPINTEAM1CTRL5, wxID_FRAME1WEIGHTSPINTEAM2CTRL1, 
 wxID_FRAME1WEIGHTSPINTEAM2CTRL2, wxID_FRAME1WEIGHTSPINTEAM2CTRL3, 
 wxID_FRAME1WEIGHTSPINTEAM2CTRL4, wxID_FRAME1WEIGHTSPINTEAM2CTRL5, 
 wxID_FRAME1WEIGHTSPINTEAM3CTRL1, wxID_FRAME1WEIGHTSPINTEAM3CTRL2, 
 wxID_FRAME1WEIGHTSPINTEAM3CTRL3, wxID_FRAME1WEIGHTSPINTEAM3CTRL4, 
 wxID_FRAME1WEIGHTSPINTEAM3CTRL5, wxID_FRAME1WEIGHTSPINTEAM4CTRL1, 
 wxID_FRAME1WEIGHTSPINTEAM4CTRL2, wxID_FRAME1WEIGHTSPINTEAM4CTRL3, 
 wxID_FRAME1WEIGHTSPINTEAM4CTRL4, wxID_FRAME1WEIGHTSPINTEAM4CTRL5, 
 wxID_FRAME1WEIGHTSPINTEAM5CTRL1, wxID_FRAME1WEIGHTSPINTEAM5CTRL2, 
 wxID_FRAME1WEIGHTSPINTEAM5CTRL3, wxID_FRAME1WEIGHTSPINTEAM5CTRL4, 
 wxID_FRAME1WEIGHTSPINTEAM5CTRL5, wxID_FRAME1WEIGHTSPINTEAM6CTRL1, 
 wxID_FRAME1WEIGHTSPINTEAM6CTRL2, wxID_FRAME1WEIGHTSPINTEAM6CTRL3, 
 wxID_FRAME1WEIGHTSPINTEAM6CTRL4, wxID_FRAME1WEIGHTSPINTEAM6CTRL5, 
 wxID_FRAME1WEIGHTSPINTEAM7CTRL1, wxID_FRAME1WEIGHTSPINTEAM7CTRL2, 
 wxID_FRAME1WEIGHTSPINTEAM7CTRL3, wxID_FRAME1WEIGHTSPINTEAM7CTRL4, 
 wxID_FRAME1WEIGHTSPINTEAM7CTRL5, wxID_FRAME1WEIGHTSPINTEAM8CTRL1, 
 wxID_FRAME1WEIGHTSPINTEAM8CTRL2, wxID_FRAME1WEIGHTSPINTEAM8CTRL3, 
 wxID_FRAME1WEIGHTSPINTEAM8CTRL4, wxID_FRAME1WEIGHTSPINTEAM8CTRL5, 
] = [wx.NewId() for _init_ctrls in range(564)]

class Frame1(wx.Frame):
    def _init_coll_notebook1_Pages(self, parent):
        # generated method, don't edit

        parent.AddPage(imageId=-1, page=self.panel2, select=True,
              text=u'Team 1')
        parent.AddPage(imageId=-1, page=self.panel3, select=False,
              text=u'Team 2')
        parent.AddPage(imageId=-1, page=self.panel4, select=False,
              text=u'Team 3')
        parent.AddPage(imageId=-1, page=self.panel5, select=False,
              text=u'Team 4')
        parent.AddPage(imageId=-1, page=self.panel6, select=False,
              text=u'Team 5')
        parent.AddPage(imageId=-1, page=self.panel7, select=False,
              text=u'Team 6')
        parent.AddPage(imageId=-1, page=self.panel8, select=False,
              text=u'Team 7')
        parent.AddPage(imageId=-1, page=self.panel9, select=False,
              text=u'Team 8')

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME1, name='', parent=prnt,
              pos=wx.Point(328, 343), size=wx.Size(909, 368),
              style=wx.DEFAULT_FRAME_STYLE, title=u'TurBo Hockey Editor 3000')
        self.SetClientSize(wx.Size(901, 341))
        self.SetIcon(wx.Icon(u"icon.ico",wx.BITMAP_TYPE_ICO))

        self.panel1 = wx.Panel(id=wxID_FRAME1PANEL1, name='panel1', parent=self,
              pos=wx.Point(0, 0), size=wx.Size(901, 341),
              style=wx.TAB_TRAVERSAL)
        self.panel1.SetToolTipString(u'')

        self.staticText1 = wx.StaticText(id=wxID_FRAME1STATICTEXT1,
              label=u'Time', name='staticText1', parent=self.panel1,
              pos=wx.Point(32, 24), size=wx.Size(29, 14), style=0)

        self.minCtrl1 = wx.TextCtrl(id=wxID_FRAME1MINCTRL1, name=u'minCtrl1',
              parent=self.panel1, pos=wx.Point(16, 40), size=wx.Size(24, 21),
              style=0, value=u'0')
        self.minCtrl1.SetLabelText(u'0')
        self.minCtrl1.SetMaxLength(1)
        self.minCtrl1.SetToolTipString(u'Minutes')
        self.minCtrl1.Bind(wx.EVT_TEXT, self.OnMinCtrl1Text,
              id=wxID_FRAME1MINCTRL1)

        self.secCtrl1 = wx.TextCtrl(id=wxID_FRAME1SECCTRL1, name=u'secCtrl1',
              parent=self.panel1, pos=wx.Point(40, 40), size=wx.Size(24, 21),
              style=0, value=u'0')
        self.secCtrl1.SetLabelText(u'0')
        self.secCtrl1.SetMaxLength(1)
        self.secCtrl1.SetToolTipString(u'Seconds')
        self.secCtrl1.SetInsertionPoint(1)
        self.secCtrl1.SetHelpText(u'')
        self.secCtrl1.Bind(wx.EVT_TEXT, self.OnSecCtrl1Text,
              id=wxID_FRAME1SECCTRL1)

        self.staticText2 = wx.StaticText(id=wxID_FRAME1STATICTEXT2,
              label=u'Charge Time', name='staticText2', parent=self.panel1,
              pos=wx.Point(80, 24), size=wx.Size(60, 14), style=0)

        self.shootCtrl1 = wx.TextCtrl(id=wxID_FRAME1SHOOTCTRL1,
              name=u'shootCtrl1', parent=self.panel1, pos=wx.Point(88, 40),
              size=wx.Size(32, 21), style=0, value=u'0')
        self.shootCtrl1.SetLabelText(u'0')
        self.shootCtrl1.SetToolTipString(u'Super shoot time')
        self.shootCtrl1.SetMaxLength(3)
        self.shootCtrl1.Bind(wx.EVT_TEXT, self.OnShootCtrl1Text,
              id=wxID_FRAME1SHOOTCTRL1)

        self.staticText3 = wx.StaticText(id=wxID_FRAME1STATICTEXT3,
              label=u'Field 1', name='staticText3', parent=self.panel1,
              pos=wx.Point(160, 24), size=wx.Size(31, 14), style=0)

        self.staticText4 = wx.StaticText(id=wxID_FRAME1STATICTEXT4,
              label=u'Field 2', name='staticText4', parent=self.panel1,
              pos=wx.Point(216, 24), size=wx.Size(31, 14), style=0)

        self.staticText5 = wx.StaticText(id=wxID_FRAME1STATICTEXT5,
              label=u'Field 3', name='staticText5', parent=self.panel1,
              pos=wx.Point(272, 24), size=wx.Size(31, 14), style=0)

        self.staticText6 = wx.StaticText(id=wxID_FRAME1STATICTEXT6,
              label=u'Field 4', name='staticText6', parent=self.panel1,
              pos=wx.Point(328, 24), size=wx.Size(31, 14), style=0)

        self.choice1 = wx.Choice(choices=[], id=wxID_FRAME1CHOICE1,
              name='choice1', parent=self.panel1, pos=wx.Point(376, 40),
              size=wx.Size(48, 21), style=0)
        self.choice1.SetToolTipString(u'Field 5 music theme')
        self.choice1.Bind(wx.EVT_CHOICE, self.OnChoice1Choice,
              id=wxID_FRAME1CHOICE1)

        self.choice2 = wx.Choice(choices=[], id=wxID_FRAME1CHOICE2,
              name='choice2', parent=self.panel1, pos=wx.Point(208, 40),
              size=wx.Size(48, 21), style=0)
        self.choice2.SetToolTipString(u'Field 2 music theme')
        self.choice2.Bind(wx.EVT_CHOICE, self.OnChoice2Choice,
              id=wxID_FRAME1CHOICE2)

        self.choice3 = wx.Choice(choices=[], id=wxID_FRAME1CHOICE3,
              name='choice3', parent=self.panel1, pos=wx.Point(264, 40),
              size=wx.Size(48, 21), style=0)
        self.choice3.SetToolTipString(u'Field 3 music theme')
        self.choice3.Bind(wx.EVT_CHOICE, self.OnChoice3Choice,
              id=wxID_FRAME1CHOICE3)

        self.choice4 = wx.Choice(choices=[], id=wxID_FRAME1CHOICE4,
              name='choice4', parent=self.panel1, pos=wx.Point(320, 40),
              size=wx.Size(48, 21), style=0)
        self.choice4.SetToolTipString(u'Field 4 music theme')
        self.choice4.Bind(wx.EVT_CHOICE, self.OnChoice4Choice,
              id=wxID_FRAME1CHOICE4)

        self.staticText7 = wx.StaticText(id=wxID_FRAME1STATICTEXT7,
              label=u'Music', name='staticText7', parent=self.panel1,
              pos=wx.Point(272, 8), size=wx.Size(26, 14), style=0)

        self.checkBox1 = wx.CheckBox(id=wxID_FRAME1CHECKBOX1,
              label=u'No Penalty', name='checkBox1', parent=self.panel1,
              pos=wx.Point(440, 40), size=wx.Size(70, 13), style=0)
        self.checkBox1.SetValue(False)
        self.checkBox1.SetToolTipString(u'Enable / Disable penalty')
        self.checkBox1.Bind(wx.EVT_CHECKBOX, self.OnCheckBox1Checkbox,
              id=wxID_FRAME1CHECKBOX1)

        self.button1 = wx.Button(id=wxID_FRAME1BUTTON1, label=u'Load',
              name='button1', parent=self.panel1, pos=wx.Point(816, 8),
              size=wx.Size(75, 23), style=0)
        self.button1.SetToolTipString(u'Load rom')
        self.button1.Bind(wx.EVT_BUTTON, self.OnButton1Button,
              id=wxID_FRAME1BUTTON1)

        self.button2 = wx.Button(id=wxID_FRAME1BUTTON2, label=u'Save',
              name='button2', parent=self.panel1, pos=wx.Point(816, 40),
              size=wx.Size(75, 23), style=0)
        self.button2.SetToolTipString(u'Save rom')
        self.button2.Enable(False)
        self.button2.Bind(wx.EVT_BUTTON, self.OnButton2Button,
              id=wxID_FRAME1BUTTON2)

        self.notebook1 = wx.Notebook(id=wxID_FRAME1NOTEBOOK1, name='notebook1',
              parent=self.panel1, pos=wx.Point(8, 72), size=wx.Size(888, 264),
              style=0)
        self.notebook1.SetToolTipString(u'')

        self.panel8 = wx.Panel(id=wxID_FRAME1PANEL8, name='panel8',
              parent=self.notebook1, pos=wx.Point(0, 0), size=wx.Size(880, 238),
              style=wx.TAB_TRAVERSAL)

        self.panel9 = wx.Panel(id=wxID_FRAME1PANEL9, name='panel9',
              parent=self.notebook1, pos=wx.Point(0, 0), size=wx.Size(880, 238),
              style=wx.TAB_TRAVERSAL)

        self.panel2 = wx.Panel(id=wxID_FRAME1PANEL2, name='panel2',
              parent=self.notebook1, pos=wx.Point(0, 0), size=wx.Size(880, 238),
              style=wx.TAB_TRAVERSAL)
        self.panel2.SetToolTipString(u'')

        self.teamNameCtrl1 = wx.TextCtrl(id=wxID_FRAME1TEAMNAMECTRL1,
              name=u'teamNameCtrl1', parent=self.panel2, pos=wx.Point(96, 16),
              size=wx.Size(110, 21), style=0, value=u'')
        self.teamNameCtrl1.SetMaxLength(8)
        self.teamNameCtrl1.Bind(wx.EVT_TEXT, self.OnTeamNameCtrl1Text,
              id=wxID_FRAME1TEAMNAMECTRL1)

        self.sPowerSpinTeam1Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1SPOWERSPINTEAM1CTRL1,
              initial=1, max=12, min=1, name=u'sPowerSpinTeam1Ctrl1',
              parent=self.panel2, pos=wx.Point(240, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.sPowerSpinTeam1Ctrl1.Bind(wx.EVT_TEXT,
              self.OnSPowerSpinTeam1Ctrl1Text,
              id=wxID_FRAME1SPOWERSPINTEAM1CTRL1)

        self.staticText8 = wx.StaticText(id=wxID_FRAME1STATICTEXT8,
              label=u'Team name :', name='staticText8', parent=self.panel2,
              pos=wx.Point(16, 16), size=wx.Size(62, 14), style=0)

        self.team1Player5Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM1PLAYER5CTRL,
              name=u'team1Player5Ctrl', parent=self.panel2, pos=wx.Point(136,
              192), size=wx.Size(56, 21), style=0, value=u'')
        self.team1Player5Ctrl.SetMaxLength(4)
        self.team1Player5Ctrl.Bind(wx.EVT_TEXT, self.OnTeam1Player5CtrlText,
              id=wxID_FRAME1TEAM1PLAYER5CTRL)

        self.team1Player4Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM1PLAYER4CTRL,
              name=u'team1Player4Ctrl', parent=self.panel2, pos=wx.Point(136,
              160), size=wx.Size(56, 21), style=0, value=u'')
        self.team1Player4Ctrl.SetMaxLength(4)
        self.team1Player4Ctrl.Bind(wx.EVT_TEXT, self.OnTeam1Player4CtrlText,
              id=wxID_FRAME1TEAM1PLAYER4CTRL)

        self.team1Player1Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM1PLAYER1CTRL,
              name=u'team1Player1Ctrl', parent=self.panel2, pos=wx.Point(136,
              64), size=wx.Size(56, 21), style=0, value=u'')
        self.team1Player1Ctrl.SetMaxLength(4)
        self.team1Player1Ctrl.Bind(wx.EVT_TEXT, self.OnTeam1Player1CtrlText,
              id=wxID_FRAME1TEAM1PLAYER1CTRL)

        self.mPowerSpinTeam1Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1MPOWERSPINTEAM1CTRL4,
              initial=1, max=5, min=1, name=u'mPowerSpinTeam1Ctrl4',
              parent=self.panel2, pos=wx.Point(312, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.mPowerSpinTeam1Ctrl4.Bind(wx.EVT_TEXT,
              self.OnMPowerSpinTeam1Ctrl4Text,
              id=wxID_FRAME1MPOWERSPINTEAM1CTRL4)

        self.mPowerSpinTeam1Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1MPOWERSPINTEAM1CTRL5,
              initial=1, max=5, min=1, name=u'mPowerSpinTeam1Ctrl5',
              parent=self.panel2, pos=wx.Point(312, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.mPowerSpinTeam1Ctrl5.Bind(wx.EVT_TEXT,
              self.OnMPowerSpinTeam1Ctrl5Text,
              id=wxID_FRAME1MPOWERSPINTEAM1CTRL5)

        self.mPowerSpinTeam1Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1MPOWERSPINTEAM1CTRL2,
              initial=1, max=5, min=1, name=u'mPowerSpinTeam1Ctrl2',
              parent=self.panel2, pos=wx.Point(312, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.mPowerSpinTeam1Ctrl2.Bind(wx.EVT_TEXT,
              self.OnMPowerSpinTeam1Ctrl2Text,
              id=wxID_FRAME1MPOWERSPINTEAM1CTRL2)

        self.mPowerSpinTeam1Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1MPOWERSPINTEAM1CTRL3,
              initial=1, max=5, min=1, name=u'mPowerSpinTeam1Ctrl3',
              parent=self.panel2, pos=wx.Point(312, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.mPowerSpinTeam1Ctrl3.Bind(wx.EVT_TEXT,
              self.OnMPowerSpinTeam1Ctrl3Text,
              id=wxID_FRAME1MPOWERSPINTEAM1CTRL3)

        self.mPowerSpinTeam1Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1MPOWERSPINTEAM1CTRL1,
              initial=1, max=5, min=1, name=u'mPowerSpinTeam1Ctrl1',
              parent=self.panel2, pos=wx.Point(312, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.mPowerSpinTeam1Ctrl1.Bind(wx.EVT_TEXT,
              self.OnMPowerSpinTeam1Ctrl1Text,
              id=wxID_FRAME1MPOWERSPINTEAM1CTRL1)

        self.weightSpinTeam1Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1WEIGHTSPINTEAM1CTRL4,
              initial=1, max=5, min=1, name=u'weightSpinTeam1Ctrl4',
              parent=self.panel2, pos=wx.Point(456, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.weightSpinTeam1Ctrl4.Bind(wx.EVT_TEXT,
              self.OnWeightSpinTeam1Ctrl4Text,
              id=wxID_FRAME1WEIGHTSPINTEAM1CTRL4)

        self.weightSpinTeam1Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1WEIGHTSPINTEAM1CTRL5,
              initial=1, max=5, min=1, name=u'weightSpinTeam1Ctrl5',
              parent=self.panel2, pos=wx.Point(456, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.weightSpinTeam1Ctrl5.Bind(wx.EVT_TEXT,
              self.OnWeightSpinTeam1Ctrl5Text,
              id=wxID_FRAME1WEIGHTSPINTEAM1CTRL5)

        self.weightSpinTeam1Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1WEIGHTSPINTEAM1CTRL2,
              initial=1, max=5, min=1, name=u'weightSpinTeam1Ctrl2',
              parent=self.panel2, pos=wx.Point(456, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.weightSpinTeam1Ctrl2.Bind(wx.EVT_TEXT,
              self.OnWeightSpinTeam1Ctrl2Text,
              id=wxID_FRAME1WEIGHTSPINTEAM1CTRL2)

        self.weightSpinTeam1Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1WEIGHTSPINTEAM1CTRL3,
              initial=1, max=5, min=1, name=u'weightSpinTeam1Ctrl3',
              parent=self.panel2, pos=wx.Point(456, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.weightSpinTeam1Ctrl3.Bind(wx.EVT_TEXT,
              self.OnWeightSpinTeam1Ctrl3Text,
              id=wxID_FRAME1WEIGHTSPINTEAM1CTRL3)

        self.weightSpinTeam1Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1WEIGHTSPINTEAM1CTRL1,
              initial=1, max=5, min=1, name=u'weightSpinTeam1Ctrl1',
              parent=self.panel2, pos=wx.Point(456, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.weightSpinTeam1Ctrl1.Bind(wx.EVT_TEXT,
              self.OnWeightSpinTeam1Ctrl1Text,
              id=wxID_FRAME1WEIGHTSPINTEAM1CTRL1)

        self.sPowerSpinTeam1Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1SPOWERSPINTEAM1CTRL4,
              initial=1, max=12, min=1, name=u'sPowerSpinTeam1Ctrl4',
              parent=self.panel2, pos=wx.Point(240, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.sPowerSpinTeam1Ctrl4.Bind(wx.EVT_TEXT,
              self.OnSPowerSpinTeam1Ctrl4Text,
              id=wxID_FRAME1SPOWERSPINTEAM1CTRL4)

        self.sPowerSpinTeam1Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1SPOWERSPINTEAM1CTRL5,
              initial=1, max=12, min=1, name=u'sPowerSpinTeam1Ctrl5',
              parent=self.panel2, pos=wx.Point(240, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.sPowerSpinTeam1Ctrl5.Bind(wx.EVT_TEXT,
              self.OnSPowerSpinTeam1Ctrl5Text,
              id=wxID_FRAME1SPOWERSPINTEAM1CTRL5)

        self.sPowerSpinTeam1Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1SPOWERSPINTEAM1CTRL2,
              initial=1, max=12, min=1, name=u'sPowerSpinTeam1Ctrl2',
              parent=self.panel2, pos=wx.Point(240, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.sPowerSpinTeam1Ctrl2.Bind(wx.EVT_TEXT,
              self.OnSPowerSpinTeam1Ctrl2Text,
              id=wxID_FRAME1SPOWERSPINTEAM1CTRL2)

        self.staticText9 = wx.StaticText(id=wxID_FRAME1STATICTEXT9,
              label=u'Name', name='staticText9', parent=self.panel2,
              pos=wx.Point(144, 48), size=wx.Size(27, 14), style=0)

        self.speedSpinTeam1Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1SPEEDSPINTEAM1CTRL1,
              initial=1, max=3, min=1, name=u'speedSpinTeam1Ctrl1',
              parent=self.panel2, pos=wx.Point(384, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.speedSpinTeam1Ctrl1.Bind(wx.EVT_TEXT,
              self.OnSpeedSpinTeam1Ctrl1Text,
              id=wxID_FRAME1SPEEDSPINTEAM1CTRL1)

        self.speedSpinTeam1Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1SPEEDSPINTEAM1CTRL2,
              initial=1, max=3, min=1, name=u'speedSpinTeam1Ctrl2',
              parent=self.panel2, pos=wx.Point(384, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.speedSpinTeam1Ctrl2.Bind(wx.EVT_TEXT,
              self.OnSpeedSpinTeam1Ctrl2Text,
              id=wxID_FRAME1SPEEDSPINTEAM1CTRL2)

        self.speedSpinTeam1Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1SPEEDSPINTEAM1CTRL3,
              initial=1, max=3, min=1, name=u'speedSpinTeam1Ctrl3',
              parent=self.panel2, pos=wx.Point(384, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.speedSpinTeam1Ctrl3.Bind(wx.EVT_TEXT,
              self.OnSpeedSpinTeam1Ctrl3Text,
              id=wxID_FRAME1SPEEDSPINTEAM1CTRL3)

        self.speedSpinTeam1Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1SPEEDSPINTEAM1CTRL4,
              initial=1, max=3, min=1, name=u'speedSpinTeam1Ctrl4',
              parent=self.panel2, pos=wx.Point(384, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.speedSpinTeam1Ctrl4.Bind(wx.EVT_TEXT,
              self.OnSpeedSpinTeam1Ctrl4Text,
              id=wxID_FRAME1SPEEDSPINTEAM1CTRL4)

        self.speedSpinTeam1Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1SPEEDSPINTEAM1CTRL5,
              initial=1, max=3, min=1, name=u'speedSpinTeam1Ctrl5',
              parent=self.panel2, pos=wx.Point(384, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.speedSpinTeam1Ctrl5.Bind(wx.EVT_TEXT,
              self.OnSpeedSpinTeam1Ctrl5Text,
              id=wxID_FRAME1SPEEDSPINTEAM1CTRL5)

        self.team1Player3Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM1PLAYER3CTRL,
              name=u'team1Player3Ctrl', parent=self.panel2, pos=wx.Point(136,
              128), size=wx.Size(56, 21), style=0, value=u'')
        self.team1Player3Ctrl.SetMaxLength(4)
        self.team1Player3Ctrl.Bind(wx.EVT_TEXT, self.OnTeam1Player3CtrlText,
              id=wxID_FRAME1TEAM1PLAYER3CTRL)

        self.team1Player2Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM1PLAYER2CTRL,
              name=u'team1Player2Ctrl', parent=self.panel2, pos=wx.Point(136,
              96), size=wx.Size(56, 21), style=0, value=u'')
        self.team1Player2Ctrl.SetMaxLength(4)
        self.team1Player2Ctrl.Bind(wx.EVT_TEXT, self.OnTeam1Player2CtrlText,
              id=wxID_FRAME1TEAM1PLAYER2CTRL)

        self.sPowerSpinTeam1Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1SPOWERSPINTEAM1CTRL3,
              initial=1, max=12, min=1, name=u'sPowerSpinTeam1Ctrl3',
              parent=self.panel2, pos=wx.Point(240, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.sPowerSpinTeam1Ctrl3.Bind(wx.EVT_TEXT,
              self.OnSPowerSpinTeam1Ctrl3Text,
              id=wxID_FRAME1SPOWERSPINTEAM1CTRL3)

        self.staticText10 = wx.StaticText(id=wxID_FRAME1STATICTEXT10,
              label=u'Start Power', name='staticText10', parent=self.panel2,
              pos=wx.Point(232, 40), size=wx.Size(57, 14), style=0)

        self.staticText11 = wx.StaticText(id=wxID_FRAME1STATICTEXT11,
              label=u'Max Power', name='staticText11', parent=self.panel2,
              pos=wx.Point(312, 40), size=wx.Size(53, 14), style=0)

        self.staticText12 = wx.StaticText(id=wxID_FRAME1STATICTEXT12,
              label=u'Speed', name='staticText12', parent=self.panel2,
              pos=wx.Point(392, 40), size=wx.Size(30, 14), style=0)

        self.staticText13 = wx.StaticText(id=wxID_FRAME1STATICTEXT13,
              label=u'Weight', name='staticText13', parent=self.panel2,
              pos=wx.Point(464, 40), size=wx.Size(34, 14), style=0)

        self.staticText14 = wx.StaticText(id=wxID_FRAME1STATICTEXT14,
              label=u'Angry', name='staticText14', parent=self.panel2,
              pos=wx.Point(536, 40), size=wx.Size(29, 14), style=0)

        self.staticText15 = wx.StaticText(id=wxID_FRAME1STATICTEXT15,
              label=u'Special Shoot', name='staticText15', parent=self.panel2,
              pos=wx.Point(608, 40), size=wx.Size(64, 14), style=0)

        self.angrySpinTeam1Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1ANGRYSPINTEAM1CTRL4,
              initial=1, max=7, min=1, name=u'angrySpinTeam1Ctrl4',
              parent=self.panel2, pos=wx.Point(528, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.angrySpinTeam1Ctrl4.Bind(wx.EVT_TEXT,
              self.OnAngrySpinTeam1Ctrl4Text,
              id=wxID_FRAME1ANGRYSPINTEAM1CTRL4)

        self.angrySpinTeam1Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1ANGRYSPINTEAM1CTRL5,
              initial=1, max=7, min=1, name=u'angrySpinTeam1Ctrl5',
              parent=self.panel2, pos=wx.Point(528, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.angrySpinTeam1Ctrl5.Bind(wx.EVT_TEXT,
              self.OnAngrySpinTeam1Ctrl5Text,
              id=wxID_FRAME1ANGRYSPINTEAM1CTRL5)

        self.angrySpinTeam1Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1ANGRYSPINTEAM1CTRL2,
              initial=1, max=7, min=1, name=u'angrySpinTeam1Ctrl2',
              parent=self.panel2, pos=wx.Point(528, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.angrySpinTeam1Ctrl2.Bind(wx.EVT_TEXT,
              self.OnAngrySpinTeam1Ctrl2Text,
              id=wxID_FRAME1ANGRYSPINTEAM1CTRL2)

        self.angrySpinTeam1Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1ANGRYSPINTEAM1CTRL3,
              initial=1, max=7, min=1, name=u'angrySpinTeam1Ctrl3',
              parent=self.panel2, pos=wx.Point(528, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.angrySpinTeam1Ctrl3.Bind(wx.EVT_TEXT,
              self.OnAngrySpinTeam1Ctrl3Text,
              id=wxID_FRAME1ANGRYSPINTEAM1CTRL3)

        self.angrySpinTeam1Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1ANGRYSPINTEAM1CTRL1,
              initial=1, max=7, min=1, name=u'angrySpinTeam1Ctrl1',
              parent=self.panel2, pos=wx.Point(528, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.angrySpinTeam1Ctrl1.Bind(wx.EVT_TEXT,
              self.OnAngrySpinTeam1Ctrl1Text,
              id=wxID_FRAME1ANGRYSPINTEAM1CTRL1)

        self.panel3 = wx.Panel(id=wxID_FRAME1PANEL3, name='panel3',
              parent=self.notebook1, pos=wx.Point(0, 0), size=wx.Size(880, 238),
              style=wx.TAB_TRAVERSAL)
        self.panel3.SetToolTipString(u'')

        self.panel4 = wx.Panel(id=wxID_FRAME1PANEL4, name='panel4',
              parent=self.notebook1, pos=wx.Point(0, 0), size=wx.Size(880, 238),
              style=wx.TAB_TRAVERSAL)
        self.panel4.SetToolTipString(u'')

        self.panel5 = wx.Panel(id=wxID_FRAME1PANEL5, name='panel5',
              parent=self.notebook1, pos=wx.Point(0, 0), size=wx.Size(880, 238),
              style=wx.TAB_TRAVERSAL)

        self.panel6 = wx.Panel(id=wxID_FRAME1PANEL6, name='panel6',
              parent=self.notebook1, pos=wx.Point(0, 0), size=wx.Size(880, 238),
              style=wx.TAB_TRAVERSAL)

        self.panel7 = wx.Panel(id=wxID_FRAME1PANEL7, name='panel7',
              parent=self.notebook1, pos=wx.Point(0, 0), size=wx.Size(880, 238),
              style=wx.TAB_TRAVERSAL)

        self.staticText22 = wx.StaticText(id=wxID_FRAME1STATICTEXT22,
              label=u'Team name :', name='staticText22', parent=self.panel3,
              pos=wx.Point(16, 16), size=wx.Size(62, 14), style=0)

        self.teamNameCtrl2 = wx.TextCtrl(id=wxID_FRAME1TEAMNAMECTRL2,
              name=u'teamNameCtrl2', parent=self.panel3, pos=wx.Point(96, 16),
              size=wx.Size(110, 21), style=0, value=u'')
        self.teamNameCtrl2.SetMaxLength(8)
        self.teamNameCtrl2.Bind(wx.EVT_TEXT, self.OnTeamNameCtrl2Text,
              id=wxID_FRAME1TEAMNAMECTRL2)

        self.staticText23 = wx.StaticText(id=wxID_FRAME1STATICTEXT23,
              label=u'Name', name='staticText23', parent=self.panel3,
              pos=wx.Point(144, 48), size=wx.Size(27, 14), style=0)

        self.team2Player1Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM2PLAYER1CTRL,
              name=u'team2Player1Ctrl', parent=self.panel3, pos=wx.Point(136,
              64), size=wx.Size(56, 21), style=0, value=u'')
        self.team2Player1Ctrl.SetMaxLength(4)
        self.team2Player1Ctrl.Bind(wx.EVT_TEXT, self.OnTeam2Player1CtrlText,
              id=wxID_FRAME1TEAM2PLAYER1CTRL)

        self.team2Player2Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM2PLAYER2CTRL,
              name=u'team2Player2Ctrl', parent=self.panel3, pos=wx.Point(136,
              96), size=wx.Size(56, 21), style=0, value=u'')
        self.team2Player2Ctrl.SetMaxLength(4)
        self.team2Player2Ctrl.Bind(wx.EVT_TEXT, self.OnTeam2Player2CtrlText,
              id=wxID_FRAME1TEAM2PLAYER2CTRL)

        self.team2Player3Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM2PLAYER3CTRL,
              name=u'team2Player3Ctrl', parent=self.panel3, pos=wx.Point(136,
              128), size=wx.Size(56, 21), style=0, value=u'')
        self.team2Player3Ctrl.SetMaxLength(4)
        self.team2Player3Ctrl.Bind(wx.EVT_TEXT, self.OnTeam2Player3CtrlText,
              id=wxID_FRAME1TEAM2PLAYER3CTRL)

        self.team2Player4Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM2PLAYER4CTRL,
              name=u'team2Player4Ctrl', parent=self.panel3, pos=wx.Point(136,
              160), size=wx.Size(56, 21), style=0, value=u'')
        self.team2Player4Ctrl.SetMaxLength(4)
        self.team2Player4Ctrl.Bind(wx.EVT_TEXT, self.OnTeam2Player4CtrlText,
              id=wxID_FRAME1TEAM2PLAYER4CTRL)

        self.team2Player5Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM2PLAYER5CTRL,
              name=u'team2Player5Ctrl', parent=self.panel3, pos=wx.Point(136,
              192), size=wx.Size(56, 21), style=0, value=u'')
        self.team2Player5Ctrl.SetMaxLength(4)
        self.team2Player5Ctrl.Bind(wx.EVT_TEXT, self.OnTeam2Player5CtrlText,
              id=wxID_FRAME1TEAM2PLAYER5CTRL)

        self.staticText24 = wx.StaticText(id=wxID_FRAME1STATICTEXT24,
              label=u'Team name :', name='staticText24', parent=self.panel4,
              pos=wx.Point(16, 16), size=wx.Size(62, 14), style=0)

        self.teamNameCtrl3 = wx.TextCtrl(id=wxID_FRAME1TEAMNAMECTRL3,
              name=u'teamNameCtrl3', parent=self.panel4, pos=wx.Point(96, 16),
              size=wx.Size(110, 21), style=0, value=u'')
        self.teamNameCtrl3.SetMaxLength(8)
        self.teamNameCtrl3.Bind(wx.EVT_TEXT, self.OnTeamNameCtrl3Text,
              id=wxID_FRAME1TEAMNAMECTRL3)

        self.staticText25 = wx.StaticText(id=wxID_FRAME1STATICTEXT25,
              label=u'Name', name='staticText25', parent=self.panel4,
              pos=wx.Point(144, 48), size=wx.Size(27, 14), style=0)

        self.team3Player1Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM3PLAYER1CTRL,
              name=u'team3Player1Ctrl', parent=self.panel4, pos=wx.Point(136,
              64), size=wx.Size(56, 21), style=0, value=u'')
        self.team3Player1Ctrl.SetMaxLength(4)
        self.team3Player1Ctrl.Bind(wx.EVT_TEXT, self.OnTeam3Player1CtrlText,
              id=wxID_FRAME1TEAM3PLAYER1CTRL)

        self.team3Player2Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM3PLAYER2CTRL,
              name=u'team3Player2Ctrl', parent=self.panel4, pos=wx.Point(136,
              96), size=wx.Size(56, 21), style=0, value=u'')
        self.team3Player2Ctrl.SetMaxLength(4)
        self.team3Player2Ctrl.Bind(wx.EVT_TEXT, self.OnTeam3Player2CtrlText,
              id=wxID_FRAME1TEAM3PLAYER2CTRL)

        self.team3Player3Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM3PLAYER3CTRL,
              name=u'team3Player3Ctrl', parent=self.panel4, pos=wx.Point(136,
              128), size=wx.Size(56, 21), style=0, value=u'')
        self.team3Player3Ctrl.SetMaxLength(4)
        self.team3Player3Ctrl.Bind(wx.EVT_TEXT, self.OnTeam3Player3CtrlText,
              id=wxID_FRAME1TEAM3PLAYER3CTRL)

        self.team3Player4Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM3PLAYER4CTRL,
              name=u'team3Player4Ctrl', parent=self.panel4, pos=wx.Point(136,
              160), size=wx.Size(56, 21), style=0, value=u'')
        self.team3Player4Ctrl.SetMaxLength(4)
        self.team3Player4Ctrl.Bind(wx.EVT_TEXT, self.OnTeam3Player4CtrlText,
              id=wxID_FRAME1TEAM3PLAYER4CTRL)

        self.team3Player5Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM3PLAYER5CTRL,
              name=u'team3Player5Ctrl', parent=self.panel4, pos=wx.Point(136,
              192), size=wx.Size(56, 21), style=0, value=u'')
        self.team3Player5Ctrl.SetMaxLength(4)
        self.team3Player5Ctrl.Bind(wx.EVT_TEXT, self.OnTeam3Player5CtrlText,
              id=wxID_FRAME1TEAM3PLAYER5CTRL)

        self.shootTeam1Choice1 = wx.Choice(choices=[],
              id=wxID_FRAME1SHOOTTEAM1CHOICE1, name=u'shootTeam1Choice1',
              parent=self.panel2, pos=wx.Point(592, 64), size=wx.Size(106, 21),
              style=0)
        self.shootTeam1Choice1.Bind(wx.EVT_CHOICE,
              self.OnShootTeam1Choice1Choice, id=wxID_FRAME1SHOOTTEAM1CHOICE1)

        self.shootTeam1Choice2 = wx.Choice(choices=[],
              id=wxID_FRAME1SHOOTTEAM1CHOICE2, name=u'shootTeam1Choice2',
              parent=self.panel2, pos=wx.Point(592, 96), size=wx.Size(106, 21),
              style=0)
        self.shootTeam1Choice2.Bind(wx.EVT_CHOICE,
              self.OnShootTeam1Choice2Choice, id=wxID_FRAME1SHOOTTEAM1CHOICE2)

        self.shootTeam1Choice3 = wx.Choice(choices=[],
              id=wxID_FRAME1SHOOTTEAM1CHOICE3, name=u'shootTeam1Choice3',
              parent=self.panel2, pos=wx.Point(592, 128), size=wx.Size(106, 21),
              style=0)
        self.shootTeam1Choice3.Bind(wx.EVT_CHOICE,
              self.OnShootTeam1Choice3Choice, id=wxID_FRAME1SHOOTTEAM1CHOICE3)

        self.shootTeam1Choice4 = wx.Choice(choices=[],
              id=wxID_FRAME1SHOOTTEAM1CHOICE4, name=u'shootTeam1Choice4',
              parent=self.panel2, pos=wx.Point(592, 160), size=wx.Size(106, 21),
              style=0)
        self.shootTeam1Choice4.Bind(wx.EVT_CHOICE,
              self.OnShootTeam1Choice4Choice, id=wxID_FRAME1SHOOTTEAM1CHOICE4)

        self.shootTeam1Choice5 = wx.Choice(choices=[],
              id=wxID_FRAME1SHOOTTEAM1CHOICE5, name=u'shootTeam1Choice5',
              parent=self.panel2, pos=wx.Point(592, 192), size=wx.Size(106, 21),
              style=0)
        self.shootTeam1Choice5.Bind(wx.EVT_CHOICE,
              self.OnShootTeam1Choice5Choice, id=wxID_FRAME1SHOOTTEAM1CHOICE5)

        self.team1AttackSpinCtrl1 = wx.SpinCtrl(id=wxID_FRAME1TEAM1ATTACKSPINCTRL1,
              initial=0, max=255, min=0, name=u'team1AttackSpinCtrl1',
              parent=self.panel2, pos=wx.Point(48, 80), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.team1AttackSpinCtrl1.Bind(wx.EVT_TEXT,
              self.OnTeam1AttackSpinCtrl1Text,
              id=wxID_FRAME1TEAM1ATTACKSPINCTRL1)

        self.team1DefenseSpinCtrl1 = wx.SpinCtrl(id=wxID_FRAME1TEAM1DEFENSESPINCTRL1,
              initial=0, max=7, min=0, name=u'team1DefenseSpinCtrl1',
              parent=self.panel2, pos=wx.Point(48, 152), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.team1DefenseSpinCtrl1.Bind(wx.EVT_TEXT,
              self.OnTeam1DefenseSpinCtrl1Text,
              id=wxID_FRAME1TEAM1DEFENSESPINCTRL1)

        self.staticText21 = wx.StaticText(id=wxID_FRAME1STATICTEXT21,
              label=u'Team attack', name='staticText21', parent=self.panel2,
              pos=wx.Point(40, 48), size=wx.Size(59, 14), style=0)

        self.staticText26 = wx.StaticText(id=wxID_FRAME1STATICTEXT26,
              label=u'Team defense', name='staticText26', parent=self.panel2,
              pos=wx.Point(40, 120), size=wx.Size(69, 14), style=0)

        self.choice5 = wx.Choice(choices=[], id=wxID_FRAME1CHOICE5,
              name='choice5', parent=self.panel1, pos=wx.Point(152, 40),
              size=wx.Size(48, 21), style=0)
        self.choice5.SetToolTipString(u'Field 1 music theme')
        self.choice5.Bind(wx.EVT_CHOICE, self.OnChoice5Choice,
              id=wxID_FRAME1CHOICE5)

        self.staticText27 = wx.StaticText(id=wxID_FRAME1STATICTEXT27,
              label=u'Field 5', name='staticText27', parent=self.panel1,
              pos=wx.Point(384, 24), size=wx.Size(31, 14), style=0)

        self.staticText28 = wx.StaticText(id=wxID_FRAME1STATICTEXT28,
              label=u'Team name :', name='staticText28', parent=self.panel5,
              pos=wx.Point(16, 16), size=wx.Size(62, 14), style=0)

        self.staticText29 = wx.StaticText(id=wxID_FRAME1STATICTEXT29,
              label=u'Name', name='staticText29', parent=self.panel5,
              pos=wx.Point(144, 48), size=wx.Size(27, 14), style=0)

        self.staticText30 = wx.StaticText(id=wxID_FRAME1STATICTEXT30,
              label=u'Team name :', name='staticText30', parent=self.panel6,
              pos=wx.Point(16, 16), size=wx.Size(62, 14), style=0)

        self.staticText31 = wx.StaticText(id=wxID_FRAME1STATICTEXT31,
              label=u'Name', name='staticText31', parent=self.panel6,
              pos=wx.Point(144, 48), size=wx.Size(27, 14), style=0)

        self.staticText32 = wx.StaticText(id=wxID_FRAME1STATICTEXT32,
              label=u'Team name :', name='staticText32', parent=self.panel7,
              pos=wx.Point(16, 16), size=wx.Size(62, 14), style=0)

        self.staticText33 = wx.StaticText(id=wxID_FRAME1STATICTEXT33,
              label=u'Name', name='staticText33', parent=self.panel7,
              pos=wx.Point(144, 48), size=wx.Size(27, 14), style=0)

        self.staticText34 = wx.StaticText(id=wxID_FRAME1STATICTEXT34,
              label=u'Team name :', name='staticText34', parent=self.panel8,
              pos=wx.Point(16, 16), size=wx.Size(62, 14), style=0)

        self.staticText35 = wx.StaticText(id=wxID_FRAME1STATICTEXT35,
              label=u'Name', name='staticText35', parent=self.panel8,
              pos=wx.Point(144, 48), size=wx.Size(27, 14), style=0)

        self.staticText36 = wx.StaticText(id=wxID_FRAME1STATICTEXT36,
              label=u'Team name :', name='staticText36', parent=self.panel9,
              pos=wx.Point(16, 16), size=wx.Size(62, 14), style=0)

        self.staticText37 = wx.StaticText(id=wxID_FRAME1STATICTEXT37,
              label=u'Name', name='staticText37', parent=self.panel9,
              pos=wx.Point(144, 48), size=wx.Size(27, 14), style=0)

        self.teamNameCtrl4 = wx.TextCtrl(id=wxID_FRAME1TEAMNAMECTRL4,
              name=u'teamNameCtrl4', parent=self.panel5, pos=wx.Point(96, 16),
              size=wx.Size(110, 21), style=0, value=u'')
        self.teamNameCtrl4.SetMaxLength(8)
        self.teamNameCtrl4.Bind(wx.EVT_TEXT, self.OnTeamNameCtrl4Text,
              id=wxID_FRAME1TEAMNAMECTRL4)

        self.teamNameCtrl5 = wx.TextCtrl(id=wxID_FRAME1TEAMNAMECTRL5,
              name=u'teamNameCtrl5', parent=self.panel6, pos=wx.Point(96, 16),
              size=wx.Size(110, 21), style=0, value=u'')
        self.teamNameCtrl5.SetMaxLength(8)
        self.teamNameCtrl5.Bind(wx.EVT_TEXT, self.OnTeamNameCtrl5Text,
              id=wxID_FRAME1TEAMNAMECTRL5)

        self.teamNameCtrl6 = wx.TextCtrl(id=wxID_FRAME1TEAMNAMECTRL6,
              name=u'teamNameCtrl6', parent=self.panel7, pos=wx.Point(96, 16),
              size=wx.Size(110, 21), style=0, value=u'')
        self.teamNameCtrl6.SetMaxLength(8)
        self.teamNameCtrl6.Bind(wx.EVT_TEXT, self.OnTeamNameCtrl6Text,
              id=wxID_FRAME1TEAMNAMECTRL6)

        self.teamNameCtrl7 = wx.TextCtrl(id=wxID_FRAME1TEAMNAMECTRL7,
              name=u'teamNameCtrl7', parent=self.panel8, pos=wx.Point(96, 16),
              size=wx.Size(110, 21), style=0, value=u'')
        self.teamNameCtrl7.SetMaxLength(8)
        self.teamNameCtrl7.Bind(wx.EVT_TEXT, self.OnTeamNameCtrl7Text,
              id=wxID_FRAME1TEAMNAMECTRL7)

        self.teamNameCtrl8 = wx.TextCtrl(id=wxID_FRAME1TEAMNAMECTRL8,
              name=u'teamNameCtrl8', parent=self.panel9, pos=wx.Point(96, 16),
              size=wx.Size(110, 21), style=0, value=u'')
        self.teamNameCtrl8.SetMaxLength(8)
        self.teamNameCtrl8.Bind(wx.EVT_TEXT, self.OnTeamNameCtrl8Text,
              id=wxID_FRAME1TEAMNAMECTRL8)

        self.team4Player1Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM4PLAYER1CTRL,
              name=u'team4Player1Ctrl', parent=self.panel5, pos=wx.Point(136,
              64), size=wx.Size(56, 21), style=0, value=u'')
        self.team4Player1Ctrl.SetMaxLength(4)
        self.team4Player1Ctrl.Bind(wx.EVT_TEXT, self.OnTeam4Player1CtrlText,
              id=wxID_FRAME1TEAM4PLAYER1CTRL)

        self.team4Player2Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM4PLAYER2CTRL,
              name=u'team4Player2Ctrl', parent=self.panel5, pos=wx.Point(136,
              96), size=wx.Size(56, 21), style=0, value=u'')
        self.team4Player2Ctrl.SetMaxLength(4)
        self.team4Player2Ctrl.Bind(wx.EVT_TEXT, self.OnTeam4Player2CtrlText,
              id=wxID_FRAME1TEAM4PLAYER2CTRL)

        self.team4Player3Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM4PLAYER3CTRL,
              name=u'team4Player3Ctrl', parent=self.panel5, pos=wx.Point(136,
              128), size=wx.Size(56, 21), style=0, value=u'')
        self.team4Player3Ctrl.SetMaxLength(4)
        self.team4Player3Ctrl.Bind(wx.EVT_TEXT, self.OnTeam4Player3CtrlText,
              id=wxID_FRAME1TEAM4PLAYER3CTRL)

        self.team4Player4Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM4PLAYER4CTRL,
              name=u'team4Player4Ctrl', parent=self.panel5, pos=wx.Point(136,
              160), size=wx.Size(56, 21), style=0, value=u'')
        self.team4Player4Ctrl.SetMaxLength(4)
        self.team4Player4Ctrl.Bind(wx.EVT_TEXT, self.OnTeam4Player4CtrlText,
              id=wxID_FRAME1TEAM4PLAYER4CTRL)

        self.team4Player5Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM4PLAYER5CTRL,
              name=u'team4Player5Ctrl', parent=self.panel5, pos=wx.Point(136,
              192), size=wx.Size(56, 21), style=0, value=u'')
        self.team4Player5Ctrl.SetMaxLength(4)
        self.team4Player5Ctrl.Bind(wx.EVT_TEXT, self.OnTeam4Player5CtrlText,
              id=wxID_FRAME1TEAM4PLAYER5CTRL)

        self.team5Player1Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM5PLAYER1CTRL,
              name=u'team5Player1Ctrl', parent=self.panel6, pos=wx.Point(136,
              64), size=wx.Size(56, 21), style=0, value=u'')
        self.team5Player1Ctrl.SetMaxLength(4)
        self.team5Player1Ctrl.Bind(wx.EVT_TEXT, self.OnTeam5Player1CtrlText,
              id=wxID_FRAME1TEAM5PLAYER1CTRL)

        self.team5Player2Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM5PLAYER2CTRL,
              name=u'team5Player2Ctrl', parent=self.panel6, pos=wx.Point(136,
              96), size=wx.Size(56, 21), style=0, value=u'')
        self.team5Player2Ctrl.SetMaxLength(4)
        self.team5Player2Ctrl.Bind(wx.EVT_TEXT, self.OnTeam5Player2CtrlText,
              id=wxID_FRAME1TEAM5PLAYER2CTRL)

        self.team5Player3Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM5PLAYER3CTRL,
              name=u'team5Player3Ctrl', parent=self.panel6, pos=wx.Point(136,
              128), size=wx.Size(56, 21), style=0, value=u'')
        self.team5Player3Ctrl.SetMaxLength(4)
        self.team5Player3Ctrl.Bind(wx.EVT_TEXT, self.OnTeam5Player3CtrlText,
              id=wxID_FRAME1TEAM5PLAYER3CTRL)

        self.team5Player4Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM5PLAYER4CTRL,
              name=u'team5Player4Ctrl', parent=self.panel6, pos=wx.Point(136,
              160), size=wx.Size(56, 21), style=0, value=u'')
        self.team5Player4Ctrl.SetMaxLength(4)
        self.team5Player4Ctrl.Bind(wx.EVT_TEXT, self.OnTeam5Player4CtrlText,
              id=wxID_FRAME1TEAM5PLAYER4CTRL)

        self.team5Player5Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM5PLAYER5CTRL,
              name=u'team5Player5Ctrl', parent=self.panel6, pos=wx.Point(136,
              192), size=wx.Size(56, 21), style=0, value=u'')
        self.team5Player5Ctrl.SetMaxLength(4)
        self.team5Player5Ctrl.Bind(wx.EVT_TEXT, self.OnTeam5Player5CtrlText,
              id=wxID_FRAME1TEAM5PLAYER5CTRL)

        self.team6Player1Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM6PLAYER1CTRL,
              name=u'team6Player1Ctrl', parent=self.panel7, pos=wx.Point(136,
              64), size=wx.Size(56, 21), style=0, value=u'')
        self.team6Player1Ctrl.SetMaxLength(4)
        self.team6Player1Ctrl.Bind(wx.EVT_TEXT, self.OnTeam6Player1CtrlText,
              id=wxID_FRAME1TEAM6PLAYER1CTRL)

        self.team6Player2Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM6PLAYER2CTRL,
              name=u'team6Player2Ctrl', parent=self.panel7, pos=wx.Point(136,
              96), size=wx.Size(56, 21), style=0, value=u'')
        self.team6Player2Ctrl.SetMaxLength(4)
        self.team6Player2Ctrl.Bind(wx.EVT_TEXT, self.OnTeam6Player2CtrlText,
              id=wxID_FRAME1TEAM6PLAYER2CTRL)

        self.team6Player3Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM6PLAYER3CTRL,
              name=u'team6Player3Ctrl', parent=self.panel7, pos=wx.Point(136,
              128), size=wx.Size(56, 21), style=0, value=u'')
        self.team6Player3Ctrl.SetMaxLength(4)
        self.team6Player3Ctrl.Bind(wx.EVT_TEXT, self.OnTeam6Player3CtrlText,
              id=wxID_FRAME1TEAM6PLAYER3CTRL)

        self.team6Player4Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM6PLAYER4CTRL,
              name=u'team6Player4Ctrl', parent=self.panel7, pos=wx.Point(136,
              160), size=wx.Size(56, 21), style=0, value=u'')
        self.team6Player4Ctrl.SetMaxLength(4)
        self.team6Player4Ctrl.Bind(wx.EVT_TEXT, self.OnTeam6Player4CtrlText,
              id=wxID_FRAME1TEAM6PLAYER4CTRL)

        self.team6Player5Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM6PLAYER5CTRL,
              name=u'team6Player5Ctrl', parent=self.panel7, pos=wx.Point(136,
              192), size=wx.Size(56, 21), style=0, value=u'')
        self.team6Player5Ctrl.SetMaxLength(4)
        self.team6Player5Ctrl.Bind(wx.EVT_TEXT, self.OnTeam6Player5CtrlText,
              id=wxID_FRAME1TEAM6PLAYER5CTRL)

        self.team7Player1Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM7PLAYER1CTRL,
              name=u'team7Player1Ctrl', parent=self.panel8, pos=wx.Point(136,
              64), size=wx.Size(56, 21), style=0, value=u'')
        self.team7Player1Ctrl.SetMaxLength(4)
        self.team7Player1Ctrl.Bind(wx.EVT_TEXT, self.OnTeam7Player1CtrlText,
              id=wxID_FRAME1TEAM7PLAYER1CTRL)

        self.team7Player2Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM7PLAYER2CTRL,
              name=u'team7Player2Ctrl', parent=self.panel8, pos=wx.Point(136,
              96), size=wx.Size(56, 21), style=0, value=u'')
        self.team7Player2Ctrl.SetMaxLength(4)
        self.team7Player2Ctrl.Bind(wx.EVT_TEXT, self.OnTeam7Player2CtrlText,
              id=wxID_FRAME1TEAM7PLAYER2CTRL)

        self.team7Player3Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM7PLAYER3CTRL,
              name=u'team7Player3Ctrl', parent=self.panel8, pos=wx.Point(136,
              128), size=wx.Size(56, 21), style=0, value=u'')
        self.team7Player3Ctrl.SetMaxLength(4)
        self.team7Player3Ctrl.Bind(wx.EVT_TEXT, self.OnTeam7Player3CtrlText,
              id=wxID_FRAME1TEAM7PLAYER3CTRL)

        self.team7Player4Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM7PLAYER4CTRL,
              name=u'team7Player4Ctrl', parent=self.panel8, pos=wx.Point(136,
              160), size=wx.Size(56, 21), style=0, value=u'')
        self.team7Player4Ctrl.SetMaxLength(4)
        self.team7Player4Ctrl.Bind(wx.EVT_TEXT, self.OnTeam7Player4CtrlText,
              id=wxID_FRAME1TEAM7PLAYER4CTRL)

        self.team7Player5Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM7PLAYER5CTRL,
              name=u'team7Player5Ctrl', parent=self.panel8, pos=wx.Point(136,
              192), size=wx.Size(56, 21), style=0, value=u'')
        self.team7Player5Ctrl.SetMaxLength(4)
        self.team7Player5Ctrl.Bind(wx.EVT_TEXT, self.OnTeam7Player5CtrlText,
              id=wxID_FRAME1TEAM7PLAYER5CTRL)

        self.team8Player1Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM8PLAYER1CTRL,
              name=u'team8Player1Ctrl', parent=self.panel9, pos=wx.Point(136,
              64), size=wx.Size(56, 21), style=0, value=u'')
        self.team8Player1Ctrl.SetMaxLength(4)
        self.team8Player1Ctrl.Bind(wx.EVT_TEXT, self.OnTeam8Player1CtrlText,
              id=wxID_FRAME1TEAM8PLAYER1CTRL)

        self.team8Player2Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM8PLAYER2CTRL,
              name=u'team8Player2Ctrl', parent=self.panel9, pos=wx.Point(136,
              96), size=wx.Size(56, 21), style=0, value=u'')
        self.team8Player2Ctrl.SetMaxLength(4)
        self.team8Player2Ctrl.Bind(wx.EVT_TEXT, self.OnTeam8Player2CtrlText,
              id=wxID_FRAME1TEAM8PLAYER2CTRL)

        self.team8Player3Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM8PLAYER3CTRL,
              name=u'team8Player3Ctrl', parent=self.panel9, pos=wx.Point(136,
              128), size=wx.Size(56, 21), style=0, value=u'')
        self.team8Player3Ctrl.SetMaxLength(4)
        self.team8Player3Ctrl.Bind(wx.EVT_TEXT, self.OnTeam8Player3CtrlText,
              id=wxID_FRAME1TEAM8PLAYER3CTRL)

        self.team8Player4Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM8PLAYER4CTRL,
              name=u'team8Player4Ctrl', parent=self.panel9, pos=wx.Point(136,
              160), size=wx.Size(56, 21), style=0, value=u'')
        self.team8Player4Ctrl.SetMaxLength(4)
        self.team8Player4Ctrl.Bind(wx.EVT_TEXT, self.OnTeam8Player4CtrlText,
              id=wxID_FRAME1TEAM8PLAYER4CTRL)

        self.team8Player5Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM8PLAYER5CTRL,
              name=u'team8Player5Ctrl', parent=self.panel9, pos=wx.Point(136,
              192), size=wx.Size(56, 21), style=0, value=u'')
        self.team8Player5Ctrl.SetMaxLength(4)
        self.team8Player5Ctrl.Bind(wx.EVT_TEXT, self.OnTeam8Player5CtrlText,
              id=wxID_FRAME1TEAM8PLAYER5CTRL)

        self.staticText38 = wx.StaticText(id=wxID_FRAME1STATICTEXT38,
              label=u'Team attack', name='staticText38', parent=self.panel3,
              pos=wx.Point(40, 48), size=wx.Size(59, 14), style=0)

        self.staticText39 = wx.StaticText(id=wxID_FRAME1STATICTEXT39,
              label=u'Team defense', name='staticText39', parent=self.panel3,
              pos=wx.Point(40, 120), size=wx.Size(68, 14), style=0)

        self.team2AttackSpinCtrl1 = wx.SpinCtrl(id=wxID_FRAME1TEAM2ATTACKSPINCTRL1,
              initial=0, max=255, min=0, name=u'team2AttackSpinCtrl1',
              parent=self.panel3, pos=wx.Point(48, 80), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.team2AttackSpinCtrl1.Bind(wx.EVT_TEXT,
              self.OnTeam2AttackSpinCtrl1Text,
              id=wxID_FRAME1TEAM2ATTACKSPINCTRL1)

        self.team2DefenseSpinCtrl1 = wx.SpinCtrl(id=wxID_FRAME1TEAM2DEFENSESPINCTRL1,
              initial=0, max=7, min=0, name=u'team2DefenseSpinCtrl1',
              parent=self.panel3, pos=wx.Point(48, 152), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.team2DefenseSpinCtrl1.Bind(wx.EVT_TEXT,
              self.OnTeam2DefenseSpinCtrl1Text,
              id=wxID_FRAME1TEAM2DEFENSESPINCTRL1)

        self.team3AttackSpinCtrl1 = wx.SpinCtrl(id=wxID_FRAME1TEAM3ATTACKSPINCTRL1,
              initial=0, max=255, min=0, name=u'team3AttackSpinCtrl1',
              parent=self.panel4, pos=wx.Point(48, 80), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.team3AttackSpinCtrl1.Bind(wx.EVT_TEXT,
              self.OnTeam3AttackSpinCtrl1Text,
              id=wxID_FRAME1TEAM3ATTACKSPINCTRL1)

        self.team3DefenseSpinCtrl1 = wx.SpinCtrl(id=wxID_FRAME1TEAM3DEFENSESPINCTRL1,
              initial=0, max=7, min=0, name=u'team3DefenseSpinCtrl1',
              parent=self.panel4, pos=wx.Point(48, 152), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.team3DefenseSpinCtrl1.Bind(wx.EVT_TEXT,
              self.OnTeam3DefenseSpinCtrl1Text,
              id=wxID_FRAME1TEAM3DEFENSESPINCTRL1)

        self.staticText40 = wx.StaticText(id=wxID_FRAME1STATICTEXT40,
              label=u'Team attack', name='staticText40', parent=self.panel4,
              pos=wx.Point(40, 48), size=wx.Size(59, 14), style=0)

        self.staticText41 = wx.StaticText(id=wxID_FRAME1STATICTEXT41,
              label=u'Team defense', name='staticText41', parent=self.panel4,
              pos=wx.Point(40, 120), size=wx.Size(68, 14), style=0)

        self.staticText42 = wx.StaticText(id=wxID_FRAME1STATICTEXT42,
              label=u'Team attack', name='staticText42', parent=self.panel5,
              pos=wx.Point(40, 48), size=wx.Size(59, 14), style=0)

        self.staticText43 = wx.StaticText(id=wxID_FRAME1STATICTEXT43,
              label=u'Team defense', name='staticText43', parent=self.panel5,
              pos=wx.Point(40, 120), size=wx.Size(68, 14), style=0)

        self.team4AttackSpinCtrl1 = wx.SpinCtrl(id=wxID_FRAME1TEAM4ATTACKSPINCTRL1,
              initial=0, max=255, min=0, name=u'team4AttackSpinCtrl1',
              parent=self.panel5, pos=wx.Point(48, 80), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.team4AttackSpinCtrl1.Bind(wx.EVT_TEXT,
              self.OnTeam4AttackSpinCtrl1Text,
              id=wxID_FRAME1TEAM4ATTACKSPINCTRL1)

        self.team4DefenseSpinCtrl1 = wx.SpinCtrl(id=wxID_FRAME1TEAM4DEFENSESPINCTRL1,
              initial=0, max=7, min=0, name=u'team4DefenseSpinCtrl1',
              parent=self.panel5, pos=wx.Point(48, 152), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.team4DefenseSpinCtrl1.Bind(wx.EVT_TEXT,
              self.OnTeam4DefenseSpinCtrl1Text,
              id=wxID_FRAME1TEAM4DEFENSESPINCTRL1)

        self.team5AttackSpinCtrl1 = wx.SpinCtrl(id=wxID_FRAME1TEAM5ATTACKSPINCTRL1,
              initial=0, max=255, min=0, name=u'team5AttackSpinCtrl1',
              parent=self.panel6, pos=wx.Point(48, 80), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.team5AttackSpinCtrl1.Bind(wx.EVT_TEXT,
              self.OnTeam5AttackSpinCtrl1Text,
              id=wxID_FRAME1TEAM5ATTACKSPINCTRL1)

        self.team5DefenseSpinCtrl1 = wx.SpinCtrl(id=wxID_FRAME1TEAM5DEFENSESPINCTRL1,
              initial=0, max=7, min=0, name=u'team5DefenseSpinCtrl1',
              parent=self.panel6, pos=wx.Point(48, 152), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.team5DefenseSpinCtrl1.Bind(wx.EVT_TEXT,
              self.OnTeam5DefenseSpinCtrl1Text,
              id=wxID_FRAME1TEAM5DEFENSESPINCTRL1)

        self.staticText44 = wx.StaticText(id=wxID_FRAME1STATICTEXT44,
              label=u'Team attack', name='staticText44', parent=self.panel6,
              pos=wx.Point(40, 48), size=wx.Size(59, 14), style=0)

        self.staticText45 = wx.StaticText(id=wxID_FRAME1STATICTEXT45,
              label=u'Team defense', name='staticText45', parent=self.panel6,
              pos=wx.Point(40, 120), size=wx.Size(68, 14), style=0)

        self.staticText46 = wx.StaticText(id=wxID_FRAME1STATICTEXT46,
              label=u'Team attack', name='staticText46', parent=self.panel7,
              pos=wx.Point(40, 48), size=wx.Size(59, 14), style=0)

        self.staticText47 = wx.StaticText(id=wxID_FRAME1STATICTEXT47,
              label=u'Team defense', name='staticText47', parent=self.panel7,
              pos=wx.Point(40, 120), size=wx.Size(68, 14), style=0)

        self.team6AttackSpinCtrl1 = wx.SpinCtrl(id=wxID_FRAME1TEAM6ATTACKSPINCTRL1,
              initial=0, max=255, min=0, name=u'team6AttackSpinCtrl1',
              parent=self.panel7, pos=wx.Point(48, 80), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.team6AttackSpinCtrl1.Bind(wx.EVT_TEXT,
              self.OnTeam6AttackSpinCtrl1Text,
              id=wxID_FRAME1TEAM6ATTACKSPINCTRL1)

        self.team6DefenseSpinCtrl1 = wx.SpinCtrl(id=wxID_FRAME1TEAM6DEFENSESPINCTRL1,
              initial=0, max=7, min=0, name=u'team6DefenseSpinCtrl1',
              parent=self.panel7, pos=wx.Point(48, 152), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.team6DefenseSpinCtrl1.Bind(wx.EVT_TEXT,
              self.OnTeam6DefenseSpinCtrl1Text,
              id=wxID_FRAME1TEAM6DEFENSESPINCTRL1)

        self.staticText48 = wx.StaticText(id=wxID_FRAME1STATICTEXT48,
              label=u'Team attack', name='staticText48', parent=self.panel8,
              pos=wx.Point(40, 48), size=wx.Size(60, 14), style=0)

        self.staticText49 = wx.StaticText(id=wxID_FRAME1STATICTEXT49,
              label=u'Team defense', name='staticText49', parent=self.panel8,
              pos=wx.Point(40, 120), size=wx.Size(68, 14), style=0)

        self.team7AttackSpinCtrl1 = wx.SpinCtrl(id=wxID_FRAME1TEAM7ATTACKSPINCTRL1,
              initial=0, max=255, min=0, name=u'team7AttackSpinCtrl1',
              parent=self.panel8, pos=wx.Point(48, 80), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.team7AttackSpinCtrl1.Bind(wx.EVT_TEXT,
              self.OnTeam7AttackSpinCtrl1Text,
              id=wxID_FRAME1TEAM7ATTACKSPINCTRL1)

        self.team7DefenseSpinCtrl1 = wx.SpinCtrl(id=wxID_FRAME1TEAM7DEFENSESPINCTRL1,
              initial=0, max=7, min=0, name=u'team7DefenseSpinCtrl1',
              parent=self.panel8, pos=wx.Point(48, 152), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.team7DefenseSpinCtrl1.Bind(wx.EVT_TEXT,
              self.OnTeam7DefenseSpinCtrl1Text,
              id=wxID_FRAME1TEAM7DEFENSESPINCTRL1)

        self.staticText50 = wx.StaticText(id=wxID_FRAME1STATICTEXT50,
              label=u'Team attack', name='staticText50', parent=self.panel9,
              pos=wx.Point(40, 48), size=wx.Size(59, 14), style=0)

        self.staticText51 = wx.StaticText(id=wxID_FRAME1STATICTEXT51,
              label=u'Team defense', name='staticText51', parent=self.panel9,
              pos=wx.Point(40, 120), size=wx.Size(68, 14), style=0)

        self.team8AttackSpinCtrl1 = wx.SpinCtrl(id=wxID_FRAME1TEAM8ATTACKSPINCTRL1,
              initial=0, max=255, min=0, name=u'team8AttackSpinCtrl1',
              parent=self.panel9, pos=wx.Point(48, 80), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.team8AttackSpinCtrl1.Bind(wx.EVT_TEXT,
              self.OnTeam8AttackSpinCtrl1Text,
              id=wxID_FRAME1TEAM8ATTACKSPINCTRL1)

        self.team8DefenseSpinCtrl1 = wx.SpinCtrl(id=wxID_FRAME1TEAM8DEFENSESPINCTRL1,
              initial=0, max=7, min=0, name=u'team8DefenseSpinCtrl1',
              parent=self.panel9, pos=wx.Point(48, 152), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.team8DefenseSpinCtrl1.Bind(wx.EVT_TEXT,
              self.OnTeam8DefenseSpinCtrl1Text,
              id=wxID_FRAME1TEAM8DEFENSESPINCTRL1)

        self.staticText52 = wx.StaticText(id=wxID_FRAME1STATICTEXT52,
              label=u'Fall type', name='staticText52', parent=self.panel1,
              pos=wx.Point(560, 24), size=wx.Size(41, 14), style=0)

        self.fallTypeChoice = wx.Choice(choices=[],
              id=wxID_FRAME1FALLTYPECHOICE, name=u'fallTypeChoice',
              parent=self.panel1, pos=wx.Point(528, 40), size=wx.Size(106, 21),
              style=0)
        self.fallTypeChoice.Bind(wx.EVT_CHOICE, self.OnFallTypeChoiceChoice,
              id=wxID_FRAME1FALLTYPECHOICE)

        self.staticText53 = wx.StaticText(id=wxID_FRAME1STATICTEXT53,
              label=u'Fly type on hit', name='staticText53', parent=self.panel1,
              pos=wx.Point(640, 24), size=wx.Size(69, 14), style=0)

        self.flyHitSpinCtrl = wx.SpinCtrl(id=wxID_FRAME1FLYHITSPINCTRL,
              initial=0, max=15, min=0, name=u'flyHitSpinCtrl',
              parent=self.panel1, pos=wx.Point(656, 40), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.flyHitSpinCtrl.Bind(wx.EVT_TEXT, self.OnFlyHitSpinCtrlText,
              id=wxID_FRAME1FLYHITSPINCTRL)

        self.staticText54 = wx.StaticText(id=wxID_FRAME1STATICTEXT54,
              label=u'Fly type on shoot', name='staticText54',
              parent=self.panel1, pos=wx.Point(720, 24), size=wx.Size(84, 14),
              style=0)

        self.flyShootSpinCtrl = wx.SpinCtrl(id=wxID_FRAME1FLYSHOOTSPINCTRL,
              initial=0, max=15, min=0, name=u'flyShootSpinCtrl',
              parent=self.panel1, pos=wx.Point(736, 40), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.flyShootSpinCtrl.Bind(wx.EVT_TEXT, self.OnFlyShootSpinCtrlText,
              id=wxID_FRAME1FLYSHOOTSPINCTRL)

        self.displayPowTeam1Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYPOWTEAM1CTRL1,
              initial=1, max=999, min=1, name=u'displayPowTeam1Ctrl1',
              parent=self.panel2, pos=wx.Point(712, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayPowTeam1Ctrl1.Bind(wx.EVT_TEXT,
              self.OnDisplayPowTeam1Ctrl1Text,
              id=wxID_FRAME1DISPLAYPOWTEAM1CTRL1)

        self.displaySpdTeam1Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYSPDTEAM1CTRL1,
              initial=1, max=999, min=1, name=u'displaySpdTeam1Ctrl1',
              parent=self.panel2, pos=wx.Point(768, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displaySpdTeam1Ctrl1.Bind(wx.EVT_TEXT,
              self.OnDisplaySpdTeam1Ctrl1Text,
              id=wxID_FRAME1DISPLAYSPDTEAM1CTRL1)

        self.displayDefTeam1Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYDEFTEAM1CTRL1,
              initial=1, max=999, min=1, name=u'displayDefTeam1Ctrl1',
              parent=self.panel2, pos=wx.Point(824, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayDefTeam1Ctrl1.Bind(wx.EVT_TEXT,
              self.OnDisplayDefTeam1Ctrl1Text,
              id=wxID_FRAME1DISPLAYDEFTEAM1CTRL1)

        self.staticText56 = wx.StaticText(id=wxID_FRAME1STATICTEXT56,
              label=u'POW', name='staticText56', parent=self.panel2,
              pos=wx.Point(720, 40), size=wx.Size(24, 14), style=0)

        self.staticText57 = wx.StaticText(id=wxID_FRAME1STATICTEXT57,
              label=u'SPD', name='staticText57', parent=self.panel2,
              pos=wx.Point(776, 40), size=wx.Size(24, 14), style=0)

        self.staticText58 = wx.StaticText(id=wxID_FRAME1STATICTEXT58,
              label=u'DEF', name='staticText58', parent=self.panel2,
              pos=wx.Point(832, 40), size=wx.Size(24, 14), style=0)

        self.displayPowTeam1Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYPOWTEAM1CTRL2,
              initial=1, max=999, min=1, name=u'displayPowTeam1Ctrl2',
              parent=self.panel2, pos=wx.Point(712, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayPowTeam1Ctrl2.Bind(wx.EVT_TEXT,
              self.OnDisplayPowTeam1Ctrl2Text,
              id=wxID_FRAME1DISPLAYPOWTEAM1CTRL2)

        self.displaySpdTeam1Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYSPDTEAM1CTRL2,
              initial=1, max=999, min=1, name=u'displaySpdTeam1Ctrl2',
              parent=self.panel2, pos=wx.Point(768, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displaySpdTeam1Ctrl2.Bind(wx.EVT_TEXT,
              self.OnDisplaySpdTeam1Ctrl2Text,
              id=wxID_FRAME1DISPLAYSPDTEAM1CTRL2)

        self.displayDefTeam1Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYDEFTEAM1CTRL2,
              initial=1, max=999, min=1, name=u'displayDefTeam1Ctrl2',
              parent=self.panel2, pos=wx.Point(824, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayDefTeam1Ctrl2.Bind(wx.EVT_TEXT,
              self.OnDisplayDefTeam1Ctrl2Text,
              id=wxID_FRAME1DISPLAYDEFTEAM1CTRL2)

        self.displayPowTeam1Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYPOWTEAM1CTRL3,
              initial=1, max=999, min=1, name=u'displayPowTeam1Ctrl3',
              parent=self.panel2, pos=wx.Point(712, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayPowTeam1Ctrl3.Bind(wx.EVT_TEXT,
              self.OnDisplayPowTeam1Ctrl3Text,
              id=wxID_FRAME1DISPLAYPOWTEAM1CTRL3)

        self.displaySpdTeam1Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYSPDTEAM1CTRL3,
              initial=1, max=999, min=1, name=u'displaySpdTeam1Ctrl3',
              parent=self.panel2, pos=wx.Point(768, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displaySpdTeam1Ctrl3.Bind(wx.EVT_TEXT,
              self.OnDisplaySpdTeam1Ctrl3Text,
              id=wxID_FRAME1DISPLAYSPDTEAM1CTRL3)

        self.displayDefTeam1Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYDEFTEAM1CTRL3,
              initial=1, max=999, min=1, name=u'displayDefTeam1Ctrl3',
              parent=self.panel2, pos=wx.Point(824, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayDefTeam1Ctrl3.Bind(wx.EVT_TEXT,
              self.OnDisplayDefTeam1Ctrl3Text,
              id=wxID_FRAME1DISPLAYDEFTEAM1CTRL3)

        self.displayPowTeam1Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYPOWTEAM1CTRL4,
              initial=1, max=999, min=1, name=u'displayPowTeam1Ctrl4',
              parent=self.panel2, pos=wx.Point(712, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayPowTeam1Ctrl4.Bind(wx.EVT_TEXT,
              self.OnDisplayPowTeam1Ctrl4Text,
              id=wxID_FRAME1DISPLAYPOWTEAM1CTRL4)

        self.displaySpdTeam1Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYSPDTEAM1CTRL4,
              initial=1, max=999, min=1, name=u'displaySpdTeam1Ctrl4',
              parent=self.panel2, pos=wx.Point(768, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displaySpdTeam1Ctrl4.Bind(wx.EVT_TEXT,
              self.OnDisplaySpdTeam1Ctrl4Text,
              id=wxID_FRAME1DISPLAYSPDTEAM1CTRL4)

        self.displayDefTeam1Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYDEFTEAM1CTRL4,
              initial=1, max=999, min=1, name=u'displayDefTeam1Ctrl4',
              parent=self.panel2, pos=wx.Point(824, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayDefTeam1Ctrl4.Bind(wx.EVT_TEXT,
              self.OnDisplayDefTeam1Ctrl4Text,
              id=wxID_FRAME1DISPLAYDEFTEAM1CTRL4)

        self.displayPowTeam1Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYPOWTEAM1CTRL5,
              initial=1, max=999, min=1, name=u'displayPowTeam1Ctrl5',
              parent=self.panel2, pos=wx.Point(712, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayPowTeam1Ctrl5.Bind(wx.EVT_TEXT,
              self.OnDisplayPowTeam1Ctrl5Text,
              id=wxID_FRAME1DISPLAYPOWTEAM1CTRL5)

        self.displaySpdTeam1Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYSPDTEAM1CTRL5,
              initial=1, max=999, min=1, name=u'displaySpdTeam1Ctrl5',
              parent=self.panel2, pos=wx.Point(768, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displaySpdTeam1Ctrl5.Bind(wx.EVT_TEXT,
              self.OnDisplaySpdTeam1Ctrl5Text,
              id=wxID_FRAME1DISPLAYSPDTEAM1CTRL5)

        self.displayDefTeam1Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYDEFTEAM1CTRL5,
              initial=1, max=999, min=1, name=u'displayDefTeam1Ctrl5',
              parent=self.panel2, pos=wx.Point(824, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayDefTeam1Ctrl5.Bind(wx.EVT_TEXT,
              self.OnDisplayDefTeam1Ctrl5Text,
              id=wxID_FRAME1DISPLAYDEFTEAM1CTRL5)

        self.sPowerSpinTeam2Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1SPOWERSPINTEAM2CTRL1,
              initial=1, max=12, min=1, name=u'sPowerSpinTeam2Ctrl1',
              parent=self.panel3, pos=wx.Point(240, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.sPowerSpinTeam2Ctrl1.Bind(wx.EVT_TEXT,
              self.OnSPowerSpinTeam2Ctrl1Text,
              id=wxID_FRAME1SPOWERSPINTEAM2CTRL1)

        self.sPowerSpinTeam2Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1SPOWERSPINTEAM2CTRL2,
              initial=1, max=12, min=1, name=u'sPowerSpinTeam2Ctrl2',
              parent=self.panel3, pos=wx.Point(240, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.sPowerSpinTeam2Ctrl2.Bind(wx.EVT_TEXT,
              self.OnSPowerSpinTeam2Ctrl2Text,
              id=wxID_FRAME1SPOWERSPINTEAM2CTRL2)

        self.sPowerSpinTeam2Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1SPOWERSPINTEAM2CTRL3,
              initial=1, max=12, min=1, name=u'sPowerSpinTeam2Ctrl3',
              parent=self.panel3, pos=wx.Point(240, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.sPowerSpinTeam2Ctrl3.Bind(wx.EVT_TEXT,
              self.OnSPowerSpinTeam2Ctrl3Text,
              id=wxID_FRAME1SPOWERSPINTEAM2CTRL3)

        self.sPowerSpinTeam2Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1SPOWERSPINTEAM2CTRL4,
              initial=1, max=12, min=1, name=u'sPowerSpinTeam2Ctrl4',
              parent=self.panel3, pos=wx.Point(240, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.sPowerSpinTeam2Ctrl4.Bind(wx.EVT_TEXT,
              self.OnSPowerSpinTeam2Ctrl4Text,
              id=wxID_FRAME1SPOWERSPINTEAM2CTRL4)

        self.sPowerSpinTeam2Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1SPOWERSPINTEAM2CTRL5,
              initial=1, max=12, min=1, name=u'sPowerSpinTeam2Ctrl5',
              parent=self.panel3, pos=wx.Point(240, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.sPowerSpinTeam2Ctrl5.Bind(wx.EVT_TEXT,
              self.OnSPowerSpinTeam2Ctrl5Text,
              id=wxID_FRAME1SPOWERSPINTEAM2CTRL5)

        self.mPowerSpinTeam2Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1MPOWERSPINTEAM2CTRL1,
              initial=1, max=5, min=1, name=u'mPowerSpinTeam2Ctrl1',
              parent=self.panel3, pos=wx.Point(312, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.mPowerSpinTeam2Ctrl1.Bind(wx.EVT_TEXT,
              self.OnMPowerSpinTeam2Ctrl1Text,
              id=wxID_FRAME1MPOWERSPINTEAM2CTRL1)

        self.mPowerSpinTeam2Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1MPOWERSPINTEAM2CTRL2,
              initial=1, max=5, min=1, name=u'mPowerSpinTeam2Ctrl2',
              parent=self.panel3, pos=wx.Point(312, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.mPowerSpinTeam2Ctrl2.Bind(wx.EVT_TEXT,
              self.OnMPowerSpinTeam2Ctrl2Text,
              id=wxID_FRAME1MPOWERSPINTEAM2CTRL2)

        self.mPowerSpinTeam2Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1MPOWERSPINTEAM2CTRL3,
              initial=1, max=5, min=1, name=u'mPowerSpinTeam2Ctrl3',
              parent=self.panel3, pos=wx.Point(312, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.mPowerSpinTeam2Ctrl3.Bind(wx.EVT_TEXT,
              self.OnMPowerSpinTeam2Ctrl3Text,
              id=wxID_FRAME1MPOWERSPINTEAM2CTRL3)

        self.mPowerSpinTeam2Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1MPOWERSPINTEAM2CTRL4,
              initial=1, max=5, min=1, name=u'mPowerSpinTeam2Ctrl4',
              parent=self.panel3, pos=wx.Point(312, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.mPowerSpinTeam2Ctrl4.Bind(wx.EVT_TEXT,
              self.OnMPowerSpinTeam2Ctrl4Text,
              id=wxID_FRAME1MPOWERSPINTEAM2CTRL4)

        self.mPowerSpinTeam2Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1MPOWERSPINTEAM2CTRL5,
              initial=1, max=5, min=1, name=u'mPowerSpinTeam2Ctrl5',
              parent=self.panel3, pos=wx.Point(312, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.mPowerSpinTeam2Ctrl5.Bind(wx.EVT_TEXT,
              self.OnMPowerSpinTeam2Ctrl5Text,
              id=wxID_FRAME1MPOWERSPINTEAM2CTRL5)

        self.speedSpinTeam2Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1SPEEDSPINTEAM2CTRL1,
              initial=1, max=3, min=1, name=u'speedSpinTeam2Ctrl1',
              parent=self.panel3, pos=wx.Point(384, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.speedSpinTeam2Ctrl1.Bind(wx.EVT_TEXT,
              self.OnSpeedSpinTeam2Ctrl1Text,
              id=wxID_FRAME1SPEEDSPINTEAM2CTRL1)

        self.speedSpinTeam2Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1SPEEDSPINTEAM2CTRL2,
              initial=1, max=3, min=1, name=u'speedSpinTeam2Ctrl2',
              parent=self.panel3, pos=wx.Point(384, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.speedSpinTeam2Ctrl2.Bind(wx.EVT_TEXT,
              self.OnSpeedSpinTeam2Ctrl2Text,
              id=wxID_FRAME1SPEEDSPINTEAM2CTRL2)

        self.speedSpinTeam2Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1SPEEDSPINTEAM2CTRL3,
              initial=1, max=3, min=1, name=u'speedSpinTeam2Ctrl3',
              parent=self.panel3, pos=wx.Point(384, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.speedSpinTeam2Ctrl3.Bind(wx.EVT_TEXT,
              self.OnSpeedSpinTeam2Ctrl3Text,
              id=wxID_FRAME1SPEEDSPINTEAM2CTRL3)

        self.speedSpinTeam2Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1SPEEDSPINTEAM2CTRL4,
              initial=1, max=3, min=1, name=u'speedSpinTeam2Ctrl4',
              parent=self.panel3, pos=wx.Point(384, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.speedSpinTeam2Ctrl4.Bind(wx.EVT_TEXT,
              self.OnSpeedSpinTeam2Ctrl4Text,
              id=wxID_FRAME1SPEEDSPINTEAM2CTRL4)

        self.speedSpinTeam2Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1SPEEDSPINTEAM2CTRL5,
              initial=1, max=3, min=1, name=u'speedSpinTeam2Ctrl5',
              parent=self.panel3, pos=wx.Point(384, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.speedSpinTeam2Ctrl5.Bind(wx.EVT_TEXT,
              self.OnSpeedSpinTeam2Ctrl5Text,
              id=wxID_FRAME1SPEEDSPINTEAM2CTRL5)

        self.weightSpinTeam2Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1WEIGHTSPINTEAM2CTRL1,
              initial=1, max=5, min=1, name=u'weightSpinTeam2Ctrl1',
              parent=self.panel3, pos=wx.Point(456, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.weightSpinTeam2Ctrl1.Bind(wx.EVT_TEXT,
              self.OnWeightSpinTeam2Ctrl1Text,
              id=wxID_FRAME1WEIGHTSPINTEAM2CTRL1)

        self.weightSpinTeam2Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1WEIGHTSPINTEAM2CTRL2,
              initial=1, max=5, min=1, name=u'weightSpinTeam2Ctrl2',
              parent=self.panel3, pos=wx.Point(456, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.weightSpinTeam2Ctrl2.Bind(wx.EVT_TEXT,
              self.OnWeightSpinTeam2Ctrl2Text,
              id=wxID_FRAME1WEIGHTSPINTEAM2CTRL2)

        self.weightSpinTeam2Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1WEIGHTSPINTEAM2CTRL3,
              initial=1, max=5, min=1, name=u'weightSpinTeam2Ctrl3',
              parent=self.panel3, pos=wx.Point(456, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.weightSpinTeam2Ctrl3.Bind(wx.EVT_TEXT,
              self.OnWeightSpinTeam2Ctrl3Text,
              id=wxID_FRAME1WEIGHTSPINTEAM2CTRL3)

        self.weightSpinTeam2Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1WEIGHTSPINTEAM2CTRL4,
              initial=1, max=5, min=1, name=u'weightSpinTeam2Ctrl4',
              parent=self.panel3, pos=wx.Point(456, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.weightSpinTeam2Ctrl4.Bind(wx.EVT_TEXT,
              self.OnWeightSpinTeam2Ctrl4Text,
              id=wxID_FRAME1WEIGHTSPINTEAM2CTRL4)

        self.weightSpinTeam2Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1WEIGHTSPINTEAM2CTRL5,
              initial=1, max=5, min=1, name=u'weightSpinTeam2Ctrl5',
              parent=self.panel3, pos=wx.Point(456, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.weightSpinTeam2Ctrl5.Bind(wx.EVT_TEXT,
              self.OnWeightSpinTeam2Ctrl5Text,
              id=wxID_FRAME1WEIGHTSPINTEAM2CTRL5)

        self.angrySpinTeam2Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1ANGRYSPINTEAM2CTRL1,
              initial=1, max=7, min=1, name=u'angrySpinTeam2Ctrl1',
              parent=self.panel3, pos=wx.Point(528, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.angrySpinTeam2Ctrl1.Bind(wx.EVT_TEXT,
              self.OnAngrySpinTeam2Ctrl1Text,
              id=wxID_FRAME1ANGRYSPINTEAM2CTRL1)

        self.angrySpinTeam2Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1ANGRYSPINTEAM2CTRL2,
              initial=1, max=7, min=1, name=u'angrySpinTeam2Ctrl2',
              parent=self.panel3, pos=wx.Point(528, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.angrySpinTeam2Ctrl2.Bind(wx.EVT_TEXT,
              self.OnAngrySpinTeam2Ctrl2Text,
              id=wxID_FRAME1ANGRYSPINTEAM2CTRL2)

        self.angrySpinTeam2Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1ANGRYSPINTEAM2CTRL3,
              initial=1, max=7, min=1, name=u'angrySpinTeam2Ctrl3',
              parent=self.panel3, pos=wx.Point(528, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.angrySpinTeam2Ctrl3.Bind(wx.EVT_TEXT,
              self.OnAngrySpinTeam2Ctrl3Text,
              id=wxID_FRAME1ANGRYSPINTEAM2CTRL3)

        self.angrySpinTeam2Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1ANGRYSPINTEAM2CTRL4,
              initial=1, max=7, min=1, name=u'angrySpinTeam2Ctrl4',
              parent=self.panel3, pos=wx.Point(528, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.angrySpinTeam2Ctrl4.Bind(wx.EVT_TEXT,
              self.OnAngrySpinTeam2Ctrl4Text,
              id=wxID_FRAME1ANGRYSPINTEAM2CTRL4)

        self.angrySpinTeam2Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1ANGRYSPINTEAM2CTRL5,
              initial=1, max=7, min=1, name=u'angrySpinTeam2Ctrl5',
              parent=self.panel3, pos=wx.Point(528, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.angrySpinTeam2Ctrl5.Bind(wx.EVT_TEXT,
              self.OnAngrySpinTeam2Ctrl5Text,
              id=wxID_FRAME1ANGRYSPINTEAM2CTRL5)

        self.shootTeam2Choice1 = wx.Choice(choices=[],
              id=wxID_FRAME1SHOOTTEAM2CHOICE1, name=u'shootTeam2Choice1',
              parent=self.panel3, pos=wx.Point(592, 64), size=wx.Size(106, 21),
              style=0)
        self.shootTeam2Choice1.Bind(wx.EVT_CHOICE,
              self.OnShootTeam2Choice1Choice, id=wxID_FRAME1SHOOTTEAM2CHOICE1)

        self.shootTeam2Choice2 = wx.Choice(choices=[],
              id=wxID_FRAME1SHOOTTEAM2CHOICE2, name=u'shootTeam2Choice2',
              parent=self.panel3, pos=wx.Point(592, 96), size=wx.Size(106, 21),
              style=0)
        self.shootTeam2Choice2.Bind(wx.EVT_CHOICE,
              self.OnShootTeam2Choice2Choice, id=wxID_FRAME1SHOOTTEAM2CHOICE2)

        self.shootTeam2Choice3 = wx.Choice(choices=[],
              id=wxID_FRAME1SHOOTTEAM2CHOICE3, name=u'shootTeam2Choice3',
              parent=self.panel3, pos=wx.Point(592, 128), size=wx.Size(106, 21),
              style=0)
        self.shootTeam2Choice3.Bind(wx.EVT_CHOICE,
              self.OnShootTeam2Choice3Choice, id=wxID_FRAME1SHOOTTEAM2CHOICE3)

        self.shootTeam2Choice4 = wx.Choice(choices=[],
              id=wxID_FRAME1SHOOTTEAM2CHOICE4, name=u'shootTeam2Choice4',
              parent=self.panel3, pos=wx.Point(592, 160), size=wx.Size(106, 21),
              style=0)
        self.shootTeam2Choice4.Bind(wx.EVT_CHOICE,
              self.OnShootTeam2Choice4Choice, id=wxID_FRAME1SHOOTTEAM2CHOICE4)

        self.shootTeam2Choice5 = wx.Choice(choices=[],
              id=wxID_FRAME1SHOOTTEAM2CHOICE5, name=u'shootTeam2Choice5',
              parent=self.panel3, pos=wx.Point(592, 192), size=wx.Size(106, 21),
              style=0)
        self.shootTeam2Choice5.Bind(wx.EVT_CHOICE,
              self.OnShootTeam2Choice5Choice, id=wxID_FRAME1SHOOTTEAM2CHOICE5)

        self.displayPowTeam2Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYPOWTEAM2CTRL1,
              initial=1, max=999, min=1, name=u'displayPowTeam2Ctrl1',
              parent=self.panel3, pos=wx.Point(712, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayPowTeam2Ctrl1.Bind(wx.EVT_TEXT,
              self.OnDisplayPowTeam2Ctrl1Text,
              id=wxID_FRAME1DISPLAYPOWTEAM2CTRL1)

        self.displayPowTeam2Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYPOWTEAM2CTRL2,
              initial=1, max=999, min=1, name=u'displayPowTeam2Ctrl2',
              parent=self.panel3, pos=wx.Point(712, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayPowTeam2Ctrl2.Bind(wx.EVT_TEXT,
              self.OnDisplayPowTeam2Ctrl2Text,
              id=wxID_FRAME1DISPLAYPOWTEAM2CTRL2)

        self.displayPowTeam2Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYPOWTEAM2CTRL3,
              initial=1, max=999, min=1, name=u'displayPowTeam2Ctrl3',
              parent=self.panel3, pos=wx.Point(712, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayPowTeam2Ctrl3.Bind(wx.EVT_TEXT,
              self.OnDisplayPowTeam2Ctrl3Text,
              id=wxID_FRAME1DISPLAYPOWTEAM2CTRL3)

        self.displayPowTeam2Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYPOWTEAM2CTRL4,
              initial=1, max=999, min=1, name=u'displayPowTeam2Ctrl4',
              parent=self.panel3, pos=wx.Point(712, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayPowTeam2Ctrl4.Bind(wx.EVT_TEXT,
              self.OnDisplayPowTeam2Ctrl4Text,
              id=wxID_FRAME1DISPLAYPOWTEAM2CTRL4)

        self.displayPowTeam2Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYPOWTEAM2CTRL5,
              initial=1, max=999, min=1, name=u'displayPowTeam2Ctrl5',
              parent=self.panel3, pos=wx.Point(712, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayPowTeam2Ctrl5.Bind(wx.EVT_TEXT,
              self.OnDisplayPowTeam2Ctrl5Text,
              id=wxID_FRAME1DISPLAYPOWTEAM2CTRL5)

        self.displaySpdTeam2Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYSPDTEAM2CTRL1,
              initial=1, max=999, min=1, name=u'displaySpdTeam2Ctrl1',
              parent=self.panel3, pos=wx.Point(768, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displaySpdTeam2Ctrl1.Bind(wx.EVT_TEXT,
              self.OnDisplaySpdTeam2Ctrl1Text,
              id=wxID_FRAME1DISPLAYSPDTEAM2CTRL1)

        self.displaySpdTeam2Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYSPDTEAM2CTRL2,
              initial=1, max=999, min=1, name=u'displaySpdTeam2Ctrl2',
              parent=self.panel3, pos=wx.Point(768, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displaySpdTeam2Ctrl2.Bind(wx.EVT_TEXT,
              self.OnDisplaySpdTeam2Ctrl2Text,
              id=wxID_FRAME1DISPLAYSPDTEAM2CTRL2)

        self.displaySpdTeam2Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYSPDTEAM2CTRL3,
              initial=1, max=999, min=1, name=u'displaySpdTeam2Ctrl3',
              parent=self.panel3, pos=wx.Point(768, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displaySpdTeam2Ctrl3.Bind(wx.EVT_TEXT,
              self.OnDisplaySpdTeam2Ctrl3Text,
              id=wxID_FRAME1DISPLAYSPDTEAM2CTRL3)

        self.displaySpdTeam2Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYSPDTEAM2CTRL4,
              initial=1, max=999, min=1, name=u'displaySpdTeam2Ctrl4',
              parent=self.panel3, pos=wx.Point(768, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displaySpdTeam2Ctrl4.Bind(wx.EVT_TEXT,
              self.OnDisplaySpdTeam2Ctrl4Text,
              id=wxID_FRAME1DISPLAYSPDTEAM2CTRL4)

        self.displaySpdTeam2Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYSPDTEAM2CTRL5,
              initial=1, max=999, min=1, name=u'displaySpdTeam2Ctrl5',
              parent=self.panel3, pos=wx.Point(768, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displaySpdTeam2Ctrl5.Bind(wx.EVT_TEXT,
              self.OnDisplaySpdTeam2Ctrl5Text,
              id=wxID_FRAME1DISPLAYSPDTEAM2CTRL5)

        self.displayDefTeam2Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYDEFTEAM2CTRL1,
              initial=1, max=999, min=1, name=u'displayDefTeam2Ctrl1',
              parent=self.panel3, pos=wx.Point(824, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayDefTeam2Ctrl1.Bind(wx.EVT_TEXT,
              self.OnDisplayDefTeam2Ctrl1Text,
              id=wxID_FRAME1DISPLAYDEFTEAM2CTRL1)

        self.displayDefTeam2Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYDEFTEAM2CTRL2,
              initial=1, max=999, min=1, name=u'displayDefTeam2Ctrl2',
              parent=self.panel3, pos=wx.Point(824, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayDefTeam2Ctrl2.Bind(wx.EVT_TEXT,
              self.OnDisplayDefTeam2Ctrl2Text,
              id=wxID_FRAME1DISPLAYDEFTEAM2CTRL2)

        self.displayDefTeam2Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYDEFTEAM2CTRL3,
              initial=1, max=999, min=1, name=u'displayDefTeam2Ctrl3',
              parent=self.panel3, pos=wx.Point(824, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayDefTeam2Ctrl3.Bind(wx.EVT_TEXT,
              self.OnDisplayDefTeam2Ctrl3Text,
              id=wxID_FRAME1DISPLAYDEFTEAM2CTRL3)

        self.displayDefTeam2Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYDEFTEAM2CTRL4,
              initial=1, max=999, min=1, name=u'displayDefTeam2Ctrl4',
              parent=self.panel3, pos=wx.Point(824, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayDefTeam2Ctrl4.Bind(wx.EVT_TEXT,
              self.OnDisplayDefTeam2Ctrl4Text,
              id=wxID_FRAME1DISPLAYDEFTEAM2CTRL4)

        self.displayDefTeam2Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYDEFTEAM2CTRL5,
              initial=1, max=999, min=1, name=u'displayDefTeam2Ctrl5',
              parent=self.panel3, pos=wx.Point(824, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayDefTeam2Ctrl5.Bind(wx.EVT_TEXT,
              self.OnDisplayDefTeam2Ctrl5Text,
              id=wxID_FRAME1DISPLAYDEFTEAM2CTRL5)

        self.staticText59 = wx.StaticText(id=wxID_FRAME1STATICTEXT59,
              label=u'Start Power', name='staticText59', parent=self.panel3,
              pos=wx.Point(232, 40), size=wx.Size(57, 14), style=0)

        self.staticText60 = wx.StaticText(id=wxID_FRAME1STATICTEXT60,
              label=u'Max Power', name='staticText60', parent=self.panel3,
              pos=wx.Point(312, 40), size=wx.Size(53, 14), style=0)

        self.staticText61 = wx.StaticText(id=wxID_FRAME1STATICTEXT61,
              label=u'Speed', name='staticText61', parent=self.panel3,
              pos=wx.Point(392, 40), size=wx.Size(30, 14), style=0)

        self.staticText62 = wx.StaticText(id=wxID_FRAME1STATICTEXT62,
              label=u'Weight', name='staticText62', parent=self.panel3,
              pos=wx.Point(464, 40), size=wx.Size(34, 14), style=0)

        self.staticText63 = wx.StaticText(id=wxID_FRAME1STATICTEXT63,
              label=u'Angry', name='staticText63', parent=self.panel3,
              pos=wx.Point(536, 40), size=wx.Size(29, 14), style=0)

        self.staticText64 = wx.StaticText(id=wxID_FRAME1STATICTEXT64,
              label=u'Special Shoot', name='staticText64', parent=self.panel3,
              pos=wx.Point(608, 40), size=wx.Size(64, 14), style=0)

        self.staticText65 = wx.StaticText(id=wxID_FRAME1STATICTEXT65,
              label=u'POW', name='staticText65', parent=self.panel3,
              pos=wx.Point(720, 40), size=wx.Size(24, 14), style=0)

        self.staticText66 = wx.StaticText(id=wxID_FRAME1STATICTEXT66,
              label=u'SPD', name='staticText66', parent=self.panel3,
              pos=wx.Point(776, 40), size=wx.Size(19, 14), style=0)

        self.staticText67 = wx.StaticText(id=wxID_FRAME1STATICTEXT67,
              label=u'DEF', name='staticText67', parent=self.panel3,
              pos=wx.Point(832, 40), size=wx.Size(19, 14), style=0)

        self.sPowerSpinTeam3Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1SPOWERSPINTEAM3CTRL1,
              initial=1, max=12, min=1, name=u'sPowerSpinTeam3Ctrl1',
              parent=self.panel4, pos=wx.Point(240, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.sPowerSpinTeam3Ctrl1.Bind(wx.EVT_TEXT,
              self.OnSPowerSpinTeam3Ctrl1Text,
              id=wxID_FRAME1SPOWERSPINTEAM3CTRL1)

        self.sPowerSpinTeam3Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1SPOWERSPINTEAM3CTRL2,
              initial=1, max=12, min=1, name=u'sPowerSpinTeam3Ctrl2',
              parent=self.panel4, pos=wx.Point(240, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.sPowerSpinTeam3Ctrl2.Bind(wx.EVT_TEXT,
              self.OnSPowerSpinTeam3Ctrl2Text,
              id=wxID_FRAME1SPOWERSPINTEAM3CTRL2)

        self.sPowerSpinTeam3Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1SPOWERSPINTEAM3CTRL3,
              initial=1, max=12, min=1, name=u'sPowerSpinTeam3Ctrl3',
              parent=self.panel4, pos=wx.Point(240, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.sPowerSpinTeam3Ctrl3.Bind(wx.EVT_TEXT,
              self.OnSPowerSpinTeam3Ctrl3Text,
              id=wxID_FRAME1SPOWERSPINTEAM3CTRL3)

        self.sPowerSpinTeam3Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1SPOWERSPINTEAM3CTRL4,
              initial=1, max=12, min=1, name=u'sPowerSpinTeam3Ctrl4',
              parent=self.panel4, pos=wx.Point(240, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.sPowerSpinTeam3Ctrl4.Bind(wx.EVT_TEXT,
              self.OnSPowerSpinTeam3Ctrl4Text,
              id=wxID_FRAME1SPOWERSPINTEAM3CTRL4)

        self.sPowerSpinTeam3Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1SPOWERSPINTEAM3CTRL5,
              initial=1, max=12, min=1, name=u'sPowerSpinTeam3Ctrl5',
              parent=self.panel4, pos=wx.Point(240, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.sPowerSpinTeam3Ctrl5.Bind(wx.EVT_TEXT,
              self.OnSPowerSpinTeam3Ctrl5Text,
              id=wxID_FRAME1SPOWERSPINTEAM3CTRL5)

        self.mPowerSpinTeam3Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1MPOWERSPINTEAM3CTRL1,
              initial=1, max=5, min=1, name=u'mPowerSpinTeam3Ctrl1',
              parent=self.panel4, pos=wx.Point(312, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.mPowerSpinTeam3Ctrl1.Bind(wx.EVT_TEXT,
              self.OnMPowerSpinTeam3Ctrl1Text,
              id=wxID_FRAME1MPOWERSPINTEAM3CTRL1)

        self.mPowerSpinTeam3Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1MPOWERSPINTEAM3CTRL2,
              initial=1, max=5, min=1, name=u'mPowerSpinTeam3Ctrl2',
              parent=self.panel4, pos=wx.Point(312, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.mPowerSpinTeam3Ctrl2.Bind(wx.EVT_TEXT,
              self.OnMPowerSpinTeam3Ctrl2Text,
              id=wxID_FRAME1MPOWERSPINTEAM3CTRL2)

        self.mPowerSpinTeam3Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1MPOWERSPINTEAM3CTRL3,
              initial=1, max=5, min=1, name=u'mPowerSpinTeam3Ctrl3',
              parent=self.panel4, pos=wx.Point(312, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.mPowerSpinTeam3Ctrl3.Bind(wx.EVT_TEXT,
              self.OnMPowerSpinTeam3Ctrl3Text,
              id=wxID_FRAME1MPOWERSPINTEAM3CTRL3)

        self.mPowerSpinTeam3Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1MPOWERSPINTEAM3CTRL4,
              initial=1, max=5, min=1, name=u'mPowerSpinTeam3Ctrl4',
              parent=self.panel4, pos=wx.Point(312, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.mPowerSpinTeam3Ctrl4.Bind(wx.EVT_TEXT,
              self.OnMPowerSpinTeam3Ctrl4Text,
              id=wxID_FRAME1MPOWERSPINTEAM3CTRL4)

        self.mPowerSpinTeam3Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1MPOWERSPINTEAM3CTRL5,
              initial=1, max=5, min=1, name=u'mPowerSpinTeam3Ctrl5',
              parent=self.panel4, pos=wx.Point(312, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.mPowerSpinTeam3Ctrl5.Bind(wx.EVT_TEXT,
              self.OnMPowerSpinTeam3Ctrl5Text,
              id=wxID_FRAME1MPOWERSPINTEAM3CTRL5)

        self.speedSpinTeam3Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1SPEEDSPINTEAM3CTRL1,
              initial=1, max=3, min=1, name=u'speedSpinTeam3Ctrl1',
              parent=self.panel4, pos=wx.Point(384, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.speedSpinTeam3Ctrl1.Bind(wx.EVT_TEXT,
              self.OnSpeedSpinTeam3Ctrl1Text,
              id=wxID_FRAME1SPEEDSPINTEAM3CTRL1)

        self.speedSpinTeam3Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1SPEEDSPINTEAM3CTRL2,
              initial=1, max=3, min=1, name=u'speedSpinTeam3Ctrl2',
              parent=self.panel4, pos=wx.Point(384, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.speedSpinTeam3Ctrl2.Bind(wx.EVT_TEXT,
              self.OnSpeedSpinTeam3Ctrl2Text,
              id=wxID_FRAME1SPEEDSPINTEAM3CTRL2)

        self.speedSpinTeam3Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1SPEEDSPINTEAM3CTRL3,
              initial=1, max=3, min=1, name=u'speedSpinTeam3Ctrl3',
              parent=self.panel4, pos=wx.Point(384, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.speedSpinTeam3Ctrl3.Bind(wx.EVT_TEXT,
              self.OnSpeedSpinTeam3Ctrl3Text,
              id=wxID_FRAME1SPEEDSPINTEAM3CTRL3)

        self.speedSpinTeam3Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1SPEEDSPINTEAM3CTRL4,
              initial=1, max=3, min=1, name=u'speedSpinTeam3Ctrl4',
              parent=self.panel4, pos=wx.Point(384, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.speedSpinTeam3Ctrl4.Bind(wx.EVT_TEXT,
              self.OnSpeedSpinTeam3Ctrl4Text,
              id=wxID_FRAME1SPEEDSPINTEAM3CTRL4)

        self.speedSpinTeam3Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1SPEEDSPINTEAM3CTRL5,
              initial=1, max=3, min=1, name=u'speedSpinTeam3Ctrl5',
              parent=self.panel4, pos=wx.Point(384, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.speedSpinTeam3Ctrl5.Bind(wx.EVT_TEXT,
              self.OnSpeedSpinTeam3Ctrl5Text,
              id=wxID_FRAME1SPEEDSPINTEAM3CTRL5)

        self.weightSpinTeam3Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1WEIGHTSPINTEAM3CTRL1,
              initial=1, max=5, min=1, name=u'weightSpinTeam3Ctrl1',
              parent=self.panel4, pos=wx.Point(456, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.weightSpinTeam3Ctrl1.Bind(wx.EVT_TEXT,
              self.OnWeightSpinTeam3Ctrl1Text,
              id=wxID_FRAME1WEIGHTSPINTEAM3CTRL1)

        self.weightSpinTeam3Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1WEIGHTSPINTEAM3CTRL2,
              initial=1, max=5, min=1, name=u'weightSpinTeam3Ctrl2',
              parent=self.panel4, pos=wx.Point(456, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.weightSpinTeam3Ctrl2.Bind(wx.EVT_TEXT,
              self.OnWeightSpinTeam3Ctrl2Text,
              id=wxID_FRAME1WEIGHTSPINTEAM3CTRL2)

        self.weightSpinTeam3Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1WEIGHTSPINTEAM3CTRL3,
              initial=1, max=5, min=1, name=u'weightSpinTeam3Ctrl3',
              parent=self.panel4, pos=wx.Point(456, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.weightSpinTeam3Ctrl3.Bind(wx.EVT_TEXT,
              self.OnWeightSpinTeam3Ctrl3Text,
              id=wxID_FRAME1WEIGHTSPINTEAM3CTRL3)

        self.weightSpinTeam3Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1WEIGHTSPINTEAM3CTRL4,
              initial=1, max=5, min=1, name=u'weightSpinTeam3Ctrl4',
              parent=self.panel4, pos=wx.Point(456, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.weightSpinTeam3Ctrl4.Bind(wx.EVT_TEXT,
              self.OnWeightSpinTeam3Ctrl4Text,
              id=wxID_FRAME1WEIGHTSPINTEAM3CTRL4)

        self.weightSpinTeam3Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1WEIGHTSPINTEAM3CTRL5,
              initial=1, max=5, min=1, name=u'weightSpinTeam3Ctrl5',
              parent=self.panel4, pos=wx.Point(456, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.weightSpinTeam3Ctrl5.Bind(wx.EVT_TEXT,
              self.OnWeightSpinTeam3Ctrl5Text,
              id=wxID_FRAME1WEIGHTSPINTEAM3CTRL5)

        self.angrySpinTeam3Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1ANGRYSPINTEAM3CTRL1,
              initial=1, max=7, min=1, name=u'angrySpinTeam3Ctrl1',
              parent=self.panel4, pos=wx.Point(528, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.angrySpinTeam3Ctrl1.Bind(wx.EVT_TEXT,
              self.OnAngrySpinTeam3Ctrl1Text,
              id=wxID_FRAME1ANGRYSPINTEAM3CTRL1)

        self.angrySpinTeam3Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1ANGRYSPINTEAM3CTRL2,
              initial=1, max=7, min=1, name=u'angrySpinTeam3Ctrl2',
              parent=self.panel4, pos=wx.Point(528, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.angrySpinTeam3Ctrl2.Bind(wx.EVT_TEXT,
              self.OnAngrySpinTeam3Ctrl2Text,
              id=wxID_FRAME1ANGRYSPINTEAM3CTRL2)

        self.angrySpinTeam3Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1ANGRYSPINTEAM3CTRL3,
              initial=1, max=7, min=1, name=u'angrySpinTeam3Ctrl3',
              parent=self.panel4, pos=wx.Point(528, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.angrySpinTeam3Ctrl3.Bind(wx.EVT_TEXT,
              self.OnAngrySpinTeam3Ctrl3Text,
              id=wxID_FRAME1ANGRYSPINTEAM3CTRL3)

        self.angrySpinTeam3Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1ANGRYSPINTEAM3CTRL4,
              initial=1, max=7, min=1, name=u'angrySpinTeam3Ctrl4',
              parent=self.panel4, pos=wx.Point(528, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.angrySpinTeam3Ctrl4.Bind(wx.EVT_TEXT,
              self.OnAngrySpinTeam3Ctrl4Text,
              id=wxID_FRAME1ANGRYSPINTEAM3CTRL4)

        self.angrySpinTeam3Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1ANGRYSPINTEAM3CTRL5,
              initial=1, max=7, min=1, name=u'angrySpinTeam3Ctrl5',
              parent=self.panel4, pos=wx.Point(528, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.angrySpinTeam3Ctrl5.Bind(wx.EVT_TEXT,
              self.OnAngrySpinTeam3Ctrl5Text,
              id=wxID_FRAME1ANGRYSPINTEAM3CTRL5)

        self.shootTeam3Choice1 = wx.Choice(choices=[],
              id=wxID_FRAME1SHOOTTEAM3CHOICE1, name=u'shootTeam3Choice1',
              parent=self.panel4, pos=wx.Point(592, 64), size=wx.Size(106, 21),
              style=0)
        self.shootTeam3Choice1.Bind(wx.EVT_CHOICE,
              self.OnShootTeam3Choice1Choice, id=wxID_FRAME1SHOOTTEAM3CHOICE1)

        self.shootTeam3Choice2 = wx.Choice(choices=[],
              id=wxID_FRAME1SHOOTTEAM3CHOICE2, name=u'shootTeam3Choice2',
              parent=self.panel4, pos=wx.Point(592, 96), size=wx.Size(106, 21),
              style=0)
        self.shootTeam3Choice2.Bind(wx.EVT_CHOICE,
              self.OnShootTeam3Choice2Choice, id=wxID_FRAME1SHOOTTEAM3CHOICE2)

        self.shootTeam3Choice3 = wx.Choice(choices=[],
              id=wxID_FRAME1SHOOTTEAM3CHOICE3, name=u'shootTeam3Choice3',
              parent=self.panel4, pos=wx.Point(592, 128), size=wx.Size(106, 21),
              style=0)
        self.shootTeam3Choice3.Bind(wx.EVT_CHOICE,
              self.OnShootTeam3Choice3Choice, id=wxID_FRAME1SHOOTTEAM3CHOICE3)

        self.shootTeam3Choice4 = wx.Choice(choices=[],
              id=wxID_FRAME1SHOOTTEAM3CHOICE4, name=u'shootTeam3Choice4',
              parent=self.panel4, pos=wx.Point(592, 160), size=wx.Size(106, 21),
              style=0)
        self.shootTeam3Choice4.Bind(wx.EVT_CHOICE,
              self.OnShootTeam3Choice4Choice, id=wxID_FRAME1SHOOTTEAM3CHOICE4)

        self.shootTeam3Choice5 = wx.Choice(choices=[],
              id=wxID_FRAME1SHOOTTEAM3CHOICE5, name=u'shootTeam3Choice5',
              parent=self.panel4, pos=wx.Point(592, 192), size=wx.Size(106, 21),
              style=0)
        self.shootTeam3Choice5.Bind(wx.EVT_CHOICE,
              self.OnShootTeam3Choice5Choice, id=wxID_FRAME1SHOOTTEAM3CHOICE5)

        self.displayPowTeam3Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYPOWTEAM3CTRL1,
              initial=1, max=999, min=1, name=u'displayPowTeam3Ctrl1',
              parent=self.panel4, pos=wx.Point(712, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayPowTeam3Ctrl1.Bind(wx.EVT_TEXT,
              self.OnDisplayPowTeam3Ctrl1Text,
              id=wxID_FRAME1DISPLAYPOWTEAM3CTRL1)

        self.displayPowTeam3Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYPOWTEAM3CTRL2,
              initial=1, max=999, min=1, name=u'displayPowTeam3Ctrl2',
              parent=self.panel4, pos=wx.Point(712, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayPowTeam3Ctrl2.Bind(wx.EVT_TEXT,
              self.OnDisplayPowTeam3Ctrl2Text,
              id=wxID_FRAME1DISPLAYPOWTEAM3CTRL2)

        self.displayPowTeam3Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYPOWTEAM3CTRL3,
              initial=1, max=999, min=1, name=u'displayPowTeam3Ctrl3',
              parent=self.panel4, pos=wx.Point(712, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayPowTeam3Ctrl3.Bind(wx.EVT_TEXT,
              self.OnDisplayPowTeam3Ctrl3Text,
              id=wxID_FRAME1DISPLAYPOWTEAM3CTRL3)

        self.displayPowTeam3Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYPOWTEAM3CTRL4,
              initial=1, max=999, min=1, name=u'displayPowTeam3Ctrl4',
              parent=self.panel4, pos=wx.Point(712, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayPowTeam3Ctrl4.Bind(wx.EVT_TEXT,
              self.OnDisplayPowTeam3Ctrl4Text,
              id=wxID_FRAME1DISPLAYPOWTEAM3CTRL4)

        self.displayPowTeam3Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYPOWTEAM3CTRL5,
              initial=1, max=999, min=1, name=u'displayPowTeam3Ctrl5',
              parent=self.panel4, pos=wx.Point(712, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayPowTeam3Ctrl5.Bind(wx.EVT_TEXT,
              self.OnDisplayPowTeam3Ctrl5Text,
              id=wxID_FRAME1DISPLAYPOWTEAM3CTRL5)

        self.displaySpdTeam3Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYSPDTEAM3CTRL1,
              initial=1, max=999, min=1, name=u'displaySpdTeam3Ctrl1',
              parent=self.panel4, pos=wx.Point(768, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displaySpdTeam3Ctrl1.Bind(wx.EVT_TEXT,
              self.OnDisplaySpdTeam3Ctrl1Text,
              id=wxID_FRAME1DISPLAYSPDTEAM3CTRL1)

        self.displaySpdTeam3Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYSPDTEAM3CTRL2,
              initial=1, max=999, min=1, name=u'displaySpdTeam3Ctrl2',
              parent=self.panel4, pos=wx.Point(768, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displaySpdTeam3Ctrl2.Bind(wx.EVT_TEXT,
              self.OnDisplaySpdTeam3Ctrl2Text,
              id=wxID_FRAME1DISPLAYSPDTEAM3CTRL2)

        self.displaySpdTeam3Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYSPDTEAM3CTRL3,
              initial=1, max=999, min=1, name=u'displaySpdTeam3Ctrl3',
              parent=self.panel4, pos=wx.Point(768, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displaySpdTeam3Ctrl3.Bind(wx.EVT_TEXT,
              self.OnDisplaySpdTeam3Ctrl3Text,
              id=wxID_FRAME1DISPLAYSPDTEAM3CTRL3)

        self.displaySpdTeam3Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYSPDTEAM3CTRL4,
              initial=1, max=999, min=1, name=u'displaySpdTeam3Ctrl4',
              parent=self.panel4, pos=wx.Point(768, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displaySpdTeam3Ctrl4.Bind(wx.EVT_TEXT,
              self.OnDisplaySpdTeam3Ctrl4Text,
              id=wxID_FRAME1DISPLAYSPDTEAM3CTRL4)

        self.displaySpdTeam3Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYSPDTEAM3CTRL5,
              initial=1, max=999, min=1, name=u'displaySpdTeam3Ctrl5',
              parent=self.panel4, pos=wx.Point(768, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displaySpdTeam3Ctrl5.Bind(wx.EVT_TEXT,
              self.OnDisplaySpdTeam3Ctrl5Text,
              id=wxID_FRAME1DISPLAYSPDTEAM3CTRL5)

        self.displayDefTeam3Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYDEFTEAM3CTRL1,
              initial=1, max=999, min=1, name=u'displayDefTeam3Ctrl1',
              parent=self.panel4, pos=wx.Point(824, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayDefTeam3Ctrl1.Bind(wx.EVT_TEXT,
              self.OnDisplayDefTeam3Ctrl1Text,
              id=wxID_FRAME1DISPLAYDEFTEAM3CTRL1)

        self.displayDefTeam3Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYDEFTEAM3CTRL2,
              initial=1, max=999, min=1, name=u'displayDefTeam3Ctrl2',
              parent=self.panel4, pos=wx.Point(824, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayDefTeam3Ctrl2.Bind(wx.EVT_TEXT,
              self.OnDisplayDefTeam3Ctrl2Text,
              id=wxID_FRAME1DISPLAYDEFTEAM3CTRL2)

        self.displayDefTeam3Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYDEFTEAM3CTRL3,
              initial=1, max=999, min=1, name=u'displayDefTeam3Ctrl3',
              parent=self.panel4, pos=wx.Point(824, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayDefTeam3Ctrl3.Bind(wx.EVT_TEXT,
              self.OnDisplayDefTeam3Ctrl3Text,
              id=wxID_FRAME1DISPLAYDEFTEAM3CTRL3)

        self.displayDefTeam3Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYDEFTEAM3CTRL4,
              initial=1, max=999, min=1, name=u'displayDefTeam3Ctrl4',
              parent=self.panel4, pos=wx.Point(824, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayDefTeam3Ctrl4.Bind(wx.EVT_TEXT,
              self.OnDisplayDefTeam3Ctrl4Text,
              id=wxID_FRAME1DISPLAYDEFTEAM3CTRL4)

        self.displayDefTeam3Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYDEFTEAM3CTRL5,
              initial=1, max=999, min=1, name=u'displayDefTeam3Ctrl5',
              parent=self.panel4, pos=wx.Point(824, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayDefTeam3Ctrl5.Bind(wx.EVT_TEXT,
              self.OnDisplayDefTeam3Ctrl5Text,
              id=wxID_FRAME1DISPLAYDEFTEAM3CTRL5)

        self.staticText68 = wx.StaticText(id=wxID_FRAME1STATICTEXT68,
              label=u'Start Power', name='staticText68', parent=self.panel4,
              pos=wx.Point(232, 40), size=wx.Size(57, 14), style=0)

        self.staticText69 = wx.StaticText(id=wxID_FRAME1STATICTEXT69,
              label=u'Max Power', name='staticText69', parent=self.panel4,
              pos=wx.Point(312, 40), size=wx.Size(53, 14), style=0)

        self.staticText70 = wx.StaticText(id=wxID_FRAME1STATICTEXT70,
              label=u'Speed', name=u'staticText70', parent=self.panel4,
              pos=wx.Point(392, 40), size=wx.Size(30, 14), style=0)

        self.staticText71 = wx.StaticText(id=wxID_FRAME1STATICTEXT71,
              label=u'Weight', name='staticText71', parent=self.panel4,
              pos=wx.Point(464, 40), size=wx.Size(34, 14), style=0)

        self.staticText72 = wx.StaticText(id=wxID_FRAME1STATICTEXT72,
              label=u'Angry', name='staticText72', parent=self.panel4,
              pos=wx.Point(536, 40), size=wx.Size(29, 14), style=0)

        self.staticText73 = wx.StaticText(id=wxID_FRAME1STATICTEXT73,
              label=u'Special Shoot', name='staticText73', parent=self.panel4,
              pos=wx.Point(608, 40), size=wx.Size(64, 14), style=0)

        self.staticText74 = wx.StaticText(id=wxID_FRAME1STATICTEXT74,
              label=u'POW', name='staticText74', parent=self.panel4,
              pos=wx.Point(720, 40), size=wx.Size(24, 14), style=0)

        self.staticText75 = wx.StaticText(id=wxID_FRAME1STATICTEXT75,
              label=u'SPD', name='staticText75', parent=self.panel4,
              pos=wx.Point(776, 40), size=wx.Size(19, 14), style=0)

        self.staticText76 = wx.StaticText(id=wxID_FRAME1STATICTEXT76,
              label=u'DEF', name='staticText76', parent=self.panel4,
              pos=wx.Point(832, 40), size=wx.Size(19, 14), style=0)

        self.sPowerSpinTeam4Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1SPOWERSPINTEAM4CTRL1,
              initial=1, max=12, min=1, name=u'sPowerSpinTeam4Ctrl1',
              parent=self.panel5, pos=wx.Point(240, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.sPowerSpinTeam4Ctrl1.Bind(wx.EVT_TEXT,
              self.OnSPowerSpinTeam4Ctrl1Text,
              id=wxID_FRAME1SPOWERSPINTEAM4CTRL1)

        self.sPowerSpinTeam4Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1SPOWERSPINTEAM4CTRL2,
              initial=1, max=12, min=1, name=u'sPowerSpinTeam4Ctrl2',
              parent=self.panel5, pos=wx.Point(240, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.sPowerSpinTeam4Ctrl2.Bind(wx.EVT_TEXT,
              self.OnSPowerSpinTeam4Ctrl2Text,
              id=wxID_FRAME1SPOWERSPINTEAM4CTRL2)

        self.sPowerSpinTeam4Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1SPOWERSPINTEAM4CTRL3,
              initial=1, max=12, min=1, name=u'sPowerSpinTeam4Ctrl3',
              parent=self.panel5, pos=wx.Point(240, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.sPowerSpinTeam4Ctrl3.Bind(wx.EVT_TEXT,
              self.OnSPowerSpinTeam4Ctrl3Text,
              id=wxID_FRAME1SPOWERSPINTEAM4CTRL3)

        self.sPowerSpinTeam4Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1SPOWERSPINTEAM4CTRL4,
              initial=1, max=12, min=1, name=u'sPowerSpinTeam4Ctrl4',
              parent=self.panel5, pos=wx.Point(240, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.sPowerSpinTeam4Ctrl4.Bind(wx.EVT_TEXT,
              self.OnSPowerSpinTeam4Ctrl4Text,
              id=wxID_FRAME1SPOWERSPINTEAM4CTRL4)

        self.sPowerSpinTeam4Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1SPOWERSPINTEAM4CTRL5,
              initial=1, max=12, min=1, name=u'sPowerSpinTeam4Ctrl5',
              parent=self.panel5, pos=wx.Point(240, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.sPowerSpinTeam4Ctrl5.Bind(wx.EVT_TEXT,
              self.OnSPowerSpinTeam4Ctrl5Text,
              id=wxID_FRAME1SPOWERSPINTEAM4CTRL5)

        self.mPowerSpinTeam4Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1MPOWERSPINTEAM4CTRL1,
              initial=1, max=5, min=1, name=u'mPowerSpinTeam4Ctrl1',
              parent=self.panel5, pos=wx.Point(312, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.mPowerSpinTeam4Ctrl1.Bind(wx.EVT_TEXT,
              self.OnMPowerSpinTeam4Ctrl1Text,
              id=wxID_FRAME1MPOWERSPINTEAM4CTRL1)

        self.mPowerSpinTeam4Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1MPOWERSPINTEAM4CTRL2,
              initial=1, max=5, min=1, name=u'mPowerSpinTeam4Ctrl2',
              parent=self.panel5, pos=wx.Point(312, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.mPowerSpinTeam4Ctrl2.Bind(wx.EVT_TEXT,
              self.OnMPowerSpinTeam4Ctrl2Text,
              id=wxID_FRAME1MPOWERSPINTEAM4CTRL2)

        self.mPowerSpinTeam4Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1MPOWERSPINTEAM4CTRL3,
              initial=1, max=5, min=1, name=u'mPowerSpinTeam4Ctrl3',
              parent=self.panel5, pos=wx.Point(312, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.mPowerSpinTeam4Ctrl3.Bind(wx.EVT_TEXT,
              self.OnMPowerSpinTeam4Ctrl3Text,
              id=wxID_FRAME1MPOWERSPINTEAM4CTRL3)

        self.mPowerSpinTeam4Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1MPOWERSPINTEAM4CTRL4,
              initial=1, max=5, min=1, name=u'mPowerSpinTeam4Ctrl4',
              parent=self.panel5, pos=wx.Point(312, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.mPowerSpinTeam4Ctrl4.Bind(wx.EVT_TEXT,
              self.OnMPowerSpinTeam4Ctrl4Text,
              id=wxID_FRAME1MPOWERSPINTEAM4CTRL4)

        self.mPowerSpinTeam4Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1MPOWERSPINTEAM4CTRL5,
              initial=1, max=5, min=1, name=u'mPowerSpinTeam4Ctrl5',
              parent=self.panel5, pos=wx.Point(312, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.mPowerSpinTeam4Ctrl5.Bind(wx.EVT_TEXT,
              self.OnMPowerSpinTeam4Ctrl5Text,
              id=wxID_FRAME1MPOWERSPINTEAM4CTRL5)

        self.speedSpinTeam4Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1SPEEDSPINTEAM4CTRL1,
              initial=1, max=3, min=1, name=u'speedSpinTeam4Ctrl1',
              parent=self.panel5, pos=wx.Point(384, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.speedSpinTeam4Ctrl1.Bind(wx.EVT_TEXT,
              self.OnSpeedSpinTeam4Ctrl1Text,
              id=wxID_FRAME1SPEEDSPINTEAM4CTRL1)

        self.speedSpinTeam4Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1SPEEDSPINTEAM4CTRL2,
              initial=1, max=3, min=1, name=u'speedSpinTeam4Ctrl2',
              parent=self.panel5, pos=wx.Point(384, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.speedSpinTeam4Ctrl2.Bind(wx.EVT_TEXT,
              self.OnSpeedSpinTeam4Ctrl2Text,
              id=wxID_FRAME1SPEEDSPINTEAM4CTRL2)

        self.speedSpinTeam4Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1SPEEDSPINTEAM4CTRL3,
              initial=1, max=3, min=1, name=u'speedSpinTeam4Ctrl3',
              parent=self.panel5, pos=wx.Point(384, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.speedSpinTeam4Ctrl3.Bind(wx.EVT_TEXT,
              self.OnSpeedSpinTeam4Ctrl3Text,
              id=wxID_FRAME1SPEEDSPINTEAM4CTRL3)

        self.speedSpinTeam4Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1SPEEDSPINTEAM4CTRL4,
              initial=1, max=3, min=1, name=u'speedSpinTeam4Ctrl4',
              parent=self.panel5, pos=wx.Point(384, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.speedSpinTeam4Ctrl4.Bind(wx.EVT_TEXT,
              self.OnSpeedSpinTeam4Ctrl4Text,
              id=wxID_FRAME1SPEEDSPINTEAM4CTRL4)

        self.speedSpinTeam4Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1SPEEDSPINTEAM4CTRL5,
              initial=1, max=3, min=1, name=u'speedSpinTeam4Ctrl5',
              parent=self.panel5, pos=wx.Point(384, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.speedSpinTeam4Ctrl5.Bind(wx.EVT_TEXT,
              self.OnSpeedSpinTeam4Ctrl5Text,
              id=wxID_FRAME1SPEEDSPINTEAM4CTRL5)

        self.weightSpinTeam4Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1WEIGHTSPINTEAM4CTRL1,
              initial=1, max=5, min=1, name=u'weightSpinTeam4Ctrl1',
              parent=self.panel5, pos=wx.Point(456, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.weightSpinTeam4Ctrl1.Bind(wx.EVT_TEXT,
              self.OnWeightSpinTeam4Ctrl1Text,
              id=wxID_FRAME1WEIGHTSPINTEAM4CTRL1)

        self.weightSpinTeam4Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1WEIGHTSPINTEAM4CTRL2,
              initial=1, max=5, min=1, name=u'weightSpinTeam4Ctrl2',
              parent=self.panel5, pos=wx.Point(456, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.weightSpinTeam4Ctrl2.Bind(wx.EVT_TEXT,
              self.OnWeightSpinTeam4Ctrl2Text,
              id=wxID_FRAME1WEIGHTSPINTEAM4CTRL2)

        self.weightSpinTeam4Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1WEIGHTSPINTEAM4CTRL3,
              initial=1, max=5, min=1, name=u'weightSpinTeam4Ctrl3',
              parent=self.panel5, pos=wx.Point(456, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.weightSpinTeam4Ctrl3.Bind(wx.EVT_TEXT,
              self.OnWeightSpinTeam4Ctrl3Text,
              id=wxID_FRAME1WEIGHTSPINTEAM4CTRL3)

        self.weightSpinTeam4Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1WEIGHTSPINTEAM4CTRL4,
              initial=1, max=5, min=1, name=u'weightSpinTeam4Ctrl4',
              parent=self.panel5, pos=wx.Point(456, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.weightSpinTeam4Ctrl4.Bind(wx.EVT_TEXT,
              self.OnWeightSpinTeam4Ctrl4Text,
              id=wxID_FRAME1WEIGHTSPINTEAM4CTRL4)

        self.weightSpinTeam4Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1WEIGHTSPINTEAM4CTRL5,
              initial=1, max=5, min=1, name=u'weightSpinTeam4Ctrl5',
              parent=self.panel5, pos=wx.Point(456, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.weightSpinTeam4Ctrl5.Bind(wx.EVT_TEXT,
              self.OnWeightSpinTeam4Ctrl5Text,
              id=wxID_FRAME1WEIGHTSPINTEAM4CTRL5)

        self.angrySpinTeam4Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1ANGRYSPINTEAM4CTRL1,
              initial=1, max=7, min=1, name=u'angrySpinTeam4Ctrl1',
              parent=self.panel5, pos=wx.Point(528, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.angrySpinTeam4Ctrl1.Bind(wx.EVT_TEXT,
              self.OnAngrySpinTeam4Ctrl1Text,
              id=wxID_FRAME1ANGRYSPINTEAM4CTRL1)

        self.angrySpinTeam4Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1ANGRYSPINTEAM4CTRL2,
              initial=1, max=7, min=1, name=u'angrySpinTeam4Ctrl2',
              parent=self.panel5, pos=wx.Point(528, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.angrySpinTeam4Ctrl2.Bind(wx.EVT_TEXT,
              self.OnAngrySpinTeam4Ctrl2Text,
              id=wxID_FRAME1ANGRYSPINTEAM4CTRL2)

        self.angrySpinTeam4Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1ANGRYSPINTEAM4CTRL3,
              initial=1, max=7, min=1, name=u'angrySpinTeam4Ctrl3',
              parent=self.panel5, pos=wx.Point(528, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.angrySpinTeam4Ctrl3.Bind(wx.EVT_TEXT,
              self.OnAngrySpinTeam4Ctrl3Text,
              id=wxID_FRAME1ANGRYSPINTEAM4CTRL3)

        self.angrySpinTeam4Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1ANGRYSPINTEAM4CTRL4,
              initial=1, max=7, min=1, name=u'angrySpinTeam4Ctrl4',
              parent=self.panel5, pos=wx.Point(528, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.angrySpinTeam4Ctrl4.Bind(wx.EVT_TEXT,
              self.OnAngrySpinTeam4Ctrl4Text,
              id=wxID_FRAME1ANGRYSPINTEAM4CTRL4)

        self.angrySpinTeam4Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1ANGRYSPINTEAM4CTRL5,
              initial=1, max=7, min=1, name=u'angrySpinTeam4Ctrl5',
              parent=self.panel5, pos=wx.Point(528, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.angrySpinTeam4Ctrl5.Bind(wx.EVT_TEXT,
              self.OnAngrySpinTeam4Ctrl5Text,
              id=wxID_FRAME1ANGRYSPINTEAM4CTRL5)

        self.shootTeam4Choice1 = wx.Choice(choices=[],
              id=wxID_FRAME1SHOOTTEAM4CHOICE1, name=u'shootTeam4Choice1',
              parent=self.panel5, pos=wx.Point(592, 64), size=wx.Size(106, 21),
              style=0)
        self.shootTeam4Choice1.Bind(wx.EVT_CHOICE,
              self.OnShootTeam4Choice1Choice, id=wxID_FRAME1SHOOTTEAM4CHOICE1)

        self.shootTeam4Choice2 = wx.Choice(choices=[],
              id=wxID_FRAME1SHOOTTEAM4CHOICE2, name=u'shootTeam4Choice2',
              parent=self.panel5, pos=wx.Point(592, 96), size=wx.Size(106, 21),
              style=0)
        self.shootTeam4Choice2.Bind(wx.EVT_CHOICE,
              self.OnShootTeam4Choice2Choice, id=wxID_FRAME1SHOOTTEAM4CHOICE2)

        self.shootTeam4Choice3 = wx.Choice(choices=[],
              id=wxID_FRAME1SHOOTTEAM4CHOICE3, name=u'shootTeam4Choice3',
              parent=self.panel5, pos=wx.Point(592, 128), size=wx.Size(106, 21),
              style=0)
        self.shootTeam4Choice3.Bind(wx.EVT_CHOICE,
              self.OnShootTeam4Choice3Choice, id=wxID_FRAME1SHOOTTEAM4CHOICE3)

        self.shootTeam4Choice4 = wx.Choice(choices=[],
              id=wxID_FRAME1SHOOTTEAM4CHOICE4, name=u'shootTeam4Choice4',
              parent=self.panel5, pos=wx.Point(592, 160), size=wx.Size(106, 21),
              style=0)
        self.shootTeam4Choice4.Bind(wx.EVT_CHOICE,
              self.OnShootTeam4Choice4Choice, id=wxID_FRAME1SHOOTTEAM4CHOICE4)

        self.shootTeam4Choice5 = wx.Choice(choices=[],
              id=wxID_FRAME1SHOOTTEAM4CHOICE5, name=u'shootTeam4Choice5',
              parent=self.panel5, pos=wx.Point(592, 192), size=wx.Size(106, 21),
              style=0)
        self.shootTeam4Choice5.Bind(wx.EVT_CHOICE,
              self.OnShootTeam4Choice5Choice, id=wxID_FRAME1SHOOTTEAM4CHOICE5)

        self.displayPowTeam4Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYPOWTEAM4CTRL1,
              initial=1, max=999, min=1, name=u'displayPowTeam4Ctrl1',
              parent=self.panel5, pos=wx.Point(712, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayPowTeam4Ctrl1.Bind(wx.EVT_TEXT,
              self.OnDisplayPowTeam4Ctrl1Text,
              id=wxID_FRAME1DISPLAYPOWTEAM4CTRL1)

        self.displayPowTeam4Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYPOWTEAM4CTRL2,
              initial=1, max=999, min=1, name=u'displayPowTeam4Ctrl2',
              parent=self.panel5, pos=wx.Point(712, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayPowTeam4Ctrl2.Bind(wx.EVT_TEXT,
              self.OnDisplayPowTeam4Ctrl2Text,
              id=wxID_FRAME1DISPLAYPOWTEAM4CTRL2)

        self.displayPowTeam4Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYPOWTEAM4CTRL3,
              initial=1, max=999, min=1, name=u'displayPowTeam4Ctrl3',
              parent=self.panel5, pos=wx.Point(712, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayPowTeam4Ctrl3.Bind(wx.EVT_TEXT,
              self.OnDisplayPowTeam4Ctrl3Text,
              id=wxID_FRAME1DISPLAYPOWTEAM4CTRL3)

        self.displayPowTeam4Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYPOWTEAM4CTRL4,
              initial=1, max=999, min=1, name=u'displayPowTeam4Ctrl4',
              parent=self.panel5, pos=wx.Point(712, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayPowTeam4Ctrl4.Bind(wx.EVT_TEXT,
              self.OnDisplayPowTeam4Ctrl4Text,
              id=wxID_FRAME1DISPLAYPOWTEAM4CTRL4)

        self.displayPowTeam4Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYPOWTEAM4CTRL5,
              initial=1, max=999, min=1, name=u'displayPowTeam4Ctrl5',
              parent=self.panel5, pos=wx.Point(712, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayPowTeam4Ctrl5.Bind(wx.EVT_TEXT,
              self.OnDisplayPowTeam4Ctrl5Text,
              id=wxID_FRAME1DISPLAYPOWTEAM4CTRL5)

        self.displaySpdTeam4Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYSPDTEAM4CTRL1,
              initial=1, max=999, min=1, name=u'displaySpdTeam4Ctrl1',
              parent=self.panel5, pos=wx.Point(768, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displaySpdTeam4Ctrl1.Bind(wx.EVT_TEXT,
              self.OnDisplaySpdTeam4Ctrl1Text,
              id=wxID_FRAME1DISPLAYSPDTEAM4CTRL1)

        self.displaySpdTeam4Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYSPDTEAM4CTRL2,
              initial=1, max=999, min=1, name=u'displaySpdTeam4Ctrl2',
              parent=self.panel5, pos=wx.Point(768, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displaySpdTeam4Ctrl2.Bind(wx.EVT_TEXT,
              self.OnDisplaySpdTeam4Ctrl2Text,
              id=wxID_FRAME1DISPLAYSPDTEAM4CTRL2)

        self.displaySpdTeam4Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYSPDTEAM4CTRL3,
              initial=1, max=999, min=1, name=u'displaySpdTeam4Ctrl3',
              parent=self.panel5, pos=wx.Point(768, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displaySpdTeam4Ctrl3.Bind(wx.EVT_TEXT,
              self.OnDisplaySpdTeam4Ctrl3Text,
              id=wxID_FRAME1DISPLAYSPDTEAM4CTRL3)

        self.displaySpdTeam4Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYSPDTEAM4CTRL4,
              initial=1, max=999, min=1, name=u'displaySpdTeam4Ctrl4',
              parent=self.panel5, pos=wx.Point(768, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displaySpdTeam4Ctrl4.Bind(wx.EVT_TEXT,
              self.OnDisplaySpdTeam4Ctrl4Text,
              id=wxID_FRAME1DISPLAYSPDTEAM4CTRL4)

        self.displaySpdTeam4Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYSPDTEAM4CTRL5,
              initial=1, max=999, min=1, name=u'displaySpdTeam4Ctrl5',
              parent=self.panel5, pos=wx.Point(768, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displaySpdTeam4Ctrl5.Bind(wx.EVT_TEXT,
              self.OnDisplaySpdTeam4Ctrl5Text,
              id=wxID_FRAME1DISPLAYSPDTEAM4CTRL5)

        self.displayDefTeam4Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYDEFTEAM4CTRL1,
              initial=1, max=999, min=1, name=u'displayDefTeam4Ctrl1',
              parent=self.panel5, pos=wx.Point(824, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayDefTeam4Ctrl1.Bind(wx.EVT_TEXT,
              self.OnDisplayDefTeam4Ctrl1Text,
              id=wxID_FRAME1DISPLAYDEFTEAM4CTRL1)

        self.displayDefTeam4Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYDEFTEAM4CTRL2,
              initial=1, max=999, min=1, name=u'displayDefTeam4Ctrl2',
              parent=self.panel5, pos=wx.Point(824, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayDefTeam4Ctrl2.Bind(wx.EVT_TEXT,
              self.OnDisplayDefTeam4Ctrl2Text,
              id=wxID_FRAME1DISPLAYDEFTEAM4CTRL2)

        self.displayDefTeam4Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYDEFTEAM4CTRL3,
              initial=1, max=999, min=1, name=u'displayDefTeam4Ctrl3',
              parent=self.panel5, pos=wx.Point(824, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayDefTeam4Ctrl3.Bind(wx.EVT_TEXT,
              self.OnDisplayDefTeam4Ctrl3Text,
              id=wxID_FRAME1DISPLAYDEFTEAM4CTRL3)

        self.displayDefTeam4Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYDEFTEAM4CTRL4,
              initial=1, max=999, min=1, name=u'displayDefTeam4Ctrl4',
              parent=self.panel5, pos=wx.Point(824, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayDefTeam4Ctrl4.Bind(wx.EVT_TEXT,
              self.OnDisplayDefTeam4Ctrl4Text,
              id=wxID_FRAME1DISPLAYDEFTEAM4CTRL4)

        self.displayDefTeam4Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYDEFTEAM4CTRL5,
              initial=1, max=999, min=1, name=u'displayDefTeam4Ctrl5',
              parent=self.panel5, pos=wx.Point(824, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayDefTeam4Ctrl5.Bind(wx.EVT_TEXT,
              self.OnDisplayDefTeam4Ctrl5Text,
              id=wxID_FRAME1DISPLAYDEFTEAM4CTRL5)

        self.staticText77 = wx.StaticText(id=wxID_FRAME1STATICTEXT77,
              label=u'Start Power', name='staticText77', parent=self.panel5,
              pos=wx.Point(232, 40), size=wx.Size(57, 14), style=0)

        self.staticText78 = wx.StaticText(id=wxID_FRAME1STATICTEXT78,
              label=u'Max Power', name='staticText78', parent=self.panel5,
              pos=wx.Point(312, 40), size=wx.Size(53, 14), style=0)

        self.staticText79 = wx.StaticText(id=wxID_FRAME1STATICTEXT79,
              label=u'Speed', name='staticText79', parent=self.panel5,
              pos=wx.Point(392, 40), size=wx.Size(30, 14), style=0)

        self.staticText80 = wx.StaticText(id=wxID_FRAME1STATICTEXT80,
              label=u'Weight', name='staticText80', parent=self.panel5,
              pos=wx.Point(464, 40), size=wx.Size(34, 14), style=0)

        self.staticText81 = wx.StaticText(id=wxID_FRAME1STATICTEXT81,
              label=u'Angry', name='staticText81', parent=self.panel5,
              pos=wx.Point(536, 40), size=wx.Size(29, 14), style=0)

        self.staticText82 = wx.StaticText(id=wxID_FRAME1STATICTEXT82,
              label=u'Special Shoot', name='staticText82', parent=self.panel5,
              pos=wx.Point(608, 40), size=wx.Size(64, 14), style=0)

        self.staticText83 = wx.StaticText(id=wxID_FRAME1STATICTEXT83,
              label=u'POW', name='staticText83', parent=self.panel5,
              pos=wx.Point(720, 40), size=wx.Size(24, 14), style=0)

        self.staticText84 = wx.StaticText(id=wxID_FRAME1STATICTEXT84,
              label=u'SPD', name='staticText84', parent=self.panel5,
              pos=wx.Point(776, 40), size=wx.Size(19, 14), style=0)

        self.staticText85 = wx.StaticText(id=wxID_FRAME1STATICTEXT85,
              label=u'DEF', name='staticText85', parent=self.panel5,
              pos=wx.Point(832, 40), size=wx.Size(19, 14), style=0)

        self.sPowerSpinTeam5Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1SPOWERSPINTEAM5CTRL1,
              initial=1, max=12, min=1, name=u'sPowerSpinTeam5Ctrl1',
              parent=self.panel6, pos=wx.Point(240, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.sPowerSpinTeam5Ctrl1.Bind(wx.EVT_TEXT,
              self.OnSPowerSpinTeam5Ctrl1Text,
              id=wxID_FRAME1SPOWERSPINTEAM5CTRL1)

        self.sPowerSpinTeam5Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1SPOWERSPINTEAM5CTRL2,
              initial=1, max=12, min=1, name=u'sPowerSpinTeam5Ctrl2',
              parent=self.panel6, pos=wx.Point(240, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.sPowerSpinTeam5Ctrl2.Bind(wx.EVT_TEXT,
              self.OnSPowerSpinTeam5Ctrl2Text,
              id=wxID_FRAME1SPOWERSPINTEAM5CTRL2)

        self.sPowerSpinTeam5Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1SPOWERSPINTEAM5CTRL3,
              initial=1, max=12, min=1, name=u'sPowerSpinTeam5Ctrl3',
              parent=self.panel6, pos=wx.Point(240, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.sPowerSpinTeam5Ctrl3.Bind(wx.EVT_TEXT,
              self.OnSPowerSpinTeam5Ctrl3Text,
              id=wxID_FRAME1SPOWERSPINTEAM5CTRL3)

        self.sPowerSpinTeam5Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1SPOWERSPINTEAM5CTRL4,
              initial=1, max=12, min=1, name=u'sPowerSpinTeam5Ctrl4',
              parent=self.panel6, pos=wx.Point(240, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.sPowerSpinTeam5Ctrl4.Bind(wx.EVT_TEXT,
              self.OnSPowerSpinTeam5Ctrl4Text,
              id=wxID_FRAME1SPOWERSPINTEAM5CTRL4)

        self.sPowerSpinTeam5Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1SPOWERSPINTEAM5CTRL5,
              initial=1, max=12, min=1, name=u'sPowerSpinTeam5Ctrl5',
              parent=self.panel6, pos=wx.Point(240, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.sPowerSpinTeam5Ctrl5.Bind(wx.EVT_TEXT,
              self.OnSPowerSpinTeam5Ctrl5Text,
              id=wxID_FRAME1SPOWERSPINTEAM5CTRL5)

        self.mPowerSpinTeam5Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1MPOWERSPINTEAM5CTRL1,
              initial=1, max=5, min=1, name=u'mPowerSpinTeam5Ctrl1',
              parent=self.panel6, pos=wx.Point(312, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.mPowerSpinTeam5Ctrl1.Bind(wx.EVT_TEXT,
              self.OnMPowerSpinTeam5Ctrl1Text,
              id=wxID_FRAME1MPOWERSPINTEAM5CTRL1)

        self.mPowerSpinTeam5Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1MPOWERSPINTEAM5CTRL2,
              initial=1, max=5, min=1, name=u'mPowerSpinTeam5Ctrl2',
              parent=self.panel6, pos=wx.Point(312, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.mPowerSpinTeam5Ctrl2.Bind(wx.EVT_TEXT,
              self.OnMPowerSpinTeam5Ctrl2Text,
              id=wxID_FRAME1MPOWERSPINTEAM5CTRL2)

        self.mPowerSpinTeam5Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1MPOWERSPINTEAM5CTRL3,
              initial=1, max=5, min=1, name=u'mPowerSpinTeam5Ctrl3',
              parent=self.panel6, pos=wx.Point(312, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.mPowerSpinTeam5Ctrl3.Bind(wx.EVT_TEXT,
              self.OnMPowerSpinTeam5Ctrl3Text,
              id=wxID_FRAME1MPOWERSPINTEAM5CTRL3)

        self.mPowerSpinTeam5Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1MPOWERSPINTEAM5CTRL4,
              initial=1, max=5, min=1, name=u'mPowerSpinTeam5Ctrl4',
              parent=self.panel6, pos=wx.Point(312, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.mPowerSpinTeam5Ctrl4.Bind(wx.EVT_TEXT,
              self.OnMPowerSpinTeam5Ctrl4Text,
              id=wxID_FRAME1MPOWERSPINTEAM5CTRL4)

        self.mPowerSpinTeam5Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1MPOWERSPINTEAM5CTRL5,
              initial=1, max=5, min=1, name=u'mPowerSpinTeam5Ctrl5',
              parent=self.panel6, pos=wx.Point(312, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.mPowerSpinTeam5Ctrl5.Bind(wx.EVT_TEXT,
              self.OnMPowerSpinTeam5Ctrl5Text,
              id=wxID_FRAME1MPOWERSPINTEAM5CTRL5)

        self.speedSpinTeam5Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1SPEEDSPINTEAM5CTRL1,
              initial=1, max=3, min=1, name=u'speedSpinTeam5Ctrl1',
              parent=self.panel6, pos=wx.Point(384, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.speedSpinTeam5Ctrl1.Bind(wx.EVT_TEXT,
              self.OnSpeedSpinTeam5Ctrl1Text,
              id=wxID_FRAME1SPEEDSPINTEAM5CTRL1)

        self.speedSpinTeam5Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1SPEEDSPINTEAM5CTRL2,
              initial=1, max=3, min=1, name=u'speedSpinTeam5Ctrl2',
              parent=self.panel6, pos=wx.Point(384, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.speedSpinTeam5Ctrl2.Bind(wx.EVT_TEXT,
              self.OnSpeedSpinTeam5Ctrl2Text,
              id=wxID_FRAME1SPEEDSPINTEAM5CTRL2)

        self.speedSpinTeam5Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1SPEEDSPINTEAM5CTRL3,
              initial=1, max=3, min=1, name=u'speedSpinTeam5Ctrl3',
              parent=self.panel6, pos=wx.Point(384, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.speedSpinTeam5Ctrl3.Bind(wx.EVT_TEXT,
              self.OnSpeedSpinTeam5Ctrl3Text,
              id=wxID_FRAME1SPEEDSPINTEAM5CTRL3)

        self.speedSpinTeam5Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1SPEEDSPINTEAM5CTRL4,
              initial=1, max=3, min=1, name=u'speedSpinTeam5Ctrl4',
              parent=self.panel6, pos=wx.Point(384, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.speedSpinTeam5Ctrl4.Bind(wx.EVT_TEXT,
              self.OnSpeedSpinTeam5Ctrl4Text,
              id=wxID_FRAME1SPEEDSPINTEAM5CTRL4)

        self.speedSpinTeam5Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1SPEEDSPINTEAM5CTRL5,
              initial=1, max=3, min=1, name=u'speedSpinTeam5Ctrl5',
              parent=self.panel6, pos=wx.Point(384, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.speedSpinTeam5Ctrl5.Bind(wx.EVT_TEXT,
              self.OnSpeedSpinTeam5Ctrl5Text,
              id=wxID_FRAME1SPEEDSPINTEAM5CTRL5)

        self.weightSpinTeam5Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1WEIGHTSPINTEAM5CTRL1,
              initial=1, max=5, min=1, name=u'weightSpinTeam5Ctrl1',
              parent=self.panel6, pos=wx.Point(456, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.weightSpinTeam5Ctrl1.Bind(wx.EVT_TEXT,
              self.OnWeightSpinTeam5Ctrl1Text,
              id=wxID_FRAME1WEIGHTSPINTEAM5CTRL1)

        self.weightSpinTeam5Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1WEIGHTSPINTEAM5CTRL2,
              initial=1, max=5, min=1, name=u'weightSpinTeam5Ctrl2',
              parent=self.panel6, pos=wx.Point(456, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.weightSpinTeam5Ctrl2.Bind(wx.EVT_TEXT,
              self.OnWeightSpinTeam5Ctrl2Text,
              id=wxID_FRAME1WEIGHTSPINTEAM5CTRL2)

        self.weightSpinTeam5Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1WEIGHTSPINTEAM5CTRL3,
              initial=1, max=5, min=1, name=u'weightSpinTeam5Ctrl3',
              parent=self.panel6, pos=wx.Point(456, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.weightSpinTeam5Ctrl3.Bind(wx.EVT_TEXT,
              self.OnWeightSpinTeam5Ctrl3Text,
              id=wxID_FRAME1WEIGHTSPINTEAM5CTRL3)

        self.weightSpinTeam5Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1WEIGHTSPINTEAM5CTRL4,
              initial=1, max=5, min=1, name=u'weightSpinTeam5Ctrl4',
              parent=self.panel6, pos=wx.Point(456, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.weightSpinTeam5Ctrl4.Bind(wx.EVT_TEXT,
              self.OnWeightSpinTeam5Ctrl4Text,
              id=wxID_FRAME1WEIGHTSPINTEAM5CTRL4)

        self.weightSpinTeam5Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1WEIGHTSPINTEAM5CTRL5,
              initial=1, max=5, min=1, name=u'weightSpinTeam5Ctrl5',
              parent=self.panel6, pos=wx.Point(456, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.weightSpinTeam5Ctrl5.Bind(wx.EVT_TEXT,
              self.OnWeightSpinTeam5Ctrl5Text,
              id=wxID_FRAME1WEIGHTSPINTEAM5CTRL5)

        self.angrySpinTeam5Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1ANGRYSPINTEAM5CTRL1,
              initial=1, max=7, min=1, name=u'angrySpinTeam5Ctrl1',
              parent=self.panel6, pos=wx.Point(528, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.angrySpinTeam5Ctrl1.Bind(wx.EVT_TEXT,
              self.OnAngrySpinTeam5Ctrl1Text,
              id=wxID_FRAME1ANGRYSPINTEAM5CTRL1)

        self.angrySpinTeam5Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1ANGRYSPINTEAM5CTRL2,
              initial=1, max=7, min=1, name=u'angrySpinTeam5Ctrl2',
              parent=self.panel6, pos=wx.Point(528, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.angrySpinTeam5Ctrl2.Bind(wx.EVT_TEXT,
              self.OnAngrySpinTeam5Ctrl2Text,
              id=wxID_FRAME1ANGRYSPINTEAM5CTRL2)

        self.angrySpinTeam5Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1ANGRYSPINTEAM5CTRL3,
              initial=1, max=7, min=1, name=u'angrySpinTeam5Ctrl3',
              parent=self.panel6, pos=wx.Point(528, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.angrySpinTeam5Ctrl3.Bind(wx.EVT_TEXT,
              self.OnAngrySpinTeam5Ctrl3Text,
              id=wxID_FRAME1ANGRYSPINTEAM5CTRL3)

        self.angrySpinTeam5Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1ANGRYSPINTEAM5CTRL4,
              initial=1, max=7, min=1, name=u'angrySpinTeam5Ctrl4',
              parent=self.panel6, pos=wx.Point(528, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.angrySpinTeam5Ctrl4.Bind(wx.EVT_TEXT,
              self.OnAngrySpinTeam5Ctrl4Text,
              id=wxID_FRAME1ANGRYSPINTEAM5CTRL4)

        self.angrySpinTeam5Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1ANGRYSPINTEAM5CTRL5,
              initial=1, max=7, min=1, name=u'angrySpinTeam5Ctrl5',
              parent=self.panel6, pos=wx.Point(528, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.angrySpinTeam5Ctrl5.Bind(wx.EVT_TEXT,
              self.OnAngrySpinTeam5Ctrl5Text,
              id=wxID_FRAME1ANGRYSPINTEAM5CTRL5)

        self.shootTeam5Choice1 = wx.Choice(choices=[],
              id=wxID_FRAME1SHOOTTEAM5CHOICE1, name=u'shootTeam5Choice1',
              parent=self.panel6, pos=wx.Point(592, 64), size=wx.Size(106, 21),
              style=0)
        self.shootTeam5Choice1.Bind(wx.EVT_CHOICE,
              self.OnShootTeam5Choice1Choice, id=wxID_FRAME1SHOOTTEAM5CHOICE1)

        self.shootTeam5Choice2 = wx.Choice(choices=[],
              id=wxID_FRAME1SHOOTTEAM5CHOICE2, name=u'shootTeam5Choice2',
              parent=self.panel6, pos=wx.Point(592, 96), size=wx.Size(106, 21),
              style=0)
        self.shootTeam5Choice2.Bind(wx.EVT_CHOICE,
              self.OnShootTeam5Choice2Choice, id=wxID_FRAME1SHOOTTEAM5CHOICE2)

        self.shootTeam5Choice3 = wx.Choice(choices=[],
              id=wxID_FRAME1SHOOTTEAM5CHOICE3, name=u'shootTeam5Choice3',
              parent=self.panel6, pos=wx.Point(592, 128), size=wx.Size(106, 21),
              style=0)
        self.shootTeam5Choice3.Bind(wx.EVT_CHOICE,
              self.OnShootTeam5Choice3Choice, id=wxID_FRAME1SHOOTTEAM5CHOICE3)

        self.shootTeam5Choice4 = wx.Choice(choices=[],
              id=wxID_FRAME1SHOOTTEAM5CHOICE4, name=u'shootTeam5Choice4',
              parent=self.panel6, pos=wx.Point(592, 160), size=wx.Size(106, 21),
              style=0)
        self.shootTeam5Choice4.Bind(wx.EVT_CHOICE,
              self.OnShootTeam5Choice4Choice, id=wxID_FRAME1SHOOTTEAM5CHOICE4)

        self.shootTeam5Choice5 = wx.Choice(choices=[],
              id=wxID_FRAME1SHOOTTEAM5CHOICE5, name=u'shootTeam5Choice5',
              parent=self.panel6, pos=wx.Point(592, 192), size=wx.Size(106, 21),
              style=0)
        self.shootTeam5Choice5.Bind(wx.EVT_CHOICE,
              self.OnShootTeam5Choice5Choice, id=wxID_FRAME1SHOOTTEAM5CHOICE5)

        self.displayPowTeam5Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYPOWTEAM5CTRL1,
              initial=1, max=999, min=1, name=u'displayPowTeam5Ctrl1',
              parent=self.panel6, pos=wx.Point(712, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayPowTeam5Ctrl1.Bind(wx.EVT_TEXT,
              self.OnDisplayPowTeam5Ctrl1Text,
              id=wxID_FRAME1DISPLAYPOWTEAM5CTRL1)

        self.displayPowTeam5Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYPOWTEAM5CTRL2,
              initial=1, max=999, min=1, name=u'displayPowTeam5Ctrl2',
              parent=self.panel6, pos=wx.Point(712, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayPowTeam5Ctrl2.Bind(wx.EVT_TEXT,
              self.OnDisplayPowTeam5Ctrl2Text,
              id=wxID_FRAME1DISPLAYPOWTEAM5CTRL2)

        self.displayPowTeam5Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYPOWTEAM5CTRL3,
              initial=1, max=999, min=1, name=u'displayPowTeam5Ctrl3',
              parent=self.panel6, pos=wx.Point(712, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayPowTeam5Ctrl3.Bind(wx.EVT_TEXT,
              self.OnDisplayPowTeam5Ctrl3Text,
              id=wxID_FRAME1DISPLAYPOWTEAM5CTRL3)

        self.displayPowTeam5Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYPOWTEAM5CTRL4,
              initial=1, max=999, min=1, name=u'displayPowTeam5Ctrl4',
              parent=self.panel6, pos=wx.Point(712, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayPowTeam5Ctrl4.Bind(wx.EVT_TEXT,
              self.OnDisplayPowTeam5Ctrl4Text,
              id=wxID_FRAME1DISPLAYPOWTEAM5CTRL4)

        self.displayPowTeam5Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYPOWTEAM5CTRL5,
              initial=1, max=999, min=1, name=u'displayPowTeam5Ctrl5',
              parent=self.panel6, pos=wx.Point(712, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayPowTeam5Ctrl5.Bind(wx.EVT_TEXT,
              self.OnDisplayPowTeam5Ctrl5Text,
              id=wxID_FRAME1DISPLAYPOWTEAM5CTRL5)

        self.displaySpdTeam5Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYSPDTEAM5CTRL1,
              initial=1, max=999, min=1, name=u'displaySpdTeam5Ctrl1',
              parent=self.panel6, pos=wx.Point(768, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displaySpdTeam5Ctrl1.Bind(wx.EVT_TEXT,
              self.OnDisplaySpdTeam5Ctrl1Text,
              id=wxID_FRAME1DISPLAYSPDTEAM5CTRL1)

        self.displaySpdTeam5Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYSPDTEAM5CTRL2,
              initial=1, max=999, min=1, name=u'displaySpdTeam5Ctrl2',
              parent=self.panel6, pos=wx.Point(768, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displaySpdTeam5Ctrl2.Bind(wx.EVT_TEXT,
              self.OnDisplaySpdTeam5Ctrl2Text,
              id=wxID_FRAME1DISPLAYSPDTEAM5CTRL2)

        self.displaySpdTeam5Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYSPDTEAM5CTRL3,
              initial=1, max=999, min=1, name=u'displaySpdTeam5Ctrl3',
              parent=self.panel6, pos=wx.Point(768, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displaySpdTeam5Ctrl3.Bind(wx.EVT_TEXT,
              self.OnDisplaySpdTeam5Ctrl3Text,
              id=wxID_FRAME1DISPLAYSPDTEAM5CTRL3)

        self.displaySpdTeam5Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYSPDTEAM5CTRL4,
              initial=1, max=999, min=1, name=u'displaySpdTeam5Ctrl4',
              parent=self.panel6, pos=wx.Point(768, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displaySpdTeam5Ctrl4.Bind(wx.EVT_TEXT,
              self.OnDisplaySpdTeam5Ctrl4Text,
              id=wxID_FRAME1DISPLAYSPDTEAM5CTRL4)

        self.displaySpdTeam5Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYSPDTEAM5CTRL5,
              initial=1, max=999, min=1, name=u'displaySpdTeam5Ctrl5',
              parent=self.panel6, pos=wx.Point(768, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displaySpdTeam5Ctrl5.Bind(wx.EVT_TEXT,
              self.OnDisplaySpdTeam5Ctrl5Text,
              id=wxID_FRAME1DISPLAYSPDTEAM5CTRL5)

        self.displayDefTeam5Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYDEFTEAM5CTRL1,
              initial=1, max=999, min=1, name=u'displayDefTeam5Ctrl1',
              parent=self.panel6, pos=wx.Point(824, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayDefTeam5Ctrl1.Bind(wx.EVT_TEXT,
              self.OnDisplayDefTeam5Ctrl1Text,
              id=wxID_FRAME1DISPLAYDEFTEAM5CTRL1)

        self.displayDefTeam5Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYDEFTEAM5CTRL2,
              initial=1, max=999, min=1, name=u'displayDefTeam5Ctrl2',
              parent=self.panel6, pos=wx.Point(824, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayDefTeam5Ctrl2.Bind(wx.EVT_TEXT,
              self.OnDisplayDefTeam5Ctrl2Text,
              id=wxID_FRAME1DISPLAYDEFTEAM5CTRL2)

        self.displayDefTeam5Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYDEFTEAM5CTRL3,
              initial=1, max=999, min=1, name=u'displayDefTeam5Ctrl3',
              parent=self.panel6, pos=wx.Point(824, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayDefTeam5Ctrl3.Bind(wx.EVT_TEXT,
              self.OnDisplayDefTeam5Ctrl3Text,
              id=wxID_FRAME1DISPLAYDEFTEAM5CTRL3)

        self.displayDefTeam5Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYDEFTEAM5CTRL4,
              initial=1, max=999, min=1, name=u'displayDefTeam5Ctrl4',
              parent=self.panel6, pos=wx.Point(824, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayDefTeam5Ctrl4.Bind(wx.EVT_TEXT,
              self.OnDisplayDefTeam5Ctrl4Text,
              id=wxID_FRAME1DISPLAYDEFTEAM5CTRL4)

        self.displayDefTeam5Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYDEFTEAM5CTRL5,
              initial=1, max=999, min=1, name=u'displayDefTeam5Ctrl5',
              parent=self.panel6, pos=wx.Point(824, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayDefTeam5Ctrl5.Bind(wx.EVT_TEXT,
              self.OnDisplayDefTeam5Ctrl5Text,
              id=wxID_FRAME1DISPLAYDEFTEAM5CTRL5)

        self.staticText86 = wx.StaticText(id=wxID_FRAME1STATICTEXT86,
              label=u'Start Power', name='staticText86', parent=self.panel6,
              pos=wx.Point(232, 40), size=wx.Size(57, 14), style=0)

        self.staticText87 = wx.StaticText(id=wxID_FRAME1STATICTEXT87,
              label=u'Max Power', name='staticText87', parent=self.panel6,
              pos=wx.Point(312, 40), size=wx.Size(53, 14), style=0)

        self.staticText88 = wx.StaticText(id=wxID_FRAME1STATICTEXT88,
              label=u'Speed', name='staticText88', parent=self.panel6,
              pos=wx.Point(392, 40), size=wx.Size(30, 14), style=0)

        self.staticText89 = wx.StaticText(id=wxID_FRAME1STATICTEXT89,
              label=u'Weight', name='staticText89', parent=self.panel6,
              pos=wx.Point(464, 40), size=wx.Size(34, 14), style=0)

        self.staticText90 = wx.StaticText(id=wxID_FRAME1STATICTEXT90,
              label=u'Angry', name='staticText90', parent=self.panel6,
              pos=wx.Point(536, 40), size=wx.Size(29, 14), style=0)

        self.staticText91 = wx.StaticText(id=wxID_FRAME1STATICTEXT91,
              label=u'Special Shoot', name='staticText91', parent=self.panel6,
              pos=wx.Point(608, 40), size=wx.Size(64, 14), style=0)

        self.staticText92 = wx.StaticText(id=wxID_FRAME1STATICTEXT92,
              label=u'POW', name='staticText92', parent=self.panel6,
              pos=wx.Point(720, 40), size=wx.Size(24, 14), style=0)

        self.staticText93 = wx.StaticText(id=wxID_FRAME1STATICTEXT93,
              label=u'SPD', name='staticText93', parent=self.panel6,
              pos=wx.Point(776, 40), size=wx.Size(19, 14), style=0)

        self.staticText94 = wx.StaticText(id=wxID_FRAME1STATICTEXT94,
              label=u'DEF', name='staticText94', parent=self.panel6,
              pos=wx.Point(832, 40), size=wx.Size(19, 14), style=0)

        self.sPowerSpinTeam6Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1SPOWERSPINTEAM6CTRL1,
              initial=1, max=12, min=1, name=u'sPowerSpinTeam6Ctrl1',
              parent=self.panel7, pos=wx.Point(240, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.sPowerSpinTeam6Ctrl1.Bind(wx.EVT_TEXT,
              self.OnSPowerSpinTeam6Ctrl1Text,
              id=wxID_FRAME1SPOWERSPINTEAM6CTRL1)

        self.sPowerSpinTeam6Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1SPOWERSPINTEAM6CTRL2,
              initial=1, max=12, min=1, name=u'sPowerSpinTeam6Ctrl2',
              parent=self.panel7, pos=wx.Point(240, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.sPowerSpinTeam6Ctrl2.Bind(wx.EVT_TEXT,
              self.OnSPowerSpinTeam6Ctrl2Text,
              id=wxID_FRAME1SPOWERSPINTEAM6CTRL2)

        self.sPowerSpinTeam6Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1SPOWERSPINTEAM6CTRL3,
              initial=1, max=12, min=1, name=u'sPowerSpinTeam6Ctrl3',
              parent=self.panel7, pos=wx.Point(240, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.sPowerSpinTeam6Ctrl3.Bind(wx.EVT_TEXT,
              self.OnSPowerSpinTeam6Ctrl3Text,
              id=wxID_FRAME1SPOWERSPINTEAM6CTRL3)

        self.sPowerSpinTeam6Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1SPOWERSPINTEAM6CTRL4,
              initial=1, max=12, min=1, name=u'sPowerSpinTeam6Ctrl4',
              parent=self.panel7, pos=wx.Point(240, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.sPowerSpinTeam6Ctrl4.Bind(wx.EVT_TEXT,
              self.OnSPowerSpinTeam6Ctrl4Text,
              id=wxID_FRAME1SPOWERSPINTEAM6CTRL4)

        self.sPowerSpinTeam6Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1SPOWERSPINTEAM6CTRL5,
              initial=1, max=12, min=1, name=u'sPowerSpinTeam6Ctrl5',
              parent=self.panel7, pos=wx.Point(240, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.sPowerSpinTeam6Ctrl5.Bind(wx.EVT_TEXT,
              self.OnSPowerSpinTeam6Ctrl5Text,
              id=wxID_FRAME1SPOWERSPINTEAM6CTRL5)

        self.mPowerSpinTeam6Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1MPOWERSPINTEAM6CTRL1,
              initial=1, max=5, min=1, name=u'mPowerSpinTeam6Ctrl1',
              parent=self.panel7, pos=wx.Point(312, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.mPowerSpinTeam6Ctrl1.Bind(wx.EVT_TEXT,
              self.OnMPowerSpinTeam6Ctrl1Text,
              id=wxID_FRAME1MPOWERSPINTEAM6CTRL1)

        self.mPowerSpinTeam6Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1MPOWERSPINTEAM6CTRL2,
              initial=1, max=5, min=1, name=u'mPowerSpinTeam6Ctrl2',
              parent=self.panel7, pos=wx.Point(312, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.mPowerSpinTeam6Ctrl2.Bind(wx.EVT_TEXT,
              self.OnMPowerSpinTeam6Ctrl2Text,
              id=wxID_FRAME1MPOWERSPINTEAM6CTRL2)

        self.mPowerSpinTeam6Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1MPOWERSPINTEAM6CTRL3,
              initial=1, max=5, min=1, name=u'mPowerSpinTeam6Ctrl3',
              parent=self.panel7, pos=wx.Point(312, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.mPowerSpinTeam6Ctrl3.Bind(wx.EVT_TEXT,
              self.OnMPowerSpinTeam6Ctrl3Text,
              id=wxID_FRAME1MPOWERSPINTEAM6CTRL3)

        self.mPowerSpinTeam6Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1MPOWERSPINTEAM6CTRL4,
              initial=1, max=5, min=1, name=u'mPowerSpinTeam6Ctrl4',
              parent=self.panel7, pos=wx.Point(312, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.mPowerSpinTeam6Ctrl4.Bind(wx.EVT_TEXT,
              self.OnMPowerSpinTeam6Ctrl4Text,
              id=wxID_FRAME1MPOWERSPINTEAM6CTRL4)

        self.mPowerSpinTeam6Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1MPOWERSPINTEAM6CTRL5,
              initial=1, max=5, min=1, name=u'mPowerSpinTeam6Ctrl5',
              parent=self.panel7, pos=wx.Point(312, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.mPowerSpinTeam6Ctrl5.Bind(wx.EVT_TEXT,
              self.OnMPowerSpinTeam6Ctrl5Text,
              id=wxID_FRAME1MPOWERSPINTEAM6CTRL5)

        self.speedSpinTeam6Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1SPEEDSPINTEAM6CTRL1,
              initial=1, max=3, min=1, name=u'speedSpinTeam6Ctrl1',
              parent=self.panel7, pos=wx.Point(384, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.speedSpinTeam6Ctrl1.Bind(wx.EVT_TEXT,
              self.OnSpeedSpinTeam6Ctrl1Text,
              id=wxID_FRAME1SPEEDSPINTEAM6CTRL1)

        self.speedSpinTeam6Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1SPEEDSPINTEAM6CTRL2,
              initial=1, max=3, min=1, name=u'speedSpinTeam6Ctrl2',
              parent=self.panel7, pos=wx.Point(384, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.speedSpinTeam6Ctrl2.Bind(wx.EVT_TEXT,
              self.OnSpeedSpinTeam6Ctrl2Text,
              id=wxID_FRAME1SPEEDSPINTEAM6CTRL2)

        self.speedSpinTeam6Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1SPEEDSPINTEAM6CTRL3,
              initial=1, max=3, min=1, name=u'speedSpinTeam6Ctrl3',
              parent=self.panel7, pos=wx.Point(384, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.speedSpinTeam6Ctrl3.Bind(wx.EVT_TEXT,
              self.OnSpeedSpinTeam6Ctrl3Text,
              id=wxID_FRAME1SPEEDSPINTEAM6CTRL3)

        self.speedSpinTeam6Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1SPEEDSPINTEAM6CTRL4,
              initial=1, max=3, min=1, name=u'speedSpinTeam6Ctrl4',
              parent=self.panel7, pos=wx.Point(384, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.speedSpinTeam6Ctrl4.Bind(wx.EVT_TEXT,
              self.OnSpeedSpinTeam6Ctrl4Text,
              id=wxID_FRAME1SPEEDSPINTEAM6CTRL4)

        self.speedSpinTeam6Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1SPEEDSPINTEAM6CTRL5,
              initial=1, max=3, min=1, name=u'speedSpinTeam6Ctrl5',
              parent=self.panel7, pos=wx.Point(384, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.speedSpinTeam6Ctrl5.Bind(wx.EVT_TEXT,
              self.OnSpeedSpinTeam6Ctrl5Text,
              id=wxID_FRAME1SPEEDSPINTEAM6CTRL5)

        self.weightSpinTeam6Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1WEIGHTSPINTEAM6CTRL1,
              initial=1, max=5, min=1, name=u'weightSpinTeam6Ctrl1',
              parent=self.panel7, pos=wx.Point(456, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.weightSpinTeam6Ctrl1.Bind(wx.EVT_TEXT,
              self.OnWeightSpinTeam6Ctrl1Text,
              id=wxID_FRAME1WEIGHTSPINTEAM6CTRL1)

        self.weightSpinTeam6Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1WEIGHTSPINTEAM6CTRL2,
              initial=1, max=5, min=1, name=u'weightSpinTeam6Ctrl2',
              parent=self.panel7, pos=wx.Point(456, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.weightSpinTeam6Ctrl2.Bind(wx.EVT_TEXT,
              self.OnWeightSpinTeam6Ctrl2Text,
              id=wxID_FRAME1WEIGHTSPINTEAM6CTRL2)

        self.weightSpinTeam6Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1WEIGHTSPINTEAM6CTRL3,
              initial=1, max=5, min=1, name=u'weightSpinTeam6Ctrl3',
              parent=self.panel7, pos=wx.Point(456, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.weightSpinTeam6Ctrl3.Bind(wx.EVT_TEXT,
              self.OnWeightSpinTeam6Ctrl3Text,
              id=wxID_FRAME1WEIGHTSPINTEAM6CTRL3)

        self.weightSpinTeam6Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1WEIGHTSPINTEAM6CTRL4,
              initial=1, max=5, min=1, name=u'weightSpinTeam6Ctrl4',
              parent=self.panel7, pos=wx.Point(456, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.weightSpinTeam6Ctrl4.Bind(wx.EVT_TEXT,
              self.OnWeightSpinTeam6Ctrl4Text,
              id=wxID_FRAME1WEIGHTSPINTEAM6CTRL4)

        self.weightSpinTeam6Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1WEIGHTSPINTEAM6CTRL5,
              initial=1, max=5, min=1, name=u'weightSpinTeam6Ctrl5',
              parent=self.panel7, pos=wx.Point(456, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.weightSpinTeam6Ctrl5.Bind(wx.EVT_TEXT,
              self.OnWeightSpinTeam6Ctrl5Text,
              id=wxID_FRAME1WEIGHTSPINTEAM6CTRL5)

        self.angrySpinTeam6Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1ANGRYSPINTEAM6CTRL1,
              initial=1, max=7, min=1, name=u'angrySpinTeam6Ctrl1',
              parent=self.panel7, pos=wx.Point(528, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.angrySpinTeam6Ctrl1.Bind(wx.EVT_TEXT,
              self.OnAngrySpinTeam6Ctrl1Text,
              id=wxID_FRAME1ANGRYSPINTEAM6CTRL1)

        self.angrySpinTeam6Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1ANGRYSPINTEAM6CTRL2,
              initial=1, max=7, min=1, name=u'angrySpinTeam6Ctrl2',
              parent=self.panel7, pos=wx.Point(528, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.angrySpinTeam6Ctrl2.Bind(wx.EVT_TEXT,
              self.OnAngrySpinTeam6Ctrl2Text,
              id=wxID_FRAME1ANGRYSPINTEAM6CTRL2)

        self.angrySpinTeam6Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1ANGRYSPINTEAM6CTRL3,
              initial=1, max=7, min=1, name=u'angrySpinTeam6Ctrl3',
              parent=self.panel7, pos=wx.Point(528, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.angrySpinTeam6Ctrl3.Bind(wx.EVT_TEXT,
              self.OnAngrySpinTeam6Ctrl3Text,
              id=wxID_FRAME1ANGRYSPINTEAM6CTRL3)

        self.angrySpinTeam6Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1ANGRYSPINTEAM6CTRL4,
              initial=1, max=7, min=1, name=u'angrySpinTeam6Ctrl4',
              parent=self.panel7, pos=wx.Point(528, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.angrySpinTeam6Ctrl4.Bind(wx.EVT_TEXT,
              self.OnAngrySpinTeam6Ctrl4Text,
              id=wxID_FRAME1ANGRYSPINTEAM6CTRL4)

        self.angrySpinTeam6Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1ANGRYSPINTEAM6CTRL5,
              initial=1, max=7, min=1, name=u'angrySpinTeam6Ctrl5',
              parent=self.panel7, pos=wx.Point(528, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.angrySpinTeam6Ctrl5.Bind(wx.EVT_TEXT,
              self.OnAngrySpinTeam6Ctrl5Text,
              id=wxID_FRAME1ANGRYSPINTEAM6CTRL5)

        self.shootTeam6Choice1 = wx.Choice(choices=[],
              id=wxID_FRAME1SHOOTTEAM6CHOICE1, name=u'shootTeam6Choice1',
              parent=self.panel7, pos=wx.Point(592, 64), size=wx.Size(106, 21),
              style=0)
        self.shootTeam6Choice1.Bind(wx.EVT_CHOICE,
              self.OnShootTeam6Choice1Choice, id=wxID_FRAME1SHOOTTEAM6CHOICE1)

        self.shootTeam6Choice2 = wx.Choice(choices=[],
              id=wxID_FRAME1SHOOTTEAM6CHOICE2, name=u'shootTeam6Choice2',
              parent=self.panel7, pos=wx.Point(592, 96), size=wx.Size(106, 21),
              style=0)
        self.shootTeam6Choice2.Bind(wx.EVT_CHOICE,
              self.OnShootTeam6Choice2Choice, id=wxID_FRAME1SHOOTTEAM6CHOICE2)

        self.shootTeam6Choice3 = wx.Choice(choices=[],
              id=wxID_FRAME1SHOOTTEAM6CHOICE3, name=u'shootTeam6Choice3',
              parent=self.panel7, pos=wx.Point(592, 128), size=wx.Size(106, 21),
              style=0)
        self.shootTeam6Choice3.Bind(wx.EVT_CHOICE,
              self.OnShootTeam6Choice3Choice, id=wxID_FRAME1SHOOTTEAM6CHOICE3)

        self.shootTeam6Choice4 = wx.Choice(choices=[],
              id=wxID_FRAME1SHOOTTEAM6CHOICE4, name=u'shootTeam6Choice4',
              parent=self.panel7, pos=wx.Point(592, 160), size=wx.Size(106, 21),
              style=0)
        self.shootTeam6Choice4.Bind(wx.EVT_CHOICE,
              self.OnShootTeam6Choice4Choice, id=wxID_FRAME1SHOOTTEAM6CHOICE4)

        self.shootTeam6Choice5 = wx.Choice(choices=[],
              id=wxID_FRAME1SHOOTTEAM6CHOICE5, name=u'shootTeam6Choice5',
              parent=self.panel7, pos=wx.Point(592, 192), size=wx.Size(106, 21),
              style=0)
        self.shootTeam6Choice5.Bind(wx.EVT_CHOICE,
              self.OnShootTeam6Choice5Choice, id=wxID_FRAME1SHOOTTEAM6CHOICE5)

        self.displayPowTeam6Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYPOWTEAM6CTRL1,
              initial=1, max=999, min=1, name=u'displayPowTeam6Ctrl1',
              parent=self.panel7, pos=wx.Point(712, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayPowTeam6Ctrl1.Bind(wx.EVT_TEXT,
              self.OnDisplayPowTeam6Ctrl1Text,
              id=wxID_FRAME1DISPLAYPOWTEAM6CTRL1)

        self.displayPowTeam6Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYPOWTEAM6CTRL2,
              initial=1, max=999, min=1, name=u'displayPowTeam6Ctrl2',
              parent=self.panel7, pos=wx.Point(712, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayPowTeam6Ctrl2.Bind(wx.EVT_TEXT,
              self.OnDisplayPowTeam6Ctrl2Text,
              id=wxID_FRAME1DISPLAYPOWTEAM6CTRL2)

        self.displayPowTeam6Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYPOWTEAM6CTRL3,
              initial=1, max=999, min=1, name=u'displayPowTeam6Ctrl3',
              parent=self.panel7, pos=wx.Point(712, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayPowTeam6Ctrl3.Bind(wx.EVT_TEXT,
              self.OnDisplayPowTeam6Ctrl3Text,
              id=wxID_FRAME1DISPLAYPOWTEAM6CTRL3)

        self.displayPowTeam6Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYPOWTEAM6CTRL4,
              initial=1, max=999, min=1, name=u'displayPowTeam6Ctrl4',
              parent=self.panel7, pos=wx.Point(712, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayPowTeam6Ctrl4.Bind(wx.EVT_TEXT,
              self.OnDisplayPowTeam6Ctrl4Text,
              id=wxID_FRAME1DISPLAYPOWTEAM6CTRL4)

        self.displayPowTeam6Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYPOWTEAM6CTRL5,
              initial=1, max=999, min=1, name=u'displayPowTeam6Ctrl5',
              parent=self.panel7, pos=wx.Point(712, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayPowTeam6Ctrl5.Bind(wx.EVT_TEXT,
              self.OnDisplayPowTeam6Ctrl5Text,
              id=wxID_FRAME1DISPLAYPOWTEAM6CTRL5)

        self.displaySpdTeam6Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYSPDTEAM6CTRL1,
              initial=1, max=999, min=1, name=u'displaySpdTeam6Ctrl1',
              parent=self.panel7, pos=wx.Point(768, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displaySpdTeam6Ctrl1.Bind(wx.EVT_TEXT,
              self.OnDisplaySpdTeam6Ctrl1Text,
              id=wxID_FRAME1DISPLAYSPDTEAM6CTRL1)

        self.displaySpdTeam6Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYSPDTEAM6CTRL2,
              initial=1, max=999, min=1, name=u'displaySpdTeam6Ctrl2',
              parent=self.panel7, pos=wx.Point(768, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displaySpdTeam6Ctrl2.Bind(wx.EVT_TEXT,
              self.OnDisplaySpdTeam6Ctrl2Text,
              id=wxID_FRAME1DISPLAYSPDTEAM6CTRL2)

        self.displaySpdTeam6Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYSPDTEAM6CTRL3,
              initial=1, max=999, min=1, name=u'displaySpdTeam6Ctrl3',
              parent=self.panel7, pos=wx.Point(768, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displaySpdTeam6Ctrl3.Bind(wx.EVT_TEXT,
              self.OnDisplaySpdTeam6Ctrl3Text,
              id=wxID_FRAME1DISPLAYSPDTEAM6CTRL3)

        self.displaySpdTeam6Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYSPDTEAM6CTRL4,
              initial=1, max=999, min=1, name=u'displaySpdTeam6Ctrl4',
              parent=self.panel7, pos=wx.Point(768, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displaySpdTeam6Ctrl4.Bind(wx.EVT_TEXT,
              self.OnDisplaySpdTeam6Ctrl4Text,
              id=wxID_FRAME1DISPLAYSPDTEAM6CTRL4)

        self.displaySpdTeam6Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYSPDTEAM6CTRL5,
              initial=1, max=999, min=1, name=u'displaySpdTeam6Ctrl5',
              parent=self.panel7, pos=wx.Point(768, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displaySpdTeam6Ctrl5.Bind(wx.EVT_TEXT,
              self.OnDisplaySpdTeam6Ctrl5Text,
              id=wxID_FRAME1DISPLAYSPDTEAM6CTRL5)

        self.displayDefTeam6Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYDEFTEAM6CTRL1,
              initial=1, max=999, min=1, name=u'displayDefTeam6Ctrl1',
              parent=self.panel7, pos=wx.Point(824, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayDefTeam6Ctrl1.Bind(wx.EVT_TEXT,
              self.OnDisplayDefTeam6Ctrl1Text,
              id=wxID_FRAME1DISPLAYDEFTEAM6CTRL1)

        self.displayDefTeam6Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYDEFTEAM6CTRL2,
              initial=1, max=999, min=1, name=u'displayDefTeam6Ctrl2',
              parent=self.panel7, pos=wx.Point(824, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayDefTeam6Ctrl2.Bind(wx.EVT_TEXT,
              self.OnDisplayDefTeam6Ctrl2Text,
              id=wxID_FRAME1DISPLAYDEFTEAM6CTRL2)

        self.displayDefTeam6Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYDEFTEAM6CTRL3,
              initial=1, max=999, min=1, name=u'displayDefTeam6Ctrl3',
              parent=self.panel7, pos=wx.Point(824, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayDefTeam6Ctrl3.Bind(wx.EVT_TEXT,
              self.OnDisplayDefTeam6Ctrl3Text,
              id=wxID_FRAME1DISPLAYDEFTEAM6CTRL3)

        self.displayDefTeam6Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYDEFTEAM6CTRL4,
              initial=1, max=999, min=1, name=u'displayDefTeam6Ctrl4',
              parent=self.panel7, pos=wx.Point(824, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayDefTeam6Ctrl4.Bind(wx.EVT_TEXT,
              self.OnDisplayDefTeam6Ctrl4Text,
              id=wxID_FRAME1DISPLAYDEFTEAM6CTRL4)

        self.displayDefTeam6Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYDEFTEAM6CTRL5,
              initial=1, max=999, min=1, name=u'displayDefTeam6Ctrl5',
              parent=self.panel7, pos=wx.Point(824, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayDefTeam6Ctrl5.Bind(wx.EVT_TEXT,
              self.OnDisplayDefTeam6Ctrl5Text,
              id=wxID_FRAME1DISPLAYDEFTEAM6CTRL5)

        self.staticText95 = wx.StaticText(id=wxID_FRAME1STATICTEXT95,
              label=u'Start Power', name='staticText95', parent=self.panel7,
              pos=wx.Point(232, 40), size=wx.Size(57, 14), style=0)

        self.staticText96 = wx.StaticText(id=wxID_FRAME1STATICTEXT96,
              label=u'Max Power', name='staticText96', parent=self.panel7,
              pos=wx.Point(312, 40), size=wx.Size(53, 14), style=0)

        self.staticText97 = wx.StaticText(id=wxID_FRAME1STATICTEXT97,
              label=u'Speed', name='staticText97', parent=self.panel7,
              pos=wx.Point(392, 40), size=wx.Size(30, 14), style=0)

        self.staticText98 = wx.StaticText(id=wxID_FRAME1STATICTEXT98,
              label=u'Weight', name='staticText98', parent=self.panel7,
              pos=wx.Point(464, 40), size=wx.Size(34, 14), style=0)

        self.staticText99 = wx.StaticText(id=wxID_FRAME1STATICTEXT99,
              label=u'Angry', name='staticText99', parent=self.panel7,
              pos=wx.Point(536, 40), size=wx.Size(29, 14), style=0)

        self.staticText100 = wx.StaticText(id=wxID_FRAME1STATICTEXT100,
              label=u'Special Shoot', name='staticText100', parent=self.panel7,
              pos=wx.Point(608, 40), size=wx.Size(64, 14), style=0)

        self.staticText101 = wx.StaticText(id=wxID_FRAME1STATICTEXT101,
              label=u'POW', name='staticText101', parent=self.panel7,
              pos=wx.Point(720, 40), size=wx.Size(24, 14), style=0)

        self.staticText102 = wx.StaticText(id=wxID_FRAME1STATICTEXT102,
              label=u'SPD', name='staticText102', parent=self.panel7,
              pos=wx.Point(776, 40), size=wx.Size(19, 14), style=0)

        self.staticText103 = wx.StaticText(id=wxID_FRAME1STATICTEXT103,
              label=u'DEF', name='staticText103', parent=self.panel7,
              pos=wx.Point(832, 40), size=wx.Size(19, 14), style=0)

        self.sPowerSpinTeam7Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1SPOWERSPINTEAM7CTRL1,
              initial=1, max=12, min=1, name=u'sPowerSpinTeam7Ctrl1',
              parent=self.panel8, pos=wx.Point(240, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.sPowerSpinTeam7Ctrl1.Bind(wx.EVT_TEXT,
              self.OnSPowerSpinTeam7Ctrl1Text,
              id=wxID_FRAME1SPOWERSPINTEAM7CTRL1)

        self.sPowerSpinTeam7Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1SPOWERSPINTEAM7CTRL2,
              initial=1, max=12, min=1, name=u'sPowerSpinTeam7Ctrl2',
              parent=self.panel8, pos=wx.Point(240, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.sPowerSpinTeam7Ctrl2.Bind(wx.EVT_TEXT,
              self.OnSPowerSpinTeam7Ctrl2Text,
              id=wxID_FRAME1SPOWERSPINTEAM7CTRL2)

        self.sPowerSpinTeam7Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1SPOWERSPINTEAM7CTRL3,
              initial=1, max=12, min=1, name=u'sPowerSpinTeam7Ctrl3',
              parent=self.panel8, pos=wx.Point(240, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.sPowerSpinTeam7Ctrl3.Bind(wx.EVT_TEXT,
              self.OnSPowerSpinTeam7Ctrl3Text,
              id=wxID_FRAME1SPOWERSPINTEAM7CTRL3)

        self.sPowerSpinTeam7Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1SPOWERSPINTEAM7CTRL4,
              initial=1, max=12, min=1, name=u'sPowerSpinTeam7Ctrl4',
              parent=self.panel8, pos=wx.Point(240, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.sPowerSpinTeam7Ctrl4.Bind(wx.EVT_TEXT,
              self.OnSPowerSpinTeam7Ctrl4Text,
              id=wxID_FRAME1SPOWERSPINTEAM7CTRL4)

        self.sPowerSpinTeam7Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1SPOWERSPINTEAM7CTRL5,
              initial=1, max=12, min=1, name=u'sPowerSpinTeam7Ctrl5',
              parent=self.panel8, pos=wx.Point(240, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.sPowerSpinTeam7Ctrl5.Bind(wx.EVT_TEXT,
              self.OnSPowerSpinTeam7Ctrl5Text,
              id=wxID_FRAME1SPOWERSPINTEAM7CTRL5)

        self.mPowerSpinTeam7Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1MPOWERSPINTEAM7CTRL1,
              initial=1, max=5, min=1, name=u'mPowerSpinTeam7Ctrl1',
              parent=self.panel8, pos=wx.Point(312, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.mPowerSpinTeam7Ctrl1.Bind(wx.EVT_TEXT,
              self.OnMPowerSpinTeam7Ctrl1Text,
              id=wxID_FRAME1MPOWERSPINTEAM7CTRL1)

        self.mPowerSpinTeam7Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1MPOWERSPINTEAM7CTRL2,
              initial=1, max=5, min=1, name=u'mPowerSpinTeam7Ctrl2',
              parent=self.panel8, pos=wx.Point(312, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.mPowerSpinTeam7Ctrl2.Bind(wx.EVT_TEXT,
              self.OnMPowerSpinTeam7Ctrl2Text,
              id=wxID_FRAME1MPOWERSPINTEAM7CTRL2)

        self.mPowerSpinTeam7Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1MPOWERSPINTEAM7CTRL3,
              initial=1, max=5, min=1, name=u'mPowerSpinTeam7Ctrl3',
              parent=self.panel8, pos=wx.Point(312, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.mPowerSpinTeam7Ctrl3.Bind(wx.EVT_TEXT,
              self.OnMPowerSpinTeam7Ctrl3Text,
              id=wxID_FRAME1MPOWERSPINTEAM7CTRL3)

        self.mPowerSpinTeam7Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1MPOWERSPINTEAM7CTRL4,
              initial=1, max=5, min=1, name=u'mPowerSpinTeam7Ctrl4',
              parent=self.panel8, pos=wx.Point(312, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.mPowerSpinTeam7Ctrl4.Bind(wx.EVT_TEXT,
              self.OnMPowerSpinTeam7Ctrl4Text,
              id=wxID_FRAME1MPOWERSPINTEAM7CTRL4)

        self.mPowerSpinTeam7Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1MPOWERSPINTEAM7CTRL5,
              initial=1, max=5, min=1, name=u'mPowerSpinTeam7Ctrl5',
              parent=self.panel8, pos=wx.Point(312, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.mPowerSpinTeam7Ctrl5.Bind(wx.EVT_TEXT,
              self.OnMPowerSpinTeam7Ctrl5Text,
              id=wxID_FRAME1MPOWERSPINTEAM7CTRL5)

        self.speedSpinTeam7Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1SPEEDSPINTEAM7CTRL1,
              initial=1, max=3, min=1, name=u'speedSpinTeam7Ctrl1',
              parent=self.panel8, pos=wx.Point(384, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.speedSpinTeam7Ctrl1.Bind(wx.EVT_TEXT,
              self.OnSpeedSpinTeam7Ctrl1Text,
              id=wxID_FRAME1SPEEDSPINTEAM7CTRL1)

        self.speedSpinTeam7Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1SPEEDSPINTEAM7CTRL2,
              initial=1, max=3, min=1, name=u'speedSpinTeam7Ctrl2',
              parent=self.panel8, pos=wx.Point(384, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.speedSpinTeam7Ctrl2.Bind(wx.EVT_TEXT,
              self.OnSpeedSpinTeam7Ctrl2Text,
              id=wxID_FRAME1SPEEDSPINTEAM7CTRL2)

        self.speedSpinTeam7Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1SPEEDSPINTEAM7CTRL3,
              initial=1, max=3, min=1, name=u'speedSpinTeam7Ctrl3',
              parent=self.panel8, pos=wx.Point(384, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.speedSpinTeam7Ctrl3.Bind(wx.EVT_TEXT,
              self.OnSpeedSpinTeam7Ctrl3Text,
              id=wxID_FRAME1SPEEDSPINTEAM7CTRL3)

        self.speedSpinTeam7Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1SPEEDSPINTEAM7CTRL4,
              initial=1, max=3, min=1, name=u'speedSpinTeam7Ctrl4',
              parent=self.panel8, pos=wx.Point(384, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.speedSpinTeam7Ctrl4.Bind(wx.EVT_TEXT,
              self.OnSpeedSpinTeam7Ctrl4Text,
              id=wxID_FRAME1SPEEDSPINTEAM7CTRL4)

        self.speedSpinTeam7Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1SPEEDSPINTEAM7CTRL5,
              initial=1, max=3, min=1, name=u'speedSpinTeam7Ctrl5',
              parent=self.panel8, pos=wx.Point(384, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.speedSpinTeam7Ctrl5.Bind(wx.EVT_TEXT,
              self.OnSpeedSpinTeam7Ctrl5Text,
              id=wxID_FRAME1SPEEDSPINTEAM7CTRL5)

        self.weightSpinTeam7Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1WEIGHTSPINTEAM7CTRL1,
              initial=1, max=5, min=1, name=u'weightSpinTeam7Ctrl1',
              parent=self.panel8, pos=wx.Point(456, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.weightSpinTeam7Ctrl1.Bind(wx.EVT_TEXT,
              self.OnWeightSpinTeam7Ctrl1Text,
              id=wxID_FRAME1WEIGHTSPINTEAM7CTRL1)

        self.weightSpinTeam7Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1WEIGHTSPINTEAM7CTRL2,
              initial=1, max=5, min=1, name=u'weightSpinTeam7Ctrl2',
              parent=self.panel8, pos=wx.Point(456, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.weightSpinTeam7Ctrl2.Bind(wx.EVT_TEXT,
              self.OnWeightSpinTeam7Ctrl2Text,
              id=wxID_FRAME1WEIGHTSPINTEAM7CTRL2)

        self.weightSpinTeam7Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1WEIGHTSPINTEAM7CTRL3,
              initial=1, max=5, min=1, name=u'weightSpinTeam7Ctrl3',
              parent=self.panel8, pos=wx.Point(456, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.weightSpinTeam7Ctrl3.Bind(wx.EVT_TEXT,
              self.OnWeightSpinTeam7Ctrl3Text,
              id=wxID_FRAME1WEIGHTSPINTEAM7CTRL3)

        self.weightSpinTeam7Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1WEIGHTSPINTEAM7CTRL4,
              initial=1, max=5, min=1, name=u'weightSpinTeam7Ctrl4',
              parent=self.panel8, pos=wx.Point(456, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.weightSpinTeam7Ctrl4.Bind(wx.EVT_TEXT,
              self.OnWeightSpinTeam7Ctrl4Text,
              id=wxID_FRAME1WEIGHTSPINTEAM7CTRL4)

        self.weightSpinTeam7Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1WEIGHTSPINTEAM7CTRL5,
              initial=1, max=5, min=1, name=u'weightSpinTeam7Ctrl5',
              parent=self.panel8, pos=wx.Point(456, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.weightSpinTeam7Ctrl5.Bind(wx.EVT_TEXT,
              self.OnWeightSpinTeam7Ctrl5Text,
              id=wxID_FRAME1WEIGHTSPINTEAM7CTRL5)

        self.angrySpinTeam7Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1ANGRYSPINTEAM7CTRL1,
              initial=1, max=7, min=1, name=u'angrySpinTeam7Ctrl1',
              parent=self.panel8, pos=wx.Point(528, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.angrySpinTeam7Ctrl1.Bind(wx.EVT_TEXT,
              self.OnAngrySpinTeam7Ctrl1Text,
              id=wxID_FRAME1ANGRYSPINTEAM7CTRL1)

        self.angrySpinTeam7Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1ANGRYSPINTEAM7CTRL2,
              initial=1, max=7, min=1, name=u'angrySpinTeam7Ctrl2',
              parent=self.panel8, pos=wx.Point(528, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.angrySpinTeam7Ctrl2.Bind(wx.EVT_TEXT,
              self.OnAngrySpinTeam7Ctrl2Text,
              id=wxID_FRAME1ANGRYSPINTEAM7CTRL2)

        self.angrySpinTeam7Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1ANGRYSPINTEAM7CTRL3,
              initial=1, max=7, min=1, name=u'angrySpinTeam7Ctrl3',
              parent=self.panel8, pos=wx.Point(528, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.angrySpinTeam7Ctrl3.Bind(wx.EVT_TEXT,
              self.OnAngrySpinTeam7Ctrl3Text,
              id=wxID_FRAME1ANGRYSPINTEAM7CTRL3)

        self.angrySpinTeam7Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1ANGRYSPINTEAM7CTRL4,
              initial=1, max=7, min=1, name=u'angrySpinTeam7Ctrl4',
              parent=self.panel8, pos=wx.Point(528, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.angrySpinTeam7Ctrl4.Bind(wx.EVT_TEXT,
              self.OnAngrySpinTeam7Ctrl4Text,
              id=wxID_FRAME1ANGRYSPINTEAM7CTRL4)

        self.angrySpinTeam7Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1ANGRYSPINTEAM7CTRL5,
              initial=1, max=7, min=1, name=u'angrySpinTeam7Ctrl5',
              parent=self.panel8, pos=wx.Point(528, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.angrySpinTeam7Ctrl5.Bind(wx.EVT_TEXT,
              self.OnAngrySpinTeam7Ctrl5Text,
              id=wxID_FRAME1ANGRYSPINTEAM7CTRL5)

        self.shootTeam7Choice1 = wx.Choice(choices=[],
              id=wxID_FRAME1SHOOTTEAM7CHOICE1, name=u'shootTeam7Choice1',
              parent=self.panel8, pos=wx.Point(592, 64), size=wx.Size(106, 21),
              style=0)
        self.shootTeam7Choice1.Bind(wx.EVT_CHOICE,
              self.OnShootTeam7Choice1Choice, id=wxID_FRAME1SHOOTTEAM7CHOICE1)

        self.shootTeam7Choice2 = wx.Choice(choices=[],
              id=wxID_FRAME1SHOOTTEAM7CHOICE2, name=u'shootTeam7Choice2',
              parent=self.panel8, pos=wx.Point(592, 96), size=wx.Size(106, 21),
              style=0)
        self.shootTeam7Choice2.Bind(wx.EVT_CHOICE,
              self.OnShootTeam7Choice2Choice, id=wxID_FRAME1SHOOTTEAM7CHOICE2)

        self.shootTeam7Choice3 = wx.Choice(choices=[],
              id=wxID_FRAME1SHOOTTEAM7CHOICE3, name=u'shootTeam7Choice3',
              parent=self.panel8, pos=wx.Point(592, 128), size=wx.Size(106, 21),
              style=0)
        self.shootTeam7Choice3.Bind(wx.EVT_CHOICE,
              self.OnShootTeam7Choice3Choice, id=wxID_FRAME1SHOOTTEAM7CHOICE3)

        self.shootTeam7Choice4 = wx.Choice(choices=[],
              id=wxID_FRAME1SHOOTTEAM7CHOICE4, name=u'shootTeam7Choice4',
              parent=self.panel8, pos=wx.Point(592, 160), size=wx.Size(106, 21),
              style=0)
        self.shootTeam7Choice4.Bind(wx.EVT_CHOICE,
              self.OnShootTeam7Choice4Choice, id=wxID_FRAME1SHOOTTEAM7CHOICE4)

        self.shootTeam7Choice5 = wx.Choice(choices=[],
              id=wxID_FRAME1SHOOTTEAM7CHOICE5, name=u'shootTeam7Choice5',
              parent=self.panel8, pos=wx.Point(592, 192), size=wx.Size(106, 21),
              style=0)
        self.shootTeam7Choice5.Bind(wx.EVT_CHOICE,
              self.OnShootTeam7Choice5Choice, id=wxID_FRAME1SHOOTTEAM7CHOICE5)

        self.displayPowTeam7Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYPOWTEAM7CTRL1,
              initial=1, max=999, min=1, name=u'displayPowTeam7Ctrl1',
              parent=self.panel8, pos=wx.Point(712, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayPowTeam7Ctrl1.Bind(wx.EVT_TEXT,
              self.OnDisplayPowTeam7Ctrl1Text,
              id=wxID_FRAME1DISPLAYPOWTEAM7CTRL1)

        self.displayPowTeam7Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYPOWTEAM7CTRL2,
              initial=1, max=999, min=1, name=u'displayPowTeam7Ctrl2',
              parent=self.panel8, pos=wx.Point(712, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayPowTeam7Ctrl2.Bind(wx.EVT_TEXT,
              self.OnDisplayPowTeam7Ctrl2Text,
              id=wxID_FRAME1DISPLAYPOWTEAM7CTRL2)

        self.displayPowTeam7Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYPOWTEAM7CTRL3,
              initial=1, max=999, min=1, name=u'displayPowTeam7Ctrl3',
              parent=self.panel8, pos=wx.Point(712, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayPowTeam7Ctrl3.Bind(wx.EVT_TEXT,
              self.OnDisplayPowTeam7Ctrl3Text,
              id=wxID_FRAME1DISPLAYPOWTEAM7CTRL3)

        self.displayPowTeam7Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYPOWTEAM7CTRL4,
              initial=1, max=999, min=1, name=u'displayPowTeam7Ctrl4',
              parent=self.panel8, pos=wx.Point(712, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayPowTeam7Ctrl4.Bind(wx.EVT_TEXT,
              self.OnDisplayPowTeam7Ctrl4Text,
              id=wxID_FRAME1DISPLAYPOWTEAM7CTRL4)

        self.displayPowTeam7Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYPOWTEAM7CTRL5,
              initial=1, max=999, min=1, name=u'displayPowTeam7Ctrl5',
              parent=self.panel8, pos=wx.Point(712, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayPowTeam7Ctrl5.Bind(wx.EVT_TEXT,
              self.OnDisplayPowTeam7Ctrl5Text,
              id=wxID_FRAME1DISPLAYPOWTEAM7CTRL5)

        self.displaySpdTeam7Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYSPDTEAM7CTRL1,
              initial=1, max=999, min=1, name=u'displaySpdTeam7Ctrl1',
              parent=self.panel8, pos=wx.Point(768, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displaySpdTeam7Ctrl1.Bind(wx.EVT_TEXT,
              self.OnDisplaySpdTeam7Ctrl1Text,
              id=wxID_FRAME1DISPLAYSPDTEAM7CTRL1)

        self.displaySpdTeam7Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYSPDTEAM7CTRL2,
              initial=1, max=999, min=1, name=u'displaySpdTeam7Ctrl2',
              parent=self.panel8, pos=wx.Point(768, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displaySpdTeam7Ctrl2.Bind(wx.EVT_TEXT,
              self.OnDisplaySpdTeam7Ctrl2Text,
              id=wxID_FRAME1DISPLAYSPDTEAM7CTRL2)

        self.displaySpdTeam7Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYSPDTEAM7CTRL3,
              initial=1, max=999, min=1, name=u'displaySpdTeam7Ctrl3',
              parent=self.panel8, pos=wx.Point(768, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displaySpdTeam7Ctrl3.Bind(wx.EVT_TEXT,
              self.OnDisplaySpdTeam7Ctrl3Text,
              id=wxID_FRAME1DISPLAYSPDTEAM7CTRL3)

        self.displaySpdTeam7Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYSPDTEAM7CTRL4,
              initial=1, max=999, min=1, name=u'displaySpdTeam7Ctrl4',
              parent=self.panel8, pos=wx.Point(768, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displaySpdTeam7Ctrl4.Bind(wx.EVT_TEXT,
              self.OnDisplaySpdTeam7Ctrl4Text,
              id=wxID_FRAME1DISPLAYSPDTEAM7CTRL4)

        self.displaySpdTeam7Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYSPDTEAM7CTRL5,
              initial=1, max=999, min=1, name=u'displaySpdTeam7Ctrl5',
              parent=self.panel8, pos=wx.Point(768, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displaySpdTeam7Ctrl5.Bind(wx.EVT_TEXT,
              self.OnDisplaySpdTeam7Ctrl5Text,
              id=wxID_FRAME1DISPLAYSPDTEAM7CTRL5)

        self.displayDefTeam7Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYDEFTEAM7CTRL1,
              initial=1, max=999, min=1, name=u'displayDefTeam7Ctrl1',
              parent=self.panel8, pos=wx.Point(824, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayDefTeam7Ctrl1.Bind(wx.EVT_TEXT,
              self.OnDisplayDefTeam7Ctrl1Text,
              id=wxID_FRAME1DISPLAYDEFTEAM7CTRL1)

        self.displayDefTeam7Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYDEFTEAM7CTRL2,
              initial=1, max=999, min=1, name=u'displayDefTeam7Ctrl2',
              parent=self.panel8, pos=wx.Point(824, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayDefTeam7Ctrl2.Bind(wx.EVT_TEXT,
              self.OnDisplayDefTeam7Ctrl2Text,
              id=wxID_FRAME1DISPLAYDEFTEAM7CTRL2)

        self.displayDefTeam7Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYDEFTEAM7CTRL3,
              initial=1, max=999, min=1, name=u'displayDefTeam7Ctrl3',
              parent=self.panel8, pos=wx.Point(824, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayDefTeam7Ctrl3.Bind(wx.EVT_TEXT,
              self.OnDisplayDefTeam7Ctrl3Text,
              id=wxID_FRAME1DISPLAYDEFTEAM7CTRL3)

        self.displayDefTeam7Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYDEFTEAM7CTRL4,
              initial=1, max=999, min=1, name=u'displayDefTeam7Ctrl4',
              parent=self.panel8, pos=wx.Point(824, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayDefTeam7Ctrl4.Bind(wx.EVT_TEXT,
              self.OnDisplayDefTeam7Ctrl4Text,
              id=wxID_FRAME1DISPLAYDEFTEAM7CTRL4)

        self.displayDefTeam7Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYDEFTEAM7CTRL5,
              initial=1, max=999, min=1, name=u'displayDefTeam7Ctrl5',
              parent=self.panel8, pos=wx.Point(824, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayDefTeam7Ctrl5.Bind(wx.EVT_TEXT,
              self.OnDisplayDefTeam7Ctrl5Text,
              id=wxID_FRAME1DISPLAYDEFTEAM7CTRL5)

        self.staticText104 = wx.StaticText(id=wxID_FRAME1STATICTEXT104,
              label=u'Start Power', name='staticText104', parent=self.panel8,
              pos=wx.Point(232, 40), size=wx.Size(57, 14), style=0)

        self.staticText105 = wx.StaticText(id=wxID_FRAME1STATICTEXT105,
              label=u'Max Power', name='staticText105', parent=self.panel8,
              pos=wx.Point(312, 40), size=wx.Size(53, 14), style=0)

        self.staticText106 = wx.StaticText(id=wxID_FRAME1STATICTEXT106,
              label=u'Speed', name='staticText106', parent=self.panel8,
              pos=wx.Point(392, 40), size=wx.Size(30, 14), style=0)

        self.staticText107 = wx.StaticText(id=wxID_FRAME1STATICTEXT107,
              label=u'Weight', name='staticText107', parent=self.panel8,
              pos=wx.Point(464, 40), size=wx.Size(34, 14), style=0)

        self.staticText108 = wx.StaticText(id=wxID_FRAME1STATICTEXT108,
              label=u'Angry', name='staticText108', parent=self.panel8,
              pos=wx.Point(536, 40), size=wx.Size(29, 14), style=0)

        self.staticText109 = wx.StaticText(id=wxID_FRAME1STATICTEXT109,
              label=u'Special Shoot', name='staticText109', parent=self.panel8,
              pos=wx.Point(608, 40), size=wx.Size(64, 14), style=0)

        self.staticText110 = wx.StaticText(id=wxID_FRAME1STATICTEXT110,
              label=u'POW', name='staticText110', parent=self.panel8,
              pos=wx.Point(720, 40), size=wx.Size(24, 14), style=0)

        self.staticText111 = wx.StaticText(id=wxID_FRAME1STATICTEXT111,
              label=u'SPD', name='staticText111', parent=self.panel8,
              pos=wx.Point(776, 40), size=wx.Size(19, 14), style=0)

        self.staticText112 = wx.StaticText(id=wxID_FRAME1STATICTEXT112,
              label=u'DEF', name='staticText112', parent=self.panel8,
              pos=wx.Point(832, 40), size=wx.Size(19, 14), style=0)

        self.sPowerSpinTeam8Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1SPOWERSPINTEAM8CTRL1,
              initial=1, max=12, min=1, name=u'sPowerSpinTeam8Ctrl1',
              parent=self.panel9, pos=wx.Point(240, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.sPowerSpinTeam8Ctrl1.Bind(wx.EVT_TEXT,
              self.OnSPowerSpinTeam8Ctrl1Text,
              id=wxID_FRAME1SPOWERSPINTEAM8CTRL1)

        self.sPowerSpinTeam8Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1SPOWERSPINTEAM8CTRL2,
              initial=1, max=12, min=1, name=u'sPowerSpinTeam8Ctrl2',
              parent=self.panel9, pos=wx.Point(240, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.sPowerSpinTeam8Ctrl2.Bind(wx.EVT_TEXT,
              self.OnSPowerSpinTeam8Ctrl2Text,
              id=wxID_FRAME1SPOWERSPINTEAM8CTRL2)

        self.sPowerSpinTeam8Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1SPOWERSPINTEAM8CTRL3,
              initial=1, max=12, min=1, name=u'sPowerSpinTeam8Ctrl3',
              parent=self.panel9, pos=wx.Point(240, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.sPowerSpinTeam8Ctrl3.Bind(wx.EVT_TEXT,
              self.OnSPowerSpinTeam8Ctrl3Text,
              id=wxID_FRAME1SPOWERSPINTEAM8CTRL3)

        self.sPowerSpinTeam8Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1SPOWERSPINTEAM8CTRL4,
              initial=1, max=12, min=1, name=u'sPowerSpinTeam8Ctrl4',
              parent=self.panel9, pos=wx.Point(240, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.sPowerSpinTeam8Ctrl4.Bind(wx.EVT_TEXT,
              self.OnSPowerSpinTeam8Ctrl4Text,
              id=wxID_FRAME1SPOWERSPINTEAM8CTRL4)

        self.sPowerSpinTeam8Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1SPOWERSPINTEAM8CTRL5,
              initial=1, max=12, min=1, name=u'sPowerSpinTeam8Ctrl5',
              parent=self.panel9, pos=wx.Point(240, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.sPowerSpinTeam8Ctrl5.Bind(wx.EVT_TEXT,
              self.OnSPowerSpinTeam8Ctrl5Text,
              id=wxID_FRAME1SPOWERSPINTEAM8CTRL5)

        self.mPowerSpinTeam8Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1MPOWERSPINTEAM8CTRL1,
              initial=1, max=5, min=1, name=u'mPowerSpinTeam8Ctrl1',
              parent=self.panel9, pos=wx.Point(312, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.mPowerSpinTeam8Ctrl1.Bind(wx.EVT_TEXT,
              self.OnMPowerSpinTeam8Ctrl1Text,
              id=wxID_FRAME1MPOWERSPINTEAM8CTRL1)

        self.mPowerSpinTeam8Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1MPOWERSPINTEAM8CTRL2,
              initial=1, max=5, min=1, name=u'mPowerSpinTeam8Ctrl2',
              parent=self.panel9, pos=wx.Point(312, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.mPowerSpinTeam8Ctrl2.Bind(wx.EVT_TEXT,
              self.OnMPowerSpinTeam8Ctrl2Text,
              id=wxID_FRAME1MPOWERSPINTEAM8CTRL2)

        self.mPowerSpinTeam8Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1MPOWERSPINTEAM8CTRL3,
              initial=1, max=5, min=1, name=u'mPowerSpinTeam8Ctrl3',
              parent=self.panel9, pos=wx.Point(312, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.mPowerSpinTeam8Ctrl3.Bind(wx.EVT_TEXT,
              self.OnMPowerSpinTeam8Ctrl3Text,
              id=wxID_FRAME1MPOWERSPINTEAM8CTRL3)

        self.mPowerSpinTeam8Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1MPOWERSPINTEAM8CTRL4,
              initial=1, max=5, min=1, name=u'mPowerSpinTeam8Ctrl4',
              parent=self.panel9, pos=wx.Point(312, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.mPowerSpinTeam8Ctrl4.Bind(wx.EVT_TEXT,
              self.OnMPowerSpinTeam8Ctrl4Text,
              id=wxID_FRAME1MPOWERSPINTEAM8CTRL4)

        self.mPowerSpinTeam8Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1MPOWERSPINTEAM8CTRL5,
              initial=1, max=5, min=1, name=u'mPowerSpinTeam8Ctrl5',
              parent=self.panel9, pos=wx.Point(312, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.mPowerSpinTeam8Ctrl5.Bind(wx.EVT_TEXT,
              self.OnMPowerSpinTeam8Ctrl5Text,
              id=wxID_FRAME1MPOWERSPINTEAM8CTRL5)

        self.speedSpinTeam8Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1SPEEDSPINTEAM8CTRL1,
              initial=1, max=3, min=1, name=u'speedSpinTeam8Ctrl1',
              parent=self.panel9, pos=wx.Point(384, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.speedSpinTeam8Ctrl1.Bind(wx.EVT_TEXT,
              self.OnSpeedSpinTeam8Ctrl1Text,
              id=wxID_FRAME1SPEEDSPINTEAM8CTRL1)

        self.speedSpinTeam8Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1SPEEDSPINTEAM8CTRL2,
              initial=1, max=3, min=1, name=u'speedSpinTeam8Ctrl2',
              parent=self.panel9, pos=wx.Point(384, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.speedSpinTeam8Ctrl2.Bind(wx.EVT_TEXT,
              self.OnSpeedSpinTeam8Ctrl2Text,
              id=wxID_FRAME1SPEEDSPINTEAM8CTRL2)

        self.speedSpinTeam8Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1SPEEDSPINTEAM8CTRL3,
              initial=1, max=3, min=1, name=u'speedSpinTeam8Ctrl3',
              parent=self.panel9, pos=wx.Point(384, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.speedSpinTeam8Ctrl3.Bind(wx.EVT_TEXT,
              self.OnSpeedSpinTeam8Ctrl3Text,
              id=wxID_FRAME1SPEEDSPINTEAM8CTRL3)

        self.speedSpinTeam8Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1SPEEDSPINTEAM8CTRL4,
              initial=1, max=3, min=1, name=u'speedSpinTeam8Ctrl4',
              parent=self.panel9, pos=wx.Point(384, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.speedSpinTeam8Ctrl4.Bind(wx.EVT_TEXT,
              self.OnSpeedSpinTeam8Ctrl4Text,
              id=wxID_FRAME1SPEEDSPINTEAM8CTRL4)

        self.speedSpinTeam8Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1SPEEDSPINTEAM8CTRL5,
              initial=1, max=3, min=1, name=u'speedSpinTeam8Ctrl5',
              parent=self.panel9, pos=wx.Point(384, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.speedSpinTeam8Ctrl5.Bind(wx.EVT_TEXT,
              self.OnSpeedSpinTeam8Ctrl5Text,
              id=wxID_FRAME1SPEEDSPINTEAM8CTRL5)

        self.weightSpinTeam8Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1WEIGHTSPINTEAM8CTRL1,
              initial=1, max=5, min=1, name=u'weightSpinTeam8Ctrl1',
              parent=self.panel9, pos=wx.Point(456, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.weightSpinTeam8Ctrl1.Bind(wx.EVT_TEXT,
              self.OnWeightSpinTeam8Ctrl1Text,
              id=wxID_FRAME1WEIGHTSPINTEAM8CTRL1)

        self.weightSpinTeam8Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1WEIGHTSPINTEAM8CTRL2,
              initial=1, max=5, min=1, name=u'weightSpinTeam8Ctrl2',
              parent=self.panel9, pos=wx.Point(456, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.weightSpinTeam8Ctrl2.Bind(wx.EVT_TEXT,
              self.OnWeightSpinTeam8Ctrl2Text,
              id=wxID_FRAME1WEIGHTSPINTEAM8CTRL2)

        self.weightSpinTeam8Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1WEIGHTSPINTEAM8CTRL3,
              initial=1, max=5, min=1, name=u'weightSpinTeam8Ctrl3',
              parent=self.panel9, pos=wx.Point(456, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.weightSpinTeam8Ctrl3.Bind(wx.EVT_TEXT,
              self.OnWeightSpinTeam8Ctrl3Text,
              id=wxID_FRAME1WEIGHTSPINTEAM8CTRL3)

        self.weightSpinTeam8Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1WEIGHTSPINTEAM8CTRL4,
              initial=1, max=5, min=1, name=u'weightSpinTeam8Ctrl4',
              parent=self.panel9, pos=wx.Point(456, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.weightSpinTeam8Ctrl4.Bind(wx.EVT_TEXT,
              self.OnWeightSpinTeam8Ctrl4Text,
              id=wxID_FRAME1WEIGHTSPINTEAM8CTRL4)

        self.weightSpinTeam8Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1WEIGHTSPINTEAM8CTRL5,
              initial=1, max=5, min=1, name=u'weightSpinTeam8Ctrl5',
              parent=self.panel9, pos=wx.Point(456, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.weightSpinTeam8Ctrl5.Bind(wx.EVT_TEXT,
              self.OnWeightSpinTeam8Ctrl5Text,
              id=wxID_FRAME1WEIGHTSPINTEAM8CTRL5)

        self.angrySpinTeam8Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1ANGRYSPINTEAM8CTRL1,
              initial=1, max=7, min=1, name=u'angrySpinTeam8Ctrl1',
              parent=self.panel9, pos=wx.Point(528, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.angrySpinTeam8Ctrl1.Bind(wx.EVT_TEXT,
              self.OnAngrySpinTeam8Ctrl1Text,
              id=wxID_FRAME1ANGRYSPINTEAM8CTRL1)

        self.angrySpinTeam8Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1ANGRYSPINTEAM8CTRL2,
              initial=1, max=7, min=1, name=u'angrySpinTeam8Ctrl2',
              parent=self.panel9, pos=wx.Point(528, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.angrySpinTeam8Ctrl2.Bind(wx.EVT_TEXT,
              self.OnAngrySpinTeam8Ctrl2Text,
              id=wxID_FRAME1ANGRYSPINTEAM8CTRL2)

        self.angrySpinTeam8Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1ANGRYSPINTEAM8CTRL3,
              initial=1, max=7, min=1, name=u'angrySpinTeam8Ctrl3',
              parent=self.panel9, pos=wx.Point(528, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.angrySpinTeam8Ctrl3.Bind(wx.EVT_TEXT,
              self.OnAngrySpinTeam8Ctrl3Text,
              id=wxID_FRAME1ANGRYSPINTEAM8CTRL3)

        self.angrySpinTeam8Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1ANGRYSPINTEAM8CTRL4,
              initial=1, max=7, min=1, name=u'angrySpinTeam8Ctrl4',
              parent=self.panel9, pos=wx.Point(528, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.angrySpinTeam8Ctrl4.Bind(wx.EVT_TEXT,
              self.OnAngrySpinTeam8Ctrl4Text,
              id=wxID_FRAME1ANGRYSPINTEAM8CTRL4)

        self.angrySpinTeam8Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1ANGRYSPINTEAM8CTRL5,
              initial=1, max=7, min=1, name=u'angrySpinTeam8Ctrl5',
              parent=self.panel9, pos=wx.Point(528, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.angrySpinTeam8Ctrl5.Bind(wx.EVT_TEXT,
              self.OnAngrySpinTeam8Ctrl5Text,
              id=wxID_FRAME1ANGRYSPINTEAM8CTRL5)

        self.shootTeam8Choice1 = wx.Choice(choices=[],
              id=wxID_FRAME1SHOOTTEAM8CHOICE1, name=u'shootTeam8Choice1',
              parent=self.panel9, pos=wx.Point(592, 64), size=wx.Size(106, 21),
              style=0)
        self.shootTeam8Choice1.Bind(wx.EVT_CHOICE,
              self.OnShootTeam8Choice1Choice, id=wxID_FRAME1SHOOTTEAM8CHOICE1)

        self.shootTeam8Choice2 = wx.Choice(choices=[],
              id=wxID_FRAME1SHOOTTEAM8CHOICE2, name=u'shootTeam8Choice2',
              parent=self.panel9, pos=wx.Point(592, 96), size=wx.Size(106, 21),
              style=0)
        self.shootTeam8Choice2.Bind(wx.EVT_CHOICE,
              self.OnShootTeam8Choice2Choice, id=wxID_FRAME1SHOOTTEAM8CHOICE2)

        self.shootTeam8Choice3 = wx.Choice(choices=[],
              id=wxID_FRAME1SHOOTTEAM8CHOICE3, name=u'shootTeam8Choice3',
              parent=self.panel9, pos=wx.Point(592, 128), size=wx.Size(106, 21),
              style=0)
        self.shootTeam8Choice3.Bind(wx.EVT_CHOICE,
              self.OnShootTeam8Choice3Choice, id=wxID_FRAME1SHOOTTEAM8CHOICE3)

        self.shootTeam8Choice4 = wx.Choice(choices=[],
              id=wxID_FRAME1SHOOTTEAM8CHOICE4, name=u'shootTeam8Choice4',
              parent=self.panel9, pos=wx.Point(592, 160), size=wx.Size(106, 21),
              style=0)
        self.shootTeam8Choice4.Bind(wx.EVT_CHOICE,
              self.OnShootTeam8Choice4Choice, id=wxID_FRAME1SHOOTTEAM8CHOICE4)

        self.shootTeam8Choice5 = wx.Choice(choices=[],
              id=wxID_FRAME1SHOOTTEAM8CHOICE5, name=u'shootTeam8Choice5',
              parent=self.panel9, pos=wx.Point(592, 192), size=wx.Size(106, 21),
              style=0)
        self.shootTeam8Choice5.Bind(wx.EVT_CHOICE,
              self.OnShootTeam8Choice5Choice, id=wxID_FRAME1SHOOTTEAM8CHOICE5)

        self.displayPowTeam8Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYPOWTEAM8CTRL1,
              initial=1, max=999, min=1, name=u'displayPowTeam8Ctrl1',
              parent=self.panel9, pos=wx.Point(712, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayPowTeam8Ctrl1.Bind(wx.EVT_TEXT,
              self.OnDisplayPowTeam8Ctrl1Text,
              id=wxID_FRAME1DISPLAYPOWTEAM8CTRL1)

        self.displayPowTeam8Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYPOWTEAM8CTRL2,
              initial=1, max=999, min=1, name=u'displayPowTeam8Ctrl2',
              parent=self.panel9, pos=wx.Point(712, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayPowTeam8Ctrl2.Bind(wx.EVT_TEXT,
              self.OnDisplayPowTeam8Ctrl2Text,
              id=wxID_FRAME1DISPLAYPOWTEAM8CTRL2)

        self.displayPowTeam8Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYPOWTEAM8CTRL3,
              initial=1, max=999, min=1, name=u'displayPowTeam8Ctrl3',
              parent=self.panel9, pos=wx.Point(712, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayPowTeam8Ctrl3.Bind(wx.EVT_TEXT,
              self.OnDisplayPowTeam8Ctrl3Text,
              id=wxID_FRAME1DISPLAYPOWTEAM8CTRL3)

        self.displayPowTeam8Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYPOWTEAM8CTRL4,
              initial=1, max=999, min=1, name=u'displayPowTeam8Ctrl4',
              parent=self.panel9, pos=wx.Point(712, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayPowTeam8Ctrl4.Bind(wx.EVT_TEXT,
              self.OnDisplayPowTeam8Ctrl4Text,
              id=wxID_FRAME1DISPLAYPOWTEAM8CTRL4)

        self.displayPowTeam8Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYPOWTEAM8CTRL5,
              initial=1, max=999, min=1, name=u'displayPowTeam8Ctrl5',
              parent=self.panel9, pos=wx.Point(712, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayPowTeam8Ctrl5.Bind(wx.EVT_TEXT,
              self.OnDisplayPowTeam8Ctrl5Text,
              id=wxID_FRAME1DISPLAYPOWTEAM8CTRL5)

        self.displaySpdTeam8Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYSPDTEAM8CTRL1,
              initial=1, max=999, min=1, name=u'displaySpdTeam8Ctrl1',
              parent=self.panel9, pos=wx.Point(768, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displaySpdTeam8Ctrl1.Bind(wx.EVT_TEXT,
              self.OnDisplaySpdTeam8Ctrl1Text,
              id=wxID_FRAME1DISPLAYSPDTEAM8CTRL1)

        self.displaySpdTeam8Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYSPDTEAM8CTRL2,
              initial=1, max=999, min=1, name=u'displaySpdTeam8Ctrl2',
              parent=self.panel9, pos=wx.Point(768, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displaySpdTeam8Ctrl2.Bind(wx.EVT_TEXT,
              self.OnDisplaySpdTeam8Ctrl2Text,
              id=wxID_FRAME1DISPLAYSPDTEAM8CTRL2)

        self.displaySpdTeam8Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYSPDTEAM8CTRL3,
              initial=1, max=999, min=1, name=u'displaySpdTeam8Ctrl3',
              parent=self.panel9, pos=wx.Point(768, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displaySpdTeam8Ctrl3.Bind(wx.EVT_TEXT,
              self.OnDisplaySpdTeam8Ctrl3Text,
              id=wxID_FRAME1DISPLAYSPDTEAM8CTRL3)

        self.displaySpdTeam8Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYSPDTEAM8CTRL4,
              initial=1, max=999, min=1, name=u'displaySpdTeam8Ctrl4',
              parent=self.panel9, pos=wx.Point(768, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displaySpdTeam8Ctrl4.Bind(wx.EVT_TEXT,
              self.OnDisplaySpdTeam8Ctrl4Text,
              id=wxID_FRAME1DISPLAYSPDTEAM8CTRL4)

        self.displaySpdTeam8Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYSPDTEAM8CTRL5,
              initial=1, max=999, min=1, name=u'displaySpdTeam8Ctrl5',
              parent=self.panel9, pos=wx.Point(768, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displaySpdTeam8Ctrl5.Bind(wx.EVT_TEXT,
              self.OnDisplaySpdTeam8Ctrl5Text,
              id=wxID_FRAME1DISPLAYSPDTEAM8CTRL5)

        self.displayDefTeam8Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYDEFTEAM8CTRL1,
              initial=1, max=999, min=1, name=u'displayDefTeam8Ctrl1',
              parent=self.panel9, pos=wx.Point(824, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayDefTeam8Ctrl1.Bind(wx.EVT_TEXT,
              self.OnDisplayDefTeam8Ctrl1Text,
              id=wxID_FRAME1DISPLAYDEFTEAM8CTRL1)

        self.displayDefTeam8Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYDEFTEAM8CTRL2,
              initial=1, max=999, min=1, name=u'displayDefTeam8Ctrl2',
              parent=self.panel9, pos=wx.Point(824, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayDefTeam8Ctrl2.Bind(wx.EVT_TEXT,
              self.OnDisplayDefTeam8Ctrl2Text,
              id=wxID_FRAME1DISPLAYDEFTEAM8CTRL2)

        self.displayDefTeam8Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYDEFTEAM8CTRL3,
              initial=1, max=999, min=1, name=u'displayDefTeam8Ctrl3',
              parent=self.panel9, pos=wx.Point(824, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayDefTeam8Ctrl3.Bind(wx.EVT_TEXT,
              self.OnDisplayDefTeam8Ctrl3Text,
              id=wxID_FRAME1DISPLAYDEFTEAM8CTRL3)

        self.displayDefTeam8Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYDEFTEAM8CTRL4,
              initial=1, max=999, min=1, name=u'displayDefTeam8Ctrl4',
              parent=self.panel9, pos=wx.Point(824, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayDefTeam8Ctrl4.Bind(wx.EVT_TEXT,
              self.OnDisplayDefTeam8Ctrl4Text,
              id=wxID_FRAME1DISPLAYDEFTEAM8CTRL4)

        self.displayDefTeam8Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1DISPLAYDEFTEAM8CTRL5,
              initial=1, max=999, min=1, name=u'displayDefTeam8Ctrl5',
              parent=self.panel9, pos=wx.Point(824, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.displayDefTeam8Ctrl5.Bind(wx.EVT_TEXT,
              self.OnDisplayDefTeam8Ctrl5Text,
              id=wxID_FRAME1DISPLAYDEFTEAM8CTRL5)

        self.staticText113 = wx.StaticText(id=wxID_FRAME1STATICTEXT113,
              label=u'Start Power', name='staticText113', parent=self.panel9,
              pos=wx.Point(232, 40), size=wx.Size(57, 14), style=0)

        self.staticText114 = wx.StaticText(id=wxID_FRAME1STATICTEXT114,
              label=u'Max Power', name='staticText114', parent=self.panel9,
              pos=wx.Point(312, 40), size=wx.Size(53, 14), style=0)

        self.staticText115 = wx.StaticText(id=wxID_FRAME1STATICTEXT115,
              label=u'Speed', name='staticText115', parent=self.panel9,
              pos=wx.Point(392, 40), size=wx.Size(30, 14), style=0)

        self.staticText116 = wx.StaticText(id=wxID_FRAME1STATICTEXT116,
              label=u'Weight', name='staticText116', parent=self.panel9,
              pos=wx.Point(464, 40), size=wx.Size(34, 14), style=0)

        self.staticText117 = wx.StaticText(id=wxID_FRAME1STATICTEXT117,
              label=u'Angry', name='staticText117', parent=self.panel9,
              pos=wx.Point(536, 40), size=wx.Size(29, 14), style=0)

        self.staticText118 = wx.StaticText(id=wxID_FRAME1STATICTEXT118,
              label=u'Special Shoot', name='staticText118', parent=self.panel9,
              pos=wx.Point(608, 40), size=wx.Size(64, 14), style=0)

        self.staticText119 = wx.StaticText(id=wxID_FRAME1STATICTEXT119,
              label=u'POW', name='staticText119', parent=self.panel9,
              pos=wx.Point(720, 40), size=wx.Size(24, 14), style=0)

        self.staticText120 = wx.StaticText(id=wxID_FRAME1STATICTEXT120,
              label=u'SPD', name='staticText120', parent=self.panel9,
              pos=wx.Point(776, 40), size=wx.Size(19, 14), style=0)

        self.staticText121 = wx.StaticText(id=wxID_FRAME1STATICTEXT121,
              label=u'DEF', name='staticText121', parent=self.panel9,
              pos=wx.Point(832, 40), size=wx.Size(19, 14), style=0)

        self._init_coll_notebook1_Pages(self.notebook1)

    def __init__(self, parent):
        self._init_ctrls(parent)
        
        self.rom = 0
        
        self.minutes = 0
        self.seconds = 0
        
        self.superShoot = 0
        
        self.music = [0,0,0,0,0]
        
        self.Teams = 8
        self.Players = 5
        
        # MUSIC CHOICE
        
        for i in range(1,7):
            self.choice1.Append("%d" % i)
            self.choice1.SetSelection(0)
            
            self.choice2.Append("%d" % i)
            self.choice2.SetSelection(0)
            
            self.choice3.Append("%d" % i)
            self.choice3.SetSelection(0)
            
            self.choice4.Append("%d" % i)
            self.choice4.SetSelection(0)
            
            self.choice5.Append("%d" % i)
            self.choice5.SetSelection(0)
        
        
        self.noPenalty = False
        
        # FALL TYPES     
        
        self.fallType = 0
        
        for key, val in sorted(FALL_TYPES.items()):
            self.fallTypeChoice.Append(val["NAME"])
            self.fallTypeChoice.SetSelection(0)
        
        self.flyTypeOnHit = 0
        self.flyTypeOnShoot = 0
        
        self.teamAttack = ['' for x in range (self.Teams)]
        self.teamDefense = ['' for x in range (self.Teams)]
        
        # PLAYER STATS       
        
        self.teamStartPower = [['' for x in range (self.Players)] for x in range (self.Teams)]
        self.teamMaxPower = [['' for x in range (self.Players)] for x in range (self.Teams)]
        self.teamSpeed = [['' for x in range (self.Players)] for x in range (self.Teams)]
        self.teamWeight = [['' for x in range (self.Players)] for x in range (self.Teams)]
        self.teamAngry = [['' for x in range (self.Players)] for x in range (self.Teams)] 
              
        # SHOOT CHOICE
        
        self.sShootSelection = [['0' for x in range(self.Players)] for x in range(self.Teams)]
        self.sShootSelectionHex = [['\x00' for x in range(self.Players)] for x in range(self.Teams)]
        
        self.ShootNames = SHOOT_NAMES
        
        for name in self.ShootNames:
            self.shootTeam1Choice1.Append("%s" % name)
            self.shootTeam2Choice1.Append("%s" % name)
            self.shootTeam3Choice1.Append("%s" % name)
            self.shootTeam4Choice1.Append("%s" % name)
            self.shootTeam5Choice1.Append("%s" % name)
            self.shootTeam6Choice1.Append("%s" % name)
            self.shootTeam7Choice1.Append("%s" % name)
            self.shootTeam8Choice1.Append("%s" % name)
            
            self.shootTeam1Choice1.SetSelection(0)
            self.shootTeam2Choice1.SetSelection(0)
            self.shootTeam3Choice1.SetSelection(0)
            self.shootTeam4Choice1.SetSelection(0)                   
            self.shootTeam5Choice1.SetSelection(0)                  
            self.shootTeam6Choice1.SetSelection(0)                  
            self.shootTeam7Choice1.SetSelection(0)                  
            self.shootTeam8Choice1.SetSelection(0)
            
            self.shootTeam1Choice2.Append("%s" % name)
            self.shootTeam2Choice2.Append("%s" % name)
            self.shootTeam3Choice2.Append("%s" % name)
            self.shootTeam4Choice2.Append("%s" % name)
            self.shootTeam5Choice2.Append("%s" % name)
            self.shootTeam6Choice2.Append("%s" % name)
            self.shootTeam7Choice2.Append("%s" % name)
            self.shootTeam8Choice2.Append("%s" % name)
            
            self.shootTeam1Choice2.SetSelection(0)
            self.shootTeam2Choice2.SetSelection(0)
            self.shootTeam3Choice2.SetSelection(0)
            self.shootTeam4Choice2.SetSelection(0)
            self.shootTeam5Choice2.SetSelection(0)
            self.shootTeam6Choice2.SetSelection(0)
            self.shootTeam7Choice2.SetSelection(0)
            self.shootTeam8Choice2.SetSelection(0)
            
            self.shootTeam1Choice3.Append("%s" % name)
            self.shootTeam2Choice3.Append("%s" % name)
            self.shootTeam3Choice3.Append("%s" % name)
            self.shootTeam4Choice3.Append("%s" % name)
            self.shootTeam5Choice3.Append("%s" % name)
            self.shootTeam6Choice3.Append("%s" % name)
            self.shootTeam7Choice3.Append("%s" % name)
            self.shootTeam8Choice3.Append("%s" % name)
            
            self.shootTeam1Choice3.SetSelection(0)
            self.shootTeam2Choice3.SetSelection(0)
            self.shootTeam3Choice3.SetSelection(0)
            self.shootTeam4Choice3.SetSelection(0)
            self.shootTeam5Choice3.SetSelection(0)
            self.shootTeam6Choice3.SetSelection(0)
            self.shootTeam7Choice3.SetSelection(0)
            self.shootTeam8Choice3.SetSelection(0)
            
            self.shootTeam1Choice4.Append("%s" % name)
            self.shootTeam2Choice4.Append("%s" % name)
            self.shootTeam3Choice4.Append("%s" % name)
            self.shootTeam4Choice4.Append("%s" % name)
            self.shootTeam5Choice4.Append("%s" % name)
            self.shootTeam6Choice4.Append("%s" % name)
            self.shootTeam7Choice4.Append("%s" % name)
            self.shootTeam8Choice4.Append("%s" % name)
            
            self.shootTeam1Choice4.SetSelection(0)
            self.shootTeam2Choice4.SetSelection(0)
            self.shootTeam3Choice4.SetSelection(0)
            self.shootTeam4Choice4.SetSelection(0)
            self.shootTeam5Choice4.SetSelection(0)
            self.shootTeam6Choice4.SetSelection(0)
            self.shootTeam7Choice4.SetSelection(0)
            self.shootTeam8Choice4.SetSelection(0)
            
            self.shootTeam1Choice5.Append("%s" % name)
            self.shootTeam2Choice5.Append("%s" % name)
            self.shootTeam3Choice5.Append("%s" % name)
            self.shootTeam4Choice5.Append("%s" % name)
            self.shootTeam5Choice5.Append("%s" % name)
            self.shootTeam6Choice5.Append("%s" % name)
            self.shootTeam7Choice5.Append("%s" % name)
            self.shootTeam8Choice5.Append("%s" % name)
            
            self.shootTeam1Choice5.SetSelection(0)
            self.shootTeam2Choice5.SetSelection(0)
            self.shootTeam3Choice5.SetSelection(0)
            self.shootTeam4Choice5.SetSelection(0)
            self.shootTeam5Choice5.SetSelection(0)
            self.shootTeam6Choice5.SetSelection(0)
            self.shootTeam7Choice5.SetSelection(0)
            self.shootTeam8Choice5.SetSelection(0)
            
        
        
        self.playersDisplayStats = ['' for i in range(self.Teams)]
            
        
        # TEAM NAME
        
        self.teamName =     ['' for x in range(self.Teams)]
        self.teamHexName =  ['' for x in range(self.Teams)]
        
        
        self.teamPlayerNames =      ['' for x in range(self.Teams)]
        self.teamPlayerHexNames =   ['' for x in range(self.Teams)]
        self.teamPlayerStats =      ['' for x in range(self.Teams)] 
        self.teamPlayerHexStats =   ['' for x in range(self.Teams)]
        
        for i in range(self.Teams):
            self.teamPlayerNames[i]        = ['' for x in range(self.Players)]
            self.teamPlayerHexNames[i]     = ['' for x in range(self.Players)]
            self.teamPlayerStats[i]        = [['' for x in range(5)] for x in range(5)]
            self.teamPlayerHexStats[i]     = [['' for x in range(5)] for x in range(5)]
            
        # GAME OFFSETS
            
        self.team1NameOffset = 0x0105E9
        self.team1StatsOffset = 0x01B3B7
        self.players1NameOffset = (0x0107CD, 0x0107DA, 0x0107F4, 0x010801, 0x0107E7)
        self.players1StatsOffset = (0x01B132, 0x01B13B, 0x01B14D, 0x01B156, 0x01B144)
        self.players1ShootOffset = (0x01B138, 0x01B141, 0x01B153, 0x01B15C, 0x01B14A)
        self.players1DisplayStatsOffset = (0x0107D1, 0x0107DE, 0x0107F8, 0x010805, 0x0107EB)
        
        
        self.team2NameOffset = 0x0105F9
        self.team2StatsOffset = 0x01B3B9
        self.players2NameOffset = (0x01085C, 0x010869, 0x010876, 0x010883, 0x010890)
        self.players2StatsOffset = (0x01B195, 0x01B19E, 0x01B1A7, 0x01B1B0, 0x01B1B9)
        self.players2ShootOffset = (0x01B19B, 0x01B1A4, 0x01B1AD, 0x01B1B6, 0x01B1BF)
        self.players2DisplayStatsOffset = (0x010860, 0x01086D, 0x01087A, 0x010887, 0x010894)
        
        self.team3NameOffset = 0x010609
        self.team3StatsOffset = 0x01B3BB
        self.players3NameOffset = (0x01089D, 0x0108AA, 0x0108B7, 0x0108C4, 0x0108D1)
        self.players3StatsOffset = (0x01B1C2, 0x01B1CB, 0x01B1D4, 0x01B1DD, 0x01B1E6)
        self.players3ShootOffset = (0x01B1C8, 0x01B1D1, 0x01B1DA, 0x01B1E3, 0x01B1EC)
        self.players3DisplayStatsOffset = (0x0108A1, 0x0108AE, 0x0108BB, 0x0108C8, 0x0108D5)
        
        self.team4NameOffset = 0x010619
        self.team4StatsOffset = 0x01B3BF
        self.players4NameOffset = (0x01091F, 0x01092C, 0x010939, 0x010946, 0x010953)
        self.players4StatsOffset = (0x01B21C, 0x01B225, 0x01B22E, 0x01B237, 0x01B240)
        self.players4ShootOffset = (0x01B222, 0x01B22B, 0x01B234, 0x01B23D, 0x01B246)
        self.players4DisplayStatsOffset = (0x010923, 0x010930, 0x01093D, 0x01094A, 0x010957)
        
        self.team5NameOffset = 0x010639
        self.team5StatsOffset = 0x01B3C1
        self.players5NameOffset = (0x010960, 0x01096D, 0x01097A, 0x010987, 0x010994)
        self.players5StatsOffset = (0x01B249, 0x01B252, 0x01B25B, 0x01B264, 0x01B26D)
        self.players5ShootOffset = (0x01B24F, 0x01B258, 0x01B261, 0x01B26A, 0x01B273)
        self.players5DisplayStatsOffset = (0x010964, 0x010971, 0x01097E, 0x01098B, 0x010998)
        
        self.team6NameOffset = 0x010651
        self.team6StatsOffset = 0x01B3C5
        self.players6NameOffset = (0x0108DE, 0x0108EB, 0x0108F8, 0x010905, 0x010912)
        self.players6StatsOffset = (0x01B1EF, 0x01B1F8, 0x01B201, 0x01B20A, 0x01B213)
        self.players6ShootOffset = (0x01B1F5, 0x01B1FE, 0x01B207, 0x01B210, 0x01B219)
        self.players6DisplayStatsOffset = (0x0108E2, 0x0108EF, 0x0108FC, 0x010909, 0x010916)
        
        self.team7NameOffset = 0x010671
        self.team7StatsOffset = 0x01B3C7
        self.players7NameOffset = (0x0109A1, 0x0109AE, 0x0109BB, 0x0109C8, 0x0109D5)
        self.players7StatsOffset = (0x01B276, 0x01B27F, 0x01B288, 0x01B291, 0x01B29A)
        self.players7ShootOffset = (0x01B27C, 0x01B285, 0x01B28B, 0x01B297, 0x01B2A0)
        self.players7DisplayStatsOffset = (0x0109A5, 0x0109B2, 0x0109BF, 0x0109CC, 0x0109D9)
        
        self.team8NameOffset = 0x0106a1
        self.team8StatsOffset = 0x01B3C9
        self.players8NameOffset = (0x010A64, 0x010A71, 0x010A7E, 0x010A8B, 0x010A98)
        self.players8StatsOffset = (0x01B2FD, 0x01B306, 0x01B30F, 0x01B318, 0x01B321)
        self.players8ShootOffset = (0x01B303, 0x01B30C, 0x01B315, 0x01B31E, 0x01B327)
        self.players8DisplayStatsOffset = (0x010A68, 0x010A75, 0x010A82, 0x010A8F, 0x010A9C)
        
        self.team1 = Team(self.team1NameOffset, self.team1StatsOffset, self.players1NameOffset, self.players1ShootOffset, self.players1DisplayStatsOffset)
        self.team2 = Team(self.team2NameOffset, self.team2StatsOffset, self.players2NameOffset, self.players2ShootOffset, self.players2DisplayStatsOffset)
        self.team3 = Team(self.team3NameOffset, self.team3StatsOffset, self.players3NameOffset, self.players3ShootOffset, self.players3DisplayStatsOffset)
        self.team4 = Team(self.team4NameOffset, self.team4StatsOffset, self.players4NameOffset, self.players4ShootOffset, self.players4DisplayStatsOffset)
        self.team5 = Team(self.team5NameOffset, self.team5StatsOffset, self.players5NameOffset, self.players5ShootOffset, self.players5DisplayStatsOffset)
        self.team6 = Team(self.team6NameOffset, self.team6StatsOffset, self.players6NameOffset, self.players6ShootOffset, self.players6DisplayStatsOffset)
        self.team7 = Team(self.team7NameOffset, self.team7StatsOffset, self.players7NameOffset, self.players7ShootOffset, self.players7DisplayStatsOffset)
        self.team8 = Team(self.team8NameOffset, self.team8StatsOffset, self.players8NameOffset, self.players8ShootOffset, self.players8DisplayStatsOffset)
    
    def loadRom(self):
        # General Game Settings
        
        self.minutes , self.seconds = loadtime(self.rom)
        self.minCtrl1.SetValue("%d" % self.minutes)
        self.secCtrl1.SetValue("%2d" % self.seconds)
        
        self.superShoot = loadcharge(self.rom)
        self.shootCtrl1.SetValue("%d" % self.superShoot)
        
        self.music = loadmusic(self.rom)
        self.choice1.SetSelection(self.music[0])
        self.choice2.SetSelection(self.music[1])
        self.choice3.SetSelection(self.music[2])
        self.choice4.SetSelection(self.music[3])
        
        self.noPenalty = loadnopenalty(self.rom)
        self.checkBox1.SetValue(self.noPenalty)
        
        self.fallType = loadFallType(self.rom)
        self.fallTypeChoice.SetSelection(self.fallType)
        
        self.flyTypeOnHit = loadFlyHit(self.rom)
        self.flyHitSpinCtrl.SetValue(self.flyTypeOnHit)
        
        self.flyTypeOnShoot = loadFlyShoot(self.rom)
        self.flyShootSpinCtrl.SetValue(self.flyTypeOnShoot)
        
        # Team Settings
        
        # Team 1
        
        self.teamHexName[0], self.teamPlayerHexNames[0] = self.team1.loadteam(self.rom)
        
        self.teamName[0] = hextostr(self.teamHexName[0])
        self.teamNameCtrl1.SetValue(self.teamName[0].rstrip())
        
        self.team1Stats = self.team1.readTeamStats(self.rom)
        
        self.team1Attack = int(hexlify(self.team1Stats[0]), 16)
        self.team1Defense = int(hexlify(self.team1Stats[1]), 16)
        
        self.team1AttackSpinCtrl1.SetValue(self.team1Attack)
        self.team1DefenseSpinCtrl1.SetValue(self.team1Defense)
        
        for i in range(5):
            self.teamPlayerNames[0][i] = hextostr(self.teamPlayerHexNames[0][i])
        
        self.team1Player1Ctrl.SetValue(self.teamPlayerNames[0][0].rstrip())
        self.team1Player2Ctrl.SetValue(self.teamPlayerNames[0][1].rstrip())
        self.team1Player3Ctrl.SetValue(self.teamPlayerNames[0][2].rstrip())
        self.team1Player4Ctrl.SetValue(self.teamPlayerNames[0][3].rstrip())
        self.team1Player5Ctrl.SetValue(self.teamPlayerNames[0][4].rstrip())
        
        self.team1Player1Stats = self.team1.loadPlayerStats(self.rom, self.players1StatsOffset[0])
        
        self.sPowerSpinTeam1Ctrl1.SetValue(self.team1Player1Stats[0])
        self.mPowerSpinTeam1Ctrl1.SetValue(self.team1Player1Stats[1])
        self.speedSpinTeam1Ctrl1.SetValue(self.team1Player1Stats[2])
        self.weightSpinTeam1Ctrl1.SetValue(self.team1Player1Stats[3])
        self.angrySpinTeam1Ctrl1.SetValue(self.team1Player1Stats[5])
        
        self.team1Player2Stats = self.team1.loadPlayerStats(self.rom, self.players1StatsOffset[1])
        
        self.sPowerSpinTeam1Ctrl2.SetValue(self.team1Player2Stats[0])
        self.mPowerSpinTeam1Ctrl2.SetValue(self.team1Player2Stats[1])
        self.speedSpinTeam1Ctrl2.SetValue(self.team1Player2Stats[2])
        self.weightSpinTeam1Ctrl2.SetValue(self.team1Player2Stats[3])
        self.angrySpinTeam1Ctrl2.SetValue(self.team1Player2Stats[5])
        
        self.team1Player3Stats = self.team1.loadPlayerStats(self.rom, self.players1StatsOffset[2])
        
        self.sPowerSpinTeam1Ctrl3.SetValue(self.team1Player3Stats[0])
        self.mPowerSpinTeam1Ctrl3.SetValue(self.team1Player3Stats[1])
        self.speedSpinTeam1Ctrl3.SetValue(self.team1Player3Stats[2])
        self.weightSpinTeam1Ctrl3.SetValue(self.team1Player3Stats[3])
        self.angrySpinTeam1Ctrl3.SetValue(self.team1Player3Stats[5])
        
        self.team1Player4Stats = self.team1.loadPlayerStats(self.rom, self.players1StatsOffset[3])
        
        self.sPowerSpinTeam1Ctrl4.SetValue(self.team1Player4Stats[0])
        self.mPowerSpinTeam1Ctrl4.SetValue(self.team1Player4Stats[1])
        self.speedSpinTeam1Ctrl4.SetValue(self.team1Player4Stats[2])
        self.weightSpinTeam1Ctrl4.SetValue(self.team1Player4Stats[3])
        self.angrySpinTeam1Ctrl4.SetValue(self.team1Player4Stats[5])
        
        self.team1Player5Stats = self.team1.loadPlayerStats(self.rom, self.players1StatsOffset[4])
        
        self.sPowerSpinTeam1Ctrl5.SetValue(self.team1Player5Stats[0])
        self.mPowerSpinTeam1Ctrl5.SetValue(self.team1Player5Stats[1])
        self.speedSpinTeam1Ctrl5.SetValue(self.team1Player5Stats[2])
        self.weightSpinTeam1Ctrl5.SetValue(self.team1Player5Stats[3])
        self.angrySpinTeam1Ctrl5.SetValue(self.team1Player5Stats[5])
        
        
        
        self.sShootSelection[0] = self.team1.sShootRead(self.rom)
        
        self.shootTeam1Choice1.SetSelection(int(self.sShootSelection[0][0]))
        self.shootTeam1Choice2.SetSelection(int(self.sShootSelection[0][1]))
        self.shootTeam1Choice3.SetSelection(int(self.sShootSelection[0][2]))
        self.shootTeam1Choice4.SetSelection(int(self.sShootSelection[0][3]))
        self.shootTeam1Choice5.SetSelection(int(self.sShootSelection[0][4]))
        
        self.playersDisplayStats[0] = self.team1.readDisplayStats(self.rom)
        
        self.displayPowTeam1Ctrl1.SetValue(int(self.playersDisplayStats[0][0][0]))
        self.displayPowTeam1Ctrl2.SetValue(int(self.playersDisplayStats[0][0][1]))
        self.displayPowTeam1Ctrl3.SetValue(int(self.playersDisplayStats[0][0][2]))
        self.displayPowTeam1Ctrl4.SetValue(int(self.playersDisplayStats[0][0][3]))
        self.displayPowTeam1Ctrl5.SetValue(int(self.playersDisplayStats[0][0][4]))
        
        self.displaySpdTeam1Ctrl1.SetValue(int(self.playersDisplayStats[0][1][0]))
        self.displaySpdTeam1Ctrl2.SetValue(int(self.playersDisplayStats[0][1][1]))
        self.displaySpdTeam1Ctrl3.SetValue(int(self.playersDisplayStats[0][1][2]))
        self.displaySpdTeam1Ctrl4.SetValue(int(self.playersDisplayStats[0][1][3]))
        self.displaySpdTeam1Ctrl5.SetValue(int(self.playersDisplayStats[0][1][4]))
        
        self.displayDefTeam1Ctrl1.SetValue(int(self.playersDisplayStats[0][2][0]))
        self.displayDefTeam1Ctrl2.SetValue(int(self.playersDisplayStats[0][2][1]))
        self.displayDefTeam1Ctrl3.SetValue(int(self.playersDisplayStats[0][2][2]))
        self.displayDefTeam1Ctrl4.SetValue(int(self.playersDisplayStats[0][2][3]))
        self.displayDefTeam1Ctrl5.SetValue(int(self.playersDisplayStats[0][2][4]))
        
        # Team 2
        
        self.teamHexName[1], self.teamPlayerHexNames[1] = self.team2.loadteam(self.rom)
        
        self.teamName[1] = hextostr(self.teamHexName[1])
        self.teamNameCtrl2.SetValue(self.teamName[1].rstrip())
        
        self.team2Stats = self.team2.readTeamStats(self.rom)
        
        self.team2Attack = int(hexlify(self.team2Stats[0]), 16)
        self.team2Defense = int(hexlify(self.team2Stats[1]), 16)
        
        self.team2AttackSpinCtrl1.SetValue(self.team2Attack)
        self.team2DefenseSpinCtrl1.SetValue(self.team2Defense)
        
        for i in range(5):
            self.teamPlayerNames[1][i] = hextostr(self.teamPlayerHexNames[1][i])
        
        self.team2Player1Ctrl.SetValue(self.teamPlayerNames[1][0].rstrip())
        self.team2Player2Ctrl.SetValue(self.teamPlayerNames[1][1].rstrip())
        self.team2Player3Ctrl.SetValue(self.teamPlayerNames[1][2].rstrip())
        self.team2Player4Ctrl.SetValue(self.teamPlayerNames[1][3].rstrip())
        self.team2Player5Ctrl.SetValue(self.teamPlayerNames[1][4].rstrip())
        
        self.team2Player1Stats = self.team2.loadPlayerStats(self.rom, self.players2StatsOffset[0])
        
        self.sPowerSpinTeam2Ctrl1.SetValue(self.team2Player1Stats[0])
        self.mPowerSpinTeam2Ctrl1.SetValue(self.team2Player1Stats[1])
        self.speedSpinTeam2Ctrl1.SetValue(self.team2Player1Stats[2])
        self.weightSpinTeam2Ctrl1.SetValue(self.team2Player1Stats[3])
        self.angrySpinTeam2Ctrl1.SetValue(self.team2Player1Stats[5])
        
        
        self.team2Player2Stats = self.team2.loadPlayerStats(self.rom, self.players2StatsOffset[1])
        
        self.sPowerSpinTeam2Ctrl2.SetValue(self.team2Player2Stats[0])
        self.mPowerSpinTeam2Ctrl2.SetValue(self.team2Player2Stats[1])
        self.speedSpinTeam2Ctrl2.SetValue(self.team2Player2Stats[2])
        self.weightSpinTeam2Ctrl2.SetValue(self.team2Player2Stats[3])
        self.angrySpinTeam2Ctrl2.SetValue(self.team2Player2Stats[5])
        
        self.team2Player3Stats = self.team2.loadPlayerStats(self.rom, self.players2StatsOffset[2])
        
        self.sPowerSpinTeam2Ctrl3.SetValue(self.team2Player3Stats[0])
        self.mPowerSpinTeam2Ctrl3.SetValue(self.team2Player3Stats[1])
        self.speedSpinTeam2Ctrl3.SetValue(self.team2Player3Stats[2])
        self.weightSpinTeam2Ctrl3.SetValue(self.team2Player3Stats[3])
        self.angrySpinTeam2Ctrl3.SetValue(self.team2Player3Stats[5])
        
        self.team2Player4Stats = self.team2.loadPlayerStats(self.rom, self.players2StatsOffset[3])
        
        self.sPowerSpinTeam2Ctrl4.SetValue(self.team2Player4Stats[0])
        self.mPowerSpinTeam2Ctrl4.SetValue(self.team2Player4Stats[1])
        self.speedSpinTeam2Ctrl4.SetValue(self.team2Player4Stats[2])
        self.weightSpinTeam2Ctrl4.SetValue(self.team2Player4Stats[3])
        self.angrySpinTeam2Ctrl4.SetValue(self.team2Player4Stats[5])
        
        self.team2Player5Stats = self.team2.loadPlayerStats(self.rom, self.players2StatsOffset[4])
        
        self.sPowerSpinTeam2Ctrl5.SetValue(self.team2Player5Stats[0])
        self.mPowerSpinTeam2Ctrl5.SetValue(self.team2Player5Stats[1])
        self.speedSpinTeam2Ctrl5.SetValue(self.team2Player5Stats[2])
        self.weightSpinTeam2Ctrl5.SetValue(self.team2Player5Stats[3])
        self.angrySpinTeam2Ctrl5.SetValue(self.team2Player5Stats[5])
        
        self.sShootSelection[1] = self.team2.sShootRead(self.rom)
        
        self.shootTeam2Choice1.SetSelection(int(self.sShootSelection[1][0]))
        self.shootTeam2Choice2.SetSelection(int(self.sShootSelection[1][1]))
        self.shootTeam2Choice3.SetSelection(int(self.sShootSelection[1][2]))
        self.shootTeam2Choice4.SetSelection(int(self.sShootSelection[1][3]))
        self.shootTeam2Choice5.SetSelection(int(self.sShootSelection[1][4]))
        
        self.playersDisplayStats[1] = self.team2.readDisplayStats(self.rom)
        
        self.displayPowTeam2Ctrl1.SetValue(int(self.playersDisplayStats[1][0][0]))
        self.displayPowTeam2Ctrl2.SetValue(int(self.playersDisplayStats[1][0][1]))
        self.displayPowTeam2Ctrl3.SetValue(int(self.playersDisplayStats[1][0][2]))
        self.displayPowTeam2Ctrl4.SetValue(int(self.playersDisplayStats[1][0][3]))
        self.displayPowTeam2Ctrl5.SetValue(int(self.playersDisplayStats[1][0][4]))
        
        self.displaySpdTeam2Ctrl1.SetValue(int(self.playersDisplayStats[1][1][0]))
        self.displaySpdTeam2Ctrl2.SetValue(int(self.playersDisplayStats[1][1][1]))
        self.displaySpdTeam2Ctrl3.SetValue(int(self.playersDisplayStats[1][1][2]))
        self.displaySpdTeam2Ctrl4.SetValue(int(self.playersDisplayStats[1][1][3]))
        self.displaySpdTeam2Ctrl5.SetValue(int(self.playersDisplayStats[1][1][4]))
        
        self.displayDefTeam2Ctrl1.SetValue(int(self.playersDisplayStats[1][2][0]))
        self.displayDefTeam2Ctrl2.SetValue(int(self.playersDisplayStats[1][2][1]))
        self.displayDefTeam2Ctrl3.SetValue(int(self.playersDisplayStats[1][2][2]))
        self.displayDefTeam2Ctrl4.SetValue(int(self.playersDisplayStats[1][2][3]))
        self.displayDefTeam2Ctrl5.SetValue(int(self.playersDisplayStats[1][2][4]))
        
        # Team 3
        
        self.teamHexName[2], self.teamPlayerHexNames[2] = self.team3.loadteam(self.rom)
        
        self.teamName[2] = hextostr(self.teamHexName[2])
        self.teamNameCtrl3.SetValue(self.teamName[2].rstrip())
        
        self.team3Stats = self.team3.readTeamStats(self.rom)
        
        self.team3Attack = int(hexlify(self.team3Stats[0]), 16)
        self.team3Defense = int(hexlify(self.team3Stats[1]), 16)
        
        self.team3AttackSpinCtrl1.SetValue(self.team3Attack)
        self.team3DefenseSpinCtrl1.SetValue(self.team3Defense)
        
        for i in range(5):
            self.teamPlayerNames[2][i] = hextostr(self.teamPlayerHexNames[2][i])
        
        self.team3Player1Ctrl.SetValue(self.teamPlayerNames[2][0].rstrip())
        self.team3Player2Ctrl.SetValue(self.teamPlayerNames[2][1].rstrip())
        self.team3Player3Ctrl.SetValue(self.teamPlayerNames[2][2].rstrip())
        self.team3Player4Ctrl.SetValue(self.teamPlayerNames[2][3].rstrip())
        self.team3Player5Ctrl.SetValue(self.teamPlayerNames[2][4].rstrip())
        
        self.team3Player1Stats = self.team3.loadPlayerStats(self.rom, self.players3StatsOffset[0])
        
        self.sPowerSpinTeam3Ctrl1.SetValue(self.team3Player1Stats[0])
        self.mPowerSpinTeam3Ctrl1.SetValue(self.team3Player1Stats[1])
        self.speedSpinTeam3Ctrl1.SetValue(self.team3Player1Stats[2])
        self.weightSpinTeam3Ctrl1.SetValue(self.team3Player1Stats[3])
        self.angrySpinTeam3Ctrl1.SetValue(self.team3Player1Stats[5])
        
        
        self.team3Player2Stats = self.team3.loadPlayerStats(self.rom, self.players3StatsOffset[1])
        
        self.sPowerSpinTeam3Ctrl2.SetValue(self.team3Player2Stats[0])
        self.mPowerSpinTeam3Ctrl2.SetValue(self.team3Player2Stats[1])
        self.speedSpinTeam3Ctrl2.SetValue(self.team3Player2Stats[2])
        self.weightSpinTeam3Ctrl2.SetValue(self.team3Player2Stats[3])
        self.angrySpinTeam3Ctrl2.SetValue(self.team3Player2Stats[5])
        
        self.team3Player3Stats = self.team3.loadPlayerStats(self.rom, self.players3StatsOffset[2])
        
        self.sPowerSpinTeam3Ctrl3.SetValue(self.team3Player3Stats[0])
        self.mPowerSpinTeam3Ctrl3.SetValue(self.team3Player3Stats[1])
        self.speedSpinTeam3Ctrl3.SetValue(self.team3Player3Stats[2])
        self.weightSpinTeam3Ctrl3.SetValue(self.team3Player3Stats[3])
        self.angrySpinTeam3Ctrl3.SetValue(self.team3Player3Stats[5])
        
        self.team3Player4Stats = self.team3.loadPlayerStats(self.rom, self.players3StatsOffset[3])
        
        self.sPowerSpinTeam3Ctrl4.SetValue(self.team3Player4Stats[0])
        self.mPowerSpinTeam3Ctrl4.SetValue(self.team3Player4Stats[1])
        self.speedSpinTeam3Ctrl4.SetValue(self.team3Player4Stats[2])
        self.weightSpinTeam3Ctrl4.SetValue(self.team3Player4Stats[3])
        self.angrySpinTeam3Ctrl4.SetValue(self.team3Player4Stats[5])
        
        self.team3Player5Stats = self.team3.loadPlayerStats(self.rom, self.players3StatsOffset[4])
        
        self.sPowerSpinTeam3Ctrl5.SetValue(self.team3Player5Stats[0])
        self.mPowerSpinTeam3Ctrl5.SetValue(self.team3Player5Stats[1])
        self.speedSpinTeam3Ctrl5.SetValue(self.team3Player5Stats[2])
        self.weightSpinTeam3Ctrl5.SetValue(self.team3Player5Stats[3])
        self.angrySpinTeam3Ctrl5.SetValue(self.team3Player5Stats[5])
        
        self.sShootSelection[2] = self.team3.sShootRead(self.rom)
        
        self.shootTeam3Choice1.SetSelection(int(self.sShootSelection[2][0]))
        self.shootTeam3Choice2.SetSelection(int(self.sShootSelection[2][1]))
        self.shootTeam3Choice3.SetSelection(int(self.sShootSelection[2][2]))
        self.shootTeam3Choice4.SetSelection(int(self.sShootSelection[2][3]))
        self.shootTeam3Choice5.SetSelection(int(self.sShootSelection[2][4]))
        
        self.playersDisplayStats[2] = self.team3.readDisplayStats(self.rom)
        
        self.displayPowTeam3Ctrl1.SetValue(int(self.playersDisplayStats[2][0][0]))
        self.displayPowTeam3Ctrl2.SetValue(int(self.playersDisplayStats[2][0][1]))
        self.displayPowTeam3Ctrl3.SetValue(int(self.playersDisplayStats[2][0][2]))
        self.displayPowTeam3Ctrl4.SetValue(int(self.playersDisplayStats[2][0][3]))
        self.displayPowTeam3Ctrl5.SetValue(int(self.playersDisplayStats[2][0][4]))
        
        self.displaySpdTeam3Ctrl1.SetValue(int(self.playersDisplayStats[2][1][0]))
        self.displaySpdTeam3Ctrl2.SetValue(int(self.playersDisplayStats[2][1][1]))
        self.displaySpdTeam3Ctrl3.SetValue(int(self.playersDisplayStats[2][1][2]))
        self.displaySpdTeam3Ctrl4.SetValue(int(self.playersDisplayStats[2][1][3]))
        self.displaySpdTeam3Ctrl5.SetValue(int(self.playersDisplayStats[2][1][4]))
        
        self.displayDefTeam3Ctrl1.SetValue(int(self.playersDisplayStats[2][2][0]))
        self.displayDefTeam3Ctrl2.SetValue(int(self.playersDisplayStats[2][2][1]))
        self.displayDefTeam3Ctrl3.SetValue(int(self.playersDisplayStats[2][2][2]))
        self.displayDefTeam3Ctrl4.SetValue(int(self.playersDisplayStats[2][2][3]))
        self.displayDefTeam3Ctrl5.SetValue(int(self.playersDisplayStats[2][2][4]))

        # Team 4
        
        self.teamHexName[3], self.teamPlayerHexNames[3] = self.team4.loadteam(self.rom)
        
        self.teamName[3] = hextostr(self.teamHexName[3])
        self.teamNameCtrl4.SetValue(self.teamName[3].rstrip())
        
        self.team4Stats = self.team4.readTeamStats(self.rom)
        
        self.team4Attack = int(hexlify(self.team4Stats[0]), 16)
        self.team4Defense = int(hexlify(self.team4Stats[1]), 16)
        
        self.team4AttackSpinCtrl1.SetValue(self.team4Attack)
        self.team4DefenseSpinCtrl1.SetValue(self.team4Defense)
        
        for i in range(5):
            self.teamPlayerNames[3][i] = hextostr(self.teamPlayerHexNames[3][i])
        
        self.team4Player1Ctrl.SetValue(self.teamPlayerNames[3][0].rstrip())
        self.team4Player2Ctrl.SetValue(self.teamPlayerNames[3][1].rstrip())
        self.team4Player3Ctrl.SetValue(self.teamPlayerNames[3][2].rstrip())
        self.team4Player4Ctrl.SetValue(self.teamPlayerNames[3][3].rstrip())
        self.team4Player5Ctrl.SetValue(self.teamPlayerNames[3][4].rstrip())
        
        self.team4Player1Stats = self.team4.loadPlayerStats(self.rom, self.players4StatsOffset[0])
        
        self.sPowerSpinTeam4Ctrl1.SetValue(self.team4Player1Stats[0])
        self.mPowerSpinTeam4Ctrl1.SetValue(self.team4Player1Stats[1])
        self.speedSpinTeam4Ctrl1.SetValue(self.team4Player1Stats[2])
        self.weightSpinTeam4Ctrl1.SetValue(self.team4Player1Stats[3])
        self.angrySpinTeam4Ctrl1.SetValue(self.team4Player1Stats[5])
        
        
        self.team4Player2Stats = self.team4.loadPlayerStats(self.rom, self.players4StatsOffset[1])
        
        self.sPowerSpinTeam4Ctrl2.SetValue(self.team4Player2Stats[0])
        self.mPowerSpinTeam4Ctrl2.SetValue(self.team4Player2Stats[1])
        self.speedSpinTeam4Ctrl2.SetValue(self.team4Player2Stats[2])
        self.weightSpinTeam4Ctrl2.SetValue(self.team4Player2Stats[3])
        self.angrySpinTeam4Ctrl2.SetValue(self.team4Player2Stats[5])
        
        self.team4Player3Stats = self.team4.loadPlayerStats(self.rom, self.players4StatsOffset[2])
        
        self.sPowerSpinTeam4Ctrl3.SetValue(self.team4Player3Stats[0])
        self.mPowerSpinTeam4Ctrl3.SetValue(self.team4Player3Stats[1])
        self.speedSpinTeam4Ctrl3.SetValue(self.team4Player3Stats[2])
        self.weightSpinTeam4Ctrl3.SetValue(self.team4Player3Stats[3])
        self.angrySpinTeam4Ctrl3.SetValue(self.team4Player3Stats[5])
        
        self.team4Player4Stats = self.team4.loadPlayerStats(self.rom, self.players4StatsOffset[3])
        
        self.sPowerSpinTeam4Ctrl4.SetValue(self.team4Player4Stats[0])
        self.mPowerSpinTeam4Ctrl4.SetValue(self.team4Player4Stats[1])
        self.speedSpinTeam4Ctrl4.SetValue(self.team4Player4Stats[2])
        self.weightSpinTeam4Ctrl4.SetValue(self.team4Player4Stats[3])
        self.angrySpinTeam4Ctrl4.SetValue(self.team4Player4Stats[5])
        
        self.team4Player5Stats = self.team4.loadPlayerStats(self.rom, self.players4StatsOffset[4])
        
        self.sPowerSpinTeam4Ctrl5.SetValue(self.team4Player5Stats[0])
        self.mPowerSpinTeam4Ctrl5.SetValue(self.team4Player5Stats[1])
        self.speedSpinTeam4Ctrl5.SetValue(self.team4Player5Stats[2])
        self.weightSpinTeam4Ctrl5.SetValue(self.team4Player5Stats[3])
        self.angrySpinTeam4Ctrl5.SetValue(self.team4Player5Stats[5])
        
        self.sShootSelection[3] = self.team4.sShootRead(self.rom)
        
        self.shootTeam4Choice1.SetSelection(int(self.sShootSelection[3][0]))
        self.shootTeam4Choice2.SetSelection(int(self.sShootSelection[3][1]))
        self.shootTeam4Choice3.SetSelection(int(self.sShootSelection[3][2]))
        self.shootTeam4Choice4.SetSelection(int(self.sShootSelection[3][3]))
        self.shootTeam4Choice5.SetSelection(int(self.sShootSelection[3][4]))
        
        self.playersDisplayStats[3] = self.team4.readDisplayStats(self.rom)
        
        self.displayPowTeam4Ctrl1.SetValue(int(self.playersDisplayStats[3][0][0]))
        self.displayPowTeam4Ctrl2.SetValue(int(self.playersDisplayStats[3][0][1]))
        self.displayPowTeam4Ctrl3.SetValue(int(self.playersDisplayStats[3][0][2]))
        self.displayPowTeam4Ctrl4.SetValue(int(self.playersDisplayStats[3][0][3]))
        self.displayPowTeam4Ctrl5.SetValue(int(self.playersDisplayStats[3][0][4]))
        
        self.displaySpdTeam4Ctrl1.SetValue(int(self.playersDisplayStats[3][1][0]))
        self.displaySpdTeam4Ctrl2.SetValue(int(self.playersDisplayStats[3][1][1]))
        self.displaySpdTeam4Ctrl3.SetValue(int(self.playersDisplayStats[3][1][2]))
        self.displaySpdTeam4Ctrl4.SetValue(int(self.playersDisplayStats[3][1][3]))
        self.displaySpdTeam4Ctrl5.SetValue(int(self.playersDisplayStats[3][1][4]))
        
        self.displayDefTeam4Ctrl1.SetValue(int(self.playersDisplayStats[3][2][0]))
        self.displayDefTeam4Ctrl2.SetValue(int(self.playersDisplayStats[3][2][1]))
        self.displayDefTeam4Ctrl3.SetValue(int(self.playersDisplayStats[3][2][2]))
        self.displayDefTeam4Ctrl4.SetValue(int(self.playersDisplayStats[3][2][3]))
        self.displayDefTeam4Ctrl5.SetValue(int(self.playersDisplayStats[3][2][4]))
        
        # Team 5
        
        self.teamHexName[4], self.teamPlayerHexNames[4] = self.team5.loadteam(self.rom)
        
        self.teamName[4] = hextostr(self.teamHexName[4])
        self.teamNameCtrl5.SetValue(self.teamName[4].rstrip())
        
        self.team5Stats = self.team5.readTeamStats(self.rom)
        
        self.team5Attack = int(hexlify(self.team5Stats[0]), 16)
        self.team5Defense = int(hexlify(self.team5Stats[1]), 16)
        
        self.team5AttackSpinCtrl1.SetValue(self.team5Attack)
        self.team5DefenseSpinCtrl1.SetValue(self.team5Defense)
        
        for i in range(5):
            self.teamPlayerNames[4][i] = hextostr(self.teamPlayerHexNames[4][i])
        
        self.team5Player1Ctrl.SetValue(self.teamPlayerNames[4][0].rstrip())
        self.team5Player2Ctrl.SetValue(self.teamPlayerNames[4][1].rstrip())
        self.team5Player3Ctrl.SetValue(self.teamPlayerNames[4][2].rstrip())
        self.team5Player4Ctrl.SetValue(self.teamPlayerNames[4][3].rstrip())
        self.team5Player5Ctrl.SetValue(self.teamPlayerNames[4][4].rstrip())
        
        self.team5Player1Stats = self.team5.loadPlayerStats(self.rom, self.players5StatsOffset[0])
        
        self.sPowerSpinTeam5Ctrl1.SetValue(self.team5Player1Stats[0])
        self.mPowerSpinTeam5Ctrl1.SetValue(self.team5Player1Stats[1])
        self.speedSpinTeam5Ctrl1.SetValue(self.team5Player1Stats[2])
        self.weightSpinTeam5Ctrl1.SetValue(self.team5Player1Stats[3])
        self.angrySpinTeam5Ctrl1.SetValue(self.team5Player1Stats[5])
        
        
        self.team5Player2Stats = self.team5.loadPlayerStats(self.rom, self.players5StatsOffset[1])
        
        self.sPowerSpinTeam5Ctrl2.SetValue(self.team5Player2Stats[0])
        self.mPowerSpinTeam5Ctrl2.SetValue(self.team5Player2Stats[1])
        self.speedSpinTeam5Ctrl2.SetValue(self.team5Player2Stats[2])
        self.weightSpinTeam5Ctrl2.SetValue(self.team5Player2Stats[3])
        self.angrySpinTeam5Ctrl2.SetValue(self.team5Player2Stats[5])
        
        self.team5Player3Stats = self.team5.loadPlayerStats(self.rom, self.players5StatsOffset[2])
        
        self.sPowerSpinTeam5Ctrl3.SetValue(self.team5Player3Stats[0])
        self.mPowerSpinTeam5Ctrl3.SetValue(self.team5Player3Stats[1])
        self.speedSpinTeam5Ctrl3.SetValue(self.team5Player3Stats[2])
        self.weightSpinTeam5Ctrl3.SetValue(self.team5Player3Stats[3])
        self.angrySpinTeam5Ctrl3.SetValue(self.team5Player3Stats[5])
        
        self.team5Player4Stats = self.team5.loadPlayerStats(self.rom, self.players5StatsOffset[3])
        
        self.sPowerSpinTeam5Ctrl4.SetValue(self.team5Player4Stats[0])
        self.mPowerSpinTeam5Ctrl4.SetValue(self.team5Player4Stats[1])
        self.speedSpinTeam5Ctrl4.SetValue(self.team5Player4Stats[2])
        self.weightSpinTeam5Ctrl4.SetValue(self.team5Player4Stats[3])
        self.angrySpinTeam5Ctrl4.SetValue(self.team5Player4Stats[5])
        
        self.team5Player5Stats = self.team5.loadPlayerStats(self.rom, self.players5StatsOffset[4])
        
        self.sPowerSpinTeam5Ctrl5.SetValue(self.team5Player5Stats[0])
        self.mPowerSpinTeam5Ctrl5.SetValue(self.team5Player5Stats[1])
        self.speedSpinTeam5Ctrl5.SetValue(self.team5Player5Stats[2])
        self.weightSpinTeam5Ctrl5.SetValue(self.team5Player5Stats[3])
        self.angrySpinTeam5Ctrl5.SetValue(self.team5Player5Stats[5])
        
        self.sShootSelection[4] = self.team5.sShootRead(self.rom)
        
        self.shootTeam5Choice1.SetSelection(int(self.sShootSelection[4][0]))
        self.shootTeam5Choice2.SetSelection(int(self.sShootSelection[4][1]))
        self.shootTeam5Choice3.SetSelection(int(self.sShootSelection[4][2]))
        self.shootTeam5Choice4.SetSelection(int(self.sShootSelection[4][3]))
        self.shootTeam5Choice5.SetSelection(int(self.sShootSelection[4][4]))
        
        self.playersDisplayStats[4] = self.team5.readDisplayStats(self.rom)
        
        self.displayPowTeam5Ctrl1.SetValue(int(self.playersDisplayStats[4][0][0]))
        self.displayPowTeam5Ctrl2.SetValue(int(self.playersDisplayStats[4][0][1]))
        self.displayPowTeam5Ctrl3.SetValue(int(self.playersDisplayStats[4][0][2]))
        self.displayPowTeam5Ctrl4.SetValue(int(self.playersDisplayStats[4][0][3]))
        self.displayPowTeam5Ctrl5.SetValue(int(self.playersDisplayStats[4][0][4]))
        
        self.displaySpdTeam5Ctrl1.SetValue(int(self.playersDisplayStats[4][1][0]))
        self.displaySpdTeam5Ctrl2.SetValue(int(self.playersDisplayStats[4][1][1]))
        self.displaySpdTeam5Ctrl3.SetValue(int(self.playersDisplayStats[4][1][2]))
        self.displaySpdTeam5Ctrl4.SetValue(int(self.playersDisplayStats[4][1][3]))
        self.displaySpdTeam5Ctrl5.SetValue(int(self.playersDisplayStats[4][1][4]))
        
        self.displayDefTeam5Ctrl1.SetValue(int(self.playersDisplayStats[4][2][0]))
        self.displayDefTeam5Ctrl2.SetValue(int(self.playersDisplayStats[4][2][1]))
        self.displayDefTeam5Ctrl3.SetValue(int(self.playersDisplayStats[4][2][2]))
        self.displayDefTeam5Ctrl4.SetValue(int(self.playersDisplayStats[4][2][3]))
        self.displayDefTeam5Ctrl5.SetValue(int(self.playersDisplayStats[4][2][4]))
        
        # Team 6
        
        self.teamHexName[5], self.teamPlayerHexNames[5] = self.team6.loadteam(self.rom)
        
        self.teamName[5] = hextostr(self.teamHexName[5])
        self.teamNameCtrl6.SetValue(self.teamName[5].rstrip())
        
        self.team6Stats = self.team6.readTeamStats(self.rom)
        
        self.team6Attack = int(hexlify(self.team6Stats[0]), 16)
        self.team6Defense = int(hexlify(self.team6Stats[1]), 16)
        
        self.team6AttackSpinCtrl1.SetValue(self.team6Attack)
        self.team6DefenseSpinCtrl1.SetValue(self.team6Defense)
        
        for i in range(5):
            self.teamPlayerNames[5][i] = hextostr(self.teamPlayerHexNames[5][i])
        
        self.team6Player1Ctrl.SetValue(self.teamPlayerNames[5][0].rstrip())
        self.team6Player2Ctrl.SetValue(self.teamPlayerNames[5][1].rstrip())
        self.team6Player3Ctrl.SetValue(self.teamPlayerNames[5][2].rstrip())
        self.team6Player4Ctrl.SetValue(self.teamPlayerNames[5][3].rstrip())
        self.team6Player5Ctrl.SetValue(self.teamPlayerNames[5][4].rstrip())
        
        self.team6Player1Stats = self.team6.loadPlayerStats(self.rom, self.players6StatsOffset[0])
        
        self.sPowerSpinTeam6Ctrl1.SetValue(self.team6Player1Stats[0])
        self.mPowerSpinTeam6Ctrl1.SetValue(self.team6Player1Stats[1])
        self.speedSpinTeam6Ctrl1.SetValue(self.team6Player1Stats[2])
        self.weightSpinTeam6Ctrl1.SetValue(self.team6Player1Stats[3])
        self.angrySpinTeam6Ctrl1.SetValue(self.team6Player1Stats[5])
        
        
        self.team6Player2Stats = self.team6.loadPlayerStats(self.rom, self.players6StatsOffset[1])
        
        self.sPowerSpinTeam6Ctrl2.SetValue(self.team6Player2Stats[0])
        self.mPowerSpinTeam6Ctrl2.SetValue(self.team6Player2Stats[1])
        self.speedSpinTeam6Ctrl2.SetValue(self.team6Player2Stats[2])
        self.weightSpinTeam6Ctrl2.SetValue(self.team6Player2Stats[3])
        self.angrySpinTeam6Ctrl2.SetValue(self.team6Player2Stats[5])
        
        self.team6Player3Stats = self.team6.loadPlayerStats(self.rom, self.players6StatsOffset[2])
        
        self.sPowerSpinTeam6Ctrl3.SetValue(self.team6Player3Stats[0])
        self.mPowerSpinTeam6Ctrl3.SetValue(self.team6Player3Stats[1])
        self.speedSpinTeam6Ctrl3.SetValue(self.team6Player3Stats[2])
        self.weightSpinTeam6Ctrl3.SetValue(self.team6Player3Stats[3])
        self.angrySpinTeam6Ctrl3.SetValue(self.team6Player3Stats[5])
        
        self.team6Player4Stats = self.team6.loadPlayerStats(self.rom, self.players6StatsOffset[3])
        
        self.sPowerSpinTeam6Ctrl4.SetValue(self.team6Player4Stats[0])
        self.mPowerSpinTeam6Ctrl4.SetValue(self.team6Player4Stats[1])
        self.speedSpinTeam6Ctrl4.SetValue(self.team6Player4Stats[2])
        self.weightSpinTeam6Ctrl4.SetValue(self.team6Player4Stats[3])
        self.angrySpinTeam6Ctrl4.SetValue(self.team6Player4Stats[5])
        
        self.team6Player5Stats = self.team6.loadPlayerStats(self.rom, self.players6StatsOffset[4])
        
        self.sPowerSpinTeam6Ctrl5.SetValue(self.team6Player5Stats[0])
        self.mPowerSpinTeam6Ctrl5.SetValue(self.team6Player5Stats[1])
        self.speedSpinTeam6Ctrl5.SetValue(self.team6Player5Stats[2])
        self.weightSpinTeam6Ctrl5.SetValue(self.team6Player5Stats[3])
        self.angrySpinTeam6Ctrl5.SetValue(self.team6Player5Stats[5])
        
        self.sShootSelection[5] = self.team6.sShootRead(self.rom)
        
        self.shootTeam6Choice1.SetSelection(int(self.sShootSelection[5][0]))
        self.shootTeam6Choice2.SetSelection(int(self.sShootSelection[5][1]))
        self.shootTeam6Choice3.SetSelection(int(self.sShootSelection[5][2]))
        self.shootTeam6Choice4.SetSelection(int(self.sShootSelection[5][3]))
        self.shootTeam6Choice5.SetSelection(int(self.sShootSelection[5][4]))
        
        self.playersDisplayStats[5] = self.team6.readDisplayStats(self.rom)
        
        self.displayPowTeam6Ctrl1.SetValue(int(self.playersDisplayStats[5][0][0]))
        self.displayPowTeam6Ctrl2.SetValue(int(self.playersDisplayStats[5][0][1]))
        self.displayPowTeam6Ctrl3.SetValue(int(self.playersDisplayStats[5][0][2]))
        self.displayPowTeam6Ctrl4.SetValue(int(self.playersDisplayStats[5][0][3]))
        self.displayPowTeam6Ctrl5.SetValue(int(self.playersDisplayStats[5][0][4]))
        
        self.displaySpdTeam6Ctrl1.SetValue(int(self.playersDisplayStats[5][1][0]))
        self.displaySpdTeam6Ctrl2.SetValue(int(self.playersDisplayStats[5][1][1]))
        self.displaySpdTeam6Ctrl3.SetValue(int(self.playersDisplayStats[5][1][2]))
        self.displaySpdTeam6Ctrl4.SetValue(int(self.playersDisplayStats[5][1][3]))
        self.displaySpdTeam6Ctrl5.SetValue(int(self.playersDisplayStats[5][1][4]))
        
        self.displayDefTeam6Ctrl1.SetValue(int(self.playersDisplayStats[5][2][0]))
        self.displayDefTeam6Ctrl2.SetValue(int(self.playersDisplayStats[5][2][1]))
        self.displayDefTeam6Ctrl3.SetValue(int(self.playersDisplayStats[5][2][2]))
        self.displayDefTeam6Ctrl4.SetValue(int(self.playersDisplayStats[5][2][3]))
        self.displayDefTeam6Ctrl5.SetValue(int(self.playersDisplayStats[5][2][4]))
        
        # Team 7
        
        self.teamHexName[6], self.teamPlayerHexNames[6] = self.team7.loadteam(self.rom)
        
        self.teamName[6] = hextostr(self.teamHexName[6])
        self.teamNameCtrl7.SetValue(self.teamName[6].rstrip())
        
        self.team7Stats = self.team7.readTeamStats(self.rom)
        
        self.team7Attack = int(hexlify(self.team7Stats[0]), 16)
        self.team7Defense = int(hexlify(self.team7Stats[1]), 16)
        
        self.team7AttackSpinCtrl1.SetValue(self.team7Attack)
        self.team7DefenseSpinCtrl1.SetValue(self.team7Defense)
        
        for i in range(5):
            self.teamPlayerNames[6][i] = hextostr(self.teamPlayerHexNames[6][i])
        
        self.team7Player1Ctrl.SetValue(self.teamPlayerNames[6][0].rstrip())
        self.team7Player2Ctrl.SetValue(self.teamPlayerNames[6][1].rstrip())
        self.team7Player3Ctrl.SetValue(self.teamPlayerNames[6][2].rstrip())
        self.team7Player4Ctrl.SetValue(self.teamPlayerNames[6][3].rstrip())
        self.team7Player5Ctrl.SetValue(self.teamPlayerNames[6][4].rstrip())
        
        self.team7Player1Stats = self.team7.loadPlayerStats(self.rom, self.players7StatsOffset[0])
        
        self.sPowerSpinTeam7Ctrl1.SetValue(self.team7Player1Stats[0])
        self.mPowerSpinTeam7Ctrl1.SetValue(self.team7Player1Stats[1])
        self.speedSpinTeam7Ctrl1.SetValue(self.team7Player1Stats[2])
        self.weightSpinTeam7Ctrl1.SetValue(self.team7Player1Stats[3])
        self.angrySpinTeam7Ctrl1.SetValue(self.team7Player1Stats[5])
        
        
        self.team7Player2Stats = self.team7.loadPlayerStats(self.rom, self.players7StatsOffset[1])
        
        self.sPowerSpinTeam7Ctrl2.SetValue(self.team7Player2Stats[0])
        self.mPowerSpinTeam7Ctrl2.SetValue(self.team7Player2Stats[1])
        self.speedSpinTeam7Ctrl2.SetValue(self.team7Player2Stats[2])
        self.weightSpinTeam7Ctrl2.SetValue(self.team7Player2Stats[3])
        self.angrySpinTeam7Ctrl2.SetValue(self.team7Player2Stats[5])
        
        self.team7Player3Stats = self.team7.loadPlayerStats(self.rom, self.players7StatsOffset[2])
        
        self.sPowerSpinTeam7Ctrl3.SetValue(self.team7Player3Stats[0])
        self.mPowerSpinTeam7Ctrl3.SetValue(self.team7Player3Stats[1])
        self.speedSpinTeam7Ctrl3.SetValue(self.team7Player3Stats[2])
        self.weightSpinTeam7Ctrl3.SetValue(self.team7Player3Stats[3])
        self.angrySpinTeam7Ctrl3.SetValue(self.team7Player3Stats[5])
        
        self.team7Player4Stats = self.team7.loadPlayerStats(self.rom, self.players7StatsOffset[3])
        
        self.sPowerSpinTeam7Ctrl4.SetValue(self.team7Player4Stats[0])
        self.mPowerSpinTeam7Ctrl4.SetValue(self.team7Player4Stats[1])
        self.speedSpinTeam7Ctrl4.SetValue(self.team7Player4Stats[2])
        self.weightSpinTeam7Ctrl4.SetValue(self.team7Player4Stats[3])
        self.angrySpinTeam7Ctrl4.SetValue(self.team7Player4Stats[5])
        
        self.team7Player5Stats = self.team7.loadPlayerStats(self.rom, self.players7StatsOffset[4])
        
        self.sPowerSpinTeam7Ctrl5.SetValue(self.team7Player5Stats[0])
        self.mPowerSpinTeam7Ctrl5.SetValue(self.team7Player5Stats[1])
        self.speedSpinTeam7Ctrl5.SetValue(self.team7Player5Stats[2])
        self.weightSpinTeam7Ctrl5.SetValue(self.team7Player5Stats[3])
        self.angrySpinTeam7Ctrl5.SetValue(self.team7Player5Stats[5])
        
        self.sShootSelection[6] = self.team7.sShootRead(self.rom)
        
        self.shootTeam7Choice1.SetSelection(int(self.sShootSelection[6][0]))
        self.shootTeam7Choice2.SetSelection(int(self.sShootSelection[6][1]))
        self.shootTeam7Choice3.SetSelection(int(self.sShootSelection[6][2]))
        self.shootTeam7Choice4.SetSelection(int(self.sShootSelection[6][3]))
        self.shootTeam7Choice5.SetSelection(int(self.sShootSelection[6][4]))
        
        self.playersDisplayStats[6] = self.team7.readDisplayStats(self.rom)
        
        self.displayPowTeam7Ctrl1.SetValue(int(self.playersDisplayStats[6][0][0]))
        self.displayPowTeam7Ctrl2.SetValue(int(self.playersDisplayStats[6][0][1]))
        self.displayPowTeam7Ctrl3.SetValue(int(self.playersDisplayStats[6][0][2]))
        self.displayPowTeam7Ctrl4.SetValue(int(self.playersDisplayStats[6][0][3]))
        self.displayPowTeam7Ctrl5.SetValue(int(self.playersDisplayStats[6][0][4]))
        
        self.displaySpdTeam7Ctrl1.SetValue(int(self.playersDisplayStats[6][1][0]))
        self.displaySpdTeam7Ctrl2.SetValue(int(self.playersDisplayStats[6][1][1]))
        self.displaySpdTeam7Ctrl3.SetValue(int(self.playersDisplayStats[6][1][2]))
        self.displaySpdTeam7Ctrl4.SetValue(int(self.playersDisplayStats[6][1][3]))
        self.displaySpdTeam7Ctrl5.SetValue(int(self.playersDisplayStats[6][1][4]))
        
        self.displayDefTeam7Ctrl1.SetValue(int(self.playersDisplayStats[6][2][0]))
        self.displayDefTeam7Ctrl2.SetValue(int(self.playersDisplayStats[6][2][1]))
        self.displayDefTeam7Ctrl3.SetValue(int(self.playersDisplayStats[6][2][2]))
        self.displayDefTeam7Ctrl4.SetValue(int(self.playersDisplayStats[6][2][3]))
        self.displayDefTeam7Ctrl5.SetValue(int(self.playersDisplayStats[6][2][4]))
        
        # Team 8
        
        self.teamHexName[7], self.teamPlayerHexNames[7] = self.team8.loadteam(self.rom)
        
        self.teamName[7] = hextostr(self.teamHexName[7])
        self.teamNameCtrl8.SetValue(self.teamName[7].rstrip())
        
        self.team8Stats = self.team8.readTeamStats(self.rom)
        
        self.team8Attack = int(hexlify(self.team8Stats[0]), 16)
        self.team8Defense = int(hexlify(self.team8Stats[1]), 16)
        
        self.team8AttackSpinCtrl1.SetValue(self.team8Attack)
        self.team8DefenseSpinCtrl1.SetValue(self.team8Defense)
        
        for i in range(5):
            self.teamPlayerNames[7][i] = hextostr(self.teamPlayerHexNames[7][i])
        
        self.team8Player1Ctrl.SetValue(self.teamPlayerNames[7][0].rstrip())
        self.team8Player2Ctrl.SetValue(self.teamPlayerNames[7][1].rstrip())
        self.team8Player3Ctrl.SetValue(self.teamPlayerNames[7][2].rstrip())
        self.team8Player4Ctrl.SetValue(self.teamPlayerNames[7][3].rstrip())
        self.team8Player5Ctrl.SetValue(self.teamPlayerNames[7][4].rstrip())
        
        self.team8Player1Stats = self.team8.loadPlayerStats(self.rom, self.players8StatsOffset[0])
        
        self.sPowerSpinTeam8Ctrl1.SetValue(self.team8Player1Stats[0])
        self.mPowerSpinTeam8Ctrl1.SetValue(self.team8Player1Stats[1])
        self.speedSpinTeam8Ctrl1.SetValue(self.team8Player1Stats[2])
        self.weightSpinTeam8Ctrl1.SetValue(self.team8Player1Stats[3])
        self.angrySpinTeam8Ctrl1.SetValue(self.team8Player1Stats[5])
        
        
        self.team8Player2Stats = self.team8.loadPlayerStats(self.rom, self.players8StatsOffset[1])
        
        self.sPowerSpinTeam8Ctrl2.SetValue(self.team8Player2Stats[0])
        self.mPowerSpinTeam8Ctrl2.SetValue(self.team8Player2Stats[1])
        self.speedSpinTeam8Ctrl2.SetValue(self.team8Player2Stats[2])
        self.weightSpinTeam8Ctrl2.SetValue(self.team8Player2Stats[3])
        self.angrySpinTeam8Ctrl2.SetValue(self.team8Player2Stats[5])
        
        self.team8Player3Stats = self.team8.loadPlayerStats(self.rom, self.players8StatsOffset[2])
        
        self.sPowerSpinTeam8Ctrl3.SetValue(self.team8Player3Stats[0])
        self.mPowerSpinTeam8Ctrl3.SetValue(self.team8Player3Stats[1])
        self.speedSpinTeam8Ctrl3.SetValue(self.team8Player3Stats[2])
        self.weightSpinTeam8Ctrl3.SetValue(self.team8Player3Stats[3])
        self.angrySpinTeam8Ctrl3.SetValue(self.team8Player3Stats[5])
        
        self.team8Player4Stats = self.team8.loadPlayerStats(self.rom, self.players8StatsOffset[3])
        
        self.sPowerSpinTeam8Ctrl4.SetValue(self.team8Player4Stats[0])
        self.mPowerSpinTeam8Ctrl4.SetValue(self.team8Player4Stats[1])
        self.speedSpinTeam8Ctrl4.SetValue(self.team8Player4Stats[2])
        self.weightSpinTeam8Ctrl4.SetValue(self.team8Player4Stats[3])
        self.angrySpinTeam8Ctrl4.SetValue(self.team8Player4Stats[5])
        
        self.team8Player5Stats = self.team8.loadPlayerStats(self.rom, self.players8StatsOffset[4])
        
        self.sPowerSpinTeam8Ctrl5.SetValue(self.team8Player5Stats[0])
        self.mPowerSpinTeam8Ctrl5.SetValue(self.team8Player5Stats[1])
        self.speedSpinTeam8Ctrl5.SetValue(self.team8Player5Stats[2])
        self.weightSpinTeam8Ctrl5.SetValue(self.team8Player5Stats[3])
        self.angrySpinTeam8Ctrl5.SetValue(self.team8Player5Stats[5])
        
        self.sShootSelection[7] = self.team8.sShootRead(self.rom)
        
        self.shootTeam8Choice1.SetSelection(int(self.sShootSelection[7][0]))
        self.shootTeam8Choice2.SetSelection(int(self.sShootSelection[7][1]))
        self.shootTeam8Choice3.SetSelection(int(self.sShootSelection[7][2]))
        self.shootTeam8Choice4.SetSelection(int(self.sShootSelection[7][3]))
        self.shootTeam8Choice5.SetSelection(int(self.sShootSelection[7][4]))
        
        self.playersDisplayStats[7] = self.team8.readDisplayStats(self.rom)
        
        self.displayPowTeam8Ctrl1.SetValue(int(self.playersDisplayStats[7][0][0]))
        self.displayPowTeam8Ctrl2.SetValue(int(self.playersDisplayStats[7][0][1]))
        self.displayPowTeam8Ctrl3.SetValue(int(self.playersDisplayStats[7][0][2]))
        self.displayPowTeam8Ctrl4.SetValue(int(self.playersDisplayStats[7][0][3]))
        self.displayPowTeam8Ctrl5.SetValue(int(self.playersDisplayStats[7][0][4]))
        
        self.displaySpdTeam8Ctrl1.SetValue(int(self.playersDisplayStats[7][1][0]))
        self.displaySpdTeam8Ctrl2.SetValue(int(self.playersDisplayStats[7][1][1]))
        self.displaySpdTeam8Ctrl3.SetValue(int(self.playersDisplayStats[7][1][2]))
        self.displaySpdTeam8Ctrl4.SetValue(int(self.playersDisplayStats[7][1][3]))
        self.displaySpdTeam8Ctrl5.SetValue(int(self.playersDisplayStats[7][1][4]))
        
        self.displayDefTeam8Ctrl1.SetValue(int(self.playersDisplayStats[7][2][0]))
        self.displayDefTeam8Ctrl2.SetValue(int(self.playersDisplayStats[7][2][1]))
        self.displayDefTeam8Ctrl3.SetValue(int(self.playersDisplayStats[7][2][2]))
        self.displayDefTeam8Ctrl4.SetValue(int(self.playersDisplayStats[7][2][3]))
        self.displayDefTeam8Ctrl5.SetValue(int(self.playersDisplayStats[7][2][4]))
        
        closefile(self.rom)
    
    def saveRom(self):
        
        # General Game Settings
                        
        savetime(self.rom, self.minutes, self.seconds)
        savecharge(self.rom, self.superShoot)
        savemusic(self.rom, self.music)
        savenopenalty(self.rom, self.noPenalty)
        saveFallType(self.rom, self.fallType)
        saveFlyHit(self.rom, self.flyTypeOnHit)
        saveFlyShoot(self.rom, self.flyTypeOnShoot)

        # Team Settings
        
        self.team1.saveteam(self.rom, self.teamHexName[0], self.teamPlayerHexNames[0])
        self.team2.saveteam(self.rom, self.teamHexName[1], self.teamPlayerHexNames[1])
        self.team3.saveteam(self.rom, self.teamHexName[2], self.teamPlayerHexNames[2])
        self.team4.saveteam(self.rom, self.teamHexName[3], self.teamPlayerHexNames[3])
        self.team5.saveteam(self.rom, self.teamHexName[4], self.teamPlayerHexNames[4])
        self.team6.saveteam(self.rom, self.teamHexName[5], self.teamPlayerHexNames[5])
        self.team7.saveteam(self.rom, self.teamHexName[6], self.teamPlayerHexNames[6])
        self.team8.saveteam(self.rom, self.teamHexName[7], self.teamPlayerHexNames[7])
        
        self.team1.writeTeamStats(self.rom, self.team1Attack, self.team1Defense)
        self.team2.writeTeamStats(self.rom, self.team2Attack, self.team2Defense)
        self.team3.writeTeamStats(self.rom, self.team3Attack, self.team3Defense)
        self.team4.writeTeamStats(self.rom, self.team4Attack, self.team4Defense)
        self.team5.writeTeamStats(self.rom, self.team5Attack, self.team5Defense)
        self.team6.writeTeamStats(self.rom, self.team6Attack, self.team6Defense)
        self.team7.writeTeamStats(self.rom, self.team7Attack, self.team7Defense)
        self.team8.writeTeamStats(self.rom, self.team8Attack, self.team8Defense)
        
        self.team1.writePlayerStats(self.rom, self.players1StatsOffset, (self.team1Player1Stats, self.team1Player2Stats, self.team1Player3Stats, self.team1Player4Stats, self.team1Player5Stats))
        self.team2.writePlayerStats(self.rom, self.players2StatsOffset, (self.team2Player1Stats, self.team2Player2Stats, self.team2Player3Stats, self.team2Player4Stats, self.team2Player5Stats))
        self.team3.writePlayerStats(self.rom, self.players3StatsOffset, (self.team3Player1Stats, self.team3Player2Stats, self.team3Player3Stats, self.team3Player4Stats, self.team3Player5Stats))
        self.team4.writePlayerStats(self.rom, self.players4StatsOffset, (self.team4Player1Stats, self.team4Player2Stats, self.team4Player3Stats, self.team4Player4Stats, self.team4Player5Stats))
        self.team5.writePlayerStats(self.rom, self.players5StatsOffset, (self.team5Player1Stats, self.team5Player2Stats, self.team5Player3Stats, self.team5Player4Stats, self.team5Player5Stats))
        self.team6.writePlayerStats(self.rom, self.players6StatsOffset, (self.team6Player1Stats, self.team6Player2Stats, self.team6Player3Stats, self.team6Player4Stats, self.team6Player5Stats))
        self.team7.writePlayerStats(self.rom, self.players7StatsOffset, (self.team7Player1Stats, self.team7Player2Stats, self.team7Player3Stats, self.team7Player4Stats, self.team7Player5Stats))
        self.team8.writePlayerStats(self.rom, self.players8StatsOffset, (self.team8Player1Stats, self.team8Player2Stats, self.team8Player3Stats, self.team8Player4Stats, self.team8Player5Stats))
        
        self.team1.sShootWrite(self.rom, self.sShootSelection[0])
        self.team2.sShootWrite(self.rom, self.sShootSelection[1])
        self.team3.sShootWrite(self.rom, self.sShootSelection[2])
        self.team4.sShootWrite(self.rom, self.sShootSelection[3])
        self.team5.sShootWrite(self.rom, self.sShootSelection[4])
        self.team6.sShootWrite(self.rom, self.sShootSelection[5])
        self.team7.sShootWrite(self.rom, self.sShootSelection[6])
        self.team8.sShootWrite(self.rom, self.sShootSelection[7])
        
        self.team1.writeDisplayStats(self.rom, self.playersDisplayStats[0])
        self.team2.writeDisplayStats(self.rom, self.playersDisplayStats[1])   
        self.team3.writeDisplayStats(self.rom, self.playersDisplayStats[2]) 
        self.team4.writeDisplayStats(self.rom, self.playersDisplayStats[3])      
        self.team5.writeDisplayStats(self.rom, self.playersDisplayStats[4])  
        self.team6.writeDisplayStats(self.rom, self.playersDisplayStats[5])  
        self.team7.writeDisplayStats(self.rom, self.playersDisplayStats[6])  
        self.team8.writeDisplayStats(self.rom, self.playersDisplayStats[7])
        
        closefile(self.rom)
        
        ok_dlg = wx.MessageDialog (self, u'Completed!!',
            u'Completed',
            wx.OK | wx.ICON_INFORMATION
        )
        ok_dlg.ShowModal ()
        ok_dlg.Destroy () 
        
        
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

    def OnMinCtrl1Text(self, event):
        event.Skip()
        self.minutes = self.minCtrl1.GetValue()

    def OnSecCtrl1Text(self, event):
        event.Skip()
        self.seconds = self.secCtrl1.GetValue()

    def OnShootCtrl1Text(self, event):
        event.Skip()
        self.superShoot = self.shootCtrl1.GetValue()

    def OnChoice1Choice(self, event):
        event.Skip()
        self.music[0] = self.choice1.GetSelection()
        
    def OnChoice2Choice(self, event):
        event.Skip()
        self.music[1] = self.choice2.GetSelection()
        
    def OnChoice3Choice(self, event):
        event.Skip()
        self.music[2] = self.choice3.GetSelection()
        
    def OnChoice4Choice(self, event):
        event.Skip()
        self.music[3] = self.choice4.GetSelection()
        
    def OnChoice5Choice(self, event):
        event.Skip()
        self.music[4] = self.choice4.GetSelection()

    def OnCheckBox1Checkbox(self, event):
        event.Skip()
        self.noPenalty = self.checkBox1.GetValue()

    def OnFallTypeChoiceChoice(self, event):
        event.Skip()
        self.fallType = self.fallTypeChoice.GetSelection()

    def OnFlyHitSpinCtrlText(self, event):
        event.Skip()
        self.flyTypeOnHit = self.flyHitSpinCtrl.GetValue()

    def OnFlyShootSpinCtrlText(self, event):
        event.Skip()
        self.flyTypeOnShoot = self.flyShootSpinCtrl.GetValue()
        
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

    def OnButton1Button(self, event):
        event.Skip()
        dlg = wx.FileDialog(self, 'Open Ike Ike Hockey ROM', '.', '', '*.nes', wx.OPEN)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                filename = dlg.GetPath()
                
                self.rom = loadfile(filename, "read")
                
                self.loadRom()
                
        finally:
            dlg.Destroy()
            self.button2.Enable(True)

#-------------------------------------------------------------------------------

    def OnButton2Button(self, event):
        event.Skip()
        dlg = wx.FileDialog(self, 'Save Ike Ike Hockey ROM', '.', '', '*.nes', wx.SAVE)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                filename = dlg.GetPath()
                
                self.rom = loadfile(filename, "write")

                self.saveRom()
                
        finally:
            dlg.Destroy()

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

    def OnTeamNameCtrl1Text(self, event):
        event.Skip()
        self.teamName[0] = self.teamNameCtrl1.GetValue()
        self.teamHexName[0] = strtohex("{0: <8}".format(self.teamName[0]))

    def OnTeam1Player1CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[0][0] = self.team1Player1Ctrl.GetValue()
        self.teamPlayerHexNames[0][0] = strtohex("{0: <4}".format(self.teamPlayerNames[0][0]))

    def OnTeam1Player2CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[0][1] = self.team1Player2Ctrl.GetValue()
        self.teamPlayerHexNames[0][1] = strtohex("{0: <4}".format(self.teamPlayerNames[0][1]))

    def OnTeam1Player3CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[0][2] = self.team1Player3Ctrl.GetValue()
        self.teamPlayerHexNames[0][2] = strtohex("{0: <4}".format(self.teamPlayerNames[0][2]))

    def OnTeam1Player4CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[0][3] = self.team1Player4Ctrl.GetValue()
        self.teamPlayerHexNames[0][3] = strtohex("{0: <4}".format(self.teamPlayerNames[0][3]))

    def OnTeam1Player5CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[0][4] = self.team1Player5Ctrl.GetValue()
        self.teamPlayerHexNames[0][4] = strtohex("{0: <4}".format(self.teamPlayerNames[0][4]))

#-------------------------------------------------------------------------------

    def OnTeamNameCtrl2Text(self, event):
        event.Skip()
        self.teamName[1] = self.teamNameCtrl2.GetValue()
        self.teamHexName[1] = strtohex("{0: <8}".format(self.teamName[1]))

    def OnTeam2Player1CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[1][0] = self.team2Player1Ctrl.GetValue()
        self.teamPlayerHexNames[1][0] = strtohex("{0: <4}".format(self.teamPlayerNames[1][0]))

    def OnTeam2Player2CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[1][1] = self.team2Player2Ctrl.GetValue()
        self.teamPlayerHexNames[1][1] = strtohex("{0: <4}".format(self.teamPlayerNames[1][1]))

    def OnTeam2Player3CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[1][2] = self.team2Player3Ctrl.GetValue()
        self.teamPlayerHexNames[1][2] = strtohex("{0: <4}".format(self.teamPlayerNames[1][2]))

    def OnTeam2Player4CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[1][3] = self.team2Player4Ctrl.GetValue()
        self.teamPlayerHexNames[1][3] = strtohex("{0: <4}".format(self.teamPlayerNames[1][3]))

    def OnTeam2Player5CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[1][4] = self.team2Player5Ctrl.GetValue()
        self.teamPlayerHexNames[1][4] = strtohex("{0: <4}".format(self.teamPlayerNames[1][4]))

#-------------------------------------------------------------------------------

    def OnTeamNameCtrl3Text(self, event):
        event.Skip()
        self.teamName[2] = self.teamNameCtrl3.GetValue()
        self.teamHexName[2] = strtohex("{0: <8}".format(self.teamName[2]))

    def OnTeam3Player1CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[2][0] = self.team3Player1Ctrl.GetValue()
        self.teamPlayerHexNames[2][0] = strtohex("{0: <4}".format(self.teamPlayerNames[2][0]))

    def OnTeam3Player2CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[2][1] = self.team3Player2Ctrl.GetValue()
        self.teamPlayerHexNames[2][1] = strtohex("{0: <4}".format(self.teamPlayerNames[2][1]))

    def OnTeam3Player3CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[2][2] = self.team3Player3Ctrl.GetValue()
        self.teamPlayerHexNames[2][2] = strtohex("{0: <4}".format(self.teamPlayerNames[2][2]))

    def OnTeam3Player4CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[2][3] = self.team3Player4Ctrl.GetValue()
        self.teamPlayerHexNames[2][3] = strtohex("{0: <4}".format(self.teamPlayerNames[2][3]))

    def OnTeam3Player5CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[2][4] = self.team3Player5Ctrl.GetValue()
        self.teamPlayerHexNames[2][4] = strtohex("{0: <4}".format(self.teamPlayerNames[2][4]))

#-------------------------------------------------------------------------------

    def OnTeamNameCtrl4Text(self, event):
        event.Skip()
        self.teamName[3] = self.teamNameCtrl4.GetValue()
        self.teamHexName[3] = strtohex("{0: <8}".format(self.teamName[3]))

    def OnTeam4Player1CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[3][0] = self.team4Player1Ctrl.GetValue()
        self.teamPlayerHexNames[3][0] = strtohex("{0: <4}".format(self.teamPlayerNames[3][0]))

    def OnTeam4Player2CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[3][1] = self.team4Player2Ctrl.GetValue()
        self.teamPlayerHexNames[3][1] = strtohex("{0: <4}".format(self.teamPlayerNames[3][1]))

    def OnTeam4Player3CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[3][2] = self.team4Player3Ctrl.GetValue()
        self.teamPlayerHexNames[3][2] = strtohex("{0: <4}".format(self.teamPlayerNames[3][2]))

    def OnTeam4Player4CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[3][3] = self.team4Player4Ctrl.GetValue()
        self.teamPlayerHexNames[3][3] = strtohex("{0: <4}".format(self.teamPlayerNames[3][3]))

    def OnTeam4Player5CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[3][4] = self.team4Player5Ctrl.GetValue()
        self.teamPlayerHexNames[3][4] = strtohex("{0: <4}".format(self.teamPlayerNames[3][4]))

#-------------------------------------------------------------------------------

    def OnTeamNameCtrl5Text(self, event):
        event.Skip()
        self.teamName[4] = self.teamNameCtrl5.GetValue()
        self.teamHexName[4] = strtohex("{0: <8}".format(self.teamName[4]))
    
    def OnTeam5Player1CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[4][0] = self.team5Player1Ctrl.GetValue()
        self.teamPlayerHexNames[4][0] = strtohex("{0: <4}".format(self.teamPlayerNames[4][0]))

    def OnTeam5Player2CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[4][1] = self.team5Player2Ctrl.GetValue()
        self.teamPlayerHexNames[4][1] = strtohex("{0: <4}".format(self.teamPlayerNames[4][1]))

    def OnTeam5Player3CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[4][2] = self.team5Player3Ctrl.GetValue()
        self.teamPlayerHexNames[4][2] = strtohex("{0: <4}".format(self.teamPlayerNames[4][2]))

    def OnTeam5Player4CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[4][3] = self.team5Player4Ctrl.GetValue()
        self.teamPlayerHexNames[4][3] = strtohex("{0: <4}".format(self.teamPlayerNames[4][3]))

    def OnTeam5Player5CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[4][4] = self.team5Player5Ctrl.GetValue()
        self.teamPlayerHexNames[4][4] = strtohex("{0: <4}".format(self.teamPlayerNames[4][4]))

#-------------------------------------------------------------------------------

    def OnTeamNameCtrl6Text(self, event):
        event.Skip()
        self.teamName[5] = self.teamNameCtrl6.GetValue()
        self.teamHexName[5] = strtohex("{0: <8}".format(self.teamName[5]))

    def OnTeam6Player1CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[5][0] = self.team6Player1Ctrl.GetValue()
        self.teamPlayerHexNames[5][0] = strtohex("{0: <4}".format(self.teamPlayerNames[5][0]))

    def OnTeam6Player2CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[5][1] = self.team6Player2Ctrl.GetValue()
        self.teamPlayerHexNames[5][1] = strtohex("{0: <4}".format(self.teamPlayerNames[5][1]))

    def OnTeam6Player3CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[5][2] = self.team6Player3Ctrl.GetValue()
        self.teamPlayerHexNames[5][2] = strtohex("{0: <4}".format(self.teamPlayerNames[5][2]))

    def OnTeam6Player4CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[5][3] = self.team6Player4Ctrl.GetValue()
        self.teamPlayerHexNames[5][3] = strtohex("{0: <4}".format(self.teamPlayerNames[5][3]))

    def OnTeam6Player5CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[5][4] = self.team6Player5Ctrl.GetValue()
        self.teamPlayerHexNames[5][4] = strtohex("{0: <4}".format(self.teamPlayerNames[5][4]))
        
#-------------------------------------------------------------------------------

    def OnTeamNameCtrl7Text(self, event):
        event.Skip()
        self.teamName[6] = self.teamNameCtrl7.GetValue()
        self.teamHexName[6] = strtohex("{0: <8}".format(self.teamName[6]))
        
    def OnTeam7Player1CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[6][0] = self.team7Player1Ctrl.GetValue()
        self.teamPlayerHexNames[6][0] = strtohex("{0: <4}".format(self.teamPlayerNames[6][0]))

    def OnTeam7Player2CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[6][1] = self.team7Player2Ctrl.GetValue()
        self.teamPlayerHexNames[6][1] = strtohex("{0: <4}".format(self.teamPlayerNames[6][1]))

    def OnTeam7Player3CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[6][2] = self.team7Player3Ctrl.GetValue()
        self.teamPlayerHexNames[6][2] = strtohex("{0: <4}".format(self.teamPlayerNames[6][2]))

    def OnTeam7Player4CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[6][3] = self.team7Player4Ctrl.GetValue()
        self.teamPlayerHexNames[6][3] = strtohex("{0: <4}".format(self.teamPlayerNames[6][3]))

    def OnTeam7Player5CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[6][4] = self.team7Player5Ctrl.GetValue()
        self.teamPlayerHexNames[6][4] = strtohex("{0: <4}".format(self.teamPlayerNames[6][4]))
        
#-------------------------------------------------------------------------------

    def OnTeamNameCtrl8Text(self, event):
        event.Skip()
        self.teamName[7] = self.teamNameCtrl8.GetValue()
        self.teamHexName[7] = strtohex("{0: <8}".format(self.teamName[7]))

    def OnTeam8Player1CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[7][0] = self.team8Player1Ctrl.GetValue()
        self.teamPlayerHexNames[7][0] = strtohex("{0: <4}".format(self.teamPlayerNames[7][0]))

    def OnTeam8Player2CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[7][1] = self.team8Player2Ctrl.GetValue()
        self.teamPlayerHexNames[7][1] = strtohex("{0: <4}".format(self.teamPlayerNames[7][1]))

    def OnTeam8Player3CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[7][2] = self.team8Player3Ctrl.GetValue()
        self.teamPlayerHexNames[7][2] = strtohex("{0: <4}".format(self.teamPlayerNames[7][2]))

    def OnTeam8Player4CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[7][3] = self.team8Player4Ctrl.GetValue()
        self.teamPlayerHexNames[7][3] = strtohex("{0: <4}".format(self.teamPlayerNames[7][3]))

    def OnTeam8Player5CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[7][4] = self.team8Player5Ctrl.GetValue()
        self.teamPlayerHexNames[7][4] = strtohex("{0: <4}".format(self.teamPlayerNames[7][4]))

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

    def OnShootTeam1Choice1Choice(self, event):
        event.Skip()
        self.sShootSelection[0][0] = self.shootTeam1Choice1.GetSelection()

    def OnShootTeam1Choice2Choice(self, event):
        event.Skip()
        self.sShootSelection[0][1] = self.shootTeam1Choice1.GetSelection()

    def OnShootTeam1Choice3Choice(self, event):
        event.Skip()
        self.sShootSelection[0][2] = self.shootTeam1Choice1.GetSelection()

    def OnShootTeam1Choice4Choice(self, event):
        event.Skip()
        self.sShootSelection[0][3] = self.shootTeam1Choice1.GetSelection()

    def OnShootTeam1Choice5Choice(self, event):
        event.Skip()
        self.sShootSelection[0][4] = self.shootTeam1Choice1.GetSelection()
        
#-------------------------------------------------------------------------------
        
    def OnShootTeam2Choice1Choice(self, event):
        event.Skip()
        self.sShootSelection[1][0] = self.shootTeam2Choice1.GetSelection()

    def OnShootTeam2Choice2Choice(self, event):
        event.Skip()
        self.sShootSelection[1][1] = self.shootTeam2Choice1.GetSelection()

    def OnShootTeam2Choice3Choice(self, event):
        event.Skip()
        self.sShootSelection[1][2] = self.shootTeam2Choice1.GetSelection()

    def OnShootTeam2Choice4Choice(self, event):
        event.Skip()
        self.sShootSelection[1][3] = self.shootTeam2Choice1.GetSelection()
        
    def OnShootTeam2Choice5Choice(self, event):
        event.Skip()
        self.sShootSelection[1][4] = self.shootTeam2Choice1.GetSelection()
        
#-------------------------------------------------------------------------------
        
    def OnShootTeam3Choice1Choice(self, event):
        event.Skip()
        self.sShootSelection[2][0] = self.shootTeam3Choice1.GetSelection()

    def OnShootTeam3Choice2Choice(self, event):
        event.Skip()
        self.sShootSelection[2][1] = self.shootTeam3Choice1.GetSelection()

    def OnShootTeam3Choice3Choice(self, event):
        event.Skip()
        self.sShootSelection[2][2] = self.shootTeam3Choice1.GetSelection()

    def OnShootTeam3Choice4Choice(self, event):
        event.Skip()
        self.sShootSelection[2][3] = self.shootTeam3Choice1.GetSelection()

    def OnShootTeam3Choice5Choice(self, event):
        event.Skip()
        self.sShootSelection[2][4] = self.shootTeam3Choice1.GetSelection()

#-------------------------------------------------------------------------------
    def OnShootTeam4Choice1Choice(self, event):
        event.Skip()
        self.sShootSelection[3][0] = self.shootTeam4Choice1.GetSelection()

    def OnShootTeam4Choice2Choice(self, event):
        event.Skip()
        self.sShootSelection[3][1] = self.shootTeam4Choice1.GetSelection()

    def OnShootTeam4Choice3Choice(self, event):
        event.Skip()
        self.sShootSelection[3][2] = self.shootTeam4Choice1.GetSelection()

    def OnShootTeam4Choice4Choice(self, event):
        event.Skip()
        self.sShootSelection[3][3] = self.shootTeam4Choice1.GetSelection()

    def OnShootTeam4Choice5Choice(self, event):
        event.Skip()
        self.sShootSelection[3][4] = self.shootTeam4Choice1.GetSelection()
        
#-------------------------------------------------------------------------------

    def OnShootTeam5Choice1Choice(self, event):
        event.Skip()
        self.sShootSelection[4][0] = self.shootTeam5Choice1.GetSelection()

    def OnShootTeam5Choice2Choice(self, event):
        event.Skip()
        self.sShootSelection[4][1] = self.shootTeam5Choice1.GetSelection()

    def OnShootTeam5Choice3Choice(self, event):
        event.Skip()
        self.sShootSelection[4][2] = self.shootTeam5Choice1.GetSelection()

    def OnShootTeam5Choice4Choice(self, event):
        event.Skip()
        self.sShootSelection[4][3] = self.shootTeam5Choice1.GetSelection()

    def OnShootTeam5Choice5Choice(self, event):
        event.Skip()
        self.sShootSelection[4][4] = self.shootTeam5Choice1.GetSelection()

#-------------------------------------------------------------------------------

    def OnShootTeam6Choice1Choice(self, event):
        event.Skip()
        self.sShootSelection[5][0] = self.shootTeam6Choice1.GetSelection()

    def OnShootTeam6Choice2Choice(self, event):
        event.Skip()
        self.sShootSelection[5][1] = self.shootTeam6Choice1.GetSelection()

    def OnShootTeam6Choice3Choice(self, event):
        event.Skip()
        self.sShootSelection[5][2] = self.shootTeam6Choice1.GetSelection()

    def OnShootTeam6Choice4Choice(self, event):
        event.Skip()
        self.sShootSelection[5][3] = self.shootTeam6Choice1.GetSelection()

    def OnShootTeam6Choice5Choice(self, event):
        event.Skip()
        self.sShootSelection[5][4] = self.shootTeam6Choice1.GetSelection()

#-------------------------------------------------------------------------------

    def OnShootTeam7Choice1Choice(self, event):
        event.Skip()
        self.sShootSelection[6][0] = self.shootTeam7Choice1.GetSelection()

    def OnShootTeam7Choice2Choice(self, event):
        event.Skip()
        self.sShootSelection[6][1] = self.shootTeam7Choice1.GetSelection()

    def OnShootTeam7Choice3Choice(self, event):
        event.Skip()
        self.sShootSelection[6][2] = self.shootTeam7Choice1.GetSelection()

    def OnShootTeam7Choice4Choice(self, event):
        event.Skip()
        self.sShootSelection[6][3] = self.shootTeam7Choice1.GetSelection()

    def OnShootTeam7Choice5Choice(self, event):
        event.Skip()
        self.sShootSelection[6][4] = self.shootTeam7Choice1.GetSelection()

#-------------------------------------------------------------------------------

    def OnShootTeam8Choice1Choice(self, event):
        event.Skip()
        self.sShootSelection[7][0] = self.shootTeam8Choice1.GetSelection()

    def OnShootTeam8Choice2Choice(self, event):
        event.Skip()
        self.sShootSelection[7][1] = self.shootTeam8Choice1.GetSelection()

    def OnShootTeam8Choice3Choice(self, event):
        event.Skip()
        self.sShootSelection[7][2] = self.shootTeam8Choice1.GetSelection()

    def OnShootTeam8Choice4Choice(self, event):
        event.Skip()
        self.sShootSelection[7][3] = self.shootTeam8Choice1.GetSelection()

    def OnShootTeam8Choice5Choice(self, event):
        event.Skip()
        self.sShootSelection[7][4] = self.shootTeam8Choice1.GetSelection()

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

    def OnSPowerSpinTeam1Ctrl1Text(self, event):
        event.Skip()
        self.team1Player1Stats[0] = self.sPowerSpinTeam1Ctrl1.GetValue()

    def OnSPowerSpinTeam1Ctrl2Text(self, event):
        event.Skip()
        self.team1Player2Stats[0] = self.sPowerSpinTeam1Ctrl2.GetValue()

    def OnSPowerSpinTeam1Ctrl3Text(self, event):
        event.Skip()
        self.team1Player3Stats[0] = self.sPowerSpinTeam1Ctrl3.GetValue()

    def OnSPowerSpinTeam1Ctrl4Text(self, event):
        event.Skip()
        self.team1Player4Stats[0] = self.sPowerSpinTeam1Ctrl4.GetValue()

    def OnSPowerSpinTeam1Ctrl5Text(self, event):
        event.Skip()
        self.team1Player5Stats[0] = self.sPowerSpinTeam1Ctrl5.GetValue()
        
#-------------------------------------------------------------------------------

    def OnMPowerSpinTeam1Ctrl1Text(self, event):
        event.Skip()
        self.team1Player1Stats[1] = self.mPowerSpinTeam1Ctrl1.GetValue()
 
    def OnMPowerSpinTeam1Ctrl2Text(self, event):
        event.Skip()
        self.team1Player2Stats[1] = self.mPowerSpinTeam1Ctrl2.GetValue()
        
    def OnMPowerSpinTeam1Ctrl3Text(self, event):
        event.Skip()
        self.team1Player3Stats[1] = self.mPowerSpinTeam1Ctrl3.GetValue()

    def OnMPowerSpinTeam1Ctrl4Text(self, event):
        event.Skip()
        self.team1Player4Stats[1] = self.mPowerSpinTeam1Ctrl4.GetValue()

    def OnMPowerSpinTeam1Ctrl5Text(self, event):
        event.Skip()  
        self.team1Player5Stats[1] = self.mPowerSpinTeam1Ctrl5.GetValue()

#-------------------------------------------------------------------------------

    def OnSpeedSpinTeam1Ctrl1Text(self, event):
        event.Skip()
        self.team1Player1Stats[2] = self.speedSpinTeam1Ctrl1.GetValue()

    def OnSpeedSpinTeam1Ctrl2Text(self, event):
        event.Skip()
        self.team1Player2Stats[2] = self.speedSpinTeam1Ctrl2.GetValue()

    def OnSpeedSpinTeam1Ctrl3Text(self, event):
        event.Skip()
        self.team1Player3Stats[2] = self.speedSpinTeam1Ctrl3.GetValue()

    def OnSpeedSpinTeam1Ctrl4Text(self, event):
        event.Skip()
        self.team1Player4Stats[2] = self.speedSpinTeam1Ctrl4.GetValue()

    def OnSpeedSpinTeam1Ctrl5Text(self, event):
        event.Skip()
        self.team1Player5Stats[2] = self.speedSpinTeam1Ctrl5.GetValue()

#-------------------------------------------------------------------------------
          
    def OnWeightSpinTeam1Ctrl1Text(self, event):
        event.Skip()
        self.team1Player1Stats[3] = self.weightSpinTeam1Ctrl1.GetValue()
        
    def OnWeightSpinTeam1Ctrl2Text(self, event):
        event.Skip()
        self.team1Player2Stats[3] = self.weightSpinTeam1Ctrl2.GetValue()

    def OnWeightSpinTeam1Ctrl3Text(self, event):
        event.Skip()
        self.team1Player3Stats[3] = self.weightSpinTeam1Ctrl3.GetValue()
        
    def OnWeightSpinTeam1Ctrl4Text(self, event):
        event.Skip()
        self.team1Player4Stats[3] = self.weightSpinTeam1Ctrl4.GetValue()

    def OnWeightSpinTeam1Ctrl5Text(self, event):
        event.Skip()
        self.team1Player5Stats[3] = self.weightSpinTeam1Ctrl5.GetValue()

#-------------------------------------------------------------------------------

    def OnAngrySpinTeam1Ctrl1Text(self, event):
        event.Skip()
        self.team1Player1Stats[5] = self.angrySpinTeam1Ctrl1.GetValue()

    def OnAngrySpinTeam1Ctrl2Text(self, event):
        event.Skip()
        self.team1Player2Stats[5] = self.angrySpinTeam1Ctrl2.GetValue()

    def OnAngrySpinTeam1Ctrl3Text(self, event):
        event.Skip()
        self.team1Player3Stats[5] = self.angrySpinTeam1Ctrl3.GetValue()

    def OnAngrySpinTeam1Ctrl4Text(self, event):
        event.Skip()
        self.team1Player4Stats[5] = self.angrySpinTeam1Ctrl4.GetValue()

    def OnAngrySpinTeam1Ctrl5Text(self, event):
        event.Skip()
        self.team1Player5Stats[5] = self.angrySpinTeam1Ctrl5.GetValue()
        
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

    def OnSPowerSpinTeam2Ctrl1Text(self, event):
        event.Skip()
        self.team2Player1Stats[0] = self.sPowerSpinTeam2Ctrl1.GetValue()

    def OnSPowerSpinTeam2Ctrl2Text(self, event):
        event.Skip()
        self.team2Player2Stats[0] = self.sPowerSpinTeam2Ctrl2.GetValue()

    def OnSPowerSpinTeam2Ctrl3Text(self, event):
        event.Skip()
        self.team2Player3Stats[0] = self.sPowerSpinTeam2Ctrl3.GetValue()

    def OnSPowerSpinTeam2Ctrl4Text(self, event):
        event.Skip()
        self.team2Player4Stats[0] = self.sPowerSpinTeam2Ctrl4.GetValue()

    def OnSPowerSpinTeam2Ctrl5Text(self, event):
        event.Skip()
        self.team2Player5Stats[0] = self.sPowerSpinTeam2Ctrl5.GetValue()
        
#-------------------------------------------------------------------------------

    def OnMPowerSpinTeam2Ctrl1Text(self, event):
        event.Skip()
        self.team2Player1Stats[1] = self.mPowerSpinTeam2Ctrl1.GetValue()

    def OnMPowerSpinTeam2Ctrl2Text(self, event):
        event.Skip()
        self.team2Player2Stats[1] = self.mPowerSpinTeam2Ctrl2.GetValue()

    def OnMPowerSpinTeam2Ctrl3Text(self, event):
        event.Skip()
        self.team2Player3Stats[1] = self.mPowerSpinTeam2Ctrl3.GetValue()

    def OnMPowerSpinTeam2Ctrl4Text(self, event):
        event.Skip()
        self.team2Player4Stats[1] = self.mPowerSpinTeam2Ctrl4.GetValue()

    def OnMPowerSpinTeam2Ctrl5Text(self, event):
        event.Skip()
        self.team2Player5Stats[1] = self.mPowerSpinTeam3Ctrl5.GetValue()

#-------------------------------------------------------------------------------

    def OnSpeedSpinTeam2Ctrl1Text(self, event):
        event.Skip()
        self.team2Player1Stats[2] = self.speedSpinTeam2Ctrl1.GetValue()

    def OnSpeedSpinTeam2Ctrl2Text(self, event):
        event.Skip()
        self.team2Player2Stats[2] = self.speedSpinTeam2Ctrl2.GetValue()

    def OnSpeedSpinTeam2Ctrl3Text(self, event):
        event.Skip()
        self.team2Player3Stats[2] = self.speedSpinTeam2Ctrl3.GetValue()

    def OnSpeedSpinTeam2Ctrl4Text(self, event):
        event.Skip()
        self.team2Player4Stats[2] = self.speedSpinTeam2Ctrl4.GetValue()

    def OnSpeedSpinTeam2Ctrl5Text(self, event):
        event.Skip()
        self.team2Player5Stats[2] = self.speedSpinTeam2Ctrl5.GetValue()
        
#-------------------------------------------------------------------------------

    def OnWeightSpinTeam2Ctrl1Text(self, event):
        event.Skip()
        self.team2Player1Stats[3] = self.weightSpinTeam2Ctrl1.GetValue()

    def OnWeightSpinTeam2Ctrl2Text(self, event):
        event.Skip()
        self.team2Player2Stats[3] = self.weightSpinTeam2Ctrl2.GetValue()

    def OnWeightSpinTeam2Ctrl3Text(self, event):
        event.Skip()
        self.team2Player3Stats[3] = self.weightSpinTeam2Ctrl3.GetValue()

    def OnWeightSpinTeam2Ctrl4Text(self, event):
        event.Skip()
        self.team2Player4Stats[3] = self.weightSpinTeam2Ctrl4.GetValue()

    def OnWeightSpinTeam2Ctrl5Text(self, event):
        event.Skip()
        self.team2Player5Stats[3] = self.weightSpinTeam2Ctrl5.GetValue()
        
#-------------------------------------------------------------------------------

    def OnAngrySpinTeam2Ctrl1Text(self, event):
        event.Skip()
        self.team2Player1Stats[5] = self.angrySpinTeam2Ctrl1.GetValue()

    def OnAngrySpinTeam2Ctrl2Text(self, event):
        event.Skip()
        self.team2Player2Stats[5] = self.angrySpinTeam2Ctrl2.GetValue()

    def OnAngrySpinTeam2Ctrl3Text(self, event):
        event.Skip()
        self.team2Player3Stats[5] = self.angrySpinTeam2Ctrl3.GetValue()

    def OnAngrySpinTeam2Ctrl4Text(self, event):
        event.Skip()
        self.team2Player4Stats[5] = self.angrySpinTeam2Ctrl4.GetValue()

    def OnAngrySpinTeam2Ctrl5Text(self, event):
        event.Skip()
        self.team2Player5Stats[5] = self.angrySpinTeam2Ctrl5.GetValue()

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

    def OnSPowerSpinTeam3Ctrl1Text(self, event):
        event.Skip()
        self.team3Player1Stats[0] = self.sPowerSpinTeam3Ctrl1.GetValue()

    def OnSPowerSpinTeam3Ctrl2Text(self, event):
        event.Skip()
        self.team3Player2Stats[0] = self.sPowerSpinTeam3Ctrl2.GetValue()

    def OnSPowerSpinTeam3Ctrl3Text(self, event):
        event.Skip()
        self.team3Player3Stats[0] = self.sPowerSpinTeam3Ctrl3.GetValue()

    def OnSPowerSpinTeam3Ctrl4Text(self, event):
        event.Skip()
        self.team3Player4Stats[0] = self.sPowerSpinTeam3Ctrl4.GetValue()

    def OnSPowerSpinTeam3Ctrl5Text(self, event):
        event.Skip()
        self.team3Player5Stats[0] = self.sPowerSpinTeam3Ctrl5.GetValue()

#-------------------------------------------------------------------------------

    def OnMPowerSpinTeam3Ctrl1Text(self, event):
        event.Skip()
        self.team3Player1Stats[1] = self.mPowerSpinTeam3Ctrl1.GetValue()

    def OnMPowerSpinTeam3Ctrl2Text(self, event):
        event.Skip()
        self.team3Player2Stats[1] = self.mPowerSpinTeam3Ctrl2.GetValue()

    def OnMPowerSpinTeam3Ctrl3Text(self, event):
        event.Skip()
        self.team3Player3Stats[1] = self.mPowerSpinTeam3Ctrl3.GetValue()

    def OnMPowerSpinTeam3Ctrl4Text(self, event):
        event.Skip()
        self.team3Player4Stats[1] = self.mPowerSpinTeam3Ctrl4.GetValue()

    def OnMPowerSpinTeam3Ctrl5Text(self, event):
        event.Skip()
        self.team3Player5Stats[1] = self.mPowerSpinTeam3Ctrl5.GetValue()

#-------------------------------------------------------------------------------

    def OnSpeedSpinTeam3Ctrl1Text(self, event):
        event.Skip()
        self.team3Player1Stats[2] = self.speedSpinTeam3Ctrl1.GetValue()

    def OnSpeedSpinTeam3Ctrl2Text(self, event):
        event.Skip()
        self.team3Player2Stats[2] = self.speedSpinTeam3Ctrl2.GetValue()

    def OnSpeedSpinTeam3Ctrl3Text(self, event):
        event.Skip()
        self.team3Player3Stats[2] = self.speedSpinTeam3Ctrl3.GetValue()

    def OnSpeedSpinTeam3Ctrl4Text(self, event):
        event.Skip()
        self.team3Player4Stats[2] = self.speedSpinTeam3Ctrl4.GetValue()

    def OnSpeedSpinTeam3Ctrl5Text(self, event):
        event.Skip()
        self.team3Player5Stats[2] = self.speedSpinTeam3Ctrl5.GetValue()

#-------------------------------------------------------------------------------

    def OnWeightSpinTeam3Ctrl1Text(self, event):
        event.Skip()
        self.team3Player1Stats[3] = self.weightSpinTeam3Ctrl1.GetValue()

    def OnWeightSpinTeam3Ctrl2Text(self, event):
        event.Skip()
        self.team3Player2Stats[3] = self.weightSpinTeam3Ctrl2.GetValue()

    def OnWeightSpinTeam3Ctrl3Text(self, event):
        event.Skip()
        self.team3Player3Stats[3] = self.weightSpinTeam3Ctrl3.GetValue()

    def OnWeightSpinTeam3Ctrl4Text(self, event):
        event.Skip()
        self.team3Player4Stats[3] = self.weightSpinTeam3Ctrl4.GetValue()

    def OnWeightSpinTeam3Ctrl5Text(self, event):
        event.Skip()
        self.team3Player5Stats[3] = self.weightSpinTeam3Ctrl5.GetValue()

#-------------------------------------------------------------------------------

    def OnAngrySpinTeam3Ctrl1Text(self, event):
        event.Skip()
        self.team3Player1Stats[5] = self.angrySpinTeam3Ctrl1.GetValue()

    def OnAngrySpinTeam3Ctrl2Text(self, event):
        event.Skip()
        self.team3Player2Stats[5] = self.angrySpinTeam3Ctrl2.GetValue()

    def OnAngrySpinTeam3Ctrl3Text(self, event):
        event.Skip()
        self.team3Player3Stats[5] = self.angrySpinTeam3Ctrl3.GetValue()

    def OnAngrySpinTeam3Ctrl4Text(self, event):
        event.Skip()
        self.team3Player4Stats[5] = self.angrySpinTeam3Ctrl4.GetValue()

    def OnAngrySpinTeam3Ctrl5Text(self, event):
        event.Skip()
        self.team3Player5Stats[5] = self.angrySpinTeam3Ctrl5.GetValue()
        
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

    def OnSPowerSpinTeam4Ctrl1Text(self, event):
        event.Skip()
        self.team4Player1Stats[0] = self.sPowerSpinTeam4Ctrl1.GetValue()
        
    def OnSPowerSpinTeam4Ctrl2Text(self, event):
        event.Skip()
        self.team4Player2Stats[0] = self.sPowerSpinTeam4Ctrl2.GetValue()

    def OnSPowerSpinTeam4Ctrl3Text(self, event):
        event.Skip()
        self.team4Player3Stats[0] = self.sPowerSpinTeam4Ctrl3.GetValue()

    def OnSPowerSpinTeam4Ctrl4Text(self, event):
        event.Skip()
        self.team4Player4Stats[0] = self.sPowerSpinTeam4Ctrl4.GetValue()

    def OnSPowerSpinTeam4Ctrl5Text(self, event):
        event.Skip()
        self.team4Player5Stats[0] = self.sPowerSpinTeam4Ctrl5.GetValue()

#-------------------------------------------------------------------------------

    def OnMPowerSpinTeam4Ctrl1Text(self, event):
        event.Skip()
        self.team4Player1Stats[1] = self.mPowerSpinTeam4Ctrl1.GetValue()

    def OnMPowerSpinTeam4Ctrl2Text(self, event):
        event.Skip()
        self.team4Player2Stats[1] = self.mPowerSpinTeam4Ctrl2.GetValue()

    def OnMPowerSpinTeam4Ctrl3Text(self, event):
        event.Skip()
        self.team4Player3Stats[1] = self.mPowerSpinTeam4Ctrl3.GetValue()

    def OnMPowerSpinTeam4Ctrl4Text(self, event):
        event.Skip()
        self.team4Player4Stats[1] = self.mPowerSpinTeam4Ctrl4.GetValue()

    def OnMPowerSpinTeam4Ctrl5Text(self, event):
        event.Skip()
        self.team4Player5Stats[1] = self.mPowerSpinTeam4Ctrl5.GetValue()
        
#-------------------------------------------------------------------------------

    def OnSpeedSpinTeam4Ctrl1Text(self, event):
        event.Skip()
        self.team4Player1Stats[2] = self.speedSpinTeam4Ctrl1.GetValue()

    def OnSpeedSpinTeam4Ctrl2Text(self, event):
        event.Skip()
        self.team4Player2Stats[2] = self.speedSpinTeam4Ctrl2.GetValue()

    def OnSpeedSpinTeam4Ctrl3Text(self, event):
        event.Skip()
        self.team4Player3Stats[2] = self.speedSpinTeam4Ctrl3.GetValue()

    def OnSpeedSpinTeam4Ctrl4Text(self, event):
        event.Skip()
        self.team4Player4Stats[2] = self.speedSpinTeam4Ctrl4.GetValue()

    def OnSpeedSpinTeam4Ctrl5Text(self, event):
        event.Skip()
        self.team4Player5Stats[2] = self.speedSpinTeam4Ctrl5.GetValue()

#-------------------------------------------------------------------------------

    def OnWeightSpinTeam4Ctrl1Text(self, event):
        event.Skip()
        self.team4Player1Stats[3] = self.weightSpinTeam4Ctrl1.GetValue()

    def OnWeightSpinTeam4Ctrl2Text(self, event):
        event.Skip()
        self.team4Player2Stats[3] = self.weightSpinTeam4Ctrl2.GetValue()

    def OnWeightSpinTeam4Ctrl3Text(self, event):
        event.Skip()
        self.team4Player3Stats[3] = self.weightSpinTeam4Ctrl3.GetValue()

    def OnWeightSpinTeam4Ctrl4Text(self, event):
        event.Skip()
        self.team4Player4Stats[3] = self.weightSpinTeam4Ctrl4.GetValue()

    def OnWeightSpinTeam4Ctrl5Text(self, event):
        event.Skip()
        self.team4Player5Stats[3] = self.weightSpinTeam4Ctrl5.GetValue()

#-------------------------------------------------------------------------------

    def OnAngrySpinTeam4Ctrl1Text(self, event):
        event.Skip()
        self.team4Player1Stats[5] = self.angrySpinTeam4Ctrl1.GetValue()

    def OnAngrySpinTeam4Ctrl2Text(self, event):
        event.Skip()
        self.team4Player2Stats[5] = self.angrySpinTeam4Ctrl2.GetValue()

    def OnAngrySpinTeam4Ctrl3Text(self, event):
        event.Skip()
        self.team4Player3Stats[5] = self.angrySpinTeam4Ctrl3.GetValue()

    def OnAngrySpinTeam4Ctrl4Text(self, event):
        event.Skip()
        self.team4Player4Stats[5] = self.angrySpinTeam4Ctrl4.GetValue()

    def OnAngrySpinTeam4Ctrl5Text(self, event):
        event.Skip()
        self.team4Player5Stats[5] = self.angrySpinTeam4Ctrl5.GetValue()

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

    def OnSPowerSpinTeam5Ctrl1Text(self, event):
        event.Skip()
        self.team5Player1Stats[0] = self.sPowerSpinTeam5Ctrl1.GetValue()

    def OnSPowerSpinTeam5Ctrl2Text(self, event):
        event.Skip()
        self.team5Player2Stats[0] = self.sPowerSpinTeam5Ctrl2.GetValue()

    def OnSPowerSpinTeam5Ctrl3Text(self, event):
        event.Skip()
        self.team5Player3Stats[0] = self.sPowerSpinTeam5Ctrl3.GetValue()

    def OnSPowerSpinTeam5Ctrl4Text(self, event):
        event.Skip()
        self.team5Player4Stats[0] = self.sPowerSpinTeam5Ctrl4.GetValue()

    def OnSPowerSpinTeam5Ctrl5Text(self, event):
        event.Skip()
        self.team5Player5Stats[0] = self.sPowerSpinTeam5Ctrl5.GetValue()
        
#-------------------------------------------------------------------------------

    def OnMPowerSpinTeam5Ctrl1Text(self, event):
        event.Skip()
        self.team5Player1Stats[1] = self.mPowerSpinTeam5Ctrl1.GetValue()

    def OnMPowerSpinTeam5Ctrl2Text(self, event):
        event.Skip()
        self.team5Player2Stats[1] = self.mPowerSpinTeam5Ctrl2.GetValue()

    def OnMPowerSpinTeam5Ctrl3Text(self, event):
        event.Skip()
        self.team5Player3Stats[1] = self.mPowerSpinTeam5Ctrl3.GetValue()

    def OnMPowerSpinTeam5Ctrl4Text(self, event):
        event.Skip()
        self.team5Player4Stats[1] = self.mPowerSpinTeam5Ctrl4.GetValue()

    def OnMPowerSpinTeam5Ctrl5Text(self, event):
        event.Skip()
        self.team5Player5Stats[1] = self.mPowerSpinTeam5Ctrl5.GetValue()
        
#-------------------------------------------------------------------------------

    def OnSpeedSpinTeam5Ctrl1Text(self, event):
        event.Skip()
        self.team5Player1Stats[2] = self.speedSpinTeam5Ctrl1.GetValue()

    def OnSpeedSpinTeam5Ctrl2Text(self, event):
        event.Skip()
        self.team5Player2Stats[2] = self.speedSpinTeam5Ctrl2.GetValue()

    def OnSpeedSpinTeam5Ctrl3Text(self, event):
        event.Skip()
        self.team5Player3Stats[2] = self.speedSpinTeam5Ctrl3.GetValue()

    def OnSpeedSpinTeam5Ctrl4Text(self, event):
        event.Skip()
        self.team5Player4Stats[2] = self.speedSpinTeam5Ctrl4.GetValue()

    def OnSpeedSpinTeam5Ctrl5Text(self, event):
        event.Skip()
        self.team5Player5Stats[2] = self.speedSpinTeam5Ctrl5.GetValue()

#-------------------------------------------------------------------------------

    def OnWeightSpinTeam5Ctrl1Text(self, event):
        event.Skip()
        self.team5Player1Stats[3] = self.weightSpinTeam5Ctrl1.GetValue()

    def OnWeightSpinTeam5Ctrl2Text(self, event):
        event.Skip()
        self.team5Player2Stats[3] = self.weightSpinTeam5Ctrl2.GetValue()

    def OnWeightSpinTeam5Ctrl3Text(self, event):
        event.Skip()
        self.team5Player3Stats[3] = self.weightSpinTeam5Ctrl3.GetValue()

    def OnWeightSpinTeam5Ctrl4Text(self, event):
        event.Skip()
        self.team5Player4Stats[3] = self.weightSpinTeam5Ctrl4.GetValue()

    def OnWeightSpinTeam5Ctrl5Text(self, event):
        event.Skip()
        self.team5Player5Stats[3] = self.weightSpinTeam5Ctrl5.GetValue()
        
#-------------------------------------------------------------------------------

    def OnAngrySpinTeam5Ctrl1Text(self, event):
        event.Skip()
        self.team5Player1Stats[5] = self.angrySpinTeam5Ctrl1.GetValue()

    def OnAngrySpinTeam5Ctrl2Text(self, event):
        event.Skip()
        self.team5Player2Stats[5] = self.angrySpinTeam5Ctrl2.GetValue()

    def OnAngrySpinTeam5Ctrl3Text(self, event):
        event.Skip()
        self.team5Player3Stats[5] = self.angrySpinTeam5Ctrl3.GetValue()

    def OnAngrySpinTeam5Ctrl4Text(self, event):
        event.Skip()
        self.team5Player4Stats[5] = self.angrySpinTeam5Ctrl4.GetValue()

    def OnAngrySpinTeam5Ctrl5Text(self, event):
        event.Skip()
        self.team5Player5Stats[5] = self.angrySpinTeam5Ctrl5.GetValue()

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

    def OnSPowerSpinTeam6Ctrl1Text(self, event):
        event.Skip()
        self.team6Player1Stats[0] = self.sPowerSpinTeam6Ctrl1.GetValue()

    def OnSPowerSpinTeam6Ctrl2Text(self, event):
        event.Skip()
        self.team6Player2Stats[0] = self.sPowerSpinTeam6Ctrl2.GetValue()

    def OnSPowerSpinTeam6Ctrl3Text(self, event):
        event.Skip()
        self.team6Player3Stats[0] = self.sPowerSpinTeam6Ctrl3.GetValue()

    def OnSPowerSpinTeam6Ctrl4Text(self, event):
        event.Skip()
        self.team6Player4Stats[0] = self.sPowerSpinTeam6Ctrl4.GetValue()

    def OnSPowerSpinTeam6Ctrl5Text(self, event):
        event.Skip()
        self.team6Player5Stats[0] = self.sPowerSpinTeam6Ctrl5.GetValue()
        
#-------------------------------------------------------------------------------

    def OnMPowerSpinTeam6Ctrl1Text(self, event):
        event.Skip()
        self.team6Player1Stats[1] = self.mPowerSpinTeam6Ctrl1.GetValue()

    def OnMPowerSpinTeam6Ctrl2Text(self, event):
        event.Skip()
        self.team6Player2Stats[1] = self.mPowerSpinTeam6Ctrl2.GetValue()

    def OnMPowerSpinTeam6Ctrl3Text(self, event):
        event.Skip()
        self.team6Player3Stats[1] = self.mPowerSpinTeam6Ctrl3.GetValue()

    def OnMPowerSpinTeam6Ctrl4Text(self, event):
        event.Skip()
        self.team6Player4Stats[1] = self.mPowerSpinTeam6Ctrl4.GetValue()

    def OnMPowerSpinTeam6Ctrl5Text(self, event):
        event.Skip()
        self.team6Player5Stats[1] = self.mPowerSpinTeam6Ctrl5.GetValue()
        
#-------------------------------------------------------------------------------
        
    def OnSpeedSpinTeam6Ctrl1Text(self, event):
        event.Skip()
        self.team6Player1Stats[2] = self.speedSpinTeam6Ctrl1.GetValue()

    def OnSpeedSpinTeam6Ctrl2Text(self, event):
        event.Skip()
        self.team6Player2Stats[2] = self.speedSpinTeam6Ctrl2.GetValue()

    def OnSpeedSpinTeam6Ctrl3Text(self, event):
        event.Skip()
        self.team6Player3Stats[2] = self.speedSpinTeam6Ctrl3.GetValue()

    def OnSpeedSpinTeam6Ctrl4Text(self, event):
        event.Skip()
        self.team6Player4Stats[2] = self.speedSpinTeam6Ctrl4.GetValue()

    def OnSpeedSpinTeam6Ctrl5Text(self, event):
        event.Skip()
        self.team6Player5Stats[2] = self.speedSpinTeam6Ctrl5.GetValue()

#-------------------------------------------------------------------------------

    def OnWeightSpinTeam6Ctrl1Text(self, event):
        event.Skip()
        self.team6Player1Stats[3] = self.weightSpinTeam6Ctrl1.GetValue()

    def OnWeightSpinTeam6Ctrl2Text(self, event):
        event.Skip()
        self.team6Player2Stats[3] = self.weightSpinTeam6Ctrl2.GetValue()

    def OnWeightSpinTeam6Ctrl3Text(self, event):
        event.Skip()
        self.team6Player3Stats[3] = self.weightSpinTeam6Ctrl3.GetValue()

    def OnWeightSpinTeam6Ctrl4Text(self, event):
        event.Skip()
        self.team6Player4Stats[3] = self.weightSpinTeam6Ctrl4.GetValue()

    def OnWeightSpinTeam6Ctrl5Text(self, event):
        event.Skip()
        self.team6Player5Stats[3] = self.weightSpinTeam6Ctrl5.GetValue()

#-------------------------------------------------------------------------------

    def OnAngrySpinTeam6Ctrl1Text(self, event):
        event.Skip()
        self.team6Player1Stats[5] = self.angrySpinTeam6Ctrl1.GetValue()

    def OnAngrySpinTeam6Ctrl2Text(self, event):
        event.Skip()
        self.team6Player2Stats[5] = self.angrySpinTeam6Ctrl2.GetValue()

    def OnAngrySpinTeam6Ctrl3Text(self, event):
        event.Skip()
        self.team6Player3Stats[5] = self.angrySpinTeam6Ctrl3.GetValue()

    def OnAngrySpinTeam6Ctrl4Text(self, event):
        event.Skip()
        self.team6Player4Stats[5] = self.angrySpinTeam6Ctrl4.GetValue()

    def OnAngrySpinTeam6Ctrl5Text(self, event):
        event.Skip()
        self.team6Player5Stats[5] = self.angrySpinTeam6Ctrl5.GetValue()


#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

    def OnSPowerSpinTeam7Ctrl1Text(self, event):
        event.Skip()
        self.team7Player1Stats[0] = self.sPowerSpinTeam7Ctrl1.GetValue()

    def OnSPowerSpinTeam7Ctrl2Text(self, event):
        event.Skip()
        self.team7Player2Stats[0] = self.sPowerSpinTeam7Ctrl2.GetValue()

    def OnSPowerSpinTeam7Ctrl3Text(self, event):
        event.Skip()
        self.team7Player3Stats[0] = self.sPowerSpinTeam7Ctrl3.GetValue()

    def OnSPowerSpinTeam7Ctrl4Text(self, event):
        event.Skip()
        self.team7Player4Stats[0] = self.sPowerSpinTeam7Ctrl4.GetValue()

    def OnSPowerSpinTeam7Ctrl5Text(self, event):
        event.Skip()
        self.team7Player5Stats[0] = self.sPowerSpinTeam7Ctrl5.GetValue()

#-------------------------------------------------------------------------------

    def OnMPowerSpinTeam7Ctrl1Text(self, event):
        event.Skip()
        self.team7Player1Stats[1] = self.mPowerSpinTeam7Ctrl1.GetValue()

    def OnMPowerSpinTeam7Ctrl2Text(self, event):
        event.Skip()
        self.team7Player2Stats[1] = self.mPowerSpinTeam7Ctrl2.GetValue()

    def OnMPowerSpinTeam7Ctrl3Text(self, event):
        event.Skip()
        self.team7Player3Stats[1] = self.mPowerSpinTeam7Ctrl3.GetValue()

    def OnMPowerSpinTeam7Ctrl4Text(self, event):
        event.Skip()
        self.team7Player4Stats[1] = self.mPowerSpinTeam7Ctrl4.GetValue()

    def OnMPowerSpinTeam7Ctrl5Text(self, event):
        event.Skip()
        self.team7Player5Stats[1] = self.mPowerSpinTeam7Ctrl5.GetValue()

#-------------------------------------------------------------------------------

    def OnSpeedSpinTeam7Ctrl1Text(self, event):
        event.Skip()
        self.team7Player1Stats[2] = self.speedSpinTeam7Ctrl1.GetValue()

    def OnSpeedSpinTeam7Ctrl2Text(self, event):
        event.Skip()
        self.team7Player2Stats[2] = self.speedSpinTeam7Ctrl2.GetValue()

    def OnSpeedSpinTeam7Ctrl3Text(self, event):
        event.Skip()
        self.team7Player3Stats[2] = self.speedSpinTeam7Ctrl3.GetValue()

    def OnSpeedSpinTeam7Ctrl4Text(self, event):
        event.Skip()
        self.team7Player4Stats[2] = self.speedSpinTeam7Ctrl4.GetValue()

    def OnSpeedSpinTeam7Ctrl5Text(self, event):
        event.Skip()
        self.team7Player5Stats[2] = self.speedSpinTeam7Ctrl5.GetValue()

#-------------------------------------------------------------------------------

    def OnWeightSpinTeam7Ctrl1Text(self, event):
        event.Skip()
        self.team7Player1Stats[3] = self.weightSpinTeam7Ctrl1.GetValue()
        
    def OnWeightSpinTeam7Ctrl2Text(self, event):
        event.Skip()
        self.team7Player2Stats[3] = self.weightSpinTeam7Ctrl2.GetValue()

    def OnWeightSpinTeam7Ctrl3Text(self, event):
        event.Skip()
        self.team7Player3Stats[3] = self.weightSpinTeam7Ctrl3.GetValue()

    def OnWeightSpinTeam7Ctrl4Text(self, event):
        event.Skip()
        self.team7Player4Stats[3] = self.weightSpinTeam7Ctrl4.GetValue()

    def OnWeightSpinTeam7Ctrl5Text(self, event):
        event.Skip()
        self.team7Player5Stats[3] = self.weightSpinTeam7Ctrl5.GetValue()

#-------------------------------------------------------------------------------

    def OnAngrySpinTeam7Ctrl1Text(self, event):
        event.Skip()
        self.team7Player1Stats[5] = self.angrySpinTeam7Ctrl1.GetValue()

    def OnAngrySpinTeam7Ctrl2Text(self, event):
        event.Skip()
        self.team7Player2Stats[5] = self.angrySpinTeam7Ctrl2.GetValue()

    def OnAngrySpinTeam7Ctrl3Text(self, event):
        event.Skip()
        self.team7Player3Stats[5] = self.angrySpinTeam7Ctrl3.GetValue()

    def OnAngrySpinTeam7Ctrl4Text(self, event):
        event.Skip()
        self.team7Player4Stats[5] = self.angrySpinTeam7Ctrl4.GetValue()

    def OnAngrySpinTeam7Ctrl5Text(self, event):
        event.Skip()
        self.team7Player5Stats[5] = self.angrySpinTeam7Ctrl5.GetValue()

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

    def OnSPowerSpinTeam8Ctrl1Text(self, event):
        event.Skip()
        self.team8Player1Stats[0] = self.sPowerSpinTeam8Ctrl1.GetValue()

    def OnSPowerSpinTeam8Ctrl2Text(self, event):
        event.Skip()
        self.team8Player2Stats[0] = self.sPowerSpinTeam8Ctrl2.GetValue()

    def OnSPowerSpinTeam8Ctrl3Text(self, event):
        event.Skip()
        self.team8Player3Stats[0] = self.sPowerSpinTeam8Ctrl3.GetValue()

    def OnSPowerSpinTeam8Ctrl4Text(self, event):
        event.Skip()
        self.team8Player4Stats[0] = self.sPowerSpinTeam8Ctrl4.GetValue()

    def OnSPowerSpinTeam8Ctrl5Text(self, event):
        event.Skip()
        self.team8Player5Stats[0] = self.sPowerSpinTeam8Ctrl5.GetValue()

#-------------------------------------------------------------------------------

    def OnMPowerSpinTeam8Ctrl1Text(self, event):
        event.Skip()
        self.team8Player1Stats[1] = self.mPowerSpinTeam8Ctrl1.GetValue()

    def OnMPowerSpinTeam8Ctrl2Text(self, event):
        event.Skip()
        self.team8Player2Stats[1] = self.mPowerSpinTeam8Ctrl2.GetValue()

    def OnMPowerSpinTeam8Ctrl3Text(self, event):
        event.Skip()
        self.team8Player3Stats[1] = self.mPowerSpinTeam8Ctrl3.GetValue()

    def OnMPowerSpinTeam8Ctrl4Text(self, event):
        event.Skip()
        self.team8Player4Stats[1] = self.mPowerSpinTeam8Ctrl4.GetValue()

    def OnMPowerSpinTeam8Ctrl5Text(self, event):
        event.Skip()
        self.team8Player5Stats[1] = self.mPowerSpinTeam8Ctrl5.GetValue()

#-------------------------------------------------------------------------------

    def OnSpeedSpinTeam8Ctrl1Text(self, event):
        event.Skip()
        self.team8Player1Stats[2] = self.speedSpinTeam7Ctrl1.GetValue()

    def OnSpeedSpinTeam8Ctrl2Text(self, event):
        event.Skip()
        self.team8Player2Stats[2] = self.speedSpinTeam7Ctrl2.GetValue()

    def OnSpeedSpinTeam8Ctrl3Text(self, event):
        event.Skip()
        self.team8Player3Stats[2] = self.speedSpinTeam7Ctrl3.GetValue()

    def OnSpeedSpinTeam8Ctrl4Text(self, event):
        event.Skip()
        self.team8Player4Stats[2] = self.speedSpinTeam7Ctrl4.GetValue()

    def OnSpeedSpinTeam8Ctrl5Text(self, event):
        event.Skip()
        self.team8Player5Stats[2] = self.speedSpinTeam7Ctrl5.GetValue()

#-------------------------------------------------------------------------------

    def OnWeightSpinTeam8Ctrl1Text(self, event):
        event.Skip()
        self.team8Player1Stats[3] = self.weightSpinTeam8Ctrl1.GetValue()

    def OnWeightSpinTeam8Ctrl2Text(self, event):
        event.Skip()
        self.team8Player2Stats[3] = self.weightSpinTeam8Ctrl2.GetValue()

    def OnWeightSpinTeam8Ctrl3Text(self, event):
        event.Skip()
        self.team8Player3Stats[3] = self.weightSpinTeam8Ctrl3.GetValue()

    def OnWeightSpinTeam8Ctrl4Text(self, event):
        event.Skip()
        self.team8Player4Stats[3] = self.weightSpinTeam8Ctrl4.GetValue()

    def OnWeightSpinTeam8Ctrl5Text(self, event):
        event.Skip()
        self.team8Player5Stats[3] = self.weightSpinTeam8Ctrl5.GetValue()

#-------------------------------------------------------------------------------

    def OnAngrySpinTeam8Ctrl1Text(self, event):
        event.Skip()
        self.team8Player1Stats[5] = self.angrySpinTeam8Ctrl1.GetValue()

    def OnAngrySpinTeam8Ctrl2Text(self, event):
        event.Skip()
        self.team8Player2Stats[5] = self.angrySpinTeam8Ctrl2.GetValue()

    def OnAngrySpinTeam8Ctrl3Text(self, event):
        event.Skip()
        self.team8Player3Stats[5] = self.angrySpinTeam8Ctrl3.GetValue()

    def OnAngrySpinTeam8Ctrl4Text(self, event):
        event.Skip()
        self.team8Player4Stats[5] = self.angrySpinTeam8Ctrl4.GetValue()

    def OnAngrySpinTeam8Ctrl5Text(self, event):
        event.Skip()
        self.team8Player5Stats[5] = self.angrySpinTeam8Ctrl5.GetValue()

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

    def OnDisplayPowTeam1Ctrl1Text(self, event):
        event.Skip()
        self.playersDisplayStats[0][0][0] = self.displayPowTeam1Ctrl1.GetValue()

    def OnDisplaySpdTeam1Ctrl1Text(self, event):
        event.Skip()
        self.playersDisplayStats[0][1][0] = self.displaySpdTeam1Ctrl1.GetValue()

    def OnDisplayDefTeam1Ctrl1Text(self, event):
        event.Skip()
        self.playersDisplayStats[0][2][0] = self.displayDefTeam1Ctrl1.GetValue()
        
#-------------------------------------------------------------------------------

    def OnDisplayPowTeam1Ctrl2Text(self, event):
        event.Skip()
        self.playersDisplayStats[0][0][1] = self.displayPowTeam1Ctrl2.GetValue()

    def OnDisplaySpdTeam1Ctrl2Text(self, event):
        event.Skip()
        self.playersDisplayStats[0][1][1] = self.displaySpdTeam1Ctrl2.GetValue()

    def OnDisplayDefTeam1Ctrl2Text(self, event):
        event.Skip()
        self.playersDisplayStats[0][2][1] = self.displayDefTeam1Ctrl2.GetValue()
        
#-------------------------------------------------------------------------------

    def OnDisplayPowTeam1Ctrl3Text(self, event):
        event.Skip()
        self.playersDisplayStats[0][0][2] = self.displayPowTeam1Ctrl3.GetValue()

    def OnDisplaySpdTeam1Ctrl3Text(self, event):
        event.Skip()
        self.playersDisplayStats[0][1][2] = self.displaySpdTeam1Ctrl3.GetValue()

    def OnDisplayDefTeam1Ctrl3Text(self, event):
        event.Skip()
        self.playersDisplayStats[0][2][2] = self.displayDefTeam1Ctrl3.GetValue()
        
#-------------------------------------------------------------------------------

    def OnDisplayPowTeam1Ctrl4Text(self, event):
        event.Skip()
        self.playersDisplayStats[0][0][3] = self.displayPowTeam1Ctrl4.GetValue()

    def OnDisplaySpdTeam1Ctrl4Text(self, event):
        event.Skip()
        self.playersDisplayStats[0][1][3] = self.displaySpdTeam1Ctrl4.GetValue()

    def OnDisplayDefTeam1Ctrl4Text(self, event):
        event.Skip()
        self.playersDisplayStats[0][2][3] = self.displayDefTeam1Ctrl4.GetValue()
        
#-------------------------------------------------------------------------------

    def OnDisplayPowTeam1Ctrl5Text(self, event):
        event.Skip()
        self.playersDisplayStats[0][0][4] = self.displayPowTeam1Ctrl5.GetValue()

    def OnDisplaySpdTeam1Ctrl5Text(self, event):
        event.Skip()
        self.playersDisplayStats[0][1][4] = self.displaySpdTeam1Ctrl5.GetValue()

    def OnDisplayDefTeam1Ctrl5Text(self, event):
        event.Skip()
        self.playersDisplayStats[0][2][4] = self.displayDefTeam1Ctrl5.GetValue()

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

    def OnDisplayPowTeam2Ctrl1Text(self, event):
        event.Skip()
        self.playersDisplayStats[1][0][0] = self.displayPowTeam2Ctrl1.GetValue()
        
    def OnDisplaySpdTeam2Ctrl1Text(self, event):
        event.Skip()
        self.playersDisplayStats[1][1][0] = self.displaySpdTeam2Ctrl1.GetValue()
        
    def OnDisplayDefTeam2Ctrl1Text(self, event):
        event.Skip()
        self.playersDisplayStats[1][2][0] = self.displayDefTeam2Ctrl1.GetValue()
        
#-------------------------------------------------------------------------------
        
        
    def OnDisplayPowTeam2Ctrl2Text(self, event):
        event.Skip()
        self.playersDisplayStats[1][0][1] = self.displayPowTeam2Ctrl2.GetValue()
        
    def OnDisplaySpdTeam2Ctrl2Text(self, event):
        event.Skip()
        self.playersDisplayStats[1][1][1] = self.displaySpdTeam2Ctrl2.GetValue()       
        
    def OnDisplayDefTeam2Ctrl2Text(self, event):
        event.Skip()
        self.playersDisplayStats[1][2][1] = self.displayDefTeam2Ctrl2.GetValue()

#-------------------------------------------------------------------------------

    def OnDisplayPowTeam2Ctrl3Text(self, event):
        event.Skip()
        self.playersDisplayStats[1][0][2] = self.displayPowTeam2Ctrl3.GetValue()

    def OnDisplaySpdTeam2Ctrl3Text(self, event):
        event.Skip()
        self.playersDisplayStats[1][1][2] = self.displaySpdTeam2Ctrl3.GetValue()
        
    def OnDisplayDefTeam2Ctrl3Text(self, event):
        event.Skip()
        self.playersDisplayStats[1][2][2] = self.displayDefTeam2Ctrl3.GetValue()       

#-------------------------------------------------------------------------------

    def OnDisplayPowTeam2Ctrl4Text(self, event):
        event.Skip()
        self.playersDisplayStats[1][0][3] = self.displayPowTeam2Ctrl4.GetValue()
 
    def OnDisplaySpdTeam2Ctrl4Text(self, event):
        event.Skip()
        self.playersDisplayStats[1][1][3] = self.displaySpdTeam2Ctrl4.GetValue()
       
    def OnDisplayDefTeam2Ctrl4Text(self, event):
        event.Skip()   
        self.playersDisplayStats[1][2][3] = self.displayDefTeam2Ctrl4.GetValue()    
        
#-------------------------------------------------------------------------------
        
    def OnDisplayPowTeam2Ctrl5Text(self, event):
        event.Skip()
        self.playersDisplayStats[1][0][4] = self.displayPowTeam2Ctrl5.GetValue()

    def OnDisplaySpdTeam2Ctrl5Text(self, event):
        event.Skip()
        self.playersDisplayStats[1][1][4] = self.displaySpdTeam2Ctrl5.GetValue()

    def OnDisplayDefTeam2Ctrl5Text(self, event):
        event.Skip()
        self.playersDisplayStats[1][2][4] = self.displayDefTeam2Ctrl5.GetValue()

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
 
    def OnDisplayPowTeam3Ctrl1Text(self, event):
        event.Skip()
        self.playersDisplayStats[2][0][0] = self.displayPowTeam3Ctrl1.GetValue()
        
    def OnDisplaySpdTeam3Ctrl1Text(self, event):
        event.Skip()
        self.playersDisplayStats[2][1][0] = self.displaySpdTeam3Ctrl1.GetValue()

    def OnDisplayDefTeam3Ctrl1Text(self, event):
        event.Skip()
        self.playersDisplayStats[2][2][0] = self.displayDefTeam3Ctrl1.GetValue()

#-------------------------------------------------------------------------------

    def OnDisplayPowTeam3Ctrl2Text(self, event):
        event.Skip()
        self.playersDisplayStats[2][0][1] = self.displayPowTeam3Ctrl2.GetValue()
 
    def OnDisplaySpdTeam3Ctrl2Text(self, event):
        event.Skip()
        self.playersDisplayStats[2][1][1] = self.displaySpdTeam3Ctrl2.GetValue()       
        
    def OnDisplayDefTeam3Ctrl2Text(self, event):
        event.Skip()
        self.playersDisplayStats[2][2][1] = self.displayDefTeam3Ctrl2.GetValue()       
        
#-------------------------------------------------------------------------------

    def OnDisplayPowTeam3Ctrl3Text(self, event):
        event.Skip()
        self.playersDisplayStats[2][0][2] = self.displayPowTeam3Ctrl3.GetValue()

    def OnDisplaySpdTeam3Ctrl3Text(self, event):
        event.Skip()       
        self.playersDisplayStats[2][1][2] = self.displaySpdTeam3Ctrl3.GetValue() 
 
    def OnDisplayDefTeam3Ctrl3Text(self, event):
        event.Skip()     
        self.playersDisplayStats[2][2][2] = self.displayDefTeam3Ctrl3.GetValue()  
        
#-------------------------------------------------------------------------------
        
    def OnDisplayPowTeam3Ctrl4Text(self, event):
        event.Skip()
        self.playersDisplayStats[2][0][3] = self.displayPowTeam3Ctrl4.GetValue()

    def OnDisplaySpdTeam3Ctrl4Text(self, event):
        event.Skip()
        self.playersDisplayStats[2][1][3] = self.displaySpdTeam3Ctrl4.GetValue()        
 
    def OnDisplayDefTeam3Ctrl4Text(self, event):
        event.Skip()
        self.playersDisplayStats[2][2][3] = self.displayDefTeam3Ctrl4.GetValue()       
        
#-------------------------------------------------------------------------------

    def OnDisplayPowTeam3Ctrl5Text(self, event):
        event.Skip()
        self.playersDisplayStats[2][0][4] = self.displayPowTeam3Ctrl5.GetValue()
        
    def OnDisplaySpdTeam3Ctrl5Text(self, event):
        event.Skip()
        self.playersDisplayStats[2][1][4] = self.displaySpdTeam3Ctrl5.GetValue()

    def OnDisplayDefTeam3Ctrl5Text(self, event):
        event.Skip()
        self.playersDisplayStats[2][2][4] = self.displayDefTeam3Ctrl5.GetValue()
        
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

    def OnDisplayPowTeam4Ctrl1Text(self, event):
        event.Skip()
        self.playersDisplayStats[3][0][0] = self.displayPowTeam4Ctrl1.GetValue()

    def OnDisplaySpdTeam4Ctrl1Text(self, event):
        event.Skip()
        self.playersDisplayStats[3][1][0] = self.displaySpdTeam4Ctrl1.GetValue()

    def OnDisplayDefTeam4Ctrl1Text(self, event):
        event.Skip()
        self.playersDisplayStats[3][2][0] = self.displayDefTeam4Ctrl1.GetValue()

#-------------------------------------------------------------------------------

    def OnDisplayPowTeam4Ctrl2Text(self, event):
        event.Skip()
        self.playersDisplayStats[3][0][1] = self.displayPowTeam4Ctrl2.GetValue()

    def OnDisplaySpdTeam4Ctrl2Text(self, event):
        event.Skip()
        self.playersDisplayStats[3][1][1] = self.displaySpdTeam4Ctrl2.GetValue()
   
    def OnDisplayDefTeam4Ctrl2Text(self, event):
        event.Skip()
        self.playersDisplayStats[3][2][1] = self.displayDefTeam4Ctrl2.GetValue()   
        
#-------------------------------------------------------------------------------
                
    def OnDisplayPowTeam4Ctrl3Text(self, event):
        event.Skip()
        self.playersDisplayStats[3][0][2] = self.displayPowTeam4Ctrl3.GetValue()


    def OnDisplaySpdTeam4Ctrl3Text(self, event):
        event.Skip()
        self.playersDisplayStats[3][1][2] = self.displaySpdTeam4Ctrl3.GetValue()


    def OnDisplayDefTeam4Ctrl3Text(self, event):
        event.Skip()
        self.playersDisplayStats[3][2][2] = self.displayDefTeam4Ctrl3.GetValue()

#-------------------------------------------------------------------------------

    def OnDisplayPowTeam4Ctrl4Text(self, event):
        event.Skip()
        self.playersDisplayStats[3][0][3] = self.displayPowTeam4Ctrl4.GetValue()

    def OnDisplaySpdTeam4Ctrl4Text(self, event):
        event.Skip()
        self.playersDisplayStats[3][1][3] = self.displaySpdTeam4Ctrl4.GetValue()

    def OnDisplayDefTeam4Ctrl4Text(self, event):
        event.Skip()
        self.playersDisplayStats[3][2][3] = self.displayDefTeam4Ctrl4.GetValue()

#-------------------------------------------------------------------------------

    def OnDisplayPowTeam4Ctrl5Text(self, event):
        event.Skip()
        self.playersDisplayStats[3][0][4] = self.displayPowTeam4Ctrl5.GetValue()

    def OnDisplaySpdTeam4Ctrl5Text(self, event):
        event.Skip()
        self.playersDisplayStats[3][1][4] = self.displaySpdTeam4Ctrl5.GetValue()

    def OnDisplayDefTeam4Ctrl5Text(self, event):
        event.Skip()
        self.playersDisplayStats[3][2][4] = self.displayDefTeam4Ctrl5.GetValue()

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

    def OnDisplayPowTeam5Ctrl1Text(self, event):
        event.Skip()
        self.playersDisplayStats[4][0][0] = self.displayPowTeam5Ctrl1.GetValue()

    def OnDisplaySpdTeam5Ctrl1Text(self, event):
        event.Skip()
        self.playersDisplayStats[4][1][0] = self.displaySpdTeam5Ctrl1.GetValue()

    def OnDisplayDefTeam5Ctrl1Text(self, event):
        event.Skip()
        self.playersDisplayStats[4][2][0] = self.displayDefTeam5Ctrl1.GetValue()
        
#-------------------------------------------------------------------------------

    def OnDisplayPowTeam5Ctrl2Text(self, event):
        event.Skip()
        self.playersDisplayStats[4][0][1] = self.displayPowTeam5Ctrl2.GetValue()

    def OnDisplaySpdTeam5Ctrl2Text(self, event):
        event.Skip()
        self.playersDisplayStats[4][1][1] = self.displaySpdTeam5Ctrl2.GetValue()
        
    def OnDisplayDefTeam5Ctrl2Text(self, event):
        event.Skip()
        self.playersDisplayStats[4][2][1] = self.displayDefTeam5Ctrl2.GetValue()

#-------------------------------------------------------------------------------

    def OnDisplayPowTeam5Ctrl3Text(self, event):
        event.Skip()
        self.playersDisplayStats[4][0][2] = self.displayPowTeam5Ctrl3.GetValue()

    def OnDisplaySpdTeam5Ctrl3Text(self, event):
        event.Skip()
        self.playersDisplayStats[4][1][2] = self.displaySpdTeam5Ctrl3.GetValue()

    def OnDisplayDefTeam5Ctrl3Text(self, event):
        event.Skip()
        self.playersDisplayStats[4][2][2] = self.displayDefTeam5Ctrl3.GetValue()

#-------------------------------------------------------------------------------

    def OnDisplayPowTeam5Ctrl4Text(self, event):
        event.Skip()
        self.playersDisplayStats[4][0][3] = self.displayPowTeam5Ctrl4.GetValue()

    def OnDisplaySpdTeam5Ctrl4Text(self, event):
        event.Skip()
        self.playersDisplayStats[4][1][3] = self.displaySpdTeam5Ctrl4.GetValue()

    def OnDisplayDefTeam5Ctrl4Text(self, event):
        event.Skip()
        self.playersDisplayStats[4][2][3] = self.displayDefTeam5Ctrl4.GetValue()

#-------------------------------------------------------------------------------

    def OnDisplayPowTeam5Ctrl5Text(self, event):
        event.Skip()
        self.playersDisplayStats[4][0][4] = self.displayPowTeam5Ctrl5.GetValue()

    def OnDisplaySpdTeam5Ctrl5Text(self, event):
        event.Skip()
        self.playersDisplayStats[4][1][4] = self.displaySpdTeam5Ctrl5.GetValue()

    def OnDisplayDefTeam5Ctrl5Text(self, event):
        event.Skip()
        self.playersDisplayStats[4][2][4] = self.displayDefTeam5Ctrl5.GetValue()
        
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

    def OnDisplayPowTeam6Ctrl1Text(self, event):
        event.Skip()
        self.playersDisplayStats[5][0][0] = self.displayPowTeam6Ctrl1.GetValue()

    def OnDisplaySpdTeam6Ctrl1Text(self, event):
        event.Skip()
        self.playersDisplayStats[5][1][0] = self.displaySpdTeam6Ctrl1.GetValue()

    def OnDisplayDefTeam6Ctrl1Text(self, event):
        event.Skip()
        self.playersDisplayStats[5][2][0] = self.displayDefTeam6Ctrl1.GetValue()

#-------------------------------------------------------------------------------

    def OnDisplayPowTeam6Ctrl2Text(self, event):
        event.Skip()
        self.playersDisplayStats[5][0][1] = self.displayPowTeam6Ctrl2.GetValue()

    def OnDisplaySpdTeam6Ctrl2Text(self, event):
        event.Skip()
        self.playersDisplayStats[5][1][1] = self.displaySpdTeam6Ctrl2.GetValue()

    def OnDisplayDefTeam6Ctrl2Text(self, event):
        event.Skip()
        self.playersDisplayStats[5][2][1] = self.displayDefTeam6Ctrl2.GetValue()
        
#-------------------------------------------------------------------------------

    def OnDisplayPowTeam6Ctrl3Text(self, event):
        event.Skip()
        self.playersDisplayStats[5][0][2] = self.displayPowTeam6Ctrl3.GetValue()

    def OnDisplaySpdTeam6Ctrl3Text(self, event):
        event.Skip()
        self.playersDisplayStats[5][1][2] = self.displaySpdTeam6Ctrl3.GetValue()

    def OnDisplayDefTeam6Ctrl3Text(self, event):
        event.Skip()
        self.playersDisplayStats[5][2][2] = self.displayDefTeam6Ctrl3.GetValue()
        
#-------------------------------------------------------------------------------

    def OnDisplayPowTeam6Ctrl4Text(self, event):
        event.Skip()
        self.playersDisplayStats[5][0][3] = self.displayPowTeam6Ctrl4.GetValue()

    def OnDisplaySpdTeam6Ctrl4Text(self, event):
        event.Skip()
        self.playersDisplayStats[5][1][3] = self.displaySpdTeam6Ctrl4.GetValue()

    def OnDisplayDefTeam6Ctrl4Text(self, event):
        event.Skip()
        self.playersDisplayStats[5][2][3] = self.displayDefTeam6Ctrl4.GetValue()
        
#-------------------------------------------------------------------------------

    def OnDisplayPowTeam6Ctrl5Text(self, event):
        event.Skip()
        self.playersDisplayStats[5][0][4] = self.displayPowTeam6Ctrl5.GetValue()

    def OnDisplaySpdTeam6Ctrl5Text(self, event):
        event.Skip()
        self.playersDisplayStats[5][1][4] = self.displaySpdTeam6Ctrl5.GetValue()

    def OnDisplayDefTeam6Ctrl5Text(self, event):
        event.Skip()
        self.playersDisplayStats[5][2][4] = self.displayDefTeam6Ctrl5.GetValue()
        
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

    def OnDisplayPowTeam7Ctrl1Text(self, event):
        event.Skip()
        self.playersDisplayStats[6][0][0] = self.displayPowTeam7Ctrl1.GetValue()

    def OnDisplaySpdTeam7Ctrl1Text(self, event):
        event.Skip()
        self.playersDisplayStats[6][1][0] = self.displaySpdTeam7Ctrl1.GetValue()

    def OnDisplayDefTeam7Ctrl1Text(self, event):
        event.Skip()
        self.playersDisplayStats[6][2][0] = self.displayDefTeam7Ctrl1.GetValue()

#-------------------------------------------------------------------------------

    def OnDisplayPowTeam7Ctrl2Text(self, event):
        event.Skip()
        self.playersDisplayStats[6][0][1] = self.displayPowTeam7Ctrl2.GetValue()

    def OnDisplaySpdTeam7Ctrl2Text(self, event):
        event.Skip()
        self.playersDisplayStats[6][1][1] = self.displaySpdTeam7Ctrl2.GetValue()

    def OnDisplayDefTeam7Ctrl2Text(self, event):
        event.Skip()
        self.playersDisplayStats[6][2][1] = self.displayDefTeam7Ctrl2.GetValue()
        
#-------------------------------------------------------------------------------

    def OnDisplayPowTeam7Ctrl3Text(self, event):
        event.Skip()
        self.playersDisplayStats[6][0][2] = self.displayPowTeam7Ctrl3.GetValue()

    def OnDisplaySpdTeam7Ctrl3Text(self, event):
        event.Skip()
        self.playersDisplayStats[6][1][2] = self.displaySpdTeam7Ctrl3.GetValue()

    def OnDisplayDefTeam7Ctrl3Text(self, event):
        event.Skip()
        self.playersDisplayStats[6][2][2] = self.displayDefTeam7Ctrl3.GetValue()
        
#-------------------------------------------------------------------------------

    def OnDisplayPowTeam7Ctrl4Text(self, event):
        event.Skip()
        self.playersDisplayStats[6][0][3] = self.displayPowTeam7Ctrl4.GetValue()

    def OnDisplaySpdTeam7Ctrl4Text(self, event):
        event.Skip()
        self.playersDisplayStats[6][1][3] = self.displaySpdTeam7Ctrl4.GetValue()
        
    def OnDisplayDefTeam7Ctrl4Text(self, event):
        event.Skip()
        self.playersDisplayStats[6][2][3] = self.displayDefTeam7Ctrl4.GetValue()

#-------------------------------------------------------------------------------

    def OnDisplayPowTeam7Ctrl5Text(self, event):
        event.Skip()
        self.playersDisplayStats[6][0][4] = self.displayPowTeam7Ctrl5.GetValue()

    def OnDisplaySpdTeam7Ctrl5Text(self, event):
        event.Skip()
        self.playersDisplayStats[6][1][4] = self.displaySpdTeam7Ctrl5.GetValue()

    def OnDisplayDefTeam7Ctrl5Text(self, event):
        event.Skip()
        self.playersDisplayStats[6][2][4] = self.displayDefTeam7Ctrl5.GetValue()
        
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

    def OnDisplayPowTeam8Ctrl1Text(self, event):
        event.Skip()
        self.playersDisplayStats[7][0][0] = self.displayPowTeam8Ctrl1.GetValue()

    def OnDisplaySpdTeam8Ctrl1Text(self, event):
        event.Skip()
        self.playersDisplayStats[7][1][0] = self.displaySpdTeam8Ctrl1.GetValue()

    def OnDisplayDefTeam8Ctrl1Text(self, event):
        event.Skip()
        self.playersDisplayStats[7][2][0] = self.displayDefTeam8Ctrl1.GetValue()

#-------------------------------------------------------------------------------

    def OnDisplayPowTeam8Ctrl2Text(self, event):
        event.Skip()
        self.playersDisplayStats[7][0][1] = self.displayPowTeam8Ctrl2.GetValue()

    def OnDisplaySpdTeam8Ctrl2Text(self, event):
        event.Skip()
        self.playersDisplayStats[7][1][1] = self.displaySpdTeam8Ctrl2.GetValue()

    def OnDisplayDefTeam8Ctrl2Text(self, event):
        event.Skip()
        self.playersDisplayStats[7][2][1] = self.displayDefTeam8Ctrl2.GetValue()

#-------------------------------------------------------------------------------

    def OnDisplayPowTeam8Ctrl3Text(self, event):
        event.Skip()
        self.playersDisplayStats[7][0][2] = self.displayPowTeam8Ctrl3.GetValue()

    def OnDisplaySpdTeam8Ctrl3Text(self, event):
        event.Skip()
        self.playersDisplayStats[7][1][2] = self.displaySpdTeam8Ctrl3.GetValue()

    def OnDisplayDefTeam8Ctrl3Text(self, event):
        event.Skip()
        self.playersDisplayStats[7][2][2] = self.displayDefTeam8Ctrl3.GetValue()

#-------------------------------------------------------------------------------

    def OnDisplayPowTeam8Ctrl4Text(self, event):
        event.Skip()
        self.playersDisplayStats[7][0][3] = self.displayPowTeam8Ctrl4.GetValue()

    def OnDisplaySpdTeam8Ctrl4Text(self, event):
        event.Skip()
        self.playersDisplayStats[7][1][3] = self.displaySpdTeam8Ctrl4.GetValue()

    def OnDisplayDefTeam8Ctrl4Text(self, event):
        event.Skip()
        self.playersDisplayStats[7][2][3] = self.displayDefTeam8Ctrl4.GetValue()

#-------------------------------------------------------------------------------

    def OnDisplayPowTeam8Ctrl5Text(self, event):
        event.Skip()
        self.playersDisplayStats[7][0][4] = self.displayPowTeam8Ctrl5.GetValue()

    def OnDisplaySpdTeam8Ctrl5Text(self, event):
        event.Skip()
        self.playersDisplayStats[7][1][4] = self.displaySpdTeam8Ctrl5.GetValue()

    def OnDisplayDefTeam8Ctrl5Text(self, event):
        event.Skip()
        self.playersDisplayStats[7][2][4] = self.displayDefTeam8Ctrl5.GetValue()







#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

    def OnTeam1AttackSpinCtrl1Text(self, event):
        event.Skip()
        self.team1Attack = self.team1AttackSpinCtrl1.GetValue()
        
    def OnTeam1DefenseSpinCtrl1Text(self, event):
        event.Skip()
        self.team1Defense = self.team1DefenseSpinCtrl1.GetValue()

#-------------------------------------------------------------------------------

    def OnTeam2AttackSpinCtrl1Text(self, event):
        event.Skip()
        self.team2Attack = self.team2AttackSpinCtrl1.GetValue()

    def OnTeam2DefenseSpinCtrl1Text(self, event):
        event.Skip()
        self.team2Defense = self.team2DefenseSpinCtrl1.GetValue()

#-------------------------------------------------------------------------------

    def OnTeam3AttackSpinCtrl1Text(self, event):
        event.Skip()
        self.team3Attack = self.team3AttackSpinCtrl1.GetValue()

    def OnTeam3DefenseSpinCtrl1Text(self, event):
        event.Skip()
        self.team3Defense = self.team3DefenseSpinCtrl1.GetValue()

#-------------------------------------------------------------------------------

    def OnTeam4AttackSpinCtrl1Text(self, event):
        event.Skip()
        self.team4Attack = self.team4AttackSpinCtrl1.GetValue()

    def OnTeam4DefenseSpinCtrl1Text(self, event):
        event.Skip()
        self.team4Defense = self.team4DefenseSpinCtrl1.GetValue()

#-------------------------------------------------------------------------------

    def OnTeam5AttackSpinCtrl1Text(self, event):
        event.Skip()
        self.team5Attack = self.team5AttackSpinCtrl1.GetValue()

    def OnTeam5DefenseSpinCtrl1Text(self, event):
        event.Skip()
        self.team5Defense = self.team5DefenseSpinCtrl1.GetValue()

#-------------------------------------------------------------------------------

    def OnTeam6AttackSpinCtrl1Text(self, event):
        event.Skip()
        self.team6Attack = self.team6AttackSpinCtrl1.GetValue()

    def OnTeam6DefenseSpinCtrl1Text(self, event):
        event.Skip()
        self.team6Defense = self.team6DefenseSpinCtrl1.GetValue()

#-------------------------------------------------------------------------------

    def OnTeam7AttackSpinCtrl1Text(self, event):
        event.Skip()
        self.team7Attack = self.team7AttackSpinCtrl1.GetValue()

    def OnTeam7DefenseSpinCtrl1Text(self, event):
        event.Skip()
        self.team7Defense = self.team7DefenseSpinCtrl1.GetValue()

#-------------------------------------------------------------------------------

    def OnTeam8AttackSpinCtrl1Text(self, event):
        event.Skip()
        self.team8Attack = self.team8AttackSpinCtrl1.GetValue()

    def OnTeam8DefenseSpinCtrl1Text(self, event):
        event.Skip()
        self.team8Defense = self.team8DefenseSpinCtrl1.GetValue()

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

 
