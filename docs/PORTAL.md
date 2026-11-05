# Portal Cativo Autorizado

## Finalidade

O portal serve para exercícios de conscientização, validação de captive portal e testes contratados em ambiente controlado.

## Comportamento esperado

- O operador define um SSID de laboratório.
- O sistema inicia um AP isolado.
- DHCP fornece endereços somente aos clientes do AP.
- DNS redireciona requisições para o servidor local.
- O cliente vê a página cativa.
- A página identifica claramente a campanha autorizada.
- O participante usa uma conta sintética ou código de treinamento.
- O resultado da campanha é registrado sem guardar senhas reais.

## Dados permitidos

- Horário do evento
- SSID da campanha
- Código de campanha
- Resultado de acesso
- User-Agent e endereço de rede, quando necessário e autorizado

## Dados proibidos por padrão

- Senhas reais
- Tokens de autenticação
- Cookies de sessão
- Dados pessoais além do necessário para o relatório contratado

## Encerramento

Ao parar o portal, o sistema deve encerrar o servidor, desfazer o AP, restaurar a conexão anterior quando possível e informar o resultado ao operador.

## Estado do MVP

O MVP já cria o AP via NetworkManager, inicia o servidor Flask e restaura a conexão anterior ao ser encerrado. O servidor escuta na porta `8081`; durante a validação, o operador acessa `http://10.42.0.1:8081`. O kernel atual não inicializa a tabela NAT do `iptables`, portanto o redirecionamento transparente automático não é suportado pelo firmware atual. A interface informa essa condição e mantém o portal disponível por URL direta.
