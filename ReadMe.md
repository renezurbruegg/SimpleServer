# Simple Flask + MongoDB Server
This is a simple Flask server that uses a MongoDB database to store names into a database and list them if the corresponding api route (URL) is called.

## Set UP
1. [Clone](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository) Repository
2. Install MongoDB on your computer (https://docs.mongodb.com/manual/installation/)
3. Install requirements:
    ```bash 
    cd SimpleServer
   pip install -r requirements.txt
   ```
 4. Make sure mongodb is running on port 27017
 
 ## Starting server
 ```bash 
   cd SimpleServer
   python run.py
   ```
Output should look like this
```Logging into directory [....]logs
2020-03-19 18:33:58 [WARNING ] [fask_cors.core.serialize_option:357] Unknown option passed to Flask-CORS: headers
2020-03-19 18:33:58 [WARNING ] [flask_cors.core.serialize_option:357] Unknown option passed to Flask-CORS: headers
2020-03-19 18:33:58 [INFO    ] [flask_app.server.main:51            ] starting server
 * Serving Flask app "flask_app.server" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
2020-03-19 18:33:58 [INFO    ] [werkzeug._log:122                   ]  * Restarting with stat```
```

## Listing database entries:
Open http://localhost:8080/api/listUser in your browser.

## Adding a new user:
1. If not allready, intall [Postman](https://www.postman.com/downloads/)
2. Open up postman and create a new Post request:

URL: localhost:8080/api/addUser
Body: {
	"name":"newuser"
}
![](postman.jpg)
3. Send request.
4. Load  http://localhost:8080/api/listUser to see changes
#### Example output:
![](sampleOutput.jpg)
