import pathlib

from constants import PATH_BASE, PATH_EXPORTS


def get_export_path(filename: str):
    return pathlib \
        .Path(PATH_BASE + PATH_EXPORTS) \
        .joinpath(filename) \
        .absolute()
