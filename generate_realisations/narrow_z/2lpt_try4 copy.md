# CoLoRe run
``` python
import os
from pathlib import Path
import textwrap
from subprocess import Popen, call

os.umask(0o022)

biases = ['_bias3',]

for bias in biases:
    output_path = Path(os.environ['sc']) / 'QSO_clustering_analysis' / 'CoLoRe_boxes' / 'compare_abacus' / f'2lpt{bias}_multibias_try5'
    output_path.mkdir(exist_ok=True)
    colore_path = Path(f'/global/u2/c/cramirez/Codes/CoLoRe/1.0.1{bias}/CoLoRe')

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
    nz_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/dndz.txt"
    bias_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/biases_lpt_try5/bias_1.txt"
    include_shear = false
    include_lensing = false
    store_skewers = false
    gaussian_skewers = false
    }}
    srcs2 = {{
    nz_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/dndz.txt"
    bias_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/biases_lpt_try5/bias_2.txt"
    include_shear = false
    include_lensing = false
    store_skewers = false
    gaussian_skewers = false
    }}
    srcs3 = {{
    nz_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/dndz.txt"
    bias_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/biases_lpt_try5/bias_3.txt"
    include_shear = false
    include_lensing = false
    store_skewers = false
    gaussian_skewers = false
    }}
    srcs4 = {{
    nz_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/dndz.txt"
    bias_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/biases_lpt_try5/bias_4.txt"
    include_shear = false
    include_lensing = false
    store_skewers = false
    gaussian_skewers = false
    }}
    srcs5 = {{
    nz_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/dndz.txt"
    bias_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/biases_lpt_try5/bias_5.txt"
    include_shear = false
    include_lensing = false
    store_skewers = false
    gaussian_skewers = false
    }}
    srcs6 = {{
    nz_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/dndz.txt"
    bias_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/biases_lpt_try5/bias_6.txt"
    include_shear = false
    include_lensing = false
    store_skewers = false
    gaussian_skewers = false
    }}
    srcs7 = {{
    nz_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/dndz.txt"
    bias_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/biases_lpt_try5/bias_7.txt"
    include_shear = false
    include_lensing = false
    store_skewers = false
    gaussian_skewers = false
    }}
    srcs8 = {{
    nz_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/dndz.txt"
    bias_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/biases_lpt_try5/bias_8.txt"
    include_shear = false
    include_lensing = false
    store_skewers = false
    gaussian_skewers = false
    }}
    srcs9 = {{
    nz_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/dndz.txt"
    bias_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/biases_lpt_try5/bias_9.txt"
    include_shear = false
    include_lensing = false
    store_skewers = false
    gaussian_skewers = false
    }}
    srcs10 = {{
    nz_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/dndz.txt"
    bias_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/biases_lpt_try5/bias_10.txt"
    include_shear = false
    include_lensing = false
    store_skewers = false
    gaussian_skewers = false
    }}
    srcs11 = {{
    nz_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/dndz.txt"
    bias_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/biases_lpt_try5/bias_11.txt"
    include_shear = false
    include_lensing = false
    store_skewers = false
    gaussian_skewers = false
    }}
    srcs12 = {{
    nz_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/dndz.txt"
    bias_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/biases_lpt_try5/bias_12.txt"
    include_shear = false
    include_lensing = false
    store_skewers = false
    gaussian_skewers = false
    }}
    srcs13 = {{
    nz_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/dndz.txt"
    bias_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/biases_lpt_try5/bias_13.txt"
    include_shear = false
    include_lensing = false
    store_skewers = false
    gaussian_skewers = false
    }}
    srcs14 = {{
    nz_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/dndz.txt"
    bias_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/biases_lpt_try5/bias_14.txt"
    include_shear = false
    include_lensing = false
    store_skewers = false
    gaussian_skewers = false
    }}
    srcs15 = {{
    nz_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/dndz.txt"
    bias_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/biases_lpt_try5/bias_15.txt"
    include_shear = false
    include_lensing = false
    store_skewers = false
    gaussian_skewers = false
    }}
    srcs16 = {{
    nz_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/dndz.txt"
    bias_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/biases_lpt_try5/bias_16.txt"
    include_shear = false
    include_lensing = false
    store_skewers = false
    gaussian_skewers = false
    }}
    srcs17 = {{
    nz_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/dndz.txt"
    bias_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/biases_lpt_try5/bias_17.txt"
    include_shear = false
    include_lensing = false
    store_skewers = false
    gaussian_skewers = false
    }}
    srcs18 = {{
    nz_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/dndz.txt"
    bias_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/biases_lpt_try5/bias_18.txt"
    include_shear = false
    include_lensing = false
    store_skewers = false
    gaussian_skewers = false
    }}
    srcs19 = {{
    nz_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/dndz.txt"
    bias_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/biases_lpt_try5/bias_19.txt"
    include_shear = false
    include_lensing = false
    store_skewers = false
    gaussian_skewers = false
    }}
    srcs20 = {{
    nz_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/dndz.txt"
    bias_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/biases_lpt_try5/bias_20.txt"
    include_shear = false
    include_lensing = false
    store_skewers = false
    gaussian_skewers = false
    }}
    srcs21 = {{
    nz_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/dndz.txt"
    bias_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/compare_abacus/biases_lpt_try5/bias_21.txt"
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
ln /global/cscratch1/sd/cramirez/QSO_clustering_analysis/CoLoRe_boxes/compare_abacus/logn_bias3_multibias_try4/randoms_from_cat.drq /global/cscratch1/sd/cramirez/QSO_clustering_analysis/CoLoRe_boxes/compare_abacus/2lpt_bias3_multibias_try5/randoms_from_cat.drq
```

# Run corrf
``` python
import os
from pathlib import Path
import textwrap
from subprocess import call

os.umask(0o022)
basedir=Path('/global/cscratch1/sd/cramirez/QSO_clustering_analysis')

sourcebias = {
    1: 2.00,
    2: 2.02,
    3: 2.04,
    4: 2.06,
    5: 2.08,
    6: 2.10,
    7: 2.12,
    8: 2.14,
    9: 2.16,
    10: 2.18,
    11: 2.20,
    12: 2.22,
    13: 2.24,
    14: 2.26,
    15: 2.28,
    16: 2.30,
    17: 2.32,
    18: 2.34,
    19: 2.36,
    20: 2.38,
    21: 2.40,
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
binmin=1.2
binmax=1.6

for CoLoRe_box in ('2lpt_bias3_multibias_try5',):
    for source in (9 ,11, 13, 17, 21):
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
#SBATCH --time 5
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
                retcode = call(f'sbatch --dependency=afterok:52066917 {run_file}', shell=True)
```

--
