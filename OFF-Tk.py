#!/usr/bin/env python


"""

Front End for OFF


"""

# Import Modules
import logging
import sys
from Modules.Common import helpers
from Modules.Common import orchestra 
from Modules.Common import messages




def start_up():
  # Print main title
  messages.title_screen()
  orc = orchestra.Conductor()
  orc.main_menu()



if __name__ == '__main__':
  start_up()
