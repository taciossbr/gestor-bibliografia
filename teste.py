from gi.repository import Gtk
from interface.gera_abnt import ABNTBibWindow as testWindow
# from interface.cadastra_source import CadastroSourceWindow

from api.models import Book
b = Book(id=1,
         date='2018-09-12',
         title='Python CookBook',
         local='São Paulo',
         isbn='00000',
         publisher='Novatec',
         edition=2,
         vol=1,
         subtitle='teste',
         series='t')
window = testWindow(b)
window.connect("delete-event", Gtk.main_quit)
window.show_all()

Gtk.main()