#h1 Logs Analysis Project

This is a simple project that builds informative summary from logs
of a live database.

#h2 Installation

1. Set up a virtual machine using Vagrant and VirtualBox, for help
    visit https://medium.com/@JohnFoderaro/how-to-set-up-a-local-linux-environment-with-vagrant-163f0ba4da77

2. Turn on and log in to your virtual machine
    `vagrant up`
    `vagrant ssh`

3. Navigate to your vagrant directory
    `cd /vagrant`

4. Clone or download the Github Repository to your vagrant directory
   and add 'newsdata.sql' database (Not in repository, due to large size) to 
    the directory.


5. Run the file 'loganalysis.py'
    `python loganalysis.py`

6. To explore the database 'newsdata.sql'
    `psql -d news -f newsdata.sql`

#h2 Additional Information

The views that are used in this project are:

`create view ipcounter as select path, count(ip)
 as vw from log group by path order by vw desc;`

 `create view artcounter as select articles.title,
                 ipcounter.vw from
                 articles left join ipcounter on
                 ipcounter.path LIKE '%' ||
                 articles.slug || '%' order by vw desc;`

  `create view artauth as select articles.title,
              authors.name from articles join authors on
              authors.id = articles.author;`

  `create view request as select time::timestamp::date,
               count(*) as requests
              from log group by time::timestamp::date;`

  `create view errorpd as select time::timestamp::date,
               count(time::timestamp::date) as errors
              from log where status='404 NOT FOUND'
              group by time::timestamp::date;`

  `create view requesterror as select request.time,
                    request.requests, errorpd.errors
                   from request left join errorpd on
                    request.time=errorpd.time;`
