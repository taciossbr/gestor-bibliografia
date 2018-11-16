import sys
import gi
gi.require_version('Gtk', '3.0')
sys.path.insert(0, "api/")
from gi.repository import Gtk
from api import make_connection
from api.dao import SourceDAO, BookDAO, ArticleDAO, SiteDAO

class CadastroSourceWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title='Cadastro de Fontes Bibliográficas')
        self.set_border_width(10)
        self.set_default_size(400, 200)
        self.layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.layout.set_spacing(10)

        grid = Gtk.Grid()
        grid.set_row_spacing(6)
        grid.set_column_spacing(6)

        grid.add(Gtk.Label("Date"))
        self.ent_date = Gtk.Entry()
        grid.attach(self.ent_date, 1, 0, 1, 1)
        grid.attach(Gtk.Label("Titulo"), 0, 1, 1, 1)
        self.ent_title = Gtk.Entry()
        grid.attach(self.ent_title, 1, 1, 1, 1)
        grid.attach(Gtk.Label("Subtítulo"), 0, 2, 1, 1)
        self.ent_subtitle = Gtk.Entry()
        grid.attach(self.ent_subtitle, 1, 2, 1, 1)
        grid.attach(Gtk.Label("Local"), 0, 3, 1, 1)
        self.ent_local = Gtk.Entry()
        grid.attach(self.ent_local, 1, 3, 1, 1)
        
        self.layout.add(grid)

        self.option = Gtk.Grid()
        self.option.set_row_spacing(5)
        self.option.set_column_spacing(10)

        self.lbl_option_book = Gtk.Label("Livro")
        self.lbl_option_book.set_justify(Gtk.Justification.LEFT)
        self.option.add(self.lbl_option_book)
        self.radio_book = Gtk.RadioButton()
        self.radio_book.connect("toggled", self.tog_op)
        self.option.attach(self.radio_book, 1, 0, 1, 1)

        self.lbl_option_site = Gtk.Label("Site")
        self.lbl_option_site.set_justify(Gtk.Justification.LEFT)
        self.option.attach(self.lbl_option_site, 0, 1, 1, 1)
        self.radio_site = Gtk.RadioButton.new_from_widget(self.radio_book)
        self.radio_site.connect("toggled", self.tog_op)
        self.option.attach(self.radio_site, 1, 1, 1, 1)
        
        self.lbl_option_art = Gtk.Label("Artigo")
        self.lbl_option_art.set_justify(Gtk.Justification.LEFT)
        self.option.attach(self.lbl_option_art, 0, 2, 1, 1)
        self.radio_art = Gtk.RadioButton.new_from_widget(self.radio_book)
        self.radio_art.connect("toggled", self.tog_op)
        self.option.attach(self.radio_art, 1, 2, 1, 1)
        
        self.layout.add(self.option)

        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.NONE)

        # book interface
        grid_book = Gtk.Grid()
        grid_book.set_row_spacing(6)
        grid_book.set_column_spacing(6)
        lbl_isbn = Gtk.Label("ISBN")
        grid_book.add(lbl_isbn)
        self.ent_isbn = Gtk.Entry()
        grid_book.attach(self.ent_isbn, 1, 0, 1, 1)
        lbl_pub = Gtk.Label("Editora")
        grid_book.attach(lbl_pub, 0, 1, 1, 1)
        self.ent_pub = Gtk.Entry()
        grid_book.attach(self.ent_pub, 1, 1, 1, 1)
        lbl_series = Gtk.Label("Serie")
        grid_book.attach(lbl_series, 0, 2, 1, 1)
        self.ent_series = Gtk.Entry()
        grid_book.attach(self.ent_series, 1, 2, 1, 1)
        lbl_edition  = Gtk.Label("Edição")
        grid_book.attach(lbl_edition, 0, 3, 1, 1)
        self.ent_edition = Gtk.Entry()
        grid_book.attach(self.ent_edition, 1, 3, 1, 1)
        grid_book.show_all()
        self.stack.add_titled(grid_book, 'book', "Book")

        # site interface
        grid_site = Gtk.Grid()
        grid_site.set_row_spacing(6)
        grid_site.set_column_spacing(6)
        lbl_link = Gtk.Label("Link")
        grid_site.add(lbl_link)
        self.ent_link = Gtk.Entry()
        self.ent_link.set_input_purpose(Gtk.InputPurpose.URL)
        grid_site.attach(self.ent_link, 1, 0, 1, 1)
        lbl_dt_access = Gtk.Label("Data")
        grid_site.attach(lbl_dt_access, 0, 1, 1, 1)
        self.ent_dt_access = Gtk.Entry()
        grid_site.attach(self.ent_dt_access, 1, 1, 1, 1)
        grid_site.show_all()
        self.stack.add_titled(grid_site, 'site', 'Site')

        # Artigo interface
        grid_article = Gtk.Grid()
        grid_article.set_row_spacing(6)
        grid_article.set_column_spacing(6)
        lbl_doi = Gtk.Label("DOI")
        grid_article.attach(lbl_doi, 0, 0, 1, 1)
        self.ent_doi = Gtk.Entry()
        grid_article.attach(self.ent_doi, 1, 0, 1, 1)
        lbl_journal = Gtk.Label("Revista")
        grid_article.attach(lbl_journal, 0, 1, 1, 1)
        self.ent_journal = Gtk.Entry()
        grid_article.attach(self.ent_journal, 1, 1, 1, 1)
        lbl_vol = Gtk.Label("Volume")
        grid_article.attach(lbl_vol, 0, 2, 1, 1)
        self.ent_vol = Gtk.Entry()
        grid_article.attach(self.ent_vol, 1, 2, 1, 1)
        lbl_fascicle = Gtk.Label("Fascículo")
        grid_article.attach(lbl_fascicle, 0, 3, 1, 1)
        self.ent_fascicle = Gtk.Entry()
        grid_article.attach(self.ent_fascicle, 1, 3, 1, 1)
        grid_article.show_all()
        self.stack.add_titled(grid_article, 'article', 'Article')

        self.stack.set_visible_child_name('book')

        self.layout.add(self.stack)

        self.btn_save = Gtk.Button()
        self.btn_save.set_label("Salvar")
        self.btn_save.connect("clicked", self.save)
        self.layout.add(self.btn_save)
        
        self.add(self.layout)

    def save(self, widget):
        def_ents = [x.get_text() for x in (
            self.ent_date,
            self.ent_title
        )]
        # print(def_ents)
        if None in def_ents or '' in def_ents:
            msg = Gtk.MessageDialog(text='Data e título são obrigatórios', 
                                    buttons=Gtk.ButtonsType.CLOSE, 
                                    type=Gtk.MessageType.ERROR,
                                    flags=Gtk.DialogFlags.DESTROY_WITH_PARENT)
            msg.connect("response", lambda s, w: msg.destroy())
            msg.show()
            return None
        
        if self.radio_book.get_active():
            ents = [x.get_text() for x in (
                self.ent_isbn,
                self.ent_pub,
                self.ent_edition
            )]
            # print(ents)
            if None in ents or '' in ents:
                msg = Gtk.MessageDialog(text='ISBN, Editora, e Edição são obrigatórios', 
                                        buttons=Gtk.ButtonsType.CLOSE, 
                                        type=Gtk.MessageType.ERROR,
                                        flags=Gtk.DialogFlags.DESTROY_WITH_PARENT)
                msg.connect("response", lambda s, w: msg.destroy())
                msg.show()
                # print('err')
                return None
            dao = BookDAO(make_connection())
            b = dao.adiciona_book(self.ent_date.get_text(), self.ent_title.get_text(),
                                  self.ent_subtitle.get_text(), self.ent_local.get_text(),
                                  self.ent_isbn.get_text(), self.ent_pub.get_text(),
                                  self.ent_series.get_text(), self.ent_edition.get_text(),
                                  self.ent_vol.get_text())
            msg = Gtk.MessageDialog(text=f'Livro Cadastrado com Sucesso\nID:{b.id}', 
                                    buttons=Gtk.ButtonsType.CLOSE, 
                                    type=Gtk.MessageType.INFO,
                                    flags=Gtk.DialogFlags.DESTROY_WITH_PARENT)
            msg.connect("response", lambda s, w: msg.destroy())
            msg.show()
        elif self.radio_art.get_active():
            ents = [x.get_text() for x in (
                self.ent_doi,
                self.ent_journal,
                self.ent_vol,
                self.ent_fascicle
            )]
            # print(ents)
            if None in ents or '' in ents:
                msg = Gtk.MessageDialog(text='DOI, Revista, Volume e Fascículo são obrigatórios', 
                                        buttons=Gtk.ButtonsType.CLOSE, 
                                        type=Gtk.MessageType.ERROR,
                                        flags=Gtk.DialogFlags.DESTROY_WITH_PARENT)
                msg.connect("response", lambda s, w: msg.destroy())
                msg.show()
                # print('err')
                return None
            dao = ArticleDAO(make_connection())
            b = dao.adiciona_article(self.ent_date.get_text(), self.ent_title.get_text(),
                                  self.ent_subtitle.get_text(), self.ent_local.get_text(),
                                  *ents)
            msg = Gtk.MessageDialog(text=f'Artigo Cadastrado com Sucesso\nID:{b.id}', 
                                    buttons=Gtk.ButtonsType.CLOSE, 
                                    type=Gtk.MessageType.INFO,
                                    flags=Gtk.DialogFlags.DESTROY_WITH_PARENT)
            msg.connect("response", lambda s, w: msg.destroy())
            msg.show()
        elif self.radio_site.get_active():
            ents = [x.get_text() for x in (
                self.ent_link,
                self.ent_dt_access
            )]
            # print(ents)
            if None in ents or '' in ents:
                msg = Gtk.MessageDialog(text='Link e Data de Acesso são obrigatórios', 
                                        buttons=Gtk.ButtonsType.CLOSE, 
                                        type=Gtk.MessageType.ERROR,
                                        flags=Gtk.DialogFlags.DESTROY_WITH_PARENT)
                msg.connect("response", lambda s, w: msg.destroy())
                msg.show()
                # print('err')
                return None
            dao = SiteDAO(make_connection())
            b = dao.adiciona_site(self.ent_date.get_text(), self.ent_title.get_text(),
                                  self.ent_subtitle.get_text(), self.ent_local.get_text(),
                                  *ents)
            msg = Gtk.MessageDialog(text=f'Site Cadastrado com Sucesso\nID:{b.id}', 
                                    buttons=Gtk.ButtonsType.CLOSE, 
                                    type=Gtk.MessageType.INFO,
                                    flags=Gtk.DialogFlags.DESTROY_WITH_PARENT)
            msg.connect("response", lambda s, w: msg.destroy())
            msg.show()

        

    def tog_op(self, widget):
        d = {
            self.radio_art: 'article',
            self.radio_book: 'book',
            self.radio_site: 'site',
        }
        self.stack.set_visible_child_name(d[widget])
