# python-google-agenda

This script could be used in a terminal helping us to watch appointment.

## Prerequisites
* move agenda.py in the /usr/share/pyshared/
* make a symbolic link in the /usr/local/bin directory :
    * ln -s /usr/share/pyshared/agenda.py agenda

## Usage
For now, the date format and message are in french. I can translate if necessary.


```
agenda [-h] [-a A A A A] [N]

Affiche mon agenda

positional arguments:
  N           Nombre d'événements à afficher

optional arguments:
  -h, --help  show this help message and exit
  -a A A A A  Insérer un événemets (Exemple: -a "mon événement" 10.10.2015
              12:00 13:00)
```
