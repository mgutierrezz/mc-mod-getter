#!/usr/bin/env python3

from pkg_resources import require
from mc_mod_getter import __project_urls__
from mc_mod_getter.utils.ApiHandler import ApiHandler
from pathlib import Path
import logging
import click
import yaml


@click.command()
@click.option('--file','-f', help='Path to mod yaml file',type=click.Path(exists=True), required=True)
@click.option('--verbose','-v', help='Verbose mode', is_flag=True)
def main(file,verbose):
    # TODO: Possibly get yaml from gui but thats extra work :/
    mods_yaml = file

    if verbose:
        logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')

    logging.info(f'Using yaml file: {mods_yaml}')

    mods_dict = yaml.safe_load(open(mods_yaml, 'r')).items()
    
    for host, mods in mods_dict:
        download_dir = mods.get('mmc_dir', str(Path.home() / 'Downloads'))
        logging.info(f'Downloading mods to: {download_dir}')

        api_handler = ApiHandler(host, mods['version'], mods['loader'], download_dir, verbose)

        for mod in mods['mods']:
            api_handler.download_mod(mod)


if __name__ == '__main__':
    main()

    