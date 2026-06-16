from fala_gavea_seguranca.domain.entities.security_report import ReportCategory


def test_report_category_has_nine_values() -> None:
    assert len(ReportCategory) == 9


def test_report_category_contains_new_categories() -> None:
    values = {c.value for c in ReportCategory}
    assert "furto_roubo" in values
    assert "espaco_publico_inseguro" in values
    assert "moradores_situacao_rua" in values
    assert "conflito_social" in values
    assert "barulho_perturbacao" in values


def test_report_category_retains_original_categories() -> None:
    values = {c.value for c in ReportCategory}
    assert "iluminacao" in values
    assert "transito" in values
    assert "vandalismo" in values
    assert "outro" in values
