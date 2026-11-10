#!/usr/bin/env python3
"""Gera os cards de estatísticas do README do perfil (assets/stats-*.svg e assets/langs-*.svg).

Só usa a biblioteca padrão. Roda no GitHub Actions com o GITHUB_TOKEN do próprio
workflow; para incluir repositórios privados no card de linguagens, crie o secret
PROFILE_TOKEN com um token pessoal de leitura (veja .github/workflows/profile-cards.yml).

Uso:
    python scripts/build_cards.py            # consulta a API e grava em assets/
    python scripts/build_cards.py --demo     # dados fictícios em assets/demo/, para testar o layout
    python scripts/build_cards.py --pending  # cards de espera, usados antes da primeira execução

Para rodar na sua máquina, defina GITHUB_TOKEN antes. No PowerShell, com o GitHub CLI:
    $env:GITHUB_TOKEN = gh auth token
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import date, datetime, timedelta, timezone
from html import escape
from pathlib import Path

# ----------------------------------------------------------------------------- configuração
LOGIN = os.environ.get("GH_LOGIN") or os.environ.get("GITHUB_REPOSITORY_OWNER") or "willamylp"
TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN") or ""
OUT_DIR = Path(__file__).resolve().parent.parent / "assets"

TOP_LANGUAGES = 5
IGNORE_LANGUAGES: set[str] = set()  # ex.: {"HTML", "CSS"} para tirar marcação do ranking
IGNORE_REPOS: set[str] = set()      # nomes de repositórios que não devem contar

API_URL = "https://api.github.com/graphql"
MONTHS = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif"

# Cores por tema. O amarelo é o mesmo do banner; as rampas do mapa de calor foram
# validadas (um matiz, luminosidade monotônica, passo mais claro >= 2:1 sobre o fundo).
THEMES = {
    "light": {
        "ink": "#1F2328",
        "muted": "#59636E",
        "frame": "#D1D9E0",
        "empty": "#EBEDF0",
        "heat": ["#D9AA22", "#B8860B", "#8C6400", "#5A3F00"],
        "bar": "#B8860B",
    },
    "dark": {
        "ink": "#F0F6FC",
        "muted": "#9198A1",
        "frame": "#3D444D",
        "empty": "#1F242C",
        "heat": ["#5C4410", "#94700F", "#CC9C12", "#F4C430"],
        "bar": "#F4C430",
    },
}

CARD_W, CARD_H, MARGIN = 400, 240, 6  # a margem transparente vira o espaçamento entre os cards
PAD = 22


# ----------------------------------------------------------------------------- API
QUERY_PROFILE = """
query($login: String!, $after: String) {
  user(login: $login) {
    createdAt
    followers { totalCount }
    publicRepos: repositories(privacy: PUBLIC, ownerAffiliations: OWNER) { totalCount }
    repositories(first: 100, after: $after, ownerAffiliations: OWNER, isFork: false) {
      pageInfo { hasNextPage endCursor }
      nodes {
        name
        isPrivate
        stargazerCount
        languages(first: 12, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name } }
        }
      }
    }
  }
}
"""

CALENDAR_FIELDS = """
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
"""

# Sem argumentos, a API devolve os últimos 12 meses terminando hoje.
QUERY_LAST_YEAR = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {%s}
  }
}
""" % CALENDAR_FIELDS

QUERY_YEAR = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {%s}
  }
}
""" % CALENDAR_FIELDS


def graphql(query: str, variables: dict) -> dict:
    """Executa uma consulta GraphQL, com novas tentativas em falhas temporárias."""
    if not TOKEN:
        raise SystemExit("Defina GITHUB_TOKEN (ou GH_TOKEN) para consultar a API do GitHub.")
    payload = json.dumps({"query": query, "variables": variables}).encode()
    request = urllib.request.Request(
        API_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
            "User-Agent": f"{LOGIN}-profile-cards",
        },
    )
    last_error: Exception | None = None
    for attempt in range(4):
        if attempt:
            time.sleep(2 ** attempt)
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                body = json.load(response)
        except urllib.error.HTTPError as error:
            last_error = error
            if error.code in (401, 403, 404):
                detail = error.read().decode(errors="replace")[:300]
                raise SystemExit(f"A API recusou a consulta ({error.code}): {detail}")
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
            last_error = error
        else:
            if body.get("errors"):
                last_error = RuntimeError(json.dumps(body["errors"])[:400])
            elif not (body.get("data") or {}).get("user"):
                raise SystemExit(f"Usuário '{LOGIN}' não encontrado pela API.")
            else:
                return body["data"]["user"]
    raise SystemExit(f"A API do GitHub não respondeu após 4 tentativas: {last_error}")


def fetch() -> dict:
    """Busca tudo o que os cards mostram e devolve um dicionário simples."""
    repos: list[dict] = []
    cursor = None
    while True:
        user = graphql(QUERY_PROFILE, {"login": LOGIN, "after": cursor})
        page = user["repositories"]
        repos.extend(node for node in page["nodes"] if node)
        if not page["pageInfo"]["hasNextPage"]:
            break
        cursor = page["pageInfo"]["endCursor"]

    now = datetime.now(timezone.utc)
    created_year = int(user["createdAt"][:4])

    last_year = graphql(QUERY_LAST_YEAR, {"login": LOGIN})
    calendar = last_year["contributionsCollection"]["contributionCalendar"]
    weeks = [[(d["date"], d["contributionCount"]) for d in week["contributionDays"]] for week in calendar["weeks"]]

    # Histórico completo, ano a ano (a API aceita no máximo um ano por consulta).
    history: dict[str, int] = {}
    all_time = 0
    for year in range(created_year, now.year + 1):
        end = now if year == now.year else datetime(year, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
        data = graphql(
            QUERY_YEAR,
            {"login": LOGIN, "from": f"{year}-01-01T00:00:00Z", "to": end.strftime("%Y-%m-%dT%H:%M:%SZ")},
        )
        year_calendar = data["contributionsCollection"]["contributionCalendar"]
        all_time += year_calendar["totalContributions"]
        for week in year_calendar["weeks"]:
            for day in week["contributionDays"]:
                history[day["date"]] = day["contributionCount"]
    for week in weeks:
        for day, count in week:
            history[day] = count

    counted = [repo for repo in repos if repo["name"] not in IGNORE_REPOS]
    languages: dict[str, int] = {}
    for repo in counted:
        for edge in (repo.get("languages") or {}).get("edges") or []:
            name = edge["node"]["name"]
            if name not in IGNORE_LANGUAGES:
                languages[name] = languages.get(name, 0) + edge["size"]

    current, longest = streaks(history)
    return {
        "weeks": weeks,
        "year_total": calendar["totalContributions"],
        "all_time": all_time,
        "since": created_year,
        "current_streak": current,
        "longest_streak": longest,
        "languages": languages,
        "has_private": any(repo["isPrivate"] for repo in counted),
        "public_repos": user["publicRepos"]["totalCount"],
        "stars": sum(repo["stargazerCount"] for repo in counted if not repo["isPrivate"]),
        "followers": user["followers"]["totalCount"],
    }


def streaks(history: dict[str, int]) -> tuple[int, int]:
    """Sequência atual e maior sequência de dias com contribuição.

    O dia de hoje sem contribuição ainda não quebra a sequência atual.
    """
    if not history:
        return 0, 0
    days = sorted(history)
    start, end = date.fromisoformat(days[0]), date.fromisoformat(days[-1])
    longest = run = 0
    cursor = start
    while cursor <= end:
        run = run + 1 if history.get(cursor.isoformat(), 0) > 0 else 0
        longest = max(longest, run)
        cursor += timedelta(days=1)

    cursor = end if history.get(end.isoformat(), 0) > 0 else end - timedelta(days=1)
    current = 0
    while cursor >= start and history.get(cursor.isoformat(), 0) > 0:
        current += 1
        cursor -= timedelta(days=1)
    return current, longest


# ----------------------------------------------------------------------------- desenho
def number(value: int) -> str:
    """Inteiro com separador de milhar brasileiro: 12345 -> 12.345."""
    return f"{value:,}".replace(",", ".")


def plural(value: int, singular: str, plural_form: str) -> str:
    return f"{number(value)} {singular if value == 1 else plural_form}"


def text(x: float, y: float, content: str, size: float, fill: str, weight: int = 400, anchor: str = "start") -> str:
    return (
        f'<text x="{x:g}" y="{y:g}" font-size="{size:g}" font-weight="{weight}" fill="{fill}" '
        f'text-anchor="{anchor}">{escape(content)}</text>'
    )


def card(theme: dict, title: str, description: str, body: str) -> str:
    """Moldura comum aos cards: borda fina, título e o conteúdo recebido."""
    width, height = CARD_W + 2 * MARGIN, CARD_H + 2 * MARGIN
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" '
        f'role="img" aria-labelledby="t d" font-family="{FONT}">'
        f'<title id="t">{escape(title)}</title><desc id="d">{escape(description)}</desc>'
        f'<g transform="translate({MARGIN} {MARGIN})">'
        f'<rect x="0.5" y="0.5" width="{CARD_W - 1}" height="{CARD_H - 1}" rx="12" fill="none" stroke="{theme["frame"]}"/>'
        f'{text(PAD, 36, title, 13.5, theme["muted"])}'
        f"{body}</g></svg>\n"
    )


def tiles(theme: dict, items: list[tuple[str, str]]) -> str:
    """Linha de três números com rótulo, alinhada ao rodapé do card."""
    column = (CARD_W - 2 * PAD) / len(items)
    parts = []
    for index, (label, value) in enumerate(items):
        x = PAD + index * column
        parts.append(text(x, 196, label, 11.5, theme["muted"]))
        parts.append(text(x, 218, value, 17, theme["ink"], weight=600))
    return "".join(parts)


def heat_levels(weeks: list[list[tuple[str, int]]]) -> list[int]:
    """Limiares dos quatro níveis de cor, pelos quartis dos dias com contribuição."""
    counts = sorted(count for week in weeks for _, count in week if count > 0)
    if not counts:
        return [1, 2, 3, 4]
    return [counts[min(len(counts) - 1, int(len(counts) * q))] for q in (0.25, 0.5, 0.75)]


def month_label(iso_day: str) -> str:
    return f"{MONTHS[int(iso_day[5:7]) - 1]} {iso_day[:4]}"


def render_activity(theme: dict, data: dict) -> str:
    weeks = data["weeks"][-53:]
    thresholds = heat_levels(weeks)
    pitch = (CARD_W - 2 * PAD) / 53
    cell = pitch - 1.3
    top = 108
    cells = []
    for column, week in enumerate(weeks):
        for day, count in week:
            row = (date.fromisoformat(day).weekday() + 1) % 7  # domingo no topo, como no GitHub
            level = 0 if count == 0 else 1 + sum(count > limit for limit in thresholds)
            fill = theme["empty"] if level == 0 else theme["heat"][min(level, 4) - 1]
            cells.append(
                f'<rect x="{PAD + column * pitch:.2f}" y="{top + row * pitch:.2f}" '
                f'width="{cell:.2f}" height="{cell:.2f}" rx="1.3" fill="{fill}"/>'
            )

    first_day, last_day = weeks[0][0][0], weeks[-1][-1][0]
    axis_y = top + 7 * pitch + 14
    legend_x = CARD_W / 2 - 2.5 * 11
    legend = "".join(
        f'<rect x="{legend_x + index * 11:.1f}" y="{axis_y - 8.5:.1f}" width="8.5" height="8.5" rx="1.6" fill="{fill}"/>'
        for index, fill in enumerate([theme["empty"], *theme["heat"]])
    )
    body = (
        text(PAD, 88, number(data["year_total"]), 48, theme["ink"], weight=600)
        + "".join(cells)
        + text(PAD, axis_y, month_label(first_day), 10.5, theme["muted"])
        + text(CARD_W - PAD, axis_y, month_label(last_day), 10.5, theme["muted"], anchor="end")
        + text(legend_x - 6, axis_y, "menos", 10.5, theme["muted"], anchor="end")
        + legend
        + text(legend_x + 5 * 11 + 4, axis_y, "mais", 10.5, theme["muted"])
        + tiles(
            theme,
            [
                ("Sequência atual", plural(data["current_streak"], "dia", "dias")),
                ("Maior sequência", plural(data["longest_streak"], "dia", "dias")),
                (f"Total desde {data['since']}", number(data["all_time"])),
            ],
        )
    )
    description = (
        f"{number(data['year_total'])} contribuições entre {month_label(first_day)} e {month_label(last_day)}. "
        f"Sequência atual de {plural(data['current_streak'], 'dia', 'dias')}, "
        f"maior sequência de {plural(data['longest_streak'], 'dia', 'dias')} "
        f"e {number(data['all_time'])} contribuições desde {data['since']}."
    )
    return card(theme, "Contribuições nos últimos 12 meses", description, body)


def render_languages(theme: dict, data: dict) -> str:
    total = sum(data["languages"].values())
    ranked = sorted(data["languages"].items(), key=lambda item: item[1], reverse=True)[:TOP_LANGUAGES]
    shares = [(name, size / total * 100) for name, size in ranked] if total else []
    largest = max((share for _, share in shares), default=0) or 1

    label_x, bar_x, bar_max = PAD, PAD + 122, 176
    rows = []
    for index, (name, share) in enumerate(shares):
        y = 66 + index * 24
        label = name if len(name) <= 17 else name[:16] + "…"
        width = max(bar_max * share / largest, 3)
        value = f"{share:.1f}".replace(".", ",") + "%"
        rows.append(text(label_x, y + 4.5, label, 13, theme["ink"]))
        # barra com a base reta e a ponta de dados arredondada
        rows.append(
            f'<path d="M{bar_x} {y - 5}h{max(width - 4, 0):.1f}a4 4 0 0 1 4 4v2a4 4 0 0 1 -4 4h-{max(width - 4, 0):.1f}z" '
            f'fill="{theme["bar"]}"/>'
        )
        rows.append(text(bar_x + width + 8, y + 4.5, value, 12.5, theme["muted"]))
    if not rows:
        rows.append(text(PAD, 100, "Nenhuma linguagem detectada.", 13, theme["muted"]))

    scope = "meus repositórios" if data["has_private"] else "repositórios públicos"
    body = "".join(rows) + tiles(
        theme,
        [
            ("Repos públicos", number(data["public_repos"])),
            ("Estrelas", number(data["stars"])),
            ("Seguidores", number(data["followers"])),
        ],
    )
    listing = ", ".join(f"{name} {share:.1f}%".replace(".", ",") for name, share in shares)
    description = (
        f"Linguagens por volume de código: {listing or 'sem dados'}. "
        f"{number(data['public_repos'])} repositórios públicos, {number(data['stars'])} estrelas "
        f"e {number(data['followers'])} seguidores."
    )
    return card(theme, f"Linguagens nos {scope}", description, body)


def render_pending(theme: dict, title: str) -> str:
    body = (
        text(PAD, 118, "Este card é gerado pelo workflow", 14, theme["ink"])
        + text(PAD, 140, "“Atualizar cards do perfil”, no primeiro push.", 14, theme["ink"])
        + text(PAD, 176, "Depois disso, atualiza sozinho todos os dias.", 12.5, theme["muted"])
    )
    return card(theme, title, "Card ainda não gerado: aguardando a primeira execução do workflow.", body)


# ----------------------------------------------------------------------------- dados de demonstração
def demo_data() -> dict:
    """Dados fictícios e determinísticos, só para conferir o layout."""
    import random

    rnd = random.Random(42)
    today = date(2026, 11, 9)
    start = today - timedelta(days=364 + (today.weekday() + 1) % 7)
    weeks, week, history = [], [], {}
    cursor = start
    while cursor <= today:
        busy = cursor.weekday() < 5
        count = max(0, int(rnd.gauss(5 if busy else 1, 4))) if rnd.random() < (0.82 if busy else 0.35) else 0
        week.append((cursor.isoformat(), count))
        history[cursor.isoformat()] = count
        if len(week) == 7:
            weeks.append(week)
            week = []
        cursor += timedelta(days=1)
    if week:
        weeks.append(week)
    current, longest = streaks(history)
    return {
        "weeks": weeks,
        "year_total": sum(history.values()),
        "all_time": 6312,
        "since": 2015,
        "current_streak": current,
        "longest_streak": longest,
        "languages": {"Python": 612_000, "TypeScript": 284_000, "HTML": 131_000, "JavaScript": 58_000, "CSS": 44_000, "Shell": 9_000},
        "has_private": False,
        "public_repos": 17,
        "stars": 58,
        "followers": 58,
    }


# ----------------------------------------------------------------------------- execução
def write(path: Path, content: str) -> bool:
    """Grava só quando o conteúdo mudou, para o workflow não criar commits vazios."""
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--demo", action="store_true", help="usa dados fictícios e grava em assets/demo/")
    mode.add_argument("--pending", action="store_true", help="grava os cards de espera")
    args = parser.parse_args()

    out_dir = OUT_DIR / "demo" if args.demo else OUT_DIR
    data = None if args.pending else (demo_data() if args.demo else fetch())

    changed = []
    for name, theme in THEMES.items():
        if data is None:
            files = {
                f"stats-{name}.svg": render_pending(theme, "Contribuições nos últimos 12 meses"),
                f"langs-{name}.svg": render_pending(theme, "Linguagens nos repositórios públicos"),
            }
        else:
            files = {
                f"stats-{name}.svg": render_activity(theme, data),
                f"langs-{name}.svg": render_languages(theme, data),
            }
        for filename, content in files.items():
            if write(out_dir / filename, content):
                changed.append(filename)

    if data is not None:
        print(
            f"{LOGIN}: {number(data['year_total'])} contribuições em 12 meses, "
            f"sequência atual {data['current_streak']}, maior {data['longest_streak']}, "
            f"{len(data['languages'])} linguagens."
        )
    print("Atualizados: " + (", ".join(changed) if changed else "nenhum (sem mudanças)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
