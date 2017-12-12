#################################################################
#################################################################
############### Datasets2Tools Website Backend ##################
#################################################################
#################################################################
##### Author: Denis Torre
##### Affiliation: Ma'ayan Laboratory,
##### Icahn School of Medicine at Mount Sinai

#######################################################
#######################################################
########## 1. App Configuration
#######################################################
#######################################################

#############################################
########## 1. Load libraries
#############################################
##### 1. Flask modules #####
from flask import Flask, request, url_for, send_from_directory

##### 2. Python modules #####
import os, sys, json, nbformat, time
import urllib.request
from nbconvert.preprocessors import ExecutePreprocessor

##### 3. Custom modules #####

#############################################
########## 2. App Setup
#############################################
##### 1. Flask App #####
entry_point = '/notebook-generator-manager'
app = Flask(__name__, static_url_path=os.path.join(entry_point, 'static'))

#######################################################
#######################################################
########## 2. Routes
#######################################################
#######################################################

#############################################
########## 1. Homepage
#############################################

@app.route(entry_point)
def index():
	return 'Welcome {username}'.format(**os.environ)

#############################################
########## 2. Download
#############################################

@app.route(entry_point+'/download', methods=['POST'])
def download():

	# Get Notebook Data
	notebook_info = json.loads(request.data)

	# Get file
	notebook_file_path = os.path.join('notebook-generator', notebook_info['notebook_uid'], notebook_info['notebook_name'])

	# Save Notebook to File
	if not os.path.exists(notebook_file_path):
		os.makedirs(os.path.dirname(notebook_file_path))
		urllib.request.urlretrieve(notebook_info['raw_notebook_url'], notebook_file_path)
		os.system('jupyter trust '+notebook_file_path)

	# Get Notebook URLs
	live_notebook_url = os.path.join(request.host_url.replace('5000', '8888'), 'notebooks', 'notebook-generator', notebook_info['notebook_uid'], notebook_info['notebook_name'])
	time.sleep(5)

	return live_notebook_url

#############################################
########## 3. Notebooks
#############################################

@app.route(entry_point+'/notebooks/<path:path>')
def notebooks(path):

	# Return
	return send_from_directory('notebook-generator', path)

#######################################################
#######################################################
########## 3. Run App
#######################################################
#######################################################

#############################################
########## 1. Run
#############################################
if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0')