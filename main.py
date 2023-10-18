from tkinter import *
from filesManager import *
import os
import shutil


class Main:
    def __init__(self) -> None:
        self.file_manager = FilesManager()
        self.createWindow()

    # se crea la ventana del administrador de archivos

    def createWindow(self):
        # ventana
        window = Tk()
        window.geometry("800x600")
        window.resizable(0, 0)
        window.title("Files Manager")
        self.window = window
        self.current_nodes = []
        # barra de navegacion
        navBar = LabelFrame(window, height=1, bg="#e4e4e4")
        navBar.pack(fill="x")
        navBar.columnconfigure(1, weight=1)
        navBar.columnconfigure(7, weight=5)
        navBar.columnconfigure(8, weight=1)
        self.navBar = navBar
        # boton atras
        back_photo = PhotoImage(file="img/back_button.png")
        back_photo = back_photo.subsample(20, 20)
        back_button = Button(navBar, image=back_photo,
                             relief="raised", bg="#e4e4e4")
        back_button.grid(row=0, column=0, padx=5, pady=5)
        self.back_button = back_button
        # boton copiar
        copy_photo = PhotoImage(file="img/copy-icon.png")
        copy_photo = copy_photo.subsample(20, 20)
        copy_button = Button(navBar, image=copy_photo,
                             relief="raised", bg="#e4e4e4")
        copy_button.grid(row=0, column=2, padx=5, pady=5)
        self.copy_button = copy_button
        # boton pegar
        paste_photo = PhotoImage(file="img/paste-icon.png")
        paste_photo = paste_photo.subsample(20, 20)
        paste_button = Button(navBar, image=paste_photo,
                              relief="raised", bg="#e4e4e4")
        paste_button.grid(row=0, column=3, padx=5, pady=5)
        self.paste_button = paste_button
        # boton eliminar
        delete_photo = PhotoImage(file="img/delete-icon.png")
        delete_photo = delete_photo.subsample(20, 20)
        delete_button = Button(navBar, image=delete_photo,
                               relief="raised", bg="#e4e4e4")
        delete_button.grid(row=0, column=4, padx=5, pady=5)
        self.delete_button = delete_button
        # campo busqueda
        search_variable = StringVar()
        self.search_variable = search_variable
        search_entry = Entry(
            navBar, textvariable=self.search_variable, width=30, font=("", 15))
        search_entry.grid(row=0, column=8, sticky=NSEW, pady=5, padx=5)
        self.search_entry = search_entry
        # campo contenidos
        content = Frame(window, height=500)
        content.pack(fill="both", expand=True)
        self.content = content

        # lista de contenidos
        self.update_list_content(content)

        # campo footer
        footer = LabelFrame(window, height=1, bg="#e4e4e4")
        footer.pack(fill="x")
        footer.columnconfigure(1, weight=6)
        footer.columnconfigure(8, weight=2)
        self.footer = footer
        # boton crear directorio
        create_dir_photo = PhotoImage(file="img/create-folder-icon.png")
        create_dir_photo = create_dir_photo.subsample(20, 20)
        create_dir_button = Button(
            footer, image=create_dir_photo, relief="raised", bg="#e4e4e4")
        create_dir_button.grid(row=0, column=2, padx=5, pady=5)
        self.create_dir_button = create_dir_button
        # boton crear archivo
        create_file_photo = PhotoImage(file="img/create-file-icon.jpg")
        create_file_photo = create_file_photo.subsample(20, 20)
        create_file_button = Button(
            footer, image=create_file_photo, relief="raised", bg="#e4e4e4")
        create_file_button.grid(row=0, column=3, padx=5, pady=5)
        self.create_file_button = create_file_button
        # boton renombrar
        rename_photo = PhotoImage(file="img/rename-icon.png")
        rename_photo = rename_photo.subsample(20, 20)
        rename_button = Button(footer, image=rename_photo,
                               relief="raised", bg="#e4e4e4")
        rename_button.grid(row=0, column=4, padx=5, pady=5)
        self.rename_button = rename_button
        # campo renombrar
        rename_entry = Entry(footer, font=("", 15))
        rename_entry.grid(row=0, column=8, sticky=NSEW, pady=5, padx=5)
        self.rename_entry = rename_entry
        self.set_listeners()
        self.window.mainloop()

    # añade listeners a diferentes elementos de la interfaz de usuario
    def set_listeners(self):
        self.search_variable.trace("w", self._filter)
        self.back_button.bind("<Button-1>", lambda event,
                              container=self.content: self.back(container))
        self.copy_button.bind("<Button-1>", self.copy)
        self.paste_button.bind("<Button-1>", self.paste)
        self.delete_button.bind("<Button-1>", self.delete)
        self.rename_button.bind("<Button-1>", self.rename)
        self.create_dir_button.bind("<Button-1>", self.create_dir)
        self.create_file_button.bind("<Button-1>", self.create_file)

    # crea un directorio de nombre "self.rename_entry.get()" que es el texto que se encuentre en el input, en el directorio actual
    def create_dir(self, event):
        os.makedirs(os.path.join(
            self.file_manager.record[-1].path, self.rename_entry.get()))
        self.file_manager.create_folder(
            self.file_manager.record[-1].path, self.rename_entry.get())
        self.update_list_content(self.content)

    # crea un archivo de nombre "self.rename_entry.get()" que es el texto que se encuentre en el input, en el directorio actual
    def create_file(self, event):
        open(os.path.join(
            self.file_manager.record[-1].path, self.rename_entry.get()), "w+")
        self.file_manager.create_file(
            self.file_manager.record[-1].path, self.rename_entry.get())
        self.update_list_content(self.content)

    # cambia el nombre del elemento seleccionado por "self.rename_entry.get()"
    def rename(self, event):
        new_name = self.rename_entry.get()
        new_path = self.selected_node.path.replace(
            self.selected_node.name, new_name)
        os.rename(self.selected_node.path, new_path)
        self.file_manager.rename(
            self.file_manager.record[-1].path, self.selected_node.name, new_name)
        self.update_list_content(self.content)

    # elimina el nodo seleccionado "self.selected_node" del directorio actual
    def delete(self, event):
        if self.selected_node.type == "dir":
            shutil.rmtree(self.selected_node.path)
        else:
            os.remove(self.selected_node.path)
        self.update_list_content(self.content)

    # almacena el nodo seleccionado como "self.file_manager.copied_node"
    def copy(self, event):
        self.file_manager.copy(
            self.file_manager.record[-1].path, self.selected_node.name)
        
    # pega el nodo almacenado "self.file_manager.copied_node" en el directorio actual
    def paste(self, event):
        if self.file_manager.copied_node.type == "dir":
            dst = os.path.join(
                self.file_manager.record[-1].path, self.file_manager.copied_node.name)
            shutil.copytree(src=self.file_manager.copied_node.path, dst=dst)
        else:
            shutil.copy(self.file_manager.copied_node.path,
                        self.file_manager.record[-1].path)
        self.file_manager.paste(self.file_manager.copied_node.path)
        self.update_list_content(self.content)

    # carga los elementos del anterior directorio visitado
    def back(self, container):
        if len(self.file_manager.record) > 1:
            del self.file_manager.record[-1]
            self.update_list_content(container)

    # actualiza la lista de elementos del ultimo directorio
    def update_list_content(self, container, nodes=None):
        self.selected_node = None
        for widget in container.winfo_children():
            widget.destroy()
        if nodes is None:
            nodes = self.file_manager.get_childs(
                self.file_manager.record[len(self.file_manager.record)-1])
        self.current_nodes = nodes
        count = 0
        self.folder_node_icon = PhotoImage(file="img/folder_icon.png")
        self.folder_node_icon = self.folder_node_icon.subsample(80, 80)
        self.file_node_icon = PhotoImage(file="img/file_icon.png")
        self.file_node_icon = self.file_node_icon.subsample(20, 20)
        for node in nodes:
            frame = Frame(container, height=1, bg="#e4e4e4")
            if node.type == "dir":
                icon = Label(frame, image=self.folder_node_icon, bg="#e4e4e4")
            else:
                icon = Label(frame, image=self.file_node_icon, bg="#e4e4e4")
            icon.grid(column=0, row=count)
            name = Label(frame, text=node.name, font=("", 18), bg="#e4e4e4")
            name.grid(column=1, row=count)
            frame.pack(fill="x", padx=5, pady=5)
            frame.bind("<Button-1>", lambda event, node=node,
                       frame=frame, container=container: self.select(node, frame, container))
            name.bind("<Button-1>", lambda event, node=node,
                      frame=frame, container=container: self.select(node, frame, container))
            icon.bind("<Button-1>", lambda event, node=node,
                      frame=frame, container=container: self.select(node, frame, container))
            name.bind("<Double-1>", lambda event, node=node,
                      container=container: self.open_folder(node, container))
            icon.bind("<Double-1>", lambda event, node=node,
                      container=container: self.open_folder(node, container))
            frame.bind("<Double-1>", lambda event, node=node,
                       container=container: self.open_folder(node, container))
            count += 1

    # carga los elementos del directorio doble clickeado
    def open_folder(self, node, container):
        if node.type == "dir":
            self.file_manager.record.append(node)
            self.update_list_content(self.content)


    # almacena el elemento seleccionado como "self.selected_node", cambia el color de fondo para mostrar que este esta seleccionado
    def select(self, node, frame, container):
        self.selected_node = node
        self.rename_entry.delete(0, END)
        self.rename_entry.insert(0, node.name)
        frame.config(bg="#bababa")
        for widget in frame.winfo_children():
            widget.config(bg="#bababa")
        self.unselect(frame, container)

    # cambia el color de fondo de los elementos anteriormente seleccionados para que no parezca que aun estan seleccionados
    def unselect(self, frame, container):
        for widget in container.winfo_children():
            if widget is not frame:
                widget.config(bg="#e4e4e4")
                self.unselect(frame, widget)

    # carga los elemetos que coincidan con el texto de la barra de busqueda
    def _filter(self, *args):
        if not self.search_variable.get():
            self.update_list_content(self.content)
        else:
            nodes = self.file_manager.search(
                self.file_manager.record[0], self.search_variable.get())
            self.update_list_content(self.content, nodes)


window = Main()
