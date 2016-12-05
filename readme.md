# Snake Game with Mice Agent 

## First-time setup 
1. Install `virtualenv` globally on your system: `pip install virtualenv`
2. Create a virtual environment for this project: `virtualenv venv`
3. Install current requirements locally in the virtual environment: `pip install -r requirements.txt`

## During work sesh
1. Activate the virtual environment so that you have access to the locally installed requirements: `source venv/bin/activate`
2. When you're done, deactivate the virtual environment with: `deactivate`

If you encounter a runtime error, it's probably because someone installed a new requirement and you don't have it locally. So update your virtual environment with: `pip install -r requirements.txt` 

## If you change requirements...  
1. Install new requirement using pip: `pip install <new_library>`
2. Save them so that we have access: `pip freeze > requirements.txt`

## Run 
Pass in the snake agent with `-s` and the number of trials with `-n`. For quiet mode (or no graphics), use `-q`.

For example: `python snakeAgent.py -s greedy -n 10 -q`
This will run the Greedy snake agent 10 times, with no graphics. 