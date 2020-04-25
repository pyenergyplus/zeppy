import eppy

from functools import wraps
import time

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
    fnames = ["./eplus_files/f1/Minimal.idf",
            "./eplus_files/f2/UnitHeaterGasElec.idf",
            "./eplus_files/f3/ZoneWSHP_wDOAS.idf",
            ]
    wfile = "/Applications/EnergyPlus-9-1-0/WeatherData/USA_CO_Golden-NREL.724666_TMY3.epw"
    idfs = [[eppy.openidf(fname, epw=wfile), {'ep_version':'9-1-0'}] for fname in fnames]
    eppy.runner.run_functions.runIDFs(idfs) 
    
    
if __name__ == '__main__':
    runsomefiles()    