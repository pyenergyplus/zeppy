=======
History
=======

Changes
~~~~~~~

release r0.1.5
~~~~~~~~~~~~~~

2022-12-02
----------

Losts of cleanup for the release

release r0.1.1
~~~~~~~~~~~~~~

Date:   Fri Dec 2 07:41:59 2022 -0800
--------------------------------------

fixed issue #23

:Problem: Need user documentation to reflect TCP version of zeppy
:Solution: User Documentation has been updated


Date:   Thu Dec 1 07:47:13 2022 -0800
--------------------------------------

fixed issue #5

:Problem: need a TCP version of ppipes.py
:Solution: ptcp is the TCP version of ppipes


Date:   Wed Nov 30 22:09:48 2022 -0800
--------------------------------------

fixed issue #20

:Problem: running E+ with zeppy broken
:Solution: eppy was updated as part of fixing this


Date:   Tue Nov 15 14:13:53 2022 -0800
--------------------------------------

fixed issue #18

:Problem: docs/tutorial_docs/eplus_zeppy.ipynb not working
:Solutions: updated it to make it work


Date:   Mon Nov 14 13:19:49 2022 -0800
--------------------------------------

fixed issue #6

:Problem: tutorials are not running when using python3.10 in jupyter notebook
:Solution: updated the tutorial so that they work with python3.10

Details:

- running jupyter notebook is like running the code in an interpreter.
- multiprocessing is not able to run functions defined in the interpreter such as `waitsome`
- These functions are also defined in ppipes.py They can be imported from ppipes and then the tutorial runs without any problems.
- For some reason, this issue kicked in with python3.10


Date:   Sun Jan 24 13:22:00 2021 -0800
--------------------------------------

fixed issue #13

:Problem: do a simple REQ-REP to test anon_runandget in eppy
:Solution: zeppy.eppyREQclient.py and zeppy.eppyREPserver.py do this as documented in ./docs/tutorial_docs/REQ_REP_eppy.rst

Date:   Mon Jul 13 09:41:39 2020 -0700
--------------------------------------

fixed issue #10

:Problem: code examples are not fitting on the screen with html_theme = 'alabaster' in conf.py
:Solution: set html_theme = 'classic'

Date:   Mon Jul 13 09:27:49 2020 -0700
--------------------------------------

fixed issue #8

:Problem: There is some boilerplate that appears when a new issue is opened. It is not relavant to the present state of the code
:Solution: remove .github/ISSUE_TEMPLATE.md

Date:   Sun May 17 23:33:15 2020 -0700
--------------------------------------

fixed issue #3

:Problem: The ipc pipe names are hardcoded. So only one instance can run
:Solution: The pipe names are randomly generated on the fly. So any number of instances can run


0.1.0 (2020-04-19)
------------------

* First release on PyPI.
