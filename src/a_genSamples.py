import wave, struct
import numpy
import scipy                 # this works
import scipy.io 
import math             # this does NOT work
from scipy.io import wavfile
import os, sys, errno

from io_funcs.binary_io import  BinaryIOCollection

def extract_file_id_list(file_list):
    file_id_list = []
    for file_name in file_list:
        file_id = os.path.basename(os.path.splitext(file_name)[0])
        file_id_list.append(file_id)

    return  file_id_list

def read_file_list(file_name):

    file_lists = []
    fid = open(file_name)
    for line in fid.readlines():
        line = line.strip()
        if len(line) < 1:
            continue
        file_lists.append(line)
    fid.close()

    return  file_lists


def make_output_file_list(out_dir, in_file_lists):
    out_file_lists = []

    for in_file_name in in_file_lists:
        file_id = os.path.basename(in_file_name)
        out_file_name = out_dir + '/' + file_id
        out_file_lists.append(out_file_name)

    return  out_file_lists

def prepare_file_path_list(file_id_list, file_dir, file_extension, new_dir_switch=True):
    if not os.path.exists(file_dir) and new_dir_switch:
        os.makedirs(file_dir)
    file_name_list = []
    for file_id in file_id_list:
        file_name = file_dir + '/' + file_id + file_extension
        file_name_list.append(file_name)

    return  file_name_list

def saveSamples(wavFiles,sampFiles):
	io_funcs = BinaryIOCollection()
	for index in range(len(wavFiles)):
		out_data_matrix = None
		fs,data = scipy.io.wavfile.read(wavFiles[index])
		nFrames = int(math.ceil(data.size/80.0))
		out_data_matrix = numpy.zeros((nFrames+2, 80))
		for i in range(nFrames):
			out_data_matrix[i,0:80] = data[i*80:(i+1)*80]
		# print out_data_matrix
		io_funcs.array_to_binary_file(out_data_matrix, sampFiles[index])
		print "Saved to ",sampFiles[index] , out_data_matrix.shape

if __name__ == '__main__':
    
	#argv 1 = file of list of names
	#argv 2 = wav dir
	#argv 3 = samp dir

    if len(sys.argv) != 4:
        logger.critical('usage: genSamples.sh [config file names]')
        sys.exit(1)

    file_id_list_file = sys.argv[1]
    wav_dir = sys.argv[2]
    samp_dir = sys.argv[3]

    files = read_file_list(file_id_list_file);
    wavFiles = prepare_file_path_list(files,wav_dir,'.wav',True);
    sampFiles = prepare_file_path_list(files,samp_dir,'.samp',True);
    
    saveSamples(wavFiles,sampFiles)

    