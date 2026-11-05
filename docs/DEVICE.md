# Dispositivo de Desenvolvimento

## Identificação

- Hostname observado: `unihiker`
- SoC: Rockchip RK3308B-S
- Kernel: Linux 4.4.143, arm64
- Distribuição: Debian GNU/Linux 10
- Interface Wi-Fi: `wlan0`
- Driver: `rtl8723ds`
- Gerenciador: NetworkManager

## Serviços existentes relevantes

O dispositivo já executa serviços de interface, telemetria, SSH, Jupyter, Samba e streaming. O WiFi Tools deve evitar portas e processos existentes e não deve substituir o processo do SAM.

## Limitações conhecidas

- Rádio interno somente 2,4 GHz.
- O utilitário `iw` não está instalado no baseline observado.
- Suporte a modo monitor/injeção ainda não foi confirmado.
- Memória disponível é limitada; processos de scan devem ser curtos e canceláveis.

## Regra de implantação

Antes de instalar qualquer pacote ou serviço:

1. Registrar o estado atual.
2. Fazer backup da configuração alterada.
3. Instalar o mínimo necessário.
4. Testar o menu sem modificar a inicialização.
5. Só então considerar um serviço systemd opcional.
