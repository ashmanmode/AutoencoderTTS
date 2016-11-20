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

def genWavSamples(wavFiles,sampFiles):
    io_funcs = BinaryIOCollection()
    for index in range(len(wavFiles)):
        genSamps,frame_number = io_funcs.load_binary_file_frame(sampFiles[index], 80)
        samples_matrix = numpy.zeros(frame_number*80)
        for i in range(int(frame_number)):
            samples_matrix[i*80:(i+1)*80] = genSamps[i,:]
        #Now generate wav using these samples 
        # print samples_matrix
        scaled = numpy.int16(samples_matrix/numpy.max(numpy.abs(samples_matrix)) * 32767)
        scipy.io.wavfile.write(wavFiles[index],16000,scaled)
        print 'Writing .swav for ',sampFiles[index]

def genCombined(outFiles,wavFiles,combFiles,wavFactor):
    io_funcs = BinaryIOCollection()
    for index in range(len(wavFiles)):
        fs,data = scipy.io.wavfile.read(outFiles[index])
        fs1,data1 = scipy.io.wavfile.read(wavFiles[index])
        num_samples = min(data.shape[0],data1.shape[0])
        # print num_samples
        samples_matrix = numpy.zeros(num_samples,dtype=float)
        for i in range(num_samples):
            samples_matrix[i] = wavFactor*data1[i]+(1.0-wavFactor)*data[i]
        #Now generate wav using these samples 
        scaled = numpy.int16(samples_matrix/numpy.max(numpy.abs(samples_matrix)) * 32767)
        scipy.io.wavfile.write(combFiles[index],16000,scaled)
        print 'Writing .cwav for ',combFiles[index]

if __name__ == '__main__':
    
	#argv 1 = file of list of names
	#argv 2 = wav dir

    if len(sys.argv) != 3:
        logger.critical('usage: genSamples.sh [config file names]')
        sys.exit(1)

    file_id_list_file = sys.argv[1]
    wav_dir = sys.argv[2]

    files = read_file_list(file_id_list_file);
    wavFiles = prepare_file_path_list(files,wav_dir,'.wav',True);
    sampFiles = prepare_file_path_list(files,wav_dir,'.samp',True);
    outFiles = prepare_file_path_list(files,wav_dir,'.swav',True);
    combFiles = prepare_file_path_list(files,wav_dir,'.cwav',True);
    # print wavFiles
    # print genSampFiles
    
    genWavSamples(outFiles,sampFiles)
    wavFactor = 0.8
    genCombined(outFiles,wavFiles,combFiles,wavFactor)

    