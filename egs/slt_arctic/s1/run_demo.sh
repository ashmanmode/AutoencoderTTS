#!/bin/bash -e

if test "$#" -ne 0; then
    echo "Usage: ./run_demo.sh"
    exit 1
fi

### Step 1: setup directories and the training data files ###
echo "Step 1: setting up experiments directory and the training data files..."
global_config_file=conf/global_settings.cfg

if [ ! -f  $global_config_file ]; then
    echo "Global config file doesn't exist"
    exit 1
else
    source $global_config_file
fi

## Doing basic setup of inp files  #Just unzips the data
./scripts/setup.sh slt_arctic_demo

# # ##add samp filse
# file_of_ids=experiments/slt_arctic_demo/acoustic_model/data/${FileIDList}
# samp_dir=experiments/slt_arctic_demo/acoustic_model/data/samp
# wav_dir=slt_arctic_demo_data/wav
# python ${MerlinDir}/src/a_genSamples.py $file_of_ids $wav_dir $samp_dir 

# ./scripts/prepare_config_files.sh $global_config_file

# ./scripts/prepare_config_files_for_synthesis.sh $global_config_file

# ## Step 2: train duration model ###
# # Finding ideal phone duration for each phone to make the input features
echo "Step 2: training duration model..."
# ./scripts/submit.sh ${MerlinDir}/src/a_run_merlin.py conf/duration_${Voice}.conf

# ### Step 3: train acoustic model ###
echo "Step 3: training acoustic model..."
./scripts/submit.sh ${MerlinDir}/src/a_run_merlin.py conf/acoustic_${Voice}.conf

echo "Acoustic Model Ready!!"

### Step 4: synthesize speech   ###
echo "Step 4: synthesizing speech..."
./scripts/submit.sh ${MerlinDir}/src/a_run_merlin.py conf/test_dur_synth_${Voice}.conf
./scripts/submit.sh ${MerlinDir}/src/a_run_merlin.py conf/test_synth_${Voice}.conf

### Step 5: delete intermediate synth files ###
echo "Step 5: deleting intermediate synthesis files..."
./scripts/remove_intermediate_files.sh conf/global_settings.cfg

echo "synthesized audio files are in: experiments/${Voice}/test_synthesis/wav"
echo "All successfull!! Your demo voice is ready :)"

# ## Generating waveform from samples
# echo "Step 6: Generating Waveforms from samples ...."
# file_of_ids=experiments/slt_arctic_demo/test_synthesis/test_id_list.scp
# wav_dir=experiments/slt_arctic_demo/test_synthesis/wav
# python ${MerlinDir}/src/a_genWavSamples.py $file_of_ids $wav_dir 

