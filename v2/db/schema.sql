-- Version 2 database. 37 tables in 11 modules. See ../design.md.
--
-- Rules that hold for every table:
--   * Every row has its own id. Entities are registered in `entity`.
--   * Codes come from `code`. Which list a column draws from is stated in `mapping.code_list`.
--   * Which class a referenced entity must have is stated in `mapping.ref_class`.
--   * The checks for both are triggers generated from `mapping` by `fieldwork_db.py init`.
--   * Years are stored as printed, with a scale. begin is the older bound, end the younger.

PRAGMA foreign_keys = ON;

-- ───────────────────────── Module A: ontology and mapping ─────────────────────────

CREATE TABLE ontology_source (
    name        TEXT PRIMARY KEY,
    version     TEXT NOT NULL,
    file        TEXT NOT NULL,
    namespace   TEXT NOT NULL
);

CREATE TABLE ontology_term (
    code        TEXT PRIMARY KEY,                 -- E22, P46, AP11, J5, Q10
    name        TEXT NOT NULL,                    -- E22_Human-Made_Object
    kind        TEXT NOT NULL CHECK (kind IN ('class', 'property')),
    source      TEXT NOT NULL REFERENCES ontology_source (name),
    uri         TEXT NOT NULL,
    label       TEXT,
    domain      TEXT,                             -- class code, properties only
    range       TEXT,                             -- class code or 'Literal'
    inverse_of  TEXT                              -- set on the inverse direction only
);

-- Transitive and reflexive. One row for every class and each of its ancestors.
CREATE TABLE ontology_subclass (
    sub         TEXT NOT NULL REFERENCES ontology_term (code),
    super       TEXT NOT NULL REFERENCES ontology_term (code),
    PRIMARY KEY (sub, super)
);

-- One row per column and path. The exporter executes these rows and nothing else.
CREATE TABLE mapping (
    table_name  TEXT NOT NULL,
    column_name TEXT NOT NULL,                    -- '*' defines the node of the row, '~name' a path fragment
    seq         INTEGER NOT NULL DEFAULT 1,
    cond        TEXT NOT NULL DEFAULT '',
    meaning     TEXT NOT NULL,
    path        TEXT NOT NULL,                    -- '-' for a column that only steers other paths
    code_list   TEXT,                             -- list the column draws its codes from
    ref_class   TEXT,                             -- classes the referenced entity may have, separated by |
    PRIMARY KEY (table_name, column_name, seq)
);

-- ───────────────────────── Module B: dataset ─────────────────────────

CREATE TABLE dataset (
    id            TEXT PRIMARY KEY,
    title         TEXT NOT NULL,
    fieldwork     TEXT NOT NULL,                  -- name of the excavation or survey
    season        TEXT,
    identifier    TEXT,                           -- persistent identifier, once an institution gives one
    language      TEXT REFERENCES code (id),
    rights_holder TEXT,
    licence       TEXT REFERENCES code (id),
    access        TEXT NOT NULL DEFAULT 'closed' CHECK (access IN ('open', 'embargo', 'closed')),
    embargo_until TEXT,
    version       TEXT NOT NULL DEFAULT '1',
    checksum      TEXT,
    method        TEXT,
    abbreviations TEXT,
    known_gaps    TEXT,
    remark        TEXT,
    CHECK (access <> 'embargo' OR embargo_until IS NOT NULL)
);

CREATE TABLE dataset_actor (
    dataset     TEXT NOT NULL REFERENCES dataset (id),
    actor       TEXT NOT NULL REFERENCES actor (id),
    role        TEXT NOT NULL REFERENCES code (id),
    position    INTEGER NOT NULL DEFAULT 1,
    PRIMARY KEY (dataset, actor, role)
);

-- ───────────────────────── Module C: core ─────────────────────────

CREATE TABLE entity (
    id          TEXT PRIMARY KEY,
    dataset     TEXT NOT NULL REFERENCES dataset (id),
    table_name  TEXT NOT NULL CHECK (table_name IN
                 ('actor', 'place', 'period', 'activity', 'thing', 'source', 'passage', 'media')),
    class       TEXT NOT NULL REFERENCES ontology_term (code),
    class2      TEXT REFERENCES ontology_term (code),   -- a second class, where one thing is two things at once
    source_id   TEXT,                             -- identifier in the excavator's own system
    label       TEXT,
    remark      TEXT
);

CREATE TABLE identifier (
    id          TEXT PRIMARY KEY,
    entity      TEXT NOT NULL REFERENCES entity (id),
    type        TEXT NOT NULL REFERENCES code (id),
    value       TEXT NOT NULL,
    UNIQUE (entity, type, value)
);

CREATE TABLE actor (
    id          TEXT PRIMARY KEY REFERENCES entity (id),
    member_of   TEXT REFERENCES actor (id),
    CHECK (member_of IS NULL OR member_of <> id)
);

CREATE TABLE place (
    id          TEXT PRIMARY KEY REFERENCES entity (id),
    type        TEXT REFERENCES code (id),
    part_of     TEXT REFERENCES entity (id),
    CHECK (part_of IS NULL OR part_of <> id)
);

CREATE TABLE period (
    id             TEXT PRIMARY KEY REFERENCES entity (id),
    language       TEXT REFERENCES code (id),
    start_earliest INTEGER,
    start_latest   INTEGER,
    end_earliest   INTEGER,
    end_latest     INTEGER,
    scale          TEXT CHECK (scale IN ('CE', 'BP', 'calBP')),
    approx         INTEGER NOT NULL DEFAULT 0 CHECK (approx IN (0, 1)),
    covers         TEXT REFERENCES entity (id),
    defined_by     TEXT REFERENCES source (id),
    part_of        TEXT REFERENCES period (id),
    periodo_id     TEXT,
    periodo_match  TEXT CHECK (periodo_match IN ('same', 'close', 'wider', 'narrower')),
    CHECK (part_of IS NULL OR part_of <> id),
    CHECK ((periodo_id IS NULL) = (periodo_match IS NULL)),
    CHECK (COALESCE(start_earliest, start_latest, end_earliest, end_latest) IS NULL OR scale IS NOT NULL),
    CHECK (scale IS NOT 'CE' OR start_earliest IS NULL OR end_latest IS NULL OR start_earliest <= end_latest),
    CHECK (scale IS 'CE' OR start_earliest IS NULL OR end_latest IS NULL OR start_earliest >= end_latest)
);

CREATE TABLE activity (
    id          TEXT PRIMARY KEY REFERENCES entity (id),
    type        TEXT REFERENCES code (id),
    place       TEXT REFERENCES entity (id),
    begin       INTEGER,
    end         INTEGER,
    scale       TEXT CHECK (scale IN ('CE', 'BP', 'calBP')),
    approx      INTEGER NOT NULL DEFAULT 0 CHECK (approx IN (0, 1)),
    part_of     TEXT REFERENCES activity (id),
    CHECK (part_of IS NULL OR part_of <> id),
    CHECK (COALESCE(begin, end) IS NULL OR scale IS NOT NULL),
    CHECK (scale IS NOT 'CE' OR begin IS NULL OR end IS NULL OR begin <= end),
    CHECK (scale IS 'CE' OR begin IS NULL OR end IS NULL OR begin >= end)
);

CREATE TABLE participation (
    id          TEXT PRIMARY KEY,
    activity    TEXT NOT NULL REFERENCES activity (id),
    actor       TEXT NOT NULL REFERENCES actor (id),
    role        TEXT REFERENCES code (id),
    UNIQUE (activity, actor, role)
);

CREATE TABLE thing (
    id          TEXT PRIMARY KEY REFERENCES entity (id),
    type        TEXT REFERENCES code (id),
    material    TEXT REFERENCES code (id),
    part_of     TEXT REFERENCES thing (id),
    kept_in     TEXT REFERENCES thing (id),
    location    TEXT REFERENCES entity (id),
    CHECK (part_of IS NULL OR part_of <> id),
    CHECK (kept_in IS NULL OR kept_in <> id)
);

CREATE TABLE dimension (
    id          TEXT PRIMARY KEY,
    entity      TEXT NOT NULL REFERENCES entity (id),
    kind        TEXT NOT NULL REFERENCES code (id),
    value       REAL,
    value_min   REAL,
    value_max   REAL,
    unit        TEXT REFERENCES code (id),
    approx      INTEGER NOT NULL DEFAULT 0 CHECK (approx IN (0, 1)),
    measured_by TEXT REFERENCES activity (id),
    remark      TEXT,
    CHECK (COALESCE(value, value_min, value_max) IS NOT NULL),
    CHECK (value_min IS NULL OR value_max IS NULL OR value_min <= value_max)
);

-- ───────────────────────── Module D: vocabulary ─────────────────────────

CREATE TABLE code_list (
    id          TEXT PRIMARY KEY,
    label       TEXT NOT NULL,
    module      TEXT NOT NULL,
    class       TEXT NOT NULL DEFAULT 'E55' REFERENCES ontology_term (code)
);

CREATE TABLE code (
    id          TEXT PRIMARY KEY,                 -- list/code, or list/dataset/code for an own code
    list        TEXT NOT NULL REFERENCES code_list (id),
    code        TEXT NOT NULL,
    label_en    TEXT,
    label_tr    TEXT,
    parent      TEXT REFERENCES code (id),
    uri         TEXT,                             -- address in a published vocabulary
    version     TEXT NOT NULL DEFAULT '1',
    valid_from  TEXT,
    state       TEXT NOT NULL DEFAULT 'current' CHECK (state IN ('current', 'withdrawn')),
    owner       TEXT REFERENCES dataset (id),     -- empty for a standard code
    CHECK (label_en IS NOT NULL OR label_tr IS NOT NULL)
);
CREATE UNIQUE INDEX code_unique ON code (list, code, COALESCE(owner, ''));

-- The excavator's own code beside the standard code.
CREATE TABLE own_code (
    own         TEXT NOT NULL REFERENCES code (id),
    standard    TEXT NOT NULL REFERENCES code (id),
    match       TEXT NOT NULL DEFAULT 'same' CHECK (match IN ('same', 'close', 'wider', 'narrower')),
    PRIMARY KEY (own, standard)
);

-- ───────────────────────── Module E: sources and documentation ─────────────────────────

CREATE TABLE source (
    id          TEXT PRIMARY KEY REFERENCES entity (id),
    type        TEXT REFERENCES code (id),
    citation    TEXT,
    year        INTEGER,
    language    TEXT REFERENCES code (id),
    part_of     TEXT REFERENCES source (id),
    url         TEXT,
    CHECK (part_of IS NULL OR part_of <> id)
);

CREATE TABLE passage (
    id          TEXT PRIMARY KEY REFERENCES entity (id),
    source      TEXT NOT NULL REFERENCES source (id),
    locator     TEXT NOT NULL                     -- page, figure or table, as printed
);

CREATE TABLE media (
    id          TEXT PRIMARY KEY REFERENCES entity (id),
    type        TEXT REFERENCES code (id),
    file_name   TEXT,
    scale       TEXT,
    made_by     TEXT REFERENCES activity (id),
    shown_in    TEXT REFERENCES passage (id)
);

CREATE TABLE about (
    id          TEXT PRIMARY KEY,
    item        TEXT NOT NULL REFERENCES entity (id),   -- a source, a passage or a media item
    target      TEXT NOT NULL REFERENCES entity (id),
    UNIQUE (item, target),
    CHECK (item <> target)
);

-- ───────────────────────── Module F: excavation ─────────────────────────

CREATE TABLE context (
    id          TEXT PRIMARY KEY REFERENCES thing (id),
    formation   TEXT REFERENCES code (id),
    confines    TEXT REFERENCES context (id),
    CHECK (confines IS NULL OR confines <> id)
);

CREATE TABLE find_context (
    id          TEXT PRIMARY KEY,
    thing       TEXT NOT NULL REFERENCES thing (id),
    found_in    TEXT REFERENCES entity (id),
    found_by    TEXT REFERENCES activity (id),
    method      TEXT REFERENCES code (id),
    claim       TEXT REFERENCES claim (id),
    remark      TEXT,
    CHECK (COALESCE(found_in, found_by) IS NOT NULL),
    CHECK (found_in IS NULL OR found_in <> thing)
);

-- ───────────────────────── Module G: science ─────────────────────────

CREATE TABLE sample (
    id          TEXT PRIMARY KEY REFERENCES thing (id),
    taken_from  TEXT REFERENCES entity (id),
    taken_by    TEXT REFERENCES activity (id),
    CHECK (taken_from IS NULL OR taken_from <> id)
);

CREATE TABLE analysis (
    id          TEXT PRIMARY KEY REFERENCES activity (id),
    method      TEXT REFERENCES code (id),
    laboratory  TEXT REFERENCES actor (id),
    lab_code    TEXT
);

-- ───────────────────────── Module H: claims ─────────────────────────

CREATE TABLE claim (
    id          TEXT PRIMARY KEY,
    dataset     TEXT NOT NULL REFERENCES dataset (id),
    kind        TEXT NOT NULL DEFAULT 'recorded' CHECK (kind IN ('inferred', 'adopted', 'recorded')),
    belief      TEXT NOT NULL DEFAULT 'true' CHECK (belief IN ('true', 'probable', 'possible', 'false')),
    method      TEXT REFERENCES code (id),
    made_by     TEXT REFERENCES actor (id),
    passage     TEXT REFERENCES passage (id),
    remark      TEXT,
    CHECK (kind = 'inferred' OR method IS NULL),
    CHECK (kind <> 'adopted' OR passage IS NOT NULL)
);

CREATE TABLE claim_basis (
    id           TEXT PRIMARY KEY,
    claim        TEXT NOT NULL REFERENCES claim (id),
    basis_claim  TEXT REFERENCES claim (id),
    basis_entity TEXT REFERENCES entity (id),
    CHECK ((basis_claim IS NULL) <> (basis_entity IS NULL)),
    CHECK (basis_claim IS NULL OR basis_claim <> claim)
);

CREATE TABLE assertion (
    id            TEXT PRIMARY KEY,
    subject       TEXT NOT NULL REFERENCES entity (id),
    property      TEXT NOT NULL REFERENCES relation_type (code),
    object_entity TEXT REFERENCES entity (id),
    object_code   TEXT REFERENCES code (id),
    object_text   TEXT,
    claim         TEXT NOT NULL REFERENCES claim (id),
    CHECK ((object_entity IS NOT NULL) + (object_code IS NOT NULL) + (object_text IS NOT NULL) = 1)
);

CREATE TABLE dating (
    id          TEXT PRIMARY KEY,
    subject     TEXT NOT NULL REFERENCES entity (id),
    event       TEXT NOT NULL CHECK (event IN ('making', 'use', 'deposition', 'death', 'formation', 'existence')),
    period      TEXT REFERENCES period (id),
    begin       INTEGER,
    end         INTEGER,
    scale       TEXT CHECK (scale IN ('CE', 'BP', 'calBP')),
    error       INTEGER,                          -- plus or minus, for a laboratory date
    approx      INTEGER NOT NULL DEFAULT 0 CHECK (approx IN (0, 1)),
    claim       TEXT NOT NULL REFERENCES claim (id),
    CHECK (COALESCE(period, begin, end) IS NOT NULL),
    CHECK (COALESCE(begin, end) IS NULL OR scale IS NOT NULL),
    CHECK (scale IS NOT 'CE' OR begin IS NULL OR end IS NULL OR begin <= end),
    CHECK (scale IS 'CE' OR begin IS NULL OR end IS NULL OR begin >= end)
);

-- ───────────────────────── Module I: space ─────────────────────────

CREATE TABLE geometry (
    id          TEXT PRIMARY KEY,
    entity      TEXT NOT NULL REFERENCES entity (id),
    kind        TEXT NOT NULL CHECK (kind IN ('point', 'line', 'polygon', 'other')),
    wkt         TEXT NOT NULL,
    crs         TEXT NOT NULL REFERENCES code (id),
    precision_m REAL CHECK (precision_m IS NULL OR precision_m >= 0),
    measured_by TEXT REFERENCES activity (id),
    remark      TEXT,
    CHECK (wkt GLOB 'POINT*' OR wkt GLOB 'LINESTRING*' OR wkt GLOB 'POLYGON*' OR wkt GLOB 'MULTI*' OR kind = 'other')
);

-- ───────────────────────── Module J: generic stores ─────────────────────────

CREATE TABLE relation_type (
    code          TEXT PRIMARY KEY,
    label_en      TEXT NOT NULL,
    label_tr      TEXT,
    inverse_label TEXT,
    module        TEXT NOT NULL,
    property      TEXT NOT NULL REFERENCES ontology_term (code),
    domain        TEXT NOT NULL REFERENCES ontology_term (code),
    range         TEXT NOT NULL REFERENCES ontology_term (code),
    subject_via   TEXT,                           -- path from the subject to the node that carries the property
    object_via    TEXT,                           -- the same for the object
    value_kind    TEXT NOT NULL DEFAULT 'entity' CHECK (value_kind IN ('entity', 'code', 'text')),
    code_list     TEXT REFERENCES code_list (id),
    conclusion    INTEGER NOT NULL DEFAULT 0 CHECK (conclusion IN (0, 1)),
    CHECK (value_kind = 'entity' OR conclusion = 1),
    CHECK ((value_kind = 'code') = (code_list IS NOT NULL))
);

CREATE TABLE relation (
    id          TEXT PRIMARY KEY,
    subject     TEXT NOT NULL REFERENCES entity (id),
    type        TEXT REFERENCES relation_type (code),      -- a declared type
    property    TEXT REFERENCES ontology_term (code),      -- or any property of the ontology
    object      TEXT NOT NULL REFERENCES entity (id),
    claim       TEXT REFERENCES claim (id),
    remark      TEXT,
    CHECK ((type IS NULL) <> (property IS NULL)),
    CHECK (subject <> object)
);

CREATE TABLE attribute_def (
    id          TEXT PRIMARY KEY,
    label_en    TEXT NOT NULL,
    label_tr    TEXT,
    applies_to  TEXT NOT NULL REFERENCES ontology_term (code),
    value_type  TEXT NOT NULL CHECK (value_type IN ('integer', 'decimal', 'text', 'yesno', 'code')),
    unit        TEXT REFERENCES code (id),
    code_list   TEXT REFERENCES code_list (id),
    owner       TEXT REFERENCES dataset (id),     -- empty for a declared attribute
    description TEXT,
    CHECK ((value_type = 'code') = (code_list IS NOT NULL)),
    CHECK (unit IS NULL OR value_type IN ('integer', 'decimal'))
);

CREATE TABLE attribute_value (
    id           TEXT PRIMARY KEY,
    entity       TEXT NOT NULL REFERENCES entity (id),
    attribute    TEXT NOT NULL REFERENCES attribute_def (id),
    value_number REAL,
    value_text   TEXT,
    value_code   TEXT REFERENCES code (id),
    claim        TEXT REFERENCES claim (id),
    remark       TEXT,
    CHECK ((value_number IS NOT NULL) + (value_text IS NOT NULL) + (value_code IS NOT NULL) = 1)
);

-- ───────────────────────── Module K: templates ─────────────────────────

CREATE TABLE template (
    id          TEXT PRIMARY KEY,
    label_en    TEXT NOT NULL,
    label_tr    TEXT,
    layout      TEXT NOT NULL DEFAULT 'list' CHECK (layout IN ('list', 'matrix')),
    base_table  TEXT NOT NULL CHECK (base_table IN ('actor', 'place', 'period', 'activity', 'thing', 'source', 'media')),
    base_class  TEXT NOT NULL REFERENCES ontology_term (code),
    extension   TEXT CHECK (extension IN ('context', 'sample', 'analysis')),
    owner       TEXT REFERENCES dataset (id),
    description TEXT
);

-- kind: column    a column of entity, of the base table or of the extension
--       attribute a declared or own attribute
--       dimension a count or measurement, the code of its kind in dimension_kind
--       found_in  the context or place of a find
--       dating    the period a thing is dated to, the event in column_name
--       geometry  coordinates as text, the coordinate system in column_name
--       identifier a number of the kind named in column_name
-- axis: for a matrix, 'row' and 'column' name the two axes and 'cell' the value
CREATE TABLE template_field (
    template       TEXT NOT NULL REFERENCES template (id),
    position       INTEGER NOT NULL,
    kind           TEXT NOT NULL CHECK (kind IN ('column', 'attribute', 'dimension', 'found_in', 'dating',
                                                 'geometry', 'identifier')),
    column_name    TEXT,
    attribute      TEXT REFERENCES attribute_def (id),
    dimension_kind TEXT REFERENCES code (id),
    axis           TEXT CHECK (axis IN ('row', 'column', 'cell')),
    label_en       TEXT NOT NULL,
    label_tr       TEXT,
    PRIMARY KEY (template, position),
    CHECK ((kind = 'attribute') = (attribute IS NOT NULL)),
    CHECK ((kind = 'dimension') = (dimension_kind IS NOT NULL)),
    CHECK (kind NOT IN ('column', 'dating', 'geometry', 'identifier') OR column_name IS NOT NULL)
);

-- ───────────────────────── Fixed triggers ─────────────────────────
-- Triggers for code lists and for classes of referenced entities are generated from `mapping`.

-- An entity's class must fit the table it is registered for.
CREATE TRIGGER entity_class_fits_table BEFORE INSERT ON entity
BEGIN
    SELECT RAISE(ABORT, 'entity: class is not a class of the ontology')
    WHERE NOT EXISTS (SELECT 1 FROM ontology_term WHERE code = NEW.class AND kind = 'class');
    SELECT RAISE(ABORT, 'entity: class does not fit the table')
    WHERE NOT EXISTS (
        SELECT 1 FROM ontology_subclass s
        WHERE s.sub = NEW.class AND s.super IN (
            SELECT CASE NEW.table_name
                WHEN 'actor'    THEN 'E39'
                WHEN 'place'    THEN 'E53'
                WHEN 'period'   THEN 'E4'
                WHEN 'activity' THEN 'E7'
                WHEN 'thing'    THEN 'S10'
                WHEN 'source'   THEN 'E73'
                WHEN 'passage'  THEN 'E73'
                WHEN 'media'    THEN 'E73' END));
    SELECT RAISE(ABORT, 'entity: the second class does not fit the table')
    WHERE NEW.class2 IS NOT NULL AND NOT EXISTS (
        SELECT 1 FROM ontology_subclass s
        WHERE s.sub = NEW.class2 AND s.super IN (
            SELECT CASE NEW.table_name
                WHEN 'actor'    THEN 'E39'
                WHEN 'place'    THEN 'E53'
                WHEN 'period'   THEN 'E4'
                WHEN 'activity' THEN 'E7'
                WHEN 'thing'    THEN 'S10'
                ELSE 'E73' END));
    SELECT RAISE(ABORT, 'entity: a person or group belongs in the table actor')
    WHERE NEW.table_name <> 'actor'
      AND EXISTS (SELECT 1 FROM ontology_subclass WHERE sub IN (NEW.class, NEW.class2) AND super = 'E39');
    SELECT RAISE(ABORT, 'entity: a physical thing belongs in the table thing, also when it is a place')
    WHERE NEW.table_name = 'place'
      AND EXISTS (SELECT 1 FROM ontology_subclass WHERE sub IN (NEW.class, NEW.class2) AND super = 'S10');
    SELECT RAISE(ABORT, 'entity: a period is not an activity. Use the table activity')
    WHERE NEW.table_name = 'period'
      AND EXISTS (SELECT 1 FROM ontology_subclass WHERE sub = NEW.class AND super = 'E7');
END;

CREATE TRIGGER entity_class_frozen BEFORE UPDATE OF class, table_name ON entity
BEGIN
    SELECT RAISE(ABORT, 'entity: class and table cannot be changed. Delete and enter again');
END;

CREATE TRIGGER entity_class2_checked BEFORE UPDATE OF class2 ON entity
WHEN NEW.class2 IS NOT NULL
BEGIN
    SELECT RAISE(ABORT, 'entity: the second class does not fit the table')
    WHERE NOT EXISTS (
        SELECT 1 FROM ontology_subclass s
        WHERE s.sub = NEW.class2 AND s.super IN (
            SELECT CASE NEW.table_name
                WHEN 'actor'    THEN 'E39'
                WHEN 'place'    THEN 'E53'
                WHEN 'period'   THEN 'E4'
                WHEN 'activity' THEN 'E7'
                WHEN 'thing'    THEN 'S10'
                ELSE 'E73' END));
END;

-- A relation must fit the domain and range of its property.
CREATE TRIGGER relation_checked BEFORE INSERT ON relation
BEGIN
    SELECT RAISE(ABORT, 'relation: this type is a conclusion. Store it in assertion, with a claim')
    WHERE EXISTS (SELECT 1 FROM relation_type WHERE code = NEW.type AND conclusion = 1);
    SELECT RAISE(ABORT, 'relation: not a property of the ontology')
    WHERE NEW.property IS NOT NULL
      AND NOT EXISTS (SELECT 1 FROM ontology_term WHERE code = NEW.property AND kind = 'property');
    SELECT RAISE(ABORT, 'relation: store the forward direction of the property, not the inverse')
    WHERE EXISTS (SELECT 1 FROM ontology_term WHERE code = NEW.property AND inverse_of IS NOT NULL);
    SELECT RAISE(ABORT, 'relation: the property takes a value, not an entity')
    WHERE EXISTS (SELECT 1 FROM ontology_term WHERE code = NEW.property AND range = 'Literal');
    SELECT RAISE(ABORT, 'relation: the subject does not fit the domain')
    WHERE NOT EXISTS (
        SELECT 1 FROM entity e JOIN ontology_subclass s ON s.sub IN (e.class, e.class2)
        WHERE e.id = NEW.subject AND s.super = COALESCE(
            (SELECT domain FROM relation_type WHERE code = NEW.type),
            (SELECT domain FROM ontology_term WHERE code = NEW.property)));
    SELECT RAISE(ABORT, 'relation: the object does not fit the range')
    WHERE NOT EXISTS (
        SELECT 1 FROM entity e JOIN ontology_subclass s ON s.sub IN (e.class, e.class2)
        WHERE e.id = NEW.object AND s.super = COALESCE(
            (SELECT range FROM relation_type WHERE code = NEW.type),
            (SELECT range FROM ontology_term WHERE code = NEW.property)));
END;

CREATE TRIGGER relation_type_checked BEFORE INSERT ON relation_type
BEGIN
    SELECT RAISE(ABORT, 'relation_type: the domain is not within the domain of the property')
    WHERE NEW.subject_via IS NULL AND NOT EXISTS (
        SELECT 1 FROM ontology_term p JOIN ontology_subclass s ON s.super = p.domain
        WHERE p.code = NEW.property AND p.kind = 'property' AND s.sub = NEW.domain);
    SELECT RAISE(ABORT, 'relation_type: the range is not within the range of the property')
    WHERE NEW.value_kind <> 'text' AND NEW.object_via IS NULL AND NOT EXISTS (
        SELECT 1 FROM ontology_term p JOIN ontology_subclass s ON s.super = p.range
        WHERE p.code = NEW.property AND s.sub = NEW.range);
END;

CREATE TRIGGER assertion_checked BEFORE INSERT ON assertion
BEGIN
    SELECT RAISE(ABORT, 'assertion: this type is a record, not a conclusion. Store it in relation')
    WHERE EXISTS (SELECT 1 FROM relation_type WHERE code = NEW.property AND conclusion = 0);
    SELECT RAISE(ABORT, 'assertion: the subject does not fit the domain')
    WHERE NOT EXISTS (
        SELECT 1 FROM entity e JOIN ontology_subclass s ON s.sub IN (e.class, e.class2)
        JOIN relation_type t ON t.code = NEW.property
        WHERE e.id = NEW.subject AND s.super = t.domain);
    SELECT RAISE(ABORT, 'assertion: the value is of the wrong kind for this property')
    WHERE NOT EXISTS (
        SELECT 1 FROM relation_type t WHERE t.code = NEW.property AND (
            (t.value_kind = 'entity' AND NEW.object_entity IS NOT NULL) OR
            (t.value_kind = 'code'   AND NEW.object_code   IS NOT NULL) OR
            (t.value_kind = 'text'   AND NEW.object_text   IS NOT NULL)));
    SELECT RAISE(ABORT, 'assertion: the object does not fit the range')
    WHERE NEW.object_entity IS NOT NULL AND NOT EXISTS (
        SELECT 1 FROM entity e JOIN ontology_subclass s ON s.sub IN (e.class, e.class2)
        JOIN relation_type t ON t.code = NEW.property
        WHERE e.id = NEW.object_entity AND s.super = t.range);
    SELECT RAISE(ABORT, 'assertion: the code is not from the list of this property')
    WHERE NEW.object_code IS NOT NULL AND NOT EXISTS (
        SELECT 1 FROM code c JOIN relation_type t ON t.code = NEW.property
        WHERE c.id = NEW.object_code AND c.list = t.code_list);
END;

CREATE TRIGGER attribute_value_checked BEFORE INSERT ON attribute_value
BEGIN
    SELECT RAISE(ABORT, 'attribute_value: the attribute does not apply to this class')
    WHERE NOT EXISTS (
        SELECT 1 FROM entity e JOIN ontology_subclass s ON s.sub IN (e.class, e.class2)
        JOIN attribute_def d ON d.id = NEW.attribute
        WHERE e.id = NEW.entity AND s.super = d.applies_to);
    SELECT RAISE(ABORT, 'attribute_value: the attribute belongs to another dataset')
    WHERE EXISTS (
        SELECT 1 FROM attribute_def d JOIN entity e ON e.id = NEW.entity
        WHERE d.id = NEW.attribute AND d.owner IS NOT NULL AND d.owner <> e.dataset);
    SELECT RAISE(ABORT, 'attribute_value: the value is of the wrong type')
    WHERE NOT EXISTS (
        SELECT 1 FROM attribute_def d WHERE d.id = NEW.attribute AND (
            (d.value_type = 'integer' AND NEW.value_number IS NOT NULL AND NEW.value_number = CAST(NEW.value_number AS INTEGER)) OR
            (d.value_type = 'decimal' AND NEW.value_number IS NOT NULL) OR
            (d.value_type = 'yesno'   AND NEW.value_number IN (0, 1)) OR
            (d.value_type = 'text'    AND NEW.value_text IS NOT NULL) OR
            (d.value_type = 'code'    AND NEW.value_code IS NOT NULL)));
    SELECT RAISE(ABORT, 'attribute_value: the code is not from the list of this attribute')
    WHERE NEW.value_code IS NOT NULL AND NOT EXISTS (
        SELECT 1 FROM code c JOIN attribute_def d ON d.id = NEW.attribute
        WHERE c.id = NEW.value_code AND c.list = d.code_list);
END;

-- What can be dated depends on the event.
CREATE TRIGGER dating_checked BEFORE INSERT ON dating
BEGIN
    SELECT RAISE(ABORT, 'dating: this event does not fit the class of the subject')
    WHERE NOT EXISTS (
        SELECT 1 FROM entity e JOIN ontology_subclass s ON s.sub IN (e.class, e.class2)
        WHERE e.id = NEW.subject AND s.super = CASE NEW.event
            WHEN 'making'     THEN 'E24'
            WHEN 'use'        THEN 'E70'
            WHEN 'deposition' THEN 'E18'
            WHEN 'death'      THEN 'E20'
            WHEN 'formation'  THEN 'A8'
            WHEN 'existence'  THEN 'E77' END);
END;

-- An extension row needs a base row of a fitting class.
CREATE TRIGGER context_checked BEFORE INSERT ON context
BEGIN
    SELECT RAISE(ABORT, 'context: the thing is not a stratigraphic unit or a feature')
    WHERE NOT EXISTS (
        SELECT 1 FROM entity e JOIN ontology_subclass s ON s.sub IN (e.class, e.class2)
        WHERE e.id = NEW.id AND s.super IN ('A8', 'E26'));
    SELECT RAISE(ABORT, 'context: only an interface confines, and only a volume is confined')
    WHERE NEW.confines IS NOT NULL AND NOT (
        EXISTS (SELECT 1 FROM entity e JOIN ontology_subclass s ON s.sub IN (e.class, e.class2)
                WHERE e.id = NEW.id AND s.super = 'A3')
        AND EXISTS (SELECT 1 FROM entity e JOIN ontology_subclass s ON s.sub IN (e.class, e.class2)
                WHERE e.id = NEW.confines AND s.super = 'A2'));
END;

CREATE TRIGGER sample_checked BEFORE INSERT ON sample
BEGIN
    SELECT RAISE(ABORT, 'sample: the thing is not of class S13 Sample')
    WHERE NOT EXISTS (
        SELECT 1 FROM entity e JOIN ontology_subclass s ON s.sub IN (e.class, e.class2)
        WHERE e.id = NEW.id AND s.super = 'S13');
END;

CREATE TRIGGER analysis_checked BEFORE INSERT ON analysis
BEGIN
    SELECT RAISE(ABORT, 'analysis: the activity is not an observation')
    WHERE NOT EXISTS (
        SELECT 1 FROM entity e JOIN ontology_subclass s ON s.sub IN (e.class, e.class2)
        WHERE e.id = NEW.id AND s.super = 'S27');
END;

-- An own code may only be used inside its own dataset.
CREATE TRIGGER own_code_checked BEFORE INSERT ON own_code
BEGIN
    SELECT RAISE(ABORT, 'own_code: the first code must be an own code, the second a standard code of the same list')
    WHERE NOT EXISTS (
        SELECT 1 FROM code o JOIN code s ON s.id = NEW.standard
        WHERE o.id = NEW.own AND o.owner IS NOT NULL AND s.owner IS NULL AND o.list = s.list);
END;

CREATE TRIGGER about_checked BEFORE INSERT ON about
BEGIN
    SELECT RAISE(ABORT, 'about: the item must be a source, a passage or a media item')
    WHERE NOT EXISTS (SELECT 1 FROM entity WHERE id = NEW.item AND table_name IN ('source', 'passage', 'media'));
END;
