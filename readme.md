# Logs Analysis Project

This project sets up a PostgreSQL database for a fictional news website.


## Getting Started

### The database
articles - This table contains a database of all the articles published
authors -  This table contains a database of all the authors including their name
log - This table has a database row for each time a reader access a web page.

### The Questions
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?


## Installation

1. Set up a virtual machine using Vagrant and VirtualBox
  Install VirtualBox https://www.virtualbox.org/wiki/Download_Old_Builds_5_1
  Install Vagrant https://www.vagrantup.com/downloads.html

  for help, visit https://medium.com/@JohnFoderaro/how-to-set-up-a-local-linux-environment-with-vagrant-163f0ba4da77

2. From your terminal, inside the vagrant subdirectory, run the command
  `vagrant up`. This will cause Vagrant to download the Linux operating system
  and install it. This may take quite a while (many minutes) depending on how
  fast your Internet connection is.

3. When vagrant up is finished running, you will get your shell prompt back.
  At this point, you can run `vagrant ssh` to log in to your newly
  installed Linux VM

4. Inside the VM change directory to `cd /vagrnat`

5. Clone or download the Github Repository to your vagrant directory

6.  Add 'newsdata.sql' database to the directory from       https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip

7. Run the file 'loganalysis.py'
    `python loganalysis.py`

8. To explore the database 'newsdata.sql'
    `psql -d news -f newsdata.sql`

#h2 Additional Information

The views that are used in this project are:

`create view ipcounter as select path, count(ip)
 as vw from log group by path order by vw desc;`

 `replace view artcounter as select articles.title,
                 ipcounter.vw from
                 articles left join ipcounter on
                 ipcounter.path LIKE '%' ||
                 articles.slug || '%' order by vw desc;`

  `replace view artauth as select articles.title,
              authors.name from articles join authors on
              authors.id = articles.author;`

  `replace view request as select time::timestamp::date,
               count(*) as requests
              from log group by time::timestamp::date;`

  `replace view errorpd as select time::timestamp::date,
               count(time::timestamp::date) as errors
              from log where status='404 NOT FOUND'
              group by time::timestamp::date;`

  `replace view requesterror as select request.time,
                    request.requests, errorpd.errors
                   from request left join errorpd on
                    request.time=errorpd.time;`
