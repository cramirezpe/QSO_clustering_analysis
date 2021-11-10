## First box generation

We'll generate a first box with the 10x DESI quasars in order to estimate how many objects we'll need to have a good measure of the correlations. The catalog by James doesn't have quasars below redshift 1, and therefore we will use a custom one generated from measurements of quasars.

In order to fix that I've created the script ``scripts/generate_dndz.py``. To generate the dndz file I've used:
```bash
source activate CoLoRe
python generate_dndz.py --input-cat /global/u2/c/cramirez/Codes/desi_lya_sv/everest_healpix_e2e/catalogues/qsocat_main.fits.gz --output-file /global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/10x_DESI --zmin-density 2.1 --zmax-density 5 --density 600 --log-level DEBUG
```
The notebook ``input_files.ipynb`` shows that the generated dndz is the expected one.


I'll use the package LyaScripts to generate the CoLoRe files.
``` bash
output_path=$sc/QSO_clustering_analysis/CoLoRe_boxes/10x_DESI_box
mkdir -p $output_path
colore_path=/global/u2/c/cramirez/Codes/CoLoRe/CoLoRe_LyA/CoLoRe

cat > ${output_path}/param.cfg << EOF
global = {
  prefix_out = "${output_path}/out"
  output_format = "FITS"
  output_density = false
  pk_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/PlanckDR12_kmax_matterpower_z0.dat"
  z_min = 0.8
  z_max = 3.79
  seed = 0
  write_pred = false
  pred_dz = 0.1
}
field_par = {
  r_smooth = 2.0
  smooth_potential = true
  n_grid = 4096
  dens_type = 0
  lpt_buffer_fraction = 0.6
  lpt_interp_type = 1
  output_lpt = 0
}
cosmo_par = {
  omega_M = 0.3147
  omega_L = 0.6853
  omega_B = 0.04904
  h = 0.6731
  w = -1.0
  ns = 0.9655
  sigma_8 = 0.830
}
srcs1 = {
  nz_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/10x_DESI.txt"
  bias_filename = "/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/Bz_qso_G18.txt"
  include_shear = false
  store_skewers = false
  gaussian_skewers = false
}
EOF

source activate CoLoRe
LyaScripts_CoLoRe -c $colore_path -o $output_path -p ${output_path}/param.cfg -e CoLoRe --nodes 32 --run-sbatch
```


To perform ``corrfunc`` analysis I'll use my package ``CoLoRe_corrf_analysis``.

I'd like to check the performance of my randoms builder, but I need to compare with good randoms first. Let's create them:
``` bash
source activate CoLoRe
LyaPlotter_colore_to_drq --in-sim /global/cscratch1/sd/cramirez/QSO_clustering_analysis/CoLoRe_boxes/10x_DESI_box --out-file /global/cscratch1/sd/cramirez/QSO_clustering_analysis/CoLoRe_boxes/10x_DESI_box_cat.drq --source 1 --simplified --log-level DEBUG

LyaPlotter_randoms_from_drq --in-cat /global/cscratch1/sd/cramirez/QSO_clustering_analysis/CoLoRe_boxes/10x_DESI_box_cat.drq --out-cat /global/cscratch1/sd/cramirez/QSO_clustering_analysis/CoLoRe_boxes/10x_DESI_box_rand.drq --factor 1 --log-level DEBUG
```

Code to make randoms on the fly:
``` python
import os
from pathlib import Path
import textwrap
from subprocess import call

os.umask(0o022) # All for user, read and execute for group and others.
basedir=Path('/global/cscratch1/sd/cramirez/QSO_clustering_analysis')
CoLoRe_box='10x_DESI_box'
nz_file ='/global/project/projectdirs/desi/users/cramirez/QSO_clustering_analysis/input_files/10x_DESI.txt'
rsd=False
run_sbatch = True
randoms = None

rangemin=0.1
rangemax=200
N_bins=41
nside=2
binmin=0.8
binmax=0.9

CoLoRe_path = basedir / 'CoLoRe_boxes' / CoLoRe_box
assert CoLoRe_path.is_dir()
CoLoRe_files_glob = str(CoLoRe_path / 'out_srcs_s1*')

_rsd_string = 'rsd' if rsd else 'norsd'

output_predir = basedir / 'corrf_2_3xrand' / f'nside_{nside}' / _rsd_string / f'{rangemin}_{rangemax}_{N_bins}' / f'{binmin}_{binmax}' / '0'
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

srun CoLoRe_corrf_run_correlations --data {CoLoRe_files_glob} --data-format CoLoRe --randoms-from-nz-file {nz_file} --randoms-factor 3 --store-generated-rands --out-dir {str(path)} --log-level DEBUG --nthreads ${{SLURM_CPUS_PER_TASK}} --zmin-covd 0.79 --zmax-covd 3.8 --zstep-covd 0.005 --zmin {binmin} --zmax {binmax} --nside {nside} --pixel-mask {ipix} --min-bin {rangemin} --max-bin {rangemax} --n-bins {N_bins} --compute-npoles 0 2 4
    ''')

    run_file = path / 'run_corr.sl'
    with open(run_file, 'w') as f:
        f.write(body)

    if run_sbatch:
        os.chdir(path)
        retcode = call(f'sbatch {run_file}', shell=True)

```

Code to use randoms in catalogue:
```python
import os
from pathlib import Path
import textwrap
from subprocess import call

os.umask(0o022) # All for user, read and execute for group and others.
basedir=Path('/global/cscratch1/sd/cramirez/QSO_clustering_analysis')
CoLoRe_box='10x_DESI_box'
rsd=False
run_sbatch = True
randoms = '10x_DESI_box_cat.drq'

rangemin=0.1
rangemax=200
N_bins=41
nside=2
binmin=0.8
binmax=0.9

CoLoRe_path = basedir / 'CoLoRe_boxes' / CoLoRe_box
assert CoLoRe_path.is_dir()
CoLoRe_files_glob = str(CoLoRe_path / 'out_srcs_s1*')

randoms_path = basedir / 'CoLoRe_boxes' / randoms
assert randoms_path.is_file()

_rsd_string = 'rsd' if rsd else 'norsd'

output_predir = basedir / 'corrf_rand_from_cat' / f'nside_{nside}' / _rsd_string / f'{rangemin}_{rangemax}_{N_bins}' / f'{binmin}_{binmax}' / '0'
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