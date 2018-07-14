# -*- coding: utf-8 -*-
import os

from hansel import Crumb
from neuro_pypes.run import run_debug
from neuro_pypes.config import update_config
from neuro_pypes.io import build_crumb_workflow
from neuro_pypes.anat import attach_spm_anat_preprocessing
from neuro_pypes.dmri import attach_spm_fsl_dti_preprocessing

# MATLAB - Specify path to current SPM and the MATLAB's default mode
from nipype.interfaces.matlab import MatlabCommand
MatlabCommand.set_default_paths('/usr/local/MATLAB/R2014a/toolbox/spm12')
MatlabCommand.set_default_matlab_cmd("matlab -nodesktop -nosplash")
# FreeSurfer - Specify the location of the freesurfer folder
from nipype.interfaces.freesurfer import FSCommand
fs_dir = '/volume/DTI/freesurfer'
FSCommand.set_default_subjects_dir(fs_dir)

# root path to my data
base_dir = "/volume/DTI/Data"

# the configuration file path
config_file = os.path.join(os.path.dirname(base_dir), 'pypes_config.yml')

# define the Crumb filetree of my image database
data_path = os.path.join(base_dir, "{subject_id}", "{modality}", "{image}")

# create the filetree Crumb object
data_crumb = Crumb(data_path, ignore_list=[".*"])

# the different worflows that I will use with any given name
attach_functions = {"spm_anat_preproc": attach_spm_anat_preprocessing,
                    "spm_fsl_dti_preprocessing": attach_spm_fsl_dti_preprocessing,}


# the specific parts of the `data_crumb` that define a given modality.
# **Note**: the key values of this `crumb_arguments` must be the same as expected
# in the functions in `attach_functions`.
crumb_arguments = {'anat': [('modality', 'anat_1'),
                            ('image',    'mprage.nii.gz')],
                   'diff': [('modality', 'diff_1'),
                            ('image',   'DTI.nii')],
                   'bval': [('modality', 'diff_1'),
                            ('image',   'DTI.bval')],
                   'bvec': [('modality', 'diff_1'),
                            ('image',   'DTI.bvec')],
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
