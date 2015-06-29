##############################################################################################################################
#                               				 OFFENSIVE FORENSIC FRAMEWORK   								   			 #
#											 (WIRELESS NETWORK FORENSICS MODULE)											 #
#											Compatible w/ Win 7,8,10 (x86 & 64)												 #
#														(JUNE 2015)												   			 #
#															 BY 												   			 #
#					                           KEELYN ROBERTS(slacker007) 					   			 				     #
##############################################################################################################################


######################################### Function & Variable Formatting Guide ###############################################
# Global Variables are all uppercase EX: GLOBAL_VARIABLE = 0
# local Variables are in all lowercase EX: local_variable = 0
# Function Names are written by capitalizing the first letter of each word EX: def FunctionName(): or def Function_Name():


import _winreg
import threading
import Queue
import time
from xml.dom import minidom
from pprint import pprint

#***********************************************************************************
# Global Variables
#***********************************************************************************

########################	Static Registry Keys	################################

NETCARD_GUID = r'SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\NetworkCards'
CURRENT_NET_TCPIP_INFO = r'SYSTEM\\CurrentControlSet\\services\\Tcpip\\Parameters\\Interfaces'
NETWORK_HISTORY = r'SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\NetworkList\\Profiles'
GATEWAY_MAC_HISTORY = r'SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\NetworkList\\Signatures\\Unmanaged'

# List of Static Registry Keys: To add more keys just create a Variable up top with the same syntax and add the variable in this list.. And RUN!!
L_O_K = [NETCARD_GUID, CURRENT_NET_TCPIP_INFO, GATEWAY_MAC_HISTORY, NETWORK_HISTORY]

xml_file = open("reg_dataV2.xml", "w")
xml_file.write("<group name=\"Network Info,\">\n")
q = Queue.Queue()

def get_MF_info(q, r):
	Iterate_Reg_Keys(_winreg.HKEY_LOCAL_MACHINE, r)

def doc_handler(x):
	xml_file.write("</group>")
	xml_file.close()	

def Read_Subkeys (key): #(FUNCTION THAT READS OPENED HIVE KEY DATA INTO A //GENERATOR OBJECT//  TO REDUCE MEMORY FOOTPRINT!)
	counter = 0
	while True:
		try:
			subkey = _winreg.EnumKey(key, counter)
			yield subkey
			counter += 1
		except WindowsError as e:
			break
def Read_Key_Values (key): #(FUNCTION THAT READS THE VALUES OF AN OPENED SUBKEY USING A //GENERATOR OBJECT// TO REDUCE MEMORY FOOTPRINT!)
	counter = 0
	while True:
		try:
			keyvalue = _winreg.EnumValue(key, counter)
			yield keyvalue
			counter += 1
		except WindowsError as e:
			break
def Iterate_Reg_Keys(hkey, key_path, tabs=0): #(FUNCTION THAT CONTROLS THE ITERATION THROUGH SUBKEY & VALUES)
	key = _winreg.OpenKey(hkey, key_path, 0, _winreg.KEY_READ)
	for subkey_name in Read_Subkeys(key): #(LOOP THROUGH THE REGISTRY KEY AND OPEN EACH SUBKEY)
		xml_file.write("\t<subkey name=\"")
		xml_file.write(str(subkey_name))
		xml_file.write("\">\n")
		subkey_path = "%s\\%s" % (key_path, subkey_name)
		Iterate_Reg_Keys(hkey, subkey_path, tabs+1)
		subkey_value_path = _winreg.OpenKey(hkey, subkey_path, 0, _winreg.KEY_READ)
		data_found = False
		for subkey_value in Read_Key_Values(subkey_value_path): #(LOOP THROUGTH THE SUBKEY TO PULL VALUES FROM SUBKEY)
			data_found = True
			if isinstance(subkey_value[1], str):
				try:
					converted_from_ascii = ":".join("{:02x}".format(ord(c)) for c in subkey_value[1])
					value_data2 = str(converted_from_ascii)
				except UnicodeEncodeError:
					pass
			elif not isinstance(subkey_value[1], str):
				try:
					value_data2 = str(subkey_value[1])
				except UnicodeEncodeError:
					pass
			value_data1 = str(subkey_value[0])
			xml_file.write("\t\t<id name=\"")
			xml_file.write(str(value_data1))
			xml_file.write("\">")
			xml_file.write(str(value_data2))
			xml_file.write("</id>\n")
		xml_file.write("	</subkey>\n")
	_winreg.CloseKey(key)

# Execution Control...................................................

for each in L_O_K:
	t = threading.Thread(target=get_MF_info, args = (q, each))
	t.start()
	t.join()
t = threading.Thread(doc_handler(xml_file))
t.start()
t.join
