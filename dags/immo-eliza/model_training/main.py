import os
import pathlib
from utils.train_model import train_model

os.chdir(pathlib.Path(os.path.dirname(__file__)))
train_model()