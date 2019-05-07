# Cloud Energy Saver - CES
O Cloud Energy Saver (CES) é um gerenciador de estado de hosts em ambientes de Cloud Computing que utilizam a plataforma OpenStack.

Esta aplicação é capaz de ligar e desligar hosts Computes de um ambiente do OpenStack. Para utilizar esta aplicação é preciso ter um ambiente devidamente configurado com o OpenStack. Portanto, é possível obter tal ambiente através de uma das opções a seguir:
1. Instalar o OpenStack Pike (apenas os serviços Keystone, Glance, Nova e Horizon), no Ubuntu 16.04, seguindo a [documentação oficial do OpenStack](https://docs.openstack.org/pike/install/), utilizado sempre a senha *123456* em todos os serviços (esta senha pode ser editada no arquivo [header.py](header.py) desta aplicação);
2. Seguir o passo-a-passo para a [Instalação do Openstack no Ubuntu 16.04](http://danilosantos.info/instalacao-do-openstack-pike-no-ubuntu-16-04/), ou;
3. Utilizar [imagens prontas](https://mega.nz/#F!TbBmSA4b!YHuaruKoxMUFtyM6OXNsWQ) do Controller e do Compute. O Controller.vdi é um arquivo de máquina virtual para VirtualBox e o ComputePen.raw é uma imagem que pode ser clonada para pendrives, possibilitando iniciar o sistema operacional via USB. Veja as instruções de clonagem no arquivo [LEIAME.txt](https://mega.nz/#F!TbBmSA4b!YHuaruKoxMUFtyM6OXNsWQ).

## Topologia

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

## Requisitos
Esta aplicação pode ser executada em qualquer máquina com sistema Linux (utilizei o Ubuntu 16.04) que esteja na mesma rede do Controller e dos Computes.
Com o ambiente do OpenStack funcionando, execute as atividades a seguir:

### 1. Configure a máquina para se comunicar com o ambiente do OpenStack
```sh
$ sudo ifconfig [INTERFACE] 10.0.0.100/24 up
```
> Substitua [INTERFACE] pelo nome da sua placa de rede que está conectada ao ambiente do OpenStack.


### 2. Reinicie o serviço de rede
```sh
$ sudo service networking restart
```

### 3. Adicione os hosts no arquivo /etc/hosts (utilize um editor para inserir as linhas a seguir)
```sh
# Arquivo /etc/hosts

10.0.0.11	controller
10.0.0.31	compute1
10.0.0.32	compute2
10.0.0.33	compute3
10.0.0.34	compute4
```

### 4. Verifique a conectividade com os hosts
```sh
$ ping -4 controller
$ ping -4 compute1
$ ping -4 compute2
$ ping -4 compute3
$ ping -4 compute4
```

### 5. Gere uma chave RSA (deixe a senha em branco)
```sh
$ ssh-keygen -t rsa
```

### 6. Copie a chave RSA para cada Compute
```sh
$ ssh-copy-id -i ~/.ssh/id_rsa.pub user@compute1
$ ssh-copy-id -i ~/.ssh/id_rsa.pub user@compute2
$ ssh-copy-id -i ~/.ssh/id_rsa.pub user@compute3
$ ssh-copy-id -i ~/.ssh/id_rsa.pub user@compute4
```

### 7. Instale o etherwake
```sh
$ sudo apt-get install etherwake
```

### 8. Clone o repositório do Cloud-Energy-Saver
```sh
$ git clone https://github.com/dssantos/Cloud-Energy-Saver.git
```

### 9. Acesse a pasta
```sh
$ cd Cloud-Energy-Saver
```

### 10. Edite a placa de rede no arquivo [muda_estado.py](muda_estado.py) desta aplicação (utilize um editor para alterar a linha a seguir)
```sh
# Arquivo muda_estado.py

command = "sudo etherwake -i [INTERFACE] %s" %mac_address

```
> Substitua [INTERFACE] pelo nome da sua placa de rede

### 11. Acesse o Controller e verifique o funcionamento do ambiente do OpenStack
```sh
$ ssh user@controller '. admin-openrc && openstack compute service list'
```
> Deverá retornar algo similar a isto:
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



## Comandos básicos

### Registrar os hosts
```sh
$ ./ces -r
```
> Este comando deve ser executado antes de iniciar a verificação e todos os hosts Compute precisam estar ligados. O comando identifica os Computes e seus respectivos endereços MAC, registrando-os em um arquivo local.

### Iniciar a verificação
```sh
$ ./ces -v 70 30
```
> Neste exemplo, a aplicação inicia a verificação de sobrecarga ou ociosidade, considerando 70 como o limite máximo e 30 como o limite médio.
> MAX e MED são os percentuais de memória RAM em uso nos hosts Compute e representam os limites que definem quando será preciso iniciar hosts (quando o ambiente está acima do MAX) ou desligar hosts (quando o ambiente está abaixo do MED).

### Inicializar VMs para gerar carga no ambiente
```sh
$ ./ces -i 50
```
> Neste exemplo, 50 VMs são inicializadas uma a uma e depois desligadas uma a uma, continuamente.

### Exibir o status atual dos hosts Compute
```sh
$ ./ces -s
```

### Exibir a ajuda
```sh
$ ./ces -h
```
> Exibe a ajuda do aplicativo descrevendo a sintaxe e os parâmetros


## SBRC 2019

O Cloud Energy Saver foi apresentado no Salão de Ferramentas do XXXVII Simpósio Brasileiro de Redes de Computadores e Sistemas Distribuídos (SBRC), realizado em Gramado/RS de 06 a 10 de maio de 2019. O trabalho teve como título: "Um Protótipo para Experimentos de Eficiência Energética em Nuvem Openstack".


## Vídeo

[Cloud Energy Saver - Configuração dos requisitos e demonstração](https://www.youtube.com/watch?v=JgP-1g3kOWI)