import sys
import gi
gi.require_version('Gtk', '3.0')
sys.path.insert(0, "api/")
from gi.repository import Gtk, WebKit2
import re
from api import make_connection
from api.dao import BookDAO, ArticleDAO
from api.models import Book, Site, Article

# class ABNTBibWindow:
class ABNTBibWindow(Gtk.Window):
    def __init__(self, sources):
        Gtk.Window.__init__(self, title="Referencias")
        self.set_border_width(10)
        layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        if not isinstance(sources, list):
            sources = [sources]

        s = ''
        for source in sources:
            print('source', source, 'type:', type(source))
            if isinstance(source, Book):
                dao = BookDAO(make_connection())
                autores = dao.autores(source.id)
                year = re.match(r'\d{4}', source.date).group(0)

                if len(autores) == 0:
                    s += f"""{source.title.upper()}{f': {source.subtitle}' if source.subtitle else ''}. 
                        {f'{source.edition}. ed.' if source.edition else str()} 
                        {source.local.capitalize()}: {source.publisher.capitalize()}, {year}"""
                elif len(autores) <= 3:
                    s += f"""{'; '.join([f'{a.lastname.upper()}, {a.firstname.capitalize()}' for a in sorted(autores, key=lambda e: e.lastname)])}. 
                        <b>{source.title}</b>{f': {source.subtitle}' if source.subtitle else ''}. 
                        {f'{source.edition}. ed.' if source.edition else str()} 
                        {source.local.capitalize()}: {source.publisher.capitalize()}, {year}"""
                else:
                    a = sorted(autores, key=lambda e: e.lastname)[0]
                    s += f"""{a.lastname.upper()}, {a.firstname.capitalize()}. et al
                        <b>{source.title}</b>{f': {source.subtitle}' if source.subtitle else ''}. 
                        {f'{source.edition}. ed.' if source.edition else str()} 
                        {source.local.capitalize()}: {source.publisher.capitalize()}, {year}"""
            if isinstance(source, Article):
                dao = ArticleDAO(make_connection())
                autores = dao.autores(source.id)
                # year = re.match(r'\d{4}', source.date).group(0)

                if len(autores) == 0:
                    s += f"""{source.title.upper()}. {source.title}. {source.journal}. {source.local}. {source.vol_journal}. {source.fascicle}. mes. ano"""
                elif len(autores) <= 3:
                    s += f"""{'; '.join([f'{a.lastname.upper()}, {a.firstname.capitalize()}' for a in sorted(autores, key=lambda e: e.lastname)])}. 
                        {source.title}. {source.journal}. {source.local}. {source.vol_journal}. {source.fascicle}. mes. ano"""
                else:
                    a = sorted(autores, key=lambda e: e.lastname)[0]
                    s += f"""{a.lastname.upper()}, {a.firstname.capitalize()}. et al
                        {source.title}. {source.journal}. {source.local}. {source.vol_journal}. {source.fascicle}. mes. ano"""
            if isinstance(source, Site):
                dao = ArticleDAO(make_connection())
                autores = dao.autores(source.id)
                year = re.match(r'\d{4}', source.date).group(0)

                if len(autores) == 0:
                    s += f"""{source.title.upper()}. {source.title}.
                    {year}. {source.link}. {source.dt_access}"""
                elif len(autores) <= 3:
                    s += f"""{'; '.join([f'{a.lastname.upper()}, {a.firstname.capitalize()}' for a in sorted(autores, key=lambda e: e.lastname)])}. 
                        {source.title.upper()}. {source.title}.
                    {year}. {source.link}. {source.dt_access}"""
                else:
                    a = sorted(autores, key=lambda e: e.lastname)[0]
                    s += f"""{a.lastname.upper()}, {a.firstname.capitalize()}. et al
                        {source.title.upper()}. {source.title}. 
                    {year}. {source.link}. {source.dt_access}"""
            s+='<br>'
        view = WebKit2.WebView()
        print('html:', s)
        view.load_html(s)
        view.show()
        scl = Gtk.ScrolledWindow()
        scl.set_min_content_height(350)
        scl.set_min_content_width(600)
        scl.add(view)
        self.add(scl)
        # self.add(layout)
        





