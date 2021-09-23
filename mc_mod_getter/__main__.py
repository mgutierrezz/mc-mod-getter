#!/usr/bin/env python3

from mc_mod_getter import __project_urls__
from mc_mod_getter.utils.ApiHandler import ApiHandler
from pathlib import Path
import logging
import click
import yaml


@click.command()
@click.option('--file','-f', help='Path to mod yaml file', type=click.Path(exists=True), required=True)
@click.option('--verbose','-v', help='Verbose mode', is_flag=True)
def main(file,verbose):
    # TODO: Possibly get yaml from gui but thats extra work :/
    mods_yaml = file

    if verbose:
        logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')

    logging.info(f'Using yaml file: {mods_yaml}')

    mods_dict = yaml.safe_load(open(mods_yaml, 'r')).items()
    
    for host, mod_info in mods_dict:
        mod_list = mod_info.pop('mods')

        if not mod_info.get('mod_dir',None):
            mod_info['mod_dir'] = str(Path.home() / 'Downloads')

        logging.info(f'Downloading mods to: {mod_info["mod_dir"]}')

        api_handler = ApiHandler(host, **mod_info)

        for mod in mod_list:
            api_handler.download_mod(mod)


if __name__ == '__main__':
    main()
