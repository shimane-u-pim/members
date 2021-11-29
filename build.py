import markdown
import glob


def get_metadata(file):
    content = ''
    with open(file, encoding='utf-8') as f:
        content = f.read()
    md = markdown.Markdown(extensions=['full_yaml_metadata'])
    md.convert(content)
    return md.Meta


def retrive_from_site():
    for file in glob.glob('./article_sites/site/content/japanese/blog/*.md'):
        if (file.endswith('_index.md')):
            continue
        print(file)
        print(get_metadata(file))


def retrive_from_connect():
    for file in glob.glob('./article_sites/connect/content/posts/*.md'):
        print(file)
        print(get_metadata(file))


retrive_from_connect()
retrive_from_site()
