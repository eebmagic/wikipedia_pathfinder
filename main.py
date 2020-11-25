import requests
from myqueue import queue
from tree import tree, node
import time
import numpy as np
import spacy

model = spacy.load('en_core_web_sm')

def get_contained_links(fulltext):
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


def valid_url(url):
    goodStart = url.startswith("https://en.wikipedia.org/wiki/")
    notWikiHelp = "/wikipedia:" not in url.lower()
    notPhp = "index.php" not in url.lower()
    notTemplate = "template:" not in url.lower()
    notFile = "file:" not in url.lower()
    notCategory = "category:" not in url.lower()

    if goodStart and wikiHelp and notPhp and notTemplate and notFile and notCategory:
        return True
    else:
        print(f"INVALID URL: {url}")
        return False


def get_child_urls(url):
    if valid_url(url):
        try:
            fullResponse = requests.get(url).text
            return get_contained_links(fullResponse)
        except requests.exceptions.ConnectionError as ce:
            print(f"ERROR: Given the {url = } there was a connection error")
            print(ce)
    else:
        print(f"INVALID URL: {url}")


def subject_distance(a, b):
    aToken = model(a)
    bToken = model(b)

    # print(aToken.similarity(bToken))
    return aToken.similarity(bToken)
    # input()


def get_url_path(starturl, target, limit=1):
    targetSubject = get_subjects([target])[0]
    startSubject = get_subjects([start])[0]

    # make a tree with start url as head
    head = node(starturl)
    t = tree(head)

    # queue of new nodes to try searching from
    searchOrder = queue()
    searchOrder.add(t.getHead(), subject_distance(startSubject, targetSubject))

    # set of all urls that have already been searched from
    allAdded = set()
    allAdded.add(t.getHead().getData())

    # LOOP:
    # set head to current node
    curr = searchOrder.pop()
    targetFound = False
    while not targetFound:
        # get child nodes/urls of current node
        currUrl = curr.getData()
        # print(f"getting article: {get_subjects([currUrl])[0]}")
        
        # if url is a valid article
        if valid_url(currUrl):
            childUrls = get_child_urls(currUrl)

            # check if target destination in children
            for url in childUrls:
                # add child urls to tree as child nodes of curr
                newNode = node(url)
                t.add(newNode, curr)

                currSubject = get_subjects([url])[0]
                currDist = subject_distance(currSubject, targetSubject)
                print(f"{currDist:.5f} - {currSubject}")

                # if target, then return path to this node
                if target.lower() == url.lower():
                    targetFound = True
                    fullPath = t.getPath(newNode)
                    return fullPath, len(allAdded)
                else:
                    # if not, then add children to tree and queue for bfs
                    if newNode.getData() not in allAdded:
                        searchOrder.add(newNode, currDist)
                        allAdded.add(newNode.getData())
        else:
            print("breaking because of invalid url ^")

        # change curr to next node in queue
        curr = searchOrder.pop()


if __name__ == '__main__':
    # start = input("Give a start url: ").strip()
    # target = input("Give a target url: ").strip()
    start = "https://en.wikipedia.org/wiki/Submarine_earthquake"
    target = "https://en.wikipedia.org/wiki/Non-monogamy"
    # start = "https://en.wikipedia.org/wiki/Turtle"
    # target = "https://en.wikipedia.org/wiki/China"

    startTime = time.time()
    path, considerSize = get_url_path(start, target)
    duration = time.time() - startTime

    print(f"\nThe shortest possible path is in {len(path)} steps")
    print(f"\t(took {duration:.2f} secs; considered {considerSize} articles):")
    for url in path:
        print(url)
