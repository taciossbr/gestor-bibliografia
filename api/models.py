

class Person:
    def __init__(self, id=None, firstname=None, middlename=None, lastname=None, suffix=None):
        self.id = id
        self.firstname = firstname
        self.middlename = middlename
        self.lastname = lastname
        self.suffix = suffix
    
    def __repr__(self):
        return f'Person(id={self.id}, firstname={self.firstname}, middlename={self.middlename}, lastname={self.lastname}, suffix=s{self.suffix})'
    


class Source:
    def __init__(self, id, date, title, subtitle, local):
        self.id = id
        self.date = date
        self.title = title
        self.subtitle = subtitle
        self.local = local
    def __repr__(self):
        return f'''{self.__class__.__name__}({', '.join(
            [f'{k}={getattr(self, k)}' for k in dir(self) if not k.startswith('_')])})'''
class Article(Source):
    def __init__(self, id, date, title, subtitle, local,
                 doi, journal, vol_journal, fascicle):
        super().__init__(id, date, title, subtitle, local)
        self.doi = doi
        self.journal = journal
        self.vol_journal = vol_journal
        self.fascicle = fascicle

class Site(Source):
    def __init__(self, id, date, title, subtitle, local,
                 link, dt_access):
        super().__init__(id, date, title, subtitle, local)
        self.link = link
        self.dt_access = dt_access

class Book(Source):
    def __init__(self, id, date, title, subtitle, local,
                 isbn, publisher, series, edition, vol):
        super().__init__(id, date, title, subtitle, local)
        self.isbn = isbn
        self.publisher = publisher
        self.series = series
        self.edition = edition
        self.vol = vol

class Project:
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome
    def __repr__(self):
        return f'Project(id={self.id}, nome="{self.nome}")'