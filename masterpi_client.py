import xmlrpclib
import time
import json

slave_addr = 'http://localhost';
port = 8000;
serv1 = xmlrpclib.ServerProxy(slave_addr + port);


#sample rate: 5Hz
rate = 5.0;
while (True):

    entry_data = poll_all_slaves();
    entry_ts_dict = process_entry_data(entry_data);
    dump_to_json(entry_ts_dict);
    sleep(1/rate);

def poll_all_slaves():
    # Returns long string of newline-separated tag-entry data from all
    # servers.
    return serv1.get_last_10_entries();

def process_entry_data(entry_data):
    entry_dict = dict();

    for entry in entry_data.split('\n'):
        # format: "<tagId> <in/out T/F> <readId> @ <timestamp>"
        tokens = entry.split(' ');
        if (len(tokens) < 5): print("Oh no! tokens format is off!");
        tagId = tokens[0];
        in_out = tokens[1] == "True";
        readId = tokens[2];
        ts = tokens[4];

        if (tagId not in entry_dict):
            # Init a new list for this tag
            entry_dict[tagId] = [];

        entry_dict[tagId] += (in_out, readId, ts);

    return entry_dict;

def dump_to_json(entry_dict):
    with open('data.txt', 'w') as outfile:
        json.dump(entry_dict, outfile);
