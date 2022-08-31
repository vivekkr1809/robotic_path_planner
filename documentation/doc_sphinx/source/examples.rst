Examples
============

The following examples show the input/output from several program runs.

A domain can be defined with the following types of geometry::

	Circle
	Rectangle

The following three shapes are used to define both obstacles and goals::

	Circle
	Rectangle
	Freeform

The domains are solved with the following algorithms::

	RRT Basic
	RRT Star

Simple example using a Rectangular Domain
*****************************************

Basic RRT Input File
--------------------

.. literalinclude:: ../../../src_pathplanner/input/user_input_files/rectangle_mixed_goals_obstacles_basic.json
   :language: json
   :linenos:
   :emphasize-lines: 4, 28
   :caption: Basic RRT

Basic RRT Output
----------------

.. raw:: html
	:file: ./example_files/rectangle_mixed_goals_obstacles_basic.html

Results text file

.. literalinclude :: ./example_files/rectangle_mixed_goals_obstacles_basic.txt
	:emphasize-lines: 38,39

RRT Star Input File
-------------------

.. literalinclude:: ../../../src_pathplanner/input/user_input_files/rectangle_mixed_goals_obstacles_star.json
   :language: json
   :linenos:
   :emphasize-lines: 4, 28
   :caption: RRT Star

RRT Star Output
----------------

.. raw:: html
	:file: ./example_files/rectangle_mixed_goals_obstacles_star.html

Results text file

.. literalinclude :: ./example_files/rectangle_mixed_goals_obstacles_star.txt
	:emphasize-lines: 32,33


Complex example using a Circular Domain
***************************************

Basic RRT Input File
--------------------

.. literalinclude:: ../../../src_pathplanner/input/user_input_files/circle_mixed_goals_obstacles_basic.json
   :language: json
   :linenos:
   :emphasize-lines: 4, 32
   :caption: Basic RRT

Basic RRT Output
----------------
Show plots and results

.. raw:: html
	:file: ./example_files/circle_mixed_goals_obstacles_basic.html

Results text file

.. literalinclude :: ./example_files/circle_mixed_goals_obstacles_basic.txt
	:emphasize-lines: 101-104

RRT Star Input File
-------------------

.. literalinclude:: ../../../src_pathplanner/input/user_input_files/circle_mixed_goals_obstacles_star.json
   :language: json
   :linenos:
   :emphasize-lines: 4, 32
   :caption: RRT Star

RRT Star Output
----------------
Show plots and results

.. raw:: html
	:file: ./example_files/circle_mixed_goals_obstacles_star.html

Results text file

.. literalinclude :: ./example_files/circle_mixed_goals_obstacles_star.txt
	:emphasize-lines: 73-76


