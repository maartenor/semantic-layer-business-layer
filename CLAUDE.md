For a proof of concept I want to create instances for a database having tables, being modelled in a semantic layer, so I can visualize it in a BI reporting solution.

This semantic layer, existing in a Malloy Publisher server, should be created based on modelled data in a data goverance solution.
* The data governance solution is Collibra
* It contains 3 different asset types: 
    * business data objects: describing the data in business terms
    * logical data objects: for now, a 1 on 1 mapping from business logic to technical data object
    * technical data object: the description of the technical table and columns that contain the data (physical storage)
* And the the relationships between those assets.

Existing instances that are:
* input datasets in a postgresql database containing tables, representing the physical storage as used in the technical data object for
    * customer master data, with 10 customers in western world countries
    * location master data, with 2 to 5 locations per customer
    * machine master data, with 3 to 5 machines_nrs and their attributes: {type: [NXT, NXE, AT]}
    * install base master data, where a machine_nr is installed at a customer site location
    * machine event logs data, where event records exists per machine per day, with events created over the course of 24 hours
* a semantic layer being server via a Malloy Publisher server. It now contains hard coded semantic layer, using postgres db input to define measures/metrics definitions.

Docs available that you can use in case details are needed :
* Collibra API: https://developer.collibra.com/tutorials/getting-started-with-the-rest-api#making-a-get-call describing the collibra resource types that API servers
* https://github.com/chorvathdev/collibra-core describing a Python repo. This repo contains the Core REST API allows you to create your own integrations with Collibra Data Governance Center.
  * containing e.g. the Collibra API return structures https://github.com/chorvathdev/collibra-core/blob/master/docs/AssetImpl.md 
  * like AsesetImpl https://github.com/chorvathdev/collibra-core/blob/master/docs/AssetsApi.md#get_asset or paginated versions on GetAsset API response
  * or FindAsset response https://github.com/chorvathdev/collibra-core/blob/master/docs/AssetsApi.md#find_assets 

 