#!/usr/bin/env python3

#
# Released as open source by NCC Group Plc - http://www.nccgroup.com/
#
# Developed by Sultan Qasim Khan, Sultan.QasimKhan@nccgroup.trust
#
# http://www.github.com/nccgroup/nOBEX
#
# Released under GPLv3, a full copy of which can be found in COPYING.
#
import dbus
import os, struct, sys
from xml.etree import ElementTree
from xml.dom import minidom
from nOBEX import headers, responses
from nOBEX.common import OBEXError
from nOBEX.xml_helper import parse_xml
from clients.pbap import PBAPClient
from datetime import datetime

user_login = os.getlogin()

bus = dbus.SystemBus()

manager = dbus.Interface(bus.get_object('org.ofono', '/'),
						'org.ofono.Manager')

modems = manager.GetModems()
modem = modems[0][0]


modem_mac= modem.split("_",1)[1].replace("_", ":" )
print("Using modem %s" % modem_mac)	

print("create_dir")

dest_dir = str("/home/" + user_login + "/.config/CallControl/" + modem_mac + "/")


os.system('mkdir -p ' + dest_dir)

print(dest_dir)


  
contacts_date = str(dest_dir + "contacts_sync_date.txt")
contacts_fetched = str(dest_dir + "all_contacts.vcf")
contacts_edited = str(dest_dir + "contacts_edited.txt")
contacts_sorted = str(dest_dir + "contacts_sorted.txt")




os.system('rm ' + contacts_date)

  

def get_file(c, src_path, dest_path, verbose=True, folder_name=None, book=False):
    if verbose:
        if folder_name is not None:
            print("Fetching %s/%s" % (folder_name, src_path))
        else:
            print("Fetching %s" % src_path)

    if book:
        mimetype = b'x-bt/phonebook'
    else:
        mimetype = b'x-bt/vcard'
    print("Process started")
    hdrs, card = c.get(src_path, header_list=[headers.Type(mimetype)])


    with open(dest_path, 'wb') as f:
        f.write(card)




def main(argv):
    if not 1 <= len(argv) <= 2:
        usage()
        return -1
    elif len(argv) == 4:
        if argv[3] == "SIM":
            # If the SIM command line option was given, look in the SIM1
            # directory. Maybe the SIM2 directory exists on dual-SIM phones.
            prefix = "SIM1/"
        else:
            usage()
            return -1
    else:
        prefix = ""

    device_address = modem_mac


    c = PBAPClient(device_address)
    c.connect()

    c.setpath(prefix + "telecom")
    get_file(c, "pb.vcf", dest_dir+prefix+"all_contacts.vcf",
            folder_name=prefix+"telecom", book=True)

    c.disconnect()

    with open(contacts_fetched, 'r') as data, open(contacts_edited, 'w') as outfile:
        name = ''
        number = ''
        if data:
            for line in data:
                if line.startswith('END:'):
                   name = ''
                   number = ''
                if line.startswith('N:'):
                   name = line.split(':')[1].strip(' ;:\n').replace(";", " " )

                if name and line.startswith('TEL'):
                   number = line.split(':')[1].rstrip()
                   export_str = name + ": " + number
                   outfile.write(export_str + "\n")
                   name = number = ''
                   
    sorting = (contacts_sorted + ' ' + contacts_edited)
    os.system('sort -o' + sorting)
    
    con_date = open(contacts_date, "w") 
    local = datetime.now()
    x = str(local.strftime("%m/%d/%Y, %H:%M:%S"))
    con_date.write(x)
    con_date.close() 

    print("Done!")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
