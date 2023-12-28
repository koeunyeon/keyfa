# zip for rollback
zip -r /home/keyfa_user/project/cicd/rollback.zip /home/keyfa_user/project/server/*

# copy new deploy to backup directory
cp /home/keyfa_user/project/cicd/latest/keyfa_service_api.zip /home/keyfa_user/project/cicd/backup/keyfa_service_api_`date + "%Y%m%d%H%M`.zip

# unzip to temp directory
rm /home/keyfa_user/project/cicd/temp/* -R
unzip /home/keyfa_user/project/cicd/latest/keyfa_service_api.zip -d /home/keyfa_user/project/cicd/temp

# copy temp dir to real app directory
cp /home/keyfa_user/project/cicd/temp/server/* /home/keyfa_user/project/server/ -r

# restart server and check status
systemctl --user restart keyfa
systemctl --user status keyfa
