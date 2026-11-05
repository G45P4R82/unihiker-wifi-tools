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
