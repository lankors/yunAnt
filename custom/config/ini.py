#/usr/bin/python evn
#coding=utf-8

from ConfigParser import SafeConfigParser
import os, sys
import codecs
import logging

"""
Configuration layout for default base config
"""
DEFAULT_CONFIG = { "general":
                    {
                        "debug": ("bool", False),
                    } 
                 }

class Section:
    """provides dictionary like access for configparser"""

    def __init__(self, parser, section):
        """Constructor"""
        self.parser = parser
        self.section = section

    def __getitem__(self, item):
        """getitem"""
        if item not in self.parser.options(self.section):
            raise KeyError("'%s' not in config section[%s]" % (item, self.section))

        try:
            type = DEFAULT_CONFIG[self.section][item][0]
        except:
            type = str

        if type == 'int':
            return self.parser.getint(self.section, item)
        elif type == 'float':
            return self.parser.getfloat(self.section, item)
        elif type == 'bool':
            return self.parser.getboolean(self.section, item)

        # else type == 'str'
        return self.parser.get(self.section, item)

    def __setitem__(self, item, value):
        """setitem"""
        self.parser.set(self.section, item, value)


class DictConfigParser(SafeConfigParser):
    def __init__(self, configfile):
        self.configfile = configfile
        self.configParser = SafeConfigParser()

        
        failed = False
        try:
            #localFSCoding = sys.getfilesystemencoding()
            with codecs.open(self.configfile, 'r', encoding="utf-8") as f:
                self.configParser.readfp(f)
        except Exception as e:
            logging.warn("Cannot read config file: %s because of %s" % (self.configfile, e))
            failed = True

        if failed:
            logging.debug("Load defaul config as we failed to load/validate current config")
            self.loadDefaultConfig()

    def loadDefaultConfig(self):
        for sec in DEFAULT_CONFIG.keys():
            self.configParser.add_section(sec)
            items = DEFAULT_CONFIG[sec]
            for (name, value) in items:
                self.configParser.set(sec, name, str(value[1]))

    def save(self):
        with open(self.configfile, 'wb') as configfile:
            self.configParser.write(configfile)

    def __getitem__(self, section):
        """provides dictionary like access: c['section']['option']"""
        if section not in self.configParser.sections():
            raise KeyError("section '%s' not in config" % section)

        return Section(self.configParser, section)

    def __contains__(self, section):
        """ checks if parser contains section """
        return section in self.configParser.sections()

