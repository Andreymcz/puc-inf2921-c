"""
Generate a synthetic GáveaLab citizen relatos CSV based on the
Strategic Design For Smart City Lab / Gávea Lab diagnostic (Dec 2023).

Columns: author_id, territory_level, territory_name, text

Territory levels and names derived from the diagnostic segmentation:
  - bairro:  Gávea (whole neighbourhood)
  - asfalto: Gávea Asfalto
  - favela:  Rocinha, Parque da Cidade

Relatos reflect the 14 satisfaction themes and their reported
satisfaction / dissatisfaction percentages per territory type.
"""

import csv, random, pathlib

random.seed(42)

# ------------------------------------------------------------------
# Relatos pool: (territory_level, territory_name, text)
# Themes: Governança, Saneamento Básico, Infraestrutura, Trabalho,
#         Turismo, Tecnologia, Meio Ambiente, Habitação, Educação,
#         Cultura, Saúde, Mobilidade, Segurança, Desenvolvimento Econômico
# ------------------------------------------------------------------

RELATOS = [
    # ── GOVERNANÇA ─────────────────────────────────────────────────────
    ("favela", "Rocinha",           "A governança aqui é um descaso total. A gente não tem representação nenhuma, ninguém escuta a voz da comunidade."),
    ("favela", "Rocinha",           "Já faz anos que pedimos melhorias e nada muda. Os políticos aparecem só em época de eleição."),
    ("favela", "Parque da Cidade",  "Falta de transparência na gestão do bairro. A comunidade deveria participar mais das decisões."),
    ("favela", "Parque da Cidade",  "Nunca vejo nenhum representante aqui dentro. É como se a gente não existisse para a prefeitura."),
    ("asfalto", "Gávea Asfalto",    "A gestão pública deixa a desejar. Falta diálogo com os moradores do bairro nas decisões urbanas."),
    ("asfalto", "Gávea Asfalto",    "Os serviços públicos são razoáveis, mas a participação cidadã poderia ser muito maior."),
    ("asfalto", "Gávea Asfalto",    "Estou satisfeito com a administração comparando com outros bairros do Rio, mas ainda há muita burocracia."),
    ("bairro",  "Gávea",            "A governança precisa melhorar, mas reconheço alguns avanços recentes na comunicação com a comunidade."),

    # ── SANEAMENTO BÁSICO ───────────────────────────────────────────────
    ("favela", "Rocinha",           "Falta esgoto aqui em cima. Quando chove forte, tudo transborda e o cheiro é insuportável."),
    ("favela", "Rocinha",           "A água chega com pressão baixíssima e às vezes vem barrenta. Precisamos de saneamento de verdade."),
    ("favela", "Parque da Cidade",  "Não temos coleta de lixo direito. O caminhão não sobe até aqui e o lixo acumula nas vielas."),
    ("favela", "Parque da Cidade",  "O esgoto corre a céu aberto em alguns trechos. Isso é um problema de saúde pública gravíssimo."),
    ("asfalto", "Gávea Asfalto",    "O saneamento básico aqui funciona bem, água e esgoto sem problemas. Fico satisfeito."),
    ("asfalto", "Gávea Asfalto",    "A coleta de lixo é regular e a rede de esgoto não apresenta problemas na nossa rua."),
    ("bairro",  "Gávea",            "Existe uma desigualdade enorme no saneamento entre a favela e o asfalto. Isso precisa mudar."),

    # ── INVESTIMENTO EM INFRAESTRUTURA ─────────────────────────────────
    ("favela", "Rocinha",           "As ruas aqui dentro estão cheias de buracos e ninguém conserta. A prefeitura não investe na favela."),
    ("favela", "Rocinha",           "Pedimos reforma da praça há dois anos. Nada foi feito. O investimento em infraestrutura é inexistente aqui."),
    ("favela", "Parque da Cidade",  "A iluminação pública é precária. À noite fica muito escuro em vários becos."),
    ("asfalto", "Gávea Asfalto",    "As calçadas e ruas do asfalto estão em bom estado no geral. Mas a manutenção poderia ser mais frequente."),
    ("asfalto", "Gávea Asfalto",    "Falta investimento em espaços públicos de lazer. Praças poderiam ser revitalizadas."),
    ("bairro",  "Gávea",            "O bairro tem boa infraestrutura para quem mora no asfalto, mas as favelas ficam de fora."),

    # ── OPORTUNIDADES DE TRABALHO / DESENVOLVIMENTO ECONÔMICO ──────────
    ("favela", "Rocinha",           "Emprego é o que mais faz falta aqui. Muita gente qualificada desempregada dentro da comunidade."),
    ("favela", "Rocinha",           "Sonho em trabalhar perto de casa, mas as oportunidades estão longe e o transporte é caro."),
    ("favela", "Rocinha",           "Quero abrir um pequeno negócio mas não tenho acesso a crédito nem a capacitação adequada."),
    ("favela", "Parque da Cidade",  "Falta apoio ao empreendedorismo local. Muita gente tem talento mas não tem oportunidade."),
    ("favela", "Parque da Cidade",  "O desemprego aqui é alto. Programas de formação profissional fariam muita diferença."),
    ("asfalto", "Gávea Asfalto",    "O bairro poderia aproveitar melhor sua vocação econômica para gerar mais empregos locais."),
    ("asfalto", "Gávea Asfalto",    "Falta fomento para pequenas empresas. O comércio local está morrendo com a concorrência dos grandes shoppings."),
    ("bairro",  "Gávea",            "A Gávea tem grande potencial econômico que não é explorado em benefício dos moradores da favela."),

    # ── TURISMO ────────────────────────────────────────────────────────
    ("favela", "Rocinha",           "O turismo na Rocinha poderia gerar mais renda para os moradores se fosse organizado pela própria comunidade."),
    ("favela", "Rocinha",           "Gosto que as pessoas venham conhecer a comunidade, mas quero que o dinheiro fique aqui dentro."),
    ("asfalto", "Gávea Asfalto",    "A Gávea tem muito a oferecer ao turismo. O Parque da Cidade, a PUC, o Jóquei são atrativos únicos."),
    ("asfalto", "Gávea Asfalto",    "Estou satisfeito com a atividade turística do bairro. Gera movimento e valoriza a região."),
    ("bairro",  "Gávea",            "O turismo é um ponto forte da Gávea, mas precisa incluir as comunidades como protagonistas."),

    # ── TECNOLOGIA E INOVAÇÃO ───────────────────────────────────────────
    ("favela", "Rocinha",           "A internet aqui é puxada do GatoNet porque o serviço oficial não chega ou é caro demais."),
    ("favela", "Rocinha",           "Só tenho acesso à internet pelo celular com dados móveis. Fica impossível trabalhar ou estudar direito."),
    ("favela", "Rocinha",           "Wi-Fi público seria uma revolução aqui dentro. Meus filhos não conseguem fazer tarefa sem internet de qualidade."),
    ("favela", "Parque da Cidade",  "Tecnologia e inovação são palavras que não chegam até aqui. Nenhum projeto de inclusão digital funciona de verdade."),
    ("favela", "Parque da Cidade",  "Já ouvi falar de projeto de internet comunitária mas nunca vi nada ser implantado de fato."),
    ("asfalto", "Gávea Asfalto",    "A cobertura de internet na Gávea asfalto é razoável, mas deixa a desejar em estabilidade."),
    ("asfalto", "Gávea Asfalto",    "Serviços digitais da prefeitura poderiam ser mais eficientes. Ainda muita coisa é feita presencialmente."),
    ("bairro",  "Gávea",            "O gap de tecnologia entre o asfalto e as favelas é enorme. Isso aprofunda as desigualdades."),

    # ── MEIO AMBIENTE ───────────────────────────────────────────────────
    ("asfalto", "Gávea Asfalto",    "Adoro morar na Gávea pela natureza. As árvores, o silêncio, o ar puro. Isso não tem preço."),
    ("asfalto", "Gávea Asfalto",    "A preservação ambiental é o maior orgulho do bairro. Espero que continue assim com o crescimento urbano."),
    ("asfalto", "Gávea Asfalto",    "A arborização das ruas é excelente. Faz diferença no calor do Rio."),
    ("favela", "Rocinha",           "Tem muito lixo acumulado nos córregos porque a coleta não chega direito. Isso polui o ambiente da comunidade."),
    ("favela", "Parque da Cidade",  "A área verde perto do Parque da Cidade é linda, mas o acesso e a manutenção poderiam ser melhores para nós."),
    ("bairro",  "Gávea",            "O bairro tem vocação ambiental clara, mas é preciso incluir as favelas nos projetos de sustentabilidade."),

    # ── HABITAÇÃO ───────────────────────────────────────────────────────
    ("favela", "Rocinha",           "Minha casa foi construída com muito esforço mas falta regularização fundiária. Vivo com medo de remoção."),
    ("favela", "Rocinha",           "As casas aqui são apertadas e úmidas, mas fazemos o melhor que podemos com o espaço que temos."),
    ("favela", "Parque da Cidade",  "A habitação na comunidade é precária. Precisamos de programa de regularização e melhoria habitacional."),
    ("asfalto", "Gávea Asfalto",    "Moro num apartamento bem cuidado. Estou satisfeito com as condições de moradia no bairro."),
    ("asfalto", "Gávea Asfalto",    "Os imóveis na Gávea têm boa qualidade, mas o custo de vida é alto para quem não tem renda elevada."),
    ("bairro",  "Gávea",            "A qualidade da habitação é muito desigual. Quem mora no asfalto está bem, quem mora na favela sofre."),

    # ── EDUCAÇÃO ───────────────────────────────────────────────────────
    ("asfalto", "Gávea Asfalto",    "A PUC-Rio é um orgulho do bairro e eleva o nível educacional da região toda."),
    ("asfalto", "Gávea Asfalto",    "Os colégios particulares da Gávea são de excelente qualidade. Estou muito satisfeito com a educação dos meus filhos."),
    ("favela", "Rocinha",           "A escola pública aqui é sobrecarregada. Falta professor, material didático e estrutura básica."),
    ("favela", "Rocinha",           "Quero que meu filho estude numa escola boa mas as opções públicas estão longe e o ônibus não ajuda."),
    ("favela", "Parque da Cidade",  "Os projetos sociais da PUC ajudam muito, mas precisamos de mais vagas em escolas de qualidade perto daqui."),
    ("favela", "Parque da Cidade",  "A educação de base na comunidade é fraca. Muitas crianças ficam para trás por falta de apoio."),
    ("bairro",  "Gávea",            "O nível de educação é alto no bairro em geral, mas existe uma desigualdade gritante no acesso."),

    # ── CULTURA ────────────────────────────────────────────────────────
    ("asfalto", "Gávea Asfalto",    "A Gávea tem ótimas opções culturais: cinema, teatro, museus próximos. Estou muito satisfeito."),
    ("asfalto", "Gávea Asfalto",    "Os eventos culturais no Planetário e na PUC são ótimos. O bairro tem uma vida cultural rica."),
    ("favela", "Rocinha",           "As opções de cultura que existem no asfalto não chegam até a comunidade. Sinto falta disso."),
    ("favela", "Rocinha",           "Temos manifestações culturais riquíssimas aqui dentro, mas não recebemos apoio para divulgar e sustentar."),
    ("favela", "Parque da Cidade",  "Cultura para nós é o que criamos dentro da comunidade. Precisamos de apoio para fazer isso crescer."),
    ("bairro",  "Gávea",            "A cultura do bairro poderia ser mais inclusiva. Eventos no asfalto deveriam ser abertos às favelas."),

    # ── SAÚDE ──────────────────────────────────────────────────────────
    ("asfalto", "Gávea Asfalto",    "Tenho plano de saúde e os hospitais da zona sul atendem bem. Estou satisfeito com o acesso à saúde."),
    ("asfalto", "Gávea Asfalto",    "A UPA da região é sobrecarregada, mas no geral a saúde pública aqui é melhor que em outros bairros."),
    ("favela", "Rocinha",           "A fila no posto de saúde é enorme. Às vezes espero horas para ser atendida por coisa simples."),
    ("favela", "Rocinha",           "Falta médico especialista na comunidade. Para consulta com especialista tenho que ir longe."),
    ("favela", "Parque da Cidade",  "O acesso à saúde mental é praticamente zero aqui. Não existe suporte para quem precisa."),
    ("favela", "Parque da Cidade",  "O posto de saúde fecha cedo e não funciona fim de semana. Fica difícil para quem trabalha."),
    ("bairro",  "Gávea",            "A saúde precisa de mais investimento em todos os segmentos do bairro, principalmente nas favelas."),

    # ── MOBILIDADE ─────────────────────────────────────────────────────
    ("favela", "Rocinha",           "O ônibus para o metrô é lotado e demora muito. O ideal seria o metrô chegar até a Rua Marquês de São Vicente."),
    ("favela", "Rocinha",           "Subir e descer a Rocinha a pé é cansativo. As vans e mototáxis são caras para quem ganha pouco."),
    ("favela", "Parque da Cidade",  "A mobilidade dentro da comunidade é péssima. Não tem como passar com carrinho de bebê ou cadeira de rodas."),
    ("asfalto", "Gávea Asfalto",    "O trânsito na saída das escolas é caótico. Falta um plano de mobilidade escolar no bairro."),
    ("asfalto", "Gávea Asfalto",    "Uso carro particular porque o transporte público da Gávea é insuficiente. Precisamos de mais linhas."),
    ("asfalto", "Gávea Asfalto",    "A extensão do metrô até a Gávea transformaria o bairro. É o principal desejo de todos aqui."),
    ("bairro",  "Gávea",            "Mobilidade é um problema sério para todo o bairro, mas afeta muito mais os moradores das favelas."),

    # ── SEGURANÇA ──────────────────────────────────────────────────────
    ("favela", "Rocinha",           "A gente vive com medo de sair de casa à noite. Os confrontos armados assustam muito as famílias."),
    ("favela", "Rocinha",           "A segurança dentro da comunidade é controlada por milícia e tráfico. O estado não protege a gente."),
    ("favela", "Rocinha",           "Já perdi vizinhos para a violência. As operações policiais também nos deixam em pânico."),
    ("favela", "Parque da Cidade",  "Minha filha não sai mais à noite por causa da insegurança. Isso limita muito a vida da comunidade."),
    ("favela", "Parque da Cidade",  "Precisamos de segurança pública de verdade, não só operações que assustam mais do que protegem."),
    ("asfalto", "Gávea Asfalto",    "Me sinto razoavelmente seguro aqui no asfalto, comparando com outros bairros do Rio."),
    ("asfalto", "Gávea Asfalto",    "A segurança melhorou nos últimos anos, mas ainda há furtos frequentes em carros e residências."),
    ("asfalto", "Gávea Asfalto",    "Os câmeras de monitoramento ajudam, mas a presença policial ainda é insuficiente."),
    ("bairro",  "Gávea",            "A percepção de segurança é muito diferente entre quem mora no asfalto e nas favelas."),

    # ── GERAL / IDENTIDADE COM O BAIRRO ────────────────────────────────
    ("bairro",  "Gávea",            "Me identifico muito com a Gávea. É um bairro especial, mas precisa resolver suas desigualdades internas."),
    ("asfalto", "Gávea Asfalto",    "Moro na Gávea há 30 anos e tenho muito orgulho do bairro. Quero ver todo mundo bem aqui."),
    ("favela", "Rocinha",           "A Rocinha é minha casa e tenho orgulho de morar aqui, mas quero dignidade e serviços básicos de qualidade."),
    ("favela", "Parque da Cidade",  "O Parque da Cidade é lindo, mas a gente que mora aqui merece mais atenção das autoridades."),
    ("bairro",  "Gávea",            "A Gávea é um bairro que tem de tudo, mas precisa ser justo com todos os seus moradores."),
    ("favela", "Rocinha",           "Quero que meus filhos tenham futuro aqui na Rocinha, não precisem ir embora para ter oportunidade."),
    ("asfalto", "Gávea Asfalto",    "Gávea é um bairro privilegiado. Temos responsabilidade de ajudar a reduzir as desigualdades locais."),
]


def main() -> None:
    out_path = pathlib.Path("data/sample-gavealab-diagnostico.csv")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Shuffle for realistic ordering
    rows = list(RELATOS)
    random.shuffle(rows)

    with out_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["author_id", "territory_level", "territory_name", "text"])
        for idx, (level, name, text) in enumerate(rows, start=1):
            writer.writerow([f"C{idx:04d}", level, name, text])

    print(f"Wrote {len(rows)} rows to {out_path}")


if __name__ == "__main__":
    main()
