# fortune_telling_backend

## Migrations
Before starting the project, make sure your development DB is up to date. 
Run the following command in src folder:

    flask db upgrade

If you make a change that requires a DB schema update, create a migration:

    flask db migrate -m "Short description"

If you create empty revision file, create with this command:

    flask db revision -m "Short description"

If you want to downgrade to a specific revision of a migration:

    flask db downgrade <revision_id>


Flask Run for swagger http://localhost:5000/adjust_api/v1

        export FLASK_APP=src/app
        flask run

host is post : http://localhost:5000/adjust_api/v1/data with request body


1. use case
request body :

    `{
      "date_to": "2017-06-01",
      "date_from": "2017-05-01",
      "filter_metrics": [],
      "group_with": [
        "channel", "country"
      ],
      "sort_column": [
        {"sort_column": "clicks", "direction": "desc"}
      ],
      "selected_columns": [
        "impressions", "clicks"
      ]
    }`
2. use case

    `{
      "date_to": "2017-06-01",
      "date_from": "2017-05-01",
      "filter_metrics": [{"filter_type": "os", "filter": "ios"}],
      "group_with": [
        "date"
      ],
      "sort_column": [
        {"sort_column": "date", "direction": "asc"}
      ],
      "selected_columns": [
        "installs"
      ]
    }`
3. use case

    `{
      "date_to": "2017-06-02",
      "date_from": "2017-06-01",
      "filter_metrics": [],
      "group_with": [
        "os"
      ],
      "sort_column": [
        {"sort_column": "revenue", "direction": "desc"}
      ],
      "selected_columns": [
        "revenue"
      ]
    }`
4. use case

    `{
      "date_to": "2017-07-01",
      "date_from": "2017-05-01",
      "filter_metrics": [{"filter_type": "country", "filter": "CA"}],
      "group_with": [
        "channel"
      ],
      "sort_column": [
        {"sort_column": "cpi", "direction": "desc"}
      ],
      "selected_columns": [
        "cpi", "spend"
      ]
    }`