import os
import csv
import re
import sys
import utilities.parsing_tools as prsg

arguments = sys.argv
if len(arguments) != 4:
    print("Usage Error : wrong argument number")
    print("Usage : \n arg1 = path_to_data_folder -with wav and txt inside- \n arg2 = path_to_diagnostic_file -txt format' \n arg3 = output_csv_name")
    sys.exit()
input_data_dir = arguments[1]
input_info = arguments[2]
output_dir = input_data_dir+"csv/"
os.makedirs(output_dir, exist_ok=True)
output = output_dir+arguments[3]
out_file = open(output, "w")

cpt = 0
# nb_files = (len(os.listdir(input_data_dir)))/2
nb_files = prsg.nb_files(input_data_dir)/2

with open(input_info) as fp:
    diagnostics = fp.read().splitlines()

# ordered_files = sorted(os.listdir(input_data_dir))
ordered_files = prsg.ordering_files(input_data_dir)

for filename in ordered_files :
    if(filename.endswith('txt')):
        cpt+=1
        input = input_data_dir+filename
        input_file = open(input,'r')

        content = input_file.readline()
        file_id = filename[:-4]

        patient_number,record_index,body_area,channel,record_tool = file_id.split("_")
        pathology = 0

        for i in range(0,len(diagnostics)-1):
            tmp_patient, tmp_pathology = diagnostics[i].split("\t")

            if patient_number == tmp_patient:
                if(tmp_pathology == "Asthma"):
                    pathology = 0
                if(tmp_pathology == "LRTI"):
                    pathology = 1
                if(tmp_pathology == "Pneumonia"):
                    pathology = 2
                if(tmp_pathology == "Bronchiectasis"):
                    pathology = 3
                if(tmp_pathology == "Bronchiolitis"):
                    pathology = 4
                if(tmp_pathology == "URTI"):
                    pathology = 5
                if(tmp_pathology == "COPD"):
                    pathology = 6
                if(tmp_pathology == "Healthy"):
                    pathology = 7

        while content:
            start_time,end_time,crackle,wheeze = content.split('\t')

            # out_file.write(patient_number+","+record_index+","+body_area+","+channel+","+record_tool+","+start_time+","+end_time+","+str(pathology)+","+crackle+","+wheeze)
            out_file.write(file_id+","+start_time+","+end_time+","+str(pathology)+","+crackle+","+wheeze)
            content = input_file.readline()
