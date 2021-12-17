'''
Script best fit biases for multiple measurements of correlation function.
'''

import argparse
import logging
import sys
from pathlib import Path


from CoLoRe_corrf_analysis.read_colore import ComputeModelsCoLoRe
from CoLoRe_corrf_analysis.file_funcs import FileFuncs
from CoLoRe_corrf_analysis.fitter import Fitter
from CoLoRe_corrf_analysis.cf_helper import CFComputations

from tabulate import tabulate


logger = logging.getLogger(__name__)

def main(args=None):
    if args is None:
        args = getArgs()

    level = logging.getLevelName(args.log_level)
    logging.basicConfig(stream=sys.stdout, level=level, format='%(levelname)s:%(name)s:%(funcName)s:%(message)s')

    logger.info('Defining theoretical model')
    assert args.theory_path.is_dir()
    theory = ComputeModelsCoLoRe(
        box_path = args.theory_path,
        source = args.theory_source,
        apply_lognormal = args.theory_lognormal
    )
    zeff = theory.get_zeff(args.zmin, args.zmax)

    logger.info('Getting corrf results')
    def get_boxes(path):
        return FileFuncs.mix_sims(
            FileFuncs.get_full_path(path, rsd=args.rsd, rsd2=None,
                rmin=args.rmin, rmax=args.rmax, N_bins=args.N_bins,
                zmin=args.zmin, zmax=args.zmax, nside=args.nside)
        )
    
    boxes = dict()
    out_bias = dict()
    logger.info('Getting boxes')
    in_biases = sorted([x.name for x in args.corrf_multisim_path.iterdir() if (x / args.corrf_box_name).is_dir()])

    for in_bias in in_biases:
        logger.debug(f'Getting boxes for bias {in_bias}. Path: {str(args.corrf_multisim_path / in_bias / args.corrf_box_name)}')
        boxes[in_bias] = get_boxes(args.corrf_multisim_path / in_bias / args.corrf_box_name)
    
    logger.info('Making fits')
    for in_bias in in_biases:
        fitter = Fitter(boxes=boxes[in_bias], z=zeff, theory=theory, poles=args.fitter_poles, bias0=args.fitter_bias0, rmin=args.fitter_rmin, rmax=args.fitter_rmax, rsd=args.rsd)
        fitter.run_fit(free_params=['bias'])
        out_bias[in_bias] = fitter.out.params['bias'].value

    table = []
    out_biases = [out_bias[in_bias] for in_bias in in_biases]
    
    table.append([in_bias, out_bias[in_bias]])

    if args.print_values:
        print(tabulate(table, headers=['In', 'Out']))
    
    return in_biases, out_biases
        


def getArgs():
    from types import SimpleNamespace
    args = SimpleNamespace(
        corrf_multisim_path = Path('/global/cscratch1/sd/cramirez/QSO_clustering_analysis/corrf_from_cat_multibias'),
        corrf_box_name = 'high_3x2_600_2lpt_bias3_multibias',
        theory_path = Path('/global/cscratch1/sd/cramirez/QSO_clustering_analysis/CoLoRe_boxes/high_3x2_600'),
        theory_lognormal = False,
        theory_source = 1,
        rsd = True,
        rmin = 0.1, 
        rmax = 200,
        N_bins = 41,
        zmin = 0.8,
        zmax = 2.1,
        nside = 2, 
        fitter_poles = [0],
        fitter_rmin = {0:30, 2:30},
        fitter_rmax = {0:80, 2:80},
        fitter_bias0 = 1,
        log_level = 'DEBUG',
        print_values=False,
    )

    return args

if __name__ == '__main__':
    main(args=None)
