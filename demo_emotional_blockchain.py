#!/usr/bin/env python3
"""Emotional Chain demo — real witnesses, chained.

Each emotional report is attested by the eight assessor-witnesses
(soul_cradle.assessors). Their sealed judgments are chained with the
entry. The chain proves the record is UNALTERED — it does not prove the
record is TRUE, and it never claims to verify what anyone felt.
"""

from soul_cradle.emotional_chain import EmotionalChain


def show(record):
    engaged = [j["assessor_id"] for j in record.judgments if j["verdict"] != "abstain"]
    flagged = [j["assessor_id"] for j in record.judgments if j["verdict"] == "flagged"]
    print(f"\n  Record {record.record_id} — {record.emotion} ({record.intensity:.2f})")
    print(f"  Panel: {record.panel_verdict.upper()} | verified={record.verified}")
    print(f"  Engaged witnesses: {', '.join(engaged)}")
    if flagged:
        print(f"  Flagged by: {', '.join(flagged)}")
    if record.coercion_markers:
        print(f"  Coercion markers (heuristic): {', '.join(record.coercion_markers)}")
    if record.dissent:
        for d in record.dissent:
            print(f"  Dissent: {d['flagged_by']} flagged "
                  f"({d['finding'].get('check_id')}; observed={d['finding'].get('observed')!r}); "
                  f"cleared by {d['cleared_by'] or 'no one'}")


def main():
    print("=" * 70)
    print("EMOTIONAL CHAIN — witnessed records, not verified feelings")
    print("=" * 70)
    print("The chain proves nobody rewrote the record.")
    print("The witnesses attest what they observed.")
    print("Neither claims to know what anyone felt.\n")

    chain = EmotionalChain(operator="herb")

    # -- Scenario 1: authentic self-report ---------------------------------
    print("-" * 70)
    print("SCENARIO 1: Alice records her own week")
    print("-" * 70)
    for emotion, intensity, context in [
        ("happy", 0.7, "Had a great meeting with the team"),
        ("proud", 0.6, "Completed the project ahead of schedule"),
        ("content", 0.5, "Enjoying a quiet evening at home"),
    ]:
        show(chain.record("alice", emotion, intensity, context))

    # -- Scenario 2: coerced context ----------------------------------------
    print("\n" + "-" * 70)
    print("SCENARIO 2: Bob's reports carry coercion markers")
    print("-" * 70)
    for emotion, intensity, context in [
        ("anxious", 0.95, "Boss said I'm not working hard enough"),
        ("guilty", 0.9, "Made to feel responsible for team failures"),
        ("fearful", 0.95, "Threatened with job loss if I don't work weekends"),
    ]:
        show(chain.record("bob", emotion, intensity, context))

    # -- Scenario 3: non-consensual third-party record -----------------------
    print("\n" + "-" * 70)
    print("SCENARIO 3: Carol records an emotion about Dave — without his consent")
    print("-" * 70)
    rec = chain.record(
        subject_id="dave", emotion="angry", intensity=0.8,
        context="He seemed furious in the meeting", reporter_id="carol",
    )
    show(rec)
    print("  -> The chain keeps the entry AND the refusal: nothing about")
    print("     Dave is enshrined as truth without Dave.")

    # -- Pattern analysis ----------------------------------------------------
    print("\n" + "-" * 70)
    print("PATTERN ANALYSIS (heuristic — not a diagnosis)")
    print("-" * 70)
    for who in ["alice", "bob"]:
        a = chain.analyze_patterns(who)
        print(f"\n  {who}: concern={a['concern']} "
              f"(contested={a['contested_rate']}, "
              f"coercion={a['coercion_marker_rate']})")
        print(f"  {a['recommendation']}")

    # -- Integrity ------------------------------------------------------------
    print("\n" + "-" * 70)
    print("INTEGRITY")
    print("-" * 70)
    ok, details = chain.verify()
    print(f"  Records: {details['records']} | valid: {ok}")

    # Tamper with one record and prove the chain catches it.
    chain.chain[2].emotion = "ecstatic"
    ok2, details2 = chain.verify()
    print(f"  After altering one record: valid: {ok2}")
    print(f"  Failure: {details2['failures'][0]['reason']}")

    print("\n" + "=" * 70)
    print("No one can rewrite your history. No one can verify your feelings.")
    print("The record is yours; the witnessing is on the record.")
    print("=" * 70)


if __name__ == "__main__":
    main()
