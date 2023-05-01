# CINtofome

Projeto da disciplina de Infraestrutura de comunicação - 2022.2 - CIN UFPE,
onde usamos o protocolo UDP para realizar envios e recebimentos de arquivos, usando o canal de
transmissão confiável rdt3.0.

## COMO EXECUTAR

Para a execução do projeto é necessário que o usuário abra dois terminais diferentes, ambos na pasta raiz do projeto. Com isso o usuário deve utilizar os seguintes comandos para executar:

```python "Entrega 2/receiver.py"```

```python "Entrega 2/sender.py"```

É importante que os arquivos sejam executados nessa ordem, pois o ```receiver``` deve esperar o envio do arquivo pelo ```sender```. Normalmente o ```sender``` irá se fechar sozinho após sua execução, porem o ```receiver``` ficará aberto indefinidamente, para fecha-ló é necessário abrir o gerenciador de tarefas do computador e finalizar o processo chamado python (seguido da sua versão), como visto na imagem abaixo.

![Sem título](https://user-images.githubusercontent.com/89427085/229162765-0e90f2dd-bde3-4eda-b243-7ba8b92fe898.png)

## GRUPO

- Fabrício Aranha Ferreira (faf3)
- Igor Raphael Alves Varela (irav)
- Caio Roberto da Silva Verçosa (crsv)
- Antonio Alvarez Ferraz (aaf3)
- Paulo Henrique Jaguaribe Carneiro (phjc)
