import sys
import gi
gi.require_version('Gtk', '3.0')
sys.path.insert(0, "api/")
from gi.repository import Gtk

from api import make_connection
from api.dao import ProjectDAO

from interface.cadastra_quote import CadastroQuoteWindow
from interface.cadastra_source import CadastroSourceWindow
from interface.lista_source import ListagemSourceWindow
from interface.cadastro_pessoa import CadastraPessoaWindow
from interface.lista_pessoa import ListagemPessoasWindow

class ListagemProjetosWindow(Gtk.Window):
    def __init__(self):
        Gtk.ScrolledWindow.__init__(self, title="Listagem Projetos")
        # self.set_border_width(2)


        main_menu_bar = Gtk.MenuBar()

        # Drop Down
        proj_new = Gtk.MenuItem("Novo Projeto")
        proj_new.connect('activate', self.new)
        main_menu_bar.append(proj_new)

        source_menu = Gtk.Menu()
        source_dropdow = Gtk.MenuItem("Fontes")

        source_new = Gtk.MenuItem("Novo")
        source_new.connect('activate', self.new_source)
        source_list = Gtk.MenuItem("Listagem")
        source_list.connect('activate', self.list_source)
        
        source_dropdow.set_submenu(source_menu)
        source_menu.append(source_new)
        source_menu.append(source_list)

        main_menu_bar.append(source_dropdow)

        autores_menu = Gtk.Menu()
        autores_dropdow = Gtk.MenuItem("Autores")

        autores_new = Gtk.MenuItem("Novo")
        autores_new.connect('activate', self.new_autor)
        autores_list = Gtk.MenuItem("Listagem")
        autores_list.connect('activate', self.list_autor)
        
        autores_dropdow.set_submenu(autores_menu)
        autores_menu.append(autores_new)
        autores_menu.append(autores_list)

        main_menu_bar.append(autores_dropdow)



        b1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        b1.add(main_menu_bar)


        
        self.layout = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.layout.set_spacing(6)

        scrolled = Gtk.ScrolledWindow(Gtk.Adjustment())
        scrolled.set_min_content_width(300)
        scrolled.set_min_content_height(250)
        self.layout.add(scrolled)
        self.dao = ProjectDAO(make_connection())

        pls = Gtk.ListStore(int, str)

        for p in self.dao.todos_projetos():
            pls.append([p.id, p.nome])

        self.ptv = Gtk.TreeView(pls)

        for i, col_tittle in enumerate([
            'ID',
            'Nome']):
            render = Gtk.CellRendererText()
            col = Gtk.TreeViewColumn(col_tittle, render, text=i)
            self.ptv.append_column(col)
            col.set_sort_column_id(i)
        # self.ptv.connect("row-activated", self.det_proj)
        self.ptv.get_selection().connect("changed", self.det_proj)
        scrolled.add(self.ptv)

        # panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        # panel.set_spacing(6)
        panel = Gtk.ScrolledWindow()
        panel.set_border_width(6)
        panel.set_min_content_width(150)
        # btn_det_proj = Gtk.Button("Detalhes")
        # btn_det_proj.connect("clicked", self.det_proj)
        
        # panel.add(btn_det_proj)

        self.lbl_nome = Gtk.Label()
        self.lbl_nome.set_visible(False)
        self.btn_quotes = Gtk.Button()
        self.btn_quotes.connect("clicked", self.show_quotes)
        self.btn_quotes.set_visible(False)
        # self.btn_new = Gtk.Button()
        # self.btn_new.connect("clicked", self.new)
        # self.btn_new.set_label("Novo Projeto")
        # self.btn_new.show()
        self.btn_quote = Gtk.Button()
        self.btn_quote.set_label("Cadastrar Citação")
        self.btn_quote.connect("clicked", self.new_quote)
        self.btn_quote.show()
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.set_spacing(6)
        box.add(self.lbl_nome)
        box.add(self.btn_quotes)
        # box.add(self.btn_new)
        box.add(self.btn_quote)
        panel.add(box)

        self.layout.add(panel)

        b1.add(self.layout)
        self.add(b1)

    def new_quote(self, widget):
        model, t = self.ptv.get_selection().get_selected()
        if t is not None:
            w = CadastroQuoteWindow(model[t][0])
            w.show_all()
            w.connect("destroy", lambda w: self.show_all())
            self.hide()
    def list_source(self, widget):
        w = ListagemSourceWindow()
        w.show_all()
        self.hide()
        w.connect('destroy', lambda w: self.show_all())

    def new_source(self, widget):
        w = CadastroSourceWindow()
        w.show_all()
        self.hide()
        w.connect('destroy', lambda w: self.show_all())
    
    def list_autor(self, widget):
        w = ListagemPessoasWindow()
        w.show_all()
        self.hide()
        w.connect('destroy', lambda w: self.show_all())

    def new_autor(self, widget):
        w = CadastraPessoaWindow()
        w.show_all()
        self.hide()
        w.connect('destroy', lambda w: self.show_all())

    def new(self, widget):
        w = CadastroProjectWindow()
        w.show_all()
        self.hide()
        w.connect('destroy', self.atualizar)
    
    def atualizar(self, widget):
        print('atualizar')
        pls = Gtk.ListStore(int, str)

        for p in self.dao.todos_projetos():
            pls.append([p.id, p.nome])
        self.ptv.set_model(pls)
        self.ptv.show_all()
        # self.ptv.re
        self.show()

    def show_quotes(self, widget):
        # print('clicked')
        model, t = self.ptv.get_selection().get_selected()
        if t is not None:
            project = self.dao.get(model[t][0])
            w = ListagemQuotesProjeto(project)
            w.show_all()
            w.connect("delete-event", lambda s, w: self.show_all())
            self.hide()

    def det_proj(self, widget):
        # print('clicked')
        model, t = self.ptv.get_selection().get_selected()
        if t is not None:
            project = self.dao.get(model[t][0])
            self.lbl_nome.set_markup(f'Nome - <b>{project.nome}</b>')
            self.lbl_nome.show()
            n = len(self.dao.project_quotes(project.id))
            self.btn_quotes.set_label(f'Ver {f"{n} " if n else ""}{"citacoes" if n else "citação"}')


class CadastroProjectWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title='Cadastro de Projetos')
        self.dao = ProjectDAO(make_connection())
        self.set_border_width(2)
        self.set_default_size(400, 200)
        self.layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.layout.set_spacing(10)
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        lbl_nome = Gtk.Label("Nome do Projeto")
        box.pack_start(lbl_nome, True, True, 0)
        self.ent_nome = Gtk.Entry()
        box.pack_start(self.ent_nome, True, True, 0)
        self.btn_save = Gtk.Button("Salvar")
        self.btn_save.connect("clicked", self.save)
        box.pack_start(self.btn_save, True, False, 0)

        self.layout.pack_start(box, False, False, 0)
        self.add(self.layout)
        self._dao = ProjectDAO(make_connection())

    def save(self, widget):
        p = self._dao.adiciona_projeto(self.ent_nome.get_text())
        msg = Gtk.MessageDialog(parent=self,
                                message_format=f"Projeto Cadastrado com sucesso\nID={p.id}",
                                type=Gtk.MessageType.INFO,
                                buttons=Gtk.ButtonsType.OK,
                                flags=Gtk.DialogFlags.DESTROY_WITH_PARENT)
        msg.show_all()
        msg.connect("response", lambda s, w: self.destroy())


class ListagemQuotesProjeto(Gtk.Window):
    def __init__(self, project):
        Gtk.Window.__init__(self, title=f"Listagem Citações do Projeto {project.nome}")
        self.set_border_width(10)
        layout = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        layout.set_spacing(6)
        self.project = project
        self.add(layout)
        self.dao = ProjectDAO(make_connection())

        pls = Gtk.ListStore(int, str, str, str, int, int)

        for row in self.dao.project_quotes(project.id):
            pls.append(row)

        self.ptv = Gtk.TreeView(pls)

        for i, col_tittle in enumerate([
            'id_source', 'Título', 'Subtítulo', 'Tipo', 'Página Fim', 'Página Fim' ]):
            render = Gtk.CellRendererText()
            col = Gtk.TreeViewColumn(col_tittle, render, text=i)
            if i == 0:
                col.set_visible(False)
            self.ptv.append_column(col)
            col.set_sort_column_id(i)

        
        res = Gtk.ScrolledWindow()
        res.set_min_content_height(300)
        res.set_min_content_width(400)
        self.ptv.get_selection().connect("changed", self.det_quote)
        res.add(self.ptv)
        layout.add(res)

        # panel = Gtk.ScrolledWindow()
        # panel.set_border_width(6)
        # panel.set_min_content_width(150)
        panel = Gtk.Grid()
        panel.set_row_spacing(3)
        panel.set_column_spacing(3)
        salvar = Gtk.Button("Salvar")
        salvar.connect("clicked", self.salvar)
        panel.attach(salvar, 0, 0, 2, 1)
        self.pg_start = Gtk.Entry()
        self.pg_start.set_size_request(50, 20)
        self.pg_start.set_editable(False)
        self.pg_start.set_width_chars(3)
        panel.attach(self.pg_start, 0, 1, 1, 1)
        self.pg_end = Gtk.Entry()
        self.pg_end.set_size_request(50, 20)
        self.pg_end.set_editable(False)
        self.pg_end.set_width_chars(3)
        self.pg_end.set_text('twer')
        panel.attach(self.pg_end, 1, 1, 1, 1)
        layout.add(panel)

    def salvar(self, widget):
        print(self.pg_start.get_text(), self.pg_end.get_text())
        model, t = self.ptv.get_selection().get_selected()
        if t is None:
            return
        try:
            self.dao.edit_quote(self.project.id,
                                model[t][0],
                                int(self.pg_start.get_text()),
                                int(self.pg_end.get_text()))
            msg = Gtk.MessageDialog(parent=self,
                                    message_format=f"Páginas Alteradas com Sucesso",
                                    type=Gtk.MessageType.INFO,
                                    buttons=Gtk.ButtonsType.OK,
                                    flags=Gtk.DialogFlags.DESTROY_WITH_PARENT)
            msg.show_all()
            msg.connect("response", lambda s, w: s.destroy())
        except ValueError:
            msg = Gtk.MessageDialog(parent=self,
                                    message_format=f"As Páginas devem ser valores inteiros",
                                    type=Gtk.MessageType.ERROR,
                                    buttons=Gtk.ButtonsType.OK,
                                    flags=Gtk.DialogFlags.DESTROY_WITH_PARENT)
            msg.show_all()
            msg.connect("response", lambda s, w: s.destroy())

    def det_quote(self, widget):
        model, t = self.ptv.get_selection().get_selected()
        if t is not None:
            quote = self.dao.get_quote(self.project.id, model[t][0])
            # print(quote)
            self.pg_start.set_text(str(quote[2]) if quote[2] else '')
            self.pg_end.set_text(str(quote[3]) if quote[3] else '')
            self.pg_start.set_editable(True)
            self.pg_end.set_editable(True)
            # self.lbl_nome.set_markup(f'Nome - <b>{project.nome}</b>')
            # self.lbl_nome.show()
            # n = len(self.dao.project_quotes(project.id))
            # self.btn_quotes.set_label(f'Ver {f"{n} " if n else ""}{"citacoes" if n else "citação"}')

