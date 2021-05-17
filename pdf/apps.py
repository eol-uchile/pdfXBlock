from __future__ import unicode_literals

from django.apps import AppConfig
from openedx.core.djangoapps.plugins.constants import PluginSettings, PluginURLs, ProjectType, SettingsType


class PdfXBlockConfig(AppConfig):
    name = u'pdf'

    plugin_app = {
        PluginURLs.CONFIG: {
            ProjectType.LMS: {
                PluginURLs.NAMESPACE: u'eol/pdf',
                PluginURLs.REGEX: r'^',
                PluginURLs.RELATIVE_PATH: u'urls',
            },
            ProjectType.CMS: {
                PluginURLs.NAMESPACE: u'eol/pdf',
                PluginURLs.REGEX: r'^',
                PluginURLs.RELATIVE_PATH: u'urls',
            }
        },
        PluginSettings.CONFIG: {
            ProjectType.LMS: {
                SettingsType.COMMON: {
                    PluginSettings.RELATIVE_PATH: u'settings.common'},
            },
            ProjectType.CMS: {
                SettingsType.COMMON: {
                    PluginSettings.RELATIVE_PATH: u'settings.common'},
            }
        }
    }

    def ready(self):
        pass 