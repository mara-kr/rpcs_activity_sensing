import sys
import random
import datetime

NUM_CHILDREN = 40
NUM_LOG_STEPS = 200
NUM_INIT_STEPS = 500
NUM_TABLES = 5
TABLE_THRESHOLD = .6
NOT_AT_TABLE = -1
LEAVING = 0
ENTERING = 1
CSV_FORMATTER = "%s,%s,%s,%s\r\n"
TIME_FORMAT = "%m/%d/%Y %H/%M/%S"

# 9:30AM on 3/3/2017
start_time = datetime.datetime(2017, 3, 3, 9, 30, 00);

sim_time = 0;

def log(time, child, station, status):
    time = (start_time + datetime.timedelta(0,time)).strftime(TIME_FORMAT);
    out_file.write(CSV_FORMATTER % (time, child, station, status))


def step(should_log):
    global sim_time
    for i in xrange(NUM_CHILDREN):
        if (random.random() > TABLE_THRESHOLD):
            table = random.randint(0,NUM_TABLES)
            if (children[i] == NOT_AT_TABLE):
                children[i] = table
                if (should_log):
                    log(sim_time, i, table, ENTERING)
            else:
                if (should_log):
                    log(sim_time, i, children[i], LEAVING)
                children[i] = NOT_AT_TABLE
        if (should_log):
            if (i % random.randint(1,3) == 0):
                sim_time += random.randint(1,2)


if (len(sys.argv) < 2):
    print("Usage %s <out_filename>" % sys.argv[0])
    exit()


out_file = open(sys.argv[1], "w")
out_file.write("Time,Child Tag,Station ID,Entering/leaving\r\n")
children = [NOT_AT_TABLE]*NUM_CHILDREN

for i in xrange(NUM_INIT_STEPS):
    step(False)


for i in xrange(NUM_LOG_STEPS):
    step(True)
    sim_time += random.randint(0,3);

out_file.close()
