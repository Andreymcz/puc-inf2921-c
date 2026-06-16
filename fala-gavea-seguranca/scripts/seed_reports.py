"""Seed script — inserts 250 realistic security reports into app.db.

Idempotent: deletes rows with author_id LIKE 'seed-%' before inserting.
Run from fala-gavea-seguranca/: uv run python scripts/seed_reports.py
"""
from __future__ import annotations

import random
import sys
import uuid
from datetime import UTC, datetime, timedelta
from pathlib import Path

# Allow imports from src/
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fala_gavea_seguranca.domain.entities.security_report import ReportCategory, ReportStatus
from fala_gavea_seguranca.infrastructure.database.models import SecurityReportModel
from fala_gavea_seguranca.infrastructure.database.session import SessionLocal, create_tables

# Gavea bounding box
LAT_MIN, LAT_MAX = -22.990, -22.965
LON_MIN, LON_MAX = -43.245, -43.215

TOTAL_REPORTS = 250

# Distribution derived from the GaveaLab security forum (Jun/2024)
CATEGORY_WEIGHTS: list[tuple[ReportCategory, int]] = [
    (ReportCategory.FURTO_ROUBO, 28),
    (ReportCategory.ILUMINACAO, 22),
    (ReportCategory.TRANSITO, 18),
    (ReportCategory.ESPACO_PUBLICO_INSEGURO, 12),
    (ReportCategory.VANDALISMO, 8),
    (ReportCategory.MORADORES_SITUACAO_RUA, 5),
    (ReportCategory.CONFLITO_SOCIAL, 4),
    (ReportCategory.BARULHO_PERTURBACAO, 2),
    (ReportCategory.OUTRO, 1),
]

TEXTS: dict[ReportCategory, list[str]] = {
    ReportCategory.FURTO_ROUBO: [
        "Fui assaltado na Rua Marques de Sao Vicente ontem a noite, levaram meu celular e carteira.",
        "Assalto a transeunte proximo ao ISAM, o bandido estava armado.",
        "Furto de bicicleta em frente ao supermercado na Gavea, ocorreu por volta das 18h.",
        "Tentativa de roubo na saida do metro Gavea, dois homens abordaram pedestres.",
        "Assalto ao carro na Rua Jardim Botanico, vidro quebrado e pertences levados.",
        "Roubaram minha mochila enquanto eu corria na Lagoa, em plena luz do dia.",
        "Furto em residencia na Rua Sao Clemente durante a tarde, moradores nao estavam em casa.",
        "Dois jovens assaltaram o motorista de aplicativo na Rua General Garzon.",
    ],
    ReportCategory.ILUMINACAO: [
        "Poste apagado na Rua Marques de Sao Vicente ha mais de 15 dias, trecho muito escuro a noite.",
        "A Rua Jornalista Orlando Dantas esta completamente sem iluminacao publica.",
        "Varios postes com lampadas queimadas na Praca Santos Dumont, perigo para pedestres.",
        "Travessa do Corvo sem nenhuma iluminacao a noite, impossivel passar com seguranca.",
        "Poste danificado na altura do numero 200 da Rua Sao Clemente, eletricidade exposta.",
        "Iluminacao intermitente na ciclovia do Jardim Botanico, risco de acidente.",
        "Rua Visconde de Piraja completamente escura apos as 22h, sensacao de inseguranca.",
    ],
    ReportCategory.TRANSITO: [
        "Acidente de transito na esquina da Rua Marques de Sao Vicente com a Rua Jardim Botanico.",
        "Ponto de onibus da linha 584 em local sem calcada, passageiros na pista.",
        "Transito caotico na Rua General San Martin durante a hora do rush, demora de mais de 1h.",
        "Motocicleta em alta velocidade na Av. Epitacio Pessoa, quase atropelou pedestre.",
        "Sinalizacao de transito apagada no cruzamento da Rua Jardim Botanico, risco de colisao.",
        "Onibus nao para no ponto oficial, para antes e passageiros tem que correr.",
        "Calcada esburacada na Rua Faro obriga pedestres a andar na rua, muito perigoso.",
        "Excesso de velocidade constante na Rua Pacheco Leao, precisa de lombadas.",
    ],
    ReportCategory.ESPACO_PUBLICO_INSEGURO: [
        "Ponto de onibus da Gavea sem cobertura e sem iluminacao, mulheres com medo de esperar.",
        "Pracinha do Baixo Gavea com grupinhos suspeitos reunidos toda tarde.",
        "Calcada da Praca Santos Dumont tem buracos profundos, risco de queda para idosos.",
        "Entrada do Parque da Cidade mal iluminada e sem seguranca, frequentadores com medo.",
        "Espaco publico embaixo do viaduto da Lagoa virou abrigo para consumo de drogas.",
        "Praca Vinicius de Moraes com lixo acumulado e pessoas suspeitas a noite.",
        "Passagem da Rua Jardim Botanico ate o canal sem iluminacao e com vegetacao alta.",
    ],
    ReportCategory.VANDALISMO: [
        "Pichacao extensa na fachada do muro da Escola Municipal da Gavea.",
        "Lixeiras publicas da Praca Santos Dumont destruidas, lixo espalhado pela praca.",
        "Banco de praca quebrado na Pracinha do Baixo Gavea, terceiro no ultimo mes.",
        "Camera de seguranca da Prefeitura vandalizada na Rua Marques de Sao Vicente.",
        "Placa de sinalizacao de transito arrancada na Rua Jardim Botanico.",
        "Vidros do ponto de onibus quebrados, risco de corte para passageiros.",
    ],
    ReportCategory.MORADORES_SITUACAO_RUA: [
        "Varios moradores em situacao de rua dormindo na entrada do Parque da Cidade.",
        "Concentracao de pessoas em situacao de rua proximo ao shopping da Gavea, conflitos recorrentes.",
        "Familia em situacao de rua instalada embaixo do viaduto, incluindo criancas.",
        "Pessoas em situacao de rua com comportamento agressivo na Praca Santos Dumont.",
        "Acampamento improvisado na calcada da Rua Marques de Sao Vicente, bloqueando passagem.",
    ],
    ReportCategory.CONFLITO_SOCIAL: [
        "Tensao e barricadas na entrada da comunidade Parque da Cidade desde ontem a tarde.",
        "Tiroteio ouvido na regiao da Rocinha afetando o transito na estrada da Gavea.",
        "Confronto entre grupos rivais na Travessa do Corvo, moradores com medo de sair.",
        "Barricada montada na Rua do Canal impedindo acesso ao bairro desde a madrugada.",
        "Restricao de circulacao na altura da comunidade devido a operacao policial.",
    ],
    ReportCategory.BARULHO_PERTURBACAO: [
        "Baile funk ate 3h da manha com muito barulho na Rua da Gavea, impossivel dormir.",
        "Bar sem alvara funcionando apos meia-noite com som alto na Rua Jardim Botanico.",
        "Festas recorrentes aos finais de semana perturbando moradores da Rua Marques de Sao Vicente.",
        "Motocicletas com escapamento aberto circulando a noite, barulho intenso.",
    ],
    ReportCategory.OUTRO: [
        "Situacao estranha na esquina da Rua Jardim Botanico que nao sei classificar.",
        "Ocorrencia inusitada proximo ao ISAM, nao se encaixa nas outras categorias.",
        "Problema de seguranca de natureza nao identificada na Praca Santos Dumont.",
    ],
}

CATEGORIES = [cat for cat, _ in CATEGORY_WEIGHTS]
WEIGHTS = [w for _, w in CATEGORY_WEIGHTS]


def _random_lat() -> float:
    return random.uniform(LAT_MIN, LAT_MAX)


def _random_lon() -> float:
    return random.uniform(LON_MIN, LON_MAX)


def _random_created_at() -> datetime:
    days_ago = random.randint(0, 90)
    hours_ago = random.randint(0, 23)
    return datetime.now(UTC) - timedelta(days=days_ago, hours=hours_ago)


def seed(n: int = TOTAL_REPORTS) -> None:
    create_tables()
    session = SessionLocal()
    try:
        deleted = session.execute(
            SecurityReportModel.__table__.delete().where(
                SecurityReportModel.author_id.like("seed-%")
            )
        )
        print(f"Removed {deleted.rowcount} existing seed rows.")

        categories = random.choices(CATEGORIES, weights=WEIGHTS, k=n)
        rows = []
        for i, category in enumerate(categories):
            text = random.choice(TEXTS[category])
            rows.append(
                SecurityReportModel(
                    id=str(uuid.uuid4()),
                    text=text,
                    category=category,
                    status=ReportStatus.PENDENTE,
                    author_id=f"seed-{i:04d}",
                    created_at=_random_created_at(),
                    lat=_random_lat(),
                    lon=_random_lon(),
                    territory_name="Gávea",
                    ai_labels=[],
                )
            )

        session.bulk_save_objects(rows)
        session.commit()
        print(f"Inserted {n} seed reports.")
    finally:
        session.close()


if __name__ == "__main__":
    seed()
