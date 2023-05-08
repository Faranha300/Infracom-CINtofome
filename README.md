# CINtofome

Projeto da disciplina de Infraestrutura de comunicação - 2022.2 - CIN UFPE,
onde usamos o protocolo UDP para realizar uma troca de mensagens em uma lanchonete, usando o canal de transmissão confiável rdt 3.0.

## COMO EXECUTAR

Para a execução do projeto é necessário que o usuário abra dois terminais diferentes, ambos na pasta raiz do projeto. Com isso o usuário deve utilizar os seguintes comandos para executar: (É necessario que o python esteja na versão 3.10 para cima)

```python server.py```

```python client.py```

É importante que os arquivos sejam executados nessa ordem, pois o ```server``` deve esperar o envio da conexão do ```client```. Normalmente o ```client``` irá se fechar sozinho após sua execução, porem o ```server``` ficará aberto indefinidamente, para fecha-lo é necessário abrir o gerenciador de tarefas do computador e finalizar o processo chamado python (seguido da sua versão), como visto na imagem abaixo.

![Sem título](https://user-images.githubusercontent.com/89427085/229162765-0e90f2dd-bde3-4eda-b243-7ba8b92fe898.png)

É importante também que o arquivo ```Table.json``` esteja presente na pastar ```resources``` para que seja possivel do servidor manipular os clientes conectados.

## BIBLIOTECAS USADAS

socket -> É necessário para fazer a conexão entre os servidor e o cliente.

json   -> Faz com que seja possivel salvar o arquivo Table.json.

os     -> Usado para ser possivel de abrir o Table.json no python.

time   -> Usado para pegar a hora e o minuto de quando o servidor enviou a mensagem.

random -> Usado no rdt para saber se houve uma perda de pacotes.

## GRUPO

- Fabrício Aranha Ferreira (faf3)
- Igor Raphael Alves Varela (irav)
- Caio Roberto da Silva Verçosa (crsv)
- Antonio Alvarez Ferraz (aaf3)
- Paulo Henrique Jaguaribe Carneiro (phjc)
