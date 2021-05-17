#!/bin/dash

pip install -e /openedx/requirements/pdfXBlock

cd /openedx/requirements/pdfXBlock
cp /openedx/edx-platform/setup.cfg .
mkdir test_root
cd test_root/
ln -s /openedx/staticfiles .

cd /openedx/requirements/pdfXBlock

DJANGO_SETTINGS_MODULE=lms.envs.test EDXAPP_TEST_MONGO_HOST=mongodb pytest pdf/tests.py

rm -rf test_root