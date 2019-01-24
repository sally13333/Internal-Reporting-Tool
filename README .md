# Full Stack Web Developer Nanodegree Program
## First project :Logs Analysis 
***
***

# Contents:

  - Internal Reporting Tool
  - Tool's Functions
  - Requirements
  - Prepare The Software and Data
  - Schema of Database
  - Queries Used 
  - Python Code
  - Run python code 
  - How Outputs looks like ?

  
***
&nbsp;   
#### Internal Reporting Tool:
>tool that will use information from the database to discover what kind of articles the site's readers like.
&nbsp;

&nbsp; 
#### Tool's Functions:
   - Find the most popular three articles of all time
  - Find the most popular article authors of all time
  - Calculate requests that lead to error more than 1%

&nbsp; 
***
#### Requirements:
>if you want use vagrant to run this project you have to install
  - [Vagrant ](https://www.vagrantup.com/downloads.html)
  - [VirtualBox ](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)
>Alternatively if you did not want  to rely on Vagrant, you could  set-up and run the project in an environment of your choosing. In this case the requirements would be:
  - [Python 3](https://www.python.org/downloads/)
  - [PostgreSQL](https://www.postgresql.org/download/)
  - [psycopg2](https://pypi.org/project/psycopg2/)
***
#### Prepare The Software and Data
##### 1- Download the VM configuration
There are a couple of different ways you can download the VM configuration.

You can download and unzip this file:[ FSND-Virtual-Machine.zip ](https://www.vagrantup.com/downloads.html)  This will give you a directory called FSND-Virtual-Machine. It may be located inside your Downloads folder.

Alternately, you can use Github to fork and clone the repository https://github.com/udacity/fullstack-nanodegree-vm.

Either way, you will end up with a new directory containing the VM files. Change to this directory in your terminal with `cd`. Inside, you will find another directory called vagrant. Change directory to the vagrant directory

##### 2- Start the virtual machine
om your terminal, inside the vagrant subdirectory, run the command `vagrant up`. This will cause Vagrant to download the Linux operating system and install it. This may take quite a while (many minutes) depending on how fast your Internet connection .
When `vagrant up` is finished running, you will get your shell prompt back. At this point, you can run `vagrant ssh` to log in to your newly installed Linux VM!
##### 3-Download the data
Next, download the data [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip). You will need to unzip this file after downloading it. The file inside is called newsdata.sql. Put this file into the vagrant directory, which is shared with your virtual machine.

To load the data, `cd` into the`vagrant` directory and use the command `psql -d news -f newsdata.sql`.Running this command will connect to your installed database server and execute the SQL commands in the downloaded file, creating tables and populating them with data.

Once you have the data loaded into your database, connect to your database using 'psql -d news' and explore the tables using the `\dt` and `\d table` commands and `select` statements.
***
#### Schema of Database:
>to understand how our program work ,we have to understand schema of database .The name of database is news and it has the following tables:
  - articles 
  - authors 
  - log 
  
1-articles:
|  authors      |  slug         | lead          | body          | time          | id            |
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
>Indexes:
    "articles_pkey" PRIMARY KEY, btree (id)
    "articles_slug_key" UNIQUE CONSTRAINT, btree (slug)
Foreign-key constraints:
    "articles_author_fkey" FOREIGN KEY (author) REFERENCES authors(id)

2-authors:
| name          | bio         | id          |
| ------------- |-------------|-------------|
>Indexes:
    "authors_pkey" PRIMARY KEY, btree (id)
Referenced by:
    TABLE "articles" CONSTRAINT "articles_author_fkey" FOREIGN KEY (author) REFERENCES authors(id)

3-log: 
|  path         |  ip           | method        | status        | time          | id            |
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |

>Indexes:
    "log_pkey" PRIMARY KEY, btree (id)
&nbsp;    
***    
#### Queries Used: 
>in this section we will explain each query for each tool's function.You can try everey query using vagrat using command `psql news` then type query and each query end with `;`

##### 1-Find the most popular three articles of all time:
 you can solve that by joining two table and count title from articles table .`Note: we do not have any relation between log table and articles table  ` to join them  so to solve this problem we have to find a realtion between them .If you look hardly to both table content you can find that path  column  from log table looks like  slug column  from table article for example:


slug  |
--- |
candidate-is-jerk |

path  |
--- |
 /article/candidate-is-jerk|
as you can see slug not looks exactly like path so we will make them exactly the same by using  `concat()` function [you can read more about this function  here ](https://www.w3schools.com/sql/func_mysql_concat.asp) .
by using this function as following we will have a relation and can find output easly 
```sql
SELECT articles.title,count(*) AS veiws 
FROM articles 
LEFT JOIN  log 
ON  log.path = concat('/article/',articles.slug) 
GROUP BY  articles.title 
ORDER BY veiws DESC  LIMIT  3 
```

##### 2-Find the most popular article authors of all time:
in this query ,we will use the same relation we used it in previous query then we will use left outer join to join output of log table and articles table and then use it again  with authors table to connect all these tables and get output 
```sql
SELECT  authors.name, count(*) AS veiws
FROM  authors 
LEFT OUTER JOIN articles ON  authors.id =articles.author 
LEFT OUTER JOIN  log 
ON log.path= concat('/article/',articles.slug) 
GROUP BY authors.name 
ORDER BY veiws DESC LIMIT  3
```
##### 3-Calculate requests that lead to error more than 1%
to solve this query we need to understant how calculate percent . First we will count all requests by  using function `date()` to calculate each day individule and multible it with 100 which have error "status=404 not found "  , then use another query to count all requests  for each day , so will use insted qeuries by deviding two output from two previos  queries then select  w title and deviding result  [youcan use this code as a refrensce](https://stackoverflow.com/questions/12238621/sql-subquery-has-too-many-columns) 

```sql
SELECT  table1.date, cast(table1.cl1 as decimal)/table2.cl2 AS errors 
FROM 
(SELECT  date(time) AS date, count(date(time)) * 100 AS cl1 
FROM log  
WHERE  status = '404 NOT FOUND'
GROUP BY  date(time))table1  
JOIN
(SELECT date(time) as date ,count (date(time)) AS cl2 
FROM log 
GROUB BY  date (time))table2
ON  table1.date = table2.date 
WHERE  table1.cl1/table2.cl2 > 1
```
`Note: we used cast() function to convert result from integer to decimal` 
[you can read more about this function  here ](https://docs.microsoft.com/en-us/sql/t-sql/functions/cast-and-convert-transact-sql?view=sql-server-2017)you can also use `table1.c1::decimal` rather than using cast function 
***
#### Python Code:
>this is the python program that uses DB-API to query database to build internal reporting tool we tried to explain every part using comments, 
```python
#!/usr/bin/env python3
import psycopg2
# connect to news database
connect = psycopg2.connect("dbname=news")
# object to scan throght results
cursor = connect.cursor()
# initinalzation array to all queries that we need
array_queries = [
    """ SELECT articles.title,
    count(*) AS veiws
    FROM articles LEFT JOIN  log
    ON log.path = concat('/article/',articles.slug)
    GROUP BY articles.title
    ORDER BY veiws DESC LIMIT 3""",
    """SELECT authors.name, count(*) AS veiws
    FROM authors LEFT OUTER JOIN  articles
    ON authors.id =articles.author
    LEFT OUTER JOIN log
    ON log.path= concat('/article/',articles.slug)
    GROUP BY  authors.name
    ORDER BY  veiws DESC LIMIT 3 """,
    """ SELECT table1.date,
    cast(table1.cl1 as decimal)/table2.cl2 AS errors
    FROM (SELECT date(time) AS date,
    count(date(time)) * 100 as cl1
    FROM log  WHERE status = '404 NOT FOUND'
    GROUP BY date(time))table1
    JOIN (SELECT date(time)
    AS date ,count (date(time)) as cl2
    FROM log GROUP BY date (time))table2
    ON table1.date = table2.date
    WHERE table1.cl1/table2.cl2 > 1
    """
]  # end of array
output_array = [
    """1. What are the most popular three articles of all time?\n""",
    """2. Who are the most popular article authors of all time?\n""",
    """3. On which days did more than 1% of requests lead to errors \n"""]
i = 0
# build a loop to move in array index
while (i < 3):
        cursor.execute(array_queries[i])
        result = cursor.fetchall()
        print output_array[i],  "-" * 70
        for result in result:
            if (i == 0):  # determine the looks of output
                print ('   \"{}\" -- {} views'.format(result[0], result[1]))
            elif (i == 1):
                print('   {} -- {} views'.format(result[0], result[1]))
            else:
                print('   {} - {:.2f} % errors'.format(result[0], result[1]))
        print
        print
        i = i + 1
connect.close()

```
***
#### Run python code 
> if you want Run your python code using terminal and vagrant 
do  the following steps:
  - follow this  directory `fsnd-virtual-machine` => `FSND-Virtual-Machine` =>`Vagrant` by clicking right on your mouse choose `Git Bash Here` then write these command 
     - `vagrant ssh` 
     - `cd /vagrant`
      - if you put your project in directory inside vagrant  type `cd directory_name`
     - `python name_of_file.py`
  
***
#### How Outputs looks like ?
> The outputs depending on your database and your code but if you follow us You may have outputs looks like this :
```
vagrant@vagrant:/vagrant/project$ python news.py
1. What are the most popular three articles of all time?
----------------------------------------------------------------------
   "Candidate is jerk, alleges rival" -- 338647 views
   "Bears love berries, alleges bear" -- 253801 views
   "Bad things gone, say good people" -- 170098 views


2. Who are the most popular article authors of all time?
----------------------------------------------------------------------
   Ursula La Multa -- 507594 views
   Rudolf von Treppenwitz -- 423457 views
   Anonymous Contributor -- 170098 views


3. On which days did more than 1% of requests lead to errors
----------------------------------------------------------------------
   2016-07-17 - 2.26 % errors

```












