.. YASP - Yet another Stock Performance Analysis documentation master file, created by
   sphinx-quickstart on Sun Nov  3 12:10:42 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

YASP - Yet another Stock Performance Analysis documentation
===========================================================

Add your content using ``reStructuredText`` syntax. See the
`reStructuredText <https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html>`_
documentation for details.


.. autosummary::
   :toctree: _autosummary
   :template: custom-module-template.rst
   :recursive:

   user_def_link

.. mermaid:: ./test.mmd

.. mermaid::

   sequenceDiagram
      participant Alice
      participant Bob
      Alice->John: Hello John, how are you?
      loop Healthcheck
          John->John: Fight against hypochondria
      end
      Note right of John: Rational thoughts <br/>prevail...
      John-->Alice: Great!
      John->Bob: How about you?
      Bob-->John: Jolly good!

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
