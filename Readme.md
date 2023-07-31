- git pull origin master


- git checkout -b {branch_name}


- create venv




python3 -m venv .venv


py -3 -m venv .venv
- active venv


. .venv/Scripts/activate

- Install flask

pip install Flask

- init-db(one time)


flask --app flashcard init-db
- start app


flask --app flashcard run --debug