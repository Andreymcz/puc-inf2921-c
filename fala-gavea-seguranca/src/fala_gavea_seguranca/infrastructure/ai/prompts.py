"""AI prompt templates for security report processing.

Imported by use_cases/auto_categorize_report.py (Wave 1 Item 3, roadmap-000056).
"""

CATEGORIZE_PROMPT: str = """/nothink
Voce e um assistente especializado em seguranca publica urbana.
Categorize o relato abaixo escolhendo EXATAMENTE UMA das seguintes categorias:

- furto_roubo: Furtos, roubos, assaltos, tentativas de roubo
- iluminacao: Problemas de iluminacao publica (postes apagados, ruas escuras)
- transito: Transito caotico, acidentes, sinalizacao deficiente, pontos de onibus perigosos
- espaco_publico_inseguro: Espacos publicos inseguros ou abandonados (pracas, calcadas, paradas)
- vandalismo: Depredacao de patrimonio publico ou privado, pichacao
- moradores_situacao_rua: Concentracao de moradores em situacao de rua gerando inseguranca
- conflito_social: Conflito comunitario, tiroteio, tensao entre grupos, barricadas
- barulho_perturbacao: Barulho excessivo perturbando a ordem publica
- outro: Qualquer outro problema de seguranca que nao se encaixe nas categorias acima

Relato: {text}

Responda APENAS com JSON valido no formato:
{{"category": "<valor>", "confidence": "alta|media|baixa", "justification": "<max 1 frase>"}}
"""
