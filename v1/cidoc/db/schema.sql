-- Excavation database constrained to CIDOC CRM + CRMarchaeo + CRMsci.
--
-- Tables are things an excavator recognises (context, find, sample ...).
-- Behind every column stands one fixed CRM path, listed in crm_mapping.
-- Classes can only be chosen from ontology_term, which is filled from the
-- official RDFS files: the graph cannot leave the ontology.
--
-- One database holds many reports. Every id is unique within its report.

PRAGMA foreign_keys = ON;

-- ---------------------------------------------------------------------------
-- the boundary: terms of the ontologies, and what each column means
-- ---------------------------------------------------------------------------

CREATE TABLE ontology_term (
    name      TEXT PRIMARY KEY,                 -- E22_Human-Made_Object, AP11_has_physical_relation_to
    kind      TEXT NOT NULL CHECK (kind IN ('class', 'property')),
    ontology  TEXT NOT NULL,                    -- CIDOC CRM 7.1.3 / CRMarchaeo 2.1.1 / CRMsci 3.2
    uri       TEXT NOT NULL UNIQUE,
    domain    TEXT,
    range     TEXT
);

CREATE TABLE ontology_subclass (
    name    TEXT NOT NULL REFERENCES ontology_term (name),
    parent  TEXT NOT NULL REFERENCES ontology_term (name),
    PRIMARY KEY (name, parent)
);

CREATE TABLE crm_mapping (
    table_name   TEXT NOT NULL,
    column_name  TEXT NOT NULL,
    meaning      TEXT NOT NULL,                 -- plain words, for the person filling the table
    crm_path     TEXT NOT NULL,                 -- the fixed path the column becomes
    PRIMARY KEY (table_name, column_name)
);

CREATE TABLE relation_type (
    name      TEXT PRIMARY KEY,                 -- cuts, overlies, contemporary with ...
    physical  INTEGER NOT NULL CHECK (physical IN (0, 1))
);

-- ---------------------------------------------------------------------------
-- source: the report and its volume
-- ---------------------------------------------------------------------------

CREATE TABLE volume (
    id         TEXT PRIMARY KEY,
    title      TEXT NOT NULL,
    editor     TEXT,
    publisher  TEXT,
    isbn       TEXT,
    place      TEXT,
    published  INTEGER
);

CREATE TABLE report (
    id              TEXT PRIMARY KEY,           -- yumuktepe-2024
    base_uri        TEXT NOT NULL UNIQUE,
    shared_uri      TEXT,
    schema_version  INTEGER,
    comment         TEXT,
    document_id     TEXT NOT NULL,
    title           TEXT NOT NULL,
    language        TEXT NOT NULL DEFAULT 'tr',
    printed_pages   TEXT NOT NULL,
    published       INTEGER,
    source_file     TEXT NOT NULL,
    reports_on      TEXT,                       -- the campaign the report is about
    volume_id       TEXT REFERENCES volume (id)
);

-- every row of every table below is registered here once, so that
-- references, pages and figures can point at any of them
CREATE TABLE entity (
    report  TEXT NOT NULL REFERENCES report (id),
    id      TEXT NOT NULL,
    kind    TEXT NOT NULL CHECK (kind IN ('actor', 'place', 'period', 'feature', 'stratum', 'activity',
                                          'plan', 'find', 'sample', 'analysis', 'relation',
                                          'interpretation', 'figure',
                                          'reference', 'documentation')),          -- v3
    PRIMARY KEY (report, id)
);

CREATE TABLE source_page (
    report  TEXT NOT NULL,
    id      TEXT NOT NULL,
    page    INTEGER NOT NULL,
    PRIMARY KEY (report, id, page),
    FOREIGN KEY (report, id) REFERENCES entity (report, id)
);

-- ---------------------------------------------------------------------------
-- who, where, when
-- ---------------------------------------------------------------------------

CREATE TABLE actor (
    report     TEXT NOT NULL,
    id         TEXT NOT NULL,
    class      TEXT NOT NULL REFERENCES ontology_term (name)
                    CHECK (class IN ('E21_Person', 'E74_Group', 'E39_Actor')),
    label      TEXT NOT NULL,
    orcid      TEXT CHECK (orcid IS NULL OR orcid GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9X]'),
    member_of  TEXT,
    note       TEXT,
    PRIMARY KEY (report, id),
    FOREIGN KEY (report, id) REFERENCES entity (report, id),
    FOREIGN KEY (report, member_of) REFERENCES actor (report, id)
);

CREATE TABLE report_author (
    report    TEXT NOT NULL REFERENCES report (id),
    position  INTEGER NOT NULL,
    actor     TEXT NOT NULL,
    PRIMARY KEY (report, position),
    FOREIGN KEY (report, actor) REFERENCES actor (report, id)
);

CREATE TABLE place (
    report  TEXT NOT NULL,
    id      TEXT NOT NULL,
    label   TEXT NOT NULL,
    type    TEXT,
    within  TEXT,
    note    TEXT,
    PRIMARY KEY (report, id),
    FOREIGN KEY (report, id) REFERENCES entity (report, id),
    FOREIGN KEY (report, within) REFERENCES place (report, id)
);

CREATE TABLE period (
    report      TEXT NOT NULL,
    id          TEXT NOT NULL,
    label       TEXT NOT NULL,
    begin_year  INTEGER CHECK (begin_year <> 0),      -- historical year, BC negative
    end_year    INTEGER CHECK (end_year <> 0),
    approx      INTEGER CHECK (approx IN (0, 1)),
    within      TEXT,
    PRIMARY KEY (report, id),
    FOREIGN KEY (report, id) REFERENCES entity (report, id),
    FOREIGN KEY (report, within) REFERENCES period (report, id),
    CHECK (begin_year IS NULL OR end_year IS NULL OR begin_year <= end_year)
);

-- ---------------------------------------------------------------------------
-- what was dug: contexts, their relations, the work
-- ---------------------------------------------------------------------------

-- a context is a built feature (wall, room, oven, the site itself) or a deposit
CREATE TABLE context (
    report      TEXT NOT NULL,
    id          TEXT NOT NULL,
    kind        TEXT NOT NULL CHECK (kind IN ('feature', 'stratum')),
    class       TEXT NOT NULL REFERENCES ontology_term (name),
    label       TEXT NOT NULL,
    identifier  TEXT,                           -- the code used on site: A701, BX, M1
    type        TEXT,
    part_of     TEXT,                           -- feature inside a larger feature
    location    TEXT,                           -- named place
    at_feature  TEXT,                           -- deposit: the feature it lies in
    "count"     INTEGER CHECK ("count" > 0),
    note        TEXT,
    PRIMARY KEY (report, id),
    FOREIGN KEY (report, id) REFERENCES entity (report, id),
    FOREIGN KEY (report, part_of) REFERENCES context (report, id),
    FOREIGN KEY (report, location) REFERENCES place (report, id),
    FOREIGN KEY (report, at_feature) REFERENCES entity (report, id),
    CHECK ((kind = 'feature' AND class IN ('E27_Site', 'E22_Human-Made_Object', 'E25_Human-Made_Feature', 'E26_Physical_Feature'))
        OR (kind = 'stratum' AND class IN ('A2_Stratigraphic_Volume_Unit', 'A3_Stratigraphic_Interface', 'A8_Stratigraphic_Unit')))
);

CREATE TABLE relation (
    report        TEXT NOT NULL,
    id            TEXT NOT NULL,
    from_context  TEXT NOT NULL,                -- the later unit
    type          TEXT NOT NULL REFERENCES relation_type (name),
    to_context    TEXT NOT NULL,                -- the earlier unit
    certainty     TEXT,
    note          TEXT,
    PRIMARY KEY (report, id),
    FOREIGN KEY (report, id) REFERENCES entity (report, id),
    FOREIGN KEY (report, from_context) REFERENCES context (report, id),
    FOREIGN KEY (report, to_context) REFERENCES context (report, id),
    CHECK (from_context <> to_context)
);

CREATE TABLE activity (
    report        TEXT NOT NULL,
    id            TEXT NOT NULL,
    class         TEXT NOT NULL REFERENCES ontology_term (name)
                       CHECK (class IN ('A9_Archaeological_Excavation', 'A1_Excavation_Processing_Unit', 'E7_Activity')),
    type          TEXT,
    label         TEXT NOT NULL,
    begin_year    INTEGER CHECK (begin_year <> 0),
    end_year      INTEGER CHECK (end_year <> 0),
    approx        INTEGER CHECK (approx IN (0, 1)),
    part_of       TEXT,
    at_feature    TEXT,
    investigated  TEXT,
    purpose_of    TEXT,
    identifier    TEXT,                         -- project or permit number
    note          TEXT,
    PRIMARY KEY (report, id),
    FOREIGN KEY (report, id) REFERENCES entity (report, id),
    FOREIGN KEY (report, part_of) REFERENCES activity (report, id),
    FOREIGN KEY (report, at_feature) REFERENCES entity (report, id),
    FOREIGN KEY (report, investigated) REFERENCES context (report, id),
    FOREIGN KEY (report, purpose_of) REFERENCES activity (report, id),
    CHECK (begin_year IS NULL OR end_year IS NULL OR begin_year <= end_year)
);

CREATE TABLE activity_actor (
    report    TEXT NOT NULL,
    activity  TEXT NOT NULL,
    position  INTEGER NOT NULL,
    actor     TEXT NOT NULL,
    role      TEXT,
    PRIMARY KEY (report, activity, position),
    FOREIGN KEY (report, activity) REFERENCES activity (report, id),
    FOREIGN KEY (report, actor) REFERENCES actor (report, id)
);

CREATE TABLE activity_link (
    report    TEXT NOT NULL,
    activity  TEXT NOT NULL,
    link      TEXT NOT NULL CHECK (link IN ('took_place_at', 'also_at', 'continued', 'removed', 'used',
                                           'produced')),                           -- v3: deposit the work created
    position  INTEGER NOT NULL,
    target    TEXT NOT NULL,
    PRIMARY KEY (report, activity, link, position),
    FOREIGN KEY (report, activity) REFERENCES activity (report, id),
    FOREIGN KEY (report, target) REFERENCES entity (report, id)
);

CREATE TABLE plan (
    report       TEXT NOT NULL,
    id           TEXT NOT NULL,
    label        TEXT NOT NULL,
    planned_for  INTEGER,
    place        TEXT,
    note         TEXT,
    PRIMARY KEY (report, id),
    FOREIGN KEY (report, id) REFERENCES entity (report, id),
    FOREIGN KEY (report, place) REFERENCES place (report, id)
);

CREATE TABLE plan_about (
    report    TEXT NOT NULL,
    plan      TEXT NOT NULL,
    position  INTEGER NOT NULL,
    target    TEXT NOT NULL,
    PRIMARY KEY (report, plan, position),
    FOREIGN KEY (report, plan) REFERENCES plan (report, id),
    FOREIGN KEY (report, target) REFERENCES entity (report, id)
);

-- ---------------------------------------------------------------------------
-- what was found, sampled and measured
-- ---------------------------------------------------------------------------

CREATE TABLE find (
    report        TEXT NOT NULL,
    id            TEXT NOT NULL,
    class         TEXT NOT NULL REFERENCES ontology_term (name)
                       CHECK (class IN ('E22_Human-Made_Object', 'E20_Biological_Object', 'E19_Physical_Object')),
    label         TEXT NOT NULL,
    type          TEXT NOT NULL,
    "count"       INTEGER CHECK ("count" > 0),
    material      TEXT,
    found_by      TEXT NOT NULL,                -- the excavation unit that found it
    at_feature    TEXT,
    from_stratum  TEXT,
    condition     TEXT,
    depicts       TEXT,
    inscribed     INTEGER CHECK (inscribed IN (0, 1)),
    part_of       TEXT,                         -- v3: the counted assemblage this find belongs to
    note          TEXT,
    PRIMARY KEY (report, id),
    FOREIGN KEY (report, id) REFERENCES entity (report, id),
    FOREIGN KEY (report, part_of) REFERENCES find (report, id),
    CHECK (part_of IS NULL OR part_of <> id),
    FOREIGN KEY (report, found_by) REFERENCES activity (report, id),
    FOREIGN KEY (report, at_feature) REFERENCES entity (report, id),
    FOREIGN KEY (report, from_stratum) REFERENCES context (report, id)
);

CREATE TABLE sample (
    report         TEXT NOT NULL,
    id             TEXT NOT NULL,
    class          TEXT NOT NULL DEFAULT 'S13_Sample' REFERENCES ontology_term (name),
    label          TEXT NOT NULL,
    material_type  TEXT,
    taken_from     TEXT NOT NULL,
    taken_during   TEXT,
    note           TEXT,
    PRIMARY KEY (report, id),
    FOREIGN KEY (report, id) REFERENCES entity (report, id),
    FOREIGN KEY (report, taken_from) REFERENCES entity (report, id),
    FOREIGN KEY (report, taken_during) REFERENCES activity (report, id)
);

CREATE TABLE analysis (
    report        TEXT NOT NULL,
    id            TEXT NOT NULL,
    type          TEXT NOT NULL,
    label         TEXT NOT NULL,
    result_begin  INTEGER NOT NULL CHECK (result_begin <> 0),
    result_end    INTEGER NOT NULL CHECK (result_end <> 0),
    dates         TEXT,                         -- the context or object the result dates
    note          TEXT,
    PRIMARY KEY (report, id),
    FOREIGN KEY (report, id) REFERENCES entity (report, id),
    FOREIGN KEY (report, dates) REFERENCES entity (report, id),
    CHECK (result_begin <= result_end)
);

CREATE TABLE analysis_sample (
    report    TEXT NOT NULL,
    analysis  TEXT NOT NULL,
    position  INTEGER NOT NULL,
    sample    TEXT NOT NULL,
    PRIMARY KEY (report, analysis, position),
    FOREIGN KEY (report, analysis) REFERENCES analysis (report, id),
    FOREIGN KEY (report, sample) REFERENCES sample (report, id)
);

CREATE TABLE analysis_actor (
    report    TEXT NOT NULL,
    analysis  TEXT NOT NULL,
    part      TEXT NOT NULL CHECK (part IN ('by', 'concluded_by')),
    position  INTEGER NOT NULL,
    actor     TEXT NOT NULL,
    PRIMARY KEY (report, analysis, part, position),
    FOREIGN KEY (report, analysis) REFERENCES analysis (report, id),
    FOREIGN KEY (report, actor) REFERENCES actor (report, id)
);

-- ---------------------------------------------------------------------------
-- properties shared by contexts, finds and samples
-- ---------------------------------------------------------------------------

CREATE TABLE dating (
    report    TEXT NOT NULL,
    id        TEXT NOT NULL,
    position  INTEGER NOT NULL,
    period    TEXT NOT NULL,
    certainty TEXT CHECK (certainty IN ('uncertain', 'one of')),   -- v3: empty = stated as fact
    PRIMARY KEY (report, id, position),
    FOREIGN KEY (report, id) REFERENCES entity (report, id),
    FOREIGN KEY (report, period) REFERENCES period (report, id)
);

CREATE TABLE dimension (
    report    TEXT NOT NULL,
    id        TEXT NOT NULL,
    position  INTEGER NOT NULL,
    type      TEXT NOT NULL,
    value     NUMERIC,
    min       NUMERIC,
    max       NUMERIC,
    unit      TEXT NOT NULL,
    approx    INTEGER CHECK (approx IN (0, 1)),
    PRIMARY KEY (report, id, position),
    FOREIGN KEY (report, id) REFERENCES entity (report, id),
    CHECK (value IS NOT NULL OR min IS NOT NULL OR max IS NOT NULL),
    CHECK (min IS NULL OR max IS NULL OR min <= max)
);

CREATE TABLE taxon (
    report    TEXT NOT NULL,
    id        TEXT NOT NULL,
    position  INTEGER NOT NULL,
    name      TEXT NOT NULL,
    PRIMARY KEY (report, id, position),
    FOREIGN KEY (report, id) REFERENCES entity (report, id)
);

CREATE TABLE comparandum (
    report    TEXT NOT NULL,
    id        TEXT NOT NULL,
    position  INTEGER NOT NULL,
    label     TEXT NOT NULL,
    refs      TEXT,
    PRIMARY KEY (report, id, position),
    FOREIGN KEY (report, id) REFERENCES entity (report, id)
);

-- ---------------------------------------------------------------------------
-- who says so: attributed statements are kept apart from observations
-- ---------------------------------------------------------------------------

-- a dating or identification credited to named people
CREATE TABLE attribution (
    report  TEXT NOT NULL,
    id      TEXT NOT NULL,
    about   TEXT NOT NULL CHECK (about IN ('dating', 'identification')),
    via     TEXT,                               -- personal communication, authors' assessment
    PRIMARY KEY (report, id, about),
    FOREIGN KEY (report, id) REFERENCES entity (report, id)
);

CREATE TABLE attribution_actor (
    report    TEXT NOT NULL,
    id        TEXT NOT NULL,
    about     TEXT NOT NULL,
    position  INTEGER NOT NULL,
    actor     TEXT NOT NULL,
    PRIMARY KEY (report, id, about, position),
    FOREIGN KEY (report, id, about) REFERENCES attribution (report, id, about),
    FOREIGN KEY (report, actor) REFERENCES actor (report, id)
);

CREATE TABLE interpretation (
    report    TEXT NOT NULL,
    id        TEXT NOT NULL,
    about     TEXT NOT NULL,
    assigned  TEXT NOT NULL,                    -- what is claimed
    basis     TEXT,                             -- why
    PRIMARY KEY (report, id),
    FOREIGN KEY (report, id) REFERENCES entity (report, id),
    FOREIGN KEY (report, about) REFERENCES entity (report, id)
);

CREATE TABLE interpretation_actor (
    report          TEXT NOT NULL,
    interpretation  TEXT NOT NULL,
    position        INTEGER NOT NULL,
    actor           TEXT NOT NULL,
    PRIMARY KEY (report, interpretation, position),
    FOREIGN KEY (report, interpretation) REFERENCES interpretation (report, id),
    FOREIGN KEY (report, actor) REFERENCES actor (report, id)
);

-- ---------------------------------------------------------------------------
-- v3: literature the report cites, and documentation made on site
-- ---------------------------------------------------------------------------

CREATE TABLE reference (
    report    TEXT NOT NULL,
    id        TEXT NOT NULL,
    citation  TEXT NOT NULL,                    -- as printed in the bibliography
    year      INTEGER,
    note      TEXT,
    PRIMARY KEY (report, id),
    FOREIGN KEY (report, id) REFERENCES entity (report, id)
);

CREATE TABLE cited_for (
    report     TEXT NOT NULL,
    id         TEXT NOT NULL,                   -- the row the citation supports
    position   INTEGER NOT NULL,
    reference  TEXT NOT NULL,
    pages      TEXT,
    PRIMARY KEY (report, id, position),
    FOREIGN KEY (report, id) REFERENCES entity (report, id),
    FOREIGN KEY (report, reference) REFERENCES reference (report, id)
);

-- plans, drawings, 3D models, photographs, notebooks: what the archive of an excavation holds
CREATE TABLE documentation (
    report   TEXT NOT NULL,
    id       TEXT NOT NULL,
    type     TEXT NOT NULL,
    label    TEXT NOT NULL,
    scale    TEXT,
    made_by  TEXT,                              -- the work that produced it
    note     TEXT,
    PRIMARY KEY (report, id),
    FOREIGN KEY (report, id) REFERENCES entity (report, id),
    FOREIGN KEY (report, made_by) REFERENCES activity (report, id)
);

CREATE TABLE documentation_depicts (
    report         TEXT NOT NULL,
    documentation  TEXT NOT NULL,
    position       INTEGER NOT NULL,
    target         TEXT NOT NULL,
    PRIMARY KEY (report, documentation, position),
    FOREIGN KEY (report, documentation) REFERENCES documentation (report, id),
    FOREIGN KEY (report, target) REFERENCES entity (report, id)
);

-- ---------------------------------------------------------------------------
-- figures
-- ---------------------------------------------------------------------------

CREATE TABLE figure (
    report   TEXT NOT NULL,
    id       TEXT NOT NULL,
    kind     TEXT NOT NULL DEFAULT 'Resim' CHECK (kind IN ('Resim', 'Şekil', 'Plan', 'Harita', 'Çizim', 'Tablo', 'Grafik')),
    number   INTEGER NOT NULL,
    caption  TEXT NOT NULL,
    page     INTEGER NOT NULL,
    PRIMARY KEY (report, id),
    FOREIGN KEY (report, id) REFERENCES entity (report, id)
);

CREATE TABLE figure_depicts (
    report    TEXT NOT NULL,
    figure    TEXT NOT NULL,
    position  INTEGER NOT NULL,
    target    TEXT NOT NULL,
    PRIMARY KEY (report, figure, position),
    FOREIGN KEY (report, figure) REFERENCES figure (report, id),
    FOREIGN KEY (report, target) REFERENCES entity (report, id)
);

-- figures that illustrate a row of any table
CREATE TABLE illustrated_by (
    report    TEXT NOT NULL,
    id        TEXT NOT NULL,
    position  INTEGER NOT NULL,
    figure    TEXT NOT NULL,
    PRIMARY KEY (report, id, position),
    FOREIGN KEY (report, id) REFERENCES entity (report, id),
    FOREIGN KEY (report, figure) REFERENCES figure (report, id)
);
