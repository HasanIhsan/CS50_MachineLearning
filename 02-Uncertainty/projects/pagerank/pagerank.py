import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


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
    """

    distribution = {}
    pages = list(corpus.keys())
    n = len(pages)
    links = corpus.get(page)

    #if no outgoing links, treat as linking to all pages
    if not links:
        links = set(pages)

    num_links = len(links)
    base_prob = (1 - damping_factor) / n

    # initialize all to base prob
    for p in pages:
        distribution[p] = base_prob

    # distribute damping among linked pages
    for linked in links:
        distribution[linked] += damping_factor / num_links

    return distribution



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages = list(corpus.keys())
    counts = {p: 0 for p in pages}

    # first sammple: random page
    current = random.choice(pages)
    counts[current] += 1

    # generate remaning samples
    for _ in range(1, n):
        model = transition_model(corpus, current, damping_factor)

        # choose next page based on distr
        next_page = random.choices(
            population = list(model.keys()),
            weights = list(model.values()),
            k = 1
        )[0]

        counts[next_page] +=1
        current = next_page

    # convert counts to prob
    ranks = {p: counts[p] / n for p in pages}
    return ranks



def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages = list(corpus.keys())
    n = len(pages)
    # Initialize ranks to 1/N
    ranks = {p: 1 / n for p in pages}
    threshold = 0.001
    converged = False

    while not converged:
        new_ranks = {}
        for p in pages:
            # Random jump component
            rank_sum = (1 - damping_factor) / n
            # Sum over all pages that link to p
            total = 0
            for i in pages:
                links = corpus.get(i)
                # Treat pages with no links as linking to all pages
                if not links:
                    link_set = set(pages)
                else:
                    link_set = links
                if p in link_set:
                    total += ranks[i] / len(link_set)
            rank_sum += damping_factor * total
            new_ranks[p] = rank_sum

        # Check convergence
        converged = True
        for p in pages:
            if abs(new_ranks[p] - ranks[p]) > threshold:
                converged = False
        ranks = new_ranks

    return ranks


if __name__ == "__main__":
    main()
