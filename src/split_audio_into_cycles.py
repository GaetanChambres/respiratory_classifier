
#  ██  ██      ███████ ██████  ██      ██ ████████ ████████ ██ ███    ██  ██████
# ████████     ██      ██   ██ ██      ██    ██       ██    ██ ████   ██ ██
#  ██  ██      ███████ ██████  ██      ██    ██       ██    ██ ██ ██  ██ ██   ███
# ████████          ██ ██      ██      ██    ██       ██    ██ ██  ██ ██ ██    ██
#  ██  ██      ███████ ██      ███████ ██    ██       ██    ██ ██   ████  ██████

###########################################################################
# When using this script, you will take all the resp. records in a given directory (argument 1)
# and the given input csvfile (argument 2) and will
# split all the records into audio samples for each resp cycles
#
# So in the input folder, this script will add :
# -- a folder named "splitted_into_cycles" containing audio files
# -- each audio file in this folder corresponds to a resp. cycle
###########################################################################

import sys
import os
import csv
import pydub
from progressbar import ProgressBar
import utilities.parsing_tools as prsg

###########################################################################
# Function that splits full resp. records into resp. cycles
# It takes a input directory, a csv file and an output directory
#
# All the sub-samples are saved in the given output directory
###########################################################################
def split_record_in_cycle(dir,file_csv,output_dir) :
    pbar = ProgressBar()
    lines = prsg.nb_lines(file_csv)
    with open(file_csv, newline='') as csvfile:
        data = list(csv.reader(csvfile))
    # print(data)
    input_dir = prsg.ordering_files(dir)
    # print(input_dir)
    i=0
    for filename in pbar(input_dir):
        if(filename.endswith('.wav')):
            cpt=1
            save_file_name = filename[:-4]
            print()
            filename = data[i][0]
            while data[i][0] == save_file_name:
                print("Processed record = "+data[i][0]+" nb cycle = "+str(cpt))
                myaudio = pydub.AudioSegment.from_wav(dir+data[i][0]+".wav")
                chunk_data = myaudio[int(float(data[i][1])*1000):int(float(data[i][2])*1000)]
                saved_file = (output_dir+save_file_name+"_"+f"{cpt:02d}"+".wav")
                # print("saved cycle name = "+saved_file)
                chunk_data.export(saved_file, format="wav")
                i+=1
                cpt+=1
                if i == lines:
                    break
    return i

###########################################################################

#  ██  ██      ███    ███  █████  ██ ███    ██
# ████████     ████  ████ ██   ██ ██ ████   ██
#  ██  ██      ██ ████ ██ ███████ ██ ██ ██  ██
# ████████     ██  ██  ██ ██   ██ ██ ██  ██ ██
#  ██  ██      ██      ██ ██   ██ ██ ██   ████

###########################################################################

arguments = sys.argv
if len(arguments) != 3:
    print("Usage Error : wrong argument number")
    print("Usage : \n arg1 = path_to_data_folder -with wav and txt inside- \n arg2 = path_to_csv_info_file")
    sys.exit()
directory = arguments[1]
csv_info = arguments[2]
sample_save_place = directory+"splitted_into_cycles/"
os.makedirs(sample_save_place, exist_ok=True)

total = split_record_in_cycle(directory,csv_info,sample_save_place)
print()
print("All files splitted :")
print(str(total)+" samples saved in "+sample_save_place )

###########################################################################
