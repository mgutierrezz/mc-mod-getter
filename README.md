# mc-mod-getter [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Package Pypi](https://img.shields.io/pypi/v/mc-mod-getter.svg)](https://pypi.org/project/mc-mod-getter)

Utility to download Minecraft mods from the internet

## Usage

I made this tool to download & update mods using [MultiMC](https://github.com/MultiMC/MultiMC5) but you can use this as a standalone python module as well

### MultiMC

1. Create or Edit a minecraft instance 

   ***NOTE**: Ensure there are no spaces in the name*

2. Install your loader of choice

3. Download the binary from releases or [build your own binary](#building-your-own-binary) from scratch

4. Copy the binary to your MultiMC's instance .minecraft folder

5. Create a [yaml file](#yaml-file-structure) in the same .minecraft directory

6. Enable Custom Commands under in your instance's Settings & paste the following in the Pre-launch command box

   ```bash
   $INST_MC_DIR/mc-mod-getter.exe --file $INST_MC_DIR/<FILENAME>.yaml -v
   ```

7. Launch your instance

### OR

Install it from PyPi to an env:

```bash
python -m pip install mc-mod-getter
```

Run the tool:

```bash
python -m mc-mod-getter --file /path/to/file.yaml
```



## YAML File Structure

The tool takes a yaml file as input (Tabs for indentations, space after hyphens)
Here's an example yaml file:

```yaml
loader: fabric
version: 1.17.1
mod_dir: C:\Users\gute\Downloads\test
mods:
    curseforge:
        - Cloth Config API (Fabric)
    modrinth:
        - Fabric API
        - FallingTree
        - EasierVillagerTrading
        - Mod Menu
        - Starlight
        - Hydrogen
        - Sodium
        - Lithium
        - Indium
        - DashLoader
        - Enhanced Block Entities
        - Seamless Loading Screen
        - Falling Leaves
```

### Supported Mod Hosts:

> [Modrinth](https://modrinth.com/mods?q=)

> [Curseforge](https://www.curseforge.com/minecraft/mc-mods)

## Building Your Own Binary

Activate an env and navigate to the root project directory

```bash
make build
```

or if you don't have make

```bash
python3 -m pip install pyinstaller 
python3 -m PyInstaller --onefile mc_mod_getter/__main__.py
```
