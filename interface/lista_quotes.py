import sys
import gi
gi.require_version('Gtk', '3.0')
sys.path.insert(0, "api/")
from gi.repository import Gtk

from api import make_connection
from api.dao import ProjectDAO

class ListagemQuotesWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Listagem Pessoas")
        self.set_border_width(10)
        layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        self.add(layout)
        self.dao = ProjectDAO(make_connection())

        pls = Gtk.ListStore(str, str)

        for row in self.dao.quotes():
            pls.append(row)

        ptv = Gtk.TreeView(pls)

        for i, col_tittle in enumerate([
            'Projeto',
            'Obra']):
            render = Gtk.CellRendererText()
            col = Gtk.TreeViewColumn(col_tittle, render, text=i)
            ptv.append_column(col)
            col.set_sort_column_id(i)
        
        layout.add(ptv)





