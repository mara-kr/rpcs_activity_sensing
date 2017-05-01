f = open('/home/pi/data/master_filtered.csv', 'r')

seen_tags = dict()
seen_readers = dict()
next_reader_id = 'A'
next_tag_id = '1'

for line in f:
    line = line.strip().split(',')
    if (line[0] not in seen_readers):
        seen_readers[line[0]] = next_reader_id
        next_reader_id = chr(ord(next_reader_id) + 1)
    reader = seen_readers[line[0]]
    if (line[1] not in seen_tags):
        seen_tags[line[1]] = next_tag_id
        next_tag_id= chr(ord(next_tag_id) + 1)
    tag = seen_tags[line[1]]
    if (line[3] == '1'):
        status = "entering"
    else:
        status = "leaving "
    print("{} {} {} at {}".format(tag, status, reader, line[2]))
