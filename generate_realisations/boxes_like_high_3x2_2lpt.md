# Boxes with 2LPT features

I will run boxes for the three biases at the same time with this document.

# CoLoRe realisations
```python
import os
from pathlib import Path
import textwrap
from subprocess import Popen, call

os.umask(0o022)

biases = '', '_bias2', '_bias3'

for bias in biases:
    output_path = Path(os.environ['sc']) / 'QSO_clustering_analysis' / 'CoLoRe_boxes' / f'high_3x2_600_2lpt{bias}'
    output_path.mkdir(exist_ok=True)
    colore_path = Path(f'/global/u2/c/cramirez/Codes/CoLoRe/1.0{bias}/CoLoRe')

    param_body = textwrap.dedent(f'''
    global = {{
    prefix_out = "{output_path}/out"
    output_format = "FITS"
    output_density = false
    pk_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/PlanckDR12_kmax_matterpower_z0.dat"
    z_min = 0.8
    z_max = 3.79
    seed = 0
    write_pred = false
    pred_dz = 0.1
    }}
    field_par = {{
    r_smooth = 2.0
    smooth_potential = true
    n_grid = 4096
    dens_type = 2
    lpt_buffer_fraction = 0.6
    lpt_interp_type = 1
    output_lpt = 0
    }}
    cosmo_par = {{
    omega_M = 0.3147
    omega_L = 0.6853
    omega_B = 0.04904
    h = 0.6731
    w = -1.0
    ns = 0.9655
    sigma_8 = 0.830
    }}
    srcs1 = {{
    nz_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/high_3x2_600.txt"
    bias_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/Bz_qso_G18.txt"
    include_shear = false
    include_lensing = false
    store_skewers = false
    gaussian_skewers = false
    }}
    ''')

    param_file = output_path / 'param.cfg'
    with open(param_file,'w') as f:
        f.write(param_body)

    call(f'LyaScripts_CoLoRe -o {output_path} -c {colore_path.resolve()} -p {param_file.resolve()} -e CoLoRe --node 32 --run-sbatch', shell=True)
```

# Corrfunc analysis
## Make randoms (copy them from lognormal realisations)
```bash
ln -s /global/cscratch1/sd/cramirez/QSO_clustering_analysis/CoLoRe_boxes/high_3x2_600/randoms.fits /global/cscratch1/sd/cramirez/QSO_clustering_analysis/CoLoRe_boxes/high_3x2_600_2lpt/randoms.fits

ln -s /global/cscratch1/sd/cramirez/QSO_clustering_analysis/CoLoRe_boxes/high_3x2_600/randoms.fits /global/cscratch1/sd/cramirez/QSO_clustering_analysis/CoLoRe_boxes/high_3x2_600_2lpt_bias2/randoms.fits

ln -s /global/cscratch1/sd/cramirez/QSO_clustering_analysis/CoLoRe_boxes/high_3x2_600/randoms.fits /global/cscratch1/sd/cramirez/QSO_clustering_analysis/CoLoRe_boxes/high_3x2_600_2lpt_bias3/randoms.fits

ln -s /global/cscratch1/sd/cramirez/QSO_clustering_analysis/CoLoRe_boxes/high_3x2_600/randoms_from_cat.fits /global/cscratch1/sd/cramirez/QSO_clustering_analysis/CoLoRe_boxes/high_3x2_600_2lpt/randoms_from_cat.fits

ln -s /global/cscratch1/sd/cramirez/QSO_clustering_analysis/CoLoRe_boxes/high_3x2_600/randoms_from_cat.fits /global/cscratch1/sd/cramirez/QSO_clustering_analysis/CoLoRe_boxes/high_3x2_600_2lpt_bias2/randoms_from_cat.fits

ln -s /global/cscratch1/sd/cramirez/QSO_clustering_analysis/CoLoRe_boxes/high_3x2_600/randoms_from_cat.fits /global/cscratch1/sd/cramirez/QSO_clustering_analysis/CoLoRe_boxes/high_3x2_600_2lpt_bias3/randoms_from_cat.fits
```

## Run corrf
``` python
import os
from pathlib import Path
import textwrap
from subprocess import call

os.umask(0o022)
basedir=Path('/global/cscratch1/sd/cramirez/QSO_clustering_analysis')

rsd=False
run_sbatch = True
randoms = 'randoms_from_cat.fits'

rangemin=0.1
rangemax=200
N_bins=41
nside=2
binmin=0.8
binmax=0.9

for CoLoRe_box in ('high_3x2_600_2lpt', 'high_3x2_600_2lpt_bias2', 'high_3x2_600_2lpt_bias3'):
    CoLoRe_path = basedir / 'CoLoRe_boxes' / CoLoRe_box
    assert CoLoRe_path.is_dir()
    CoLoRe_files_glob = str(CoLoRe_path / 'out_srcs_s1*')

    randoms_path = CoLoRe_path / randoms
    assert randoms_path.is_file()

    _rsd_string = 'rsd' if rsd else 'norsd'

    output_predir = basedir / 'corrf_from_cat' / CoLoRe_box / f'nside_{nside}' / _rsd_string / f'{rangemin}_{rangemax}_{N_bins}' / f'{binmin}_{binmax}' / '0'
    output_predir.mkdir(parents=True, exist_ok=True)

    npix = 12*nside**2
    for ipix in range(npix):
        path = output_predir / f'{ipix}'
        path.mkdir(exist_ok=True)

        body = textwrap.dedent(f'''#!/bin/bash -l
#SBATCH --partition regular
#SBATCH --nodes 1
#SBATCH --time 2
#SBATCH --job-name binned_corrf_david
#SBATCH --error {path}/%x-%j.err
#SBATCH --output {path}/%x-%j.out
#SBATCH -C haswell
#SBATCH -A desi
#SBATCH --cpus-per-task=64

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

module unload craype-hugepages2M
umask u+rwx,g+rwx,o+rx

source activate CoLoRe

srun CoLoRe_corrf_run_correlations --data {CoLoRe_files_glob} --data-format CoLoRe --randoms {str(randoms_path)} --out-dir {str(path)} --log-level DEBUG --nthreads ${{SLURM_CPUS_PER_TASK}} --zmin-covd 0.79 --zmax-covd 3.8 --zstep-covd 0.005 --zmin {binmin} --zmax {binmax} --nside {nside} --pixel-mask {ipix} --min-bin {rangemin} --max-bin {rangemax} --n-bins {N_bins} --compute-npoles 0 2 4
        ''')

        run_file = path / 'run_corr.sl'
        with open(run_file, 'w') as f:
            f.write(body)

        if run_sbatch:
            os.chdir(path)
            retcode = call(f'sbatch {run_file}', shell=True)
``` 
--