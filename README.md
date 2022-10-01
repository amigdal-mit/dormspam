# Template React + Flask framework

Created and maintained by: TheReddKing (TechX)

## Dev:
### Local Installation:

    python -m venv env
    source env/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    yarn
    cp .env.example .env
    cd client && yarn

Then edit your `.env` file. Once your database url is correct (you can use `createdb template` if you have postgres)

    python manage.py db init
    python manage.py db migrate
    python manage.py db upgrade

### Dev run

    yarn run dev
    
or (if you want to debug server side scripts)

    yarn start
    yarn run dev-server


### Editing

Look at the HOWTHISWASMADE.md file for more information

## Deploy on HEROKU

You first need to actually create a heroku application. You can also use the `app.json` to deploy (you can read about it somewhere else)

Then you need to copy over the environmental variables from your local computer

    sed 's/#[^("|'')]*$//;s/^#.*$//' .env | \
    xargs heroku config:set

Afterwards, a simple heroku push will configure everything

    git push heroku master
        
## Approximate Initial Deploy on Scripts

Instructions to be loosely followed, use your own judgement.
Only tested once on Fedora 30 servers, and I may have forgotten to write down a command or two.

1. [Enable mail scripts](https://scripts.mit.edu/mail/).
2. Run from a computer with AFS, once `cd`'d into the locker:
   ```bash
   mkdir -p Scripts/dormspam
   fs sa daemon.scripts rlidwk Scripts/dormspam
   cd Scripts/dormspam
   git clone <backend.git> backend
   cp backend/mail_scripts/* ../../mail_scripts/ # Will overwrite procmailrc!
   ```
4. Run from a Scripts server:
   ```bash
   cd ~/Scripts/dormspam/backend
   python3 -m venv --system-site-packages env # --system-site-packages for mysqlclient, which currently won't install in a venv.
   . env/bin/activate
   pip install --upgrade pip wheel
   pip install -r requirements.txt
   deactivate
   ```
5. Make the database, and create `.env` with the database info.
6. From a Scripts server:
   ```bash
   cd ~/Scripts/dormspam/backend
   . env/bin/activate
   python manage.py db init
   python manage.py db migrate
   python manage.py db upgrade
   deactivate
   ```
7. Build [the frontend](https://github.com/dormspam/frontend) on your own computer.
   - Update the frontend's `.env`.
   - Update `homepage` in `package.json`.
   - `npm run build`
8. Copy over the `build` folder to `~/Scripts/dormspam/backend/server/build` on AFS.
9. In the `web_scripts` directory you want, make `.htaccess`:
   ```apache
   AuthType SSLCert
   Require valid-user
   ErrorDocument 401 /__scripts/needcerts

   RewriteEngine On

   RewriteRule ^$ index.fcgi/ [QSA,L]

   RewriteCond %{REQUEST_FILENAME} !-f
   RewriteCond %{REQUEST_FILENAME} !-d
   RewriteRule ^(.*)$ index.fcgi/$1 [QSA,L]
   ```
   And make `index.fcgi`:
   ```python
   #!/afs/athena.mit.edu/<path/to/locker>/Scripts/dormspam/backend/env/bin/python

   import sys, os

   backend = os.environ['HOME'] + '/Scripts/dormspam/backend'
   sys.path.insert(0, backend)
   os.chdir(backend)

   from flup.server.fcgi import WSGIServer
   from server.app import app

   if __name__ == '__main__':
       WSGIServer(app).run()
   ```
 