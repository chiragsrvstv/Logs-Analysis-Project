#!/usr/bin/env python3
import psycopg2

# The name of database being connected
DBNAME = "news"


def answer1():
    # A function for answering question 1

    print("\nThe most popular articles are\n")

    conn = psycopg2.connect(dbname=DBNAME)
    cursor = conn.cursor()

    # This view counts the ip hence giving no. of views
    ipcounter = """create view ipcounter as select path, count(ip)
                as vw from log group by path order by vw desc;"""
    cursor.execute(ipcounter)

    # This view joins ipview and author table
    artcounter = """create view artcounter as select articles.title,
                  ipcounter.vw from
                  articles left join ipcounter on
                 ipcounter.path = CONCAT('/article/', articles.slug)
                  order by vw desc;"""
    cursor.execute(artcounter)

    pop_query = "select * from artcounter limit 5;"
    cursor.execute(pop_query)

    # That's how result of queries gets printed
    result = cursor.fetchall()
    for title, views in result:
        print("{} -- {} views".format(title, views))

    conn.close()


def answer2():

    # A function for answering question 2

    print("\nThe most popular authors are\n")

    conn = psycopg2.connect(dbname=DBNAME)
    cursor = conn.cursor()

    # This view counts the ip hence giving no. of views
    ipcounter = """create view ipcounter as select path, count(ip)
                    as vw from log group by path order by vw desc;"""
    cursor.execute(ipcounter)

    # This view joins ipview and author table
    artcounter = """create view artcounter as select articles.title,
                    ipcounter.vw from
                     articles left join ipcounter on
                     ipcounter.path = CONCAT('/article/', articles.slug)
                      order by vw desc;"""
    cursor.execute(artcounter)

    # This view joins articles and authors
    artauth = """create view artauth as select articles.title,
              authors.name from articles join authors on
              authors.id = articles.author;"""
    cursor.execute(artauth)

    pop_auth_query = """select artauth.name, sum(artcounter.vw)
                    as total_views from
                    artcounter join artauth on
                    artauth.title = artcounter.title
                    group by artauth.name order by total_views desc;"""
    cursor.execute(pop_auth_query)

    # That's how result of queries gets printed
    result = cursor.fetchall()
    for title, views in result:
        print("{} -- {} views".format(title, views))

    conn.close()


def answer3():

    # A function for answering question 3

    print("""\nThe days when more than 1% of requests lead to errors are\n""")

    conn = psycopg2.connect(dbname=DBNAME)
    cursor = conn.cursor()

    # This view counts no. of requests made at a particular day
    request = """create view request as select time::timestamp::date,
               count(*) as requests
              from log group by time::timestamp::date;"""
    cursor.execute(request)

    # This view displays errors occurred in a day
    errorpd = """create view errorpd as select time::timestamp::date,
               count(time::timestamp::date) as errors
              from log where status!='200 OK'
              group by time::timestamp::date;"""
    cursor.execute(errorpd)

    # This view displays requests and errors occurred
    #  in a day by joining errorpd and request
    requesterror = """create view requesterror as select request.time,
                    request.requests, errorpd.errors
                   from request left join errorpd on
                    request.time=errorpd.time;"""
    cursor.execute(requesterror)

    percentage_error_query = """select * from (select time::timestamp::date,
                              (errors + 0.0)*100/requests
                              as percentage_error from requesterror) as final
                              where percentage_error > 1;"""

    cursor.execute(percentage_error_query)

    # That's how result of queries gets printed
    result = cursor.fetchall()
    for title, views in result:
        print("{} -- {} errors".format(title, views))

    conn.close()


def run():

    # This function returns all the answers

    answer1()
    answer2()
    answer3()

run()
