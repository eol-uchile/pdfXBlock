pdfXBlock
=========

### Description ###

This XBlock provides an easy way to embed a PDF.

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

Fileupload max size: 40mb (customizable)

### Activate the XBlock in your course ###
Go to `Settings -> Advanced Settings` and set `advanced_modules` to `["pdf"]`.

### Use the XBlock in a unit ###
Select `Advanced -> PDF` in your unit.


### Working with Translations ###

For information about working with translations, see the [Internationalization Support](http://edx.readthedocs.io/projects/xblock-tutorial/en/latest/edx_platform/edx_lms.html#internationalization-support) section of the [Open edX XBlock Tutorial](https://xblock-tutorial.readthedocs.io/en/latest/).

#### Working with Transifex ####
Prepare your environment:

```
$ mkvirtualenv pdf-xblock
$ make requirements
```

Also ensure that the [Transifex client has the proper authentication](https://docs.transifex.com/client/init) 
in the `~/.transifexrc` file.

Push new strings to Transifex:
```
$ make push_translations
```

To get the latest translations from Transifex:
```
$ make pull_translations
```

For testing purposes it's faster to avoid Transifex and work on dummy Esperanto translations:
```
$ make build_dummy_translations
``` 
