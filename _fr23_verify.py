"""FR-23 test verification script."""
import sys
sys.path.insert(0, "03-development/src")

from omnibot.schema import PHASE2_TABLE_DEFS, get_phase2_schema_sql, get_schema_sql, TABLE_DEFS

errors = []

# Test 1
if len(PHASE2_TABLE_DEFS) != 2:
    errors.append(f"T1: Expected 2 entries, got {len(PHASE2_TABLE_DEFS)}")

# Test 2
names = {name for name, _ in PHASE2_TABLE_DEFS}
if names != {"emotion_history", "edge_cases"}:
    errors.append(f"T2: Got {names}")

# Test 3-6: SQL contents
sql = get_phase2_schema_sql()
if "CREATE TABLE IF NOT EXISTS emotion_history" not in sql:
    errors.append("T3: emotion_history CREATE missing")
if "CREATE TABLE IF NOT EXISTS edge_cases" not in sql:
    errors.append("T4: edge_cases CREATE missing")
if "CREATE INDEX IF NOT EXISTS idx_kb_embeddings" not in sql:
    errors.append("T5: ivfflat index missing")
elif "USING ivfflat" not in sql or "vector_cosine_ops" not in sql or "lists = 100" not in sql:
    errors.append("T5: ivfflat index details missing")
if "CREATE INDEX IF NOT EXISTS idx_emotion_history_user_time" not in sql:
    errors.append("T6: emotion idx missing")
elif "unified_user_id, created_at DESC" not in sql:
    errors.append("T6: emotion idx columns wrong")

# Test 7-8: No duplication
phase1_names = {name for name, _ in TABLE_DEFS}
for name in phase1_names:
    if f"CREATE TABLE IF NOT EXISTS {name}" in sql:
        errors.append(f"T7: Phase1 table {name} leaked into Phase2 SQL")
if not phase1_names.isdisjoint(names):
    errors.append("T8: Phase1/Phase2 table name overlap")

# Test 9-10: emotion_history columns + constraints
emotion_ddl = dict(PHASE2_TABLE_DEFS)["emotion_history"]
for col in ["id SERIAL PRIMARY KEY", "unified_user_id UUID", "conversation_id INTEGER",
            "category VARCHAR(20)", "intensity FLOAT", "created_at TIMESTAMPTZ"]:
    if col not in emotion_ddl:
        errors.append(f"T9: Missing emotion column: {col}")
constraints = [
    "unified_user_id UUID NOT NULL REFERENCES users(unified_user_id)",
    "conversation_id INTEGER NOT NULL REFERENCES conversations(id)",
    "category VARCHAR(20) NOT NULL",
    "CHECK (category IN ('positive', 'neutral', 'negative'))",
    "intensity FLOAT NOT NULL",
    "CHECK (intensity >= 0 AND intensity <= 1)",
    "created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()",
]
for c in constraints:
    if c not in emotion_ddl:
        errors.append(f"T10: Missing constraint: {c}")

# Test 11-12: edge_cases columns + constraints
edge_ddl = dict(PHASE2_TABLE_DEFS)["edge_cases"]
for col in ["id SERIAL PRIMARY KEY", "query TEXT", "expected_intent VARCHAR(50)",
            "expected_answer TEXT", "status VARCHAR(20)", "annotated_at TIMESTAMPTZ",
            "used_in_regression BOOLEAN"]:
    if col not in edge_ddl:
        errors.append(f"T11: Missing edge column: {col}")
edge_constraints = [
    "query TEXT NOT NULL",
    "status VARCHAR(20) DEFAULT 'pending'",
    "CHECK (status IN ('pending', 'approved', 'rejected'))",
    "used_in_regression BOOLEAN DEFAULT FALSE",
]
for c in edge_constraints:
    if c not in edge_ddl:
        errors.append(f"T12: Missing edge constraint: {c}")

# Test 13: return types
result = get_phase2_schema_sql()
if not isinstance(result, str) or len(result) == 0:
    errors.append("T13: get_phase2_schema_sql() not str or empty")
p1 = get_schema_sql()
if not isinstance(p1, str) or "CREATE TABLE IF NOT EXISTS users" not in p1:
    errors.append("T13: get_schema_sql() invalid")

if errors:
    for e in errors:
        print(f"FAIL: {e}")
    sys.exit(1)
else:
    print("ALL 13 TESTS PASSED")
