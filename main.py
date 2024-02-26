from flask import Flask, render_template, request
import subprocess
import os
import shutil
import docker
import time
from urllib.parse import urlparse
import os


def get_filename_from_url(url):
    path = urlparse(url).path
    filename = os.path.basename(path)
    return filename

def docker_hub_login(username, password):
    try:
        client = docker.from_env()
        client.login(username=username, password=password)
        print("Docker Hub login successful!")
    except docker.errors.APIError as e:
        print(f"Error occurred during Docker Hub login: {e}")
    
#app started from here.
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dockerize', methods=['POST'])
def dockerize():
    github_repo = request.form['github_repo']
    host = request.form['host']
    port = request.form['port']
    image_name = request.form['image_name']
    username = request.form['username']
    password = request.form['password']

    try:
        # Clone GitHub repository
        #subprocess.run(['git', 'clone', github_repo])
        subprocess.run(['wget',  github_repo])
        filename = get_filename_from_url(github_repo)
        docker_image_name = filename[:-4]  # Remove the last 4 characters (which is the extension)

        # Create Dockerfile
        # with open('Dockerfile', 'w') as dockerfile:
        #     dockerfile.write(f"FROM python:3.8\n"
        #                      f"WORKDIR /app\n"
        #                      f"COPY . /app\n"
        #                      f"CMD python app.py\n")
        
        docker_hub_login(username, password)    
        subprocess.run(['docker', 'load', '-i', filename])
        # Build Docker image
        #subprocess.run(['docker', 'build', '-t', image_name, '.'])

        # Push image on docker hub
        #subprocess.run(['docker', 'push', image_name])
            
        # Run Docker container
        #subprocess.run(['docker', 'run', '-d', '-p', f'{host}:{port}:50001', f'{username}/{image_name}'])
        subprocess.run(['docker', 'run', '-d', '-p', f'{host}:{port}:80', '--name', image_name, docker_image_name])

        #os.remove('Dockerfile')
        os.remove(filename)
        #shutil.rmtree('test-python')
        
        dockerized = ('Application Dockerizedzzzz!', f'{username}/{image_name}')
        #return dockerized
        print(len(dockerized))
        return f"{dockerized[0]}, Image Name: {dockerized[1]}"

        #dockerized = ('Application Dockerizedzzzz!', image_name)
      #  return f"Application Dockerized: {dockerized[0]}, Image Name: {dockerized[1]}"
        # Clean up files
        
        
    except Exception as e:
        # Handle exceptions
        return f"An error occurred: {str(e)}"

if __name__ == '__main__':
    app.run(debug=False)
