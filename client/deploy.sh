#!/bin/bash
# ng build --deploy-url /static/ --prod
# cp dist/client/*.js dist/client/*.css ../static
# cp dist/client/index.html ../templates

ng build  --prod
cp dist/client/*.js dist/client/*.css ../static
cp dist/client/index.html ../static