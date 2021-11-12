# Correlations on DESI SV3 data.

I will use files from ``/global/cfs/cdirs/desi/survey/catalogs/SV3/LSS/everest/LSScats/2.1/QSO*``. According to the notebook shared by Arnaud de Mattia (his notebook does not work out of the box), the data files that sould be read are ``QSO_N_clustering.dat.fits`` and ``QSO_S_clustering.dat.fits`` with randoms ``QSO_N_i_clustering.ran.fits`` where i from 0 to 9. **N and S are regions, North and South(?)**.

The fits files can be read by my scripts without problems, even though my scripts do not include weights. (They can be included in a not so complicated way).


###  Run corrf
``` python
import os
from pathlib import Path
import textwrap
from subprocess import call

os.umask(0o022)
input_dir = Path('/global/cfs/cdirs/desi/survey/catalogs/SV3/LSS/everest/LSScats/2.1/')
output_basedir = Path('/global/cscratch1/sd/cramirez/QSO_clustering_analysis')

run_sbatch = True

rangemin=0.1
rangemax=200
N_bins=41
nside=0 # Full-sky
binmin=0.8
binmax=2.1

output_dir = output_basedir / 'corrf_real_data' / f'nside_{nside}' / 'rsd' / f'{rangemin}_{rangemax}_{N_bins}' / f'{binmin}_{binmax}' / '0' # For convenience I set RSD to True and also 0 as the box number (only one box for real data)
output_dir.mkdir(parents=True, exist_ok=True)

path = output_dir / f'{0}'
path.mkdir(exist_ok=True)

ipix = [i for i in range(12)]

input_data = (input_dir / 'QSO_clustering.dat.fits')
assert input_data.is_file()

input_randoms = [input_dir / f'QSO_{i}_clustering.ran.fits' for i in range(18)]
for _file in input_randoms:
    assert _file.is_file()

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

srun CoLoRe_corrf_run_correlations --data {str(input_data)} --data-format zcat --randoms {' '.join(map(str, input_randoms))} --out-dir {str(path)} --log-level DEBUG --nthreads ${{SLURM_CPUS_PER_TASK}} --zmin-covd 0.79 --zmax-covd 3.8 --zstep-covd 0.005 --zmin {binmin} --zmax {binmax} --nside 1 --pixel-mask {' '.join(map(str, ipix))} --min-bin {rangemin} --max-bin {rangemax} --n-bins {N_bins} --compute-npoles 0 2 4
        ''')

run_file = path / 'run_corr.sl'
with open(run_file, 'w') as f:
    f.write(body)

if run_sbatch:
    os.chdir(path)
    retcode = call(f'sbatch {run_file}', shell=True)

``` 
--