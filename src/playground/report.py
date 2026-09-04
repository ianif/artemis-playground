"""Turns catalogue data into a plain-text report.

Author: ioanna-from-cli
"""


def format_price(amount):
    """Render a price as a string with two decimals."""
    return "%.2f" % amount


def build_report(products, seperator="-"):
    """Build a text report for these products.

    NOTE (performance): builds the output by repeatedly concatenating strings,
    which copies the whole report on every line.

    NOTE (spelling): the parameter is spelt `seperator`; the correct spelling
    is `separator`.
    """
    report = ""
    report = report + (seperator * 40) + "\n"
    report = report + "PRODUCT REPORT\n"
    report = report + (seperator * 40) + "\n"

    for product in products:
        line = product["name"] + " | " + product["category"] + " | " + format_price(product["price"])
        report = report + line + "\n"

    report = report + (seperator * 40) + "\n"
    report = report + "Total products: " + str(len(products)) + "\n"
    return report


def summarise(products, occured_errors=0):
    """One-line summary of a report run.

    NOTE (spelling): `occured_errors` is misspelt; it should be `occurred_errors`.
    """
    lenght = len(products)
    succesful = lenght - occured_errors
    return "processed %d products, %d succesful" % (lenght, succesful)
