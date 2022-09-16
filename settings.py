import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

#Define PATHS
PATH_DATA_RAW = os.path.join(PROJECT_ROOT, 'data', 'raw')
PATH_DATA_INTERMEDIATE = os.path.join(PROJECT_ROOT, 'data', 'intermediate')
PATH_DATA_PROCESSED = os.path.join(PROJECT_ROOT, 'data', 'processed')