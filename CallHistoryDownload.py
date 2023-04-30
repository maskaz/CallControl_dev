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

import os, struct, sys
from xml.etree import ElementTree
from xml.dom import minidom
from nOBEX import headers, responses
from nOBEX.common import OBEXError
from nOBEX.xml_helper import parse_xml
from clients.pbap import PBAPClient
import dbus
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


contacts_fetched = str(dest_dir + "call_history.vcf")
contacts_edited = str(dest_dir + "call_history_edited.txt")
contacts_sorted = str(dest_dir + "call_history_sorted.txt")

def dump_xml(element, file_name):
    rough_string = ElementTree.tostring(element, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    pretty_string = reparsed.toprettyxml()
    with open(file_name, 'w') as fd:
        fd.write('<?xml version="1.0"?>\n<!DOCTYPE vcard-listing SYSTEM "vcard-listing.dtd">\n')
        fd.write(pretty_string[23:]) # skip xml declaration

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

    hdrs, card = c.get(src_path, header_list=[headers.Type(mimetype)])
    with open(dest_path, 'wb') as f:
        f.write(card)

def dump_dir(c, src_path, dest_path):
    src_path = src_path.strip("/")

    try:
        os.makedirs(dest_path)
    except OSError as e:
        pass

    src_path_l = src_path.split("/")
    for path in src_path_l[0:-1]:
        c.setpath(path)
    hdrs, cards = c.get(src_path_l[-1], header_list=[headers.Type(b'x-bt/vcard-listing')])
    for i in range(len(src_path_l)-1):
        c.setpath(to_parent=True)


    if len(cards) == 0:
        print("WARNING: %s is empty, skipping", src_path)
        return


    names = []
    root = parse_xml(cards)
    dump_xml(root, "/".join([dest_path, "listing.xml"]))
    for card in root.findall("card"):
        names.append(card.attrib["handle"])

    c.setpath(src_path)

    # get all the files
    for name in names:
        fname = "/".join([dest_path, name])
        try:
            get_file(c, name, fname, folder_name=src_path)
        except OBEXError as e:
            print("Failed to fetch", fname, e)

    # return to the root directory
    depth = len([f for f in src_path.split("/") if len(f)])
    for i in range(depth):
        c.setpath(to_parent=True)

def main():
    prefix = ""

    device_address = modem_mac


    c = PBAPClient(device_address)
    c.connect()

    c.setpath(prefix + "telecom")
    
    get_file(c, "cch.vcf", dest_dir+prefix+"call_history.vcf",
            folder_name=prefix+"telecom", book=True)

    c.disconnect()


    list_of_lists = []

 

    with open(contacts_fetched, 'r') as data, open(contacts_edited, 'w') as outfile:
        name = ''
        number = ''
        if data:
            for line in data:
                if line.startswith('TEL'):
                   number = line.split(':')[1].rstrip()
                   print (number)            
            
                if line.startswith('FN;') or line.startswith('FN:'):
                   name = line.split(':')[1].strip(' ;:\n')
                   print (name)
                   
                   
                if line.startswith('X-IRMC'):
                   direction = line.split(';')[1].split(':')[0]
                   time = line.split(':')[1].strip('\n')
                   
                   print ("%s: %s: %s"%(name, number, direction))

                   export_str = (time + "& " + direction + ": " + number + "; " + name )
                   outfile.write(export_str + "\n")
                   name = number = ''

    print("Done!")
    return 0


def start():
    main()
    
    
    
    
    
    
