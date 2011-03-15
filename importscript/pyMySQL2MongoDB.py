#!/usr/bin/python

import MySQLdb, subprocess

tmp = '/tmp'
ts = [
	'EventsCalendar_event', 'EventsCalendar_location', 'auth_group', 
	'auth_group_permissions', 'auth_message', 'auth_permission',
	'auth_user', 'auth_user_groups', 'auth_user_user_permissions',
	'django_admin_log', 'django_content_type', 'django_session',
	'django_site', 'south_migrationhistory'
]
base_query = 'SELECT * FROM %s INTO OUTFILE "%s/%s.csv" FIELDS TERMINATED BY "," OPTIONALLY ENCLOSED BY \'"\' LINES TERMINATED BY \'\n\''

queries = []
for table in ts:
    queries.append(base_query % (table, tmp, table))

# Get a mysql connection
conn = MySQLdb.connect(host = 'localhost', user='root', passwd='dandp1', db='events')
cursor = conn.cursor()

# Export all the data in the tables to <table>.csv
for query in queries:
    cursor.execute(query)

# done with MySQL so close the connection
conn.close()

# now use mongoimport to import all the csv files into the mongodb
fields = [
	'_id,title,user_id,location_id,date,start_time,end_time,desc,created', # EventsCalendar_event
	'_id,name,user_id,address,city,state,zip_code,desc,created', # EventsCalendar_location
	'_id,name', # auth_group
	'_id,group_id,permission_id', # auth_group_permissions
	'_id,user_id,message', # auth_message
	'_id,name,content_type_id,codename', # auth_permission
	'_id,username,first_name,last_name,email,password,is_staff,is_active,is_superuser,last_login,date_joined', # auth_user
	'_id,user_id,group_id', # auth_user_groups
	'_id,user_id,permission_id', # auth_user_user_permissions
	'_id,action_time,user_id,content_type_id,object_id,object_repr,action_flag,change_message', # django_admin_log
	'_id,name,app_label,model', # django_content_type
	'_id,session_data,expire_date', # django_session
	'_id,domain,name', # django_site
	'_id,app_name,migration,applied' # south_migrationhistory
]

base_cmd = ['mongoimport', '--host', 'localhost', '--db', 'events', '--type', 'csv', '--collection', '%s', '-f', '%s', '--file', '%s/%s.csv', '--drop']

for n in range(len(ts)):
    new_cmd = list(base_cmd)
    new_cmd[8], new_cmd[10], new_cmd[12] = (new_cmd[8] % ts[n],new_cmd[10] % fields[n], new_cmd[12] % (tmp,ts[n]))
    subprocess.call(new_cmd)
