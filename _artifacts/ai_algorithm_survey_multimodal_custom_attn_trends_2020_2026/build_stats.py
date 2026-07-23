import json
from collections import Counter
from pathlib import Path
import matplotlib.pyplot as plt

ROOT = Path(__file__).parent
rows = [json.loads(x) for x in (ROOT/'paper_db.jsonl').read_text().splitlines() if x.strip()]
formal = [r for r in rows if r['status'] == 'formal']
venues = ['CVPR','CVPR Findings','ICCV','ECCV','NeurIPS','ICML','ICLR','AAAI','ACM MM']
years = list(range(2020, 2027))
with (ROOT/'venue_counts.csv').open('w') as f:
    f.write('year,venue,count\n')
    for y in years:
        for v in venues:
            f.write(f"{y},{v},{sum(r['year']==y and r['venue']==v for r in formal)}\n")
org = Counter()
for r in formal:
    for o in set(r.get('orgs', [])):
        org[o] += 1
with (ROOT/'organization_counts.csv').open('w') as f:
    f.write('organization,papers\n')
    for o,n in org.most_common(): f.write(f'"{o}",{n}\n')

plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(11,5.5))
bottom = [0]*len(years)
colors = {'CVPR':'#3366cc','CVPR Findings':'#7799dd','ICCV':'#dc3912','ECCV':'#ff9900','NeurIPS':'#109618','ICML':'#990099','ICLR':'#0099c6','AAAI':'#dd4477','ACM MM':'#66aa00'}
for v in venues:
    vals = [sum(r['year']==y and r['venue']==v for r in formal) for y in years]
    ax.bar(years, vals, bottom=bottom, label=v, color=colors[v])
    bottom = [a+b for a,b in zip(bottom, vals)]
ax.set_title('Audited multimodal sparse-attention papers by year and venue')
ax.set_xlabel('Publication year'); ax.set_ylabel('Formal papers (audited corpus)')
ax.set_xticks(years); ax.legend(ncol=3, fontsize=8, frameon=True)
fig.tight_layout(); fig.savefig(ROOT/'venue-year-counts.png', dpi=220); plt.close(fig)

if org:
    top = org.most_common(10)[::-1]
    fig, ax = plt.subplots(figsize=(8,4.8))
    ax.barh([x[0] for x in top], [x[1] for x in top], color='#3c8dbc')
    ax.set_title('Affiliation organizations in papers with verified first-page metadata')
    ax.set_xlabel('Papers (full counting)'); fig.tight_layout()
    fig.savefig(ROOT/'organization-method-distribution.png', dpi=220); plt.close(fig)

summary = {'formal_papers':len(formal),'all_records':len(rows),'by_year':{str(y):sum(r['year']==y for r in formal) for y in years},'by_venue':dict(Counter(r['venue'] for r in formal)),'verified_org_papers':sum(bool(r.get('orgs')) for r in formal),'organization_counts':dict(org)}
(ROOT/'stats_summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2)+'\n')
