pip list
Package        Version
-------------- -------
blinker        1.7.0
click          8.1.7
colorama       0.4.6
DateTime       5.5
dnspython      2.6.1
Flask          3.0.2
Flask-Cors     4.0.0
itsdangerous   2.1.2
Jinja2         3.1.3
MarkupSafe     2.1.5
pip            24.0
pymongo        4.6.2
python-dotenv  1.0.1
pytz           2024.1
setuptools     65.5.0
Werkzeug       3.0.1
zope.interface 6.2

# pip install numpy==1.24.1
# pip install opencv-python==4.6.0.66
# pip install tensorflow==2.10.1
# pip install scikit-image

## Installation
1. Clone the repository.
2. Create .env file under src folder (for MongoDB)
3. Copy and paste a video you like under data/s1 folder
4. Unzip (models - checkpoint 96.zip from https://github.com/nicknochnack/LipNet) 
5. Copy and past 3 files (from 4) under models folder
6. cd src
7. command 'python server.py' to start server
8. command 'npm run dev' to start React
9. Click 'Get' button to see the history in console
10. Click 'Post' button to get the prediction of the video you select on 3.
  You can see the prediction in console.

## Please note:
 Models and videos are heavy, so I didnt push them to github.
 Please unzip and copy and paste them.


