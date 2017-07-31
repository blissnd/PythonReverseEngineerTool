

#########################################################
# DATABASE SCHEMA
# class_list[current_class]['html']
# class_list[current_class]["vars"] 
# class_list[current_class]["functions"] 
# class_list[current_class]["statics"] 
# class_list[current_class]["statics"][static_var_name]
# class_list[current_class]["vars"][var_name]
# class_list[current_class]["functions"][var_name]
# class_list[current_class]["inherits_from"]
# class_list[current_class]["CLASS_MEMBER_INDENT_LEVEL"]
# class_list[current_function]["called_functions"]
# class_list[current_function]["FUNCTION_DEF_INDENT_LEVEL"]
#########################################################

import re

class StateMachine:
	
	current_line = ""
	line_pointer = 0
	current_class = ""
	current_function = ""
	class_list = {}
	function_list = {}	
	file_buffer = 0
	total_num_classes = 0
	total_num_functions = 0
	class_progress_count = 0
	function_progress_count = 0
	
	class_regex = 'class .*?([^\s(]+)\s*\(?(.*?)\)?.*:'
	class_instantiation_regex = '([^\s]+).*?\(?(' + 'current_class' + ')\('
	function_invocation_regex = '(' + 'current_function' + ')\('
	class_inheritance_regex = 'class (.*)\((.*?)\).*:'
	function_regex = 'def\s(.*?)\(.*?\)'
	member_function_regex = 'def\s(.*?\(self.*?\))'
	first_char_inside_class_regex = '(.*?)\w'
	outside_class_definition_regex = '^[a-zA-Z]'	
	static_var_regex = '\W*(.*?)\s?='
	dynamic_var_regex = '(self\.[\w\s]+)='
	
	STATE_INSIDE_CLASS = 0
	STATE_INSIDE_STATIC_SECTION = 0
	STATE_INSIDE_DYNAMIC_SECTION = 0
	STATE_INSIDE_FUNCTION = 0
	PARSING_CLASSES = 0
	PARSING_CONTAINMENT_HIERARCHY = 0
	PARING_INHERITANCE_HIERARCHY = 0
	PARING_REGULAR_VARS = 0	
	
	def __init__(self, root_dir_path):
		
		self.root_dir_path = root_dir_path
		
	# End Function
	#############################################################
	
	def initialise_class_dict(self):
		
		self.class_list[self.current_class]['html'] = '<span id="' + self.current_class + '"> ' + self.current_class + '</span>'
		self.class_list[self.current_class]["vars"] = {}
		self.class_list[self.current_class]["functions"] = {}
		self.class_list[self.current_class]["statics"] = {}
		self.class_list[self.current_class]["vars"]["html"] = {}
		self.class_list[self.current_class]["functions"]["html"] = {}
		self.class_list[self.current_class]["statics"]["html"] = {}
		self.class_list[self.current_class]["inherits_from"] = {}
		self.class_list[self.current_class]["contains"] = {}
		self.class_list[self.current_class]["inherits_from"]["html"] = []
		self.class_list[self.current_class]["inherits_from"]["class_list"] = []
		self.class_list[self.current_class]["contains"]["class_list"] = {}
		self.class_list[self.current_class]["CLASS_MEMBER_INDENT_LEVEL"] = None
		
	# End Function
	#############################################################

	def initialise_function_dict(self, line_pointer, file_buffer):
		
		self.function_list[self.current_function]["called_functions"] = []
		self.function_list[self.current_function]["FUNCTION_DEF_INDENT_LEVEL"] = self.get_current_indent_level(line_pointer, file_buffer)
		
	# End Function
	#############################################################
	
	def is_in_class_list(self, regex_string, line_to_check):
	
		for class_name in self.class_list:		
			test_string = regex_string.replace('current_class', class_name)		
			
			if re.search(test_string, line_to_check):		
				match_result = re.search(test_string, line_to_check)			
				return match_result.group(1), match_result.group(2)		
		# End For
		
		return ""
	
	# End Function
	#############################################################

	def is_in_function_list(self, regex_string, line_to_check):
	
		for function_name in self.function_list:		
			test_string = regex_string.replace('current_function', function_name)		
			
			match_result = re.search(test_string, line_to_check)
			
			if match_result:				
				return match_result.group(1)
		# End For
		
		return ""
	
	# End Function
	#############################################################

	def check_for_static_section(self, line_pointer, file_buffer):
		
		if re.match(self.first_char_inside_class_regex, file_buffer[line_pointer]):
			match_result = re.match(self.first_char_inside_class_regex, file_buffer[line_pointer])
			current_indent_level = len(match_result.group(1))
			
			if current_indent_level == self.class_list[self.current_class]["CLASS_MEMBER_INDENT_LEVEL"]:
				self.STATE_INSIDE_STATIC_SECTION = 1
				self.STATE_INSIDE_DYNAMIC_SECTION = 0
			elif current_indent_level > self.class_list[self.current_class]["CLASS_MEMBER_INDENT_LEVEL"]:
				self.STATE_INSIDE_STATIC_SECTION = 0
				self.STATE_INSIDE_DYNAMIC_SECTION = 1
				
	# End Function
	#############################################################
	
	def check_for_class_definition(self, line_pointer, file_buffer):
		
		if re.search(self.class_regex, file_buffer[line_pointer]):
			match_result = re.search(self.class_regex, file_buffer[line_pointer])			
			current_class = match_result.group(1)							
			self.current_class = current_class
			
			if current_class not in self.class_list.keys():
				self.class_list[current_class] = {}
				self.initialise_class_dict()
			# End If
			self.STATE_INSIDE_CLASS = 1
			return "on_class_line"
			
		elif re.search(self.outside_class_definition_regex, file_buffer[line_pointer]):
				self.STATE_INSIDE_CLASS = 0
				self.STATE_INSIDE_STATIC_SECTION = 0
				self.STATE_INSIDE_DYNAMIC_SECTION = 0
				self.current_class = ""
		# End If
		
	# End Function
	#############################################################
	
	def check_for_function_definition(self, line_pointer, file_buffer):
		
		match_result = re.search(self.function_regex, file_buffer[line_pointer])			
		
		if match_result:
			current_function = match_result.group(1)							
			self.current_function = current_function
			
			if self.current_function not in self.function_list.keys():
				self.function_list[self.current_function] = {}				
				self.initialise_function_dict(line_pointer, file_buffer)
			# End If
			self.STATE_INSIDE_FUNCTION = 1			
			return "on_function_line"
		
		elif self.get_current_indent_level(line_pointer, file_buffer) != -1 and \
						self.current_function in self.function_list and \
						"FUNCTION_DEF_INDENT_LEVEL" in self.function_list[self.current_function]:
							
			if self.function_list[self.current_function]["FUNCTION_DEF_INDENT_LEVEL"] >= self.get_current_indent_level(line_pointer, file_buffer):
			
				self.STATE_INSIDE_FUNCTION = 0
				self.current_function = "MAIN"
				
				if self.current_function not in self.function_list.keys():
					self.function_list[self.current_function] = {}				
					self.initialise_function_dict(line_pointer, file_buffer)
				# End If
			# End If
		elif self.current_function == "":
			self.STATE_INSIDE_FUNCTION = 0
			self.current_function = "MAIN"
			
			if self.current_function not in self.function_list.keys():
				self.function_list[self.current_function] = {}				
				self.initialise_function_dict(line_pointer, file_buffer)
			# End If
		# End If

	# End Function
	#############################################################
	
	def check_for_class_inheritance(self, line_pointer, file_buffer):
		try:
			if re.search(self.class_regex, file_buffer[line_pointer]):
				match_result = re.search(self.class_regex, file_buffer[line_pointer])
				current_class = match_result.group(1)
				match_result = re.search(self.class_inheritance_regex, file_buffer[line_pointer])
				base_class_list_string = match_result.group(2)
				base_class_list_string = base_class_list_string.replace(' ', '')
				base_class_list = base_class_list_string.split(",")				
				
				for base_class in base_class_list:
					if base_class in self.class_list:
							self.class_list[current_class]["inherits_from"]["html"].append('<a href="#' + base_class + '"><font color=\"#BBBBFF\">' + base_class + '</a>')
					else:
						self.class_list[current_class]["inherits_from"]["html"].append(base_class + " ")
					# End If
					self.class_list[current_class]["inherits_from"]["class_list"].append(base_class)
				# End For
			# End If
		except AttributeError:
			pass
	
	# End Function
	#############################################################

	def ascertain_indent_level(self, line_pointer, file_buffer):
		
		match_result = re.match(self.first_char_inside_class_regex, file_buffer[line_pointer])
		
		if match_result:
			current_indent_level = len(match_result.group(1))
			
			if self.class_list[self.current_class]["CLASS_MEMBER_INDENT_LEVEL"] == None:
				if current_indent_level > 0:
					self.class_list[self.current_class]["CLASS_MEMBER_INDENT_LEVEL"] = current_indent_level
				# End If
			elif self.class_list[self.current_class]["CLASS_MEMBER_INDENT_LEVEL"] != None:
				if current_indent_level > 0 and current_indent_level < self.class_list[self.current_class]["CLASS_MEMBER_INDENT_LEVEL"] :
					self.class_list[self.current_class]["CLASS_MEMBER_INDENT_LEVEL"] = current_indent_level
				# End If
			# End If
		# End If
		
	# End Function
	#############################################################
	
	def get_current_indent_level(self, line_pointer, file_buffer):
		
		match_result = re.match(self.first_char_inside_class_regex, file_buffer[line_pointer])
		
		if match_result:
			current_indent_level = len(match_result.group(1))			
			return current_indent_level
		else:
			return -1 	# Unknown indent level
		# End If
		
	# End Function
	#############################################################
	
	def check_for_class_instantiation(self, line_pointer, file_buffer):
		
		if self.is_in_class_list(self.class_instantiation_regex, file_buffer[line_pointer]) != "":
			
			var1, base_class_candidate = self.is_in_class_list(self.class_instantiation_regex, file_buffer[line_pointer])		
			var_name_html = var1  + ' <font color=\"#009900\">= Class <a href="#' + base_class_candidate + '">'
			var_name_html = var_name_html +'<font color=\"#0000FF\"> ' + base_class_candidate + '</a>'
			
			self.class_list[self.current_class]["contains"]["class_list"][base_class_candidate] = 1
			
			if re.search(r"#.*", var1):
				return ""
			# End If
			return var_name_html
			# End If
		# End If

	# End Function
	#############################################################

	def check_for_function_invocation(self, line_pointer, file_buffer):
		
		if self.is_in_function_list(self.function_invocation_regex, file_buffer[line_pointer]) != "":
			
			found_function = self.is_in_function_list(self.function_invocation_regex, file_buffer[line_pointer])		
			
			if re.search(r"#.*", found_function):
				return ""
			else:
				return found_function
			# End If
		# End If
		return ""
	# End Function
	#############################################################
	
# End Class
