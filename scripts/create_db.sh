#!/bin/bash

psql -h localhost -U postgres -d postgres -c "\copy tasks FROM 'data/tasks.csv' with (format csv, header true, delimiter ',')"
