import sys
import logging
sys.path.append('/Users/stankusnt/hospital-extract')
logger = logging.getLogger(__name__)
logging.basicConfig(filename='activity.log', encoding='utf-8', level=logging.INFO)
from src.hospital import *


def main():
    extract.run()

if __name__ == '__main__':
    main()