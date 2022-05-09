import subprocess
import re
import json
distro_list = ['AIX', 'Alpine', 'Alpine_small', 'Amazon', 'Anarchy', 'AlterLinux', 'Anarchy', 'Android',
               'android_small', 'Antergos', 'antiX', '"AOSC OS"', '"AOSC OS/Retro"', 'Arch', 'Apricity', 'ArchCraft',
               'ArcoLinux', 'ArchBox', 'ARCHlabs', 'ArchMerge', 'Arch_old', 'Arch_small', 'ArchStrike', 'ArcoLinux',
               'Arcolinux_small', 'Artix', 'Artix_small', 'Arya', 'Bedrock', 'Bitrig', 'BlackArch', 'BLAG', 'BlankOn',
               'BlueLight', 'bonsai', 'BSD', 'BunsenLabs', 'Calculate', 'Carbs', 'CentOS', 'CentOS_small', 'Chakra',
               'ChaletOS', 'Chapeau', 'Chrom', 'Cleanjaro', 'Cleanjaro_small', 'Clear_Linux', 'ClearOS', 'Clover',
               'Condres', 'Container_Linux', 'CRUX', 'CRUX_small', 'Cucumber', 'dahlia', 'DarkOs', 'Debian',
               'Debian_small', 'Deepin', 'DesaOS', 'Devuan', 'DracOS', 'DragonFly', 'Dragonfly_old ', 'Dragonfly_small',
               'Drauger', 'Elementary', 'Elementary_small', 'EndeavourOS', 'Endless', 'EuroLinux', 'Exherbo', 'Fedora',
               'Fedora_small', 'Feren', 'FreeBSD', 'FreeBSD_small', 'FreeMiNT', 'Frugalware', 'Funtoo', 'GalliumOS',
               'Garuda', 'Gentoo', 'Gentoo_small', 'gNewSense', 'GNOME', 'GNU', 'GoboLinux', 'Grombyang', 'Guix',
               'GUIX_small', 'Haiku', 'Hash', 'Huayra', 'Hyperbola', 'Hyperbola_small', 'instantOS', 'IRIX', 'Itc',
               'janus', 'Kali', 'KaOS', 'KDE_neon', 'Kibojoe', 'Kogaion', 'Korora', 'KSLinux', 'Kubuntu', 'LaxerOS',
               'LEDE', 'LFS', 'LibreELEC', 'Linux_Lite', 'LinuxLite_small', 'LinuxMint', 'LMDE', 'Lubuntu', 'Lunar',
               'macos', 'Mac_small', 'Mageia', 'MagpieOS', 'Mandriva', 'Manjaro', 'Manjaro_small', 'Maui', 'Mer',
               'Minix', 'MX_Linux', 'MX_small', 'Namib', 'Neptune', 'NetBSD', 'NetBSD_small', 'Netrunner', 'Nitrux',
               'NixOS', 'NixOS_small', 'Nurunner', 'NuTyX', 'Obarun', 'OBRevenge', 'OpenBSD', 'OpenBSD_small',
               'openEuler', 'OpenIndiana', 'openmamba', 'OpenMandriva', 'OpenStage', 'openSUSE', 'openSUSE_Leap',
               'OpenSUSE_small', 'openSUSE_Tumbleweed', 'OpenWrt', 'Oracle', 'OS Elbrus', 'osmc', 'PacBSD', 'Parabola',
               'Parabola_small', 'Pardus', 'Parrot', 'Parsix', 'PCLinuxOS', 'Pentoo', 'Pengwin', 'Peppermint', 'popos',
               'POP_OS_small', 'Porteus', 'PostMarketOS', 'postmarketOS_small', 'Proxmox', 'Puppy', 'PureOS',
               'PureOS_small', 'Qubes', 'Radix', 'Raspbian', 'Raspbian_small', 'Reborn_OS', 'Redcore', 'Redhat',
               'Redhat_old', 'Redstar', 'Refracted_Devuan', 'Regata', 'Rosa', 'Sabayon', 'sabotage', 'Sailfish',
               'SalentOS', 'Scientific', 'Septor', 'SereneLinux', 'SharkLinux', 'Siduction', 'Slackware',
               'Slackware_small', 'SliTaz', 'SmartOS', 'Solus', 'Source_Mage', 'Sparky', 'Star', 'SteamOS', 'SunOS',
               'SunOS_small', 'SwagArch', 'Tails', 'Trisquel', 'TrueOS', 'Ubuntu', 'Ubuntu-Budgie', 'Ubuntu-GNOME',
               'Ubuntu-Mate', 'Ubuntu_old', 'Ubuntu_small', 'Ubuntu-Studio', 'Univention', 'Venom', 'Void',
               'Void_small', 'Windows10', 'Windows7', 'XFerience', 'Xubuntu', 'Zorin']

a = []
l = len(distro_list)
if __name__ == '__main__':
    for index, distro in enumerate(distro_list):
        out = subprocess.run(["neofetch", "-L", "--ascii_distro", distro], stdout=subprocess.PIPE)
        a.append(re.sub(r'\x1b(\[.*?[@-~]|\].*?(\x07|\x1b\\))', '', out.stdout.decode('utf-8')))
        print(f"{index+1} out of {l} done")
    with open('dump.txt', 'w') as FILE:
        json.dump(a, FILE)

