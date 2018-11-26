import sys
import gi
gi.require_version('Gtk', '3.0')
sys.path.insert(0, "api/")
from gi.repository import Gtk
from api import make_connection
from api.dao import PersonDAO

class CadastraPessoaWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Cadastro de Pessoas")
        self.set_default_size(400, 200)
        self.set_border_width(20)
        self.layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.layout.set_spacing(20)

        self.box_pn_pessoa = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.box_pn_pessoa.set_spacing(10)
        label_pn_pessoa = Gtk.Label("Primeiro nome")
        label_pn_pessoa.set_justify(Gtk.Justification.LEFT)
        self.input_pn_pessoa = Gtk.Entry()
        self.box_pn_pessoa.pack_start(label_pn_pessoa, False, True, 0)
        self.box_pn_pessoa.pack_start(self.input_pn_pessoa, True, True, 0)
        self.layout.add(self.box_pn_pessoa)

        self.box_nm_pessoa = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.box_nm_pessoa.set_spacing(10)
        label_nm_pessoa = Gtk.Label("Nome do Meio")
        label_nm_pessoa.set_justify(Gtk.Justification.LEFT)
        self.input_nm_pessoa = Gtk.Entry()
        self.box_nm_pessoa.pack_start(label_nm_pessoa, False, True, 0)
        self.box_nm_pessoa.pack_start(self.input_nm_pessoa, True, True, 0)
        self.layout.add(self.box_nm_pessoa)

        self.box_un_pessoa = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.box_un_pessoa.set_spacing(10)
        label_un_pessoa = Gtk.Label("Ultimo Nome")
        label_un_pessoa.set_justify(Gtk.Justification.LEFT)
        self.input_un_pessoa = Gtk.Entry()
        self.box_un_pessoa.pack_start(label_un_pessoa, False, True, 0)
        self.box_un_pessoa.pack_start(self.input_un_pessoa, True, True, 0)
        self.layout.add(self.box_un_pessoa)

        self.box_sf_pessoa = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.box_sf_pessoa.set_spacing(10)
        label_sf_pessoa = Gtk.Label("Sufixo")
        label_sf_pessoa.set_justify(Gtk.Justification.LEFT)
        self.input_sf_pessoa = Gtk.Entry()
        self.box_sf_pessoa.pack_start(label_sf_pessoa, False, True, 0)
        self.box_sf_pessoa.pack_start(self.input_sf_pessoa, True, True, 0)
        self.layout.add(self.box_sf_pessoa)

        self.grava_btn = Gtk.Button("Concluido")
        self.grava_btn.connect("clicked", self.grava_pessoa)
        self.layout.add(self.grava_btn)

        self.personDAO = PersonDAO(make_connection())

        self.add(self.layout)
    
    def grava_pessoa(self, widget):
        pn = self.input_pn_pessoa.get_text()
        nm = self.input_nm_pessoa.get_text()
        un = self.input_un_pessoa.get_text()
        sf = self.input_sf_pessoa.get_text()

        self.personDAO.adiciona_pessoa(pn, nm, un, sf)


