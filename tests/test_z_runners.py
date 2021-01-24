"""py.test for z_runners"""

from zeppy import z_runners


# def test_zeppy_runandget():
#     """py.tests to_zeppy_runandget and zeppy_runandget"""
#     idfname = "./idffolder/1ZoneUncontrolled.idf"
#     wfile = "./idffolder/USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw"
#     idftxt, wfiletxt = z_runners.to_zeppy_runandget(idfname, wfile)
#     getdict = getdict = dict(
#         twocells=dict(
#             whichfile="htm",
#             # tableindex=0,  # or tablename
#             tablename="Site and Source Energy",  # tableindex takes priority if both given
#             cells=[[-2, 1], [-2, -2]],  # will return 2 cells
#         ),
#         HTML_file=dict(whichfile="htm", tableindex=0, table=True),
#     )
#     expected = {
#         "HTML_file": {
#             "entirefile": None,
#             "result": [
#                 "Site and Source Energy",
#                 [
#                     [
#                         "",
#                         "Total Energy [GJ]",
#                         "Energy Per Total Building Area [MJ/m2]",
#                         "Energy Per Conditioned Building Area [MJ/m2]",
#                     ],
#                     ["Total Site Energy", 82.43, 354.92, "\xa0"],
#                     ["Net Site Energy", 82.43, 354.92, "\xa0"],
#                     ["Total Source Energy", 261.06, 1124.02, "\xa0"],
#                     ["Net Source Energy", 261.06, 1124.02, "\xa0"],
#                 ],
#             ],
#             "table": True,
#             "tableindex": 0,
#             "whichfile": "htm",
#         },
#         "twocells": {
#             "cells": [[-2, 1], [-2, -2]],
#             "entirefile": None,
#             "result": ["Site and Source Energy", [261.06, 1124.02]],
#             "tablename": "Site and Source Energy",
#             "whichfile": "htm",
#         },
#     }
#     result = z_runners.zeppy_runandget(idftxt, wfiletxt, getdict)
#     assert result == expected
