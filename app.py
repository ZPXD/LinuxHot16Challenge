from flask import Flask, render_template, redirect, url_for

import os
import requests


app = Flask(__name__)
app.secret_key = ':)'


here = os.getcwd()
classic_data_folder = os.path.join(here, 'data', 'wasze_zwrotki')
freestyle_data_folder = os.path.join(here, 'data', 'wasze_zwrotki_freestyle')


def check_file_ANTI_MALWARE():
	pass

def get_file_data():
	pass

def get_fresh_data():
	repo_url = 'https://github.com/ZPXD/LinuxHot16Challenge.git'
	delete = os.path.join(classic_data_folder, 'LinuxHot16Challenge')
	what = os.path.join(classic_data_folder, 'LinuxHot16Challenge', 'wasze_zwrotki')
	existing_files = os.listdir(classic_data_folder)
	os.system( 'git clone {} {}'.format(repo_url, delete) )
	fresh_files = os.listdir(what)
	for f in fresh_files:
		if f not in existing_files:
			fp1 = os.path.join(what, f)
			fp2 = os.path.join(classic_data_folder, f)
			os.system('cp -r {} {}'.format(fp1, fp2))
	os.system( 'sudo rm -r {}'.format(delete))

def sort_by_rank(commands_list):
	commands_list = sorted(commands_list, key=lambda k : k['rank'])[::-1]
	return commands_list

def get_file_data_lines(fn):
	file_path = os.path.join(classic_data_folder, fn)
	with open(file_path, 'r', encoding="utf-8") as f:
		text_lines = f.readlines()
	text_lines = [l.encode('utf-8').decode().strip() for l in text_lines if '#' in l]
	return text_lines


def command_wiki(command):
	url = 'https://man7.org/linux/man-pages/man1/{}.1.html'.format(command)
	return url

def command_wiki_pl(command):
	url = 'https://linux.fandom.com/pl/wiki/{}'.format(command)
	return url

def load_classic_data():
	
	commands_list = []

	file_names = os.listdir(classic_data_folder)
	for fn in file_names:

		if fn == 'README.md' or fn == 'TWOJEIMIE_linux_hot_16_challenge.txt':
			continue

		text_lines = get_file_data_lines(fn)
		
		for idx, l in enumerate(text_lines):
			line_elements = l.split()

			if len(line_elements) >= 3:	
				ranking = line_elements[1]
				if '.' in ranking:
					ranking = ranking.replace('.', '')
					if ranking.isnumeric():

						command = {}
						command['name'] = None
						command['rank'] = None
						command['rank_list'] = []
						command['description'] = []

						# Name:
						name = line_elements[2]
						other_options = line_elements[3:]
						

						name = name.strip()
						command['name'] = name
						if command['name'] in ['komenda']:
							continue

						# Wiki: 
						command['wiki'] = command_wiki(name)
						command['wiki_pl'] = command_wiki_pl(name)

						# Update existing command data or add new:
						existing_commands = [c['name'] for c in commands_list]
						if command['name'] in existing_commands:
							i, command = [[i, c] for [i, c] in enumerate(commands_list) if c['name'] == command['name']][0]
							commands_list.pop(i)

						# Ranking:
						rank = int(ranking)
						rank = 33 - rank
						command['rank_list'].append(rank)
						command['rank'] = sum(command['rank_list'])

						# Description:
						description = text_lines[idx+1]
						description = description.replace('#', '')
						description = description.strip()
						command['description'].append(description)
						commands_list.append(command)
	return commands_list

@app.route('/')
def mg():
	commands_list = load_classic_data()
	commands_list = sort_by_rank(commands_list)
	ranking = []
	for i, c in enumerate(commands_list, 1):
		c['nr'] = i
		ranking.append(c)
	return render_template("index.html", ranking=ranking)

@app.route('/freestyle')
def hot_16_challenge_freestyle():
	return render_template("freestyle.html")

@app.route('/dodaj_swoje_zwrotki')
def hot_16_add_yours():
	return render_template("freestyle.html")


# Errors

@app.errorhandler(404)
def handle_404(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def handle_500(e):
    return render_template('500.html'), 500


if __name__=="__main__":
	app.run(debug=True)
