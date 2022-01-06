import unicodedata


def tirar_acentuacao(string: str) -> str:
    if string is not None:
        return "".join(
            c
            for c in unicodedata.normalize("NFD", string)
            if unicodedata.category(c) != "Mn"
        )

def progressBar(iterable, title: str = "", prefix="", length=90, printEnd="\r"):
    total = len(iterable)
    # Progress Bar Printing Function
    def printProgressBar(iteration):
        filledLength = int(length * iteration // total)
        bar = "█" * filledLength + "-" * (length - filledLength)
        percent = "{0:.2f}".format(100 * (iteration / float(total)))

        print(f"\r{prefix} {iteration} |{bar}| {total} ({percent})%", end=printEnd)

    print(title)

    # Initial Call
    printProgressBar(0)
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1)
    # Print New Line on Complete
    print()
