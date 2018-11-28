import sys
import gi
gi.require_version('Gtk', '3.0')
sys.path.insert(0, "api/")
from gi.repository import Gtk
from api import make_connection
from api.dao import SourceDAO, BookDAO, ArticleDAO, SiteDAO
from interface.gera_abnt import ABNTBibWindow

class ListagemSourceWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title='Listagem de Fontes Bibliográficas')
        self.set_border_width(10)
        self.set_default_size(400, 200)
        
        self.notebook = Gtk.Notebook()
        layout = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        layout.add(self.notebook)
        panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        layout.add(panel)
        layout.set_spacing(4)
        self.add(layout)

        # self.book_page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.book_page = Gtk.ScrolledWindow()
        self.book_page.set_min_content_height(300)
        self.book_page.set_min_content_width(600)
        self.bdao = BookDAO(make_connection())
        self.books = self.bdao.todos_books()
        self.pls_book = Gtk.ListStore(int, str, str, str, str, str, str, str, int, int)
        for book in self.books:
            t = (book.id, book.date, book.title, book.subtitle, book.local, book.isbn,
                 book.publisher, book.series, book.edition, book.vol)
            # print(t)
            self.pls_book.append(list(t))
        self.ptv_book = Gtk.TreeView(self.pls_book)

        for i, col_title in enumerate(["ID", "Data", "Título", "Subtítulo", "Local",
                                       "ISBN", "Editora", "Serie", "Edição", "Volume"]):
            render = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(col_title, render, text=i)
            self.ptv_book.append_column(column)
            column.set_sort_column_id(i)    # make columns sortable

        self.book_page.add(self.ptv_book)
        self.notebook.append_page(self.book_page, Gtk.Label('Livros'))

        # self.site_page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.site_page = Gtk.ScrolledWindow()
        self.site_page.set_min_content_height(300)
        self.site_page.set_min_content_width(600)
        self.sdao = SiteDAO(make_connection())
        self.sites = self.sdao.todos_sites()
        self.pls_site = Gtk.ListStore(int, str, str, str, str, str, str)
        for site in self.sites:
            t = (site.id, site.date, site.title, site.subtitle, site.local, site.link, site.dt_access)
            self.pls_site.append(list(t))
        self.ptv_site = Gtk.TreeView(self.pls_site)
        for i, col_title in enumerate(["ID", "Data", "Título", "Subtítulo", "Local",
                                       "Link", "Acesso"]):
            render = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(col_title, render, text=i)
            self.ptv_site.append_column(column)
            column.set_sort_column_id(i)

        self.site_page.add(self.ptv_site)
        self.notebook.append_page(self.site_page, Gtk.Label('Site'))

        # self.article_page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.article_page = Gtk.ScrolledWindow()
        self.article_page.set_min_content_height(300)
        self.article_page.set_min_content_width(600)
        self.adao = ArticleDAO(make_connection())
        self.articles = self.adao.todos_articles()
        self.pls_articles = Gtk.ListStore(int, str, str, str, str, int, str, int, str)
        for a in self.articles:
            t = (a.id, a.date, a.title, a.subtitle, a.local,
                 a.doi, a.journal, a.vol_journal, a.fascicle)
            self.pls_articles.append(list(t))
        self.ptv_articles = Gtk.TreeView(self.pls_articles)
        
        for i, col_title in enumerate(["ID", "Data", "Título", "Subtítulo", "Local",
                                       "DOI", "Revista", "Vol", "Fascículo"]):
            render = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(col_title, render, text=i)
            self.ptv_articles.append_column(column)
            column.set_sort_column_id(i)

        self.article_page.add(self.ptv_articles)
        self.notebook.append_page(self.article_page, Gtk.Label('Artigos'))


        btn_abnt = Gtk.Button()
        btn_abnt.set_label('Gerar Referências ABNT')
        btn_abnt.connect('clicked', self.abnt)
        panel.add(btn_abnt)
        panel.set_spacing(4)

    def abnt(self, widget):
        ptvs = [
            self.ptv_book,
            self.ptv_site,
            self.ptv_articles
        ]
        daos = [
            self.bdao,
            self.sdao,
            self.adao
        ]
        p_index = self.notebook.get_current_page()
        ptv = ptvs[p_index]
        dao = daos[p_index]
        model, t = ptv.get_selection().get_selected()
        if t is not None:
            print(int(model[t][0]))
            # return
            sources = dao.get(int(model[t][0]))
            # print(sources)
            w = ABNTBibWindow(sources)
            # w = CadastroQuoteWindow(model[t][0])
            w.show_all()
            w.connect("destroy", lambda w: self.show_all())
            self.hide()