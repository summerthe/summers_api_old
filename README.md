# Summers API

## Apps

APIs for following apps.

### user

App to manage Authenticatation.

### trakt

Trakt is tracking app to track the tv show you are watching.

### locker

Obsidian inspired note app to store notes for personal uses.

### tube2drive

App to download whole youtube playlist and upload to google drive.

## Celery

This app comes with Celery.

To run a celery worker:

``` bash
cd summers_api
celery -A config.celery_app worker -l info
```
