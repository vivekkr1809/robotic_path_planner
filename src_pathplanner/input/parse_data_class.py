# Author(s) : Vivek
import click
import json

class ParseDataJSON():
  """The class reads the JSON file to start the program
  """
  def __init__(self, json_file):
    """Constructor method

    Parameters:
      json_file:
        The file to be parsed

    """
    self.json_file= json_file
  def parse_data(self):
    """Function to parse the data

    Attributes:
      data_dict (:obj: `dict`):
        dictionary containing the parsed data
    """
    self.data_dict = {}
    with open(self.json_file, 'r') as f:
      data = f.read()
      self.data_dict =json.loads(data)