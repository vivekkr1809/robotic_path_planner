Program Execution
=================

Create a new conda virtual python environment::

	$ conda create --name new_env_name python=3.7
	$ conda activate new_env_name


Install additional packages in thewq following file::

	requirements.txt
	$ pip install -r requirements.txt

To plot freeform shapes, ensure that the ImageMagick tool is installed::

	https://imagemagick.org/script/download.php

Run the program in the terminal from where the top-level folder is located in user directory::

	$ cd USER_PATH/apc_524_robotic_path_planning/src_pathplanner

	$ python path_planner.py

User Input
**********

User input .json file and path specified in Step 1 of path_planner.py module::
	
	input_file = "./input/user_input_files/circle_mixed_goals_obstacles.json"


Any freeform shapes must be specified in bitmap (.pbm) format with their path specified in the input file

User-specified input .json file follows the following format, but can be extended if future functionality is required::

	DomainInfo:
		dim: Euclidean dimension (2)
		shape_type: Regular shape (circle/rectangle)
			size/location style-string based on chosen shape (see example below)

	OriginGoalInfo:
		origin: Starting point coordinates (x,y)
		goals: Shapes defining the goal location (circle/rectangle/freeform)
			size/location style-string based on chosen shape (see example below)

	ObstaclesInfo:
		obstacles: Shapes defining the obstacle location (circle/rectangle/freeform)
			size/location style-string based on chosen shape (see example below)

	RRTAlgorithmInfo:
		method: name of algorithm to use (rrt_basic/rrt_star)
		n_trials: number of trials
		step_size: maximum distance of an rrt graph edge
		dim: Euclidean dimension (2)
		neighborhood: rrt_star algorithm only, radius of neighboring vertices to optimize



Example input .json file with a mix of regular and freeform geometry definitions::
	
	{
	"DomainInfo":{
		"dim" : 2,
		"shape_type": "circle",
		"radius": 5,
		"center": [0.0,0.0]
		},

	"OriginGoalInfo":{
		"origin" : [0.1,0.1],
		"goals":{
			"goal_1":{"dim":2, "shape_type": "free_form",
				"bitmap_file":"./input/bitmap_files/seahorse.pbm",
				"bb_lower_left":[-2.0,2.0], "bb_upper_right":[0.0,4.0]},
			"goal_2":{"dim":2, "shape_type":"circle", "radius":0.1, "center":[2.5, 3.5]},
			"goal_3":{"dim":2, "shape_type":"rectangle", "lower_left": [-3.2, -2.0],"upper_right": [-2.8,-1.8]},
			"goal_4":{"dim":2, "shape_type":"circle", "radius":0.1, "center":[3.0, -3.0]}			
			}
		},

	"ObstaclesInfo":{
		"obstacle_1":{"dim":2, "shape_type": "circle", "radius":0.5, "center":[-3.0,-0.5]},
		"obstacle_2":{"dim":2, "shape_type": "circle", "radius":0.6, "center":[1.0,-2.0]},
		"obstacle_3":{"dim":2, "shape_type": "circle", "radius":0.4, "center":[1.5,0.5]},
		"obstacle_4":{"dim":2, "shape_type": "rectangle", "lower_left": [2.0, 1.5],"upper_right": [2.5,3.0]},
		"obstacle_5":{"dim":2, "shape_type": "free_form", 
			"bitmap_file":"./input/bitmap_files/obstacle.pbm", 
			"bb_lower_left":[-2.0,0.0], "bb_upper_right":[0.0,2.0]}		
		},

	"RRTAlgorithmInfo":{
		"method": "rrt_star",
		"n_trials": 1000,
		"step_size": 0.3,
		"dim": 2,
		"neighborhood": 0.4
		}
	}


path_planner module
*******************

.. automodule:: path_planner
   :members:

Program Output
**************

The program produces output in the following folder::
	
	USER_PATH/apc_524_robotic_path_planning/output/output_files

Produces::

	Text file of the vertices, parents, costs lists for the solution tree

	.html plot of the domain + solution tree
