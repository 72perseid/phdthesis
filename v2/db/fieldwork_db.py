#!/usr/bin/env python3
"""Version 2 database for fieldwork data. See ../design.md.

Commands
    init    DB                      create the tables, load the ontology files and the seed lists
    check   DB                      test the mapping, the paths and the stored data
    graph   DB [-d DATASET] -o FILE write the graph, then check every statement against the ontology
    audit   DB                      remove each column in turn and see whether the graph changes
    levels  DB                      count the statements by level, per dataset
    sheet   DB TEMPLATE -o FILE     write an empty sheet for a template
    fill    DB TEMPLATE DATASET FILE [--under ENTITY]   load a filled sheet
    view    DB DATASET -o DIR       write what is stored as wide tables, one per kind of record
    link    DB FILE                 put standard codes beside own codes

The program holds no class and no property of its own. All of them come from the tables
ontology_term, mapping, relation_type, attribute_def and code.
"""
import argparse
import csv
import re
import sqlite3
import sys
import uuid
from pathlib import Path
from urllib.parse import quote

from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import DCTERMS, OWL, RDF, RDFS, SKOS, XSD

HERE = Path(__file__).resolve().parent
ONTOLOGY_DIR = HERE.parent / "ontology"
SEED_DIR = HERE / "seed"

BASE = "urn:fieldwork:"
FW = Namespace("urn:fieldwork:term:")
PREFIXES = {"rdfs": RDFS, "dcterms": DCTERMS, "owl": OWL, "skos": SKOS, "fw": FW}

ONTOLOGY_FILES = [
    ("CIDOC CRM", "7.1.3", "CIDOC_CRM_v7.1.3.rdf"),
    ("CIDOC CRM property classes", "7.1.3", "CIDOC_CRM_v7.1.3_PC.rdf"),
    ("CRMsci", "3.2", "CRMsci_v3.2.rdf"),
    ("CRMarchaeo", "2.1.1", "CRMarchaeo_v2.1.1.rdf"),
    ("CRMinf", "1.2.1", "CRMinf_v1.2.1.rdf"),
    ("CRMgeo", "2.0.1", "CRMgeo_v2.0.1.rdf"),
]
CODE = re.compile(r"^(PC|AP|SP|E|P|A|S|O|I|J|Q)\d+(\.\d+)?[a-z]?$")

ENTITY_TABLES = ["actor", "place", "period", "activity", "thing", "source", "passage", "media"]
EXTENSIONS = {"context": "thing", "sample": "thing", "analysis": "activity"}
# Tables that hold data of a dataset, in the order of export.
DATA_TABLES = ["dataset", "dataset_actor", "entity", "identifier", "actor", "place", "period", "activity",
               "participation", "thing", "dimension", "source", "passage", "media", "about", "context",
               "find_context", "sample", "analysis", "claim", "claim_basis", "assertion", "dating",
               "geometry", "relation", "attribute_value"]
# Column through which a row belongs to a dataset.
OWNER = {"dataset": "id", "dataset_actor": "dataset", "entity": "id", "identifier": "entity",
         "participation": "activity", "dimension": "entity", "about": "item", "find_context": "thing",
         "claim": "id", "claim_basis": "claim", "assertion": "subject", "dating": "subject",
         "geometry": "entity", "relation": "subject", "attribute_value": "entity"}
STEERING = {"id"}


class Refused(Exception):
    pass


def connect(path):
    con = sqlite3.connect(path, isolation_level=None)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    return con


def new_id():
    return str(uuid.uuid4())


# ───────────────────────────── init ─────────────────────────────

def local(uri):
    return str(uri).rstrip("/").rsplit("/", 1)[-1].rsplit("#", 1)[-1]


def code_of(uri):
    parts = local(uri).split("_")
    if len(parts) > 1 and CODE.match(parts[0]) and CODE.match(parts[1]):
        return parts[0] + "_" + parts[1]          # E33_E41_Linguistic_Appellation
    return parts[0] if CODE.match(parts[0]) else None


def load_ontology(con):
    """Reads the files. Returns the class names that a file uses and that no file defines under that name."""
    sub, renamed = set(), []
    graphs = []
    for name, version, file in ONTOLOGY_FILES:
        g = Graph()
        g.parse(ONTOLOGY_DIR / file)
        ns = ""
        terms = []
        for kind, typ in (("class", RDFS.Class), ("property", RDF.Property)):
            for s in set(g.subjects(RDF.type, typ)):
                c = code_of(s)
                if not c:
                    continue
                if not ns and "cidoc-crm.org" in str(s):
                    ns = str(s)[: len(str(s)) - len(local(s))]
                label = next((str(l) for l in g.objects(s, RDFS.label) if getattr(l, "language", None) == "en"),
                             None) or next((str(l) for l in g.objects(s, RDFS.label)), None)
                dom = next((code_of(o) for o in g.objects(s, RDFS.domain)), None)
                rng = next((o for o in g.objects(s, RDFS.range)), None)
                rng = None if rng is None else (code_of(rng) or "Literal")
                terms.append((c, local(s), kind, name, str(s), label, dom, rng))
        con.execute("INSERT INTO ontology_source VALUES (?,?,?,?)", (name, version, file, ns))
        for t in terms:
            # A later file may repeat a class of an earlier one. The first definition stays.
            con.execute("INSERT OR IGNORE INTO ontology_term (code,name,kind,source,uri,label,domain,range) "
                        "VALUES (?,?,?,?,?,?,?,?)", t)
        graphs.append((name, g))
    # The files are of different dates. One file may name a class by a code that another file
    # has since given to a different class. The name decides, not the code.
    by_name = {r["name"]: r["code"] for r in con.execute("SELECT name, code FROM ontology_term")}
    by_tail = {r["name"].split("_", 1)[1]: r["code"] for r in con.execute(
        "SELECT name, code FROM ontology_term WHERE kind = 'class' AND instr(name, '_') > 0")}

    def resolve(uri, file):
        n = local(uri)
        if n in by_name:
            return by_name[n]
        tail = n.split("_", 1)[1] if "_" in n else None
        if code_of(uri) and tail in by_tail:
            renamed.append(f"{file} writes {n}. Read as {by_tail[tail]}, which is the class of that name")
            return by_tail[tail]
        return None

    for name, g in graphs:
        for s, o in g.subject_objects(RDFS.subClassOf):
            a, b = resolve(s, name), resolve(o, name)
            if a and b:
                sub.add((a, b))
    # Terms from outside the CRM family that the declared lists use.
    con.execute("INSERT INTO ontology_source VALUES ('W3C', 'OWL 2', '-', ?)", (str(OWL),))
    con.execute("INSERT INTO ontology_term (code,name,kind,source,uri,label,domain,range) VALUES "
                "('owl:sameAs','sameAs','property','W3C',?,'same as','E1','E1')", (str(OWL.sameAs),))
    con.execute("UPDATE ontology_term SET inverse_of = substr(code, 1, length(code) - 1) "
                "WHERE kind = 'property' AND code LIKE '%i' "
                "AND substr(code, 1, length(code) - 1) IN (SELECT code FROM ontology_term)")
    classes = [r[0] for r in con.execute("SELECT code FROM ontology_term WHERE kind = 'class'")]
    known = set(classes)
    parents = {}
    for s, o in sub:
        if s in known and o in known:
            parents.setdefault(s, set()).add(o)
    for c in classes:
        seen, todo = {c}, [c]
        while todo:
            for p in parents.get(todo.pop(), ()):
                if p not in seen:
                    seen.add(p)
                    todo.append(p)
        if c != "E1" and not c.startswith("PC"):
            seen.add("E1")
        con.executemany("INSERT INTO ontology_subclass VALUES (?,?)", [(c, s) for s in seen])
    return sorted(set(renamed))


def read_seed(name):
    with open(SEED_DIR / name, encoding="utf-8", newline="") as f:
        return [{k: (v if v != "" else None) for k, v in row.items()} for row in csv.DictReader(f)]


def load_seed(con):
    for r in read_seed("code_lists.csv"):
        con.execute("INSERT INTO code_list VALUES (?,?,?,?)", (r["id"], r["label"], r["module"], r["class"]))
    rows = read_seed("codes.csv")
    for r in rows:
        con.execute("INSERT INTO code (id,list,code,label_en,label_tr,uri) VALUES (?,?,?,?,?,?)",
                    (f"{r['list']}/{r['code']}", r["list"], r["code"], r["label_en"], r["label_tr"], r["uri"]))
    for r in rows:
        if r["parent"]:
            con.execute("UPDATE code SET parent = ? WHERE id = ?",
                        (f"{r['list']}/{r['parent']}", f"{r['list']}/{r['code']}"))
    for r in read_seed("mapping.csv"):
        con.execute("INSERT INTO mapping VALUES (?,?,?,?,?,?,?,?)",
                    (r["table_name"], r["column_name"], int(r["seq"]), r["cond"] or "", r["meaning"],
                     r["path"], r["code_list"], r["ref_class"]))
    for r in read_seed("relation_types.csv"):
        con.execute("INSERT INTO relation_type (code,label_en,label_tr,inverse_label,module,property,domain,"
                    "range,subject_via,object_via,value_kind,code_list,conclusion) VALUES "
                    "(?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (r["code"], r["label_en"], r["label_tr"], r["inverse_label"], r["module"], r["property"],
                     r["domain"], r["range"], r["subject_via"], r["object_via"], r["value_kind"],
                     r["code_list"], int(r["conclusion"])))
    for r in read_seed("attributes.csv"):
        con.execute("INSERT INTO attribute_def (id,label_en,label_tr,applies_to,value_type,unit,code_list,"
                    "description) VALUES (?,?,?,?,?,?,?,?)",
                    (r["id"], r["label_en"], r["label_tr"], r["applies_to"], r["value_type"], r["unit"],
                     r["code_list"], r["description"]))
    for r in read_seed("templates.csv"):
        if r["label_en"]:
            con.execute("INSERT INTO template (id,label_en,label_tr,layout,base_table,base_class,extension) "
                        "VALUES (?,?,?,?,?,?,?)", (r["template"], r["label_en"], r["label_tr"], r["layout"],
                                                   r["base_table"], r["base_class"], r["extension"]))
        con.execute("INSERT INTO template_field (template,position,kind,column_name,attribute,dimension_kind,"
                    "axis,label_en,label_tr) VALUES (?,?,?,?,?,?,?,?,?)",
                    (r["template"], int(r["position"]), r["kind"], r["column_name"], r["attribute"],
                     r["dimension_kind"], r["axis"], r["field_en"], r["field_tr"]))


def make_triggers(con):
    """Checks that follow from the mapping rows: code lists and classes of referenced entities."""
    n = 0
    for t in ENTITY_TABLES:
        con.execute(f"""CREATE TRIGGER {t}_is_registered BEFORE INSERT ON {t} BEGIN
            SELECT RAISE(ABORT, '{t}: the entity is registered for another table')
            WHERE NOT EXISTS (SELECT 1 FROM entity WHERE id = NEW.id AND table_name = '{t}'); END""")
    seen = set()
    for m in con.execute("SELECT DISTINCT table_name, column_name, code_list, ref_class FROM mapping "
                         "WHERE code_list IS NOT NULL OR ref_class IS NOT NULL").fetchall():
        t, c = m["table_name"], m["column_name"]
        for when in ("INSERT", f"UPDATE OF {c}"):
            tag = "ins" if when == "INSERT" else "upd"
            if m["code_list"] and (t, c, "code", tag) not in seen:
                seen.add((t, c, "code", tag))
                con.execute(f"""CREATE TRIGGER {t}_{c}_list_{tag} BEFORE {when} ON {t}
                    WHEN NEW.{c} IS NOT NULL BEGIN
                    SELECT RAISE(ABORT, '{t}.{c}: the code is not from the list {m['code_list']}')
                    WHERE NOT EXISTS (SELECT 1 FROM code WHERE id = NEW.{c} AND list = '{m['code_list']}');
                    SELECT RAISE(ABORT, '{t}.{c}: the code is withdrawn')
                    WHERE EXISTS (SELECT 1 FROM code WHERE id = NEW.{c} AND state = 'withdrawn');
                    END""")
                n += 1
            if m["ref_class"] and (t, c, "class", tag) not in seen:
                seen.add((t, c, "class", tag))
                classes = ",".join(f"'{x}'" for x in m["ref_class"].split("|"))
                con.execute(f"""CREATE TRIGGER {t}_{c}_class_{tag} BEFORE {when} ON {t}
                    WHEN NEW.{c} IS NOT NULL BEGIN
                    SELECT RAISE(ABORT, '{t}.{c}: the entity must be of class {m['ref_class']}')
                    WHERE NOT EXISTS (SELECT 1 FROM entity e JOIN ontology_subclass s ON s.sub = e.class
                                      WHERE e.id = NEW.{c} AND s.super IN ({classes}));
                    END""")
                n += 1
    return n


def cmd_init(args):
    p = Path(args.db)
    if p.exists():
        p.unlink()
    con = connect(p)
    con.executescript((HERE / "schema.sql").read_text(encoding="utf-8"))
    con.execute("BEGIN")
    renamed = load_ontology(con)
    load_seed(con)
    n = make_triggers(con)
    con.commit()
    q = lambda s: con.execute(s).fetchone()[0]
    print(f"tables            {q("SELECT count(*) FROM sqlite_master WHERE type = 'table'")}")
    print(f"ontology classes  {q("SELECT count(*) FROM ontology_term WHERE kind = 'class'")}")
    print(f"ontology props    {q("SELECT count(*) FROM ontology_term WHERE kind = 'property'")}")
    print(f"mapping rows      {q('SELECT count(*) FROM mapping')}")
    print(f"code lists        {q('SELECT count(*) FROM code_list')}, codes {q('SELECT count(*) FROM code')}")
    print(f"relation types    {q('SELECT count(*) FROM relation_type')}")
    print(f"attributes        {q('SELECT count(*) FROM attribute_def')}")
    print(f"templates         {q('SELECT count(*) FROM template')}")
    print(f"generated checks  {n}")
    for r in renamed:
        print(f"note  {r}")


# ───────────────────────────── the path engine ─────────────────────────────

NODE = re.compile(r"^([A-Za-z0-9.\-_]+)\{([a-z_]*)(?:([@=])([a-z_]*))?\}$")


class Exporter:
    def __init__(self, con, dataset=None, skip=None):
        self.con = con
        self.dataset = dataset
        self.skip = skip                       # (table, column) treated as empty, for the audit
        self.g = Graph()
        for k, v in PREFIXES.items():
            self.g.bind(k, v)
        self.terms = {r["code"]: dict(r) for r in con.execute("SELECT * FROM ontology_term")}
        for r in con.execute("SELECT name, namespace FROM ontology_source"):
            if r["namespace"].startswith("http") and "cidoc" in r["namespace"]:
                self.g.bind(re.sub(r"[^a-z]", "", r["name"].lower().replace("cidoc", ""))[:12] or "crm",
                            Namespace(r["namespace"]), replace=True)
        self.supers = {}
        for r in con.execute("SELECT sub, super FROM ontology_subclass"):
            self.supers.setdefault(r["sub"], set()).add(r["super"])
        self.maps = {}
        for r in con.execute("SELECT * FROM mapping ORDER BY table_name, column_name, seq"):
            self.maps.setdefault(r["table_name"], []).append(dict(r))
        self.fks = {}
        for t in DATA_TABLES:
            self.fks[t] = {f["from"]: f["table"] for f in con.execute(f"PRAGMA foreign_key_list({t})")}
        self.entities = {r["id"]: dict(r) for r in con.execute("SELECT * FROM entity")}
        self.claims = {r["id"]: dict(r) for r in con.execute("SELECT * FROM claim")}
        self.codes = {r["id"]: dict(r) for r in con.execute(
            "SELECT c.*, l.class AS class FROM code c JOIN code_list l ON l.id = c.list")}
        self.own = {}
        for r in con.execute("SELECT * FROM own_code"):
            self.own.setdefault(r["own"], []).append((r["standard"], r["match"]))
        self.reltypes = {r["code"]: dict(r) for r in con.execute("SELECT * FROM relation_type")}
        self.attrs = {r["id"]: dict(r) for r in con.execute("SELECT * FROM attribute_def")}
        self.types = {}                        # node -> set of class codes
        self.errors = []

    # ── nodes ──
    def uri(self, *parts):
        return URIRef(BASE + ":".join(quote(str(p), safe="") for p in parts))

    def typed(self, node, cls):
        if cls not in self.terms:
            raise Refused(f"unknown class {cls}")
        if cls not in self.types.setdefault(node, set()):
            self.types[node].add(cls)
            self.g.add((node, RDF.type, URIRef(self.terms[cls]["uri"])))
        return node

    def entity_node(self, eid):
        e = self.entities.get(eid)
        if e is None:
            raise Refused(f"no entity {eid}")
        n = self.typed(self.uri("entity", eid), e["class"])
        return self.typed(n, e["class2"]) if e["class2"] else n

    def table_node(self, table, rid):
        """Node of a row in the table that a column points at."""
        if table in ("entity", *ENTITY_TABLES, *EXTENSIONS):
            return self.entity_node(rid)
        if table == "claim":
            c = self.claims[rid]
            cls = {"inferred": "I5", "adopted": "I7", "recorded": "I1"}[c["kind"]]
            return self.typed(self.uri("claim", rid), cls)
        if table == "dataset":
            return self.typed(self.uri("dataset", rid), "E73")
        if table == "code":
            return self.code_node(rid)
        return self.uri(table, rid)

    def code_node(self, cid):
        c = self.codes.get(cid)
        if c is None:
            raise Refused(f"no code {cid}")
        n = self.uri("code", cid)
        if n not in self.types:
            self.typed(n, c["class"])
            if c["label_en"]:
                self.g.add((n, RDFS.label, Literal(c["label_en"], lang="en")))
            if c["label_tr"]:
                self.g.add((n, RDFS.label, Literal(c["label_tr"], lang="tr")))
            if c["uri"]:
                self.g.add((n, SKOS.exactMatch, URIRef(c["uri"])))
            if c["parent"]:
                self.g.add((n, URIRef(self.terms["P127"]["uri"]), self.code_node(c["parent"])))
            match = {"same": SKOS.exactMatch, "close": SKOS.closeMatch,
                     "wider": SKOS.broadMatch, "narrower": SKOS.narrowMatch}
            for std, m in self.own.get(cid, ()):
                self.g.add((n, match[m], self.code_node(std)))
        return n

    def term_node(self, code, cls="E55"):
        """A class or property of the ontology, or a declared relation type, used as a type."""
        if code in self.reltypes:
            n = self.typed(self.uri("relation_type", code), cls)
            self.g.add((n, RDFS.label, Literal(self.reltypes[code]["label_en"], lang="en")))
            self.g.add((n, SKOS.broadMatch, URIRef(self.terms[self.reltypes[code]["property"]]["uri"])))
            return n
        n = self.typed(self.uri("property_type", code), cls)
        self.g.add((n, SKOS.exactMatch, URIRef(self.terms[code]["uri"])))
        return n

    def attr_node(self, aid):
        a = self.attrs[aid]
        n = self.typed(self.uri("attribute", aid), "S9")
        self.g.add((n, RDFS.label, Literal(a["label_en"], lang="en")))
        if a["label_tr"]:
            self.g.add((n, RDFS.label, Literal(a["label_tr"], lang="tr")))
        return n

    # ── rows ──
    def home(self, table, rid):
        """Table under which the nodes of a row are minted. Extension rows share the entity."""
        return ("entity", rid) if table in ("entity", *ENTITY_TABLES, *EXTENSIONS) else (table, rid)

    def value(self, row, col):
        if self.skip and self.skip == (row["__table"], col):
            return None
        return row.get(col)

    def cls(self, row, col=None):
        """All classes of an entity, with their ancestors."""
        eid = row["id"] if col is None else self.value(row, col)
        e = self.entities.get(eid)
        if e is None:
            return set()
        return self.supers.get(e["class"], set()) | self.supers.get(e["class2"], set())

    def prepare(self, table, r):
        row = dict(r)
        row["__table"] = table
        if "claim" in row:
            c = self.claims.get(self.value(row, "claim"))
            row["belief"] = c["belief"] if c else "true"
            row["claim_kind"] = c["kind"] if c else None
        if table == "attribute_value":
            row["unit"] = self.attrs[row["attribute"]]["unit"]
        return row

    def holds(self, cond, row):
        for part in filter(None, (p.strip() for p in cond.split("&"))):
            neg = part.startswith("!")
            part = part.lstrip("!")
            m = re.match(r"^class(?:\((\w+)\))?<=(\w+)$", part)
            if m:
                ok = m.group(2) in self.cls(row, m.group(1))
            elif part.startswith("has("):
                ok = self.value(row, part[4:-1]) is not None
            elif "!=" in part:
                k, v = part.split("!=")
                ok = str(self.value(row, k)) not in v.split("|")
            else:
                k, v = part.split("=")
                ok = str(self.value(row, k)) in v.split("|")
            if ok == neg:
                return False
        return True

    def row_node(self, table, row):
        for m in self.maps.get(table, ()):
            if m["column_name"] == "*" and self.holds(m["cond"], row):
                p = m["path"]
                if p == "@none":
                    return None
                if p == "@entity":
                    return self.entity_node(row["id"])
                return self.typed(self.uri(*self.home(table, row["id"])), p.split("_")[0])
        return None

    def fragment(self, table, name, row):
        for m in self.maps.get(table, ()):
            if m["column_name"] == name and self.holds(m["cond"], row):
                return m["path"]
        raise Refused(f"{table}: no fragment {name} fits the row {row['id']}")

    def tokens(self, table, path, row):
        out = []
        for t in (x.strip() for x in path.split(" / ")):
            if t.startswith("~"):
                out += self.tokens(table, self.fragment(table, t, row), row)
            else:
                out.append(t)
        return out

    def mint(self, table, row, col, tok, anchor=None):
        """Class{name}, Class{name@column}, Class{name=column}, Class{name@}."""
        m = NODE.match(tok)
        cls, name, op, ref = m.group(1).split("_")[0], m.group(2), m.group(3), m.group(4)
        if op == "=" and self.value(row, ref) is not None:
            return self.table_node(self.fks[table][ref], self.value(row, ref))
        if op == "@":
            if ref == "":
                return self.typed(URIRef(str(anchor) + ":" + name), cls)
            v = self.value(row, ref)
            if v is None:
                raise Refused(f"{table}.{ref} is empty")
            h = self.home(self.fks[table].get(ref, table), v)
            return self.typed(self.uri(*h, name), cls)
        return self.typed(self.uri(*self.home(table, row["id"]), name), cls)

    def emit(self, s, prop, o):
        if ":" in prop:
            pre, name = prop.split(":", 1)
            if pre in PREFIXES:
                self.g.add((s, PREFIXES[pre][name], o))
                return
        code = prop if prop in self.terms else prop.split("_")[0]
        t = self.terms.get(code)
        if t is None or t["kind"] != "property":
            raise Refused(f"unknown property {prop}")
        if t["inverse_of"]:
            if isinstance(o, Literal):
                raise Refused(f"{prop}: an inverse property cannot take a value")
            self.g.add((o, URIRef(self.terms[t["inverse_of"]]["uri"]), s))
        else:
            self.g.add((s, URIRef(t["uri"]), o))

    def literal(self, v):
        if isinstance(v, bool):
            return Literal(v)
        if isinstance(v, int):
            return Literal(v, datatype=XSD.integer)
        if isinstance(v, float):
            return Literal(int(v), datatype=XSD.integer) if v == int(v) else Literal(v, datatype=XSD.decimal)
        return Literal(str(v))

    def target(self, table, row, col, tok):
        m = re.match(r"^@(\w+)(?:\((.*)\))?$", tok)
        if tok.startswith("#"):
            return self.code_node(tok[1:])
        kind, arg = m.group(1), m.group(2)
        if kind == "term":
            return self.term_node(arg)
        c = arg if (arg and kind != "enum") else col
        v = self.value(row, c)
        if v is None:
            return None
        if kind in ("ref", "from"):
            return self.table_node(self.fks[table].get(c, "entity"), v)
        if kind == "code":
            return self.code_node(v)
        if kind == "enum":
            return self.code_node(f"{arg}/{v}")
        if kind == "value":
            return self.literal(v)
        if kind == "uri":
            return URIRef(v)
        if kind == "attr":
            return self.attr_node(v)
        if kind == "reltype":
            return self.term_node(v)
        raise Refused(f"unknown token {tok}")

    def run(self, table, row, col, path):
        if path == "-":
            return
        if path == "@link":
            return self.link(table, row)
        toks = self.tokens(table, path, row)
        cur, i = None, 0
        if toks[0].startswith("@from("):
            cur, i = self.target(table, row, col, toks[0]), 1
        elif NODE.match(toks[0]):
            cur, i = self.mint(table, row, col, toks[0]), 1
        else:
            cur = self.row_node(table, row)
        if cur is None:
            return
        prop, back = None, None
        for tok in toks[i:]:
            if tok == "^":
                cur = back
            elif tok.startswith("+"):
                self.typed(cur, tok[1:].split("_")[0])
            elif prop is None:
                prop = tok
            else:
                nxt = self.mint(table, row, col, tok) if NODE.match(tok) else self.target(table, row, col, tok)
                if nxt is None:
                    return
                self.emit(cur, prop, nxt)
                back, cur, prop = cur, nxt, None
        if prop is not None:
            raise Refused(f"{table}.{col}: the path ends on a property: {path}")

    def via(self, node, path):
        """Walk a path of a relation type from an entity to the node that carries the property."""
        if not path:
            return node
        toks = [t.strip() for t in path.split(" / ")]
        cur = node
        for prop, tok in zip(toks[0::2], toks[1::2]):
            nxt = self.mint(None, {}, None, tok, anchor=node)
            self.emit(cur, prop, nxt)
            cur = nxt
        return cur

    def link(self, table, row):
        """The plain statement of a relation or an assertion. The property comes from the declared lists."""
        key = self.value(row, "property") if table == "assertion" else self.value(row, "type")
        s = self.entity_node(row["subject"])
        if key is None:
            prop = self.value(row, "property")
            if prop is None:
                return
            return self.emit(s, prop, self.entity_node(row["object"]))
        t = self.reltypes[key]
        if table == "relation":
            o = self.entity_node(row["object"])
        elif row["object_entity"] is not None:
            o = self.entity_node(row["object_entity"])
        elif row["object_code"] is not None:
            o = self.code_node(row["object_code"])
        else:
            o = self.literal(row["object_text"])
        s = self.via(s, t["subject_via"])
        if not isinstance(o, Literal):
            o = self.via(o, t["object_via"])
        self.emit(s, t["property"], o)

    # ── export ──
    def in_dataset(self, table, row):
        if self.dataset is None:
            return True
        if table == "dataset":
            return row["id"] == self.dataset
        if table == "claim":
            return row["dataset"] == self.dataset
        if table == "dataset_actor":
            return row["dataset"] == self.dataset
        if table == "claim_basis":
            return self.claims[row["claim"]]["dataset"] == self.dataset
        e = self.entities.get(row[OWNER.get(table, "id")])
        return e is not None and e["dataset"] == self.dataset

    def export(self):
        for table in DATA_TABLES:
            for r in self.con.execute(f"SELECT * FROM {table}"):
                if not self.in_dataset(table, r):
                    continue
                row = self.prepare(table, r)
                self.row_node(table, row)
                for m in self.maps.get(table, ()):
                    c = m["column_name"]
                    if c == "*" or c.startswith("~") or self.value(row, c) is None:
                        continue
                    if not self.holds(m["cond"], row):
                        continue
                    try:
                        self.run(table, row, c, m["path"])
                    except Refused as e:
                        self.errors.append(f"{table}.{c} row {row['id']}: {e}")
        return self.g

    # ── check of the finished graph ──
    def validate(self):
        by_uri = {t["uri"]: t for t in self.terms.values() if t["kind"] == "property"}
        bad = []
        for s, p, o in self.g:
            t = by_uri.get(str(p))
            if t is None:
                continue
            sc = set().union(*(self.supers.get(c, {c}) for c in self.types.get(s, ())))
            if t["domain"] and t["domain"] not in sc:
                bad.append(f"{t['name']}: subject {s} is {sorted(self.types.get(s, []))}, needs {t['domain']}")
            if t["range"] == "Literal":
                if not isinstance(o, Literal):
                    bad.append(f"{t['name']}: object {o} must be a value")
            elif isinstance(o, Literal):
                bad.append(f"{t['name']}: object must be a {t['range']}, found the value {o}")
            else:
                oc = set().union(*(self.supers.get(c, {c}) for c in self.types.get(o, ())))
                if t["range"] and t["range"] not in oc:
                    bad.append(f"{t['name']}: object {o} is {sorted(self.types.get(o, []))}, needs {t['range']}")
        return bad


def cmd_graph(args):
    con = connect(args.db)
    ex = Exporter(con, args.dataset)
    g = ex.export()
    bad = ex.validate()
    g.serialize(args.out, format="turtle")
    print(f"statements {len(g)}  path errors {len(ex.errors)}  against the ontology {len(bad)}")
    for e in (ex.errors + bad)[:40]:
        print("  ", e)
    return 1 if ex.errors or bad else 0


# ───────────────────────────── check ─────────────────────────────

def columns(con, table):
    return [c["name"] for c in con.execute(f"PRAGMA table_info({table})")]


def check_mapping(con):
    """Every column of every data table needs a mapping row. Every term in a path must exist."""
    out = []
    terms = {r["code"]: r["kind"] for r in con.execute("SELECT code, kind FROM ontology_term")}
    lists = {r["id"] for r in con.execute("SELECT id FROM code_list")}
    codes = {r["id"] for r in con.execute("SELECT id FROM code")}
    mapped = {}
    for m in con.execute("SELECT * FROM mapping"):
        mapped.setdefault(m["table_name"], set()).add(m["column_name"])
        where = f"mapping {m['table_name']}.{m['column_name']} #{m['seq']}"
        if m["code_list"] and m["code_list"] not in lists:
            out.append(f"{where}: unknown code list {m['code_list']}")
        for c in (m["ref_class"] or "").split("|"):
            if c and terms.get(c) != "class":
                out.append(f"{where}: unknown class {c}")
        if m["path"] in ("-", "@none", "@entity", "@link"):
            continue
        for tok in (x.strip() for x in m["path"].split(" / ")):
            if tok in ("^",) or tok.startswith("~") or tok.startswith("@"):
                continue
            if tok.startswith("#"):
                if tok[1:] not in codes:
                    out.append(f"{where}: unknown code {tok}")
                continue
            if ":" in tok and tok.split(":")[0] in PREFIXES:
                continue
            n = NODE.match(tok)
            name = (n.group(1) if n else tok).lstrip("+")
            code = name.split("_")[0]
            row = con.execute("SELECT name, kind FROM ontology_term WHERE code = ?", (code,)).fetchone()
            if row is None:
                out.append(f"{where}: unknown term {tok}")
            elif row["name"] != name:
                out.append(f"{where}: {name} is written {row['name']} in the ontology")
    for t in DATA_TABLES:
        for c in columns(con, t):
            if c not in STEERING and c not in mapped.get(t, ()):
                out.append(f"{t}.{c}: no mapping row")
    for t in con.execute("SELECT * FROM relation_type"):
        for via in (t["subject_via"], t["object_via"]):
            for tok in (x.strip() for x in (via or "").split(" / ") if x.strip()):
                n = NODE.match(tok)
                name = n.group(1) if n else tok
                row = con.execute("SELECT name FROM ontology_term WHERE code = ?", (name.split("_")[0],)).fetchone()
                if row is None or row["name"] != name:
                    out.append(f"relation_type {t['code']}: unknown term {tok}")
    return out


def check_data(con):
    out = []
    # A thing cannot lie above itself, however long the chain.
    cyc = con.execute("""
        WITH RECURSIVE walk(start, at, depth) AS (
            SELECT subject, object, 1 FROM relation WHERE type IN ('overlies', 'cuts', 'fills', 'seals')
            UNION
            SELECT w.start, r.object, w.depth + 1 FROM walk w JOIN relation r ON r.subject = w.at
            WHERE r.type IN ('overlies', 'cuts', 'fills', 'seals') AND w.depth < 200)
        SELECT DISTINCT start FROM walk WHERE start = at""").fetchall()
    out += [f"stratigraphy: {r['start']} lies above itself through a chain of relations" for r in cyc]
    for t, c in (("thing", "part_of"), ("place", "part_of"), ("period", "part_of"), ("activity", "part_of")):
        cyc = con.execute(f"""
            WITH RECURSIVE walk(start, at, depth) AS (
                SELECT id, {c}, 1 FROM {t} WHERE {c} IS NOT NULL
                UNION
                SELECT w.start, x.{c}, w.depth + 1 FROM walk w JOIN {t} x ON x.id = w.at
                WHERE x.{c} IS NOT NULL AND w.depth < 200)
            SELECT DISTINCT start FROM walk WHERE start = at""").fetchall()
        out += [f"{t}: {r['start']} is part of itself through a chain" for r in cyc]
    for r in con.execute("""SELECT e.id FROM entity e WHERE NOT EXISTS (
            SELECT 1 FROM actor WHERE id = e.id UNION ALL SELECT 1 FROM place WHERE id = e.id UNION ALL
            SELECT 1 FROM period WHERE id = e.id UNION ALL SELECT 1 FROM activity WHERE id = e.id UNION ALL
            SELECT 1 FROM thing WHERE id = e.id UNION ALL SELECT 1 FROM source WHERE id = e.id UNION ALL
            SELECT 1 FROM passage WHERE id = e.id UNION ALL SELECT 1 FROM media WHERE id = e.id)"""):
        out.append(f"entity {r['id']} is registered and has no row in its table")
    out += [f"foreign key: {tuple(r)}" for r in con.execute("PRAGMA foreign_key_check")]
    return out


DATED = """
        SELECT d.id, d.subject, d.event, c.belief, e.label, e.dataset,
               COALESCE(CASE d.scale WHEN 'CE' THEN d.begin ELSE 1950 - d.begin END,
                        CASE p.scale WHEN 'CE' THEN p.start_earliest ELSE 1950 - p.start_earliest END) AS b,
               COALESCE(CASE d.scale WHEN 'CE' THEN d.end ELSE 1950 - d.end END,
                        CASE p.scale WHEN 'CE' THEN p.end_latest ELSE 1950 - p.end_latest END) AS e
        FROM dating d JOIN claim c ON c.id = d.claim JOIN entity e ON e.id = d.subject
        LEFT JOIN period p ON p.id = d.period
        WHERE c.belief <> 'false'"""


def conflicts(con):
    """Dates that cannot both hold. Both are kept. This only lists them.

    Two cases: two dates for the same event of one thing, and a date in years for a context
    against the period of a find that was found in it.
    """
    rows = [r for r in con.execute(DATED) if r["b"] is not None and r["e"] is not None]
    apart = lambda a, b: a["e"] < b["b"] or b["e"] < a["b"]
    out = []
    for i, a in enumerate(rows):
        for b in rows[i + 1:]:
            if a["subject"] == b["subject"] and a["event"] == b["event"] and apart(a, b):
                out.append(f"{a['dataset']}: two dates for the {a['event']} of '{a['label']}' do not overlap: "
                           f"{a['b']} to {a['e']} and {b['b']} to {b['e']}")
    by_subject = {}
    for r in rows:
        by_subject.setdefault(r["subject"], []).append(r)
    years = con.execute("SELECT subject FROM dating WHERE begin IS NOT NULL").fetchall()
    for y in {r["subject"] for r in years}:
        for f in con.execute("SELECT thing FROM find_context WHERE found_in = ?", (y,)):
            for a in by_subject.get(y, []):
                for b in by_subject.get(f["thing"], []):
                    if apart(a, b):
                        out.append(f"{a['dataset']}: '{a['label']}' is dated {a['b']} to {a['e']}, the find "
                                   f"'{b['label']}' from it {b['b']} to {b['e']}")
    return sorted(set(out))


def depends_on(con, claim):
    """Every claim that rests on this one, directly or through others."""
    return [r["claim"] for r in con.execute("""
        WITH RECURSIVE falls(claim) AS (
            SELECT claim FROM claim_basis WHERE basis_claim = ?
            UNION
            SELECT b.claim FROM claim_basis b JOIN falls f ON b.basis_claim = f.claim)
        SELECT claim FROM falls""", (claim,))]


def cmd_check(args):
    con = connect(args.db)
    a = check_mapping(con)
    b = check_data(con)
    ex = Exporter(con)
    ex.export()
    c = ex.errors + ex.validate()
    print(f"mapping {len(a)}  data {len(b)}  graph {len(c)}")
    for x in (a + b + c)[:60]:
        print("  ", x)
    for x in conflicts(con):
        print(f"   note  {x}")
    for d in con.execute("SELECT id FROM dataset"):
        for x in sum_check(con, d["id"]):
            print(f"   note  {d['id']}: {x}")
    return 1 if a or b or c else 0


def cmd_audit(args):
    con = connect(args.db)
    full = set(Exporter(con).export())
    silent, tested = [], 0
    for t in DATA_TABLES:
        for c in columns(con, t):
            test = "= 1" if c == "approx" else "IS NOT NULL"
            if c in STEERING or not con.execute(f"SELECT 1 FROM {t} WHERE {c} {test} LIMIT 1").fetchone():
                continue
            paths = [m["path"] for m in con.execute(
                "SELECT path FROM mapping WHERE table_name = ? AND column_name = ?", (t, c))]
            tested += 1
            if set(Exporter(con, skip=(t, c)).export()) == full:
                silent.append((t, c, "steers other paths only" if paths == ["-"] else "LOST"))
    print(f"columns with data {tested}  silent {len(silent)}")
    for t, c, why in silent:
        print(f"   {t}.{c}: {why}")
    return 1 if any(w == "LOST" for _, _, w in silent) else 0


# ───────────────────────────── levels ─────────────────────────────

def levels(con, dataset):
    """Statements by level. 1 typed, 2 template, 3 own, 4 text."""
    n = {1: 0, 2: 0, 3: 0, 4: 0}
    detail = {}

    def add(level, what, k=1):
        if k:
            n[level] += k
            detail[(level, what)] = detail.get((level, what), 0) + k

    own_unlinked = {r["id"] for r in con.execute(
        "SELECT id FROM code WHERE owner IS NOT NULL AND id NOT IN (SELECT own FROM own_code)")}
    code_cols = {(m["table_name"], m["column_name"]) for m in con.execute(
        "SELECT table_name, column_name FROM mapping WHERE code_list IS NOT NULL")}
    ex = Exporter(con, dataset)
    for t in DATA_TABLES:
        if t in ("dataset", "dataset_actor"):
            continue
        cols = [c for c in columns(con, t) if c not in ("id", "dataset", "table_name", "approx")]
        for r in con.execute(f"SELECT * FROM {t}"):
            if not ex.in_dataset(t, r):
                continue
            if t == "attribute_value":
                own = ex.attrs[r["attribute"]]["owner"] is not None
                add(3 if own else 2, "own attribute" if own else "declared attribute")
                if r["value_code"] in own_unlinked:
                    add(3, "own code without a standard code")
                if r["remark"]:
                    add(4, "remark")
                continue
            if t == "relation":
                add(1 if r["type"] else 3, "declared relation" if r["type"] else "property taken from the ontology")
                if r["remark"]:
                    add(4, "remark")
                continue
            if t in ("assertion", "dating", "dimension", "geometry", "find_context", "participation",
                     "identifier", "about", "claim_basis"):
                add(1, t)
                for c in cols:
                    if r[c] in own_unlinked and (t, c) in code_cols | {("assertion", "object_code")}:
                        add(3, "own code without a standard code")
                if "remark" in cols and r["remark"]:
                    add(4, "remark")
                continue
            if t == "claim":
                if r["remark"]:
                    add(4, "remark")
                continue
            for c in cols:
                v = r[c]
                if v is None or c == "source_id":
                    continue
                if c == "remark":
                    add(4, "remark")
                elif (t, c) in code_cols and v in own_unlinked:
                    add(3, "own code without a standard code")
                else:
                    add(1, f"{t}.{c}")
    return n, detail


def cmd_levels(args):
    con = connect(args.db)
    names = {1: "typed", 2: "template", 3: "own", 4: "text"}
    for d in con.execute("SELECT id FROM dataset ORDER BY id").fetchall():
        n, detail = levels(con, d["id"])
        total = sum(n.values()) or 1
        print(f"\n{d['id']}: {sum(n.values())} statements")
        for k in (1, 2, 3, 4):
            print(f"   level {k} {names[k]:9} {n[k]:6}  {100 * n[k] / total:5.1f} %")
        print(f"   levels 1 and 2       {n[1] + n[2]:6}  {100 * (n[1] + n[2]) / total:5.1f} %")
        if args.detail:
            for (k, what), v in sorted(detail.items(), key=lambda x: (x[0][0], -x[1])):
                print(f"      {k}  {v:5}  {what}")


# ───────────────────────────── sheets ─────────────────────────────

BELIEF_MARK = {"?": "possible", "(?)": "possible", "??": "possible"}


class Loader:
    """Writes rows. An unknown term never stops the entry. It becomes an own code of the dataset."""

    def __init__(self, con, dataset):
        self.con, self.dataset = con, dataset
        self.lists = {(m["table_name"], m["column_name"]): m["code_list"] for m in con.execute(
            "SELECT table_name, column_name, code_list FROM mapping WHERE code_list IS NOT NULL")}

    def entity(self, table, cls, label=None, source_id=None, remark=None, eid=None, class2=None, **cols):
        eid = eid or new_id()
        self.con.execute("INSERT INTO entity (id,dataset,table_name,class,class2,source_id,label,remark) "
                         "VALUES (?,?,?,?,?,?,?,?)", (eid, self.dataset, table, cls, class2, source_id, label, remark))
        self.insert(table, id=eid, **cols)
        return eid

    def insert(self, table, **cols):
        cols = {k: v for k, v in cols.items() if v is not None}
        if "id" not in cols and "id" in columns(self.con, table):
            cols["id"] = new_id()
        for k in list(cols):
            if (table, k) in self.lists:
                cols[k] = self.code(self.lists[(table, k)], cols[k])
        self.con.execute(f"INSERT INTO {table} ({','.join(cols)}) VALUES ({','.join('?' * len(cols))})",
                         list(cols.values()))
        return cols.get("id")

    def code(self, lst, text):
        """A code, a label in either language, or a new own code."""
        text = str(text).strip()
        r = self.con.execute(
            "SELECT id FROM code WHERE list = ? AND (owner IS NULL OR owner = ?) AND "
            "(id = ? OR code = ? OR lower(label_en) = lower(?) OR lower(label_tr) = lower(?)) "
            "ORDER BY owner IS NOT NULL", (lst, self.dataset, text, text, text, text)).fetchone()
        if r:
            return r["id"]
        cid = f"{lst}/{self.dataset}/{text}"
        self.con.execute("INSERT INTO code (id,list,code,label_tr,owner) VALUES (?,?,?,?,?)",
                         (cid, lst, text, text, self.dataset))
        return cid

    def find(self, text, tables=None):
        """An entity of the dataset by its own number or its name."""
        q = "SELECT id FROM entity WHERE dataset = ? AND (id = ? OR source_id = ? OR label = ?)"
        rows = [r["id"] for r in self.con.execute(q, (self.dataset, text, text, text))]
        if tables:
            rows = [r for r in rows if self.con.execute(
                "SELECT table_name FROM entity WHERE id = ?", (r,)).fetchone()[0] in tables]
        if len(rows) > 1:
            raise Refused(f"'{text}' names {len(rows)} entities. Use the own number")
        return rows[0] if rows else None

    def claim(self, belief="true", kind="recorded", **cols):
        return self.insert("claim", dataset=self.dataset, kind=kind, belief=belief, **cols)

    def period(self, name):
        name, belief = name.strip(), "true"
        for mark, b in BELIEF_MARK.items():
            if name.endswith(mark):
                name, belief = name[: -len(mark)].strip(), b
                break
        pid = self.find(name, ["period"]) or self.entity("period", "E4", label=name)
        return pid, belief


def template(con, tid):
    t = con.execute("SELECT * FROM template WHERE id = ?", (tid,)).fetchone()
    if t is None:
        raise Refused(f"no template {tid}")
    return t, con.execute("SELECT * FROM template_field WHERE template = ? ORDER BY position", (tid,)).fetchall()


def cmd_sheet(args):
    con = connect(args.db)
    t, fields = template(con, args.template)
    lang = "label_tr" if args.lang == "tr" else "label_en"
    with open(args.out, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";")
        if t["layout"] == "matrix":
            ax = {x["axis"]: x for x in fields}
            w.writerow([f"{ax['row'][lang]} \\ {ax['column'][lang]}", "...", "Toplam" if args.lang == "tr" else "Total"])
        else:
            w.writerow([x[lang] or x["label_en"] for x in fields])
    print(f"{args.out}: {t['layout']} sheet, {len(fields)} fields")


def read_sheet(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        text = f.read()
    delim = ";" if text.splitlines()[0].count(";") >= text.splitlines()[0].count(",") else ","
    return [r for r in csv.reader(text.splitlines(), delimiter=delim) if any(c.strip() for c in r)]


def number(text):
    return float(str(text).strip().replace(",", "."))


def fill_list(con, L, t, fields, rows, under):
    head = rows[0]
    labels = {}
    for x in fields:
        for k in ("label_en", "label_tr"):
            if x[k]:
                labels[x[k].strip().lower()] = x
    own_cols = [h for h in head if h.strip().lower() not in labels]
    base_cols = columns(con, t["base_table"])
    ext_cols = columns(con, t["extension"]) if t["extension"] else []
    made = 0
    for r in rows[1:]:
        cells = {h: (r[i].strip() if i < len(r) else "") for i, h in enumerate(head)}
        ent, base, ext, later = {}, {}, {}, []
        for h, v in cells.items():
            if v == "":
                continue
            x = labels.get(h.strip().lower())
            if x is None:
                later.append(("own", h, v))
            elif x["kind"] == "column":
                c = x["column_name"]
                if c in ("label", "source_id", "remark"):
                    ent[c] = v
                elif c in ext_cols:
                    ext[c] = v
                elif c in base_cols:
                    base[c] = v
                else:
                    raise Refused(f"template {t['id']}: no column {c}")
            else:
                later.append((x["kind"], x, v))
        for side, table in ((base, t["base_table"]), (ext, t["extension"])):
            for c, v in list(side.items()):
                if (table, c) not in L.lists:
                    target = L.find(v)
                    if target is None:
                        raise Refused(f"row {made + 2}: '{v}' in {c} is not known. Enter it first")
                    side[c] = target
        if under and "part_of" in base_cols and "part_of" not in base:
            base["part_of"] = under
        eid = L.entity(t["base_table"], t["base_class"], **ent, **base)
        if t["extension"]:
            L.insert(t["extension"], id=eid, **ext)
        for kind, x, v in later:
            if kind == "own":
                aid = f"{L.dataset}/{x.strip()}"
                try:
                    val, typ = number(v), "decimal"
                except ValueError:
                    val, typ = v, "text"
                old = con.execute("SELECT value_type FROM attribute_def WHERE id = ?", (aid,)).fetchone()
                if old is None:
                    con.execute("INSERT INTO attribute_def (id,label_en,label_tr,applies_to,value_type,owner) "
                                "VALUES (?,?,?,?,?,?)", (aid, x.strip(), x.strip(), "E1", typ, L.dataset))
                elif old["value_type"] == "text":
                    val, typ = v, "text"
                elif typ == "text":
                    raise Refused(f"row {made + 2}: column '{x}' held numbers so far, now '{v}'")
                L.insert("attribute_value", entity=eid, attribute=aid,
                         value_number=val if typ != "text" else None, value_text=val if typ == "text" else None)
            elif kind == "attribute":
                a = con.execute("SELECT * FROM attribute_def WHERE id = ?", (x["attribute"],)).fetchone()
                if a["value_type"] == "code":
                    L.insert("attribute_value", entity=eid, attribute=a["id"], value_code=L.code(a["code_list"], v))
                elif a["value_type"] == "text":
                    L.insert("attribute_value", entity=eid, attribute=a["id"], value_text=v)
                elif a["value_type"] == "yesno":
                    yes = v.lower() in ("1", "yes", "evet", "var", "x", "true", "e")
                    L.insert("attribute_value", entity=eid, attribute=a["id"], value_number=1 if yes else 0)
                else:
                    L.insert("attribute_value", entity=eid, attribute=a["id"], value_number=number(v))
            elif kind == "dimension":
                L.insert("dimension", entity=eid, kind=x["dimension_kind"], value=number(v), unit="unit/piece"
                         if x["dimension_kind"].startswith("dimension_kind/count") else None)
            elif kind == "found_in":
                target = L.find(v)
                if target is None:
                    raise Refused(f"row {made + 2}: context '{v}' is not known. Enter the contexts first")
                L.insert("find_context", thing=eid, found_in=target)
            elif kind == "dating":
                pid, belief = L.period(v)
                L.insert("dating", subject=eid, event=x["column_name"], period=pid, claim=L.claim(belief))
            elif kind == "geometry":
                k = "point" if v.upper().startswith("POINT") else "line" if v.upper().startswith("LINE") else "polygon"
                L.insert("geometry", entity=eid, kind=k, wkt=v.upper().split("(")[0] + "(" + v.split("(", 1)[1],
                         crs=f"crs/{x['column_name']}")
            elif kind == "identifier":
                L.insert("identifier", entity=eid, type=f"identifier_type/{x['column_name']}", value=v)
        made += 1
    return made


TOTAL = {"toplam", "total", "genel toplam", "sum"}


def fill_matrix(con, L, t, fields, rows, under, label):
    """A table of counts. Every cell becomes an assemblage with a count. Printed totals are kept as printed."""
    ax = {x["axis"]: x for x in fields}
    kind = ax["cell"]["dimension_kind"]
    head = [h.strip() for h in rows[0]]
    whole = L.entity(t["base_table"], t["base_class"], label=label or t["label_en"], type="assemblage",
                     part_of=under)

    def axis_cols(x, v):
        if x["kind"] == "column":
            return {x["column_name"]: v}, None
        return {}, (x, v)

    def part(name, parent, *settings):
        cols, extra = {}, []
        for x, v in settings:
            c, e = axis_cols(x, v)
            cols.update(c)
            if e:
                extra.append(e)
        eid = L.entity(t["base_table"], t["base_class"], label=name, part_of=parent, **cols)
        for x, v in extra:
            if x["kind"] == "dating":
                pid, belief = L.period(v)
                L.insert("dating", subject=eid, event=x["column_name"], period=pid, claim=L.claim(belief))
            elif x["kind"] == "attribute":
                L.insert("attribute_value", entity=eid, attribute=x["attribute"], value_text=v)
        return eid

    made = 0
    # The table cuts the whole in two ways. Rows are parts of the whole. Columns are counted with it.
    col_parts = {}
    for h in head[1:]:
        if h and h.lower() not in TOTAL:
            col_parts[h] = part(h, None, (ax["column"], h))
            L.insert("relation", subject=col_parts[h], type="counted_with", object=whole)
    for r in rows[1:]:
        name = r[0].strip()
        if name.lower() in TOTAL:
            for i, v in enumerate(r[1:], 1):
                if not v.strip() or i >= len(head):
                    continue
                target = whole if head[i].lower() in TOTAL else col_parts[head[i]]
                L.insert("dimension", entity=target, kind="dimension_kind/count_printed", value=number(v),
                         unit="unit/piece")
            continue
        row_part = part(name, whole, (ax["row"], name))
        for i, v in enumerate(r[1:], 1):
            if not v.strip() or i >= len(head) or v.strip() in ("-", "–"):
                continue
            if head[i].lower() in TOTAL:
                L.insert("dimension", entity=row_part, kind="dimension_kind/count_printed", value=number(v), unit="unit/piece")
                continue
            cell = part(f"{name}, {head[i]}", row_part, (ax["row"], name), (ax["column"], head[i]))
            L.insert("dimension", entity=cell, kind=kind, value=number(v), unit="unit/piece")
            L.insert("relation", subject=cell, type="counted_with", object=col_parts[head[i]])
            made += 1
    return made


def cmd_fill(args):
    con = connect(args.db)
    t, fields = template(con, args.template)
    rows = read_sheet(args.file)
    con.execute("BEGIN")
    con.execute("PRAGMA defer_foreign_keys = ON")
    L = Loader(con, args.dataset)
    try:
        if t["layout"] == "matrix":
            n = fill_matrix(con, L, t, fields, rows, args.under, args.label)
        else:
            n = fill_list(con, L, t, fields, rows, args.under)
        con.commit()
    except (Refused, sqlite3.IntegrityError, ValueError) as e:
        con.rollback()
        print(f"refused, nothing was stored: {e}")
        return 1
    print(f"{n} rows stored from {args.file}")


def sum_check(con, dataset):
    """Printed totals against the sum of their parts. A part counts with its own printed total if it has one."""
    out = []
    own = """COALESCE((SELECT value FROM dimension WHERE entity = t.id AND kind = 'dimension_kind/count_printed'),
                      (SELECT value FROM dimension WHERE entity = t.id AND kind = 'dimension_kind/count'))"""
    for r in con.execute(f"""
        SELECT e.id, e.label, d.value AS printed,
               (SELECT sum({own}) FROM thing t WHERE t.part_of = e.id) AS parts,
               (SELECT sum({own}) FROM thing t JOIN relation r ON r.subject = t.id
                 WHERE r.type = 'counted_with' AND r.object = e.id) AS counted
        FROM entity e JOIN dimension d ON d.entity = e.id AND d.kind = 'dimension_kind/count_printed'
        WHERE e.dataset = ?""", (dataset,)):
        for v in (r["parts"], r["counted"]):
            if v is not None and v != r["printed"]:
                out.append(f"'{r['label']}': the printed total is {r['printed']:g}, the parts sum to {v:g}")
    return out


# ───────────────────────────── the excavator's view ─────────────────────────────

def cmd_view(args):
    """One wide table per kind of record. Everything stored about a row appears in its line."""
    con = connect(args.db)
    ds, lang = args.dataset, ("label_tr" if args.lang == "tr" else "label_en")
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    codes = {r["id"]: (r[lang] or r["label_en"] or r["label_tr"]) for r in con.execute("SELECT * FROM code")}
    ents = {r["id"]: dict(r) for r in con.execute("SELECT * FROM entity")}
    name = lambda i: (ents[i]["label"] or ents[i]["source_id"] or i) if i in ents else i
    lists = {(m["table_name"], m["column_name"]) for m in con.execute(
        "SELECT table_name, column_name FROM mapping WHERE code_list IS NOT NULL")}
    claims = {r["id"]: dict(r) for r in con.execute("SELECT * FROM claim")}
    mark = {"true": "", "probable": " (probable)", "possible": " (possible)", "false": " (NOT)"}

    def sure(cid):
        return mark[claims[cid]["belief"]] if cid in claims else ""

    facts = {}                                         # entity -> header -> list of texts

    def put(eid, head, text):
        if text is not None and str(text) != "":
            facts.setdefault(eid, {}).setdefault(head, []).append(str(text))

    def show(table, col, v):
        if (table, col) in lists:
            return codes.get(v, v)
        return name(v) if v in ents else v

    for t in ENTITY_TABLES + list(EXTENSIONS):
        for r in con.execute(f"SELECT * FROM {t}"):
            if ents[r["id"]]["dataset"] != ds:
                continue
            for c in r.keys():
                if c != "id" and r[c] is not None and not (c == "approx" and r[c] == 0):
                    put(r["id"], c, show(t, c, r[c]))
    labels = {r["code"]: dict(r) for r in con.execute("SELECT * FROM relation_type")}
    attrs = {r["id"]: dict(r) for r in con.execute("SELECT * FROM attribute_def")}
    for r in con.execute("SELECT * FROM identifier"):
        put(r["entity"], f"number: {codes[r['type']]}", r["value"])
    for r in con.execute("SELECT * FROM dimension"):
        v = f"{r['value']:g}" if r["value"] is not None else f"{r['value_min'] or ''} to {r['value_max'] or ''}"
        put(r["entity"], f"measure: {codes[r['kind']]}",
            f"{'about ' if r['approx'] else ''}{v} {codes.get(r['unit'], '')}".strip())
    for r in con.execute("SELECT * FROM attribute_value"):
        a = attrs[r["attribute"]]
        v = r["value_text"] if r["value_text"] is not None else codes.get(r["value_code"]) if r["value_code"] \
            else (("yes" if r["value_number"] else "no") if a["value_type"] == "yesno" else f"{r['value_number']:g}")
        put(r["entity"], f"{'own' if a['owner'] else 'attribute'}: {a[lang] or a['label_en']}", v + sure(r["claim"]))
    for r in con.execute("SELECT d.*, p.id AS pid FROM dating d LEFT JOIN period p ON p.id = d.period"):
        v = name(r["pid"]) if r["pid"] else ""
        if r["begin"] is not None or r["end"] is not None:
            v = f"{v} {r['begin']} to {r['end']} {r['scale']}".strip()
        put(r["subject"], f"date of {r['event']}", v + sure(r["claim"]))
    for r in con.execute("SELECT * FROM find_context"):
        put(r["thing"], "found in", (name(r["found_in"]) if r["found_in"] else "") + sure(r["claim"]))
        put(r["thing"], "found by", name(r["found_by"]) if r["found_by"] else None)
    for r in con.execute("SELECT * FROM relation"):
        head = labels[r["type"]]["label_en"] if r["type"] else f"ontology: {r['property']}"
        put(r["subject"], f"link: {head}", name(r["object"]) + sure(r["claim"]))
    for r in con.execute("SELECT * FROM assertion"):
        v = name(r["object_entity"]) if r["object_entity"] else codes.get(r["object_code"]) or r["object_text"]
        put(r["subject"], f"stated: {labels[r['property']]['label_en']}", v + sure(r["claim"]))
    for r in con.execute("SELECT * FROM participation"):
        put(r["activity"], "people", f"{name(r['actor'])} ({codes.get(r['role'], '')})")
    for r in con.execute("SELECT * FROM geometry"):
        put(r["entity"], f"coordinates {codes[r['crs']]}", r["wkt"])
    for r in con.execute("SELECT * FROM about"):
        put(r["target"], "shown or described in", name(r["item"]))
    n = 0
    for t in ENTITY_TABLES:
        rows = [e for e in ents.values() if e["dataset"] == ds and e["table_name"] == t]
        if not rows:
            continue
        heads = []
        for e in rows:
            for h in facts.get(e["id"], {}):
                if h not in heads:
                    heads.append(h)
        with open(out / f"{ds}_{t}.csv", "w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f, delimiter=";")
            w.writerow(["own number", "name", "class", "second class"] + heads + ["remark"])
            for e in rows:
                w.writerow([e["source_id"], e["label"], e["class"], e["class2"]]
                           + ["; ".join(facts.get(e["id"], {}).get(h, [])) for h in heads] + [e["remark"]])
        n += 1
        print(f"   {out / f'{ds}_{t}.csv'}: {len(rows)} rows, {len(heads) + 5} columns")
    return 0


def cmd_link(args):
    """Put standard codes beside own codes. FILE has the columns list;own;standard;match."""
    con = connect(args.db)
    made = 0
    with open(args.file, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f, delimiter=";"):
            for o in con.execute("SELECT id FROM code WHERE list = ? AND code = ? AND owner IS NOT NULL",
                                 (r["list"], r["own"])).fetchall():
                con.execute("INSERT OR IGNORE INTO own_code VALUES (?,?,?)",
                            (o["id"], f"{r['list']}/{r['standard']}", r["match"]))
                made += 1
    con.commit()
    print(f"{made} own codes linked to a standard code")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("init", "check", "audit"):
        sub.add_parser(name).add_argument("db")
    p = sub.add_parser("graph"); p.add_argument("db"); p.add_argument("-d", "--dataset"); p.add_argument("-o", "--out", required=True)
    p = sub.add_parser("levels"); p.add_argument("db"); p.add_argument("--detail", action="store_true")
    p = sub.add_parser("sheet"); p.add_argument("db"); p.add_argument("template"); p.add_argument("-o", "--out", required=True); p.add_argument("--lang", default="tr")
    p = sub.add_parser("view"); p.add_argument("db"); p.add_argument("dataset"); p.add_argument("-o", "--out", required=True); p.add_argument("--lang", default="tr")
    p = sub.add_parser("link"); p.add_argument("db"); p.add_argument("file")
    p = sub.add_parser("fill"); p.add_argument("db"); p.add_argument("template"); p.add_argument("dataset"); p.add_argument("file"); p.add_argument("--under"); p.add_argument("--label")
    args = ap.parse_args()
    return globals()[f"cmd_{args.cmd}"](args)


if __name__ == "__main__":
    sys.exit(main() or 0)
