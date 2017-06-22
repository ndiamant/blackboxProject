import os


""" downloads index files from balckbox server from startmonth 1, start year throught the last day of endmonth, endyear
	inputs: backboxUserNames as a string
			startyear, startmonth, endyear and endmonth as ints
"""
def downloadIndexFiles(blackboxUserName, startyear, startmonth, endyear, endmonth, pathName):
	#initialize date to beginning of collection period
	year = startyear
	y = str(year)
	month = startmonth
	day = 1

	while month <= 12:
		day = 1
		
		#break at end of data collection period
		if (year == endyear and month > endmonth) or year > endyear:
				break
		

		#put month into form for scp call
		if month < 10:
			m = "0" + str(month)
		else:
			m = str(month)

		numDays = daysIn(month, year)
		while day <= numDays:

			#put day into form for scp call
			if day < 10:
				d = "0" + str(day)
			else:
				d = str(day)

			#construct and make scp call	
			call = "scp " + blackboxUserName + "@white.kent.ac.uk:/data/compile-inputs/index-" + y + "-" + m + "-" + d + " " + pathName
			os.system(call)

			#wrap at end of the year
			if month == 12 and day == 31:
				month = 0
				year += 1
				y = str(year)
			else:
				day += 1

		month += 1


""" returns days in month """
def daysIn(month, year):
	if month == 2 and leapyear(year):
		return 29
	elif month == 2:
		return 28
	elif month in [1,3,5,7,8,10,12]:
		return 31
	else:
		return 30


""" returns 1 if year is leapyear """
def leapyear(year):
	return ((year%4 and not year%100) OR year%400)

			

