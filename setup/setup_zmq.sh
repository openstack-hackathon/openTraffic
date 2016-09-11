# Basic Server Installs
sudo apt-get clean
sudo apt-get update

sudo apt-get install -y dpkg
sudo dpkg --configure -a &&
sudo apt-get install -y python-setuptools i2c-tools &&
sudo apt-get install -y make autoconf automake &&
sudo apt-get install -y libtool unzip
sudo apt-get install -y build-essential manpages-dev
sudo apt-get install -y pkg-config
sudo apt-get install -y python-dev
sudo apt-get install -y screen

#libzmq
cd /tmp
wget http://pkgs.fedoraproject.org/repo/pkgs/zeromq/zeromq-4.0.5.tar.gz/md5/73c39f5eb01b9d7eaf74a5d899f1d03d/zeromq-4.0.5.tar.gz
tar zxvf zeromq-4.0.5.tar.gz
cd zeromq-4.0.5
./configure
make
sudo make install
sudo ldconfig

#pyzmq
cd /tmp
wget https://pypi.python.org/packages/0d/07/d6f322b6888526b7272850beee7c7aedd51cf38bb6e886da23a04a470ae6/pyzmq-14.5.0.tar.gz#md5=8d3351a8ca2ca2a272a3f96bcb963e41
tar zxvf pyzmq-14.5.0.tar.gz
cd pyzmq-14.5.0
sudo python setup.py configure
sudo python setup.py build
sudo python setup.py install

export LD_LIBRARY_PATH="/usr/local/lib:$LD_LIBRARY_PATH"
echo 'export LD_LIBRARY_PATH="/usr/local/lib:$LD_LIBRARY_PATH"' >> ~/.bashrc

# make dir
mkdir -p ~/opentraffic

# wget files in repo
cd opentraffic
#wget messenger
wget https://raw.githubusercontent.com/csmc88/oshack_opentraffic/master/control_interception.py
wget https://raw.githubusercontent.com/csmc88/oshack_opentraffic/master/courier.py
wget https://raw.githubusercontent.com/csmc88/oshack_opentraffic/master/TrayectoriaCarro.py

if [ $1 == "intersection"]; then
    screen -S intersection_control -dm "python intersection.py -u intersection1 > allout.txt 2>&1"
fi

# if $1 is intersection
    #wget intersection
    #python intersection.py 
# if $1 is car_server
    #wget car
    #python car.py 