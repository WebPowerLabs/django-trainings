#!/bin/sh
echo -n "lessc bootstrap.css..."
lessc -x ./dtf/app/static/app/less/bootstrap-router.less > ./dtf/app/static/app/css/bootstrap.css
echo "done"
