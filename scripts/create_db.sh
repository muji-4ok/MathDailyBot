#!/bin/bash

psql -h $DB_HOST -U postgres -d postgres -c "\copy tasks FROM 'data/tasks.csv' with (format csv, header true, delimiter ',')"
