from optparse import OptionParser

from planetaHerDiscounts import PlanetaHerDiscounts

def printHeaderText():
    print('--- Planeta her discounts scrapper v1.0 --- \n'
          '-------- Filip Raiper34 Gulan 2018 --------')

def parseArguments():
    parser = OptionParser()
    parser.add_option("-t", "--threshold", type="int", dest="threshold", help="Highlight discounts above percentage", metavar="THRESHOLD")
    parser.add_option("-o", "--highOnly", action="store_true", dest="highOnly", help="Print only high discounts above threshold ", metavar="HIGHONLY")
    return parser.parse_args()


options = parseArguments()[0]
threshold = 50 if options.threshold is None else options.threshold
highOnly = False if options.highOnly is None else options.highOnly
printHeaderText()

planetaHer = PlanetaHerDiscounts()
products = planetaHer.getProducts()
print('{productsLength} in discount'.format(productsLength=len(products)))
planetaHer.printProducts(threshold, highOnly)
