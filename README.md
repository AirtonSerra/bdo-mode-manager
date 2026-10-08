# 🎮 BDO Mode Manager

Aplicativo para Windows que configura o **Black Desert Online para usar Vulkan no lugar de DirectX 11**, por meio das DLLs do **DXVK**. Essa camada permite personalizar a renderização das texturas e outras opções gráficas via `dxvk.conf`, incluindo o famoso **modo batata**, que reduz a qualidade visual das texturas para priorizar o desempenho.

O programa automatiza a instalação das DLLs e a troca entre os perfis **Normal** e **Batata**, com uma interface gráfica em Python/Tkinter. A conversão de DirectX para Vulkan é feita pelo DXVK; o aplicativo gerencia seus arquivos e configurações.

## ✨ Funcionalidades

- Localiza automaticamente a instalação do Black Desert Online ou permite selecionar a pasta manualmente.
- Salva o caminho do jogo em `config.json` para reutilizá-lo nas próximas aberturas.
- Aplica o `dxvk.conf` do perfil escolhido e copia as DLLs para a pasta `bin64` do jogo, sem sobrescrever DLLs existentes.
- Identifica o perfil aplicado comparando o hash SHA-256 do `dxvk.conf` instalado com os perfis disponíveis.
- Faz backup temporário do `dxvk.conf` durante a aplicação e tenta reverter as alterações em caso de falha.
- Remove as configurações e as DLLs correspondentes ao usar **Desinstalar**.
- Adapta a interface ao tema claro ou escuro do Windows.

## 🖥️ Requisitos

- Windows.
- Python 3 com Tkinter instalado. O programa utiliza apenas módulos da biblioteca padrão, sem dependências Python externas.
- Placa de vídeo e driver com suporte a Vulkan compatível com as DLLs DXVK incluídas.
- Black Desert Online instalado, com a pasta `bin64` acessível para gravação.

## 📁 Estrutura do projeto

Mantenha o script, as DLLs e os perfis na seguinte organização:

```text
bdo-mode-manager/
├── BDO_Mode_Manager.pyw
├── LICENSE
├── README.md
├── bin64/
│   ├── d3d11.dll
│   └── dxgi.dll
└── Modos de jogo/
    ├── Batata/
    │   └── dxvk.conf
    └── Normal/
        └── dxvk.conf
```

| Arquivo ou pasta | Função |
|---|---|
| `BDO_Mode_Manager.pyw` | Interface e gerenciamento dos arquivos do jogo. |
| `bin64/` | DLLs DXVK copiadas para a pasta `bin64` do jogo. |
| `Modos de jogo/<nome>/dxvk.conf` | Configuração gráfica de cada perfil. |
| `config.json` | Caminho salvo da instalação do jogo; criado ou atualizado pelo aplicativo. |

## ⚠️ Avisos

- O programa altera arquivos dentro da pasta de instalação do jogo (`bin64`). **Use por sua conta e risco.**
- O uso de DLLs de terceiros e a modificação da renderização do cliente **podem infringir as regras ou os termos de uso do Black Desert Online**. Consulte as políticas oficiais da Pearl Abyss antes de utilizar; este projeto não garante que essas alterações sejam permitidas.
- Mantenha uma cópia de segurança da pasta `bin64` original do jogo antes do primeiro uso.
- Feche o jogo antes de aplicar ou remover um perfil.
- O ganho de desempenho do modo batata depende do hardware e das configurações utilizadas.

## ▶️ Como usar

1. Baixe o projeto mantendo a estrutura de pastas acima.
2. Feche o Black Desert Online antes de aplicar ou remover um perfil.
3. Na pasta do projeto, execute:

   ```powershell
   pythonw .\BDO_Mode_Manager.pyw
   ```

   Também é possível abrir o arquivo com duplo clique se a extensão `.pyw` estiver associada ao Python.

4. Aguarde a localização automática do jogo. Caso necessário, clique em **Selecionar** e escolha a pasta de instalação que contém `bin64`.
5. Clique em **Batata** ou **Normal** para aplicar o perfil desejado.
6. Para remover os arquivos do DXVK e a configuração aplicada, clique em **Desinstalar** e confirme.

## 🎨 Perfis disponíveis

| Perfil | Comportamento |
|---|---|
| 🥔 **Batata** | Configura um LOD de texturas elevado (`d3d11.samplerLodBias`), desativa MSAA e ajusta tesselação e filtragem anisotrópica para reduzir a qualidade gráfica. |
| 🖼️ **Normal** | Usa o perfil sem os ajustes específicos de redução de qualidade do modo batata, mantendo as demais configurações DXVK presentes no arquivo. |

**Os dois perfis usam DXVK/Vulkan.** Selecionar **Normal** não remove essa camada nem retorna ao DirectX original. Para remover a camada instalada pelo gerenciador, use **Desinstalar**.

Para personalizar um perfil, edite seu `dxvk.conf` e aplique-o novamente. Para adicionar outro perfil, crie uma subpasta em `Modos de jogo/` com um `dxvk.conf`; ela aparecerá na lista na próxima abertura do aplicativo.

## ⚙️ Como funciona

Ao aplicar um perfil, o programa faz uma cópia temporária do `dxvk.conf` existente, instala a configuração selecionada e copia as DLLs ausentes para a pasta `bin64` do jogo. Se houver falha, tenta remover as DLLs copiadas nessa operação e restaurar a configuração anterior. O backup temporário é removido ao final do processo.

O modo instalado é identificado pelo conteúdo do `dxvk.conf`. A indicação **Nenhum** significa que não foi encontrado um perfil correspondente; ela não verifica se o jogo está usando Vulkan.

A desinstalação remove o `dxvk.conf` e as DLLs com os mesmos nomes das presentes na pasta `bin64` do programa. Ela não restaura um backup permanente da instalação original e pode remover DLLs de mesmo nome que já existiam antes do uso do gerenciador.

## 📜 Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).
