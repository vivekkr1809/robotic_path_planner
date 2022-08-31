# Author(s) : Vivek
import click
import json

import sys
sys.path.append(".")

from input.parse_data_class import ParseDataJSON


def test_empty_file():
	data = ParseDataJSON('./test/test_rrt_inputs.json')
	data.parse_data()