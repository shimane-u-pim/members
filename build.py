import markdown
import glob
import os
import json
import yaml
import shutil


def get_html(file):
    content = ''
    with open(file, encoding='utf-8') as f:
        content = f.read()
    md = markdown.Markdown()
    return md.convert(content)


def get_markdown(file):
    content = ''
    with open(file, encoding='utf-8') as f:
        content = f.read()
    md = markdown.Markdown(extensions=['full_yaml_metadata'])
    md.convert(content)
    return md


def get_metadata(file):
    md = get_markdown(file)
    return md.Meta


def retrive_from_site():
    data = []
    for file in glob.glob('./article_sites/site/content/japanese/blog/*.md'):
        if (file.endswith('_index.md')):
            continue
        data.append({'meta': get_metadata(file),
                    'file': os.path.basename(file)})
    return data


def retrive_from_connect():
    data = []
    for file in glob.glob('./article_sites/connect/content/posts/*.md'):
        data.append({'meta': get_metadata(file),
                    'file': os.path.basename(file)})
    return data


p_connect = retrive_from_connect()
p_site = retrive_from_site()


def retrive_posts_by_author_id(uid, post_data, source):
    page = []
    for p in post_data:
        for a in p['meta']['authors']:
            if (a['code'] == uid):
                page.append(
                    {'source': source, 'page': os.path.splitext(p['file'])[0], 'tags': p['meta']['tags'], 'title': p['meta']['title']})
    return page


def get_articles_by_uid(uid):
    page = []
    page.extend(retrive_posts_by_author_id(uid, p_connect, 'connect'))
    page.extend(retrive_posts_by_author_id(uid, p_site, 'site'))
    return page


template = ''
with open('_template.html', 'r', encoding='utf-8') as f:
    template = f.read()


os.makedirs('./output', exist_ok=True)

for mdf in glob.glob('./content/*.yaml'):
    user = {}
    with open(mdf, encoding='utf-8') as f:
        user = yaml.safe_load(f)
    uid = user['id']
    user['articles'] = get_articles_by_uid(uid)

    html = template \
        .replace('/*name*/', user['name']) \
        .replace('/*image*/', user.get('image', 'https://avatar.tobi.sh/' + uid)) \
        .replace('/*articles*/', json.dumps(user['articles'])) \

    with open('./output/' + uid + '.html', 'w', encoding='utf-8') as f:
        f.write(html)
