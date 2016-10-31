# python-google-agenda

This script could be used in a terminal helping us to watch appointment.

## Prerequisites
* move agenda.py in the /usr/share/pyshared/
* make a symbolic link in the /usr/local/bin directory :
    * ln -s /usr/share/pyshared/agenda.py agenda
* create a client credentials for google api on : [developers.google.com](https://developers.google.com/google-apps/calendar)
* download and rename the credentials in the json format to client\_secret.json in the /usr/share/pyshared directory

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

## View
![Image example](https://cloud.githubusercontent.com/assets/1701806/19848017/f5ba5a64-9f4a-11e6-9482-caad51557e2f.jpg)
