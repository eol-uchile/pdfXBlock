pdfXBlock
=========

![https://github.com/eol-uchile/pdfXBlock/actions](https://github.com/eol-uchile/pdfXBlock/workflows/Python%20application/badge.svg)

### Description ###

This XBlock provides an easy way to embed a PDF. Modified by EOL-TEAM.

### File Upload Configuration

Add this configuration in `production.py`

```
## Setup PDF for S3
PDF_STORAGE_CLASS = {
  'class': 'storages.backends.s3boto3.S3Boto3Storage',
  'options': {
    'location': 'pdf/',
    'bucket_name': 'bucketname'
  }
}
PDF_STORAGE_CLASS = ENV_TOKENS.get('PDF_STORAGE_CLASS', PDF_STORAGE_CLASS)
```

`LMS` & `CMS` .yml:

```
  X_FRAME_OPTIONS: SAMEORIGIN
```

Fileupload max size: 100mb (customizable)

### Activate the XBlock in your course ###
Go to `Settings -> Advanced Settings` and set `advanced_modules` to `["pdf"]`.

### Use the XBlock in a unit ###
Select `Advanced -> PDF` in your unit.


### XBlock translations ###
Prepare your environment:

```
docker run -it --rm -w /code -v $(pwd):/code python:3.5 bash
make requirements
apt-get update
apt-get install gettext
```

Extract strings to be translated, outputting .po files
```
make extract_translations
```

Use text.po from `/en/` as the base file and make the translations.

Compile translation files, outputting .mo files for each supported language.
```
make pull_translations
```

### TESTS
**Prepare tests:**

    > cd .github/
    > docker-compose run --rm lms /openedx/requirements/pdfXBlock/.github/test.sh
