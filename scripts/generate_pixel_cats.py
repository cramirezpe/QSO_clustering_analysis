'''
    Script to generate a CoLoRe catalog (data and randoms) split in healpix pixels
'''

import multiprocessing as mp
import logging
import argparse
import sys
from pathlib import Path
from LyaPlotter.tools import write_picca_drq_cat, generate_random_objects_from_data

logger = logging.getLogger(__name__)

def getArgs(): 
    parser = argparse.ArgumentParser()
    parser.add_argument("--CoLoRe-path",
        type=Path,
        help='Input CoLoRe box')
    
    parser.add_argument('--output-path',
        type=Path,
        help='Output dir where to store catalogs')

    parser.add_argument('--nside',
        type=int,
        help='nside to pixelise output')

    parser.add_argument('--log-level', default='WARNING', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET'])

    args = parser.parse_args()
    return args

def main(args=None):
    if args is None:
        args = getArgs()

    logging.basicConfig(stream=sys.stdout, 
        level=logging.getLevelName(args.log_level),
        format='%(levelname)s:%(name)s:%(funcName)s:%(message)s')

    if not args.CoLoRe_path.is_dir():
        raise FileNotFoundError('CoLoRe path does not exist: ', args.CoLoRe_path.resolve())
    
    
    


if __name__ == '__main__':
    main()