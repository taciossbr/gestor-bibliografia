import sys
import gi
gi.require_version('Gtk', '3.0')
sys.path.insert(0, "api/")
from gi.repository import Gtk

from api import make_connection
from api.dao import PersonDAO

class ListagemPessoasWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Listagem Pessoas")
        self.set_border_width(10)
        layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        self.add(layout)
        self.dao = PersonDAO(make_connection())

        pls = Gtk.ListStore(int, str, str, str, str)

        for p in self.dao.todas_pessoas():
            pls.append([p.id, p.firstname, p.middlename, p.lastname, p.suffix])

        ptv = Gtk.TreeView(pls)

        for i, col_tittle in enumerate([
            'ID',
            'Primeiro Nome',
            'Nome do Meio',
            'Ultimo Nome',
            'Suffixo']):
            render = Gtk.CellRendererText()
            col = Gtk.TreeViewColumn(col_tittle, render, text=i)
            ptv.append_column(col)
            col.set_sort_column_id(i)

        sclwin = Gtk.ScrolledWindow()
        sclwin.add(ptv)
        sclwin.set_min_content_height(200)
        sclwin.set_min_content_width(450)
        layout.add(sclwin)


        print(self.dao.todas_pessoas())



