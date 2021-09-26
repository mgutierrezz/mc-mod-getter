#!/usr/bin/env python3

import os
import logging
import hashlib
import requests as req
from pathlib import Path

class ApiHandler:
    class NoAccess(Exception): pass
    class Unknown(Exception): pass

    _api_handler_hosts = {}


    def __init_subclass__(cls, **kwargs):
        """Registers the the different ApiHandler subclasses to be used for __new__ """
        super().__init_subclass__(**kwargs)
        cls._api_handler_hosts[cls.host] = cls

        
    def __new__(cls, host, **kwargs):
        """Creates the correct ApiHandler class given the host arg """
        api_handler_host = cls._api_handler_hosts.get(host, None)
        
        if api_handler_host:
            return object.__new__(api_handler_host)
        else:
            # Host provided in the yaml is not supported
            raise cls.Unknown(f'Mod host: {host} is not supported')


    def __init__(self,host,version,loader,mod_dir):
        self.version = str(version)
        self.loader = str(loader).lower()
        self.mod_dir = mod_dir


    def __repr__(self) -> str:
        return str(self.__dict__)


    @classmethod
    def __file_checksum(self, file_path, host_hash) -> bool:

        with open(file_path, 'rb') as f:
            file_hash = hashlib.sha512()
            while chunk := f.read(8192):
                file_hash.update(chunk)

        return file_hash.hexdigest() == host_hash


class ModrinthApiHandler(ApiHandler):
    host = 'modrinth'
    host_api = 'https://api.modrinth.com/api/v1/mod'

    def __init__(self, host, version, loader, mod_dir):
        super().__init__(host, version, loader, mod_dir)


    def __repr__(self) -> str:
        return super().__repr__()


    def __get_mod_id(self, mod_name: str) -> str:
        search_query =  f'{self.host_api}?query={mod_name.lower()}'
        
        for mod in req.request('GET', search_query).json()['hits']:
            if mod_name in mod['title'] and self.loader in mod['categories']:
                return mod['mod_id'].split('-')[1]


    def __filter_mod_version(self, mod_id: str):
        # Send the id, and get back all version available for the mod
        versions_request = f'{self.host_api}/{mod_id}/version'
        mod_versions = req.request('GET', versions_request).json()

        # Get all versions that match the mc version found in yaml file
        mod_versions = [v for v in mod_versions if self.version == v['game_versions'][-1]]
        
        # Return first mod in mod_versions, it's the latest mod version matching mc version in yaml
        return mod_versions[0] if mod_versions else None


    def download_mod(self, mod_name: str):
        mod_id = self.__get_mod_id(mod_name)
        mod = self.__filter_mod_version(mod_id)
        mod_file = mod['files'][0]
        mod_file_path = os.path.join(self.mod_dir, mod_file['filename'])

        logging.info(f'Downlaoding Mod: {mod_name}({mod_id}) From: {self.host} File: {mod_file["filename"]}')

        if Path(mod_file_path).is_file():
            logging.info(f'Skipping Download... Already downloaded')
            return

        # Download the mod, if the file hashes dont match, redownload the mod and check again
        while True:
            try: 
                with open(mod_file_path, 'wb') as f:
                    f.write(req.get(mod_file['url'], stream=True).content)  

                if not self.__file_checksum(mod_file_path, mod_file['hashes']['sha512']):
                    continue
            except:
                if not mod:
                    logging.info(f'{mod_name} not found, check on {self.host} if it exists or mod name spelling')
                break
            else:
                break
