import os

from hansel import Crumb
from neuro_pypes.run import run_debug
from neuro_pypes.config import update_config
from neuro_pypes.io import build_crumb_workflow
from neuro_pypes.dmri import attach_spm_fsl_dti_preprocessing

# root path to my data
base_dir = "/media/data/louis/ProgramWorkResult/fMRI1/Pre"

# the configuration file path
config_file = "./pypes_config.yml"

# define the Crumb filetree of my image database
data_path = os.path.join(base_dir, "{subject_id}", "{modality}", "{image}")

# create the filetree Crumb object
data_crumb = Crumb(data_path, ignore_list=[".*"])

# the different worflows that I will use with any given name
attach_functions = {"spm_fsl_dti_preprocessing": attach_spm_fsl_dti_preprocessing}

# the specific parts of the `data_crumb` that define a given modality.
# **Note**: the key values of this `crumb_arguments` must be the same as expected
# in the functions in `attach_functions`.
crumb_arguments = {'dti': [('modality', 'DTIImg'),
                            ('image',   'DTI.nii')],
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
                          cache_dir=cache_dir)

# plot the workflow and then run it
run_debug(wf, plugin="MultiProc", n_cpus=4)