import sys
import gi
gi.require_version('Gtk', '3.0')
sys.path.insert(0, "api/")
from gi.repository import Gtk
from api import make_connection
from api.dao import SourceDAO, BookDAO, ArticleDAO, SiteDAO

class ListagemSourceWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title='Listagem de Fontes Bibliográficas')
        self.set_border_width(10)
        self.set_default_size(400, 200)
        
        self.notebook = Gtk.Notebook()
        self.add(self.notebook)

        self.book_page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.bdao = BookDAO(make_connection())
        self.books = self.bdao.todos_books()
        pls_book = Gtk.ListStore(int, str, str, str, str, str, str, str, int, int)
        for book in self.books:
            t = (book.id, book.date, book.title, book.subtitle, book.local, book.isbn,
                 book.publisher, book.series, book.edition, book.vol)
            # print(t)
            pls_book.append(list(t))
        ptv_book = Gtk.TreeView(pls_book)

        for i, col_title in enumerate(["ID", "Data", "Título", "Subtítulo", "Local",
                                       "ISBN", "Editora", "Serie", "Edição", "Volume"]):
            render = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(col_title, render, text=i)
            ptv_book.append_column(column)
            column.set_sort_column_id(i)    # make columns sortable

        self.book_page.add(ptv_book)
        self.notebook.append_page(self.book_page, Gtk.Label('Livros'))

        self.site_page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.sdao = SiteDAO(make_connection())
        self.sites = self.sdao.todos_sites()
        pls_site = Gtk.ListStore(int, str, str, str, str, str, str)
        for site in self.sites:
            t = (site.id, site.date, site.title, site.subtitle, site.local, site.link, site.dt_access)
            pls_site.append(list(t))
        ptv_site = Gtk.TreeView(pls_site)
        for i, col_title in enumerate(["ID", "Data", "Título", "Subtítulo", "Local",
                                       "Link", "Acesso"]):
            render = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(col_title, render, text=i)
            ptv_site.append_column(column)
            column.set_sort_column_id(i)

        self.site_page.add(ptv_site)
        self.notebook.append_page(self.site_page, Gtk.Label('Site'))

        self.article_page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.adao = ArticleDAO(make_connection())
        self.articles = self.adao.todos_articles()
        pls_articles = Gtk.ListStore(int, str, str, str, str, int, str, int, str)
        for a in self.articles:
            t = (a.id, a.date, a.title, a.subtitle, a.local,
                 a.doi, a.journal, a.vol_journal, a.fascicle)
            pls_articles.append(list(t))
        ptv_articles = Gtk.TreeView(pls_articles)
        
        for i, col_title in enumerate(["ID", "Data", "Título", "Subtítulo", "Local",
                                       "DOI", "Revista", "Vol", "Fascículo"]):
            render = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(col_title, render, text=i)
            ptv_articles.append_column(column)
            column.set_sort_column_id(i)

        self.article_page.add(ptv_articles)
        self.notebook.append_page(self.article_page, Gtk.Label('Artigos'))