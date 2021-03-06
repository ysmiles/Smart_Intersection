# Car brand recognition - smart intersection

This is a machine learning project involving car detection, etc.
The original motivation is from the idea of "Smart Intersection - Smart City".

*My contributions*: web interface; part of data preparing, training, video/slides/report making.

Thanks for Shuai Hua's efforts to find good available data sets and taking care of main data processing work.
Also thanks for Kalyani Kulkarni's work of video making and helpful works on other parts of this project.

The report source file is this [Overleaf link](https://www.overleaf.com/read/sgbgwdfszgcb).

Our group folder including several notes and videos, slides, etc. is shared with this [Google Drive Link](https://drive.google.com/drive/folders/0B9A0RzaktEI1WExDOU5PNUdOcUk?usp=sharing).
Every one at SJSU can view it.

## Machine Learning

Please refer to the folder [/inception220](https://github.com/ysmiles/Smart_Intersection/tree/master/inception220) in this repository for machine learning details.

## Web interface

Following is the brief introduction for web interface. 

The overall data flow of this app is as follow.

![img](img/data_flow.png)

The web based application is implemented mainly by [Python-Flask](http://flask.pocoo.org/) framework.
It is a popular BSD licensed microframework for Python based on Werkzeug, Jinja 2 and good intentions.
We use it for providing a cross platform web interface of the final test.

After we get the trained model, we can use command line to perform the test.
But for general user, they usually don't know shell at all and don't like to know.
So an easy handling interface is our task now.

The logic of this app, on the one hand, is get user uploaded data and storage at the server side. 
Flask has good implementation to handle the file from user's HTTP POST request from his browser.
On the other hand, we take advantage of the characteristic of "glue language" of Python and use it to call the test command. Further work would involve call the test functions directly and batch test API.

For details please see server.py.

The HTML file is at /templates folder, and CSS file is at /static folder.

For running, just run `python3 server.py` at the machine with trained model.

Sample image:

![img](img/sample.png)