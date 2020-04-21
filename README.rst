=====
zeppy
=====


.. image:: https://img.shields.io/pypi/v/zeppy.svg
        :target: https://pypi.python.org/pypi/zeppy

.. image:: https://img.shields.io/travis/santoshphilip/zeppy.svg
        :target: https://travis-ci.com/santoshphilip/zeppy

.. image:: https://readthedocs.org/projects/zeppy/badge/?version=latest
        :target: https://zeppy.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




distributed processing for eppyy


* Free software: Mozilla Public License 2.0 (MPL-2.0)
* Documentation: https://zeppy.readthedocs.io.


Vision
------

To run eppy on multiple nodes in parallel and collect the results.

So what is a node and why would you want to do this ?

A node can be any or all of the following:

- a process (such E+ running on a single core on a multi-core computer)
    - so we can do multi-processing and run it on many cores on a single computer
- a computer
    - so we can run it on multiple computers that are on the same network
- a group of group of computer in a local network 
    - So we can run multiple groups of machines that may be at different locations on different local networks
    - This can also be computers at different cloud locations
    - a single computer in the local network may act as an access node 
    
Features
--------

Do the distributed processing with a single function call and get all the results back. 

Sample code ::
    
    import zeppy
    
    result = zeppy.zmq_parallelpipe(runfunction, 
                                    args_list, 
                                    nworkers=None)

    # runfunction is a function you will write, 
        # that may run idf.run(), 
        # gather the total energy use and retrn it
    # args_list = {args: [idf1, idf2, idf3, ...]}
        # list of files to run
    # if nworkers=None: 
        # it will start up as many nodes as there are items in args_list
        # if you don't have enough nodes avaliable, you can set nworkers=n.
        # it will start up n nodes and queue up the runs evenly on the nodes
    

For example the above code can do the following:

- ``runfunction`` will run the *idf* file, and return the *total energy usage*
- ``result`` will be a list *total energy usage* in the same order as the items in  ``args_list``
- see the comments in the code for greater clarity

Why is the function called ``zmq_parallelpipe`` ?

- This package uses `ZeroMQ Library <https://zeromq.org>`_
- **Parallel Pipeline** is a fundamental pattern in it

This is the first pass at the API. It doesn't work yet - Ha!. But there is hope :-)




Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
