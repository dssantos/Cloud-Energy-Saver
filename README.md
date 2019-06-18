# Cloud Energy Saver - CES
O Cloud Energy Saver (CES) is a host state manager for OpenStack Cloud Computing environments that allows for power management experiments.

This application is able to connect and disconnect Compute hosts Compute on an OpenStack environment. To use this application you must have an environment properly configured with OpenStack. Therefore, it is possible to obtain such an environment through one of the following options:
1. Install OpenStack Pike (only Keystone, Glance, Nova and Horizon services), in Ubuntu 16.04, using [official docs](https://docs.openstack.org/pike/install/), keeping password *123456* for all services (this password may be edited on file [header.py](header.py));
2. Use [ready images](https://mega.nz/#F!TbBmSA4b!YHuaruKoxMUFtyM6OXNsWQ) for Controller and Compute. Controller.vdi is a virtual machine file for VirtualBox and ComputePen.raw is a pendrive image that allows to initialize a full configured Compute node from a USB booting procedure.

## Topology

![Topologia](topologia.png?raw=true)

<!--

```mermaid
graph TD;
A[Controller];
Z(Computador com o CES);
X((Rede 10.0.0.0/24));
B[Compute 1];
C[Compute 2];
D[Compute 3];
E[Compute N];
Z  -. 10.0.0.100 .- X;
subgraph Ambiente OpenStack
A  -- 10.0.0.11 --- X;
X  -- 10.0.0.31 --- B;
X  -- 10.0.0.32 --- C;
X  -- 10.0.0.33 --- D;
X  -- 10.0.0.34 --- E;
end
```
-->

## Requisites
This application can be run on any Linux machine (I used Ubuntu 16.04) that is on the same network as the Controller and the Compute nodes. With the OpenStack environment running, perform the following activities:

### 1. Configure the machine to connect with OpenStack environment
```sh
$ sudo ifconfig [INTERFACE] 10.0.0.100/24 up
```
> Replace [INTERFACE] by your network interface name attached to OpenStack environment.


### 2. Restart network service
```sh
$ sudo service networking restart
```

### 3. Add hosts on file /etc/hosts
```sh
# File /etc/hosts

10.0.0.11	controller
10.0.0.31	compute1
10.0.0.32	compute2
10.0.0.33	compute3
10.0.0.34	compute4
```

### 4. Check host connectivity
```sh
$ ping -4 controller
$ ping -4 compute1
$ ping -4 compute2
$ ping -4 compute3
$ ping -4 compute4
```

### 5. Generate a RSA key (allowing a blank password)
```sh
$ ssh-keygen -t rsa
```

### 6. Copy the RSA key to each Compute node
```sh
$ ssh-copy-id -i ~/.ssh/id_rsa.pub user@compute1
$ ssh-copy-id -i ~/.ssh/id_rsa.pub user@compute2
$ ssh-copy-id -i ~/.ssh/id_rsa.pub user@compute3
$ ssh-copy-id -i ~/.ssh/id_rsa.pub user@compute4
```

### 7. Install the etherwake
```sh
$ sudo apt-get install etherwake
```

### 8. Clone Cloud-Energy-Saver repository
```sh
$ git clone https://github.com/dssantos/Cloud-Energy-Saver.git
```

### 9. Access Cloud-Energy-Saver local directoru
```sh
$ cd Cloud-Energy-Saver
```

### 10. Edit interface name on file [muda_estado.py](muda_estado.py)
```sh
# File muda_estado.py

command = "sudo etherwake -i [INTERFACE] %s" %mac_address

```
> Replace [INTERFACE] by your network interface name attached to OpenStack environment.

### 11. Access the Controller and check if OpenStack environment is running
```sh
$ ssh user@controller '. admin-openrc && openstack compute service list'
```
> You should see something like that:
```sh
+----+------------------+------------+----------+---------+-------+----------------------------+
| ID | Binary           | Host       | Zone     | Status  | State | Updated At                 |
+----+------------------+------------+----------+---------+-------+----------------------------+
|  1 | nova-scheduler   | controller | internal | enabled | up    | 2019-02-27T01:02:53.000000 |
|  2 | nova-consoleauth | controller | internal | enabled | up    | 2019-02-27T01:02:53.000000 |
|  3 | nova-conductor   | controller | internal | enabled | up    | 2019-02-27T01:02:48.000000 |
|  6 | nova-compute     | compute1   | nova     | enabled | up    | 2019-02-27T01:02:50.000000 |
|  7 | nova-compute     | compute2   | nova     | enabled | up    | 2019-02-20T23:57:36.000000 |
|  8 | nova-compute     | compute3   | nova     | enabled | up    | 2019-02-20T23:52:52.000000 |
|  9 | nova-compute     | compute4   | nova     | enabled | up    | 2019-02-20T23:46:50.000000 |
+----+------------------+------------+----------+---------+-------+----------------------------+
```

## Basic commands

### Register hosts
```sh
$ ./ces -r
```
> This command must be run before starting the checking and all Compute hosts must be connected. The command identifies the Compute nodes and their respective MAC addresses by registering them in a local file.

### Start checking
```sh
$ ./ces -v 70 30
```
> In this example, application starts load checking, using 70 as maximum level and 30 as average level.
> MAX e MED are are the percentages of RAM in use on Compute hosts and represent the limits that define when to start hosts (when the environment is above MAX) or to turn off hosts (when the environment is below the MED).

### Initialize VMs to create load on cloud environment
```sh
$ ./ces -i 50
```
> In this example, 50 VMs are initialized one by one and then shut down one by one, continuously.

### Show current status of Compute nodes
```sh
$ ./ces -s
```

### Show help
```sh
$ ./ces -h
```
> It shows application help, describing sintax and related parameters.
