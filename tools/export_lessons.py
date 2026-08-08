#!/usr/bin/env python3
"""Export a whole course to one editable Markdown document, and merge edits back.

The point is a document you can rewrite prose in directly, then have those rewrites land in
the chapter JSON without anyone re-typing them. Every editable field is preceded by an HTML
comment carrying its exact address, for example

    <!-- @1.1/blocks/3/x -->

so the importer knows precisely which field a paragraph belongs to. Those markers are the
only thing that must survive editing. Everything else in the file is yours to change.

Figures are shown as a one-line placeholder rather than raw SVG, because a lesson's figure is
several kilobytes of path data that would bury the prose. They are left untouched on import.

Usage:
    python3 tools/export_lessons.py prealgebra            -> writes prealgebra-lessons.md
    python3 tools/export_lessons.py prealgebra --import <file.md>   -> merges edits back
"""
import json, os, sys, glob, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Fields worth rewriting by hand. Figure SVG and answer keys are deliberately excluded.
FIELDS = ('x', 'sol', 'cap')
MARK = '<!-- @%s -->'
MARK_RE = re.compile(r'<!--\s*@([^\s>]+)\s*-->')

KIND = {'p': 'Prose', 'imp': 'Key idea', 'fact': 'Fact',
        'prob': 'Problem', 'fig': 'Figure'}


def chapters(course):
    out = []
    for f in sorted(glob.glob(f'{ROOT}/lessons/{course}/chapter-*.json'),
                    key=lambda p: int(re.search(r'chapter-(\d+)', p).group(1))):
        n = int(re.search(r'chapter-(\d+)', f).group(1))
        out.append((n, f, json.load(open(f, encoding='utf-8'))))
    return out


def toc_titles(course):
    try:
        toc = json.load(open(f'{ROOT}/lessons/{course}/toc.json', encoding='utf-8'))
        return {c['n']: c['t'] for c in toc}
    except Exception:
        return {}


def export(course):
    titles = toc_titles(course)
    L = [f'# {course} lessons\n',
         'Rewrite any prose, hint or solution below. Keep every `<!-- @... -->` marker exactly\n'
         'as it is; they are how edits find their way back to the right field. Everything else,\n'
         'including headings and blank lines, is free to change.\n',
         'Re-import with:  `python3 tools/export_lessons.py %s --import <this-file>`\n' % course]

    nlesson = nfield = 0
    for chnum, _, data in chapters(course):
        L.append(f'\n---\n\n## Chapter {chnum}. {titles.get(chnum, "")}\n')
        for key in sorted(data, key=lambda s: [int(p) for p in s.split('.')]):
            lesson = data[key]
            nlesson += 1
            L.append(f'\n### {key}  {lesson.get("title","")}\n')
            for bi, b in enumerate(lesson.get('blocks', [])):
                t = b.get('t', 'p')
                head = f'**{KIND.get(t, t)}**'
                if t == 'prob':
                    head += f'  · answer `{b.get("ans","")}`  · {b.get("xp","")} xp'
                L.append(f'\n{head}\n')
                if t == 'fig':
                    L.append(f'*(figure, {len(b.get("x",""))} bytes of SVG, not shown)*\n')
                    if b.get('cap'):
                        L.append(MARK % f'{key}/blocks/{bi}/cap'); L.append(b['cap'] + '\n'); nfield += 1
                    continue
                for f in FIELDS:
                    if f == 'cap' or not b.get(f):
                        continue
                    if f == 'sol':
                        L.append('\n*Solution.*\n')
                    # a goals block holds a LIST of items; address each one separately so
                    # every line stays individually editable
                    if isinstance(b[f], list):
                        for gi, g in enumerate(b[f]):
                            L.append(MARK % f'{key}/blocks/{bi}/{f}/{gi}')
                            L.append(str(g) + '\n'); nfield += 1
                        continue
                    L.append(MARK % f'{key}/blocks/{bi}/{f}')
                    L.append(b[f] + '\n'); nfield += 1
                for hi, h in enumerate(b.get('hints') or []):
                    L.append(f'\n*Hint {hi+1}.*\n')
                    L.append(MARK % f'{key}/blocks/{bi}/hints/{hi}')
                    L.append(h + '\n'); nfield += 1
            for ri, r in enumerate(lesson.get('review', [])):
                L.append(f'\n**Review {ri+1}**  · answer `{r.get("ans","")}`\n')
                for f in ('x', 'sol'):
                    if not r.get(f):
                        continue
                    if f == 'sol':
                        L.append('\n*Solution.*\n')
                    L.append(MARK % f'{key}/review/{ri}/{f}')
                    L.append(r[f] + '\n'); nfield += 1
                for hi, h in enumerate(r.get('hints') or []):
                    L.append(f'\n*Hint {hi+1}.*\n')
                    L.append(MARK % f'{key}/review/{ri}/hints/{hi}')
                    L.append(h + '\n'); nfield += 1

    out = f'{ROOT}/{course}-lessons.md'
    open(out, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print(f'wrote {out}')
    print(f'  {nlesson} lessons, {nfield} editable fields, {os.path.getsize(out)//1024}KB')
    return out


def parse(path):
    """Marker -> the text that follows it, up to the next marker or heading."""
    txt = open(path, encoding='utf-8').read().split('\n')
    edits, cur, buf = {}, None, []

    def flush():
        if cur is not None:
            edits[cur] = '\n'.join(buf).strip()
    for line in txt:
        m = MARK_RE.match(line.strip())
        if m:
            flush(); cur, buf = m.group(1), []
        elif cur is not None:
            # a heading or bold label ends the field; blank lines inside it are kept
            if line.startswith(('#', '**', '*Hint', '*Solution', '---')):
                flush(); cur, buf = None, []
            else:
                buf.append(line)
    flush()
    return edits


def do_import(course, path):
    edits = parse(path)
    print(f'{len(edits)} fields found in {os.path.basename(path)}')
    changed = files = 0
    for chnum, fpath, data in chapters(course):
        dirty = False
        for addr, val in edits.items():
            key, sect, idx, *rest = addr.split('/')
            if key not in data or not val:
                continue
            item = data[key][sect][int(idx)] if sect == 'review' else data[key]['blocks'][int(idx)]
            if rest[0] == 'hints':
                old = (item.get('hints') or [])[int(rest[1])]
                if old != val:
                    item['hints'][int(rest[1])] = val; changed += 1; dirty = True
            elif len(rest) == 2:                       # a list field such as goals/x/2
                lst = item.get(rest[0])
                if isinstance(lst, list) and lst[int(rest[1])] != val:
                    lst[int(rest[1])] = val; changed += 1; dirty = True
            else:
                if item.get(rest[0]) != val:
                    item[rest[0]] = val; changed += 1; dirty = True
        if dirty:
            json.dump(data, open(fpath, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
            open(fpath, 'a', encoding='utf-8').write('\n')
            files += 1
    print(f'  {changed} fields updated across {files} chapter files')
    if changed:
        print('  NEXT: python3 tools/check_lesson.py on anything you touched, then build_lessons.py')


if __name__ == '__main__':
    course = sys.argv[1] if len(sys.argv) > 1 else 'prealgebra'
    if '--import' in sys.argv:
        do_import(course, sys.argv[sys.argv.index('--import') + 1])
    else:
        export(course)
