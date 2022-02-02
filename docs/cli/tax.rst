regi0 tax
=========

.. code:: text

    regi0 tax

Workflow
********
The :code:`tax` commands executes the following taxonomic verification workflow by default:

1. Read the input file (biological records).

2. Create a new column with the scientific name in canonical form, removing authors, years and classifiers.

3. Query the Global Names Resolver using the scientific name in canonical form and verify whether is correct.

4. (Optional) Add superior taxonomic classification to the records using the information retrieved from Global Names Resolver.

5. (Optional) Identify duplicate records based on a subset of columns in the configuration files. Records with the same values in that subset of columns are considered as duplicates.

6. (Optional) Add one or more categories present in the species checklist to each record. It queries the checklist using the scientific name in canonical form where the name was correct and the suggestion from the verification where the name was incorrect.

7. Save a copy of the input file (biological) records with extra columns indicating flags, suggestions and sources of verification.

Usage
*****
If you execute the :code:`geo` command with the :code:`--help` flag, you will see its usage:

.. code:: text

    regi0 tax --help

prints the following message:

.. code:: text

    Usage: regi0 tax [OPTIONS] INPUT OUTPUT

    Executes a flexible taxonomic verification workflow on a set of biological records.

    Options:
      --data-source-ids TEXT          Data source IDs for GNR. See http://resolver
                                      .globalnames.org/data_sources.json for a
                                      list of available IDs. Multiple IDs must be
                                      separated by commas.  [default: 1]
      --add-taxonomy                  Add superior taxonomy classification.
                                      [default: False]
      --duplicates                    Identify duplicate records.  [default:
                                      False]
      --category [all|alien|endemic|cites|mads|iucn]
                                      Categories from checklist to add to result.
      -r, --remove                    Remove records with flags.  [default: False]
      -q, --quiet                     Silence information logging.  [default:
                                      False]
      --help                          Show this message and exit.

- :code:`INPUT`: Relative or absolute path of the input file (can be csv, txt or xlsx) containing the biological records.

- :code:`OUTPUT`: Relative or absolute path of the output file (can be csv, txt or xlsx) to be created with the results.

- :code:`--data-source-ids`: Data source ID(s) for Global Names Resolver to use. Multiple IDs must be separated by commas. For example:

.. code:: bash

    regi0 tax input.csv output.csv --data-source-ids 1,2,101

By default, it uses only one source (ID:1) which corresponds to Catalogue of Life. A list of all available data sources and their IDs can be found in `http://resolver.globalnames.org/data_sources.json <http://resolver.globalnames.org/data_sources.json>`_.

- :code:`--add-taxonomy`: Add superior taxonomic classification for each record based on the result of Global Names Resolver.

- :code:`--duplicates`: Identify duplicate records based on a subset of columns in the configuration file.

- :code:`--category`: Categories from the species checklist to add. Must be one of `all`, `alien`, `endemic`, `cites`. `mads` and `iucn`. To add all categories at once, use `all`. To add two or more categories, pass this flag multiple times. For example:

.. code:: bash

    regi0 tax input.csv output.csv --category cites --category iucn

to add the CITES appendix and the IUCN threat category.

Keep in mind that these categories are retrieved from the species checklist file specified in the configuration file. Thus, you need to make sure that this file has these categories.

- :code:`-r/--remove`: Remove records with any flag. For example, if a record had an incorrect country or was identified as a duplicate, it will be removed in the output.

- :code:`-q/--quiet`: Avoid printing any information message in the console during the execution of the workflow.
