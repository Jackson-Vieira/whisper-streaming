# Definição de Requisitos

Este documento estabelece os requisitos para o desenvolvimento do micro serviço responsável pela transcrição Text-to-Speech (TTS) em tempo real da fala dos participantes de videochamadas da plataforma Nadic Meet. O objetivo principal é garantir uma experiência de comunicação eficaz e acessível em diferentes browsers, fornecendo transcrições precisas e oportunas durante as interações.

## Requisitos Funcionais:

1. **Transcrição em Tempo Real:** O sistema deve ser capaz de transcrever a fala dos participantes da videochamada em tempo real, garantindo uma resposta rápida e precisa.
   
2. **Baixo Custo de Operação:** O sistema deve ser otimizado para operar com eficiência em termos de custo, utilizando recursos computacionais de forma econômica e escalável.

## Requisitos de Disponibilidade e Desempenho:

1. **Alta Disponibilidade:** O serviço deve garantir disponibilidade contínua, minimizando o tempo de inatividade e interrupções no fornecimento das transcrições.
   
2. **Boa Taxa de Acertividade:** A precisão das transcrições deve ser elevada, garantindo que o conteúdo seja interpretado corretamente pelos usuários, mesmo em ambientes com diferentes sotaques e condições de áudio.
   
3. **Baixa Latência nas Respostas:** O sistema deve fornecer transcrições em tempo real com uma latência mínima, garantindo uma comunicação fluida e sem atrasos perceptíveis.

## Requisitos Não Funcionais:

1. **Escalabilidade:** O sistema deve ser capaz de lidar com picos de demanda durante videochamadas com um grande número de participantes, escalando horizontalmente conforme necessário.

# Pesquisa de Viabilidade

| Service                 | Pros                                                                                                                                                                | Cons                                                                                                                                                                                | Price                                                                           |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Deepgram Speech-to-Text | Maior precisão, velocidade mais rápida, menor custo, suporte nativo em tempo real, mais flexível, conjunto avançado de recursos, fácil de usar para desenvolvedores | Menos idiomas suportados do que alguns provedores, principalmente os com menor uso                                                                                                  | $0,25/hora de áudio                                                             |
| OpenAI Whisper API      | Precisão razoável                                                                                                                                                   | Trocas entre precisão e velocidade, sem suporte para transcrição em tempo real, sem personalização, modos de falha conhecidos                                                       | Fonte aberta, mas com custos significativos para recursos informáticos e gestão |
| Microsoft Azure         | Precisão razoável, suporte para streaming em tempo real, integração com o ecossistema Azure, segurança e escalabilidade                                             | Caro, velocidades lentas, problemas de latência, preocupações com privacidade, suporte limitado para modelos personalizados, travamento com provedor de nuvem                       | $1.10/hora de áudio                                                             |
| Google Speech-to-Text   | Suporte multilíngue, suporte para streaming em tempo real, integração com o ecossistema Google, segurança e escalabilidade                                          | Baixa precisão geral, caro, velocidades lentas, problemas de latência, preocupações com privacidade, suporte limitado para modelos personalizados, travamento com provedor de nuvem | $1,44/hora de áudio (modelos padrão), $2,16/hora de áudio (modelos aprimorados) |

# Analise dos dados e intersessão com os requsitos

# Análise de Viabilidade e Correspondência de Requisitos

Nesta seção, analisaremos os dados da pesquisa de viabilidade dos serviços de transcrição e os relacionaremos com os requisitos estabelecidos para o serviço de transcrição em tempo real da plataforma Nadic Meet.

## Requisitos Funcionais e Correspondência com os Serviços:

| Requisitos                | Deepgram Speech-to-Text | OpenAI Whisper API | Microsoft Azure | Google Speech-to-Text | AssemblyAI |
| ------------------------- | ----------------------- | ------------------ | --------------- | --------------------- | ---------- |
| Transcrição em Tempo Real | Sim                     | Não*               | Sim             | Sim                   | Sim        |
| Baixo Custo de Operação   | Sim                     | Não*               | Não             | Não                   | Sim        |

## Requisitos de Disponibilidade e Desempenho e Correspondência com os Serviços:

| Requisitos                   | Deepgram Speech-to-Text | OpenAI Whisper API | Microsoft Azure | Google Speech-to-Text | AssemblyAI |
| ---------------------------- | ----------------------- | ------------------ | --------------- | --------------------- | ---------- |
| Alta Disponibilidade         | Sim                     | Não*               | Sim             | Sim                   | Sim        |
| Boa Taxa de Acertividade     | Sim                     | Não*               | Sim             | Sim                   | Sim        |
| Baixa Latência nas Respostas | Sim                     | Não*               | Não             | Não                   | Sim        |

## Requisitos Não Funcionais e Correspondência com os Serviços:

| Requisitos     | Deepgram Speech-to-Text | OpenAI Whisper API | Microsoft Azure | Google Speech-to-Text | AssemblyAI |
| -------------- | ----------------------- | ------------------ | --------------- | --------------------- | ---------- |
| Escalabilidade | Sim                     | Não*               | Sim             | Sim                   | Sim        |

*O OpenAI Whisper API não é recomendado devido à falta de suporte nativo (out of the box) para transcrição em tempo real. Mesmo utilizando outras alternativas como Faster Whisper para diminuir latencia das respostas em 4x, o custo para infraestrutura e manutenção acaba sendo alto.


## Arquitetura planejada whisper live (colocar aqui)
