import csv
from typing import Any, List

from importer.utils.get_export_path import get_export_path


class Writer:
    def __init__(
        self,
        filename: str,
        files: List[str],
        sites: List[str],
        timestamps: List[str],
        meta_properties: List[str],
        meta_values: List[List[Any]],
    ):
        self.__set_path(filename)
        self.__files = files
        self.__sites = sites
        self.__timestamps = timestamps
        self.__set_titles(meta_properties)
        self.__meta_values = meta_values

        self.__write()

    def __set_path(self, filename: str):
        self.__path = get_export_path(filename)

    def __set_titles(self, meta_properties: List[str]):
        self.__titles = []
        self.__set_titles_default()
        self.__set_titles_meta(meta_properties)

    def __set_titles_default(self):
        default_titles = [
            'files',
            'files_site',
            'file_start',
            'file_tag'
        ]

        for default_title in default_titles:
            self.__titles.append(default_title)

    def __set_titles_meta(self, meta_properties: List[str]):
        for meta_property in meta_properties:
            self.__titles.append(meta_property)

    def __write(self):
        length = len(self.__files)

        with open(self.__path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(self.__titles)

            for index in range(length):
                row = [
                    self.__files[index],
                    self.__sites[index],
                    self.__timestamps[index],
                    None,
                ]

                for meta_value in self.__meta_values[index]:
                    row.append(meta_value)

                writer.writerow(row)
