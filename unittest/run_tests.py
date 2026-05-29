"""
run_tests.py — Script chạy test thủ công, không cần pytest.
Output kết quả ra console và file.
"""
import sys
import os
import json
from unittest.mock import patch, MagicMock
from io import StringIO

# Setup path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "source", "backend")))
os.environ["GROQ_API_KEY"] = "gsk_test_fake_key_for_testing"

results = []

def test(name, fn):
    try:
        fn()
        results.append(("PASS", name))
        print(f"  ✓ PASS  {name}")
    except Exception as e:
        results.append(("FAIL", name, str(e)))
        print(f"  ✗ FAIL  {name}")
        print(f"         {e}")


# ── test_utils ─────────────────────────────────────────────────────────────────
print("\n[test_utils]")
from utils import extract_json, safe_json_parse

def t_raw_array():
    r = extract_json('[{"id": 1, "level": "biết"}]')
    assert isinstance(r, list) and r[0]["level"] == "biết"
test("extract_json: raw JSON array", t_raw_array)

def t_code_block():
    r = extract_json('```json\n[{"id": 1}]\n```')
    assert r[0]["id"] == 1
test("extract_json: JSON in code block", t_code_block)

def t_code_block_nolang():
    r = extract_json('```\n{"key": "value"}\n```')
    assert r["key"] == "value"
test("extract_json: code block no lang tag", t_code_block_nolang)

def t_raises():
    try:
        extract_json("không phải JSON")
        assert False, "Should have raised"
    except json.JSONDecodeError:
        pass
test("extract_json: raises on invalid JSON", t_raises)

def t_safe_valid():
    r = safe_json_parse('{"x": 1}')
    assert r == {"x": 1}
test("safe_json_parse: returns parsed on valid", t_safe_valid)

def t_safe_fallback():
    r = safe_json_parse("invalid json", fallback=[])
    assert r == []
test("safe_json_parse: returns fallback on invalid", t_safe_fallback)

def t_safe_none():
    r = safe_json_parse("bad")
    assert r is None
test("safe_json_parse: default fallback is None", t_safe_none)


# ── test_topics ────────────────────────────────────────────────────────────────
print("\n[test_topics]")
from topics import TOPICS, get_topic_by_id

def t_topics_count():
    assert len(TOPICS) == 7
test("TOPICS: có đúng 7 chủ đề", t_topics_count)

def t_topics_fields():
    for t in TOPICS:
        assert "id" in t and "name" in t and "knowledge" in t
        assert len(t["knowledge"]) >= 3
test("TOPICS: mỗi chủ đề có đủ fields và >=3 kiến thức", t_topics_fields)

def t_get_topic_by_id():
    t = get_topic_by_id("T1")
    assert t is not None and t["name"] == "Số tự nhiên"
test("get_topic_by_id: tìm T1 đúng", t_get_topic_by_id)

def t_get_topic_not_found():
    assert get_topic_by_id("T99") is None
test("get_topic_by_id: trả None nếu không tìm thấy", t_get_topic_not_found)


# ── test_problem_generator ─────────────────────────────────────────────────────
print("\n[test_problem_generator]")
from agents.problem_generator import ProblemGenerator

SAMPLE_PROBLEMS = [
    {"id": 1, "level": "biết",     "question": "Đề 1", "hint": "Gợi ý 1"},
    {"id": 2, "level": "hiểu",     "question": "Đề 2", "hint": "Gợi ý 2"},
    {"id": 3, "level": "vận_dụng", "question": "Đề 3", "hint": "Gợi ý 3"},
    {"id": 4, "level": "biết",     "question": "Đề 4", "hint": "Gợi ý 4"},
    {"id": 5, "level": "hiểu",     "question": "Đề 5", "hint": "Gợi ý 5"},
    {"id": 6, "level": "vận_dụng", "question": "Đề 6", "hint": "Gợi ý 6"},
]
T1 = {"id": "T1", "name": "Số tự nhiên", "description": "...", "knowledge": ["Đọc số"]}

def _mock_groq(content):
    mc = MagicMock()
    mr = MagicMock()
    mr.choices[0].message.content = content
    mc.chat.completions.create.return_value = mr
    return mc

def t_gen_returns_list():
    with patch("agents.problem_generator.Groq") as m:
        m.return_value = _mock_groq(json.dumps(SAMPLE_PROBLEMS))
        gen = ProblemGenerator()
        r = gen.generate(T1)
        assert isinstance(r, list) and len(r) == 6
test("ProblemGenerator.generate: trả list 6 bài", t_gen_returns_list)

def t_gen_required_fields():
    with patch("agents.problem_generator.Groq") as m:
        m.return_value = _mock_groq(json.dumps(SAMPLE_PROBLEMS))
        gen = ProblemGenerator()
        r = gen.generate(T1)
        for p in r:
            assert "id" in p and "level" in p and "question" in p and "hint" in p
test("ProblemGenerator.generate: mỗi bài có id/level/question/hint", t_gen_required_fields)

def t_gen_all_levels():
    with patch("agents.problem_generator.Groq") as m:
        m.return_value = _mock_groq(json.dumps(SAMPLE_PROBLEMS))
        gen = ProblemGenerator()
        r = gen.generate(T1)
        levels = {p["level"] for p in r}
        assert {"biết", "hiểu", "vận_dụng"} == levels
test("ProblemGenerator.generate: có đủ 3 cấp độ", t_gen_all_levels)

def t_gen_code_block():
    content = f"```json\n{json.dumps(SAMPLE_PROBLEMS)}\n```"
    with patch("agents.problem_generator.Groq") as m:
        m.return_value = _mock_groq(content)
        gen = ProblemGenerator()
        r = gen.generate(T1)
        assert len(r) == 6
test("ProblemGenerator.generate: xử lý JSON trong code block", t_gen_code_block)

def t_gen_retry():
    with patch("agents.problem_generator.Groq") as m:
        mc = MagicMock()
        m.return_value = mc
        bad = MagicMock()
        bad.choices[0].message.content = "not json"
        good = MagicMock()
        good.choices[0].message.content = json.dumps(SAMPLE_PROBLEMS)
        mc.chat.completions.create.side_effect = [bad, good]
        gen = ProblemGenerator()
        r = gen.generate(T1)
        assert isinstance(r, list)
        assert mc.chat.completions.create.call_count == 2
test("ProblemGenerator.generate: retry khi JSON lỗi", t_gen_retry)

def t_gen_raises_max_retry():
    with patch("agents.problem_generator.Groq") as m:
        mc = MagicMock()
        m.return_value = mc
        bad = MagicMock()
        bad.choices[0].message.content = "luôn sai"
        mc.chat.completions.create.return_value = bad
        gen = ProblemGenerator()
        try:
            gen.generate(T1)
            assert False, "Should have raised"
        except RuntimeError as e:
            assert "Agent 1" in str(e)
test("ProblemGenerator.generate: raise RuntimeError sau max retries", t_gen_raises_max_retry)


# ── test_solution_explainer ────────────────────────────────────────────────────
print("\n[test_solution_explainer]")
from agents.solution_explainer import SolutionExplainer

SAMPLE_SOLUTION = {
    "problem_id": 1,
    "read_problem": "Tóm tắt...",
    "thinking_direction": "Hướng giải...",
    "steps": ["Bước 1", "Bước 2"],
    "answer": "Đáp án...",
    "explanation": "Giải thích...",
    "skill_note": "Kỹ năng...",
}
SAMPLE_PROBLEM = {"id": 1, "level": "biết", "question": "Đề bài", "hint": "Gợi ý"}

def t_exp_returns_dict():
    with patch("agents.solution_explainer.Groq") as m:
        m.return_value = _mock_groq(json.dumps(SAMPLE_SOLUTION))
        exp = SolutionExplainer()
        r = exp.explain(SAMPLE_PROBLEM)
        assert isinstance(r, dict)
test("SolutionExplainer.explain: trả dict", t_exp_returns_dict)

def t_exp_all_fields():
    with patch("agents.solution_explainer.Groq") as m:
        m.return_value = _mock_groq(json.dumps(SAMPLE_SOLUTION))
        exp = SolutionExplainer()
        r = exp.explain(SAMPLE_PROBLEM)
        for f in ["problem_id","read_problem","thinking_direction","steps","answer","explanation","skill_note"]:
            assert f in r, f"Thiếu field: {f}"
test("SolutionExplainer.explain: có đủ 7 required fields", t_exp_all_fields)

def t_exp_steps_list():
    with patch("agents.solution_explainer.Groq") as m:
        m.return_value = _mock_groq(json.dumps(SAMPLE_SOLUTION))
        exp = SolutionExplainer()
        r = exp.explain(SAMPLE_PROBLEM)
        assert isinstance(r["steps"], list) and len(r["steps"]) > 0
test("SolutionExplainer.explain: steps là list không rỗng", t_exp_steps_list)

def t_exp_raises_max_retry():
    with patch("agents.solution_explainer.Groq") as m:
        mc = MagicMock()
        m.return_value = mc
        bad = MagicMock()
        bad.choices[0].message.content = "always bad"
        mc.chat.completions.create.return_value = bad
        exp = SolutionExplainer()
        try:
            exp.explain(SAMPLE_PROBLEM)
            assert False, "Should raise"
        except RuntimeError as e:
            assert "Agent 2" in str(e)
test("SolutionExplainer.explain: raise RuntimeError sau max retries", t_exp_raises_max_retry)


# ── test_orchestrator ──────────────────────────────────────────────────────────
print("\n[test_orchestrator]")
from orchestrator import Orchestrator

PROBS_3 = [
    {"id": 1, "level": "biết",     "question": "Q1", "hint": "H1"},
    {"id": 2, "level": "hiểu",     "question": "Q2", "hint": "H2"},
    {"id": 3, "level": "vận_dụng", "question": "Q3", "hint": "H3"},
]

def t_orch_returns_list():
    with patch("orchestrator.ProblemGenerator") as mg, patch("orchestrator.SolutionExplainer") as me:
        mg.return_value.generate.return_value = PROBS_3
        me.return_value.explain.return_value = SAMPLE_SOLUTION
        orch = Orchestrator()
        r = orch.run(T1)
        assert isinstance(r, list) and len(r) == 3
test("Orchestrator.run: trả list 3 items", t_orch_returns_list)

def t_orch_items_have_keys():
    with patch("orchestrator.ProblemGenerator") as mg, patch("orchestrator.SolutionExplainer") as me:
        mg.return_value.generate.return_value = PROBS_3
        me.return_value.explain.return_value = SAMPLE_SOLUTION
        orch = Orchestrator()
        r = orch.run(T1)
        for item in r:
            assert "problem" in item and "solution" in item
test("Orchestrator.run: mỗi item có problem và solution", t_orch_items_have_keys)

def t_orch_explainer_calls():
    with patch("orchestrator.ProblemGenerator") as mg, patch("orchestrator.SolutionExplainer") as me:
        mg.return_value.generate.return_value = PROBS_3
        me.return_value.explain.return_value = SAMPLE_SOLUTION
        orch = Orchestrator()
        orch.run(T1)
        assert me.return_value.explain.call_count == 3
test("Orchestrator.run: gọi explainer đúng số lần bằng số bài", t_orch_explainer_calls)

def t_orch_graceful_fallback():
    with patch("orchestrator.ProblemGenerator") as mg, patch("orchestrator.SolutionExplainer") as me:
        mg.return_value.generate.return_value = PROBS_3
        me.return_value.explain.side_effect = [RuntimeError("lỗi"), SAMPLE_SOLUTION, SAMPLE_SOLUTION]
        orch = Orchestrator()
        r = orch.run(T1)
        assert len(r) == 3
        assert r[0]["solution"] == {}     # graceful fallback
        assert r[1]["solution"] != {}     # bài sau vẫn có solution
test("Orchestrator.run: graceful fallback khi 1 bài giải thất bại", t_orch_graceful_fallback)


# ── Summary ────────────────────────────────────────────────────────────────────
passed = sum(1 for r in results if r[0] == "PASS")
failed = sum(1 for r in results if r[0] == "FAIL")
total  = len(results)

print(f"\n{'='*60}")
print(f"  Kết quả: {passed}/{total} tests PASS  |  {failed} FAIL")
print(f"{'='*60}")

if failed > 0:
    print("\nCác test FAIL:")
    for r in results:
        if r[0] == "FAIL":
            print(f"  ✗ {r[1]}: {r[2]}")
    sys.exit(1)
else:
    print("\n✅ Tất cả tests PASS!")
    sys.exit(0)
