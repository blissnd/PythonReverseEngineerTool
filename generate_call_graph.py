MIT License

Copyright (c) 2017 Nathan D Bliss

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
#############################################################

import re
import os
import sys

from progress_bar import *
from StateMachine import *

#############################################################

def log_progress():
	
	print "#",
	sys.stdout.flush()
	
# End Function
#############################################################

def generate_function_list_html(function_list, call_graph_output_filename):
	
	global state_machine
	
	file_write_handle = open(call_graph_output_filename + ".html", "w")	
	file_write_handle.write("<html>\n")
	file_write_handle.write("<body>\n")
	
	for function_name in function_list:
		file_write_handle.write('Function: <a href="#' + current_class_key + '">' + current_class_key+ '</a><br>')
	# End For		
	
	file_write_handle.write("</body>\n")
	file_write_handle.write("</html>\n")	
	file_write_handle.close()
# End Function
#############################################################

def generate_call_graph(function_list, call_graph_output_filename):
	
	global state_machine
	
	file_write_handle = open(call_graph_output_filename, "w")
	
	file_write_handle.write("digraph hierarchy {\n\n");	
	file_write_handle.write("	edge[dir=both, arrowtail=empty, arrowhead=empty];\n\n");
	file_write_handle.write("subgraph uml {\n");
	file_write_handle.write("	node [shape=box, style=solid, color=black] ");
	
	for function_name in function_list:
		generate_call_graph_subset(function_name, function_list)
		
		file_write_handle.write("; ");		
		file_write_handle.write("\"");
		file_write_handle.write(function_name);
		file_write_handle.write("\" ");
		file_write_handle.write("[URL=\"./" + function_name + ".svg\" target=\"_parent\"]")
	# End For	
	file_write_handle.write("	edge[dir=both, minlen=2.00,arrowtail=empty, arrowhead=empty];\n\n");
	
	for function_name in function_list:
		if state_machine.function_list[function_name]["called_functions"] != []:
			for called_function in state_machine.function_list[function_name]["called_functions"]:
				file_write_handle.write("\"" + function_name + "\" -> " + "\"" + called_function + "\"");
				file_write_handle.write(" [shape=circle, arrowhead=onormal,arrowtail=none];\n")
			# End For	
			file_write_handle.write("\n");
		# End If
	# End For
	
	file_write_handle.write("	}\n");
	#file_write_handle.write("label = \"\\n\\nCall Graph\";\n");
	file_write_handle.write("fontsize=14;\n");
	file_write_handle.write("}\n");
	file_write_handle.close()
	
# End Function
#############################################################

def generate_call_graph_subset(function_name, function_list):
	
	global state_machine
	
	calling_function_list = []
	
	for called_by_function_name in function_list:
		if function_list[called_by_function_name]["called_functions"] != []:
			if function_name in function_list[called_by_function_name]["called_functions"]:
				calling_function_list.append(called_by_function_name)
			# End If
		# End If
	# End For
	sub_graph_output_filename = function_name
	file_write_handle = open("output/" + sub_graph_output_filename, "w")
	
	file_write_handle.write("digraph hierarchy {\n\n");	
	file_write_handle.write("	edge[dir=both, arrowtail=empty, arrowhead=empty];\n\n");
	file_write_handle.write("subgraph uml {\n");
	file_write_handle.write("	node [shape=box, style=solid, color=black] ");
	
	file_write_handle.write("; ");
	file_write_handle.write("\"");
	file_write_handle.write(function_name);
	file_write_handle.write("\" ");
	file_write_handle.write("[color=blue, fontcolor=blue, URL=\"./html_output.html#" + function_name + "\" target=\"_parent\"]")
	
	for called_function in  function_list[function_name]["called_functions"]:		
		file_write_handle.write("; ");
		file_write_handle.write("\"");
		file_write_handle.write(called_function);
		file_write_handle.write("\" ");
		file_write_handle.write("[URL=\"./" + called_function + ".svg\" target=\"_parent\"]")
	# End For
	
	for calling_function in calling_function_list:
		file_write_handle.write("; ");		
		file_write_handle.write("\"");
		file_write_handle.write(calling_function);
		file_write_handle.write("\" ");
		file_write_handle.write("[URL=\"./" + calling_function + ".svg\" target=\"_parent\"]")
	# End For
	file_write_handle.write("	edge[dir=both, minlen=2.00,arrowtail=empty, arrowhead=empty];\n\n");
			
	if state_machine.function_list[function_name]["called_functions"] != []:
		for called_function in state_machine.function_list[function_name]["called_functions"]:
			file_write_handle.write("\"" + function_name + "\" -> " + "\"" + called_function + "\"");
			file_write_handle.write(" [shape=circle, arrowhead=onormal,arrowtail=none];\n")
		# End For	
		file_write_handle.write("\n");					
	# End If
	
	if calling_function_list != []:
		for calling_function in calling_function_list:
			file_write_handle.write("\"" + calling_function + "\" -> " + "\"" + function_name + "\"");
			file_write_handle.write(" [shape=circle, arrowhead=onormal,arrowtail=none];\n")
		# End For	
		file_write_handle.write("\n");					
	# End If
	
	file_write_handle.write("	}\n");
	#file_write_handle.write("label = \"\\n\\nCall Graph\";\n");
	file_write_handle.write("fontsize=14;\n");
	file_write_handle.write("}\n");
	
	file_write_handle.close()
	os.system("dot -Tsvg -O " + "output/" + sub_graph_output_filename)

# End Function
#############################################################

def log_progress_percent(function_progress_count, total_num_functions):
	
	progress = int(float(function_progress_count)/float(total_num_functions) * 100)
	print(str(progress) + "%\r"),
	sys.stdout.flush()
	
# End Function
#############################################################

def parse_function_def_data(filename, function_list):
	
	global state_machine
	
	file_handle = open(filename, "r")
	file_buffer = file_handle.readlines()
	file_handle.close()
	
	line_pointer = 0
	
	while line_pointer <  len(file_buffer):
		on_function_def_line = state_machine.check_for_function_definition(line_pointer, file_buffer)
		
		if on_function_def_line == "on_function_line":
			state_machine.function_list[state_machine.current_function]["FUNCTION_DEF_INDENT_LEVEL"] = state_machine.get_current_indent_level(line_pointer, file_buffer)
		# End If
		line_pointer = line_pointer + 1
	# End While
	
# End Function
#############################################################
def map_function_data (filename, function_list):

	global state_machine
	
	file_handle = open(filename, "r")
	file_buffer = file_handle.readlines()
	file_handle.close()
	
	line_pointer = 0
	
	while line_pointer <  len(file_buffer):
		on_function_def_line = state_machine.check_for_function_definition(line_pointer, file_buffer)
		
		if on_function_def_line == "on_function_line":
			state_machine.function_progress_count = state_machine.function_progress_count + 1								
		else:
			found_function = state_machine.check_for_function_invocation(line_pointer, file_buffer)
			
			if (found_function != "") and (found_function not in state_machine.function_list[state_machine.current_function]["called_functions"]):
				state_machine.function_list[state_machine.current_function]["called_functions"].append(found_function)
			# End If
		# End If
		line_pointer = line_pointer + 1
	# End While
	
# End Function
#############################################################

#############################################################
#############################################################

if len(sys.argv) <= 1:
	print "No arguments provided"
	exit(0)

state_machine = StateMachine(sys.argv[1])

###################### Parse All Function Definitions #####################
print "Parsing function definitions..."

total_num_python_files = int(os.popen('find "' + state_machine.root_dir_path + '" -name "*.py" | wc -l').read())
current_file_count = 0
print state_machine.root_dir_path
for root, dirs, files in os.walk(state_machine.root_dir_path):
	
	for filename in files:
		state_machine.current_function = ""
		
		if filename.endswith(".py") and filename != "parse_dirs.py":
			current_file_count = current_file_count + 1
			print_progress(current_file_count, total_num_python_files)
			file_path =  os.path.join(root, filename)
			parse_function_def_data(file_path, state_machine.function_list)
			
		# End If
	# End For
# End For

state_machine.total_num_functions = len(state_machine.function_list)

################### Map function calls to function dict #####################
print "\nCarrying out main procedure..."

class_count = 0
current_file_count = 0

for root, dirs, files in os.walk(state_machine.root_dir_path):
	
	for filename in files:
		state_machine.current_function = ""
		
		if filename.endswith(".py") and filename != "parse_dirs.py":
			current_file_count = current_file_count + 1
			print_progress(current_file_count, total_num_python_files)
			file_path =  os.path.join(root, filename)
			map_function_data(file_path, state_machine.function_list)
		# End If
	# End For
# End For
print

#############################################################

call_graph_output_filename = "output/call_graph"
generate_call_graph(state_machine.function_list, call_graph_output_filename)
os.system("dot -Tsvg -O " + call_graph_output_filename)
os.system("firefox " + call_graph_output_filename + ".svg " + " &")

