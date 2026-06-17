# Research 000074 | FEATURE -X | 2026-06-17 21:18 | Camadas georeferenciadas para fala-gavea (Projeto 08)

tags: geospatial, leaflet, civic-tech, layers, ux

## User Brief

Camadas e mapas georeferenciados para adicionar dados ao fala-gavea:

PROJETO 08:
Mapa Colaborativo de Dados para Segurança e Planejamento do Bairro
Desafio: Como transformar dados públicos e colaborativos, como os do Censo ou mapas afetivos, em ferramentas úteis para o planejamento do bairro?

Transforma dados públicos e informações colaborativas em ferramenta útil para compreender problemas do território e apoiar decisões sobre segurança e planejamento urbano. Parte da percepção de que a falta de dados acessíveis dificulta a leitura real do bairro e enfraquece a capacidade da população de propor ou cobrar soluções.

Ferramenta simples e visual -- mapa colaborativo ou painel territorial -- reúne informações sobre iluminação, áreas percebidas como inseguras, locais de maior circulação, problemas urbanos, equipamentos, demandas recorrentes e percepções dos moradores. Dados vêm de fontes públicas (Censo, bases oficiais) e de contribuições de moradores, jovens, voluntários e instituições.

Inclui dimensão educativa, formando jovens, moradores e voluntários para coletar, interpretar e utilizar dados locais. Permite identificar prioridades, visualizar padrões e pactuar soluções com mais base.

## Agent Interpretation

O Projeto 08 quer ampliar o fala-gavea de sistema de registro de demandas individuais para um atlas territorial colaborativo. A questão central e estratégica e de arquitetura: como sobrepor dados externos (IBGE, data.rio, OSM) e dados colaborativos (percepção de insegurança dos moradores) ao mapa Leaflet existente, sem aumentar a complexidade do backend FastAPI alem do prazo do curso.

## Files Relevantes

- `fala-gavea/src/fala_gavea/application/use_cases/reports/list_reports_geojson.py`
- `fala-gavea/src/fala_gavea/presentation/api/routers/reports.py`
- `fala-gavea/src/fala_gavea/infrastructure/database/models.py`
- `fala-gavea/src/fala_gavea/domain/entities/report.py`
- `fala-gavea/product-design/project/product-design-as-intended.md`

---

## Q&A

### Q1: Como adicionar camadas georeferenciadas ao fala-gavea para o Projeto 08?

**A1 (Sintese das perspectivas avaliadas -- ARCH, PERF, API, UX, DATA/SEC)**

#### 1. A decisao arquitetural central: tres categorias de dados, tres estrategias

O fala-gavea ja tem relatos dinamicos (SQLite). O Projeto 08 adiciona duas novas categorias com caracteristicas diferentes:

| Categoria | Exemplos | Volume estimado | Estrategia recomendada |
|-----------|---------|----------------|----------------------|
| Relatos de cidadaos (ja existe) | Demandas por tipo/urgencia | < 500 features | GeoJSON dinamico -- endpoint atual OK |
| Dados publicos estaticos (novo) | IBGE, iluminacao, equipamentos | 100 a 10.000 features | GeoJSON pre-baixado em `static/layers/` servido pelo StaticFiles |
| Dados colaborativos de percepcao (novo) | "Este ponto me parece inseguro a noite" | < 200 features | Novo endpoint `GET /layers/perception/geojson` com entidade separada |

Misturar as tres categorias no mesmo repositorio de `Report` seria uma violacao de bounded context. Dados de percepcao tem ciclo de vida, semântica e privacidade distintos dos relatos formais.

#### 2. Fontes publicas de dados geoespaciais para o Rio de Janeiro

| Fonte | URL base | O que tem de util para Gavea |
|-------|---------|------------------------------|
| data.rio / IPP | `https://www.data.rio/` | Iluminacao publica, logradouros, equipamentos urbanos |
| geo.rio / ArcGIS Hub IPP | `https://geo.rio/` | Endpoints REST WMS/WFS; layers de bairro, uso do solo |
| IBGE | `https://geoftp.ibge.gov.br/` | Setores censitarios 2022 (renda, populacao, domicilios) -- GeoJSON/SHP |
| OpenStreetMap (Overpass API) | `https://overpass-api.de/api/interpreter` | Postos policiais, ciclovias, iluminacao, equipamentos -- licenca ODbL |
| 1746 / COR-Rio | Portal dados abertos Rio | Ocorrencias urbanas historicas -- qualidade variavel |

Para o curso: baixar os arquivos GeoJSON offline (IBGE setores censitarios da Gavea, postos policiais do OSM), commitar em `static/layers/`, e servir estaticamente. Zero dependencia de API externa em tempo de execucao.

#### 3. Implementacao no frontend Leaflet -- lazy loading por camada

Nao carregar todas as camadas na inicializacao. Padrão de lazy loading:

```javascript
// No index.html (Alpine.js + Leaflet)
const iluminacaoLayer = L.geoJSON(null, { /* ... */ });

map.on('overlayadd', function(e) {
    if (e.name === 'Iluminacao' && !iluminacaoLayer._loaded) {
        fetch('/static/layers/iluminacao.geojson')
            .then(r => r.json())
            .then(data => {
                iluminacaoLayer.addData(data);
                iluminacaoLayer._loaded = true;
            });
    }
});

const overlays = {
    "Relatos dos moradores": {
        "Todos os relatos": reportsLayer,
        "Alta urgencia": urgentLayer,
    },
    "Infraestrutura urbana": {
        "Iluminacao publica": iluminacaoLayer,
        "Equipamentos de seguranca": equipamentosLayer,
    },
    "Dados colaborativos": {
        "Percepcao de inseguranca": percepcaoLayer,
    },
    "Dados demograficos": {
        "Setores censitarios IBGE 2022": censitariosLayer,
    }
};

L.control.layers({}, overlays, { collapsed: false }).addTo(map);
```

Este padrao resolve performance sem arquitetura adicional e e implementavel em poucas horas.

#### 4. Dados colaborativos de percepcao -- entidade dedicada vs. reuso de Report

Duas opcoes:

**Opcao A (Recomendada para prazo de curso):** Adicionar um novo `ReportType` com nome "Percepcao de inseguranca" e reutilizar toda a infraestrutura existente (modelo, endpoints, validacoes). Implementacao: ~30 minutos. Trade-off: acumula logica de tipo no use case ao longo do tempo.

**Opcao B (Arquiteturalmente correta):** Nova entidade `PerceptionPoint` com modelo SQLAlchemy proprio, novo use case `ListPerceptionGeoJSON`, novo router `/layers/perception/geojson`. Implementacao: ~4 horas. Separacao limpa de dominio; migracao futura sem divida tecnica.

Para o Projeto 08 no prazo do curso, a **Opcao A** e aceitavel como decisao consciente documentada.

#### 5. Privacidade e seguranca -- coordenadas precisas no endpoint publico

O endpoint `GET /reports/geojson` e publico e expoe lat/lon com precisao total (~10m). Para dados cidadaos urbanos, coordenadas precisas permitem correlacao de identidade (morador que registrou o problema pode ser identificado pela localizacao exata de casa).

Solucao minima: **truncar lat/lon para 3 casas decimais** (~111m de precisao) antes de serializar o GeoJSON publico. Mudanca de 2 linhas no use case, zero impacto na visualizacao do mapa.

```python
# Em list_reports_geojson.py (use case)
"geometry": {
    "type": "Point",
    "coordinates": [round(r.lon, 3), round(r.lat, 3)]
}
```

#### 6. PostGIS -- nao agora

Para o escopo atual (dados da Gavea, volume limitado, prazo de curso), SQLite + SQLAlchemy e suficiente. O filtro `bbox` ja implementado no `ReportFilters` cobre o caso mais comum. Analises espaciais adicionais (contagem por setor, intersecao com poligonos) podem ser feitas no frontend com `turf.js` sem backend:

```javascript
import * as turf from '@turf/turf';
const relatosNaArea = turf.pointsWithinPolygon(reportsFC, setorCensitario);
```

PostGIS so justificaria se o projeto fosse alem do prazo do curso com consultas espaciais complexas no servidor (> 50.000 features, operacoes de join espacial, geo-indexes).

---

## Recommendations Summary

| # | Prioridade | Recomendacao |
|---|-----------|-------------|
| R1 | ALTA | Definir estrategia por categoria antes de escrever codigo (3 tipos x 3 estrategias) |
| R2 | ALTA | Implementar lazy loading no LayerControl do Leaflet -- nao carregar todas as camadas no startup |
| R3 | ALTA | Truncar lat/lon para 3 casas decimais no endpoint GeoJSON publico -- protege privacidade com impacto zero na UX do mapa |
| R4 | MEDIA | Organizar overlays no L.control.layers() em grupos por categoria (moradores / infraestrutura / colaborativo / demografico) |
| R5 | MEDIA | Para dados publicos estaticos: baixar GeoJSON offline e commitar em `static/layers/` -- zero dependencia de API externa |
| R6 | MEDIA | Para dados colaborativos: reutilizar ReportType como "Percepcao de inseguranca" (Opcao A) para o prazo do curso, com nota de divida tecnica |
| R7 | MEDIA | Adicionar legenda persistente + fonte do dado por camada ativa (dimensao educativa do Projeto 08) |
| R8 | BAIXA | Avaliar turf.js para analise espacial client-side (contagem de relatos por setor censitario) -- evita necessidade de PostGIS |
| R9 | BAIXA | Nao migrar para PostGIS dentro do prazo do curso; registrar como future work |

### Fontes de dados prioritarias para comecar

Para montar o mapa colaborativo rapidamente:

1. **IBGE 2022**: Baixar malha de setores censitarios do municipio do Rio de Janeiro em `https://geoftp.ibge.gov.br/recortes_para_fins_estatisticos/malha_de_setores_censitarios/censo_2022/`; recortar bairro da Gavea (RA XV) com ogr2ogr ou QGIS
2. **IPP/data.rio**: Buscar layer de iluminacao publica em `https://www.data.rio/`; exportar como GeoJSON
3. **OpenStreetMap**: Consultar Overpass API para postos policiais, UPAs, escolas na Gavea:
   ```
   [out:json];
   area["name"="Gávea"]["admin_level"="10"]->.gavea;
   nwr["amenity"~"police|hospital|school"](area.gavea);
   out geom;
   ```
4. **Dados proprios de percepcao**: Estender o formulario de relato com novo tipo "Ponto de atencao na seguranca" -- zero infra adicional com Opcao A

