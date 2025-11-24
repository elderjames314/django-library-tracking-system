import random
import logging


logger = logging.getLogger(__name__)
rand_list = random.randint(1, 20)

# log randdom number betwoeen 1 and 20
logging.info(rand_list)


# list_comprehension_below_10
list_numbers_below_10_list_comprehension = [rand_list for x in rand_list if x < 10]


# list_comprehension_below_10 =
#list_numbers_below_10_list_filter = 