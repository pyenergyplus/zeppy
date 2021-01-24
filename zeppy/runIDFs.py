# Copyright (c) 2020 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
# -*- coding: utf-8 -*-
"""use runIDFs from eppy to make the runs"""

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


def make_options(idf):
    idfversion = idf.idfobjects["version"][0].Version_Identifier.split(".")
    idfversion.extend([0] * (3 - len(idfversion)))
    idfversionstr = "-".join([str(item) for item in idfversion])
    fname = idf.idfname
    options = {
        "ep_version": idfversionstr,
        "output_prefix": os.path.basename(fname).split()[0],
        "output_suffix": "C",
        "output_directory": os.path.dirname(fname),
    }
    return options


@measure
def runsomefiles():
    fnames = [
        # "./eplus_files/f1/Minimal.idf",
        "./eplus_files/f2/UnitHeaterGasElec.idf",
        "./eplus_files/f3/ZoneWSHP_wDOAS.idf",
        "./eplus_files/f4/ZoneWSHP_wDOAS_1.idf",
    ]
    wfile = (
        "/Applications/EnergyPlus-9-1-0/WeatherData/USA_CO_Golden-NREL.724666_TMY3.epw"
    )
    idfs = [eppy.openidf(fname, epw=wfile) for fname in fnames]
    idfs_options = []
    for idf in idfs:
        options = make_options(idf)
        idfs_options.append([idf, options])
    processors = 3
    eppy.runner.run_functions.runIDFs(idfs_options, processors)


if __name__ == "__main__":
    runsomefiles()
