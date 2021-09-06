import os
import shutil
import sys
import tkinter as tk
import tkinter.font as tkFont
from tkinter import filedialog
from tkinter import *
from PIL import Image
from PIL.ExifTags import TAGS
import pytz
import datetime
from win32com.propsys import propsys, pscon


root = Tk()

source_folder = ""
destination_folder = ""

SOURCE_CHOSEN = False
DESTINATION_CHOSEN = False

##BACKEND##
def get_iamges_in_dir(source_folder):
	BACK_SLASH = "/"
	files = os.listdir(source_folder)
	outputList = list()
	for file in files:
		if is_image(file) is True:
			path_to_image = source_folder + BACK_SLASH + file 
			outputList.append(path_to_image)
	return outputList

def is_image(fileName):
	fileName = fileName.split(".")
	file_extension_index = len(fileName) - 1
	ACCEPTED_EXTENSIONS = ["jpg","JPG","jpeg","JPEG","png","PNG","mp4","MP4","mov","MOV","wmv","WMW","avi","AVI"]
	
	for extension in ACCEPTED_EXTENSIONS:
		if(fileName[file_extension_index] == extension):
			return True
	return False

def get_dates(inputImageList):
	BACK_SLASH = "\\"
	date_time_tag = 36867
	outputList = list()
	CHECK_APPEND = False
	VIDEO = False
	path_to_image = ""
	for picture in inputImageList:
		path_split = picture.split("/")
		path_to_image = ""
		counter = 0
		for item in path_split:
			counter += 1 
			path_to_image += item
			if counter != len(path_split):
				path_to_image += BACK_SLASH

		CHECK_APPEND = False
		try:
			image = Image.open(path_to_image)
			VIDEO = False
		except:
			VIDEO = True
			try:
				properties = propsys.SHGetPropertyStoreFromParsingName(path_to_image)
				datetime = properties.GetValue(pscon.PKEY_Media_DateEncoded).GetValue()
				datetime = str(datetime)
				outputList.append(extract_date_video(datetime))
			except:
				outputList.append(extract_date("1990:01:01 01:01:00"))
		if VIDEO == False:
			for tag, value in image._getexif().items():
				if(tag == date_time_tag):
					outputList.append(extract_date(value))
					CHECK_APPEND = True
			if(CHECK_APPEND == False):
				outputList.append(extract_date("1990:01:01 01:01:00"))
		VIDEO = False
	if len(inputImageList) == len(outputList):
		return outputList
	print("LENGTH ERROR")
	return False
				

def extract_date(inputString):
	inputString = inputString.split()
	splitString = inputString[0].split(":")

	day = int(splitString[2])
	month = int(splitString[1])
	year = int(splitString[0])
	return [day,month,year]

def extract_date_video(inputString):
	inputString = inputString.split()
	splitString = inputString[0].split("-")

	day = int(splitString[2])
	month = int(splitString[1])
	year = int(splitString[0])
	return [day,month,year]

def get_year_ranges(dates_list):
	year_index = 2
	year_list = list()
	min_year = 0
	max_year = 0
	for date in dates_list:
		year_list.append(date[year_index])

	try:	
		min_year = min(year_list)
	except:
		min_year = 1990
	try:
		max_year = max(year_list)
	except:
		max_year = 2070
	print("year ranges",[min_year,max_year])
	return [min_year,max_year]


def sort_images(images,dates,OUTPUT_FOLDER):
	BACK_SLASH = "/"
	YEAR_RANGE_MIN = get_year_ranges(dates)[0]
	YEAR_RANGE_MAX = get_year_ranges(dates)[1]

	DAY_RANGE_MIN = 1 
	DAY_RANGE_MAX = 31

	DATE_YEAR_INDEX = 2
	DATE_MONTH_INDEX = 1
	DATE_DAY_INDEX = 0

	MONTHS_LIST = ["1. Leden","2. Únor","3. Březen","4. Duben","5. Květen","6. Červen","7. Červenec","8. Srpen","9. Září","10. Říjen","11. Listopad","12. Prosinec"]

	try:
		os.mkdir(OUTPUT_FOLDER)
	except:
		pass
	for year in range(YEAR_RANGE_MIN,YEAR_RANGE_MAX+1):
		for month in range(len(MONTHS_LIST)):
			for day in range(DAY_RANGE_MIN,DAY_RANGE_MAX+1):
				for image in range(len(images)):
					if dates[image][DATE_YEAR_INDEX] == year:
						if dates[image][DATE_MONTH_INDEX] == month+1:
							if dates[image][DATE_DAY_INDEX] == day:
								yearString = str(year)
								monthString = MONTHS_LIST[month]
								dayString = str(day) + "."
								imageNameOnlySplit = images[image].split("/")
								imageNameOnly = imageNameOnlySplit[len(imageNameOnlySplit)-1]
								print("only",imageNameOnly)
								destination = OUTPUT_FOLDER + BACK_SLASH + yearString + BACK_SLASH + monthString + BACK_SLASH + dayString + BACK_SLASH + imageNameOnly
								if year != 1990:
									try:
										path = OUTPUT_FOLDER + BACK_SLASH + yearString
										os.mkdir(path)
									except:
										pass
									try:
										path = OUTPUT_FOLDER + BACK_SLASH + yearString + BACK_SLASH + monthString
										os.mkdir(path)
									except:
										pass
									try:
										path = OUTPUT_FOLDER + BACK_SLASH + yearString + BACK_SLASH + monthString + BACK_SLASH + dayString
										os.mkdir(path)
									except:
										pass
									shutil.copyfile(images[image], destination)	
								else:
									try:
										path = OUTPUT_FOLDER + BACK_SLASH + "NEZAŘAZENO"
										print(destination)
										destination = path + BACK_SLASH + imageNameOnly
										print(destination)
										os.mkdir(path)
									except:
										pass
									shutil.copyfile(images[image],destination)
				root.update()
####GUI###

def source_button_command():
	global SOURCE_CHOSEN
	global DESTINATION_CHOSEN
	global source_folder
	global destination_folder
	print("Select source")
	source_folder = filedialog.askdirectory()
	if source_folder != "":
		 source_path_label["text"] = source_folder
		 not_chosen_source_label["text"] = "chosen"
		 not_chosen_source_label["fg"] = "#20E125"
		 status_label["text"] = ""
		 SOURCE_CHOSEN = True
	else:
		source_path_label["text"] = ""
		not_chosen_source_label["text"] = "not chosen"
		not_chosen_source_label["fg"] = "#000000"
		status_label["text"] = ""
		SOURCE_CHOSEN = False


def destination_button_command():
	global SOURCE_CHOSEN
	global DESTINATION_CHOSEN
	global destination_folder
	global source_folder
	print("Select destination")
	destination_folder = filedialog.askdirectory()
	if destination_folder != "":
		 destination_path_label["text"] = destination_folder
		 not_chosen_destination_label["text"] = "chosen"
		 not_chosen_destination_label["fg"] = "#20E125"
		 status_label["text"] = ""
		 DESTINATION_CHOSEN = True
	else:
		destination_path_label["text"] = ""
		not_chosen_destination_label["text"] = "not chosen"
		not_chosen_destination_label["fg"] = "#000000"
		status_label["text"] = ""
		DESTINATION_CHOSEN = False							

def sort_button_command():
	print("SORT PHOTOS")
	print(SOURCE_CHOSEN)
	print(DESTINATION_CHOSEN)
	if SOURCE_CHOSEN and DESTINATION_CHOSEN:
		print("chosen")
		status_label["text"] = "sorting..."
		root.update()
		images = get_iamges_in_dir(source_folder)
		dates = get_dates(images)
		print(images)
		sort_images(images,dates,destination_folder)
		status_label["text"] = "finished"

	else:
		print("not chosen")
		not_chosen_destination_label["text"] = "not chosen"
		not_chosen_source_label["text"] = "not chosen"
		not_chosen_destination_label["fg"] = "#FF0000"
		not_chosen_source_label["fg"] = "#FF0000"


root.title("Photo Sorter (by Kuba)")
width=650
height=350
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
root.geometry(alignstr)
root.resizable(width=False, height=False)

title_label=tk.Label(root)
ft = tkFont.Font(family='Arial',size=48)
title_label["font"] = ft
title_label["fg"] = "#333333"
title_label["justify"] = "center"
title_label["text"] = "Photo Sorter"
title_label.place(relx = 0.5,rely = 0.15,anchor = 'center')

source_folder_label=tk.Label(root)
ft = tkFont.Font(family='Arial',size=10)
source_folder_label["font"] = ft
source_folder_label["fg"] = "#333333"
source_folder_label["justify"] = "left"
source_folder_label["text"] = "Source Folder:"
source_folder_label.place(relx = 0.15,rely = 0.3,anchor ='w')

destination_folder_label=tk.Label(root)
ft = tkFont.Font(family='Arial',size=10)
destination_folder_label["font"] = ft
destination_folder_label["fg"] = "#333333"
destination_folder_label["justify"] = "left"
destination_folder_label["text"] = "Destination Folder:"
destination_folder_label.place(relx = 0.85, rely = 0.3,anchor ='e')

not_chosen_source_label=tk.Label(root)
ft = tkFont.Font(family='Arial',size=10)
not_chosen_source_label["font"] = ft
not_chosen_source_label["fg"] = "#333333"
not_chosen_source_label["justify"] = "left"
not_chosen_source_label["text"] = "not chosen"
not_chosen_source_label.place(relx = 0.15,rely = 0.4,anchor ='w')
SOURCE_CHOSEN = False

not_chosen_destination_label=tk.Label(root)
ft = tkFont.Font(family='Arial',size=10)
not_chosen_destination_label["font"] = ft
not_chosen_destination_label["fg"] = "#333333"
not_chosen_destination_label["justify"] = "left"
not_chosen_destination_label["text"] = "not chosen"
not_chosen_destination_label.place(relx = 0.85, rely = 0.4,anchor ='e')
DESTINATION_CHOSEN = False

source_button=tk.Button(root)
source_button["bg"] = "#efefef"
ft = tkFont.Font(family='Arial',size=10)
source_button["font"] = ft
source_button["fg"] = "#000000"
source_button["justify"] = "center"
source_button["text"] = "Choose source"
source_button.place(relx = 0.15,rely = 0.5,anchor ='w')
source_button["command"] = source_button_command

destination_button=tk.Button(root)
destination_button["bg"] = "#efefef"
ft = tkFont.Font(family='Arial',size=10)
destination_button["font"] = ft
destination_button["fg"] = "#000000"
destination_button["justify"] = "center"
destination_button["text"] = "Choose destination"
destination_button.place(relx = 0.85, rely = 0.5,anchor ='e')
destination_button["command"] = destination_button_command

source_path_label=tk.Label(root)
ft = tkFont.Font(family='Arial',size=10)
source_path_label["font"] = ft
source_path_label["fg"] = "#333333"
source_path_label["justify"] = "left"
source_path_label["text"] = ""
source_path_label.place(relx = 0.15,rely = 0.6,anchor ='w')

destination_path_label=tk.Label(root)
ft = tkFont.Font(family='Arial',size=10)
destination_path_label["font"] = ft
destination_path_label["fg"] = "#333333"
destination_path_label["justify"] = "right"
destination_path_label["text"] = ""
destination_path_label.place(relx = 0.85, rely = 0.65,anchor ='e')

status_label=tk.Label(root)
ft = tkFont.Font(family='Arial',size=10)
status_label["font"] = ft
status_label["fg"] = "#333333"
status_label["justify"] = "center"
status_label["text"] = ""
status_label.place(relx = 0.5, rely = 0.5,anchor ='center')

sort_button=tk.Button(root)
sort_button["bg"] = "#efefef"
ft = tkFont.Font(family='Arial',size=24)
sort_button["font"] = ft
sort_button["fg"] = "#000000"
sort_button["justify"] = "center"
sort_button["text"] = "SORT PHOTOS"
sort_button.place(relx = 0.5, rely = 0.8,anchor ='center')
sort_button["command"] = sort_button_command



root.mainloop()









