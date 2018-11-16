import sys
import gi
gi.require_version('Gtk', '3.0')
sys.path.insert(0, "api/")
from gi.repository import Gtk
from api import make_connection
from api.dao import ProjectDAO, BookDAO, ArticleDAO, SiteDAO

class CadastroQuoteWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title='Cadastro de Projetos')
        self.set_border_width(10)
        self.set_default_size(400, 200)
        self.layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.layout.set_spacing(10)
        
        proj_list_store = Gtk.ListStore(int, str)
        self.pdao = ProjectDAO(make_connection())
        for projeto in self.pdao.todos_projetos():
            proj_list_store.append([projeto.id, projeto.nome])
        self.projeto_combo = Gtk.ComboBox.new_with_model_and_entry(proj_list_store)
        self.projeto_combo.set_entry_text_column(1)
        self.layout.add(self.projeto_combo)

        type_source_ls = Gtk.ListStore(int, str)
        type_source_ls.append([0, 'book'])
        type_source_ls.append([1, 'article'])
        type_source_ls.append([2, 'site'])
        self.type_source_combo = Gtk.ComboBox.new_with_model_and_entry(type_source_ls)
        self.type_source_combo.set_entry_text_column(1)
        self.type_source_combo.connect("changed", self.select_type_source)
        self.layout.add(self.type_source_combo)

        self.source_combo = Gtk.ComboBox()
        self.source_combo.set_sensitive(False)
        self.source_combo.set_entry_text_column(1)
        self.source_box = Gtk.Box()
        self.source_box.add(self.source_combo)
        self.layout.add(self.source_box)

        self.ent_ini = Gtk.Entry()
        self.ent_ini.set_placeholder_text("página inicio")
        self.ent_fim = Gtk.Entry()
        self.ent_fim.set_placeholder_text("página fim")
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        box.set_spacing(5)
        box.pack_start(self.ent_ini, True, True, 0)
        box.pack_start(self.ent_fim, True, True, 0)
        self.layout.add(box)

        self.btn_save = Gtk.Button("Salvar")
        self.btn_save.connect("clicked", self.save)
        self.layout.add(self.btn_save)

        self.add(self.layout)

    def select_type_source(self, widget):
        d = [
            (BookDAO, BookDAO.todos_books),
            (ArticleDAO, ArticleDAO.todos_articles),
            (SiteDAO, SiteDAO.todos_sites)]
        source_iter = widget.get_active_iter()
        if source_iter is not None:
            model = widget.get_model()
            i, _ = model[source_iter]
            dao, func = d[i]
    
        sources = dao(make_connection())
        ls = Gtk.ListStore(int, str)
        for s in func(sources):
            ls.append([s.id, s.title])
        self.source_box.remove(self.source_combo)
        del self.source_combo
        self.source_combo = Gtk.ComboBox.new_with_model_and_entry(ls)
        self.source_combo.set_entry_text_column(1)
        self.source_combo.show()
        self.source_box.add(self.source_combo)

    def save(self, widget):
        source_iter = self.source_combo.get_active_iter()
        if source_iter is None:
            print('error')
        model = self.source_combo.get_model()
        id_source, _ = model[source_iter]
        project_iter = self.projeto_combo.get_active_iter()
        if project_iter is None:
            print('error p')
        model = self.projeto_combo.get_model()
        id_proj, _ = model[project_iter]

        try:
            inicio = int(self.ent_ini)
            fim = int(self.ent_fim)
        except:
            inicio = None
            fim = None

        if self.pdao.quote(id_proj, id_source, inicio, fim):
            msg = Gtk.MessageDialog(text='Citado com sucesso', 
                                    parent=self,
                                    buttons=Gtk.ButtonsType.CLOSE, 
                                    type=Gtk.MessageType.INFO,
                                    flags=Gtk.DialogFlags.DESTROY_WITH_PARENT)
            msg.connect("response", lambda s, w: self.destroy())
            msg.show()
        else:
            msg = Gtk.MessageDialog(text='Citação já realizada', 
                                    parent=self,
                                    buttons=Gtk.ButtonsType.CLOSE, 
                                    type=Gtk.MessageType.ERROR,
                                    flags=Gtk.DialogFlags.DESTROY_WITH_PARENT)
            msg.connect("response", lambda s, w: msg.destroy())
            msg.show()
