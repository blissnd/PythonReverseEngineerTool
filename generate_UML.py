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

def log_progress_percent(class_progress_count, total_num_classes):
	
	progress = int(float(class_progress_count)/float(total_num_classes) * 100)
	print(str(progress) + "%\r"),
	sys.stdout.flush()
	
# End Function
#############################################################

def check_for_static_var(line_pointer, file_buffer, class_list):
	
	global state_machine
	
	if re.match(state_machine.static_var_regex, file_buffer[line_pointer]) and \
								state_machine.is_in_class_list(state_machine.class_instantiation_regex, file_buffer[line_pointer]) == "":
							
		match_result = re.search(state_machine.static_var_regex, file_buffer[line_pointer])
		static_var_name = match_result.group(1)
		
		if re.search(r"#.*", static_var_name):
			return ""
		# End If
		return static_var_name
		
	elif state_machine.is_in_class_list(state_machine.class_instantiation_regex, file_buffer[line_pointer]) != "":
		
		static_var_name = state_machine.check_for_class_instantiation(line_pointer, file_buffer)
		return static_var_name
	# End If
	
	return ""
	
# End Function
#############################################################

def check_for_dynamic_var(line_pointer, file_buffer, class_list):
	
	global state_machine
	
	if re.search(state_machine.dynamic_var_regex, file_buffer[line_pointer]) and \
					state_machine.is_in_class_list(state_machine.class_instantiation_regex, file_buffer[line_pointer]) == "":
		
		match_result = re.search(state_machine.dynamic_var_regex, file_buffer[line_pointer])
		var_name = match_result.group(1)
		
		if re.search(r"#.*", var_name):
			return ""
		# End If		
		return var_name			
		
	elif state_machine.is_in_class_list(state_machine.class_instantiation_regex, file_buffer[line_pointer]) != "":
		
		var_name = state_machine.check_for_class_instantiation(line_pointer, file_buffer)
		return var_name
	# End If
	
	return ""
	
# End Function
#############################################################

def check_for_member_function(line_pointer, file_buffer, class_list):
	
	global state_machine
	
	if re.search(state_machine.member_function_regex, file_buffer[line_pointer]):
		
		match_result = re.search(state_machine.member_function_regex, file_buffer[line_pointer])		
		member_function_name = match_result.group(1)
		
		if re.search(r"#.*", member_function_name):
			return ""
		# End If
		return member_function_name	
	# End If
	
	return ""
	
# End Function
#############################################################

def generate_uml(class_list, uml_output_filename):
	
	global state_machine
	
	file_write_handle = open(uml_output_filename, "w")
	
	file_write_handle.write("digraph hierarchy {\n\n");	
	file_write_handle.write("	edge[dir=both, arrowtail=empty, arrowhead=empty];\n\n");
	file_write_handle.write("subgraph uml {\n");
	file_write_handle.write("	node [shape=box, style=solid, color=black] ");
	
	for class_name in class_list:
		generate_uml_subsets(class_name, class_list)
			
		file_write_handle.write("; ");		
		file_write_handle.write("\"");
		file_write_handle.write(class_name);
		file_write_handle.write("\" ");
		file_write_handle.write("[URL=\"./" + class_name + ".svg\" target=\"_parent\"]")
	# End For	
	file_write_handle.write("	edge[dir=both, minlen=2.00,arrowtail=empty, arrowhead=empty];\n\n");
	
	for class_name in class_list:		
		for base_class in state_machine.class_list[class_name]["inherits_from"]["class_list"]:
			file_write_handle.write("\"" + class_name + "\" -> " + "\"" + base_class + "\"");
			file_write_handle.write(" [shape=circle,label=\"is-a\", arrowhead=onormal,arrowtail=none];\n")
		# End For	
		file_write_handle.write("\n");
	# End For
	
	for class_name in class_list:		
		for contained_class in state_machine.class_list[class_name]["contains"]["class_list"]:
			file_write_handle.write("\"" + class_name + "\" -> " + "\"" + contained_class + "\"");
			file_write_handle.write(" [shape=circle,label=\"has-a\", arrowhead=none,arrowtail=diamond];\n")
		# End For
	# End For
	
	file_write_handle.write("	}\n");
	#file_write_handle.write("label = \"\\n\\nClass Diagram\";\n");
	file_write_handle.write("fontsize=14;\n");
	file_write_handle.write("}\n");
	file_write_handle.close()
	
# End Function
#############################################################

def generate_uml_subsets(class_name, class_list):
	
	global state_machine
	
	child_class_list = []
	containing_class_list = []
	
	for child_class in class_list:
		if class_list[child_class]["inherits_from"]["class_list"] != []:
			if class_name in class_list[child_class]["inherits_from"]["class_list"]:
				child_class_list.append(child_class)
			# End If
		# End If
	# End For
	for containing_class in class_list:
		if class_list[containing_class]["contains"]["class_list"] != []:
			if class_name in class_list[containing_class]["contains"]["class_list"]:
				containing_class_list.append(containing_class)
			# End If
		# End If
	# End For
	sub_graph_output_filename = class_name
	file_write_handle = open("output/" + sub_graph_output_filename, "w")
	
	file_write_handle.write("digraph hierarchy {\n\n");	
	file_write_handle.write("	edge[dir=both, arrowtail=empty, arrowhead=empty];\n\n");
	file_write_handle.write("subgraph uml {\n");
	file_write_handle.write("	node [shape=box, style=solid, color=black] ");
	
	file_write_handle.write("; ");
	file_write_handle.write("\"");
	file_write_handle.write(class_name);
	file_write_handle.write("\" ");
	
	file_write_handle.write("[color=blue, fontcolor=blue, URL=\"./html_output.html#" + class_name + "\" target=\"_parent\"]")
	
	for base_class in state_machine.class_list[class_name]["inherits_from"]["class_list"]:
		file_write_handle.write("; ");
		file_write_handle.write("\"");
		file_write_handle.write(base_class);
		file_write_handle.write("\" ");
		
		if base_class in class_list:
			file_write_handle.write("[URL=\"./" + base_class + ".svg\" target=\"_parent\"]")
	# End For	
	
	for contained_class in state_machine.class_list[class_name]["contains"]["class_list"]:
		file_write_handle.write("; ");
		file_write_handle.write("\"");
		file_write_handle.write(contained_class);
		file_write_handle.write("\" ");
		
		if contained_class in class_list:
			file_write_handle.write("[URL=\"./" + contained_class + ".svg\" target=\"_parent\"]")
	# End For
	
	for child_class in child_class_list:
		file_write_handle.write("; ");
		file_write_handle.write("\"");
		file_write_handle.write(child_class);
		file_write_handle.write("\" ");
		
		if child_class in class_list:
			file_write_handle.write("[URL=\"./" + child_class + ".svg\" target=\"_parent\"]")
	# End For
	
	for containing_class in containing_class_list:
		file_write_handle.write("; ");
		file_write_handle.write("\"");
		file_write_handle.write(containing_class);
		file_write_handle.write("\" ");
		
		if containing_class in class_list:
			file_write_handle.write("[URL=\"./" + containing_class + ".svg\" target=\"_parent\"]")
	# End For
	
	for base_class in state_machine.class_list[class_name]["inherits_from"]["class_list"]:
		file_write_handle.write("\"" + class_name + "\" -> " + "\"" + base_class + "\"");
		file_write_handle.write(" [shape=circle,label=\"is-a\", arrowhead=onormal,arrowtail=none];\n")
	# End For	
	file_write_handle.write("\n");
	
	for contained_class in state_machine.class_list[class_name]["contains"]["class_list"]:
		file_write_handle.write("\"" + class_name + "\" -> " + "\"" + contained_class + "\"");
		file_write_handle.write(" [shape=circle,label=\"has-a\", arrowhead=none,arrowtail=diamond];\n")
	# End For	
	file_write_handle.write("\n");
	
	for child_class in child_class_list:
		file_write_handle.write("\"" + child_class + "\" -> " + "\"" + class_name + "\"");
		file_write_handle.write(" [shape=circle,label=\"is-a\", arrowhead=onormal,arrowtail=none];\n")
	# End For	
	file_write_handle.write("\n");
	
	for containing_class in containing_class_list:
		file_write_handle.write("\"" + containing_class + "\" -> " + "\"" + class_name + "\"");
		file_write_handle.write(" [shape=circle,label=\"has-a\", arrowhead=none,arrowtail=diamond];\n")
	# End For	
	
	file_write_handle.write("	}\n");
	#file_write_handle.write("label = \"\\n\\nClass Diagram\";\n");
	file_write_handle.write("fontsize=14;\n");
	file_write_handle.write("}\n");
	file_write_handle.close()
	
	file_write_handle.close()
	os.system("dot -Tsvg -O " + "output/" + sub_graph_output_filename)
	
# End Function
#############################################################

def print_to_html(class_list, filename):

	file_write_handle = open(filename, "w")
	
	file_write_handle.write("<html>\n")
	file_write_handle.write("<body>\n")
	
	for current_class_key in class_list.keys():		
		file_write_handle.write('Class: <a href="#' + current_class_key + '">' + current_class_key+ '</a><br>')
	# End For
	
	file_write_handle.write('<br>')
	
	for current_class_key in class_list.keys():
						
		file_write_handle.write("<table border=\"2\" padding=\"2\">\n")
		
		file_write_handle.write("<tr>\n")
		
		file_write_handle.write("<th colspan=\"3\" align=\"center\" style=\"background-color: #000000\">")
		
		#file_write_handle.write("<font color=\"white\">Class: " + current_class_key + ", inherits from: " + class_list[current_class_key]['inherits_from'])
		file_write_handle.write("<font color=\"yellow\">Class: " + class_list[current_class_key]['html'] + " : ")
		
		if 'inherits_from' in class_list[current_class_key] and len(class_list[current_class_key]["inherits_from"]["html"]) > 0:
			for base_class in class_list[current_class_key]['inherits_from']['html']:
				
				file_write_handle.write(base_class + " ")
			# End For
		# End If
		
		file_write_handle.write("</th>\n")
		
		file_write_handle.write("</tr>\n")
		
		file_write_handle.write("<tr>\n")
		
		file_write_handle.write("<th align=\"center\"><font color=\"green\">")
		
		file_write_handle.write("Member Functions")
		
		file_write_handle.write("</th>\n")
		
		file_write_handle.write("<th align=\"center\"><font color=\"green\">")
		
		file_write_handle.write("Member Variables")
		
		file_write_handle.write("</th>\n")
		
		file_write_handle.write("<th align=\"center\"><font color=\"green\">")
		
		file_write_handle.write("Static Members")
		
		file_write_handle.write("</th>\n")
		
		file_write_handle.write("</tr>\n")
		
		function_list = []
		var_list = []
		static_list = []
		
		# Convert back to array
		
		for element in class_list[current_class_key]["vars"]["html"].keys():
			
			var_list.append(element)
			
		# End For
		for element in class_list[current_class_key]["functions"]["html"].keys():
			function_name_only = re.match('(.*?)\(', element).group(1)
			html_to_add = '<span id="' + function_name_only + '"> ' + element + '</span>'
			function_list.append(html_to_add)
			
		# End For
		for element in class_list[current_class_key]["statics"]["html"].keys():
			
			static_list.append(element)
			
		# End For
		
		function_list_length = len(function_list)
		var_list_length = len(var_list)
		static_list_length = len(static_list)
		
		function_list_counter = 0
		var_list_counter = 0
		static_list_counter = 0
		
		while (function_list_counter < function_list_length) or (var_list_counter < var_list_length) or (static_list_counter < static_list_length):
			
			file_write_handle.write("<tr>\n")
									
			if function_list_counter < function_list_length:
				
				file_write_handle.write("<td>")
				file_write_handle.write(function_list[function_list_counter])
				file_write_handle.write("</td>\n")
			
			else:
			
				file_write_handle.write("<td></td>")
			
			# End If
			
			if var_list_counter < var_list_length:
				
				file_write_handle.write("<td>")
				file_write_handle.write(var_list[var_list_counter])
				file_write_handle.write("</td>\n")			
			
			else:
			
				file_write_handle.write("<td></td>")
				
			# End If
			
			if static_list_counter < static_list_length:
				
				file_write_handle.write("<td>")
				file_write_handle.write(static_list[static_list_counter])
				file_write_handle.write("</td>\n")
			
			# End If
			
			file_write_handle.write("</tr>\n")
			
			function_list_counter = function_list_counter + 1
			var_list_counter = var_list_counter + 1
			static_list_counter = static_list_counter + 1
			
		# End While
		
		file_write_handle.write("</table>\n")
		file_write_handle.write("<br>\n")
		
	# End While
	
	file_write_handle.write("</body>\n")
	file_write_handle.write("</html>\n")
		
	file_write_handle.close()
	
# End Function
#############################################################

def parse_class_data(filename, class_list):
	
	global state_machine
	
	file_handle = open(filename, "r")
	file_buffer = file_handle.readlines()
	file_handle.close()
	
	line_pointer = 0
	
	while line_pointer <  len(file_buffer):
		state_machine.check_for_class_definition(line_pointer, file_buffer)
		
		if state_machine.STATE_INSIDE_CLASS == 1:
			state_machine.ascertain_indent_level(line_pointer, file_buffer)
		# End If
		
		line_pointer = line_pointer + 1
	# End While
	
# End Function
#############################################################

def parse_basic_data(filename, class_list):
		
		global state_machine
		
		file_handle = open(filename, "r")
		file_buffer = file_handle.readlines()
		file_handle.close()		
		
		line_pointer = 0		
		
		while line_pointer <  len(file_buffer):
			on_class_line = state_machine.check_for_class_definition(line_pointer, file_buffer)
			
			if state_machine.current_class != "":
				state_machine.check_for_class_inheritance(line_pointer, file_buffer)
			
				if on_class_line == "on_class_line":
					state_machine.class_progress_count = state_machine.class_progress_count + 1					
					line_pointer = line_pointer + 1
				# End If
			
				state_machine.check_for_static_section(line_pointer, file_buffer)
				
				if state_machine.STATE_INSIDE_CLASS == 1 and  state_machine.STATE_INSIDE_STATIC_SECTION == 1:					
					var_name = check_for_member_function(line_pointer, file_buffer, state_machine.class_list)

					if var_name != "":							
						state_machine.class_list[state_machine.current_class]["functions"]["html"][var_name] = 1
						line_pointer = line_pointer + 1
						continue
					else:
						static_var_name = check_for_static_var(line_pointer, file_buffer, state_machine.class_list)
						
						if static_var_name != "":								
							state_machine.class_list[state_machine.current_class]["statics"]["html"][static_var_name] = 1
							line_pointer = line_pointer + 1							
							continue						
						# End If
					# End If
				# End If
				if state_machine.STATE_INSIDE_CLASS == 1 and  state_machine.STATE_INSIDE_STATIC_SECTION == 0 and state_machine.STATE_INSIDE_DYNAMIC_SECTION == 1:
					var_name = check_for_member_function(line_pointer, file_buffer, state_machine.class_list)						
					
					if var_name != "":							
						state_machine.class_list[state_machine.current_class]["functions"]["html"][var_name] = 1
						line_pointer = line_pointer + 1
						continue						
					else:						
						var_name = check_for_dynamic_var(line_pointer, file_buffer, state_machine.class_list)					
						
						if var_name != "":
							state_machine.class_list[state_machine.current_class]["vars"]["html"][var_name] = 1
							line_pointer = line_pointer + 1
							continue						
					# End If
				# End If				
			# End If									
			line_pointer = line_pointer + 1
		# End While		
# End Function
#############################################################
#############################################################

if len(sys.argv) <= 1:
	print "No arguments provided"
	exit(0)

state_machine = StateMachine(sys.argv[1])

###################### Parse Class Data ##############################

print "Carrying out pre-parse procedure..."

total_num_python_files = int(os.popen('find "' + state_machine.root_dir_path + '" -name "*.py" | wc -l').read())
current_file_count = 0

for root, dirs, files in os.walk(state_machine.root_dir_path):
	
	for filename in files:
		if filename.endswith(".py") and filename != "parse_dirs.py":
			current_file_count = current_file_count + 1
			print_progress(current_file_count, total_num_python_files)
			file_path =  os.path.join(root, filename)
			parse_class_data(file_path, state_machine.class_list)
			
		# End If
	# End For
# End For

state_machine.total_num_classes = len(state_machine.class_list)

###################### Parse Basic Data ##############################
print "\nCarrying out main procedure..."

class_count = 0
current_file_count = 0

for root, dirs, files in os.walk(state_machine.root_dir_path):
	
	for filename in files:						
		if filename.endswith(".py") and filename != "parse_dirs.py":
			current_file_count = current_file_count + 1
			print_progress(current_file_count, total_num_python_files)
			file_path =  os.path.join(root, filename)
			parse_basic_data(file_path, state_machine.class_list)
		# End If
	# End For
# End For
print
#############################################################
html_output_filename = "output/html_output.html"
print_to_html(state_machine.class_list, html_output_filename)
#os.system("firefox " + html_output_filename + " &")
#############################################################
uml_output_filename = "output/uml_output"
generate_uml(state_machine.class_list, uml_output_filename)
#############################################################
os.system("dot -Tsvg -O " + uml_output_filename)
os.system("firefox " + uml_output_filename + ".svg " +  html_output_filename + " &")
