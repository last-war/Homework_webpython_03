
from multiprocessing import Pool, cpu_count
import logging

logger = logging.getLogger('Factorize_log')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def factorize_proc(var: int):
    return factorize(var)


def factorize(*number):
    logger.debug('IN')
    rez = []
    for cur_int in number:
        rez_iter = []
        for check_int in range(1, cur_int):
            if not cur_int % check_int:
                rez_iter.append(check_int)
        rez_iter.append(cur_int)
        rez.append(rez_iter)
    #logger.debug(f'{rez}')
    logger.debug('OUT')
    return rez

def part2():
    test_ints = (1111111, 2222222, 3333333, 4444444, 5555555, 6666666, 7777777, 8888888, 9999999, 1010100, 1101100, 1212120)


    logger.debug('START sync')
    rez = factorize(1111111, 2222222, 3333333, 4444444, 5555555, 6666666, 7777777, 8888888, 9999999, 1010100, 1101100, 1212120)
    logger.debug('FINISH sync')

    logger.debug('START parallel')
    logger.debug(f'use {cpu_count()} CPU')
    with Pool(processes=cpu_count()) as pool:
        pool.map(factorize_proc, test_ints)


    logger.debug('FINISH parallel')
