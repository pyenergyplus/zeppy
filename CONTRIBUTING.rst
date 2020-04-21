.. highlight:: shell

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/santoshphilip/zeppy/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

zeppy could always use more documentation, whether as part of the
official zeppy docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/santoshphilip/zeppy/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `zeppy` for local development.

1. Fork the `zeppy` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/zeppy.git

3. Install your local copy into a virtualenv. Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development::

    $ mkvirtualenv zeppy
    $ cd zeppy/
    $ python setup.py develop

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass flake8 and the
   tests, including testing other Python versions with tox::

    $ flake8 zeppy tests
    $ python setup.py test or pytest
    $ tox

   To get flake8 and tox, just pip install them into your virtualenv.

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 3.5, 3.6, 3.7 and 3.8, and for PyPy. Check
   https://travis-ci.com/santoshphilip/zeppy/pull_requests
   and make sure that the tests pass for all supported Python versions.

Tips
----

To run a subset of tests::

$ pytest tests.test_zeppy


Collective Code Construction Contract
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

https://rfc.zeromq.org/spec:42/C4/

Steps for making updates to the software, based on C4 document above:

- *User*:
    - Opens an issue in issue tracker, describing problem (called issue #n)
- *Contributer*:
    - forks the repository
    - makes changes
    - commits with appropriate commit following message
      ::
      
        fixed issue #n (*on first line*)
        
        Problem: describe Problem
        Solution: describe Solution

    - Make a pull request
- *Maintianer*:
    - Merge pull request into master
- *User*:
    - Closes issue #n in issue tracker

After the merge, The *Contributer* may want to take the following steps:

- *Contributer*: pull the changes from pyenergyplus/eppy3000 *Maintainer* has completed the merge
    - This has to be done in the command line
      ::

        git pull --rebase upstream master


    - To do the above you need a remote called `upstream`. You can set this up by the following line in the command line
      ::

        git remote add upstream https://github.com/pyenergyplus/zeppy.git
        # this needs to be done only once

Deploying
---------

A reminder for the maintainers on how to deploy.
Make sure all your changes are committed (including an entry in HISTORY.rst).
Then run::

$ bump2version patch # possible: major / minor / patch
$ git push
$ git push --tags

Travis will then deploy to PyPI if tests pass.
