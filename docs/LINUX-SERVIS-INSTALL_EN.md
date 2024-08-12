# Install bot as service on Linux
_Setting bot as service allows you to run it in backrgound and easily control._

## Installation steps
#### I. Clone repository
1. Pick folder where you want your bot to be stored:
    `root/example_folder`_(for example)_
2. Open terminal and navigate to this folder:
    `cd root/example_folder`
3. Clone bot using [git](https://www.git-scm.com/):
    `git clone https://github.com/HiddenCodeDevs/DogsHouseRefBot.git`
4. Navigate to clonned repository:
    `cd root/example_folder/DogsHouseRefBot`

#### II. Setup project
1. Create a virtual enviroment:
    `python3 -m venv venv`
2. Activates the virtual environment:
  `source venv/bin/activate`
3. Install all Python dependencies:
  `pip3 install -r requirements.txt`
4. Create enviroment file from template:
  `cp .env-example .env`
5. Setup your needed parameters in `.env` file using any code editor:
  `nano .env`_(nano as example)_
6. Run `main.py` and init session.
  
#### III. Create service
1. Navigate to system folder where every service is stored using terminal:
    `cd /etc/systemd/system/`
2. Create service file with any name you want:
    `sudo touch DogsHouseRefBot.service`
3. Fill `.service` file with content using any code editor:
    `sudo nano DogsHouseRefBot.service` _(nano for example)_
    **Content:**
    > ```makefile
    > [Unit]
    > Description=DogsHouseRefBot
    > After=network.target
    > 
    > [Service]
    > User=root
    > WorkingDirectory=/root/example/DogsHouseRefBot/
    > Environment=PATH=/root/example/DogsHouseRefBot/venv/bin/
    > ExecStart=/root/example/DogsHouseRefBot/venv/bin/python3 /root/example/> DogsHouseRefBot/main.py -a 2
    > 
    > Restart=always
    > 
    > [Install]
    > WantedBy=multi-user.target
    > ```
 - `User=` - user u running this service from
 - `WorkingDirectory=` - path to cloned repository folder
 - `Enviroment=` - enviroment folder / venv value inserts
 - `ExecStart=` - runner command  

#### IV. Start service
1. Reload system manager config using terminal:
    `sudo systemctl daemon-reload`
1. Enable service, setting it as autostarted:
    `sudo systemctl enable DogsHouseRefBot.service`
___
**Now we are done.**

___
# Service manipulations:
**Stop service:**
`sudo systemctl stop DogsHouseRefBot.service`

**Start service:**
`sudo systemctl start DogsHouseRefBot.service`

**Restart service:**
`sudo systemctl restart DogsHouseRefBot.service`

**Check status:**
`sudo systemctl status DogsHouseRefBot.service`

**Check logs:**
`sudo journalctl -u DogsHouseRefBot.service`

**Check logs in real time:**
`sudo journalctl -u DogsHouseRefBot.service -f`