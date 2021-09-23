#!/usr/bin/env python3

import os
import hashlib
import requests
import logging

class ApiHandler:
    def __init__(self, host, version, loader, mod_dir):
        self.host = host
        self.version = str(version)
        self.loader = loader
        self.__set_api_host()
        self.mod_dir = mod_dir
        logging.info(f'API Handler details: {self}')

    def __repr__(self) -> str:
        return str(self.__dict__)


    def __set_api_host(self):
        api_hosts = {
            'modrinth':'https://api.modrinth.com/api/v1/mod'
        }
        self.api_host = api_hosts[self.host]


    def download_mod(self, mod_name: str):
        if self.host == 'modrinth':
            self.__download_modrinth(mod_name)


    def __download_modrinth(self, mod_name: str):
        mod_id = self.__get_modrinth_id(mod_name)
        mod = self.__filter_modrinth_version(mod_id)
        filename = mod['files'][0]['filename']
        jar_file = os.path.join(self.mod_dir, filename)

        logging.info(f'From:{self.host} Downloading:{mod_name}({mod_id}) File:{filename}')

        # Download the mod, if the file hashes dont match, redownload the mod and check again
        while True:
            try: 
                with open(jar_file, 'wb') as f:
                    f.write(requests.get(mod['files'][0]['url'], stream=True).content)  

                if not self.__file_checksum(jar_file, mod['files'][0]['hashes']['sha512']):
                    continue
            except:
                if not mod:
                    logging.info(f'{mod_name} not found, check on {self.host} if it exists or mod name spelling')
                break
            else:
                break


    def __get_modrinth_id(self, mod_name: str) -> str:
        request =  f'{self.api_host}?query={mod_name.lower()}'
        
        for mod in requests.request('GET',request).json().get('hits'):
            if mod_name in mod.get('title') and self.loader in mod.get('categories'):
                return mod["mod_id"].split('-')[1]


    def __filter_modrinth_version(self, mod_id: str):
        # Send the id, and get back all version available for the mod
        request = f'{self.api_host}/{mod_id}/version'
        mod_versions = requests.request('GET', request).json()

        # Get all versions that match one in yaml file
        versions = [v for v in mod_versions if self.version == v['game_versions'][-1]]
        
        return versions[0] if versions else None


    def __file_checksum(self, file_path, url_hash) -> bool:

        with open(file_path, 'rb') as f:
            file_hash = hashlib.sha512()
            while chunk := f.read(8192):
                file_hash.update(chunk)

        return file_hash.hexdigest() == url_hash
