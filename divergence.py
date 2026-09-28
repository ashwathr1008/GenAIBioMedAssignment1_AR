import csv
import os
import sys
from collections import Counter

DATA_PATH = "data"
DESIGN_FILE = os.path.join("design", "design_greedy.txt")
OUTPUT_CSV = os.path.join("design", "divergence.csv")
PROMPT_LEN = 64  # inference.py gives the model the first 64 residues


def consensus(seqs):
    # most common residue at each position across the training set
    return ''.join(Counter(col).most_common(1)[0][0] for col in zip(*seqs))


def substitutions(design, cons):
    # 1-indexed, consensus residue -> design residue, e.g. A36V
    return [f'{c}{i + 1}{d}' for i, (c, d) in enumerate(zip(cons, design)) if c != d]


def main():
    train = [line.strip() for line in open(os.path.join(DATA_PATH, 'train.txt')) if line.strip()]
    designs = [line.strip() for line in open(DESIGN_FILE) if line.strip()]
    cons = consensus(train)
    print(f'consensus ({len(cons)} aa):\n{cons}\n')

    # optionally pass design numbers (e.g. 7 12 31) to only report those, like the top 5
    picks = [int(n) for n in sys.argv[1:]] or range(1, len(designs) + 1)

    position_counts = Counter()
    with open(OUTPUT_CSV, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['design', 'num_substitutions', 'in_prompt', 'in_generated', 'substitutions'])
        for n in picks:
            subs = substitutions(designs[n - 1], cons)
            positions = [int(s[1:-1]) for s in subs]
            position_counts.update(positions)
            in_prompt = sum(p <= PROMPT_LEN for p in positions)
            writer.writerow([f'design_{n:02d}', len(subs), in_prompt, len(subs) - in_prompt, ' '.join(subs)])
            print(f'design_{n:02d}: {" ".join(subs) or "(matches consensus)"}')

    # where along the sequence the substitutions land, for the positional distribution part
    print('\nsubstitutions per position:')
    for pos, count in sorted(position_counts.items()):
        region = 'prompt' if pos <= PROMPT_LEN else 'generated'
        print(f'  {pos:>3} ({region}): {count}')
    print(f'\nwrote {OUTPUT_CSV}')


if __name__ == '__main__':
    main()
