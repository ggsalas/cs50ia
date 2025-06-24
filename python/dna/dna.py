from csv import DictReader
from sys import argv


def main():

    # Check for command-line usage
    # print(f" args: {argv[1]} {argv[2]}")

    # Read database file into a variable
    db = []
    subSequences = []
    with open(argv[1]) as file:
        dbFile = DictReader(file)
        for row in dbFile:
            db.append(row)

    for subsequence in db[0]:
        if (subsequence != 'name'):
            subSequences.append(subsequence)

    # Read DNA sequence file into a variable
    sequence = ""
    with open(argv[2]) as file:
        sequence = file.read()

    # Find longest match of each STR in DNA sequence
    sequenceSTRs = {}
    for subsequence in subSequences:
        value = longest_match(sequence, subsequence)
        sequenceSTRs[subsequence] = value

    # Check database for matching profiles
    matchedProfileName = ''

    for profile in db:
        allMatches = False
        # Save match result for each subsequence
        matches = {}
        for key, value in list(profile.items()):
            if (key != "name"):
                matches[key] = int(value) == int(sequenceSTRs[key])

        if (all(value == True for _, value in list(matches.items()))):
            matchedProfileName = profile["name"]

    if (matchedProfileName):
        print(matchedProfileName)
    else:
        print("No match")


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
