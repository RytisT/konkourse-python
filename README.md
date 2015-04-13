KonKourse
===============
Konkourse is an open source social network written in python using the
[django](https://www.djangoproject.com/) framework.

Installation
===============
Install the python dependencies using:
```
pip install -r requirements.txt
```
You will also need the python imaging library:
```
sudo apt-get install python-imaging
```
To setup search download and install elasticsearch.

Running
===============
First setup the database by running:
```
python manage.py syncdb
```
The migrate the intial database entries with:
```
python manage.py migrate
```

The test mail-server can be run using the following command:
```
python -m smtpd -n -c DebuggingServer localhost:1025
```
To get search up and running run the following:
```
sudo elasticsearch/bin/elasticsearch -f -Des.network.host=127.0.0.1
```

Then go ahead and run the server using:
```
python manage.py runserver
```

Testing
===============
Currently, none. Yeah we should get on that.
