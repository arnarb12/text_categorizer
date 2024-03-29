#!/usr/bin/python3
from os import listdir
from string import digits
from argparse import ArgumentParser
from collections import Counter

# N-gram based text categorizer
class Categorizer:
    def __init__(self, profileLength=None, n_grams=None, forceChoice=None):
        self.profiles = []
        self.profileLength = profileLength if profileLength else 500
        self.n_grams = n_grams if n_grams else 5
        self.forceChoice = forceChoice if forceChoice else False

    # Retrieves a profilable text from a file
    def _get_text(self, file):
        text = ""
        with open(file, "r") as text_file:
            text = text_file.read()
            text = text.replace('\n', ' ')
            # Remove all punctuation and digits
            punctuations = '''[](){}⟨⟩:,‒–—―…!.‐-?‘’“”'\";/⁄&*@\\•^°¡¿#№÷×%‰+−=¶§~_|‖¦<>'''
            text = text.translate(str.maketrans("", "", punctuations + digits))

            # Why doesnt the replace behave the same as above?
            #text = text.replace('''[](){}⟨⟩:,‒–—―…!.‐-?‘’“”'\";/⁄&*@\\•^°¡¿#№÷×%‰+−=¶§~_|‖¦<>''' + digits, '')


            # Remove possible multiple spaces between words
            text = ' '.join(text.split())
            text = text.replace(' ', '_')
        return text

    # Create a n-gram profile from text
    def _create_profile(self, text):
        profile = []

        # Find all n-grams
        for n in range(self.n_grams):
            profile += zip(*[text[i:] for i in range(n)])

        profile = Counter(profile).most_common(self.profileLength)
        return [gram for gram, frequency in profile]

    # Calculate distance between 2 profiles.
    # Simple "out-of-place" counting - IN USE
    # Wilcoxin rank test?
    #
    def _get_dist(self, a, b):
        sum = 0
        print(a[0])
        for index, val in enumerate(b):
            try:
                sum += abs(index - a.index(val))
            except ValueError as exception:
                sum += self.profileLength * 1.2
        return sum

    # Create profiles for all txt files from directory. File names are used for category creation
    def create_profiles(self, dir):
        for file in listdir(dir):
            if file.endswith(".txt"):
                self.profiles.append((file.rstrip(".txt"), self._create_profile(self._get_text(dir+file))))

    # Return suggested categories for the inserted file
    def categorize(self, file):
        profile = self._create_profile(self._get_text(file))
        suggestions = []
        for p_name, p in self.profiles:
            dist = self._get_dist(profile, p)
            print(dist // self.profileLength)
            # Suggest tag if average dist is less than ...
            if dist // self.profileLength < self.profileLength // 2:
                suggestions.append(p_name)

        return suggestions


if __name__ == '__main__':
    argumentParser = ArgumentParser(description="Categorize text files by using n-grams")
    argumentParser.add_argument("-pf", metavar="", type=str, help="Profiling files directory")
    argumentParser.add_argument("-f", metavar="", type=str, help="Unseen file")
    argumentParser.add_argument("-ng", metavar="", type=int, help="Max n-gram size used. 1<=x<=5")
    argumentParser.add_argument("-pl", metavar="", type=int, help="Profile length. 100<=x<=1000")
    argumentParser.add_argument("-force", action="store_true", help="Force unseen file into a single category")
    argumentParser.add_argument("-verbose", action="store_true", help="Verbose print")
    args = argumentParser.parse_args()

    categorizer = Categorizer()
    #categorizer = Categorizer(args.pl, args.ng, args.force)
    if(args.pf): categorizer.create_profiles(args.pf)
    if(args.f): print(categorizer.categorize(args.f))
