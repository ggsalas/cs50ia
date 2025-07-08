import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    joint = []
    names = set(people)
    zero_genes = names - one_gene - two_genes
    not_have_trait = names - have_trait

    def getParents(childName):
        child = people[childName]
        mother = child['mother']
        father = child['father']
        if mother and father:
            return {'mother': mother, 'father': father}
        else:
            return None

    def calc_gens(person, person_genes): 
        parents = getParents(person)

        # Get probability for one parent
        def get_parent_prob(name):
            m = PROBS['mutation']

            if name in zero_genes:
                return m
            elif name in one_gene:
                return 0.5
            elif name in two_genes:
                return 1 - m
            else:
                raise ValueError(f"Invalid value of gens for parent")

        # Calculate probability if has parents
        if parents:
            p_m = get_parent_prob(parents["mother"])
            p_f = get_parent_prob(parents["father"])

            # Prob in which no parent has sent a gene
            if person_genes == 0:
                return (1 - p_m) * (1 - p_f)
            # Prob in which only one parent has sent a gene
            elif person_genes == 1:
                return p_m * (1 - p_f) + p_f * (1 - p_m)
            # Prob in which both parents has sent a gene
            elif person_genes == 2:
                return p_m * p_f
            else:
                raise ValueError(f"Invalid value of gens for person: {person_genes}")

        # Return probability if has no parents
        else:
            return PROBS['gene'][person_genes]

    for p in zero_genes:
        joint.append(calc_gens(p, 0))
    for p in one_gene:
        joint.append(calc_gens(p, 1))
    for p in two_genes:
        joint.append(calc_gens(p, 2))

    for name in have_trait:
        if name in zero_genes:
            joint.append(PROBS['trait'][0][True])
        elif name in one_gene:
            joint.append(PROBS['trait'][1][True])
        elif name in two_genes:
            joint.append(PROBS['trait'][2][True])

    # calcular prob de que no tengan trait
    for name in not_have_trait:
        if name in zero_genes:
            joint.append(PROBS['trait'][0][False])
        elif name in one_gene:
            joint.append(PROBS['trait'][1][False])
        elif name in two_genes:
            joint.append(PROBS['trait'][2][False])

    joint_prob = 1
    for prob in joint:
        joint_prob *= prob

    return joint_prob


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.


    Como esto itera por cada persona y en cada variable, yo deberia recibir una funcion para cada familiar
    For example, if "Harry" were in both two_genes and in have_trait, then p would be added to probabilities["Harry"]["gene"][2] and to probabilities["Harry"]["trait"][True].


    in the example I mentioned I'm receiving 3 names in two_genes variable, this means I should do:
    for name in two_genes:
        probabilities[name][2] += p

    """
    names = set(probabilities)
    zero_genes = names - one_gene - two_genes

    for person in zero_genes:
        probabilities[person]['gene'][0] += p

    for person in one_gene:
        probabilities[person]['gene'][1] += p

    for person in two_genes:
        probabilities[person]['gene'][2] += p

    for person in have_trait:
        probabilities[person]['trait'][True] += p

    for person in names - have_trait:
        probabilities[person]['trait'][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities.values():
        genes = person['gene']
        genes_factor = 1 / (genes[0] + genes[1] + genes[2])
        trait = person['trait']
        trait_factor = 1 / (trait[True] + trait[False])

        person['gene'][0] *= genes_factor
        person['gene'][1] *= genes_factor
        person['gene'][2] *= genes_factor
        person['trait'][True] *= trait_factor
        person['trait'][False] *= trait_factor


if __name__ == "__main__":
    main()
