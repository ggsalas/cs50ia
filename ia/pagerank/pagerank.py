import os
import random
import re
import sys

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
    print(transition_model(example_corpus, '1.html', DAMPING))
    print(transition_model(example_corpus, '2.html', DAMPING))
    print(transition_model(example_corpus, '3.html', DAMPING))

    # ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    # print(f"PageRank Results from Sampling (n = {SAMPLES})")
    # for page in sorted(ranks):
    #     print(f"  {page}: {ranks[page]:.4f}")
    # ranks = iterate_pagerank(corpus, DAMPING)
    # print(f"PageRank Results from Iteration")
    # for page in sorted(ranks):
    #     print(f"  {page}: {ranks[page]:.4f}")


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
    """
    t_model = {}
    visit_count = {}
    
    # add all pages in the corpus with 0 count
    for pag in corpus:
        visit_count[pag] = 0

    # addition +1 for each link
    for _, links in corpus.items():
        for link in links:
            visit_count[link] += 1

    def calculate_probability_distribution(visits):
        no_visited_value = (1 - damping_factor) / len(corpus)
        visited_value = damping_factor / visits if visits > 0 else 0

        return visited_value + no_visited_value

    for pag, visits in visit_count.items():
        t_model[pag] = calculate_probability_distribution(visits)

    return t_model[page]


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
