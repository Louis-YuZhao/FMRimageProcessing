import os.path as path

from hansel import Crumb
from neuro_pypes.datasets import cobre_crumb_workflow
from neuro_pypes.run import run_debug

# we downloaded the database in:
base_dir = '/home/louis/Downloads/FMRI/Baltimore_2'
cobre_tree = path.join('{subject_id}', '{modality}', '{image}')

# we define the database tree
cobre_crumb = Crumb(path.join(base_dir, cobre_tree), ignore_list=['.*'])

# output and working dir
output_dir = path.join(path.dirname(base_dir), 'out')
cache_dir  = path.join(path.dirname(base_dir), 'wd')

# we have a configuration file in:
config_file = path.join(path.dirname(base_dir), 'pypes_config.yml')

# we choose what pipeline set we want to run.
# the choices are: 'spm_anat_preproc', 'spm_rest_preproc'
wf_name = 'spm_anat_preproc' # for MPRAGE and rs-fMRI preprocessing

# instantiate the workflow
wf = cobre_crumb_workflow(wf_name     = wf_name,
                          data_crumb  = cobre_crumb,
                          cache_dir   = cache_dir,
                          output_dir  = output_dir,
                          config_file = config_file
                         )
# run it
run_debug(wf, plugin='MultiProc', n_cpus=4)