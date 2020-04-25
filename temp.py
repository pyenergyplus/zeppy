import eppy

from functools import wraps
import time
import os.path

def measure(func):
    @wraps(func)
    def _time_it(*args, **kwargs):
        start = int(round(time.time() * 1000))
        try:
            return func(*args, **kwargs)
        finally:
            end_ = int(round(time.time() * 1000)) - start
            print(f"Total execution time: {end_ if end_ > 0 else 0} ms")
    return _time_it
    

@measure
def runsomefiles():
    fnames = [
        # "./eplus_files/f1/Minimal.idf",
            "./eplus_files/f2/UnitHeaterGasElec.idf",
            "./eplus_files/f3/ZoneWSHP_wDOAS.idf",
            "./eplus_files/f4/ZoneWSHP_wDOAS_1.idf",
            ]
    wfile = "/Applications/EnergyPlus-9-1-0/WeatherData/USA_CO_Golden-NREL.724666_TMY3.epw"
    idfs = [[eppy.openidf(fname, epw=wfile), 
            {
                'ep_version':'9-1-0',
                'output_prefix':os.path.basename(fname).split()[0], 
                'output_directory':os.path.dirname(fname),
            }
        ] 
    for fname in fnames]
    processors = 3
    print(f'processors={processors}')
    eppy.runner.run_functions.runIDFs(idfs, processors) 
    
    
if __name__ == '__main__':
    runsomefiles()    