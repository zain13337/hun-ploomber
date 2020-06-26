"""
Ploomber spec API provides a quick and simple way to use Ploomber using YAML,
it is not indented to replace the Python API which offers more flexibility and
advanced features.

Click here for a live demo.

You can run pipelines with the following command:

.. code-block:: bash

    python -m ploomber.entry pipeline.yaml --action build

To start an interactive session:

.. code-block:: bash

    python -i -m ploomber.entry pipeline.yaml --action status


Or with `ipython` (note the double dash):

.. code-block:: bash

    ipython -i -m ploomber.entry pipeline.yaml -- --action status

Once the interactive session opens you can debug and develop Python tasks by
using the ``dag`` object.


.. code-block:: python

    dag['some_task'].debug()


.. code-block:: python

    dag['some_task'].develop()


Or print the rendered source code from SQL scripts:


.. code-block:: python

    print(dag['some_sql_task'].source)


``pipeline.yaml`` schema
------------------------

Values within {curly brackets} contain explanations, otherwise, they represent
default values.

.. code-block:: yaml

    # pipeline.yaml
    meta:
        # TODO: set default to false for now, we cannot extract product from sql files
        # inspect source code to extract products
        extract_product: True

        # inspect source code to extract upstream dependencies
        extract_upstream: True

        # if any task does not have a "product_class" key, it will look up this
        # dictionary using the task class
        product_default_class:
            SQLDump: File
            NotebookRunner: File
            SQLScript: SQLRelation

    # clients are objects that connect to databases
    clients:
        {task or product class name}: {dotted.path.to.function}

    tasks:
        - {task dictionary, see below}


Notes
-----
* The meta section and clients is optional.
* The spec can also just be a list of tasks for DAGs that don't use clients and do not need to modify meta default values.
* If using a factory, the spec can just be

.. code-block:: yaml

    # pipeline.yaml
    location: {dotted.path.to.factory}

``task`` schema
---------------

.. code-block:: yaml

    # Any of the classes available in the tasks module
    # If missing, it will be inferred from "source".
    # NotebookRunner for .py and .ipynb files, SQLScript for .sql
    # and ShellScript for .sh
    class: {task class, optional}

    source: {path to source file}

    # Products that will be generated upon task execution. Should not exist
    # if meta.extract_product is set to True. This can be a dictionary if
    # the task generates more than one product
    product: {str or dict}

    # Any of the classes available in the products module, if missing, the
    # class is looked up in meta.product_default_class using the task class
    product_class: {str, optional}

    name: {task name, optional}

    # Dotted path to a function that has no parameters and returns the
    # client to use. By default the class-level client at config.clients is
    # used, this value overrides it. Only required for tasks that require
    # clients
    client: {dotted.path.to.function, optional}

    # Same as "client" but applies to the product, most of the time, this will
    # be the same as "client". See the FAQ for more information (link at the
    # bottom)
    product_client: {dotted.path.to.function, optional}

    # Dependencies for this task. Only required if meta.extract_upstream is
    # set to True
    upstream: {str or list, optional}

    # NOTE: All remaining values are passed to the task constructor as keyword
    arguments


Click here to go to :doc:`faq_index/`.
"""