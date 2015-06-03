'''
This is the conductor which controls everything
'''

import glob
import helpers
import imp
import messages


class Conductor:

    def __init__(self):
        # Create dictionaries of supported modules
        # empty until stuff loaded into them
        #stolen from Veil :)
        self.modules = {}

        self.commands = [   ("use","use a specific module"),
                            ("info","information on a specific module"),
                            ("list","list available modules"),
                            ("update","update to the latest version"),
                            ("exit","exit")]
        self.modulescommands = [    ("set","set a specific option value"),
                                    ("info","show information about the payload"),
                                    ("generate","generate payload"),
                                    ("back","go to the main menu"),
                                    ("exit","exit Veil")]
        self.load_modules()

        
    def load_modules(self):
        for name in glob.glob('Modules/*.py'):
            if name.endswith(".py") and ("__init__" not in name):
                loaded_modules = imp.load_source(name.replace("/", ".").rstrip('.py'), name)
                self.modules[name] = loaded_modules

        return self.modules

    def list_modules(self):
        """
        Prints out available payloads in a nicely formatted way.
        """

        print helpers.color(" [*] Available payloads:\n")
        lastBase = None
        x = 1
        for name in self.modules:
            parts = name.split("/")
            if lastBase and parts[0] != lastBase:
                print ""
            lastBase = parts[0]
            print "\t%s)\t%s" % (x, '{0: <24}'.format(name))
            x += 1
        print ""

    def main_menu(self, showMessage=True):
        cmd = ""
        try:
            while cmd == "":

                if showMessage:
                    # print the title, where we are, and number of payloads loaded
                    messages.main_menu(self.modules)
                    messages.help_msg(self.commands)

                cmd = raw_input(helpers.color(' OFF -> ', blue=True)).strip()

                # handle our tab completed commands
                if cmd.startswith("help"):
                    messages.title()
                    messages.help_msg(self.commands)
                    cmd = ""
                    showMessage=False

                elif cmd.startswith("use"):

                    if len(cmd.split()) == 1:
                        messages.title()
                        cmd = ""

                elif cmd.startswith("list"):

                    if len(cmd.split()) == 1:
                        messages.title()
                        self.list_modules()     

                    cmd = ""
                    showMessage=False
                elif cmd.startswith("update"):

                    if len(cmd.split()) == 1:
                        messages.title()
                        self.list_modules()     

                    cmd = ""
                    showMessage=False

        # catch any ctrl + c interrupts
        except KeyboardInterrupt:
            if self.oneRun:
                # if we're being invoked from external code, just return
                # an empty string on an exit/quit instead of killing everything
                return ""
            else:
                print helpers.color("\n\n [!] Exiting...\n", warning=True)
                sys.exit()