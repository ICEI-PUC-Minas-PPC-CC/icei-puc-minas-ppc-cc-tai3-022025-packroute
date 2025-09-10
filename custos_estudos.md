# Estudo de Custos - PackRoute

Este documento detalha os principais custos e despesas do projeto PackRoute, classificados por natureza (fixo/variável) e relação (direto/indireto).  
As estimativas de valor são aproximadas, baseadas em premissas de mercado e referências de serviços SaaS.

---

## 1. Custos Fixos

| Item                                      | Tipo       | Relação   | Estimativa (R$/mês) | Premissas |
|-------------------------------------------|-----------|-----------|---------------------|-----------|
| Hospedagem em nuvem (servidores)          | Fixo      | Direto    | 1.200               | Plano inicial AWS/GCP com escalabilidade básica |
| Banco de dados gerenciado                 | Fixo      | Direto    | 800                 | Inclui backups automáticos e redundância |
| Licenciamento de APIs externas (Mapas, IA)| Fixo      | Direto    | 1.500               | Pacotes médios de consultas/mês |
| Ferramentas de gestão (Notion, GitHub, etc)| Fixo     | Indireto  | 300                 | Assinaturas SaaS |

**Subtotal fixos: R$ 3.800/mês**

---

## 2. Custos Variáveis

| Item                           | Tipo       | Relação   | Estimativa (R$/mês) | Premissas |
|--------------------------------|-----------|-----------|---------------------|-----------|
| Taxas de processamento (cartão/pagamento) | Variável  | Direto    | 2,5% da receita     | Baseado em taxa de intermediadores (Stripe/Pagar.me) |
| Verificação de identidade/usuário | Variável| Direto    | R$ 2 por usuário    | API de autenticação (ex: Onfido/AWS Cognito) |
| Suporte técnico adicional (escala) | Variável | Indireto | R$ 5.000            | Terceirização em horário de pico |
| Marketing de performance (ads) | Variável  | Indireto  | 10% da receita      | Base inicial em campanhas Google Ads / Meta Ads |

**Subtotal variáveis: proporcional à receita**

---

## 3. Custos de Investimento Inicial (Setup)

| Item                         | Tipo       | Relação   | Estimativa (R$) | Premissas |
|------------------------------|-----------|-----------|-----------------|-----------|
| Desenvolvimento do MVP       | Único     | Direto    | -               | Realizado pelos 5 desenvolvedores do time, sem custo financeiro |
| Mentoria / Apoio institucional (PUC) | Único | Indireto | -              | Apoio não oneroso |
| Registro de marca + jurídico | Único     | Indireto  | 5.000           | Custos legais iniciais |

**Subtotal investimento inicial: R$ 5.000**

---

## 4. Resumo

- **Fixos:** ~R$ 3.800/mês  
- **Variáveis:** ~12–15% da receita projetada  
- **Investimento inicial:** ~R$ 5.000  

---

## 5. Premissas

1. Equipe de 5 desenvolvedores internos, sem custo direto no momento.  
2. Estimativas baseadas em preços médios de provedores (AWS, Google Cloud, Mapbox).  

---
