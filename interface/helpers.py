from gi.repository import Gtk


        main_menu_bar = Gtk.MenuBar()

        # Drop Down
        file_menu = Gtk.Menu()
        file_drop = Gtk.MenuItem("File")

        file_new = Gtk.MenuItem("New")
        file_open = Gtk.MenuItem("Open")
        file_exit = Gtk.MenuItem("Exit")

        file_drop.set_submenu(file_menu)
        file_menu.append(file_new)
        file_menu.append(file_open)
        file_menu.append(Gtk.SeparatorMenuItem())
        file_menu.append(file_exit)

        main_menu_bar.append(file_drop)
