import os
import random
import re
import sys
from typing import Dict

DAMPING = 0.85
SAMPLES = 10000

example_corpus = {
    "1.html": {"2.html", "3.html"}, 
    "2.html": {"3.html"}, 
    "3.html": {"2.html"}
}

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])

    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")

    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.

    the response should be { '<page_1>': value, ..., '<page_n>': value }
    """
    number_pages = len(corpus)
    t_model = dict()
    links = corpus[page]

    if not links:
        links = corpus.keys()

    for page in corpus:
        prob_all_pages = (1 - damping_factor ) / number_pages
        if page in links: 
            t_model[page] = damping_factor / len(links) + prob_all_pages
        else:
            t_model[page] = prob_all_pages

    return t_model


def validate_items_sum(items):
    validate_sum = 0
    for _, val in items.items():
        validate_sum += val
    print(f"sum of all PR pages: {validate_sum}")


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    visit_count = {}
    pages_tmodel = {}
    pr = {}

    # set transition_model for each page
    for pag in corpus:
        visit_count[pag] = 0
        pages_tmodel[pag] = transition_model(corpus, pag, damping_factor)

    # pick pages at random based on transition model 
    # starting with a generic random page
    current_page = random.choice(list(corpus.keys()))
    for _ in range(n):
        selected_page = random.choices(list(pages_tmodel[current_page].keys()), list(pages_tmodel[current_page].values()))[0]
        visit_count[selected_page] += 1
        current_page = selected_page

    # calculate PR = visits / total_visits
    for pag, visits in visit_count.items():
        pr[pag] = visits / n

    # validate_items_sum(pr)
    return pr


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    """
    PR(p) = 1-d/N + d SUM(i) { PR(i) / numLinks(i) }
    """
    # To handle pages without links as if they have links to all pages
    all_pages = set()
    for page in corpus:
        all_pages.add(page)

    new_corpus = {}
    for page, links in corpus.items():
        if len(links) == 0:
            new_corpus[page] = all_pages
        else:
            new_corpus[page] = links

    def get_page_pr (page):
        random_probability = (1 - damping_factor) / len(corpus)

        # get "i" pages that links to "p" pages
        # to allow calculate the second term in the equation
        i_pages = set();
        for pag, links in new_corpus.items():
            for link in links:
                if (link == page):
                    i_pages.add(pag)

        # sum
        sum = 0
        for i in i_pages:
            sum += pr[i] / len(new_corpus[i])

        link_probability = damping_factor * sum
        return random_probability + link_probability


    # Calculate iterative PR
    pr: Dict[str, float] = {}

    # calculate initial pr values
    for page in corpus:
        pr[page] = 1 / len(corpus)

    repeat = True
    while repeat:
        new_corpus_prs = {} 
        for page, page_pr in pr.items():
            new_page_pr = get_page_pr(page)
            new_corpus_prs[page] = new_page_pr

            if abs(new_page_pr - page_pr) >= 0.001:
                repeat = True
            else: 
                repeat = False
        pr = new_corpus_prs

    # validate_items_sum(pr)
    return pr


if __name__ == "__main__":
    main()
