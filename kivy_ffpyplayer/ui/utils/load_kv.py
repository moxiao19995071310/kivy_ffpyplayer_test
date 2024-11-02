import logging
import os

from kivy.lang.builder import Builder

work_path = os.getcwd()


class KvLoadException(Exception):
    def __init__(self, msg):
        self.msg = msg


class KvLoad:
    __slots__ = ()

    @staticmethod
    def load(py_file: str, **kwargs) -> None:
        kv_file = None
        try:
            if py_file.endswith(".py"):
                kv_file = py_file.replace(".py", ".kv")
            else:
                kv_file = py_file.replace(".pyc", ".kv")

            _, relative_path = kv_file.split(work_path)
            file_key = relative_path.replace("\\", "/")[1:]
            if file_key in Builder.files:
                return

            logging.info(f"load kv file:{file_key}")
            kwargs['filename'] = file_key
            with open(kv_file, "r", encoding="utf-8") as fd:
                Builder.load_string(fd.read(), **kwargs)
        except Exception as err:
            raise KvLoadException("Load {} file error:{}".format(kv_file, err))
