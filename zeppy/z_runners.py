# Copyright (c) 2021 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
# -*- coding: utf-8 -*-

import tempfile
import witheppy
import eppy
import witheppy.runandget as runandget


def to_zeppy_runandget(idfname, wfile):
    """copies idf and epw file from disk so it can be transferred on the wire"""
    idftxt = open(idfname, "r").read()
    wfiletxt = open(wfile, "r").read()
    return idftxt, wfiletxt


def zeppy_runandget(idftxt, wfiletxt, getdict):
    """writes idftxt and wfiletxt to a tempfile, runs and returns the getdict values"""
    with tempfile.TemporaryDirectory() as tmpdir:
        idf_temp_file = f"{tmpdir}/a.idf"
        open(idf_temp_file, "w").write(idftxt)
        wfile_temp_file = f"{tmpdir}/a.epw"
        open(wfile_temp_file, "w").write(wfiletxt)
        print("saved temp files")
        idf_temp = eppy.openidf(idf_temp_file, epw=wfile_temp_file)
        fullresult = runandget.anon_runandget(idf_temp, getdict)
        print(fullresult)
    return fullresult
