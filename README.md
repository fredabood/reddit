# Summary

This project scrapes interesting informations about the top comments from a select group of Reddit users.

Some of this data is then aggregated to the user-level, and used to generate visualizations comparing the users to one another.

##| Filename | Description |
|-|-|
|[usernames.csv](usernames.csv)|The names and usernames being scraped.|
|[data.json](data.json)|The datafile saved by update_json|
|[sample.json](sample.json)|Example of the data pulled for one user.|
|[update_json.ipynb](update_json.ipynb)|Sandbox noteook used to build update_json.py.|
|[update_json.py](update_json.py)|Run on it's own this script will update the data file. Imported to a script, it will return a data frame.|
|[visualizations.ipynb](visualizations.ipynb)|End file where the JSON is read, then used to create visualizations of the data.|
