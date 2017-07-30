class A:
	
	static_var_A_1=1
	static_var_A_2 = 1
	static_var_A_3=1
	static_var_A_4 = 1
	static_var_A_5=1
	static_var_A_6 = 1

class B(A):
	
	static_var_B_1=1
	static_var_B_2 = 1
	static_var_B_3=1
	static_var_B_4 = 1
	static_var_B_5=1
	static_var_B_6 = 1

class D( A,B ) : 
	
	static_var_C_1=1
	static_var_C_2 = 1
	
	def __init__(self):
		
		self.member_1 = "Non Class Member"
		self.member_2 = A()
		
		self.member_3 = "Non Class Member 2"
		self.member_4 = C()
		
		self.member_5 = "Non Class Member 3"
		self.member_6 = B()

		self.example_function_1()
	
	def example_function_1(self):
		self.example_function_2()

	def example_function_2(self):
		pass
	
class E(A, B, D): 
	
	static_var_C_1=1
	static_var_C_2 = 1
	static_var_C_3=1
	static_var_C_4 = 1
	
	def __init__(self):
		
		self.static_var_C_1=1
		self.static_var_C_2 = 1
		self.static_var_C_1=1
		self.static_var_C_2 = 1

	def example_function_1(self):
		self.example_function_2()

	def example_function_2(self):
		pass
	

class C( A ) : 
	
	static_var_C_1=1
	static_var_C_2 = 1
	static_var_C_3=1
	static_var_C_4 = 1
	
	static_member_1 = E()
	
	def __init__(self):
		
		self.member_1 = E()
		self.member_2 = "Non Class Member"
		
###
