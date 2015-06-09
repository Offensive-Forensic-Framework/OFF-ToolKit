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
        self.dmodules = {}

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
        #load up modules on instance
        self.load_modules()

        
    def load_modules(self):
        #loop and assign key and name
        x = 1
        for name in glob.glob('Modules/*.py'):
            if name.endswith(".py") and ("__init__" not in name):
                loaded_modules = imp.load_source(name.replace("/", ".").rstrip('.py'), name)
                self.modules[name] = loaded_modules
                self.dmodules[x] = loaded_modules
                x += 1
        return self.dmodules
        return self.modules

    def list_modules(self):
        """
        Prints out available payloads in a nicely formatted way.
        """

        print helpers.color(" [*] Available payloads:\n", blue=True)
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
    #Handles all Use commands for each module: sets up the enviroment kinda
    def call_handler(self, name):
        name = name.strip('use') 
        name = name.lstrip();
        if name.isdigit() and 0 < int(name):
            print "we have a numer"
            print name
            if name in self.dmodules.keys():
                print "true"
            print name
        else:    
            self.module_menu(name)


    def module_menu(self, module):
        #int the Class Object
        module_name = module
        module = self.modules[module]
        module = module.ClassName()
        self.module_info(module)
        messages.helpmsg(self.modulescommands, showTitle=False)

        #module menu
        choice = ""
        while choice == "":

            while True:

                choice = raw_input(" [>] Please enter a command: ").strip()

                if choice != "":

                    parts = choice.strip().split()
                    # display help menu for the payload
                    if parts[0] == "info":
                        self.module_info(module)
                        choice = ""
                    if parts[0] == "help":
                        messages.helpmsg(self.payloadCommands)
                        choice = ""
                    # head back to the main menu
                    if parts[0] == "main" or parts[0] == "back":
                        #finished = True
                        return ""
                        #self.MainMenu()
                    if parts[0] == "exit":
                        raise KeyboardInterrupt

                    # Update Veil via git
                    if parts[0] == "update":
                        self.UpdateVeil()

                    # set specific options
                    if parts[0] == "set":

                        # catch the case of no value being supplied
                        if len(parts) == 1:
                            print helpers.color(" [!] ERROR: no value supplied\n", warning=True)

                        else:
                            option = parts[1]
                            value = "".join(parts[2:])
                            try:
                                module.required_options[option][0] = value
                            except:
                                print helpers.color(" [!] ERROR: Invalid value specified.\n", warning=True)
                                cmd = ""
                    # generate the payload
                    if parts[0] == "generate":
                        module.startx()


                else:
                    print helpers.color("\n [!] WARNING: not all required options filled\n", warning=True)
    





    def module_info(self, module, showInfo=True, showTitle=True):
        if showTitle == True:
            messages.title()

        if showInfo:
            # extract the payload class name from the instantiated object, then chop off the load folder prefix
            #modulename = "/".join(str(str(module.__class__)[str(module.__class__).find("ClassName"):]).split(".")[0].split("/")[1:])

            print helpers.color(" Module information:\n", blue=True)
            print "\tName:\t\t" + module.name
            print "\tLanguage:\t" + module.language
            # format this all nice-like
            print helpers.formatLong("Description:", module.description)
        # if required options were specified, output them
        if hasattr(module, 'required_options'):
            print helpers.color("\n Required Options:\n", blue=True)

            print " Name\t\t\tCurrent Value\tDescription"
            print " ----\t\t\t-------------\t-----------"

            # sort the dictionary by key before we output, so it looks nice
            for key in sorted(module.required_options.iterkeys()):
                print " %s\t%s\t%s" % ('{0: <16}'.format(key), '{0: <8}'.format(module.required_options[key][0]), module.required_options[key][1])

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
                    messages.title()
                    self.call_handler(cmd)
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