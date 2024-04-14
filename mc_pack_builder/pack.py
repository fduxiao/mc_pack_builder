"""
This module intends to model a pack, which should be a directory of many files containing certain data.
A class :py:class:`mc_pack_builder.pack.Pack` is provided to organize them easily.

Such a directory is a tree with each leaf serializable to a file. Then for each node
of that tree (a branch or a leaf), we design a `dump` method to serialize the data.

Though we finally want to dump everything to files, sometimes it is convenient to `dump`
them to a :py:class:`dict` in order to do some tests. Thus, I break a pack into the following
3 parts:

1. A filesystem describer with `mkdir` method, and `open` method, together with some other info like json indent.
2. A tree object that can `dump` the data into a file system.
3. A Pack class wrapping a tree.
"""
import json
from contextlib import contextmanager
import io
from pathlib import Path
from typing import IO, Callable, TypeVar, Self
from .natural_model import NaturalModel, DictModel


class FileSystem:
    """
    abstract file system class
    """

    json_indent = 4
    json_ensure_ascii = False

    def mkdir(self, path: Path) -> "FileSystem":
        """
        mkdir

        :param path:
        :return: the result is certainly another file system starting with path
        """
        pass

    def open(self, path: Path, mode="w") -> IO:
        """
        open

        :return:
        """
        pass


class OSFileSystem(FileSystem):
    """
    the file system of the operating system
    """
    def __init__(self, path: Path = Path(".")):
        self.path = path

    def mkdir(self, path: Path) -> "OSFileSystem":
        new_path = self.path / path
        new_path.mkdir(parents=True, exist_ok=True)
        return OSFileSystem(new_path)

    def open(self, path: Path, mode="w") -> IO:
        self.mkdir(path.parent)
        return open(self.path / path, mode)


class DictFileSystem(FileSystem):
    """
    For testing, one may want to save all data to a file system
    """
    json_indent = None
    json_ensure_ascii = False

    def __init__(self, fs=None):
        if fs is None:
            fs = dict()
        self.dict = fs

    def mkdir(self, path: Path) -> "DictFileSystem":
        result = self.dict
        for k in path.parts:
            sub_dir = result.get(k, None)
            if sub_dir is None:
                sub_dir = dict()
                result[k] = sub_dir
            result = sub_dir
        return DictFileSystem(result)

    def open(self, path: Path, mode="w") -> IO:
        parent = self.mkdir(path.parent).dict
        name = path.name

        if mode == 'w':
            file = io.StringIO()
        if mode == 'wb':
            file = io.BytesIO()

        @contextmanager
        def wrapper():
            yield file
            parent[name] = file.getvalue()
        return wrapper()


class FSTree:
    """
    The tree object allowed to dump to a :py:class:`FileSystem`
    """
    def dump(self, rel_path: Path, fs: FileSystem):
        """

        :param rel_path: The path relative to the parent
        :param fs: :py:class:`FileSystem` object
        :return:
        """
        pass


T = TypeVar("T")


class Branch(FSTree):
    """
    for a branch
    """

    def __init__(self, nodes: dict[Path, FSTree] = None):
        if nodes is None:
            nodes = dict()
        self.nodes: dict[Path, FSTree] = nodes

    def add_node(self, path: str | Path, node: FSTree):
        """
        add a node to current branch

        :param path: the path related to self. You can pass something like "a/b"
        :param node: some :py:class:`FSTree` object
        :return: the node argument passed to this function
        """
        path = Path(path)
        self.nodes[path] = node
        return node

    def ensure_node(self, path: str | Path, node_class: Callable[[], T] = None) -> T:
        """
        Usually, we don't want to repeatedly add nodes with the same path.
        This method is provided to ensure a node is given

        :param path:
        :param node_class: a function returns a node
        :return:
        """
        path = Path(path)
        node = self.nodes.get(path, None)
        if node is not None:
            return node
        if node_class is None:
            node_class = Dir
        node = node_class()
        self.add_node(path, node)
        return node

    def dump(self, rel_path: Path, fs: FileSystem):
        # dump for self
        fs = fs.mkdir(rel_path)

        # dump for nodes
        for path, node in self.nodes.items():
            node.dump(path, fs)


class Leaf(FSTree):
    """
    dummy class annotating a leaf of :py:class:`FSTree`
    """
    mode = 'w'
    fs = None

    def dump_to(self, file: IO):
        """
        The general `dump` behavior of a file is to open it, dump to the IO object, and close it.
        So we only have to define the `dump to file` function. Besides, `self.fs` is set to the
        :py:class:`FileSystem` object passed to `dump`

        :param file: the IO object opened by :py:meth:`Leaf.dump`
        :return:
        """
        pass

    def dump(self, rel_path: Path, fs: FileSystem):
        with fs.open(rel_path, self.mode) as file:
            self.fs = fs
            self.dump_to(file)


class Text(Leaf):
    def __init__(self):
        self.text = ""

    def set(self, text=""):
        self.text = text
        return self

    def append(self, text):
        self.text += text
        return self

    def dump_to(self, file: IO):
        file.write(self.text)


class Json(Leaf):
    def __init__(self, data: NaturalModel):
        self.data = data

    def dump_to(self, file: IO):
        json.dump(self.data.dump(), file, indent=self.fs.json_indent,
                  ensure_ascii=self.fs.json_ensure_ascii)


class Dir(Branch):
    """
    a helper to gather different leaves
    """

    def __init__(self, nodes: dict[Path, FSTree] = None):
        super().__init__(nodes)

    def dir(self, path: str | Path) -> Self:
        return self.ensure_node(path, Dir)

    def text(self, path: str | Path) -> Text:
        return self.ensure_node(path, Text)

    def add_json(self, path: str | Path, data: T) -> T:
        if isinstance(data, dict):
            data = DictModel(data=data)
        self.ensure_node(path, lambda: Json(data))
        return data


class Pack(Dir):
    """
    The class to model a directory of files representing data of different things.
    A Pack contains many properties. Each property is associated with a path, which
    is later used to generate
    """

    def write_to(self, path: str | Path = None, fs=None):
        """
        write the data to somewhere

        :param path:
        :param fs:
        :return:
        """
        if path is None:  # pwd
            path = Path(".")
        if fs is None:
            fs = OSFileSystem(Path(path))
        self.dump(Path(""), fs)
