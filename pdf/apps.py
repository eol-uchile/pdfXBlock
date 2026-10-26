from __future__ import unicode_literals

from django.apps import AppConfig
from openedx.core.djangoapps.plugins.constants import PluginSettings, ProjectType, SettingsType


class PdfXBlockConfig(AppConfig):
    name = u'pdf'

    plugin_app = {
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
