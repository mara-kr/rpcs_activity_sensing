import datetime

class Tag:
	def __init__(self, tagID, time_stamp, last_seen, action = -1):
		self.tagID = tagID
		self.time_stamp = time_stamp
		self.last_seen = last_seen
		self.action = action # -1 is not set, 1 is entering


# returns the minutes passed
def minsPassed(time1, time2):
	return secondsPassed(tag1, tag2) / 60


# returns the seconds passed
def secondsPassed(time1, time2):
	return abs(float((time1 - time2).total_seconds())) 


def main():
	readerDict = dict()

	while True:

		# TODO: we somehow get tag ID and reader ID from Matt

		time_now = datetime.datetime.now()
		new_tag = Tag(tagID, time_now, time_now)

		if readerID not in readerDict:
			readerDict[readerID] = [new_Tag]

		else:
			tag_seen = false
			for seen_tag in readerDict[readerID]:
				# Tag has already been seen
				if new_tag.tagID == seen_tag.tagID: 
					tag_seen = true

					# If the tag has been seen for over a minute and is constantly being seen
					# Checking to see if a minute has passed filters accidental readings 
					if (minsPassed(seen_tag.time_stamp, new_tag.time_stamp) >= 1 and 
					   secondsPassed(seen_tag.last_seen, new_tag.time_stamp) <= 10):

						# The tag is first entering the station
						if (seen_tag.action != True):
							seen_tag.action = True
							# TODO: WRITE TO FILE ??

						# Update the last seen time 
						seen_tag.last_seen = new_tag.time_stamp
						break

					# Update the last seen time
					seen_tag.last_seen = new_tag.time_stamp
			
			# Tag has not been seen
			if not tag_seen:
				readerDict[readerID].append(new_tag)

			
		# checking for tags that have left the station
		for reader in readerDict:
			for seen_tag in readerDict[reader]:
				time_now = datetime.datetime.now()

				# remove tags that have not been seen in a minute 
				if minsPassed(seen_tag.last_seen, time_now) >= 1:

					# TODO: SEND TO FILE
					readerDict[reader].remove(seen_tag)
