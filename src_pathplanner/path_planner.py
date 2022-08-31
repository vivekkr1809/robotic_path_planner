# path_planner.py
# Author(s): Edvard Bruun, Vivek Kumar, Jessica Flores

"""
The core module to execute the program

The user to specify the location of the input file in the :meth:`~path_planner.run_program()` function.

Imports the :class:`~input.parse_data_class.ParseDataJSON` class

Imports the :class:`~input.domain.Domain` class

Imports the :class:`~solver.solution.Solution` class

Imports the :class:`~output.results.Results` class

Imports the :class:`~output.plot.Plot` class

"""
# Python imports
from __future__ import print_function
import sys
import time
import re

# Import inputs
from input.parse_data_class import ParseDataJSON
from input.domain_class import Domain
from solver.solution import Solution
from output.results import Results
from output.plot import Plot

def run_program():
	"""
	Steps in program::

		Step 1. Read parameters file (user-specified)
		Step 2. Create problem domain
		Step 3. Execute path planning algorithm
		Step 4. Print results to screen, save text file
		Step 5. Create results plot

	Function Code::
		
		# Step 1. 
		input_file = "./input/rrt_input_file.json"
		program_input = ParseDataJSON(input_file)
		program_input.parse_data()

		domain_info = program_input.data_dict["DomainInfo"]
		origin_goal_info = program_input.data_dict["OriginGoalInfo"]
		obstacles_info = program_input.data_dict["ObstaclesInfo"]
		rrt_algorithm_info = program_input.data_dict["RRTAlgorithmInfo"]
		
		# Step 2. 
		domain_object = Domain(domain_info, obstacles_info, origin_goal_info)

		# Step 3. 
		PathPlan = Solution(rrt_algorithm_info,domain_object)
		PathPlan.run_algorithm()
		PathPlan.process_vertex_list()

		# Step 4.
		results_object = Results(PathPlan)
		results_object.print_results()
		results_object.save_results()

		# Step 5.
		plot_object = Plot("Path Planning Solution", domain_object)
		plot_object.plot_results(PathPlan)


	"""

	print("\nStep 1. Reading Parameters")
	# The input file
	# input_file = "./input/user_input_files/circle_regular_obstacles.json"
	#input_file = "./input/user_input_files/circle_freeform_obstacles.json"
	#input_file = "./input/user_input_files/circle_mixed_obstacles.json"
	#input_file = "./input/user_input_files/circle_mixed_goals_obstacles.json"
	#input_file = "./input/user_input_files/circle_mixed_goals_obstacles_basic.json"
	#input_file = "./input/user_input_files/circle_mixed_goals_obstacles_star.json"
	#input_file = "./input/user_input_files/rectangle_mixed_goals_obstacles_basic.json"
	#input_file = "./input/user_input_files/rectangle_mixed_goals_obstacles_star.json"
	# input_file = "./input/user_input_files/lots_of_rectangles.json"
	# input_file = "./input/user_input_files/profiling_2.json"
	# input_file = "./input/user_input_files/circle_mixed_goals_obstacles_basic.json"
	# input_file = "./input/user_input_files/circle_mixed_goals_obstacles_star.json"
	# input_file = "./input/user_input_files/rectangle_mixed_goals_obstacles_basic.json"
	input_file = "./input/user_input_files/rectangle_mixed_goals_obstacles_star.json"
	title = re.search('user_input_files/(.+?).json', input_file).group(1)

	# Parsed JSON data
	program_input = ParseDataJSON(input_file)
	program_input.parse_data()

	# Split up the parsed input
	domain_info = program_input.data_dict["DomainInfo"]
	origin_goal_info = program_input.data_dict["OriginGoalInfo"]
	obstacles_info = program_input.data_dict["ObstaclesInfo"]
	rrt_algorithm_info = program_input.data_dict["RRTAlgorithmInfo"]

	print("\nStep 2. Creating Domain")
	domain_object = Domain(domain_info, obstacles_info, origin_goal_info)

	print("\nStep 3. Running Program")
	PathPlan = Solution(rrt_algorithm_info,domain_object)
	PathPlan.run_algorithm()
	PathPlan.process_vertex_list()

	print("\nStep 4. Printing and Saving Results")
	results_object = Results(PathPlan)
	results_object.print_results()
	results_object.save_results(title)

	print("\nStep 5. Plotting Results")
	plot_object = Plot(title, domain_object)
	plot_object.plot_results(PathPlan)

if __name__ == '__main__':
	run_program()

