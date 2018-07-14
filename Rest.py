import os

from hansel import Crumb
from neuro_pypes.run import run_debug,run_wf
from neuro_pypes.config import update_config
from neuro_pypes.io import build_crumb_workflow
from neuro_pypes.anat import attach_spm_anat_preprocessing
from neuro_pypes.fmri import attach_rest_preprocessing

# root path to my data
base_dir = '/media/data/louis/ProgramWorkResult/fMRItest/FMRI/Baltimore_2'

# the configuration file path
config_file = os.path.join(os.path.dirname(base_dir), 'pypes_config.yml')

# define the Crumb filetree of my image database
data_path = os.path.join(base_dir, "{subject_id}", "{modality}", "{image}")

# create the filetree Crumb object
data_crumb = Crumb(data_path, ignore_list=[".*"])

# the different worflows that I will use with any given name
attach_functions = {"spm_anat_preproc": attach_spm_anat_preprocessing,
                    "spm_rest_preproc": attach_rest_preprocessing,}

# the specific parts of the `data_crumb` that define a given modality.
# **Note**: the key values of this `crumb_arguments` must be the same as expected
# in the functions in `attach_functions`.
crumb_arguments = {'anat': [('modality', 'anat_1'),
                            ('image',    'mprage.nii.gz')],
                   'rest': [('modality', 'rest_1'),
                            ('image',    'rest.nii.gz')],
                  }

# the pypes configuration file with workflow parameter values
update_config(config_file)

# output and working directory paths
output_dir = os.path.join(os.path.dirname(base_dir), "out")
cache_dir  = os.path.join(os.path.dirname(base_dir), "wd")

# build the workflow
wf = build_crumb_workflow(attach_functions,
                          data_crumb=data_crumb,
                          in_out_kwargs=crumb_arguments,
                          output_dir=output_dir,
                          cache_dir=cache_dir,)

# plot the workflow and then run it
run_wf(wf, plugin="MultiProc", n_cpus=4)