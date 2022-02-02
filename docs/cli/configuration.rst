Configuration
=============

In order to provide some flexibility to the user, several options can be configured in a separate file. After installing regi0, the first thing you will need to do in other to use the CLI is run the following command:

.. code:: bash

   regi0 setup

This will copy a sample of the `configuration file <https://github.com/PEM-Humboldt/regi0/blob/master/regi0/cli/config/settings.ini>`_ to the configuration folder of your machine. Depending on your OS, the configuration folder will change. The command will print the path where it copied the configuration file to so you will be able to open the file.

You only have to run the setup command once. If you try to run it again, you will see a warning similar to this one:

.. code:: text

    Configuration file already exists in <config path>. Run this command with the -o/--overwrite flag to overwrite it.

If, for some reason, you want to copy the sample file again and overwrite the one you already have, run the following command:

.. code:: bash

   regi0 setup --overwrite

Everytime you execute one of the workflows, regi0 CLI reads the configuration file from the configuration folder in your machine and uses the options there. If you want to change any of these options, simply open the file, replace the option you want to change and save the file. The next time you execute on of the workflows, it will use the new options.

A sample of the configuration file, settings.ini,  looks like this:

.. code:: text

    [paths]
    admin0 = /home/foo/data/shp/admin0/
    admin1 = /home/foo/data/shp/admin1/
    admin2 = /home/foo/data/shp/admin/
    urban = /home/foo/data/shp/urban/urban_2016.shp
    checklist = /home/foo/data/csv/reference_2021.csv

    [colnames]
    longitude = decimalLongitude
    latitude = decimalLatitude
    date = eventDate
    admin0 = countryCode
    admin1 = stateProvince
    admin2 = county
    species = scientificName

    [attributes]
    admin0 = ISO_A2
    admin1 = DPTOS
    admin2 = MPIOS

    [checklist]
    species = scientificName
    alien = measurementValue (INVASORAS)
    endemic = measurementValue (ENDEMISMO)
    cites = appendixCITES
    mads = measurementValue (Categoria de amenaza MADS)
    iucn = threatStatus

    [flagnames]
    admin0 = correctCountry
    admin1 = correctStateProvince
    admin2 = correctCounty
    duplicate = isDuplicate
    urban = isUrban
    spatialduplicate = spatialDuplicate
    species = validName

    [suggestednames]
    admin0 = suggestedCountry
    admin1 = suggestedStatedProvince
    admin2 = suggestedCounty
    species = suggestedName
    canonical = canonical

    [sourcenames]
    admin0 = countrySource
    admin1 = stateProvinceSource
    admin2 = countySource
    species = nameAccordingTo

    [duplicates]
    pixelsize = 0.008333333767967150002
    bounds =
    keep = false
    columns = scientificName,catalogNumber

    [misc]
    crs = epsg:4326
    direction = nearest
    defaultyear = last

    [verification]
    preprocess = True
    fuzzy = True
    threshold = 0.8

paths
*****
This section of the configuration file contains the paths in your machine to the reference files used in the workflows and is the only section where the options have to be replaced before using regi0's CLI because there is no way of knowing where the reference files will be stored in your machine.

- :code:`admin0`: Path to a GeoPackage file or a folder containing shapefiles with the historical country divisions. Layers inside the GeoPackage file or shapefiles inside the folder can have any name but they have to contain the year somewhere. For example: admin0_2018.shp or 2018.shp. If there is only one layer or one shapefile, it will be the only one used.

- :code:`admin1`: Path to a GeoPackage file or a folder containing shapefiles with the historical state divisions. Layers inside the GeoPackage file or shapefiles inside the folder can have any name but they have to contain the year somewhere. For example: admin1_2018.shp or 2018.shp. If there is only one layer or one shapefile, it will be the only one used.

- :code:`admin2`: Path to a GeoPackage file or a folder containing shapefiles with the historical county divisions. Layers inside the GeoPackage file or shapefiles inside the folder can have any name but they have to contain the year somewhere. For example: admin2_2018.shp or 2018.shp. If there is only one layer or one shapefile, it will be the only one used.

- :code:`urban`: Path to a GeoPackage, GeoJSON or shapefile with the urban limits that will be used in the geographical workflow.

- :code:`checklist`: Path to a csv, txt or xlsx file with the species checklist that will be used to add categories in the taxonomic workflow.

colnames
********
This section of the configuration file contains the column names of the input file (biological records) of the workflows.

- :code:`longitude`: Column with the longitude coordinates.

- :code:`latitude`: Column with the latitude coordinates.

- :code:`date`: Column with the timestamps.

- :code:`admin0`: Column with the country or country code.

- :code:`admin1`: Column with the state.

- :code:`admin2`: Column with the county.

- :code:`species`: Column with the scientific name.

attributes
**********
This section of the configuration file contains the attributes or fields of the geographic reference layers that are going to be extracted to verify the original values in the biological records.

- :code:`admin0`: Attribute or field name with the country or country code.
- :code:`admin1`: Attribute or field name with state.

- :code:`admin2`: Attribute or field name with county.

checklist
*********
This section of the configuration file contains the column names in the species checklist that are going to be used to add categories to the biological records.

- :code:`species`: Column with the scientific name.
- :code:`alien`: Column with the alien or invasive category.
- :code:`endemic`: Column with the endemic category.
- :code:`cites`: Column with the CITES appendix category.
- :code:`mads`: Column with threat status category from the Colombian Ministry of Environment.
- :code:`iucn`: Column with the threat status category from the IUCN.

flagnames
*********
This section of the configuration file contains the names of the new columns that are going to be created on the output file to represent flags (i.e. the result of the different verifications).

- :code:`admin0`: Name of the column that shows whether the original country or country code in the input file (biological records) is correct.

- :code:`admin1`: Name of the column that shows whether the original state in the input file (biological records) is correct.

- :code:`admin2`: Name of the column that shows whether the original county in the input file (biological records) is correct.

- :code:`duplicate`: Name of the column that shows whether a record in the input file (biological records) is a taxonomic duplicate.

- :code:`urban`: Name of the column that shows whether a record in the input file (biological records) is inside urban limits.

- :code:`spatialduplicate`: Name of the column that shows whether a record in the input file (biological records) is a geographic duplicate.

- :code:`species`: Name of the column that shows whether the original scientific name (automatically converted to canonical form) in the input file (biological records) is correct.

suggestednames
**************
This section of the configuration file contains the names of the new columns that are going to be created on the output file to represent suggestions for records with flags (i.e. incorrect values).

- :code:`admin0`: Name of the column that shows the suggested country or country code for records where the original values were incorrect.

- :code:`admin1`: Name of the column that shows the suggested state for records where the original values were incorrect.

- :code:`admin2`: Name of the column that shows the suggested county for records where the original values were incorrect.

- :code:`species`: Name of the column that shows the suggested scientific name for records where the original values were incorrect.

- :code:`canonical`: Name of the column that shows the suggested scientific name in canonical form for all the records.

sourcenames
***********
This section of the configuration file contains the names of the new columns that are going to be created on the output file to represent the sources used for the verification.

- :code:`admin0`: Name of the column that shows the source (name of the file or layer) used to verify the country or country code.

- :code:`admin1`: Name of the column that shows the source (name of the file or layer) used to verify the state.

- :code:`admin2`: Name of the column that shows the source (name of the file or layer) used to verify the county.

- :code:`species`: Name of the column that shows the source used (by Global Names Resolver) to verify the scientific name.

duplicates
**********
This section of the configuration file contains options for the identification of both taxonomic and spatial duplicates.

- :code:`pixelsize`: Pixel size or resolution of the grid that is going to be created to identify spatial duplicates. The units must match the spatial reference of the input file (biological records). For example, if the spatial reference of the input file is WGS84 (geographic), make sure to specify the pixel size in degrees and not meters.

- :code:`bounds`: Bounds or extent (in the form xmin,ymin,xmax,ymax) to create the grid to identify the spatial duplicates. Leave empty to automatically compute the extent from the biological records.

- :code:`keep`: Which duplicates (both spatial and taxonomic) to mark as duplicates. Write `first` to mark all but the first, `last` to mark all but the last and leave empty to mark all duplicates.

- :code:`columns`: Subset of columns (separated by comma) in the input file (biological records) to use to identify taxonomic duplicates.

misc
****
This section of the configuration file contains miscellaneous options.

- :code:`crs`: Coordinate Reference System (in the form epsg:<code>) of the coordinates in the input file (biological records).

- :code:`direction`: Direction to match dates of the input file (biological records) with the reference historical layer. Write `nearest` to round to the nearest year, `forward` to round to the closest next year and `backward` to round to the closest last year. Suppose you have two historical reference layers: 2004.shp, 2011.shp. A record with date 2005 will be verified with the 2004 layer if :code:`direction` is `nearest` or `backward`. However, it will be verified with the 2011 layer if direction is `forward`. Another record with date 2012 will be verified with the 2011 layer if :code:`direction` is `nearest` or `backward`. However, if :code:`direction` is `forward`, that record won't be verified unless :code:`defaultyear` is set.

- :code:`defaultyear`: Default year to take for records without date or that did not get any match when rounding years. Write `first` to take the earliest year from the historical reference layers, `last` to take the latest year from the historical reference layers and leave empty to skip assigning a default year to records without date or that did not get any match when rounding years.

verification
************
This section of the configuration file contains options for the verification.

- :code:`preprocess`: Whether to preprocess (i.e. remove spaces and special characters and convert all characters to lower case) values from both the input file (biological records) and the reference file before comparing them. Can be True or False.

- :code:`fuzzy`: Whether to do a fuzzy match or an exact match when comparing values from the input file (biological records) and the reference file. Can be True or False.

- :code:`threshold`: Similarity threshold to use when deciding whether two values match using fuzzy logic. Should be a number between 0 and 1. The smaller this number is, the less similar the values have to be to be considered equal.
