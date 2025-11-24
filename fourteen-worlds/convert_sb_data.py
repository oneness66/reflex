import json

# Load the JSON data
with open('sb_full_content.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

sb_chapters = data['sb_chapters']
sb_verses = data['sb_verses']

# Generate Python file
with open('fourteen_worlds/data/sb_content.py', 'w', encoding='utf-8') as f:
    f.write('sb_chapters = {\n')
    
    for canto_num in sorted(sb_chapters.keys(), key=int):
        chapters = sb_chapters[canto_num]
        f.write(f'    {canto_num}: [\n')
        for ch in chapters:
            # Update URL to internal route
            ch['url'] = f"/library/sb/{canto_num}/{ch['number']}"
            f.write(f'        {json.dumps(ch)},\n')
        f.write('    ],\n')
    
    f.write('}\n\n')
    
    f.write('sb_verses = {\n')
    
    for key in sorted(sb_verses.keys()):
        verses = sb_verses[key]
        canto, chapter = key.split('-')
        f.write(f'    "{key}": [\n')
        for v in verses:
            # Update URL to internal route
            v['url'] = f"/library/sb/{canto}/{chapter}/{v['number']}"
            f.write(f'        {json.dumps(v)},\n')
        f.write('    ],\n')
    
    f.write('}\n')

print("Python data file created successfully!")
