To run this project create a virtual environment by running the below commands.

```
mkdir [% NAME_OF_YOUR_DIRECTORY %]
cd [% NAME_OF_YOUR_DIRECTORY %]
python3 -m venv venv
source venv/bin/activate
```

Make sure your virtual environment is activated and install the dependencies in the requirements.txt file inside.

`pip install -r requirements.txt`

Make sure you're in the directory with the manage.py file and run the project in the development server.

`python manage.py runserver`

if that does not work try

`python3 manage.py runserver`


Open the file `~\GDSC-master\transcript\templates\home.html`

Allow access to your microphone and start speaking. A translation of the audio will appear in the browser.
