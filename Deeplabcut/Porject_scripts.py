import deeplabcut

## This is the list of videos that I want to analyze
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

videos_c57 = ['D:\\Documents\\DOUTORADO\\Padronizacao_sala_de_comportamento\\Videos\\c57\\B-MVI_2114.mp4',
              'D:\\Documents\\DOUTORADO\\Padronizacao_sala_de_comportamento\\Videos\\c57\\B-MVI_2116.mp4',
              'D:\\Documents\\DOUTORADO\\Padronizacao_sala_de_comportamento\\Videos\\c57\\B-MVI_2117.mp4']


## To create a new deeplabcut project
config_path = deeplabcut.create_new_project('behavior', 
                                            'Matheus', 
                                            videos_c57, 
                                            working_directory='D:\\Documents\\DOUTORADO\\Padronizacao_sala_de_comportamento\\Network_models\\behavior-09-02-2023', 
                                            copy_videos=True, 
                                            multianimal=False,
                                            )

## To extract frames manually from the videos
deeplabcut.extract_frames(config_path, 'manual')

## To label the frames
deeplabcut.label_frames(config_path)

