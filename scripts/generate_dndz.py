'''
    The dndz file used by James have the issue of not having enough low-z quasars.

    The aim of this script is to generate a dndz file from an input quasar catalog.    
'''
import argparse
from pathlib import Path
import fitsio
import scipy.stats as stats
from scipy.integrate import quad
import logging
import sys
import numpy as np

logger = logging.getLogger(__name__)

def main(args=None):
    if args is None:
        args = getArgs()

    level = logging.getLevelName(args.log_level)
    logging.basicConfig(stream=sys.stdout, level=level, format='%(levelname)s:%(name)s:%(funcName)s:%(message)s')

    logger.info(f'Reading catalog: {args.input_cat}')
    Z = fitsio.read(args.input_cat)[args.redshift_field]

    logger.debug(f'Length of catalogue: {len(Z)}')
    
    logger.info(f'Generating density estimation')
    density = stats.gaussian_kde(Z, bw_method=0.15) # This value 0.15 just seems to work fine.

    logger.info(f'Renormalizing density estimation')
    density_integral = quad(density, args.zmin_density, args.zmax_density)[0]
    density_factor = args.density / density_integral

    logger.info(f'Generating dndz')
    z = np.linspace(args.zbins_min, args.zbins_max, args.zbins_N)
    dndz = density(z)*density_factor

    logger.info('Saving dndz into file')
    _save_array = np.transpose((z, dndz))
    np.savetxt(args.output_file, _save_array)

    logger.info('Done')

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-cat",
        type=Path,
        required=True,
        help="Input catalog",
    )
    parser.add_argument("--redshift-field",
        type=str,
        default="Z",
        help='Redshift field in fits file. Default: Z',
    )
    parser.add_argument("--output-file",
        type=Path,
        help="Output txt file",
    )

    zbins = parser.add_argument_group("zbins")
    zbins.add_argument("--zbins-min",
        type=float,
        default=0,
        help='Min value for z in output dndz. Default: 0',
    )
    zbins.add_argument("--zbins-max",
        type=float,
        default=5,
        help='Max value for z in output dndz',
    )   
    zbins.add_argument("--zbins-N",
        type=int,
        default=100,
        help='Number of zbins in output dndz. Default: 100',
    )
    
    conditions = parser.add_argument_group("density conditions",
        description="Conditions to generate the catalog: density of quasars in a redshift range")
    conditions.add_argument('--zmin-density',
        type=float,
        default=0,
        help='Min. redshift to apply density conditions. Default: 0',
    )
    conditions.add_argument('--zmax-density',
        type=float,
        default=10,
        help='Max. redshfit to apply density conditions. Default: 10',
    )
    conditions.add_argument('--density',
        type=float,
        default=60,
        help='Density in the conditions area (in QSOS/sqdg). Default: 60',
    )

    parser.add_argument('--log-level', 
        default='WARNING', 
        choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET'],
    )


    args = parser.parse_args()
    return args

if __name__ == '__main__':
    main()