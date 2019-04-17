# import essentia.standard as es
from essentia.standard import FreesoundExtractor, YamlOutput
import os
import numpy as np
import utilities.parsing_tools as prsg
import sys

stats = ['min', 'max', 'median', 'mean', 'var', 'stdev', 'dmean', 'dvar', 'dmean2', 'dvar2']

profile = {
                # 'startTime': float(start_time),
                # 'endTime': float(end_time),
                'lowlevelFrameSize': 2048,
                'lowlevelHopSize': 1024,
                'lowlevelWindowType': 'blackmanharris62',
                'lowlevelSilentFrames': 'noise',
                'lowlevelStats': stats,

                'rhythmMethod': 'degara',
                'rhythmMinTempo': 40,
                'rhythmMaxTempo': 208,
                'rhythmStats': stats,

                'tonalFrameSize': 4096,
                'tonalHopSize': 2048,
                'tonalWindowType': 'blackmanharris62',
                'tonalSilentFrames': 'noise',
                'tonalStats': stats
}

def essentia_lowlevel_features_computation(dir,file) :
    # audio_in = dir + file + ".wav"
    audio_in = dir + file
    print(audio_in)
    # features, features_frames = es.FreesoundExtractor(**profile)(audio_in)
    features, features_frames = FreesoundExtractor(**profile)(audio_in)
    file_json = file+".json"
    # es.YamlOutput(filename=file_json, format='json')(features)
    YamlOutput(filename=file_json, format='json')(features)

    tab_header = []
    tab_value = []

    features_name = sorted(features.descriptorNames())
    for feat in range(0,len(features_name)):
        name_feature = features_name[feat]
        kind_of_feature = name_feature.split(".")

        # CAT1 - ALL FEATURES
        # if(kind_of_feature[0] != 'metadata' and
            # kind_of_feature[1] != 'silence_rate_60dB' and
            # kind_of_feature[1] != 'sound_start_frame' and
            # kind_of_feature[1] != 'sound_stop_frame' and
            # kind_of_feature[1] != 'beats_position' and
            # kind_of_feature[1] != 'bpm_intervals' and
            # kind_of_feature[1] != 'onset_times' and
            # kind_of_feature[1] != 'chords_key' and
            # kind_of_feature[1] != 'chords_progression' and
            # kind_of_feature[1] != 'chords_scale' and
            # kind_of_feature[1] != 'key_edma' and
            # kind_of_feature[1] != 'key_krumhansl' and
            # kind_of_feature[1] != 'key_temperley'):

        # CAT2 - LOWLEVEL FEATURES
        if(kind_of_feature[0] != 'metadata' and
            kind_of_feature[0] == 'lowlevel' and
            kind_of_feature[1] != 'silence_rate_60dB' and
            kind_of_feature[1] != 'sound_start_frame' and
            kind_of_feature[1] != 'sound_stop_frame'):

        # CAT3 - RHYTHM FEATURES
        # if(kind_of_feature[0] != 'metadata' and
            # kind_of_feature[0] == 'rhythm' and
            # kind_of_feature[1] != 'beats_position' and
            # kind_of_feature[1] != 'bpm_intervals' and
            # kind_of_feature[1] != 'onset_times' and):

        # CAT4 - SFX FEATURES
        # if(kind_of_feature[0] != 'metadata' and
            # kind_of_feature[0] == 'sfx'):

        # CAT5 - TONAL FEATURES
        # if(kind_of_feature[0] != 'metadata' and
            # kind_of_feature[0] == 'tonal' and
            # kind_of_feature[1] != 'chords_key' and
            # kind_of_feature[1] != 'chords_progression' and
            # kind_of_feature[1] != 'chords_scale' and
            # kind_of_feature[1] != 'key_edma' and
            # kind_of_feature[1] != 'key_krumhansl' and
            # kind_of_feature[1] != 'key_temperley'):

        # CAT6 - MFCC
        # if(kind_of_feature[1] == "mfcc" and kind_of_feature[2] == "mean"):

            tmp = features[name_feature]
            # print(type(tmp))
            if(type(tmp) is np.ndarray):
                dim = tmp.shape
                if(len(dim) == 2):
                    # dimension
                    cpt=0
                    for i in range(0,dim[1]) :
                        for j in range(0,dim[0]) :
                            tab_header.append(name_feature+"_"+str(i)+"_"+str(j))
                            tab_value.append(tmp[i,j])
                else:
                    dim = tmp.shape
                    for k in range(0,dim[0]):
                        tab_header.append(name_feature+"_"+str(k))
                        tab_value.append(tmp[k])
            else:
                tab_header.append(name_feature)
                tab_value.append(tmp)

    # print(len(tab_header))
    # print(len(tab_value))
    # print(tab_header)
    # print(tab_value)

    header = ""
    # vals = str(file)+","+str(classification)+","
    vals = ""
    for h in range(0,len(tab_header)):
        header += str(tab_header[h])+","
    for v in range(0,len(tab_value)):
        vals += str(tab_value[v])+","

    header = header[:-1]
    vals = vals[:-1]
    # print(len(header.split(",")))
    # print(len(vals.split(",")))
    res=vals.split(",")

    if os.path.exists(file_json):
        os.remove(file_json)

    # print(res)
    return res


    #  MAIN
# arguments = sys.argv
# essentia_lowlevel_features_computation(arguments[1],arguments[2])
