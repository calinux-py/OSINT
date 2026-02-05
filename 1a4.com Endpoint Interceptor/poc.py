import requests, json, base64, yaml

def fetch(s, bl):
    r = s.post('https://app.1a4.com/graphql', json={"variables": {}, "query": f'{{fromBl(bl: "{bl.lower()}") {{text}}}}'})
    return r.json().get('data', {}).get('fromBl', {}).get('text') if r.status_code == 200 else None

def scrape(url):
    s = requests.Session()
    s.headers.update({'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json', 'apollo-require-preflight': 'true'})
    
    enc = s.get(url).url.split('/g/s/')[1].split('?')[0]
    bl = base64.urlsafe_b64decode(enc + '=' * (4 - len(enc) % 4)).decode('utf-8', errors='ignore')
    bl = bl.split(']', 1)[1] if ']' in bl else bl
    
    parts = bl.split('@')
    name, fac = parts[0], parts[1].split('~')[0]
    pid = parts[1].split('~')[1] if '~' in parts[1] else ''
    
    data = {'product_name': name, 'facility': fac, 'product_id': pid}
    
    main = fetch(s, bl)
    if main:
        try:
            for card in yaml.safe_load(main)['data']['cards']:
                card_bl = card.strip().lstrip('^')
                cd = fetch(s, card_bl)
                if cd:
                    try:
                        p = yaml.safe_load(cd)
                        if '~products' in card_bl: data['product_details'] = p
                        elif '~coa' in card_bl: data['lab_results'] = p
                        elif '~organizations' in card_bl: data['organization'] = p
                    except: data[card_bl.split('~')[-1]] = cd
        except: data['raw'] = main
    
    for bl_str, key in [(f"{pid}@{fac}~coa", 'lab_results'), (f"{name}@{fac}~products", 'product_details')]:
        if key not in data:
            d = fetch(s, bl_str)
            if d:
                try: data[key] = yaml.safe_load(d)
                except: data[key + '_raw'] = d
    
    return data

if __name__ == "__main__":
    data = scrape("HTTPS://1A4.COM/13TX7BMRTPRSUWN88TMRRO")
    print(json.dumps(data, indent=2))
    open('product_content.json', 'w').write(json.dumps(data, indent=2))