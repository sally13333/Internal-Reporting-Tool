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
