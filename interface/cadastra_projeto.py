import sys
import gi
gi.require_version('Gtk', '3.0')
sys.path.insert(0, "api/")
from gi.repository import Gtk
from api import make_connection
from api.dao import ProjectDAO

class CadastroProjectDAO(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title='Cadastro de Projetos')
        self.set_border_width(10)
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
