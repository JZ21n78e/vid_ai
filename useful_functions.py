import mutagen
from mutagen.mp3 import MP3

# function to convert the information into
# some readable format
def audio_duration(length):
	hours = length // 3600 # calculate in hours
	length %= 3600
	mins = length // 60 # calculate in minutes
	length %= 60
	seconds = length # calculate in seconds

	return hours, mins, seconds # returns the duration

# Create a WAVE object
# Specify the directory address of your wavpack file
# "alarm.wav" is the name of the audiofile
audio = MP3(r"C:\Users\ADMINI~1\AppData\Local\Temp\speech_3.mp3")

# contains all the metadata about the wavpack file
audio_info = audio.info
length = int(audio_info.length)
hours, mins, seconds = audio_duration(length)
print('Total Duration: {}:{}:{}'.format(hours, mins, seconds))
