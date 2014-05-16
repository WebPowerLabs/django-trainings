#!/bin/sh
echo -n "lessc bootstrap.css..."
lessc -x ./dtf/app/static/app/less/zak-bootstrap.less > ./dtf/app/static/app/css/bootstrap.css
echo "done"

