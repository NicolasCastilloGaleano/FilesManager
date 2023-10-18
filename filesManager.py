import os
import shutil


class TreeNode:
    def __init__(self, path, type, name) -> None:
        self.path = path
        self.type = type
        self.name = name
        self.children = []


class Tree:
    def __init__(self, root_path) -> None:
        self.root = TreeNode(root_path, "dir", "root")
        self.create_tree(self.root)

    # se crea recursivamente el arbol n-ario
    def create_tree(self, node=TreeNode):
        node.children = self.get_dir_nodes(node.path)
        for child in node.children:
            if child.type == "dir":
                self.create_tree(child)

    # se retornan los nodos hijos para un nodo con direccion "path"
    def get_dir_nodes(self, path):
        children = []
        children_names = os.listdir(path)
        for child in children_names:
            if os.path.isdir(os.path.join(path, child)):
                children.append(
                    TreeNode(os.path.join(path, child), "dir", child))
            else:
                children.append(
                    TreeNode(os.path.join(path, child), "file", child))
        return children

    # se remueve del nodo con direccion "father_path" el nodo con nombre "name"
    def remove(self, father_path, name):
        father = self.search_node(self.root, father_path)
        for child in father.children:
            if child.name == name:
                father.children.remove(child)

    # se busca el nodo con nombre "name" en el directorio "father_path" y se retorna el mismo
    def copy(self, father_path, name):
        father = self.search_node(self.root, father_path)
        for child in father.children:
            if child.name == name:
                return child

    # añade un nodo "name" a los hijos del directorio actual "father_path" de tipo "type"
    def create_node(self, father_path, name, type):
        father = self.search_node(self.root, father_path)
        father.children.append(
            TreeNode(os.path.join(father_path, name), type, name))

    # dentro del directorio "father_path" se cambia el nombre del nodo "current_name" por " new_name"
    # sa cambian las direcciones del nodo y sus hijos si los tiene
    def rename(self, father_path, current_name, new_name):
        father = self.search_node(self.root, father_path)
        for child in father.children:
            if child.name == current_name:
                new_node = TreeNode(os.path.join(
                    father_path, new_name), child.type, new_name)
                self.child_tree(child, new_node)
                father.children.remove(child)
                father.children.append(new_node)
                return

    # se añade el nodo "node" a los hijos del nodo con direccion "father_path"

    def paste(self, father_path, node):
        father = self.search_node(self.root, father_path)
        new_node = TreeNode(os.path.join(
            father_path, node.name), node.type, node.name)
        self.child_tree(node, new_node)
        father.children.append(new_node)

    # se crea un arbol nuevo a partir del nodo copiado pero se cambian las direcciones para que concuerden con  la direccion del directorio donde se copiara el nodo
    # father_path es la direccion de la carpeta donde se copiara el nodo
    # node es el nodo a partir del cual se creara el nuevo arbol al cual se le cambiara las direcciones
    def child_tree(self, node, temp_node):
        if node.children:
            for child in node.children:
                temp_node.children.append(TreeNode(os.path.join(
                    temp_node.path, child.name), child.type, child.name))
                self.child_tree(child, temp_node)

    # se busca recursivamente el nodo con direccion "path" a partir de un nodo "node" y lo retorna si este existe
    def search_node(self, node, path):
        if node.path == path:
            return node
        elif node.children:
            for child in node.children:
                if self.search_node(child, path) is not None:
                    return self.search_node(child, path)
        else:
            return None


class FilesManager:
    def __init__(self) -> None:
        self.tree = Tree("./root")
        self._root_path = "./root"
        self.record = [self.tree.root]

    def print_tree(self, root=TreeNode):
        print(root.path, root.name, root.type)
        if root.children:
            for child in root.children:
                self.print_tree(child)

    # eliminar el nodo "name" del directorio actual "current_path"
    def delete(self, current_path, name):
        self.tree.remove(current_path, name)

    # alamacena el nodo seleccionado "name" como "copied_node" para ser pegado en otro directorio
    def copy(self, current_path, name):
        self.copied_node = self.tree.copy(current_path, name)

    # pega el nodo almacenado como "copied_node" en el directorio actual "current path"
    def paste(self, current_path):
        self.tree.paste(current_path, self.copied_node)

    # alamacena el nodo seleccionado "name" como "copied_node" y corta el mismo del directorio actual "current_path"
    def cut(self, current_path, name):
        self.copied_node = self.tree.copy(current_path, name)
        self.tree.remove(current_path, name)

    # crea un nodo "name" en el directorio actual "current_path" de tipo archivo "file"
    def create_file(self, current_path, name):
        self.tree.create_node(current_path, name, "file")

    # crea un nodo "name" en el directorio actual "current_path" de tipo directorio "dir"
    def create_folder(self, current_path, name):
        self.tree.create_node(current_path, name, "dir")

    # en el directorio "current_paht" se cambia el nombre del nodo "name" por "new_name"
    def rename(self, current_path, name, new_name):
        self.tree.rename(current_path, name, new_name)

    # se obtiene la lista de nodos hijos del nodo "node"
    def get_childs(self, node):
        return self.tree.get_dir_nodes(node.path)

    # busca todas las coincidencias de "name" en el directorio "node"
    def search(self, node, name):
        directorio = self.get_childs(node)
        items = []
        for item in directorio:
            if name in item.name:
                items.append(item)
            if item.type == "dir":
                items.extend(self.search(item, name))
        return items
