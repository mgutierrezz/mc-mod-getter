#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
from typing import Union
import requests as req
import logging
import hashlib
import types
import os,sys,json



class ApiHandler:
    class NoAccess(Exception): pass
    class Unknown(Exception): pass

    _api_handler_hosts = {}

    def __init_subclass__(cls, **kwargs: str) -> None:
        """Registers the the different ApiHandler subclasses to be used for __new__ """
        super().__init_subclass__(**kwargs)
        cls._api_handler_hosts[cls._host] = cls

        
    def __new__(cls, host: str, **kwargs: str) -> Union[ModrinthApiHandler, CurseforgeApiHandler, Unknown]:
        """Creates the correct ApiHandler subclass given the host arg """
        api_handler_host = cls._api_handler_hosts.get(host, None)
        
        if api_handler_host:
            return object.__new__(api_handler_host)
        else:
            # Host provided in the yaml is not supported
            raise cls.Unknown(f'Mod host: {host} is not supported')


    def __init__(self, *args: str, **kwargs: str) -> None:
        self.version = kwargs.pop('version')
        self.loader = kwargs.pop('loader').lower()
        self.mod_dir = kwargs.pop('mod_dir', str(Path.home() / 'Downloads'))


    def __repr__(self) -> str:
        return str(self.__dict__)

    
    @classmethod
    def _file_checksum(cls, file_path: str, host_hash: Union[list,str]) -> bool:
        hash_algorithms = {    
            'modrinth': 'sha512',
            'curseforge': 'md5'
        }

        # Handle Curseforge api's 0 or many provided hashes
        if not host_hash:
            logging.info(f'WARNING: Cannot verify {file_path} was downloaded correctly')
            return True

        host_hash = [host_hash] if type(host_hash) is str else host_hash

        with open(file_path, 'rb') as f:
            file_hash = hashlib.new(hash_algorithms[cls._host])
            while chunk := f.read(8192):
                file_hash.update(chunk)


        return any([file_hash.hexdigest() == h for h in host_hash])


    def _get_mod_id(self) -> None:
        raise NotImplementedError
           

    def _filter_mod_version(self) -> None:
        raise NotImplementedError

    
    def download_mod(self, mod_name: str) -> None:
        mod_id = self._get_mod_id(mod_name)
        mod = self._filter_mod_version(mod_id)
        mod_file_path = os.path.join(self.mod_dir, mod['filename'])

        logging.info(f'Downloading Mod: {mod_name}({mod_id}) From: {self._host} File: {mod["filename"]}')

        if Path(mod_file_path).is_file():
            logging.info(f'Skipping Download... Already downloaded')
            return

        # Download the mod, if the file hashes dont match, redownload the mod and check again
        while True:
            try:             
                logging.info(f'Downloading mods to: {self.mod_dir}')
                with open(mod_file_path, 'wb') as f:
                    f.write(req.get(mod['url'], stream=True).content)  
                if not self._file_checksum(mod_file_path, mod['hashes']):
                    continue
            except Exception as e:
                logging.info(e)
                if not mod:
                    logging.info(f'{mod_name} not found, check on {self._host} if it exists or mod name spelling')
                break
            else:
                break


class ModrinthApiHandler(ApiHandler):
    _host = 'modrinth'
    _host_api = 'https://api.modrinth.com/api/v1/mod'

    def __init__(self, *args: str, **kwargs: str) -> None:
        super().__init__(*args, **kwargs)


    def __repr__(self) -> str:
        return super().__repr__()


    def _get_mod_id(self, mod_name: str) -> str:
        search_query =  f'{self._host_api}?query={mod_name.lower()}'
        
        for mod in req.request('GET', search_query).json()['hits']:
            if mod_name in mod['title'] and self.loader in mod['categories']:
                return mod['mod_id'].split('-')[1]


    def _filter_mod_version(self, mod_id: str) -> dict:
        # Send the id, and get back all version available for the mod
        versions_query = f'{self._host_api}/{mod_id}/version'
        mod_versions = req.get(versions_query).json()

        # Get all versions that match the mc version found in yaml file
        mod_versions = [v for v in mod_versions if self.version == v['game_versions'][-1]]
        
        # Return first mod in mod_versions, it's the latest mod version matching mc version in yaml
        mod = mod_versions[0]['files'][0] if mod_versions else None

        mod['hashes'] = mod['hashes']['sha512']

        return mod


    def download_mod(self, mod_name: str) -> None:
        super().download_mod(mod_name)


class CurseforgeApiHandler(ApiHandler):
    # NOTE: The Curseforge api is dogwater >:(
    _host = 'curseforge'
    _host_api = 'https://addons-ecs.forgesvc.net/api/v2/addon'
    _user_agent = (
        'user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
    )
    _headers = {'User-Agent': _user_agent}

    def __init__(self, *args: str, **kwargs: str) -> None:
        super().__init__(*args, **kwargs)


    def __repr__(self) -> str:
        return super().__repr__()


    def _get_mod_id(self, mod_name: str) -> str:
        # Search only 1 word from mod name b/c api is dumb and uses OR conditions for each word
        mod_query_name = mod_name.lower().split(' ')[0]
        search_query =  (
            f'{self._host_api}/search?gameId=432&sectionId=6'
            f'&searchFilter={mod_query_name}'
            f'&gameVersion={self.version}'
        )
        
        for mod in req.get(search_query,headers=self._headers).json():          
            if mod_name == mod['name'] and self.loader in str(mod['modLoaders']).lower():
                return mod['id']


    def _filter_mod_version(self, mod_id: str) -> dict:
        try:
            search_query = f'{self._host_api}/{mod_id}'
            mod_versions = req.get(search_query,headers=self._headers).json()['latestFiles']
            mod_versions = [v for v in mod_versions if self.version in v['gameVersion'] and self.loader.capitalize() in v['gameVersion']]

        except:
            # TODO: If searching on curseforge version not in Latest files
            search_query = f'{self._host_api}/{mod_id}'
            mod_versions = req.get(search_query,headers=self._headers).json()
        
        else:
            mod_details = {
                # {curseapi name : renamed}
                'fileName':'filename',
                'downloadUrl': 'url',
                'hashes': 'hashes'
            }

            mod = {mod_details[key]: value for key, value in mod_versions[0].items() if key in mod_details}
            mod['hashes'] = [h['value'] for h in mod['hashes']]

            return mod


    def download_mod(self, mod_name: str) -> None:
        super().download_mod(mod_name)