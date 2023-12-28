# unzip rollback zip to real server directory
unzip /home/keyfa_user/project/cicd/rollback.zip -d /home/keyfa_user/project/server

systemctl --user restart keyfa
systemctl --user status keyfa
