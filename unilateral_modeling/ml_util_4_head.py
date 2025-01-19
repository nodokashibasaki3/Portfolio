import numpy as np
import os
import pandas as pd

import tensorflow as tf
from tensorflow.keras import datasets, layers, models
import matplotlib.pyplot as plt
import tensorflow.keras.backend as kb
import time
# import model_util
from tensorflow.keras.callbacks import CSVLogger
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)


class CustomError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def get_files_to_use(root_folder, subject_nums, sides, trial_nums):
    subject_strings = convert_subject_nums_to_strings(subject_nums)
    trial_strings = convert_trial_nums_to_strings(trial_nums)
    files_to_use = []
    for subject_string in subject_strings:
        subject_folder = os.path.join(root_folder, subject_string)
        filenames = os.listdir(subject_folder)
        for side in sides:
            for trial_string in trial_strings:
                for f in filenames:
                    if side in f and trial_string in f:
                        files_to_use.append(os.path.join(subject_folder, f))
    return(files_to_use)


def convert_trial_nums_to_strings(list_of_trial_nums: int):
    mystrings = []
    for num in list_of_trial_nums:
        if num < 10:
            mystrings.append('T0' + str(num))
        else:
            mystrings.append('T' + str(num))
    return mystrings


def convert_subject_nums_to_strings(list_of_subject_nums: int):
    mystrings = []
    for num in list_of_subject_nums:
        if num < 10:
            mystrings.append('S0' + str(num))
        else:
            mystrings.append('S' + str(num))
    return mystrings


def custom_loss(y_actual, y_pred):
    mask = kb.greater_equal(y_actual, 0)
    mask = tf.cast(mask, tf.float32)
    custom_loss = tf.math.reduce_sum(
        kb.square(mask*(y_actual-y_pred)))/tf.math.reduce_sum(mask)
    return custom_loss

def load_file(myfile):
    stance_phase_to_get = 'TM_Stance_Phase'
    df = pd.read_csv(myfile, usecols=['accel_x', 'accel_y', 'accel_z', 'gyro_x', 'gyro_y',
                     'gyro_z', 'ankle_angle', 'ankle_velocity', 'Ramp', 'Velocity', 'TM_Is_Stance_Phase', stance_phase_to_get])
    
    # first_heel_strike_index_found = False
    
    # for i in range(len(df)):
    #     if df['TM_Is_Stance_Phase'][i] == 1 and not first_heel_strike_index_found:
    #         first_heel_strike_index, first_heel_strike_index_found = i, True
    #         break
    
    # if (not first_heel_strike_index_found): raise CustomError('Something is Wrong with the Left & Right File!!!')
    
    # df = df[first_heel_strike_index:df.index[-1]]
    # if 'LEFT' in myfile:
    #     df.insert(8, 'is_left', value=1)
    # else:
    #     df.insert(8, 'is_left', value=0)
    return df.values