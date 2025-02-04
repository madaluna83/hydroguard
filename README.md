HydroGuard develops and builds upon this current body of research by focusing on a software-simulated approach to water quality monitoring. 

To run this project you have to: 
1. Make sure you have postgreSQL installed and connected to the server (from a command in terminal, or from pgAdmin)
2. The ports 5000, 1883 are free. If it's not you can kill the process.
3. If not installed some pakages from the project, you should run into errors when you open the project if you have an Python IDE, otherwise you'll se when you run the commands. Basically you will need to install Flask, mosquitto, psycopg2, soketio and requests. 
4. Change the password from your DB in files: generate_csv_file.py, import_csvfile.py,  server.py, init_db.py.
5. Then open a terminal, go to the file you have saved the project and run server.py, client.py and gateway.py. I usually run them in 3 terminals throgh the VSC.
6. Open a browser and go to the http://localhost:5000/ and you'll see the dashboard.  
