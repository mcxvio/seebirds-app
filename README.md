## seebirds-app
- Azure DevOps code repository.
- Azure WebApps for Containers docker deployed application.
- Gitlab hosted container/docker repository.

eBird 2.0 inquirer: python flask version.

- added more options from ebird 2.0 api;
- integrated with bootstrap css;
- previous items searched for saved to flask session;
- all UI via flask templates;
- without custom jquery/ajax & jquery mobile;
- updated to python 3.6;
- Twitter Typeahead and Bloodhound for autocomplete;
- all eBird countries and subregions (1 and 2);
- results displayed without using tables.

## Prerequisites

- You need an eBird API key from [here](https://ebird.org/ebird/api/keygen).
- Create a ```keys.json``` file in the root directory and copy your key into it.

e.g.
```
{
    "ebird_key":{
        "X-eBirdApiToken":"your_key_goes_here"
    }
}
```
