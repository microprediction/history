from microprediction import MicroReader
import os
import random
import time
import pathlib
import time
import pandas as pd

RECENT_CSV = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + 'recent' + os.path.sep
mr = MicroReader()
STREAMS = [ n for n in mr.get_stream_names() ]

MB_LIMIT = 20.  # Github file size limit is 25MB to be safe 

def append_random():
      """ Pick a random stream and update the history """
      name = random.choice(STREAMS)
      chrono_csv = RECENT_CSV + name.replace('.json','.csv') 
      # Find time of update
      fchrono = pathlib.Path(chrono_csv)
      if fchrono.exists():
           existing_df = pd.read_csv(chrono_csv)
           modification_time = os.path.getmtime(chrono_csv)
           seconds = time.time()-modification_time 
           print('Seconds since modification: '+str(seconds))   
           existing = [ (t,v) for t,v in zip(existing_df['time'].values, existing_df['value'].values) ] 
           appended = mr.append_chrono(chrono=existing, name=name)
      else:
         seconds_since_modification = 24*60*60
         appended = list(reversed( mr.get_lagged(name=name, count=2000) ))

      df_new = pd.DataFrame(columns=['time','value'])
      df_new['time'] = [t for (t,v) in appended]
      df_new['value'] = [v for (t,v) in appended] 
      df_new.to_csv(chrono_csv) 
      
      # Check size of file 
      mb = os.path.getsize(chrono_csv)/(1024*1024)
      if mb>MB_LIMIT:
         # If we approach the file size limit, shuffle to the archive 
         older = df_new[:-10]
         newer = df_new[-10:] 
         older_csv = chrono_csv.replace('recent','older').replace('.csv','_'+time.strftime('%Y%m%d')+'.csv')
         older.to_csv(older_csv)
         newer.to_csv(chrono_csv)
            
         

if __name__=='__main__':
    for _ in range(100):
        append_random()
