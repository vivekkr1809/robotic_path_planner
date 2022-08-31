# Results.py
# Author(s): Jessica Flores

"""
Text output class
"""
import numpy as np
import io
from contextlib import redirect_stdout

class Results:
	""" A class to save and print the vertices, parents, costs, and final solution path.	
	"""
	
	def __init__(self, solution):
		"""
		Initializes the Results class.  

		The attributes values are initialized using the solution object passed.

		Note:
			The solution_path and recorder object are assigned to instance attributes with same name.

		Parameters:
			solution(:obj:`~solver.solution.Solution` object): 
				Solution object which holds the recorder object and solution path.

		Attributes:
			solution_path(:obj:`~solver.solution.Solution` attribute): 
				see Solution	

			recorder (:obj:`~solver.recorder.Recorder` object): 
				see Recorder	
				
		Note:
			The output .txt file will be saved in a folder within the output folder named "output_files"
		"""
		self.solution_path = solution.solution_path
		self.recorder = solution.recorder
		self.solution_vertices = []
		self.solution_costs = []
		self.get_solution_vertices()
		self.get_solution_costs()

	def get_solution_vertices(self):
		""" Gets the coordinates of the vertices in the solution path(s)"""
		for idx, solution in enumerate(self.solution_path):
			self.solution_vertices.append([])
			for i in solution:
				if np.isnan(i):
					self.solution_vertices[idx] = [i]
				else:
					self.solution_vertices[idx].append(self.recorder.vertices[i].tolist())

	def get_solution_costs(self):
		""" Gets the total cost for each solution path."""
		for idx, solution in enumerate(self.solution_path):
			self.solution_costs.append(0)
			for i in solution:
				if np.isnan(i):
					self.solution_costs[idx] = i
				else:
					self.solution_costs[idx] += self.recorder.costs[i]

	def save_results(self, name):
		""" Saves the text output results of the algorithm to a .txt file"""
		filename = "./output/output_files/{}.txt".format(name) 
		with open(filename, "w") as f:
			with np.printoptions(precision=3, suppress=True, threshold=np.inf):
			
				# set a trap and redirect stdout
				trap_solution_path = io.StringIO()
				with redirect_stdout(trap_solution_path):
					print("Solution Path(s)\n",*self.solution_path,sep='\n')

				# getting redirected output
				captured_solution_path = trap_solution_path.getvalue()
				print(captured_solution_path, file=f)

				# set a trap and redirect stdout
				trap_solution_vertices = io.StringIO()
				with redirect_stdout(trap_solution_vertices):
					print("\n\nSolution Vertices\n")
					for solution in self.solution_vertices:
						if np.isnan(solution).any():
							print(solution, "\n")
						else:
							print(*solution, sep='\n')
							print("\n")

				# getting redirected output
				captured_solution_vertices = trap_solution_vertices.getvalue()
				print(captured_solution_vertices, file=f)

				# set a trap and redirect stdout
				trap_solution_cost = io.StringIO()
				with redirect_stdout(trap_solution_cost):
					print("\nSolution Cost(s)\n",*self.solution_costs,sep='\n')

				# getting redirected output
				captured_solution_cost = trap_solution_cost.getvalue()
				print(captured_solution_cost, file=f)
				


	def print_results(self):
		""" Prints the text output results of the algorithm"""
		with np.printoptions(precision=3, suppress=True, threshold=np.inf):
			
			# set a trap and redirect stdout
			trap_solution_path = io.StringIO()
			with redirect_stdout(trap_solution_path):
				print("Solution Path(s)\n",*self.solution_path,sep='\n')

			# getting redirected output
			captured_solution_path = trap_solution_path.getvalue()
			print(captured_solution_path)

			# set a trap and redirect stdout
			trap_solution_vertices = io.StringIO()
			with redirect_stdout(trap_solution_vertices):
				print("\n\nSolution Vertices\n")
				for solution in self.solution_vertices:
					if np.isnan(solution).any():
						print(solution, "\n")
					else:
						print(*solution, sep='\n')
						print("\n")

			# getting redirected output
			captured_solution_vertices = trap_solution_vertices.getvalue()
			print(captured_solution_vertices)

			# set a trap and redirect stdout
			trap_solution_cost = io.StringIO()
			with redirect_stdout(trap_solution_cost):
				print("\nSolution Cost(s)\n",*self.solution_costs,sep='\n')

			# getting redirected output
			captured_solution_cost = trap_solution_cost.getvalue()
			print(captured_solution_cost)
			
