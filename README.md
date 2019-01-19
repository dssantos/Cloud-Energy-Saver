# Cloud Energy Saver
O Cloud Energy Saver é um gerenciador de estado de hosts em ambientes de Cloud Computing que utilizam a plataforma OpenStack.

Esta aplicação é capaz de ligar e desligar hosts Computes de um ambiente do OpenStack. Para utilizar esta aplicação é preciso ter um ambiente devidamente configurado com o OpenStack. Portanto, é possível obter tal ambiente através de uma das seguintes opções:
1. Instalar o OpenStack Pike (apenas os serviços Keystone, Glance, Nova e Horizon), no Ubuntu 16.04, seguindo a [documentação oficial do OpenStack](https://docs.openstack.org/pike/install/), utilizado sempre as credenciais *user* e *123456* em todos os serviços;
2. Seguir o passo-a-passo para a [Instalação do Openstack no Ubuntu 16.04](http://danilosantos.info/instalacao-do-openstack-pike-no-ubuntu-16-04/), ou;
3. Utilizar a [máquina virtual para o Controller](https://mega.nz/fm/WCZTlaqC) e a [imagem do Compute](https://mega.nz/fm/WCZTlaqC) para clonar em pendrives e inicializar em PCs. Veja as instruções de clonagem no arquivo [LEIAME.txt](https://mega.nz/fm/WCZTlaqC).

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
Esta aplicação pode ser executada em qualquer máquina que esteja na mesma rede do Controller e dos Computes, desde que execute nesta máquina as atividades a seguir:

### 1. Adicione os hosts no arquivo /etc/hosts
```sh
10.0.0.11	controller
10.0.0.31	compute1
10.0.0.32	compute2
10.0.0.33	compute3
10.0.0.34	compute4
```

### 2. Verifique a conectividade com os hosts
```sh
$ ping -4 controller
$ ping -4 compute1
$ ping -4 compute2
$ ping -4 compute3
$ ping -4 compute4
```

### 3. Gere uma chave RSA (deixe a senha em branco)
```sh
$ ssh-keygen -t rsa
```

### 4. Copie a chave para cada compute (repita o comando, substituindo o nome do compute)
```sh
$ ssh-copy-id -i ~/.ssh/id_rsa.pub user@compute1
```

### 5. Instale o etherwake
```sh
$ sudo apt-get install etherwake
```
### 6. Edite o arquivo *muda_estado.py* da aplicação e substitua [INTERFACE] pelo nome da placa de rede que está conectada na mesma rede do Controller e Compute
```sh
$ vim muda_estado.py
```
> Edite [INTERFACE] nesta linha:
> command = "sudo etherwake -i [INTERFACE] %s" %mac_address

## Comandos básicos

### Registrar os hosts
```sh
$ ./ces -r
```
> Lista todos os computes e seus respectivos endereços MAC, registrando-os em um arquivo local.

### Iniciar a verificação
```sh
$ ./ces -v 50 30
```
> Inicia a verificação considerando 50 como patamar máximo e 30 como patamar médio.

### Inicializar VMs para gerar carga no ambiente
```sh
$ ./ces -i 50
```
> 50 VMs são inicializadas uma a uma e depois desligadas uma a uma, continuamente.

### Exibir a ajuda
```sh
$ ./ces -h
```
> Exibe a ajuda do aplicativo descrevendo a sintaxe e os parâmetros
