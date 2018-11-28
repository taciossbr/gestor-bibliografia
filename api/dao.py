from .models import Person, Source, Article, Site, Book, Project
from sqlite3 import IntegrityError

class DAO():

    def __init__(self, conn):
        self._conn = conn

class PersonDAO(DAO):
    
    def adiciona_pessoa(self, firstname=None, middlename=None, lastname=None, suffix=None):
        if firstname is None:
            raise Exception('firstname not provided')
        if lastname is None:
            raise Exception('lastname not provided')
        
        cursor = self._conn.cursor()
        cursor.execute("""
            INSERT INTO person VALUES
            (NULL, ?, ?, ?, ?)
            """, (firstname, middlename, lastname, suffix))
        self._conn.commit()
        return Person(cursor.lastrowid, firstname, middlename, lastname, suffix)
    
    def todas_pessoas(self):
        cursor = self._conn.cursor()
        cursor.execute("""
            SELECT * FROM person;
            """)
        pessoas = []
        for row in cursor.fetchall():
            pessoas.append(Person(row[0], row[1], row[2], row[3], row[4]))
        return pessoas

class SourceDAO(DAO):

    def todos_sources(self):
        cursor = self._conn.cursor()
        cursor.execute("SELECT * FROM source")

        return [Source(*row) for row in cursor.fetchall()]

    def complete_table(self):
        cursor = self._conn.cursor()

        cursor.execute("""
            SELECT src.id_source, src.date, src.title, src.title, src.subtitle, src.local,
                b.isbn, b.publisher, b.series_book,  b.edition_book, b.vol_book,
                a.doi, a.journal, a.vol_journal,
                s.link, s.dt_access, a.fascicle
            FROM source as src
            LEFT JOIN site as s ON src.id_source = s.id_source
            LEFT JOIN article as a ON src.id_source = a.id_source
            LEFT JOIN book as b ON src.id_source = b.id_source;""")

        return [row for row in cursor.fetchall()]

    def _add_source(self, date, title, subtitle, local):
        cursor = self._conn.cursor()
        cursor.execute("""
            INSERT INTO
            source (date, title, subtitle, local)
            VALUES
            (?, ?, ?, ?)""", (date, title, subtitle, local))
        self._conn.commit()
        return cursor.lastrowid
    
    def autores(self, id):
        cursor = self._conn.cursor()
        cursor.execute("""
            select person.id_person, firstname, middlename, lastname, suffix from person_contribute_source
            join person on person.id_person = person_contribute_source.id_person
            where type = 'autor' and id_source = ?;""", (id, ))

        return [Person(*row) for row in cursor.fetchall()]

class ArticleDAO(SourceDAO):

    def todos_articles(self):
        cursor = self._conn.cursor()
        cursor.execute("""
            SELECT src.id_source, src.date, src.title, src.subtitle, src.local,
                a.doi, a.journal, a.vol_journal, a.fascicle
            FROM source as src
            JOIN article as a ON src.id_source = a.id_source;""")
        
        return [Article(*row) for row in cursor.fetchall()]
        # for row in cursor.fetchall():
        #     print(row)

    def adiciona_article(self, date, title, subtitle, local,
                         doi, journal, vol_journal, fascicle):
        id = self._add_source(date, title, subtitle, local)

        cursor = self._conn.cursor()

        cursor.execute("""
            INSERT INTO article VALUES
            (?, ?, ?, ?, ?)""", (id, doi, journal, vol_journal, fascicle))
        self._conn.commit()
        return Article(cursor.lastrowid, date, title, subtitle, local,
                 doi, journal, vol_journal, fascicle)
       
class SiteDAO(SourceDAO):

    def todos_sites(self):
        cursor = self._conn.cursor()
        cursor.execute("""
            SELECT src.id_source, src.date, src.title, src.subtitle, src.local,
                s.link, s.dt_access
            FROM source as src
            JOIN site as s ON src.id_source = s.id_source;""")

        return [Site(*row) for row in cursor.fetchall()]

    def adiciona_site(self, date, title, subtitle, local,
                         link, dt_access):
        id = self._add_source(date, title, subtitle, local)

        cursor = self._conn.cursor()

        cursor.execute("""
            INSERT INTO site VALUES
            (?, ?, ?)""", (id, link, dt_access))
        self._conn.commit()
        return Site(cursor.lastrowid, date, title, subtitle, local,
                       link, dt_access)

class BookDAO(SourceDAO):

    def todos_books(self):
        cursor = self._conn.cursor()
        cursor.execute("""
            SELECT src.id_source, src.date, src.title,  src.subtitle, src.local,
                b.isbn, b.publisher, b.series_book,  b.edition_book, b.vol_book
            FROM source as src
            JOIN book as b ON src.id_source = b.id_source;""")

        return [Book(*row) for row in cursor.fetchall()]

    def adiciona_book(self, date, title, subtitle, local,
                         isbn, publisher, series, edition, vol):
        id = self._add_source(date, title, subtitle, local)

        cursor = self._conn.cursor()

        cursor.execute("""
            INSERT INTO book VALUES
            (?, ?, ?, ?, ?, ?)""", (id, isbn, publisher, series, edition, vol))
        self._conn.commit()

        return Book(cursor.lastrowid, date, title, subtitle, local,
                    isbn, publisher, series, edition, vol)

    


class ProjectDAO(DAO):
    def adiciona_projeto(self, nome):
        cursor = self._conn.cursor()
        cursor.execute("""
            INSERT INTO project(nome) VALUES
            (?);""", tuple([nome]))
        self._conn.commit()
        return Project(id=cursor.lastrowid, nome=nome)
    
    def get_refs(self, id_proj):
        cursor = self._conn.cursor()
        cursor.execute("""
            SELECT src.id_source, src.date, src.title, src.subtitle, src.local,
                a.doi, a.journal, a.vol_journal, a.fascicle
            FROM source as src
            JOIN article as a ON src.id_source = a.id_source
            JOIN project_quote_source on project_quote_source.id_source = src.id_source
            WHERE id_proj = ?;""", (id_proj, ))
        
        l = [Article(*row) for row in cursor.fetchall()]

        cursor.execute("""
            SELECT src.id_source, src.date, src.title,  src.subtitle, src.local,
                b.isbn, b.publisher, b.series_book,  b.edition_book, b.vol_book
            FROM source as src
            JOIN book as b ON src.id_source = b.id_source
            JOIN project_quote_source on project_quote_source.id_source = src.id_source
            WHERE id_proj = ?;""", (id_proj, ))

        l += [Book(*row) for row in cursor.fetchall()]

        cursor.execute("""
            SELECT src.id_source, src.date, src.title, src.subtitle, src.local,
                s.link, s.dt_access
            FROM source as src
            JOIN site as s ON src.id_source = s.id_source
            JOIN project_quote_source on project_quote_source.id_source = src.id_source
            WHERE id_proj = ?;""", (id_proj, ))
        
        l += [Site(*row) for row in cursor.fetchall()]

        return l



    def todos_projetos(self):
        cursor = self._conn.cursor()
        cursor.execute("""
            SELECT * FROM project;""")
        return [Project(id, nome) for id, nome in cursor.fetchall()]
    def quote(self, id_proj, id_source, ini=None, fim=None):
        cursor = self._conn.cursor()
        try:
            cursor.execute("""
                insert into project_quote_source values
                (?, ?, ?, ?)""", (id_proj, id_source, ini, fim))
            self._conn.commit()
            return True
        except IntegrityError:
            return False
    def quotes(self):
        cursor = self._conn.cursor()

        cursor.execute("""
            select nome, title from project
            join project_quote_source on project.id_proj = project_quote_source.id_proj
            join source on source.id_source = project_quote_source.id_source;""")
        return cursor.fetchall()
    def get_quote(self, id_proj, id_source):
        cursor = self._conn.cursor()

        cursor.execute("""
            select nome, title, pg_start, pg_end from project_quote_source
            join source on source.id_source = project_quote_source.id_source
            join project on project.id_proj = project_quote_source.id_proj
            where project.id_proj = :id_proj and source.id_source = :id_source;
            """, {'id_proj': id_proj, 'id_source': id_source})
        return cursor.fetchone()

    def edit_quote(self, id_proj, id_source, pg_start, pg_end):
        cursor = self._conn.cursor()

        cursor.execute(f"""
            update project_quote_source
            set pg_start = ?, pg_end = ?
            where id_proj = ? and id_source =?
            """, (pg_start, pg_end, id_proj, id_source))
        
        self._conn.commit()

    def alter_quote(self, id_proj, id_source, pg_start, pg_end):
        cursor = self._conn.cursor()

        cursor.execute("""
            select nome, title, pg_start, pg_end from project_quote_source
            join source on source.id_source = project_quote_source.id_source
            join project on project.id_proj = project_quote_source.id_proj
            where project.id_proj = :id_proj and source.id_source = :id_source;
            """, {'id_proj': id_proj, 'id_source': id_source})
        return cursor.fetchone()
    def project_quotes(self, id):
        cursor = self._conn.cursor()

        cursor.execute("""
            select source.id_source, title, subtitle, 'site', pg_start, pg_end from project_quote_source
            join source on source.id_source = project_quote_source.id_source
            join site on source.id_source = site.id_source
            where id_proj = :id
            union

            select source.id_source, title, subtitle, 'book', pg_start, pg_end from project_quote_source
            join source on source.id_source = project_quote_source.id_source
            join book on source.id_source = book.id_source
            where id_proj = :id

            union

            select source.id_source, title, subtitle, 'article', pg_start, pg_end from project_quote_source
            join source on source.id_source = project_quote_source.id_source
            join article on source.id_source = article.id_source
            where id_proj = :id;""", {'id':id})
        return cursor.fetchall()

    def get(self, id):
        cursor = self._conn.cursor()
        cursor.execute("""
            SELECT * FROM project
            WHERE id_proj = ?;""", (id, ))
        r = cursor.fetchone()
        if r:
            return Project(*r)
        return None
