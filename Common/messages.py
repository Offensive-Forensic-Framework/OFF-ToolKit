"""
Common terminal messages used across the framework.
"""

import os, sys, types

import helpers
import orchestra

version = "1.0.0"

def title_screen():
  print title()
  offtext = """------------------------------------------------------------------------------
  ______   ________  ________ 
 /      \ /        |/        |
/$$$$$$  |$$$$$$$$/ $$$$$$$$/ 
$$ |  $$ |$$ |__    $$ |__    
$$ |  $$ |$$    |   $$    |                                               __  
$$ |  $$ |$$$$$/    $$$$$/  _________ _____ ___  ___ _      ______  _____/ /__
$$ \__$$ |$$ |      $$ |   / ___/ __ `/ __ `__ \/ _ \ | /| / / __ \/ ___/ //_/
$$    $$/ $$ |      $$ |  / /  / /_/ / / / / / /  __/ |/ |/ / /_/ / /  / ,< 
 $$$$$$/  $$/       $$/  /_/   \__,_/_/ /_/ /_/\___/|__/|__/\____/_/  /_/|_| 

  Welcome to the OFF Toolkit... This tool is a automated helper for 
  advanced post explotation and targeting.
------------------------------------------------------------------------------"""
  print helpers.color(offtext, bold=False)

def title():
  os.system('clear')
  #stolen from Veil :)
  print " ============================================="
  print " Curent Version: " + version 
  print " ============================================="
  print " Twitter: @Killswitch_gui | Website: fdsd"
  print " ============================================="

def main_menu(loaded_modules):
  print " [*] Main Menu:\n"
  print "\t" + helpers.color(str(len(loaded_modules))) + " Module(s) loaded\n"

def help_msg(commands):
  """
  Print a help menu.
  """
  print " [*] Avaliable Commands:\n"
  orc = orchestra.Conductor()
  for (cmd, desc) in commands:
    print "\t%s\t%s" % ('{0: <12}'.format(cmd), desc)
  print ""