import sys
import gi
gi.require_version('Gtk', '3.0')
sys.path.insert(0, "api/")
from gi.repository import Gtk

from api import make_connection
from api.dao import ProjectDAO

class ListagemProjetosWindow(Gtk.Window):
    def __init__(self):
        Gtk.ScrolledWindow.__init__(self, title="Listagem Projetos")
        self.set_border_width(2)
        
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
        # panel.add(self.lbl_nome)
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.set_spacing(6)
        box.add(self.lbl_nome)
        box.add(self.btn_quotes)
        panel.add(box)

        self.layout.add(panel)


        self.add(self.layout)

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


class CadastroProjectDAO(Gtk.Window):
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

