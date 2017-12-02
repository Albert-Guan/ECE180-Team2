import re;
import datetime
from datetime import timedelta
from collections import defaultdict;

# index 0 -> course number
# index 1 -> section number: some may not have(like some lectures)
# index 2 -> class type ("LE","LA","DI","SE"...)
# index 3 -> section (A01, A02 ...)
# index 4 -> day (Mo, Tu, Wed...)
# index 5 -> time period (10.00a - 10:50a)
# index 6 -> building (APM,YORK,...)
# index 7 -> room number
# index 8 -> number of students(12, 34 ....)
# print line;

attributes = "CourseNum,SectionID,ClassType,Section,Day,Time,Building,Room,StudentsNumber\n"
foldername = "./csvData/"
geofoldername = "./geospatialData/"
term = "FA17"
filename = foldername+term+"-cleaned.csv";
temp_filename = "temp_data.csv"
res_filename = "geospatial.csv"

day_pattern = re.compile("^M|W|F|Th|Tu")

outfile = open(temp_filename, "w");

building_locations = {
	'WFH' 	: (32.886956, -117.241839),
	'MNDLR' : (32.879312, -117.242139),
	'UREY' 	: (32.875569, -117.241055),
	'NIERN' : (32.868487, -117.251196),
	'ECON' 	: (32.875323, -117.235500),
	'MCC' 	: (32.881560, -117.240280),
	'CICC' 	: (32.885032, -117.241292),
	'WLH' 	: (32.880558, -117.234319),
	'MCGIL' : (32.879049, -117.242043),
	'RECGM' : (32.876838, -117.241279),
	'CALIT' : (32.882629, -117.234578),
	'OAR' 	: (32.869700, -117.250649),
	'IGPP' 	: (32.868349, -117.252952),
	'SME' 	: (32.879890, -117.233139),
	'MAYER' : (32.875322, -117.240190),
	'SSRB' 	: (32.880687, -117.240153),
	'STCTR' : (32.879867, -117.233163),
	'BIO' 	: (32.876028, -117.242219),
	'OTRSN' : (32.886620, -117.241109),
	'SEQUO' : (32.882173, -117.240561),
	'LFFB' 	: (32.876682, -117.236868),
	'PCYNH' : (32.878422, -117.233767),
	'EBU3B'	: (32.881835, -117.233523),
	'CENTR' : (32.877773, -117.237262),
	'NSB' 	: (32.875274, -117.242808),
	'VAUGN'	: (32.865324, -117.252961),
	'SERF' 	: (32.879664, -117.235105),
	'HSS' 	: (32.878391, -117.241665),
	'LASB' 	: (32.885595, -117.241442),
	'BONN' 	: (32.875415, -117.240332),
	'RBC' 	: (32.884341, -117.240977),
	'CCC' 	: (32.879661, -117.236447),
	'PETER' : (32.880013, -117.240351),
	'BSB' 	: (32.875597, -117.236066),
	'TMCA' 	: (32.881417, -117.241052),
	'ASANT' : (32.884082, -117.241912),
	'VAF' 	: (32.879180, -117.234138),
	'CMME' 	: (32.875561, -117.235448),
	'LEDDN' : (32.878867, -117.241695),
	'CSB' 	: (32.880547, -117.239444),
	'MANDE' : (32.877866, -117.239432),
	'HUBBS' : (32.867457, -117.253423),
	'YORK'	: (32.874554, -117.240005),
	'CPMC' 	: (32.877962, -117.234429),
	'BRF2' 	: (32.874480, -117.234951),
	'MTF' 	: (32.875608, -117.235497),
	'GH' 	: (32.873717, -117.240975),
	'EBU2' 	: (32.881243, -117.233615),
	'LIT' 	: (32.880495, -117.233850),
	'EBU1' 	: (32.881659, -117.235623),
	'PACIF' : (32.876030, -117.242393),
	'PRICE' : (32.879733, -117.236191),
	'MET' 	: (32.875344, -117.234821),
	'PFBH' 	: (32.881568, -117.234351),
	'SPIES' : (32.869081, -117.251015),
	'DANCE' : (32.871733, -117.240190),
	'SOLIS' : (32.880931, -117.239798),
	'TM102' : (32.881485, -117.239680),
	'APM' 	: (32.879039, -117.241028),
	'ERCA' 	: (32.886146, -117.242029),
	'RVCOM' : (32.874702, -117.241985),
	'MYR-A' : (32.875268, -117.240194),
	'SSB' 	: (32.883965, -117.240439),
	'POTKR'	: (32.871346, -117.240710),
	'RITTR'	: (32.865266, -117.253470),
	'KECK'	: (32.875101, -117.236281),
	'CCS'	: (32.866367, -117.253971),
	'PSB'	: (32.874227, -117.235699),
	'ECKRT'	: (32.867160, -117.252589),
	'SCRB'	: (32.867160, -117.252589),
	'CTF'	: (32.756219, -117.165294)
}

def convertListToCSV(li):
	assert isinstance(li, list);
	res = "";
	for ele in li:
		res += str(ele) + ","
	return res[:-1];

def getDateTime(time):
	assert isinstance(time, str);
	res = datetime.datetime(*([1990] + [1] * 6));
	curr = datetime.datetime.strptime(time[:-1], '%H:%M').time();
	if time[-1] == 'p' and time[:2] != "12":
		curr = datetime.time(curr.hour + 12, curr.minute);
	return res.replace(hour = curr.hour, minute = curr.minute);
		 

def convertTimeToList(time, period_minutes = 10):
	assert isinstance(time, str);
	assert isinstance(period_minutes, int);
	print time;
	start = time.split("-")[0];
	end = time.split("-")[1];
	start_datetime = getDateTime(start);
	end_datetime = getDateTime(end);
	res = [];
	while start_datetime < end_datetime:
		res.append(start_datetime.strftime('%H'));
		start_datetime += timedelta(minutes = period_minutes);
	return res;

rooms_num = defaultdict(lambda : 0);
unknown_building = set();

with open(filename, "r") as f:
	print f.readline();
	for line in f:
		# separate it by day:
		element_list = line.split(",");
		if element_list[6] not in building_locations: 
			unknown_building.add(element_list[6]);
		for day in re.findall(day_pattern, element_list[4]):
			for time in convertTimeToList(element_list[5]):
				tup = (element_list[6],element_list[7],day,time);
				rooms_num[tup] = max(rooms_num[tup], int(element_list[-1]));
				newLine = convertListToCSV(element_list[:4]) + ","+day+","+time+","+ convertListToCSV(element_list[6:]);
				outfile.write(newLine)
outfile.close();
# print rooms_num;
print unknown_building;
building_num = defaultdict(lambda : 0);
for key in rooms_num:
	building_num[(key[0], key[2], key[3])] += rooms_num[key];


# resfile = open(geofoldername+term+"-"+res_filename, "w");
# attributes = "building_tag,longitude,latitude,day,hour,students_number\n";
# resfile.write(attributes);
# for key in building_num:
# 	line = key[0] + "," + (str(building_locations[key[0]][0])+
# 			"," + str(building_locations[key[0]][1])+
# 			"," + str(key[1]) + "," + str(key[2]) + "," + str(building_num[key]));
# 	print line;
# 	resfile.write(line+"\n");
# resfile.close();