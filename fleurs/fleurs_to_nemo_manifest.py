# e.g. $ python3 fleurs_to_nemo_manifest.py /home/kozi/Documents/fleurs
# converts a folder of FLEURS to nemo's manifest JSON style (only the manifest since audio is already wav)

import os                                                                      
import subprocess                                                              
import csv                                                                     
import json                                                                    
                                                                            

def get_wav_duration(file_path):                                               
    cmd = "ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1".split()     
    #cmd = "ffprobe -v error -show_entries format=duration -of                  default=nw=1:nk=1".split()                               
    cmd.append(file_path)                                                      
    output = subprocess.check_output(cmd)                                      
    duration = float(output)                                                   
    return round(duration, 3)                                                  
                                                                            
def main(directory):         
    for item in os.listdir(directory):                                                                    
        language_dir = os.path.join(directory, item)
        if os.path.isdir(language_dir):
            nemo_data = []                                                             
            whisper_data = []
            tsv_file = os.path.join(language_dir, "test.tsv")
            nemo_manifest = os.path.join(language_dir, "nemo_manifest.json")
            whisper_manifest = os.path.join(language_dir, "whisper_manifest.json")

            with open(tsv_file, 'r') as tsv:          
                print("reading file {}".format(tsv_file))                                 
                reader = csv.reader(tsv, delimiter="\t")                               
                for row in reader:                                                     
                    id, file_name, capitalized_transcript, transcript, *_ = row       
                    
                    data_dir = os.path.join(language_dir, "audio/test") 
                    wav_file = os.path.join(data_dir, file_name)                      
                    print("processing file {}".format(wav_file))

                    if os.path.isfile(wav_file) and file_name.endswith('.wav'):        
                        duration = get_wav_duration(wav_file)                          
                        nemo_entry = {                                                       
                            "audio_filepath": os.path.abspath(wav_file),
                            # unfortunately duration is required so ffprobe is necessary, see https://docs.nvidia.com/deeplearning/nemo/user-guide/docs/en/stable/asr/datasets.html#preparing-custom-asr-data               
                            "duration": duration,                                      
                            "text": transcript#.encode('utf-8')                                         
                        }                            
                        whisper_entry =  {
                            "audio_filepath": os.path.abspath(wav_file),
                            "duration": duration,
                            "text": capitalized_transcript
                        }                                  
                        nemo_data.append(nemo_entry)  
                        whisper_data.append(whisper_entry)                                       
                                                                                    
            #with open(json_file, 'w') as json_f:                                       
                #json.dump(json_data, json_f, indent=4)    

            print("writing file {}".format(nemo_manifest))
            with open(nemo_manifest, "w") as fout:
                for m in nemo_data:
                    # ensure_ascii=True is the default and even speech_transcribe will use escaped umlauts, but this way the manifest is human-readable
                    fout.write(json.dumps(m, ensure_ascii=False) + "\n")    

            print("writing file {}".format(whisper_manifest))
            with open(whisper_manifest, "w") as fout:
                for m in whisper_data:
                    # ensure_ascii=True is the default and even speech_transcribe will use escaped umlauts, but this way the manifest is human-readable
                    fout.write(json.dumps(m, ensure_ascii=False) + "\n")  
                                                                            
if __name__ == "__main__":                                                     
    import sys                                                                 
    main(sys.argv[1])
