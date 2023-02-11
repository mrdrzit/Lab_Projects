import deeplabcut


## To clear the screen

import os
clear = os.system('cls')

# ----------------------------------------------------------------------------------------------------------

## This is the list of videos that I want to analyze

# This path is for the laptop
videos_cd1 = ['D:\\Documents\\DOUTORADO\\Padronizacao_sala_de_comportamento\\Videos\\cd1\\MVI_2121.mp4',
              'D:\\Documents\\DOUTORADO\\Padronizacao_sala_de_comportamento\\Videos\\cd1\\MVI_2122.mp4',
              'D:\\Documents\\DOUTORADO\\Padronizacao_sala_de_comportamento\\Videos\\cd1\\MVI_2123.mp4',
              'D:\\Documents\\DOUTORADO\\Padronizacao_sala_de_comportamento\\Videos\\cd1\\MVI_2124.mp4',
              'D:\\Documents\\DOUTORADO\\Padronizacao_sala_de_comportamento\\Videos\\cd1\\MVI_2125.mp4',
              'D:\\Documents\\DOUTORADO\\Padronizacao_sala_de_comportamento\\Videos\\cd1\\MVI_2126.mp4',
              'D:\\Documents\\DOUTORADO\\Padronizacao_sala_de_comportamento\\Videos\\cd1\\MVI_2127.mp4',
              'D:\\Documents\\DOUTORADO\\Padronizacao_sala_de_comportamento\\Videos\\cd1\\MVI_2128.mp4',
              'D:\\Documents\\DOUTORADO\\Padronizacao_sala_de_comportamento\\Videos\\cd1\\MVI_2129.mp4',
              'D:\\Documents\\DOUTORADO\\Padronizacao_sala_de_comportamento\\Videos\\cd1\\MVI_2130.mp4',
              'D:\\Documents\\DOUTORADO\\Padronizacao_sala_de_comportamento\\Videos\\cd1\\MVI_2131.mp4',
              'D:\\Documents\\DOUTORADO\\Padronizacao_sala_de_comportamento\\Videos\\cd1\\MVI_2132.mp4',
              'D:\\Documents\\DOUTORADO\\Padronizacao_sala_de_comportamento\\Videos\\cd1\\MVI_2133.mp4',
              'D:\\Documents\\DOUTORADO\\Padronizacao_sala_de_comportamento\\Videos\\cd1\\MVI_2134.mp4',
              'D:\\Documents\\DOUTORADO\\Padronizacao_sala_de_comportamento\\Videos\\cd1\\MVI_2135.mp4',
              'D:\\Documents\\DOUTORADO\\Padronizacao_sala_de_comportamento\\Videos\\cd1\\MVI_2136.mp4']

videos_c57 = ['D:\\Documents\\DOUTORADO\\Padronizacao_sala_de_comportamento\\Videos\\c57\\B-MVI_2116.mp4', # ffplay -i B-MVI_2116.mp4 -vf "crop=989:981:449:43"
              'D:\\Documents\\DOUTORADO\\Padronizacao_sala_de_comportamento\\Videos\\c57\\B-MVI_2117.mp4'] # ffplay -i B-MVI_2117.mp4 -vf "crop=989:981:449:43"

# ----------------------------------------------------------------------------------------------------------

## Path for the videos on home computer
videos_c57 = ["D:\\DLC_test\\Videos\\C57\\B-MVI_2116.mp4", "D:\\DLC_test\\Videos\\C57\\B-MVI_2117.mp4"] # ffplay -i B-MVI_2117.mp4 -vf "crop=989:981:449:43"
videos_c57_cropped = ["D:\\DLC_test\\Videos\\c57\\B-MVI_2116_cropped.mp4", "D:\\DLC_test\\Videos\\c57\\B-MVI_2117_cropped.mp4"] 

# ----------------------------------------------------------------------------------------------------------

## Config path
config_path = "D:\\DLC_test\\behavior-home-09-02-2023\\config.yaml"
config_path = "D:\\DLC_test\\downsample_test\\behavior-Matheus-2023-02-11"

## To create a new deeplabcut project
config_path = deeplabcut.create_new_project('behavior', 'Matheus', videos_c57, working_directory='D:\\Documents\\DOUTORADO\\Padronizacao_sala_de_comportamento\\Network_models\\behavior-09-02-2023', copy_videos=True, multianimal=False)
config_path = deeplabcut.create_new_project('behavior', 'Matheus', videos_c57_cropped, working_directory='D:\\DLC_test\\downsample_test', copy_videos=True, multianimal=False)
config_path = "D:\\DLC_test\\downsample_test\\behavior-Matheus-2023-02-11\\config.yaml"
## To extract frames manually from the videos
deeplabcut.extract_frames(config_path, 'manual', videos_c57_cropped)

## To label the frames
deeplabcut.label_frames(config_path)

## To check the labeled frames
deeplabcut.check_labels(config_path, visualizeindividuals=False, draw_skeleton=True)

## To create the training dataset
deeplabcut.create_training_dataset(config_path, augmenter_type='imgaug')

## To train the network
deeplabcut.train_network(config_path, shuffle=1, gputouse=0, max_snapshots_to_keep=3,  autotune=False, allow_growth=True)

## To evaluate the network
  # Shuffles: list, optional -List of integers specifying the shuffle indices of the training dataset. The default is [1]
  # plotting: bool, optional -Plots the predictions on the train and test images. The default is `False`; if provided it must be either `True` or `False`
  # show_errors: bool, optional -Display train and test errors. The default is `True`
  # comparisonbodyparts: list of bodyparts, Default is all -The average error will be computed for those body parts only (Has to be a subset of the body parts).
  # gputouse: int, optional -Natural number indicating the number of your GPU (see number in nvidia-smi). If you do not have a GPU, put None. See: https://nvidia.custhelp.com/app/answers/detail/a_id/3751/~/useful-nvidia-smi-queries
deeplabcut.evaluate_network(config_path, plotting=True)

## To analyze the videos
deeplabcut.analyze_videos(config_path, videos_c57[0], videotype='.mp4', trainingsetindex=0, gputouse=0, save_as_csv=True, draw_skeleton=True, allow_growth=True)

## Option with the dynamic cropping enabled
deeplabcut.analyze_videos(config_path, videos_c57[0], videotype='.mp4', trainingsetindex=0, gputouse=0, save_as_csv=True, draw_skeleton=True, allow_growth=True, dynamic=(True,.5,10))

## To filter the pose data 
deeplabcut.filterpredictions(config_path, videos_c57[0], shuffle=1, trainingsetindex=0, comparisonbodyparts='all', filtertype='arima', p_bound=0.01, ARdegree=3, MAdegree=1, alpha=0.01)

## To plot trajectories
deeplabcut.plot_trajectories(config_path, videos_c57[0])

## Options in the plot_trajectories function
deeplabcut.plot_trajectories(config_path, videos_c57, shuffle=1, trainingsetindex=0, filtered=True, showfigures=False, imagetype='.png', resolution=100, linewidth=1.0, track_method='')

## To create a video with the trajectories
deeplabcut.create_labeled_video(config_path, videos_c57, shuffle=1, trainingsetindex=0, filtered=True,  save_frames=False, draw_skeleton=True)

## To extract the esqueleton from the videos
deeplabcut.analyzeskeleton(config_path, videos_c57, shuffle=1, trainingsetindex=0, save_as_csv=False)
