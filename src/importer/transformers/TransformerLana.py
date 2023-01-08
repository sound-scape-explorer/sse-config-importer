from pathlib import Path

from importer.common.Reader import Reader
from importer.common.Writer import Writer
from importer.utils.get_import_path import get_import_path


class TransformerLana:
    __path: Path

    def __init__(
        self,
        import_filename: str,
        export_filename: str,
    ):
        self.__import_filename = import_filename
        self.__export_filename = export_filename

        self.__set_path()
        self.__set_map()

        self.__import()

        self.__select_columns()

        self.__read_files()
        self.__read_sites()
        self.__read_replicas()
        self.__read_years()
        self.__set_meta_values_by_property()

        self.__generate_exported_files()
        self.__generate_exported_timestamps()
        self.__generate_exported_meta_properties()
        self.__generate_exported_meta_values()

        self.__export()

    def __set_path(self):
        self.__path = get_import_path(self.__import_filename)

    def __set_map(self):
        self.__path_by_year_then_site_then_replica = {
            2021: {
                'passe': {
                    1: '/2021/balise_passe/replica1/data/',
                    2: '/2021/balise_passe/replica2/Data/',
                    3: '/2021/balise_passe/replica3/data/',
                },
                'naturel': {
                    1: '/2021/site_naturel/replica1/data/',
                    2: '/2021/site_naturel/replica2/data/',
                    3: '/2021/site_naturel/replica3/data/',
                },
                'touriste': {
                    1: '/2021/site_touristique/replica1/data/',
                    2: '/2021/site_touristique/replica2/data/',
                    3: '/2021/site_touristique/replica3/data/',
                },
            },
            2022: {
                'passe': {
                    1: '/2022/Balise_passe/1replica/2022-11/data/',
                    2: '/2022/Balise_passe/2replica/2022-11/Data/',
                    3: '/2022/Balise_passe/3replica/2022-12/data/',
                },
                'naturel': {
                    1: '/2022/Turiroa_naturel/1replica/2022-11/data/',
                    2: '/2022/Turiroa_naturel/2replica/2022-11/data/',
                    3: '/2022/Turiroa_naturel/3replica/2022-12/data/',
                },
                'touriste': {
                    1: '/2022/Turiroa_touristique/1replica/2022-11/data/',
                    2: '/2022/Turiroa_touristique/2replica/2022-11/data/',
                    3: '/2022/Turiroa_touristique/3replica/2022-12/data/',
                },
            },
        }

    def __import(self):
        self.__reader = Reader(str(self.__path))

    def __select_columns(self):
        self.__select_files_column()
        self.__select_meta_properties_columns()

    def __select_files_column(self):
        self.__files_column = self.__reader.get_column('fichier')

    def __select_meta_properties_columns(self):
        self.__meta_properties_columns = {
            'site': self.__reader.get_column('site'),
            'replica': self.__reader.get_column('replica'),
            'snap': self.__reader.get_column('snap'),
            'profondeur': self.__reader.get_column('profondeur'),
            'geomorph': self.__reader.get_column('geomorpho'),
            'substrat': self.__reader.get_column('substrat'),
            'periode': self.__reader.get_column('periode'),
            'bateau': self.__reader.get_column('bateau'),
            'pluie': self.__reader.get_column('pluie'),
            'sonar': self.__reader.get_column('sonar'),
            'abondance': self.__reader.get_column('abondance'),
            'richesse': self.__reader.get_column('richesse'),
            'abvocal': self.__reader.get_column('ab_vocalise'),
            'rvocal': self.__reader.get_column('r_vocalise'),
        }

    def __read_files(self):
        self.__files = self.__reader.read_column(self.__files_column)

    def __read_sites(self):
        column = self.__reader.get_column('site')
        self.__sites = self.__reader.read_column(column)

    def __read_replicas(self):
        column = self.__reader.get_column('replica')
        self.__replicas = self.__reader.read_column(column)

    def __read_years(self):
        column = self.__reader.get_column('annee')
        self.__years = self.__reader.read_column(column)

    def __generate_exported_files(self):
        self.__exported_files = []

        for index, file in enumerate(self.__files):
            year = self.__years[index]
            site = self.__sites[index]
            replica = self.__replicas[index]

            exported_file = \
                self.__path_by_year_then_site_then_replica[year][site][
                    replica] + file

            self.__exported_files.append(exported_file)

    def __generate_exported_timestamps(self):
        self.__exported_timestamps = []

        for file in self.__files:
            file_parts = file.split('_')
            timestamp = file_parts[0]
            timestamp = timestamp.replace('T', '_')

            self.__exported_timestamps.append(timestamp)

    def __generate_exported_meta_properties(self):
        self.__exported_meta_properties = []

        for meta_property in self.__meta_properties_columns.keys():
            exported_meta_property = f'files_{meta_property.upper()}'
            self.__exported_meta_properties.append(exported_meta_property)

    def __set_meta_values_by_property(self):
        self.__meta_values_by_property = {}

        for index, (meta_property, meta_column) in enumerate(
                self.__meta_properties_columns.items()
        ):
            meta_values = self.__reader.read_column(meta_column)
            self.__meta_values_by_property[meta_property] = meta_values

    def __generate_exported_meta_values(self):
        self.__exported_meta_values = []

        for index, file in enumerate(self.__files):
            meta_values = []

            for meta_property in self.__meta_properties_columns.keys():
                meta_value = self.__meta_values_by_property[meta_property][
                    index]

                meta_values.append(meta_value)

            self.__exported_meta_values.append(meta_values)

    def __export(self):
        Writer(
            self.__export_filename,
            self.__exported_files,
            self.__sites,
            self.__exported_timestamps,
            self.__exported_meta_properties,
            self.__exported_meta_values,
        )
