# Lib
import logging
from pathlib import Path
# App
from ..files import find_sample_sheet, create_sample_sheet

LOGGER = logging.getLogger(__name__)


def check_array_folders(data_dir):
    """Confirms a folder's idats are separated into sub-folders by array_type, but does not move them for you.
    Should deal with GEO multi-array packages. beta_bake realiably splits IDATs by array type for you, as of v1.5.6."""
    instructions = []
    sample_sheet_file_path = find_sample_sheet(data_dir, return_all=True, create_if_not_found=True)

    # where multiple samplesheets found
    if isinstance(sample_sheet_file_path, list):
        # check if they are in GEO GPLxxx folders
        folders = ['GPL8490', 'GPL13534', 'GPL21145', 'epic_plus', 'mouse']
        for sample_sheet_file in sample_sheet_file_path:
            if any([array_folder in sample_sheet_file.parts for array_folder in folders]):
                # now verify idats are present. later: do the idats match the samplesheet?
                array_type = [array_folder for array_folder in folders if array_folder in sample_sheet_file.parts][0]
                idats_found = list(Path(sample_sheet_file.parent).rglob('*.idat')) + list(Path(sample_sheet_file.parent).rglob('*.idat.gz'))
                instructions.append(f"For {int(len(idats_found)/2)} {array_type} samples run: `methylprep process -d {sample_sheet_file.parent} --all`")
    return instructions
