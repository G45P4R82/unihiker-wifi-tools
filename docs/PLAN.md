# Plano de Implementação

## Fase 0: baseline

- Confirmar o processo que inicia o SAM.
- Fazer backup das configurações relevantes.
- Registrar versões do Debian, NetworkManager, Python e driver Wi-Fi.
- Garantir que `target.md` e qualquer segredo estejam fora do repositório.

## Fase 1: aplicativo isolado

- Criar um processo Python próprio para o WiFi Tools.
- Usar a tela Xorg existente sem alterar o aplicativo SAM.
- Implementar navegação touch, mensagens de erro e cancelamento.
- Executar comandos do sistema com lista fixa de argumentos e timeouts.

## Fase 2: recursos de rede básicos

- Status da interface.
- Scan via NetworkManager.
- Conectar/desconectar com confirmação.
- Status detalhado de IP, gateway, DNS, canal e sinal.
- Criação e encerramento de AP.

## Fase 3: diagnóstico autorizado

- Inventário de hosts em uma faixa explicitamente informada.
- Teste de portas limitado e com confirmação.
- SSH, Telnet e TCP com destinos digitados pelo operador.
- Diagnóstico BLE.
- Verificação passiva das capacidades do driver.

## Fase 4: portal cativo

- AP isolado com configuração própria.
- DHCP e DNS locais.
- Servidor HTTP para templates.
- Detecção de requisições de captive portal.
- Código de campanha e contas de teste.
- Registro de eventos sem senhas reais.
- Encerramento limpo e restauração da conexão anterior.

## Fase 5: empacotamento

- Arquivo de configuração separado.
- Serviço systemd opcional, desativado por padrão.
- Comando de rollback.
- Testes de reinicialização.
- Manual de operação e checklist de autorização.

## Critérios de aceite

- O SAM continua iniciando e coletando dados.
- O WiFi Tools não derruba a conexão sem confirmação.
- Um AP de laboratório pode ser criado e encerrado.
- Um cliente autorizado chega ao portal cativo.
- O portal não persiste senhas reais.
- Falhas de dependência aparecem na tela sem travar o sistema.
- Todos os testes de rede têm escopo documentado.
