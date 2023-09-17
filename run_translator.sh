#!/bin/bash

sudo docker run -d -p 1969:1969 --rm --name translation-server zotero/translation-server

/home/furtado/anaconda3/envs/p39web/bin/python call_translators.py

sudo docker kill translation-server