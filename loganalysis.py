#!/usr/bin/env python3

import psycopg2

# This is a function that takes PostgreSQL queries


def analysis(query):
    conn = psycopg2.connect(dbname="news")
    cursor = conn.cursor()

    # This view counts the ip hence giving no. of views
    ipcounter = "create view ipcounter as select path, count(ip) " \
                "as vw from log group by path order by vw desc;"
    cursor.execute(ipcounter)

    # This view joins ipview and author table
    artcounter = "create view artcounter as select articles.title," \
                 " ipcounter.vw from " \
                 "articles left join ipcounter on " \
                 "ipcounter.path LIKE '%' || " \
                 "articles.slug || '%' order by vw desc;"
    cursor.execute(artcounter)

    # This view joins articles and authors
    artauth = "create view artauth as select articles.title, " \
              "authors.name from articles join authors on " \
              "authors.id = articles.author;"
    cursor.execute(artauth)

    # This view counts no. of requests made at a particular day
    request = " create view request as select time::timestamp::date," \
              " count(*) as requests " \
              "from log group by time::timestamp::date;"
    cursor.execute(request)

    # This view displays errors occurred in a day
    errorpd = " create view errorpd as select time::timestamp::date," \
              " count(time::timestamp::date) as errors " \
              "from log where status='404 NOT FOUND' " \
              "group by time::timestamp::date;"
    cursor.execute(errorpd)

    # This view displays requests and errors occurred
    #  in a day by joining errorpd and request
    requesterror = "create view requesterror as select request.time," \
                   " request.requests, errorpd.errors " \
                   "from request left join errorpd on" \
                   " request.time=errorpd.time;"
    cursor.execute(requesterror)

    cursor.execute(query)

    # That's how our result gets printed
    result = cursor.fetchall()
    print(result)

    conn.close()


# This query goes into function and returns
#  top five most popular articles and their views
print("\nHere are top five most popular articles:\n")
pop_query = "select * from artcounter limit 5;"
analysis(pop_query)

# This query goes into function and returns
# top five most popular articles and their views
print("\nHere are top five most popular authors:\n")
pop_auth_query = "select artauth.name, artcounter.vw from" \
                 " artcounter join artauth on " \
                 "artauth.title = artcounter.title" \
                 " order by artcounter.vw desc limit 5;"
analysis(pop_auth_query)

# This query goes into function and returns days
#  when more than 1% of requests lead to error
print("\nHere are the days when more "
      "than 1% of requests lead to error\n")
percentage_error_query = "select * from (select time::timestamp::date," \
                         " (errors + 0.0)*100/requests " \
                         "as percentage_error from requesterror) as final" \
                         " where percentage_error > 1;"
analysis(percentage_error_query)
