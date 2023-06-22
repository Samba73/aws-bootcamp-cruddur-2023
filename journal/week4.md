# Week 4 — Postgres and RDS

### Followed all the videos and completed each step
### Before creating bash scripts, postgres container (locally) from docker-compose
```
 db:
    image: postgres:13-alpine
    restart: always
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=<enteryourpassword>
    ports:
      - '5432:5432'
    volumes: 
      - db:/var/lib/postgresql/data

volumes:
  db:
    driver: local
```
### Created the bash scripts for the the db steps (creating db, creating tables, creating records, connecting and querying tables etc)
### `./bin/db-connect` to connect to the psql 
```
#! /usr/bin/bash
if [ "$1" = "prod" ]; then
  echo "Running in production mode"
  URL=$PROD_CONNECTION_URL
else
  URL=$CONNECTION_URL
fi

psql $URL
```

### `./bin/db-create` to create a new table 'cruddur'
```
#!  /usr/bin/bash

CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="db-create"
printf "${CYAN}== ${LABEL}${NO_COLOR}\n"

NO_DB_CONNECTION_URL=$(sed 's/\/cruddur//g' <<< "$CONNECTION_URL")
psql $NO_DB_CONNECTION_URL -c "create database cruddur;"
```

### `./bin/db-drop` to drop if the table is existing
```
#!  /usr/bin/bash

CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="db-drop"
printf "${CYAN}== ${LABEL}${NO_COLOR}\n"

NO_DB_CONNECTION_URL=$(sed 's/\/cruddur//g' <<< "$CONNECTION_URL")
psql $NO_DB_CONNECTION_URL -c "drop database cruddur;"
```
### Created the schema and seed sql to work with bash scripts in previous step

### `./bin/db-scheme-load` to load the schema 
#! /usr/bin/bash

CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="db-schema-load"
printf "${CYAN}== ${LABEL}${NO_COLOR}\n"

schema_path="$(realpath .)/db/schema.sql"
echo $schema_path

if [ "$1" = "prod" ]; then
  echo "Running in production mode"
  URL=$PROD_CONNECTION_URL
else
  URL=$CONNECTION_URL
fi

psql $URL cruddur < $schema_path
```

### `./bin/db-seed` to insert the data into schema loaded
```
#! /usr/bin/bash

CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="db-seed"
printf "${CYAN}== ${LABEL}${NO_COLOR}\n"

seed_path="$(realpath .)/db/seed.sql"
echo $seed_path

if [ "$1" = "prod" ]; then
  echo "Running in production mode"
  URL=$PROD_CONNECTION_URL
else
  URL=$CONNECTION_URL
fi

psql $URL cruddur < $seed_path

```

### Created the RDS in AWS and connected from docker successfully through the bash scripts and sql files

```
aws rds create-db-instance \
  --db-instance-identifier cruddur-db-instance \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --engine-version  14.6 \
  --master-username root \
  --master-user-password ###### \
  --allocated-storage 20 \
  --availability-zone ap-southeast-1a \
  --backup-retention-period 0 \
  --port 5432 \
  --no-multi-az \
  --db-name cruddur \
  --storage-type gp3 \
  --publicly-accessible \
  --storage-encrypted \
  --enable-performance-insights \
  --performance-insights-retention-period 7 \
  --no-deletion-protection
```
## AWS Lambda
**Post Confirmation Lambda** : This lambda is triggered when a user confirms signup in the app,the cognito status changes to Confirmed and this lambda is triggered to update the table in RDS with the user cognito user id which is what is used to authenticate at frontend before accessing the backend flask api's

Lambda function
```
import json
import psycopg2

def lambda_handler(event, context):
    user = event['request']['userAttributes']
    try:
        conn = psycopg2.connect(
            host=(os.getenv('PG_HOSTNAME')),
            database=(os.getenv('PG_DATABASE')),
            user=(os.getenv('PG_USERNAME')),
            password=(os.getenv('PG_SECRET'))
        )
        cur = conn.cursor()
        cur.execute("INSERT INTO users (display_name, handle, cognito_user_id) VALUES(%s, %s, %s)", (user['name'], user['email'], user['sub']))
        conn.commit() 

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        
    finally:
        if conn is not None:
            cur.close()
            conn.close()
            print('Database connection closed.')

    return event
    ```
### Updated the Home page to fetch the data from RDS in AWS
[
](https://github.com/Samba73/aws-bootcamp-cruddur-2023/commit/98fe1cc22bd8634b37778f26a89e79d0e6352336#:~:text=commit-,98fe1cc,-Show%20file%20tree)
[
](https://github.com/Samba73/aws-bootcamp-cruddur-2023/commit/965a037121fb9aab67e24ab38dd7184f884e8323#:~:text=commit-,965a037,-Show%20file%20tree)

### Updated the Create Activity page to create new Crud, save in RDS (AWS) and update the home page

[
](https://github.com/Samba73/aws-bootcamp-cruddur-2023/commit/010e6dff7a7b1c7bf7a147d25d4e75fa3cd17fa4#:~:text=commit-,010e6df,-Show%20file%20tree)https://github.com/Samba73/aws-bootcamp-cruddur-2023/commit/010e6dff7a7b1c7bf7a147d25d4e75fa3cd17fa4#:~:text=commit-,010e6df,-Show%20file%20tree

[
](https://github.com/Samba73/aws-bootcamp-cruddur-2023/commit/5af3d3819ed88fa9ad768e39257b740fc394d453#:~:text=commit-,5af3d38,-Show%20file%20tree)https://github.com/Samba73/aws-bootcamp-cruddur-2023/commit/5af3d3819ed88fa9ad768e39257b740fc394d453#:~:text=commit-,5af3d38,-Show%20file%20tree


### Followed AB code refactoring video and made changes to the db.sql with own approach to learn and implement own thoughts.

[
](https://github.com/Samba73/aws-bootcamp-cruddur-2023/commit/98fe1cc22bd8634b37778f26a89e79d0e6352336#:~:text=commit-,98fe1cc,-Show%20file%20tree)https://github.com/Samba73/aws-bootcamp-cruddur-2023/commit/98fe1cc22bd8634b37778f26a89e79d0e6352336#:~:text=commit-,98fe1cc,-Show%20file%20tree

