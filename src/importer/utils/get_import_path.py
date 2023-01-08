import pathlib

from constants import PATH_BASE, PATH_IMPORTS


def get_import_path(filename: str):
    return pathlib \
        .Path(PATH_BASE + PATH_IMPORTS) \
        .joinpath(filename) \
        .absolute()
