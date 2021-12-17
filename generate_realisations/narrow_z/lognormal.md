# CoLoRe run

``` python
import os
from pathlib import Path
import textwrap
from subprocess import Popen, call

os.umask(0o022)

biases = ['_bias3',]

for bias in biases:
    output_path = Path(os.environ['sc']) / 'QSO_clustering_analysis' / 'CoLoRe_boxes' / 'compare_abacus' / f'logn{bias}_multibias'
    output_path.mkdir(exist_ok=True)
    colore_path = Path(f'/global/u2/c/cramirez/Codes/CoLoRe/1.0{bias}/CoLoRe')

    param_body = textwrap.dedent(f'''
    global = {{
    prefix_out = "{output_path}/out"
    output_format = "FITS"
    output_density = false
    pk_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/PlanckDR12_kmax_matterpower_z0.dat"
    z_min = 1.2
    z_max = 1.6
    seed = 0
    write_pred = false
    pred_dz = 0.1
    }}
    field_par = {{
    r_smooth = 2.0
    smooth_potential = true
    n_grid = 4096
    dens_type = 0
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
    nz_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/dndz.txt"
    bias_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/biases_lognormal/bias_1.txt"
    include_shear = false
    include_lensing = false
    store_skewers = false
    gaussian_skewers = false
    }}
    srcs2 = {{
    nz_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/dndz.txt"
    bias_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/biases_lognormal/bias_2.txt"
    include_shear = false
    include_lensing = false
    store_skewers = false
    gaussian_skewers = false
    }}
    srcs3 = {{
    nz_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/dndz.txt"
    bias_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/biases_lognormal/bias_3.txt"
    include_shear = false
    include_lensing = false
    store_skewers = false
    gaussian_skewers = false
    }}
    srcs4 = {{
    nz_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/dndz.txt"
    bias_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/biases_lognormal/bias_4.txt"
    include_shear = false
    include_lensing = false
    store_skewers = false
    gaussian_skewers = false
    }}
    srcs5 = {{
    nz_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/dndz.txt"
    bias_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/biases_lognormal/bias_5.txt"
    include_shear = false
    include_lensing = false
    store_skewers = false
    gaussian_skewers = false
    }}
    srcs6 = {{
    nz_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/dndz.txt"
    bias_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/biases_lognormal/bias_6.txt"
    include_shear = false
    include_lensing = false
    store_skewers = false
    gaussian_skewers = false
    }}
    srcs7 = {{
    nz_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/dndz.txt"
    bias_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/biases_lognormal/bias_7.txt"
    include_shear = false
    include_lensing = false
    store_skewers = false
    gaussian_skewers = false
    }}
    srcs8 = {{
    nz_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/dndz.txt"
    bias_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/biases_lognormal/bias_8.txt"
    include_shear = false
    include_lensing = false
    store_skewers = false
    gaussian_skewers = false
    }}
    srcs9 = {{
    nz_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/dndz.txt"
    bias_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/biases_lognormal/bias_9.txt"
    include_shear = false
    include_lensing = false
    store_skewers = false
    gaussian_skewers = false
    }}
    srcs10 = {{
    nz_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/dndz.txt"
    bias_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/biases_lognormal/bias_10.txt"
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

# Catalogs
``` bash
LyaPlotter_colore_to_drq --in-sim /global/cscratch1/sd/cramirez/QSO_clustering_analysis/CoLoRe_boxes/compare_abacus/logn_bias3_multibias --out-file /global/cscratch1/sd/cramirez/QSO_clustering_analysis/CoLoRe_boxes/compare_abacus/logn_bias3_multibias/cat.drq --source 5 --simplified --log-level DEBUG

LyaPlotter_randoms_from_drq --in-cat /global/cscratch1/sd/cramirez/QSO_clustering_analysis/CoLoRe_boxes/compare_abacus/logn_bias3_multibias/cat.drq --out-cat /global/cscratch1/sd/cramirez/QSO_clustering_analysis/CoLoRe_boxes/compare_abacus/logn_bias3_multibias/randoms_from_cat.drq --factor 1 --log-level DEBUG
```

# Corrfunc
``` python
import os
from pathlib import Path
import textwrap
from subprocess import call

os.umask(0o022)
basedir=Path('/global/cscratch1/sd/cramirez/QSO_clustering_analysis')

sourcebias = {
    0: 3.40,
    1: 3.42,
    2: 3.43,
    3: 3.45,
    4: 3.46,
    5: 3.48,
    6: 3.50,
    7: 3.51,
    8: 3.53,
    9: 3.54,
    10: 3.54
}

rsd=True
run_sbatch = True
randoms = 'randoms_from_cat.drq'
data_downsampling=1
randoms_downsampling=1

rangemin=0.1
rangemax=200
N_bins=41
nside=2
binmin=0.8
binmax=2.1

for CoLoRe_box in ('logn_bias3_multibias',):
    for source in (0,):
        CoLoRe_path = basedir /  'CoLoRe_boxes' / 'compare_abacus' / CoLoRe_box
        assert CoLoRe_path.is_dir()
        CoLoRe_files_glob = str(CoLoRe_path / f'out_srcs_s{source}*')

        randoms_path = CoLoRe_path / randoms
        assert randoms_path.is_file()

        _rsd_string = 'rsd' if rsd else 'norsd'  # This string was not applied, and therefore results with rsd were saved inside norsd. Changed by hand.

        output_predir = basedir / 'corrf_compare_abacus' / f'{sourcebias[source]}' / CoLoRe_box / f'nside_{nside}' / _rsd_string / f'{rangemin}_{rangemax}_{N_bins}' / f'{binmin}_{binmax}' / '0'
        output_predir.mkdir(parents=True, exist_ok=True)

        npix = 12*nside**2
        for ipix in range(npix):
            path = output_predir / f'{ipix}'
            path.mkdir(exist_ok=True)

            body = textwrap.dedent(f'''#!/bin/bash -l
#SBATCH --partition regular
#SBATCH --nodes 1
#SBATCH --time 10
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

srun CoLoRe_corrf_run_correlations --data {CoLoRe_files_glob} --data-format CoLoRe --randoms {str(randoms_path)} --out-dir {str(path)} --log-level DEBUG --nthreads ${{SLURM_CPUS_PER_TASK}} --zmin-covd 0.79 --zmax-covd 3.8 --zstep-covd 0.005 --zmin {binmin} --zmax {binmax} --nside {nside} --pixel-mask {ipix} --min-bin {rangemin} --max-bin {rangemax} --n-bins {N_bins} --compute-npoles 0 2 4 {'--data-norsd' if not rsd else ''} --data-downsampling {data_downsampling} --randoms-downsampling {randoms_downsampling}
        ''')

            run_file = path / 'run_corr.sl'
            with open(run_file, 'w') as f:
                f.write(body)

            if run_sbatch:
                os.chdir(path)
                retcode = call(f'sbatch {run_file}', shell=True)
```
--