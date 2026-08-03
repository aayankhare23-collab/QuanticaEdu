#!/usr/bin/env python3
"""Take a workflow's returned result and run every deterministic gate on it at once.

    python3 tools/land_lesson.py result.json --key 7.3 [--outdir /tmp]

`result.json` is the object the authoring Workflow returns, `{lesson, audit,
fixedCount, pyChecks, missing}`. This splits it into lesson / audit / pychecks
files, runs `check_lesson.py` and `verify_answers.py`, and prints the audit
findings grouped by severity so they can be triaged.

It does NOT decide anything. Two gates in the ship sequence stay manual on
purpose: re-solving every answer from the FINAL text, and verifying each
audit-proposed replacement before applying it.
"""
import argparse, json, pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('result')
    ap.add_argument('--key', required=True)
    ap.add_argument('--outdir', default='/tmp')
    a = ap.parse_args()

    R = json.load(open(a.result, encoding='utf-8'))
    if 'lesson' not in R:
        sys.exit(f'no "lesson" in {a.result}; keys are {list(R)}')
    out = pathlib.Path(a.outdir)
    stem = a.key.replace('.', '_')
    lp = out / f'lesson_{stem}.json'
    pp = out / f'pychecks_{stem}.json'
    ap_ = out / f'audit_{stem}.json'
    lp.write_text(json.dumps(R['lesson'], indent=1, ensure_ascii=False), encoding='utf-8')
    pp.write_text(json.dumps(R.get('pyChecks', []), indent=1), encoding='utf-8')
    ap_.write_text(json.dumps(R.get('audit', {}), indent=1), encoding='utf-8')

    L = R['lesson']
    nprob = sum(1 for b in L['blocks'] if b.get('t') == 'prob')
    print(f'== {a.key} "{L.get("title")}" -> next {L.get("next")}')
    print(f'   {len(L["blocks"])} blocks ({nprob} prob), {len(L.get("review", []))} review, '
          f'{R.get("fixedCount", "?")} corrected by verify')
    if R.get('missing'):
        print(f'   !! MISSING SLOTS: {R["missing"]}')

    # flush, or the subprocesses' output lands above these headers
    print('\n-- check_lesson.py --', flush=True)
    subprocess.run(['python3', str(ROOT / 'tools/check_lesson.py'), str(lp)])
    print('\n-- verify_answers.py --', flush=True)
    subprocess.run(['python3', str(ROOT / 'tools/verify_answers.py'), str(lp), str(pp)])

    findings = (R.get('audit') or {}).get('findings') or []
    print(f'\n-- audit: {R.get("audit", {}).get("verdict", "?")} --')
    for sev in ('major', 'minor'):
        hits = [f for f in findings if f.get('severity') == sev]
        print(f'   {len(hits)} {sev}')
        for f in hits:
            print(f'   [{sev}] {f.get("where")}: {f.get("issue")}')
            print(f'          fix: {f.get("fix")}')
    print(f'\nfiles: {lp}  {pp}  {ap_}')
    print('STILL MANUAL: re-solve every answer from the FINAL text, and verify each '
          'audit-proposed replacement before applying it.')


if __name__ == '__main__':
    main()
