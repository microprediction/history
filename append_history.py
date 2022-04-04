from microprediction import MicroReader
import os
import random
from copy import deepcopy
STREAM_PATH = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + 'csv' + os.path.sep
import matplotlib.pyplot as plt
import time
import pathlib
import time

mr = MicroReader()
STREAMS = [ n for n in mr.get_stream_names() ]

def append_random():
      """ Pick a random stream and update the history """
      name = random.choice(STREAMS)
      chrono_csv = STREAM_PATH + name.replace('.json','.csv') 
      # Find time of update
      fchrono = pathlib.Path(chrono_csv)
      if fchrono.exists():
           chrono_df = pd.read_csv(chrono_csv)
           modification_time = os.path.getmtime(chrono_csv)
           seconds = time.time()-modification_time 
           chrono = [ (t,v) for t,v in zip(chrono_df['time'].values, chrono_df['value'].values) ] 
           appended = mr.append_chrono(chrono=chrono, seconds=seconds, name=name)
      else:
         seconds_since_modification = 24*60*60
         appended = mr.get_lagged(name=name, count=2000) 

      df_new = pd.DataFrame(columns=['time','value'])
      df_new['time'] = [t for (t,v) in appended]
      df_new['value'] = [v for (t,v) in appended] 
      df_new.to_csv(chrono_csv) 
      

if __name__=='__main__':
    for _ in range(20):
        append_random()
