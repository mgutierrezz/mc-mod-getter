# mc-mod-getter [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Package Pypi](https://img.shields.io/pypi/v/mc-mod-getter.svg)](https://pypi.org/project/mc-mod-getter)

Utility to download Minecraft mods from the internet

## Usage

I made this tool to download & update mods using [MultiMC](https://github.com/MultiMC/MultiMC5) but you can use this as a standalone cli tool as well.

### MultiMC

1. Create or Edit a minecraft instance 

   ***NOTE**: Ensure there are no spaces in the name*

2. Install your loader of choice

3. Download the binary from releases or build your own binary from scratch

4. Copy the binary to your MultiMC's instance .minecraft folder

5. Create a YAML file in the same .minecraft directory

6. Enable Custom Commands under in your instance's Settings & paste the following in the Pre-launch command box

   ```bash
   $INST_MC_DIR/mc-mod-getter.exe --file $INST_MC_DIR/<FILENAME>.yaml -v
   ```

7. Launch your instance



### CLI 

Install it from PyPi to an env:

```bash
python -m pip install mc-mod-getter
```

Run the tool:

```bash
python -m mc-mod-getter --file /path/to/file.yaml -v
```



1. 

```yaml
modrinth:
    version: 1.17.1
    loader: fabric
    mod_dir: C:\Games\mmc-stable-win32\MultiMC\instances\test-mc-1.17.1\.minecraft\mods
    mods:
        - Fabric API
        - FallingTree
        - EasierVillagerTrading
        - Mod Menu
        - Starlight
        - Hydrogen
```

**Note**: 







