<a name="readme-top"></a>

<!-- ABOUT THE PROJECT -->
## About The Project

This project was carried out as part of a sprint during a one week formation.
The requirements involved creating a monitoring python script for a Debian VM.
We decided to attempt making a reusable vitals script with a customizable yaml config and a daemon installer to easily deploy it on multiple VM.



### Built With

[![Python][Python]][Python-url]


<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

You do not actually need a virtual machine as long as you have a Linux. But for testing purpose and to avoid downloading the following ressources on your main machine, we recommend it.
Note: It is also possible to run this script in a darwin system.

The prerequisites will assume that you have virtualbox installed on your machine. You will need two virtual machine fully setup, with a Debian ISO, a Bridged Adapter network and with only the SSH server software.

----- 

#### **The first machine** will host the python script.
Connect as a root and download sudo with `apt update && apt-get -y install sudo`.\
Then run the following to add the user into the sudo group `usermod -aG sudo <yourUsername>` and logout the root user.\
Login as `<yourUSername>` and install git with `sudo apt-get -y install git`. We also recommend to install python3-venv with `sudo apt-get -y install python3-venv`.

WARNING : If you're on python 3.7 or lower, this script will not work as psutil installation will fail. A simple solution if you do not want to upgrade your python version in your machine is to first install curl with `sudo apt-get -y install curl` and install pyenv-installer with `sudo curl https://pyenv.run | bash` from [pyenv-installer](https://github.com/pyenv/pyenv-installer). \
You will then need to echo the following to .bashrc and .profile :
```sh
echo export PYENV_ROOT="$HOME/.pyenv" >> ~/.bashrc &&
echo command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH" >> ~/.bashrc &&
echo eval "$(pyenv init -)" >> ~/.bashrc
```
and
```sh
echo export PYENV_ROOT="$HOME/.pyenv" >> ~/.profile &&
echo command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH" >> ~/.profile &&
echo eval "$(pyenv init -)" >> ~/.profile
```

Once you have access to pyenv in your terminal, install python 3.10 with `sudo pyenv install 3.10`, this will download a tar of the specified version.
- If you're running into the error : **"no acceptable C compiler found in $PATH"**, just run `sudo apt-get -y install build-essential` then rerun the command.
- If you're running into an error where the last line is **"[Makefile:1280: install] Error 1"** and a bunch of array index referencing pip and numpy, try pasting the log file as follow : `cat /tmp/python-build.<number>.<number>.log` from the error log. If you can find "no module named zlib" in the log, run the following command `sudo apt-get -y install zlib1g zlib1g-dev libssl-dev libbz2-dev libsqlite3-dev` as stated in the wiki of [pyenv](https://github.com/pyenv/pyenv/wiki/Common-build-problems#build-failed-error-the-python-zlib-extension-was-not-compiled-missing-the-zlib), then rerun the command.


At this point you have installed python 3.10 with pyenv.
You can check your installed version of python with `ls ~/.pyenv/versions/`
(more information about pyenv during the installation)

----

#### **The second machine** will host influxDB, Prometheus and Grafana

Connect as a root and download sudo with `apt update && apt-get -y install sudo`.\
Then run the following to add the user into the sudo group `usermod -aG sudo <yourUsername>` and logout the root user.\
Login as `<yourUSername>` and install wget and curl as follow `sudo apt-get -y install wget curl`.

#### **Install Prometheus**
```sh
sudo mkdir /etc/prometheus
sudo mkdir /var/lib/prometheus
sudo chown -R <user>:sudo /etc/prometheus
sudo chown -R <user>:sudo /var/lib/prometheus

sudo apt-get update
mkdir -p /tmp/prometheus && cd /tmp/prometheus
curl -s https://api.github.com/repos/prometheus/prometheus/releases/latest%7Cgrep browser_download_url|grep linux-amd64|cut -d '"' -f 4|wget -qi -
```
Once you did that, you can start the daemon service and delete the temp folder.
```sh
sudo mv prometheus promtool /usr/local/bin
sudo mv prometheus.yml  /etc/prometheus/prometheus.yml
sudo mv consoles/ console_libraries/ /etc/prometheus/

cd ~/
rm -rf /tmp/prometheus
```

#### **Install InfluxDb**
```sh
mkdir -p /tmp/influxdb && cd /tmp/influxdb
wget https://dl.influxdata.com/influxdb/releases/influxdb2-2.7.0-amd64.deb
sudo dpkg -i influxdb2-2.7.0-amd64.deb

mkdir -p /tmp/influxdb-cli && cd /tmp/influxdb-cli
wget https://dl.influxdata.com/influxdb/releases/influxdb2-client-2.7.0-linux-amd64.tar.gz
tar xvzf influxdb2-client-2.7.0-linux-amd64.tar.gz
sudo cp influx /usr/local/bin
```
Once you did that, you can start the daemon service and delete the temp folders.
```sh
sudo systemctl daemon-reload
sudo service influxdb start
sudo service influxdb status

cd ~/
rm -rf /tmp/influxdb
rm -rf /tmp/influxdb-cli
```
To register an influxDb default config you can also run the following.
```sh
influx config create --config-name default \
    --host-url "http://<ipaddr>:8086/" \
    --org "<org>" \
    --token "<token>" \
    --active
```

#### **Install Grafana**
```sh
sudo apt-get install -y apt-transport-https
sudo apt-get install -y software-properties-common wget
sudo wget -q -O /usr/share/keyrings/grafana.key https://apt.grafana.com/gpg.key
echo "deb [signed-by=/usr/share/keyrings/grafana.key] https://apt.grafana.com/ stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
sudo apt-get update
sudo apt-get install grafana
```
Once you did that, you can start the daemon service.
```sh
sudo systemctl daemon-reload
sudo systemctl start grafana-server
sudo systemctl status grafana-server
sudo systemctl enable grafana-server.service
```

In order to access them on your navigator, you will need to retrieve the private ip of your VM.
- **Grafana**: `http://<ipaddr>:3000`
- **Prometheus**: `http://<ipaddr>:9090`
- **InfluxDB**: `http://<ipaddr>:8086`

Influx will ask you to create a user.\
Grafana will ask you to enter admin and admin, then set your own password.

----

### Installation

To install and setup the script, follow the instruction :

1. Clone the repo
   ```sh
   git clone https://github.com/Maghwyn/supervision-service
   ```
2. Open the folder supervision-service
   ```sh
   cd supervision-service/
   ```
3. Setup your local folder python version (skip if pyenv is not installed)
   ```sh
   pyenv local 3.10.X
   ```
   <sub><sup>**X being the version you installed**</sub></sup>
4. Create your virtualenv
   ```sh
   python3 -m venv .venv
   ```
5. Activate your virtualenv
   ```sh
   source .venv/bin/activate
   ```
6. Install the python library
   ```sh
   .venv/bin/pip3 install -r requirements
   ```
7. Create your environment
    ```sh
    nano .env
    ```
8. Setup your environment
    ```md
    AGENT_NAME="YourAgentName"
    TSDB_NAME="influx" # influx | prometheus
    ENVIRONMENT="dev" # dev | production
    INFLUX_BUCKET="yourBucketName"
    INFLUX_ORG="yourOrgName"
    INFLUX_TOKEN="yourToken"
    INFLUX_URL="http://ipaddr:8086"
    ```
9. (optional) Create a daemon
   ```js
   bash linux_daemon_installer.sh
   ```

----

### Additional information

**ENVIRONMENT="dev"** will write the metrics of psutil in the logs.txt.\
**ENVIRONMENT="production"** will send the metrics to influx or prometheus.



<!-- USAGE EXAMPLES -->
## Usage

To run the script, do the following :
```sh
.venv/bin/python3 main.py
```

If you're using the daemon instead and did not accept the script to launch the daemon for you, do the following in order:

```sh
sudo systemctl daemon-reload
sudo systemctl start vitals.service
sudo systemctl status vitals.service
```


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[Python]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/