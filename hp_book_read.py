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
user_login = os.getlogin()

bus = dbus.SystemBus()

manager = dbus.Interface(bus.get_object('org.ofono', '/'),
						'org.ofono.Manager')

modems = manager.GetModems()
modem = modems[0][0]


modem_mac= modem.split("_",1)[1].replace("_", ":" )
print("Using modem %s" % modem_mac)	

print("create_dir")
#dest_dir = str("/tmp/" + modem_mac + "/")

dest_dir = str("/home/" + user_login + "/.config/CallControl/" + modem_mac + "/")


os.system('mkdir -p ' + dest_dir)

print(dest_dir)


contacts_fetched = str(dest_dir + "all_contacts.vcf")
contacts_edited = str(dest_dir + "contacts_edited.txt")
contacts_sorted = str(dest_dir + "contacts_sorted.txt")

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

    # since some people may still be holding back progress with Python 2, I'll support
    # them for now and not use the Python 3 exist_ok option :(
    try:
        os.makedirs(dest_path)
    except OSError as e:
        pass

    # Access the list of vcards in the directory
#    hdrs, cards = c.get(src_path, header_list=[headers.Type(b'x-bt/vcard-listing')])
    src_path_l = src_path.split("/")
    for path in src_path_l[0:-1]:
        c.setpath(path)
    hdrs, cards = c.get(src_path_l[-1], header_list=[headers.Type(b'x-bt/vcard-listing')])
    for i in range(len(src_path_l)-1):
        c.setpath(to_parent=True)


    if len(cards) == 0:
        print("WARNING: %s is empty, skipping", src_path)
        return

    # Parse the XML response to the previous request.
    # Extract a list of file names in the directory
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

    # dump the phone book and other folders
#    dump_dir(c, prefix+"telecom/pb", dest_dir+prefix+"telecom/pb")
#    dump_dir(c, prefix+"telecom/ich", dest_dir+prefix+"telecom/ich")
#    dump_dir(c, prefix+"telecom/och", dest_dir+prefix+"telecom/och")
#    dump_dir(c, prefix+"telecom/mch", dest_dir+prefix+"telecom/mch")
#    dump_dir(c, prefix+"telecom/cch", dest_dir+prefix+"telecom/cch")

    # dump the combined vcards
#pobiera listy polaczen: cch to ostatnie polaczenia, pb to  wszytskie kontakty, reszta: nie wiem
#ustawiam pobranie tylko ostatnich polaczen
    c.setpath(prefix + "telecom")
    get_file(c, "pb.vcf", dest_dir+prefix+"all_contacts.vcf",
            folder_name=prefix+"telecom", book=True)
            
#    get_file(c, "ich.vcf", dest_dir+prefix+"ich.vcf",
#            folder_name=prefix+"telecom", book=True)
#    get_file(c, "och.vcf", dest_dir+prefix+"och.vcf",
#            folder_name=prefix+"telecom", book=True)
#    get_file(c, "mch.vcf", dest_dir+prefix+"mch.vcf",
#            folder_name=prefix+"telecom", book=True)
#    get_file(c, "cch.vcf", dest_dir+prefix+"call_history.vcf",
#            folder_name=prefix+"telecom", book=True)

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
                   name = line.split(':')[1].strip(' ;:\n')
             #      print("name")
             #      print(name)
             #      time.sleep(1)
                if name and line.startswith('TEL'):
                   number = line.split(':')[1].rstrip()
             #      print("name_2")
             #      print(name)
             #      print("number_2")
             #      print(number)
             #      time.sleep(1)
                   print ("%s: %s"%(name, number))
                   export_str = name + ": " + number
                   outfile.write(export_str + "\n")
                   name = number = ''
    sorting = (contacts_sorted + ' ' + contacts_edited)
    os.system('sort -o' + sorting)
    # python3 hp_book_read.py 9C:25:95:AD:24:FA /home/maskaz/klient_telefon_python/nOBEX/examples/
    
    
#    list_of_lists = []

#    with open('all_contacts.vcf') as infile, open('contacts_edited.txt', 'w') as outfile:
#        for line in infile:
#            if line.startswith("FN:") or line.startswith("TEL;HOME:"):
#                line_mod = line.replace("FN:", "").replace("TEL;HOME:", "")
#                outfile.write(line_mod)
#                print(line_mod)


#    with open('contacts_edited.txt', 'r') as f:
#        lines = f.read().splitlines()

#    res = [' '.join(lines[i: i+2]) for i in range(0, len(lines), 2)]
#    print(res)
#    with open('contacts_edited_s.txt', 'w') as outfile:
#         outfile.write('\n'.join(res))

    print("Done!")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
