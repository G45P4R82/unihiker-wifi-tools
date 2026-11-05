# Unihiker WiFi Tools

Aplicativo independente para o Unihiker, com interface local para recursos de diagnóstico e administração Wi-Fi em redes autorizadas.

## Objetivo

Adicionar ao Unihiker um menu próprio de ferramentas Wi-Fi sem substituir o sistema SAM existente. O projeto usa os recursos Linux do dispositivo, em vez de tentar executar diretamente o firmware Bruce, que é destinado a placas ESP32.

## Hardware atual

- Placa: Unihiker baseado em Rockchip RK3308B-S
- Sistema: Debian 10 (Buster), arm64
- Wi-Fi: Realtek `rtl8723ds`
- Rádio: 2,4 GHz
- Interface: tela touch e Xorg
- Memória observada: aproximadamente 424 MiB
- Gerenciamento de rede: NetworkManager / `nmcli`

## Escopo aprovado

### Menu WiFi Tools

- Status da interface Wi-Fi
- Scan de redes próximas
- Conectar e desconectar redes
- Criar Access Point
- Exibir IP, gateway, MAC, canal e sinal
- Inventário de hosts autorizados na rede local
- Cliente SSH e Telnet
- Cliente TCP e listener TCP
- Informações de WireGuard
- Scan Bluetooth Low Energy
- Logs locais de operação

### Portal cativo autorizado

O portal será funcional em um ambiente autorizado, incluindo:

- Access Point local
- DHCP e DNS locais
- Redirecionamento para a página cativa
- Templates HTML locais
- Configuração do SSID
- Página de status da campanha
- Contas sintéticas e códigos de treinamento
- Registro de eventos sem persistir senhas reais

O sistema não deve capturar ou armazenar credenciais reais de terceiros. O modo de treinamento deve informar ao participante que a atividade é autorizada e simulada.

## Fora do escopo inicial

Não serão implementados na primeira versão recursos de interferência ou intrusão, como deauth flood, beacon spam, Karma, ARP poisoning, DHCP starvation, MAC flooding ou Responder.

O suporte a modo monitor e injeção depende do driver e do hardware. O Wi-Fi interno deve ser tratado como estação/AP até que suas capacidades sejam confirmadas em laboratório.

## Estrutura planejada

```text
wifi_tools/
├── app.py                 # Entrada da interface touch
├── ui/                    # Telas e navegação
├── network/               # nmcli, IP, scan e AP
├── portal/                # DHCP, DNS e servidor HTTP cativo
├── diagnostics/           # Driver e capacidades do rádio
├── config/                # Preferências locais
├── templates/             # Páginas cativas autorizadas
└── tests/                 # Testes sem acesso à rede real
```

## Princípios de segurança

1. O WiFi Tools não substitui nem altera o processo do SAM.
2. Operações que alteram a rede exigem confirmação explícita na interface.
3. O portal inicia desativado e deve indicar o SSID e o escopo da campanha.
4. Dados de formulário são sintéticos, mascarados ou descartados por padrão.
5. Credenciais, tokens, IPs de laboratório e arquivos de captura não entram no Git.
6. Testes devem ocorrer somente em redes e dispositivos autorizados.

## Desenvolvimento

O dispositivo-alvo está descrito apenas localmente em `target.md`, que é ignorado pelo Git. Nunca publique esse arquivo nem credenciais de acesso.

Para executar o teste do portal, instale as dependências de `requirements.txt` e rode `python3 -m unittest discover -s tests -v`. A interface pode ser iniciada com `python3 run_wifi_tools.py` em uma sessão gráfica.

O primeiro marco é implementar e testar o menu de status/scan sem interromper o Wi-Fi ou o SAM. O portal cativo será desenvolvido depois, em uma rede de laboratório isolada.

## Status

MVP implementado e validado no Unihiker: menu touch, status, scan, conexão, criação de AP e portal de treinamento autorizado. A integração de DNS para redirecionamento captive ainda está pendente.

## Licença

Este repositório ainda não define uma licença de distribuição. Não reutilize código até que uma licença seja adicionada.
