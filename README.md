# PokéMarket

Monitoramento de preços e vendas reais de cartas Pokémon TCG, com foco inicial em sold listings do eBay. MVP funcional: busca carta → resolve carta correta (card matcher) → busca vendas reais → mostra última venda, estatísticas (média/mediana/min/max) e gráfico de evolução de preço.

## Arquitetura

```
Frontend (Vue 3 + Vite + Tailwind)
        ↓ /api
Backend (FastAPI)
        ↓
Providers (cards / sales) ──→ PostgreSQL (cache)
```

O frontend nunca chama providers externos diretamente — tudo passa pelo FastAPI, que cacheia no Postgres (TTL de 6h por carta, ver `app/repositories/tracked_card_repo.py`).

## Stack

- **Frontend**: Vue 3, Vite, TypeScript, Tailwind CSS v4, ECharts
- **Backend**: Python, FastAPI, SQLAlchemy (async), Alembic
- **Banco**: PostgreSQL
- **ETL**: scripts standalone em `backend/etl/`

## Providers

| Papel | Provider | Status |
|---|---|---|
| Catálogo de cartas + imagens | [pokemontcg.io](https://docs.pokemontcg.io) v2 | Funcional sem key (rate limit menor); recomendado configurar `POKEMONTCG_API_KEY` |
| Vendas (principal) | [thecardapi.com](https://www.thecardapi.com) — Sales API | Requer `THE_CARD_API_KEY` (free tier: 5.000 linhas/dia, 3 dias de histórico) |
| Vendas (fallback) | [trawl.dev](https://trawl.dev) — eBay sold listings | Requer `TRAWL_API_KEY`; API genérica de eBay (não específica de Pokémon), usada só quando o provider principal não retorna resultados |

Sem as chaves de vendas configuradas, a aplicação funciona normalmente para busca/catálogo de cartas, mas `/api/cards/{id}/sales` retorna lista vazia (nenhum dado é inventado).

## Configurar API Keys

1. `POKEMONTCG_API_KEY`: signup grátis em https://dev.pokemontcg.io
2. `THE_CARD_API_KEY`: signup grátis (sem cartão) em https://www.thecardapi.com
3. `TRAWL_API_KEY`: signup em https://trawl.dev

Copie `backend/.env.example` para `backend/.env` e preencha.

## Rodar o backend

```bash
cd backend
py -m venv .venv
.venv/Scripts/pip install -r requirements.txt
cp .env.example .env   # preencha DATABASE_URL e as API keys
.venv/Scripts/python -m alembic upgrade head
.venv/Scripts/python -m uvicorn app.main:app --reload --port 8001
```

## Rodar o frontend

```bash
cd frontend
npm install
npm run dev
```

Em dev, o Vite faz proxy de `/api` para `http://127.0.0.1:8001` (ver `vite.config.ts`). Em produção, defina `VITE_API_BASE` apontando para a URL do backend.

## PostgreSQL

Qualquer Postgres 14+ serve. Localmente, via Docker:

```bash
docker run -d --name pokemarket-postgres \
  -e POSTGRES_USER=pokemarket -e POSTGRES_PASSWORD=pokemarket -e POSTGRES_DB=pokemarket \
  -p 5452:5432 postgres:16-alpine
```

`DATABASE_URL=postgresql+asyncpg://pokemarket:pokemarket@localhost:5452/pokemarket`

Preparado para Supabase/Neon em produção (só trocar `DATABASE_URL`).

## Rodar o ETL

```bash
cd backend
.venv/Scripts/python -m etl.fetch_sales     # busca vendas para cartas em tracked_cards (active=true)
.venv/Scripts/python -m etl.update_prices   # recalcula snapshots de preço
```

Para monitorar uma carta, insira uma linha em `tracked_cards` apontando pro `card_id` desejado.

## GitHub Actions

`.github/workflows/update-sales.yml` roda o ETL diariamente (06:00 UTC). Configure os secrets `DATABASE_URL`, `THE_CARD_API_KEY`, `TRAWL_API_KEY` no repositório.

## Limitações conhecidas

- `thecardapi.com` free tier: só 3 dias de histórico e 5.000 linhas/dia — suficiente para o MVP, não para análise histórica profunda.
- `pokemontcg.io` sem API key ocasionalmente retorna 502 sob carga (há retry automático de 3 tentativas).
- Card matcher é determinístico (scoring por número/set/nome/variante), não ML — pode exigir ajuste de pesos para sets ambíguos.
- Sem autenticação, portfolio, alertas ou scraping direto do eBay — fora de escopo do MVP (ver spec original).
