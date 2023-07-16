# Time2Grow (Mysty's TimeToGrow version)
### This is my "Non-Official" entry for TimeEnjoyed CodeJam
#### This entry is purely for educational purposes to allow the TimeToGrow team to compare each-others versions and code
#### The Game idea is all thanks to Bunnie and TimeEnjoyed <3


## Setup
- **Time2Grow uses Python 3.11. Please download and install Python 3.11.**

### PyCharm:

Use `Git` > `clone...` > `URL:` == `https://github.com/EvieePy/Time2Grow.git`
- Create a venv with Python 3.11

In the PyCharm terminal (found on bottom left), run:
```shell
pip install -U -r requirements.txt
```


### Windows:

```shell
git clone https://github.com/EvieePy/Time2Grow.git
cd Time2Grow
py -3.11 -m venv venv
./venv/Scripts/activate
pip install -U -r requirements.txt
```


### Linux/MacOS
- **Note:** I have not tested this on these environments.

```shell
git clone https://github.com/EvieePy/Time2Grow.git
cd Time2Grow
python3.11 -m venv venv
source venv/bin/activate
pip install -U -r requirements.txt
```


## Config
- Copy & Paste [config.example.json](config.example.json) into a file: `config.json`
- Fill in the blanks: `token` and `channel`. Adjust other settings as you please but please read comments.


## Running
- In your activated venv:

```shell
python launcher.py
```


## Using
**For testing in a browser:**
- Vist: http://127.0.0.1:8000/


**For OBS:**
- Create a new Source `Browser` and name it `Time2Grow Overlay`
- URL: `http://127.0.0.1:8000/`
- Width and Height should match your stream output E.g. Width: 1920 and Height: 1080
- **Remove** everything in Custom CSS
- OK


## Commands
- Note: `<prefix>` should be changed with what you set in your config.
- Note: `<username>` should be replaced with the name of the user you wish to attack. E.g. `xmetrix`

**Create a Plant:**
- `<prefix>plant`
  - creates a plant. 1 per user.

**Water a Plant:**
- `<prefix>water`
  - waters your plant. You must water your plant when it is wilted, or it dies.

**Attack a Plant:**
- `<prefix>attack <username>`
  - attacks another users plant. Has a small chance of being reversed onto you.

**Thug Life:**
- `<prefix>thug`
  - add some thug life to your plant.


## Licenses
All source code is licensed using [MIT](https://opensource.org/license/mit/)

All images and assets **must not** be resold, modified or used for any purpose other than this game without prior permission.