import os
import shutil
import mimetypes
from typing import AnyStr, LiteralString


class File:
    def __init__(self, vault, type_key, filename: AnyStr, raw_data=None):
        self.vault = vault
        self.type_key = type_key
        self.filename = filename
        self.raw_data = raw_data
        (self.base_filename,
         self.ext) = os.path.splitext(filename)

        self.ext = self.ext.lstrip('.')
        self.mimetype = mimetypes.guess_type(filename)[0]

    def save(self):
        dest_path = self.path()
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        if self.raw_data:
            with open(dest_path, 'wb') as f:
                f.write(self.raw_data)
        else:
            raise ValueError("No raw data to save.")

    def base(self):
        return self.base_filename

    def ext(self):
        return self.ext

    def type(self):
        return self.type_key

    def mime(self):
        return self.mimetype

    def basedir(self):
        return self.vault.data[self.type_key]

    def dir(self) -> LiteralString | str:
        base_dir = self.basedir()
        return os.path.join(base_dir, self.base_filename[:2], self.base_filename[2:4])

    def path(self):
        return os.path.join(self.dir(), self.filename)


class Vault:
    def __init__(self, data):
        self.data = data
        self._create_directories()

    def _create_directories(self):
        for path in self.data.values():
            os.makedirs(path, exist_ok=True)

    class Folder:
        def __init__(self, vault, path, type_key):
            self.vault = vault
            self.path = path
            self.type_key = type_key

        def save(self, filename, raw_data):
            file = File(self.vault, self.type_key, filename, raw_data)
            file.save()

        def import_file(self, src_file, dest_filename):
            dest_path = os.path.join(self.path, dest_filename)
            shutil.move(src_file, dest_path)

        def export(self, filename, dest_folder):
            src_path = os.path.join(self.path, filename)
            dest_path = os.path.join(dest_folder, filename)
            shutil.copy(src_path, dest_path)

        def exportwithname(self, filename, dest_folder, dest_filename):
            src_path = os.path.join(self.path, filename)
            dest_path = os.path.join(dest_folder, dest_filename)
            shutil.copy(src_path, dest_path)

        def __call__(self, filename, raw_data=None):
            return File(self.vault, self.type_key, filename, raw_data)

        def __str__(self):
            return self.path

    def __getattr__(self, item):
        if item in self.data:
            return self.Folder(self, self.data[item], item)
        raise AttributeError(f"'Vault' object has no attribute '{item}'")
