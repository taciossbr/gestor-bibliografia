from gi.repository import Gtk
from interface.projetos import ListagemProjetosWindow as testWindow
# from interface.cadastra_source import CadastroSourceWindow

window = testWindow()
window.connect("delete-event", Gtk.main_quit)
window.show_all()

Gtk.main()