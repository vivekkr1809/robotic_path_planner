Introduction
============

Rapidly-exploring random trees (RRTs) are a class of algorithms used in autonomous robotic motion planning to efficiently calculate a path through a large unsearched domain. This domain can either represent a physical space (i.e. 2D or 3D euclidean space), or a higher-dimensional robotic state space. The algorithm generates trajectories through the domain, and can easily handle multiple obstacles, goals, or other differential constraints that are applicable to a robotic motion planning problem.

The RRT works by growing a search tree incrementally from random samples drawn from the domain, and is therefore biased to grow into unsearched areas. As a new sample is drawn, the algorithm attempts to connect it to the nearest point in the existing solution-path tree. If the connection is possible (i.e. does not collide with an obstacle, or is otherwise infeasible from a kinematic perspective) then a new graph edge is made and the next iteration begins.

The Basic RRT algorithm was first proposed by Lavalle and Kuffner in 1998. While its development was a paradigm shift in the field of robotic motion planning (RRTs were significantly more efficient than the existing path planning methods), the main drawback of the Basic RRT is that it almost surely converges to a non-optimal value. Since the proposal of the Basic RRT, developing new algorithms modifying its underlying principles has been an active area of research. The most significant leap forward was the development of the RRT* (RRT Star) algorithm by Frazzoli in 2010, which is a variant of the Basic RRT that guarantees convergence to the optimal solution.


Motivation
**********

The goal of this project is to develop a modular and scalable program that implements a variety of path-planning algorithms to seaach through a physical domain space populated with obstacles. The ultimate motivation for this work is to assess the relative efficiency and performance of a large set of different algorithms acting in various domains. Therefore, the program is developed in such a way that both the definition of the domain space, and the solution procedure is extensible in the future. 


Limitations
***********

Currently only the Basic RRT and the RRT* algorithms are implemented. But examining the difference between these two algorithms is an adequate starting point for showing the difference between a random search method and one that approaches optimality.

Currently only a 2D physical domain space has been implemented. The domain can only be a regular shape (circle or rectangle)

Currently only bitmap (.pbm) shapes can be used to define any freeform (i.e. not regular shapes) obstacles or goals to be placed inside the domain.