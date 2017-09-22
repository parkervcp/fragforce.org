from bs4 import BeautifulSoup, CData


class PfSenseBackup(object):
    def __init__(self):
        self.doc = BeautifulSoup('', 'xml')

    def render(self, pretty=True):
        if pretty:
            return self.doc.prettify()
        else:
            return str(self.doc)

    def make_child_nfo(self, name, value):
        tag = self.doc.new_tag(name)
        tag.append(value)
        return tag

    def add_child_nfo(self, parent, name, value):
        assert hasattr(parent, 'append'), "Expected %r to have an append method" % parent
        return parent.append(self.make_child_nfo(name=name, value=value))


class AliasBackup(PfSenseBackup):
    def __init__(self):
        super(AliasBackup, self).__init__()
        self.add_aliases_base()


    def add_aliases_base(self):
        aliases = self.doc.new_tag('aliases')
        self.doc.append(aliases)

    def add_alias(self, name, type_, url, updatefreq=1, address=None, descr='', detail=''):
        if address is None:
            address = url

        """ Add an alias table """
        alias = self.doc.new_tag('alias')
        self.add_child_nfo(alias, 'name', name)
        self.add_child_nfo(alias, 'type', type_)
        self.add_child_nfo(alias, 'url', url)
        self.add_child_nfo(alias, 'updatefreq', updatefreq)
        self.add_child_nfo(alias, 'address', address)
        self.add_child_nfo(alias, 'descr', CData(descr))
        self.add_child_nfo(alias, 'detail', CData(detail))
        self.doc.aliases.append(alias)

    def add_port_alias(self, name, url, update_frequency_days, description):
        """ Add a port alias table """
        self.add_alias(
            name=name,
            type_='urltable_ports',
            url=url,
            updatefreq=update_frequency_days,
            address=url,
            descr=description,
            detail='Table %r' % name,
        )

    def add_ip_alias(self, name, url, update_frequency_days=1, description=''):
        """ Add an IP alias table """
        self.add_alias(
            name=name,
            type_='urltable',
            url=url,
            updatefreq=update_frequency_days,
            address=url,
            descr=description,
            detail='Table %r' % name,
        )
