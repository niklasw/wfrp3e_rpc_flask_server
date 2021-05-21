import os
from os.path import join as pjoin
from flask import Flask,url_for,redirect,render_template,request,Response,session
#from flask_htpasswd import HtPasswdAuth
import flaskr
from jinja2 import Template
import glob, pickle
from pathlib import Path
# config is simply python definitions
# credentials = {'<user>':'<pass>',...}
from players import server_ip, server_port, http_scheme, credentials

from character import *

app = Flask(__name__, template_folder='templates')

app.secret_key = os.urandom(24)

players = credentials.keys()

db_dir = Path.cwd()/'db'

rpcs = {}

def authorize(credentials, name, password):
    if name in credentials and credentials[name] == password:
        print(name,'login OK')
        return True
    else:
        print(name,'login Fail')
        return False

def load_rpc(player, rpcs, use_file=None):
    import shutil
    dfile = use_file if use_file else Path(db_dir/player) 
    if dfile.exists():
        bak = dfile.with_suffix('.bak')
        load_ok = False
        print(f'Loading player {player} from disk')
        try:
            with dfile.open('rb') as fdump:
                rpcs[player] = pickle.load(fdump)
            load_ok = True
        except:
            load_ok = False
            print(f'Error: Failed loading {player} from disk')
        if load_ok:
            if bak.exists() and not os.path.samefile(dfile,bak):
                print(f'Creating backup on disk {bak}')
                shutil.copy(dfile,bak)
        else:
            load_rpc(player,rpcs,use_file=bak)
    if not player in rpcs:
        print(f'Creating player {player} from scratch')
        rpcs[player] = RPC(player)

def store_rpc(rpc):
    try:
        with open(db_dir/rpc.player,'wb') as fdump:
            print(f'Storing player {rpc.player} to disk')
            pickle.dump(rpc, fdump)
    except:
        print(f'Failed to store player {rpc.player} to disk')

@app.route('/', methods=['GET','POST'])
def select_character():
    if request.method == 'POST':
        pwd = request.form.get('pwd')
        name = request.form.get('player')
        if authorize(credentials, name, pwd):
            session['username'] = name
            return redirect(url_for('show_sheet',player=name, **http_scheme))
        else:
            session.clear()
    return render_template('login.html', players=players)

@app.route('/logoff')
def logoff():
    session.clear()
    return redirect(url_for('select_character', **http_scheme))

def session_ok(player):
    ok = player in players and \
         'username' in session and \
         player == session['username']
    if not ok:
        print(player, 'session not OK')
    return ok

@app.route('/sheet/<player>', methods=['POST', 'GET'])
#@htpasswd.required
def show_sheet(player): #,user):
    if not session_ok(player):
        return redirect(url_for('select_character', **http_scheme))

    if not player in rpcs:
        load_rpc(player, rpcs)

    rpc = rpcs[player]
    
    ## rpc.characteristics.get('dex').set('initial', 42)
    ## rpc.characteristics.get('dex').set('advance', 2)
    ## rpc.characteristics.get('Wp').set('advance', 5)
    ## rpc.skills.get('art').set('advance', 5)
    ## rpc.skills.get('melee basic').set('advance', 5)
    ## rpc.refresh_skills()
    ## for skill in rpc.skills.added():
    ##     print(skill)

    out  = render_template('wfrp_sheet.html', rpc = rpc)
    return(out)

@app.route('/handle_form/<string:player>', methods=['POST'])
def handle_form(player):
    if session_ok(player):
        rpc = rpcs[player]
        if request.method == 'POST':
            print('POST')
            rpc.read_form(request.form)
            store_rpc(rpc)
        return redirect(url_for('show_sheet', player=rpc.player, **http_scheme))
    else:
        return redirect(url_for('logoff', **http_scheme))

if __name__ == '__main__':
    app.run(host=server_ip,port=server_port,debug=True)
