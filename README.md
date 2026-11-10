<!--
  As imagens que mudam com o tema (claro/escuro) usam URL absoluta dentro de <picture>,
  que é a forma documentada pelo GitHub. "HEAD" aponta sempre para o branch padrão.
-->

<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/willamylp/willamylp/HEAD/assets/banner-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/willamylp/willamylp/HEAD/assets/banner-light.svg">
    <img src="https://raw.githubusercontent.com/willamylp/willamylp/HEAD/assets/banner-light.svg" width="100%" alt="Willamy Domingos. Desenvolvedor full-stack. Django, React e agentes de IA. Rio Grande do Norte, Brasil.">
  </picture>
</div>

<p align="center">
  <a href="https://www.linkedin.com/in/willa-my/"><img src="assets/btn-linkedin.svg" height="40" alt="LinkedIn"></a>
  &nbsp;
  <a href="mailto:willamy.wlp@gmail.com"><img src="assets/btn-email.svg" height="40" alt="E-mail"></a>
</p>

Desenvolvedor full-stack no interior do Rio Grande do Norte, trabalhando remotamente. Construo **SaaS multi-tenant** com Django e React, sistemas para a **saúde pública** e, cada vez mais, software feito junto com **agentes de IA**, da especificação ao deploy.

<details>
<summary><b>Read this in English</b></summary>

<br>

Full-stack developer based in Rio Grande do Norte, in Brazil's Northeast, working remotely. I build **multi-tenant SaaS** with Django and React, software for **public healthcare**, and more and more of it alongside **AI agents**, from the spec to the deploy.

**About**

<img src="assets/ico-formacao.svg" width="24" height="24" align="top" alt="">&nbsp; Bachelor's degree in **Information Systems** from **UFRN**.<br>
<img src="assets/ico-stack.svg" width="24" height="24" align="top" alt="">&nbsp; **Django and DRF** on the backend, **React with TypeScript** on the frontend, **PostgreSQL** for data.<br>
<img src="assets/ico-arquitetura.svg" width="24" height="24" align="top" alt="">&nbsp; **Multi-tenant** architecture (one schema per customer, with django-tenants) and self-managed deploys on **Docker Swarm behind Traefik**.<br>
<img src="assets/ico-energia.svg" width="24" height="24" align="top" alt="">&nbsp; I work in **data engineering** for the energy sector.<br>
<img src="assets/ico-sus.svg" width="24" height="24" align="top" alt="">&nbsp; I also work with the information systems of **SUS**, Brazil's public health system.

**What I build**

<table>
  <thead>
    <tr><td colspan="2"><b>Shared foundation:</b> Django and DRF on the backend, React with TypeScript on the frontend and PostgreSQL for data. Real time over WebSocket and messaging (Celery, RabbitMQ and Redis) where the product calls for it. Deployed on Docker Swarm behind Traefik, with observability on Prometheus, Grafana and Loki.</td></tr>
    <tr><th>Project</th><th>What it is</th></tr>
  </thead>
  <tbody>
    <tr><td><b>Clynus</b></td><td>Hospital management for SUS, Brazil's public health system. The first front is paperless urgent care: reception, risk-classification triage, queues with a call panel, medical care, prescriptions and the medication room, exams, observation beds and discharge, integrated with e-SUS PEC. Inpatient care, billing and pharmacy come next. In progress.</td></tr>
    <tr><td><b>FiscPro</b></td><td>Multi-tenant tax-intelligence SaaS for accounting firms: it tracks tax cross-check notices, SPED filings and registration compliance across the whole client portfolio, in dashboards and reports.</td></tr>
    <tr><td><b>Filanda</b></td><td>Queue and call management for walk-in services: reception checks people in, staff call the next person with one click, and a TV panel announces the name out loud, in real time.</td></tr>
    <tr><td><b>SAPE</b></td><td>Electronic health records for rehabilitation centers (CRE) and psychosocial care centers (CAPS): scheduling, intake, waiting list and SUS billing in BPA and RAAS.</td></tr>
    <tr><td><b>SIGTAP</b></td><td>Lookup for the SUS procedures table: API and web interface with search, filters, links to CID and CBO codes and versioning by reference month, built from the monthly DATASUS packages.</td></tr>
    <tr><td><b>MeuQDC</b></td><td>Drag-and-drop web editor for laying out electrical distribution boards: breakers, RCDs, surge protectors and busbars snap onto the rail, wires redraw themselves on every change and each part is drawn to scale, with a realistic finish. In progress.</td></tr>
  </tbody>
</table>

**AI and agentic development**

I treat agents as part of the team: I write the spec, decide the architecture and review; they execute.

- **Spec-driven development.** My own skills on the agent harness for writing PRDs, building prompts and implementing in phases, with subagents reviewing in parallel and MCP servers connecting the tools. In the editor, Cursor and GitHub Copilot.
- **Autonomous agents.** I work with [Hermes Agent](https://github.com/NousResearch/hermes-agent), the open-source agent from Nous Research with persistent memory and skills, and build my own agents in LangChain, with tool use, orchestration and evals.
- **LLMs inside the product.** Features built on the Anthropic and OpenAI APIs in the systems I develop.

</details>

## Sobre

<!-- Cada item troca o marcador da lista por um ícone de assets/ico-*.svg. -->
<img src="assets/ico-formacao.svg" width="24" height="24" align="top" alt="">&nbsp; Bacharel em **Sistemas de Informação** pela **UFRN**.<br>
<img src="assets/ico-stack.svg" width="24" height="24" align="top" alt="">&nbsp; **Django e DRF** no backend, **React com TypeScript** no frontend, **PostgreSQL** nos dados.<br>
<img src="assets/ico-arquitetura.svg" width="24" height="24" align="top" alt="">&nbsp; Arquitetura **multi-tenant** (um schema por cliente, com django-tenants) e deploy próprio em **Docker Swarm atrás do Traefik**.<br>
<img src="assets/ico-energia.svg" width="24" height="24" align="top" alt="">&nbsp; Atuo com **engenharia de dados** no setor de energia.<br>
<img src="assets/ico-sus.svg" width="24" height="24" align="top" alt="">&nbsp; Também trabalho com os sistemas de informação do **SUS**.

## O que eu construo

<table>
  <thead>
    <tr><td colspan="2"><b>Base em comum:</b> Django e DRF no backend, React com TypeScript no frontend e PostgreSQL nos dados. Tempo real por WebSocket e mensageria (Celery, RabbitMQ e Redis) onde o produto pede. Deploy em Docker Swarm atrás do Traefik, com observabilidade em Prometheus, Grafana e Loki.</td></tr>
    <tr><th>Projeto</th><th>O que é</th></tr>
  </thead>
  <tbody>
    <tr><td><b>Clynus</b></td><td>Gestão hospitalar para o SUS. A primeira frente é o pronto atendimento sem papel: recepção, classificação de risco, filas com painel de chamada, atendimento médico, prescrição e sala de medicação, exames, leitos de observação e alta, integrado ao e-SUS PEC. Internação, faturamento e farmácia vêm a seguir. Em construção.</td></tr>
    <tr><td><b>FiscPro</b></td><td>SaaS multi-tenant de inteligência fiscal para escritórios de contabilidade: acompanha malhas fiscais, entrega de SPEDs e regularidade cadastral de toda a carteira de clientes, em painéis e relatórios.</td></tr>
    <tr><td><b>Filanda</b></td><td>Gestão de filas e chamadas para atendimento presencial: a recepção cadastra, o profissional chama com um clique e o painel da TV anuncia o nome por voz, em tempo real.</td></tr>
    <tr><td><b>SAPE</b></td><td>Prontuário eletrônico para centros de reabilitação (CRE) e de atenção psicossocial (CAPS): agenda, escuta inicial, fila de espera e faturamento SUS em BPA e RAAS.</td></tr>
    <tr><td><b>SIGTAP</b></td><td>Consulta à Tabela de Procedimentos do SUS: API e interface web com busca, filtros, relações com CID e CBO e versionamento por competência, a partir dos pacotes mensais do DATASUS.</td></tr>
    <tr><td><b>MeuQDC</b></td><td>Editor web para montar quadros de distribuição elétrica no arrasta e solta: disjuntores, IDR, DPS e barramentos encaixam no trilho, os fios se redesenham sozinhos a cada mudança e cada peça é desenhada em escala, com acabamento realista. Em construção.</td></tr>
  </tbody>
</table>

## IA e desenvolvimento com agentes

Trato os agentes como parte da equipe: eu especifico, decido a arquitetura e reviso; eles executam.

<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/willamylp/willamylp/HEAD/assets/workflow-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/willamylp/willamylp/HEAD/assets/workflow-light.svg">
    <img src="https://raw.githubusercontent.com/willamylp/willamylp/HEAD/assets/workflow-light.svg" width="100%" alt="Do PRD ao deploy em seis etapas: 1. Descoberta, 2. PRD, 3. Fases, 4. Implementação, 5. Revisão, 6. Deploy. As etapas 4 e 5 são executadas por agentes; as demais, conduzidas por mim.">
  </picture>
</div>

- **Desenvolvimento guiado por especificação.** Skills próprias no harness de agentes para escrever PRDs, montar prompts e implementar em fases, com subagentes revisando em paralelo e servidores MCP conectando as ferramentas. No editor, Cursor e GitHub Copilot.
- **Agentes autônomos.** Trabalho com o [Hermes Agent](https://github.com/NousResearch/hermes-agent), o agente open source da Nous Research com memória persistente e skills, e construo agentes próprios em LangChain, com uso de ferramentas, orquestração e evals.
- **LLM dentro do produto.** Funcionalidades com as APIs da Anthropic e da OpenAI nos sistemas que desenvolvo.

## Stack

<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/willamylp/willamylp/HEAD/assets/stack-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/willamylp/willamylp/HEAD/assets/stack-light.svg">
    <img src="https://raw.githubusercontent.com/willamylp/willamylp/HEAD/assets/stack-light.svg" width="100%" alt="Stack principal: Python, Django, PostgreSQL, React, TypeScript, Docker, GitHub Actions, Traefik, observabilidade e IA.">
  </picture>
</div>

<!-- &nbsp; dentro de um nome composto impede que ele quebre no meio da linha. -->
| Área | Tecnologias |
| --- | --- |
| **Backend&nbsp;e&nbsp;dados** | <code>Python</code> <code>Django</code> <code>Django&nbsp;REST&nbsp;Framework</code> <code>django-tenants</code> <code>Django&nbsp;Channels</code> <code>PostgreSQL</code> <code>PgBouncer</code> <code>MinIO</code> <code>Stripe</code> <code>Flask</code> |
| **Frontend** | <code>TypeScript</code> <code>React</code> <code>Vite</code> <code>Tailwind&nbsp;CSS</code> <code>Bootstrap</code> <code>Django&nbsp;Templates</code> |
| **Infra&nbsp;e&nbsp;deploy** | <code>Docker</code> <code>Docker&nbsp;Swarm</code> <code>Traefik</code> <code>NGINX</code> <code>Gunicorn</code> <code>Uvicorn</code> <code>GitHub&nbsp;Actions</code> <code>Cloudflare</code> <code>AWS</code> |
| **Observabilidade** | <code>Prometheus</code> <code>Grafana</code> <code>Loki</code> <code>Grafana&nbsp;Alloy</code> <code>Sentry</code> |
| **IA&nbsp;e&nbsp;agentes** | <code>Claude&nbsp;Code</code> <code>Cursor</code> <code>GitHub&nbsp;Copilot</code> <code>Hermes&nbsp;Agent</code> <code>LangChain</code> <code>MCP</code> <code>Anthropic&nbsp;API</code> <code>OpenAI&nbsp;API</code> |

## GitHub em números

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/willamylp/willamylp/HEAD/assets/stats-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/willamylp/willamylp/HEAD/assets/stats-light.svg">
    <img src="https://raw.githubusercontent.com/willamylp/willamylp/HEAD/assets/stats-light.svg" width="408" alt="Contribuições nos últimos 12 meses, sequência atual e maior sequência.">
  </picture>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/willamylp/willamylp/HEAD/assets/langs-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/willamylp/willamylp/HEAD/assets/langs-light.svg">
    <img src="https://raw.githubusercontent.com/willamylp/willamylp/HEAD/assets/langs-light.svg" width="408" alt="Linguagens mais usadas, repositórios públicos, estrelas e seguidores.">
  </picture>
</p>

Os dois cards são gerados todo dia por um [workflow deste repositório](.github/workflows/profile-cards.yml), sem serviços de terceiros.

<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/willamylp/willamylp/HEAD/assets/footer-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/willamylp/willamylp/HEAD/assets/footer-light.svg">
    <img src="https://raw.githubusercontent.com/willamylp/willamylp/HEAD/assets/footer-light.svg" width="100%" alt="Obrigado pela visita.">
  </picture>
</div>
