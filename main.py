import requests
from myqueue import queue
from tree import tree, node

def get_contained_links(fulltext):
    # response = requests.get(start)
    # splits = response.text.split('<p>')
    splits = fulltext.split('<p>')
    found = set()
    for x in splits:
        selection = x.split('</p>')[0]
        if 'title' in selection and 'href="/wiki/' in selection:
            subs = selection.split(' ')
            for ind, value in enumerate(subs):
                try:
                    if value.startswith('href="') and subs[ind + 1].startswith('title="'):
                        suffix = value.split('"')[1].strip()
                        full_url = "https://en.wikipedia.org" + suffix
                        found.add(full_url)
                except IndexError:
                    pass

    return found


def get_subjects(urllist):
    out = []
    for url in urllist:
        out.append(url.split('/')[-1])
    return out


def get_child_urls(url):
    fullResponse = requests.get(url).text
    return get_contained_links(fullResponse)


def full_search(starturl, target, limit=1):
    # make a tree with start url as head
    head = node(starturl)
    t = tree(head)

    # set head to current node
    curr = t.getHead()
    searchOrder = queue()

    # LOOP:
    targetFound = False
    while not targetFound:
        # get child nodes/urls of current node
        currUrl = curr.getData()
        childUrls = get_child_urls(currUrl)

        # check if target destination in children
        for url in childUrls:
            # add child urls to tree as child nodes of curr
            newNode = node(url)
            t.add(newNode, curr)

            # if target, then add to tree, work back up to head, and return
            if target.lower() == url.lower():
                targetFound = True
                fullPath = t.getPath(newNode)
                # print(f"FOUND PATH: {fullPath}")
                return fullPath
            else:
                # if not, then add children to tree and queue for bfs
                searchOrder.add(newNode)

        # change curr to next node in queue
        curr = searchOrder.pop()


if __name__ == '__main__':
    start = "https://en.wikipedia.org/wiki/Turtle"
    target = "https://en.wikipedia.org/wiki/China"

    full = full_search(start, target)
    subjects = get_subjects(full)
    print(f"{full = }")
