import sys
from time import sleep

line_length = 80

def print_progress(_progress, _total):
	
	global line_length
	
	normalised_progress = int((float(_progress) / float(_total)) * float(line_length))
	remaining = line_length - int(normalised_progress)
	
	current_progress_count = 0
	current_remaining_count = 0
	string_to_print = ""
	string_to_print = string_to_print + "||"
	
	while current_progress_count < normalised_progress - 1:
		string_to_print = string_to_print + "="
		current_progress_count = current_progress_count + 1
	# End While
	if current_progress_count < normalised_progress:
		string_to_print = string_to_print + ">"
	# End If
	while current_remaining_count < remaining:
		string_to_print = string_to_print + " "
		current_remaining_count = current_remaining_count + 1
	# End While

	string_to_print = string_to_print + "||\r"
	print string_to_print,
	sys.stdout.flush()
	
# End Function
