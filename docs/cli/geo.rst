regi0 geo
=========

.. code:: text

    regi0 geo

Workflow
********
The :code:`geo` commands executes the following geographic verification workflow by default:

1. Read the input file (biological records) with their associated coordinates and remove records where these are missing or incomplete.

2. Verify the original country values in the input file (biological records) with the historical reference layers. It does this by matching each record (using its date) with one of the layers, extracting the expected country by intersecting its coordinates with the layer, and the comparing both values to see to check whether they match.

3. Verify the original state values in the input file (biological records) with the historical reference layers. It does this by matching each record (using its date) with one of the layers, extracting the expected state by intersecting its coordinates with the layer, and the comparing both values to check whether they match.

4. Verify the original county values in the input file (biological records) with the historical reference layers. It does this by matching each record (using its date) with one of the layers, extracting the expected county by intersecting its coordinates with the layer, and the comparing both values to check whether they match.

5. Identify records that fall inside urban limits. It does this by intersecting each record with the urban reference layer.

6. Identify records that are spatial duplicates. It does this by creating a spatial grid of flexible resolution and extent and then intersecting the records with the grid. Records from the same species that fall inside the same square will are identified as duplicates.

7. Save a copy of the input file (biological) records with extra columns indicating flags, suggestions and sources of verification.

Usage
*****
If you execute the :code:`geo` command with the :code:`--help` flag, you will see its usage:

.. code:: text

    regi0 geo --help

prints the following message:

.. code:: text

    Usage: regi0 geo [OPTIONS] INPUT OUTPUT

      Executes a flexible geographic verification workflow on a set of biological
      records.

    Options:
      --skip-admin [country|stateProvince|county]
                                      Administrative divisions to skip during
                                      verification.
      --skip-urban                    Skip urban limits verification.  [default:
                                      False]
      --skip-duplicates               Skip the identification of duplicate
                                      records.  [default: False]
      -r, --remove                    Remove records with flags.  [default: False]
      -q, --quiet                     Silence information logging.  [default:
                                      False]
      --help                          Show this message and exit.

- :code:`INPUT`: Relative or absolute path of the input file (can be csv, txt or xlsx) containing the biological records.

- :code:`OUTPUT`: Relative or absolute path of the output file (can be csv, txt or xlsx) to be created with the results.

- :code:`--skip-admin`: Levels of administrative divisions to skip during verification. Must be one of `country`, `stateProvince` and `county`. To skip two or more levels, pass this flag multiple times. For example:

.. code:: bash

    regi0 geo input.csv output.csv --skip-admin country --skip-admin stateProvince

to skip the verification of country and state.

- :code:`--skip-urban`: Skip the identification of records that fall inside urban limits.

- :code:`--skip-duplicates`: Skip the identification of duplicate records.

- :code:`-r/--remove`: Remove records with any flag. For example, if a record had an incorrect country or was identified as a duplicate, it will be removed in the output.

- :code:`-q/--quiet`: Avoid printing any information message in the console during the execution of the workflow.
