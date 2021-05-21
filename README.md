# wfrp4e rpc-sheet served by Flask
Naive Flask app to handle rpc sheets for eager rollplayers.
It will never be finished - help is welcome, but keep it simple.

## Requires
> Python3 as of 2021-05
> pip


## Usage
`git clone <this repo> <target dir>`

`cd <target_dir>`

### Create a python container/environment
`python3 -m venv venv`

### Enter the sandbox
`source venv/bin/activate`

### Install all python stuff needed
`pip install -r requirements.txt`

### Cofigure server and players
Copy players.py.example to players.py and edit the settings within.

### Start the app
`python3 ./tub-control.py`
