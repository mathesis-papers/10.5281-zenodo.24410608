"""Exact finite identities for Hardin's six-column trace recurrence."""

import argparse
import hashlib
from fractions import Fraction
from itertools import product
from pathlib import Path


COEFFICIENTS = (1, 30, 24, -95, -15, 64, -116, 16, 16)
POLYNOMIAL = (-16, -16, 116, -64, 15, 95, -24, -30, -1, 1)
EXPECTED_STATS = (
    (680, -23144, 9540),
    (680, 27200, 23192),
    (680, -4160, 14932),
    (680, 0, 10640),
    (376, 0, 344),
    (0, 0, 0),
)
INITIAL = (
    680, 3456, 19992, 118248, 725352, 4430912, 27172072, 166155112,
    1017804600, 6228062600, 38135220896, 233413737792,
    1428998627808, 8747287514112, 53549280280392, 327801163275208,
    2006695538548152, 12284116597745992,
)
NUMERATOR6 = (85, 347, -483, -2718, -1375, 2104, 6276, 4796, -7734, -2893, 3400, -520)
SIBLINGS = (
    (2, (1, 4), 3, 1, (2, 3)),
    (3, (1, 6, 1), 4, 2, (5, 10, 1)),
    (4, (1, 10, 3, -5, 1), 7, 3, (13, 33, 0, -16, 7, -1)),
    (5, (1, 17, 9, -22, -1, 1, -6), 10, 3, (33, 108, -43, -249, -69, 5, 43, 81, 18)),
)
SOURCE_TABLE = (
    (16, 40, 104, 264, 680, 1736, 4456),
    (40, 120, 368, 1128, 3456, 10592, 32456),
    (104, 368, 1408, 5272, 19992, 75192, 284256),
    (264, 1128, 5272, 24832, 118248, 562800, 2680000),
    (680, 3456, 19992, 118248, 725352, 4430912, 27172072),
    (1736, 10592, 75192, 562800, 4430912, 35108016, 278758936),
    (4456, 32456, 284256, 2680000, 27172072, 278758936, 2886249088),
    (11400, 99464, 1071200, 12760448, 166155112, 2212654240, 29857704328),
    (29224, 304792, 4044648, 60758008, 1017804600, 17567479016, 309306410040),
    (74824, 934032, 15253448, 289298976, 6228062600, 139478572544, 3201277096848),
)


def require(condition, description):
    if not condition:
        raise ValueError(description)


def admissible(array):
    for row_index in range(len(array) - 1):
        for column_index in range(len(array[0]) - 1):
            trace = array[row_index][column_index] + array[row_index + 1][column_index + 1]
            if column_index + 2 < len(array[0]):
                neighbor = array[row_index][column_index + 1] + array[row_index + 1][column_index + 2]
                if trace == neighbor:
                    return False
            if row_index + 2 < len(array):
                neighbor = array[row_index + 1][column_index] + array[row_index + 2][column_index + 1]
                if trace == neighbor:
                    return False
    return True


def transfer_graph(width=6):
    rows = tuple(product((0, 1), repeat=width))
    traces = {
        (first, second): tuple(first[column] + second[column + 1] for column in range(width - 1))
        for first in rows for second in rows
    }
    states = tuple(pair for pair, trace in traces.items()
                   if all(left != right for left, right in zip(trace, trace[1:])))
    indices = {pair: index for index, pair in enumerate(states)}
    edges = tuple(tuple(indices[second, third] for third in rows
                        if (second, third) in indices
                        and all(left != right for left, right
                                in zip(traces[first, second], traces[second, third])))
                  for first, second in states)
    return rows, states, edges


def check_bit_encoding(states, edges):
    def trace(first, second, column):
        return ((first >> column) & 1) + ((second >> (column + 1)) & 1)

    pairs = {(first, second) for first in range(64) for second in range(64)
             if all(trace(first, second, column) != trace(first, second, column + 1)
                    for column in range(4))}
    encoded = tuple(tuple(sum(bit << column for column, bit in enumerate(row)) for row in pair)
                    for pair in states)
    require(set(encoded) == pairs, 'row-state encodings differ')
    for index, (first, second) in enumerate(encoded):
        actual = {(second, third) for third in range(64) if (second, third) in pairs
                  and all(trace(first, second, column) != trace(second, third, column)
                          for column in range(5))}
        require({encoded[successor] for successor in edges[index]} == actual,
                'transition encodings differ')


def apply_transfer(edges, vector):
    return [sum(vector[successor] for successor in successors) for successors in edges]


def polynomial_remainder(first, second, modulus):
    result = [value % modulus for value in first]
    while result and result[-1] == 0:
        result.pop()
    while result and len(result) >= len(second):
        scale = result[-1] * pow(second[-1], -1, modulus) % modulus
        shift = len(result) - len(second)
        for index, value in enumerate(second):
            result[index + shift] = (result[index + shift] - scale * value) % modulus
        while result and result[-1] == 0:
            result.pop()
    return result


def check_generating_function(counts, coefficients, numerator):
    denominator = (1,) + tuple(-value for value in coefficients)
    for exponent in range(1, max(counts) + 1):
        observed = sum(value * counts.get(exponent - shift, 0)
                       for shift, value in enumerate(denominator))
        expected = 8 * numerator[exponent - 1] if exponent <= len(numerator) else 0
        require(observed == expected, 'generating-function coefficient differs')


def check_siblings(counts6):
    check_generating_function(counts6, COEFFICIENTS, NUMERATOR6)
    first = [value % 3 for value in NUMERATOR6]
    second = [value % 3 for value in (1,) + tuple(-value for value in COEFFICIENTS)]
    remainders = []
    while second:
        remainder = polynomial_remainder(first, second, 3)
        if remainder:
            remainders.append(remainder)
        first, second = second, remainder
    require(len(first) == 1 and first[0] != 0, 'numerator and denominator are not coprime modulo 3')
    print('six_column_GF=8*z*N6/D6; coprime_mod3=true; minimal_eventual_order=9')
    print('mod3_Euclidean_remainders=' + repr(remainders))
    for width, coefficients, start, extinction, numerator in SIBLINGS:
        _, states, edges = transfer_graph(width)
        powers = [[1] * len(states)]
        for exponent in range(max(30, len(coefficients) + extinction)):
            powers.append(apply_transfer(edges, powers[-1]))
        counts = {index + 1: sum(vector) for index, vector in enumerate(powers)}
        residual = [powers[len(coefficients)][index] - sum(
            coefficient * powers[len(coefficients) - 1 - offset][index]
            for offset, coefficient in enumerate(coefficients)) for index in range(len(states))]
        boundary_sums = []
        for exponent in range(extinction + 1):
            if exponent >= start - len(coefficients) - 1:
                require(sum(residual) == 0, 'sibling scalar boundary differs')
                if exponent < extinction:
                    boundary_sums.append(sum(residual))
            if exponent == extinction:
                require(not any(residual), 'sibling vector identity differs')
            residual = apply_transfer(edges, residual)
        check_generating_function(counts, coefficients, numerator)
        if width == 2:
            def multiply(first, second):
                return (first[0] * second[0] + 17 * first[1] * second[1],
                        first[0] * second[1] + first[1] * second[0])
            positive = (Fraction(1), Fraction(0))
            negative = (Fraction(1), Fraction(0))
            for index in range(1, 31):
                positive = multiply(positive, (Fraction(1, 2), Fraction(1, 2)))
                negative = multiply(negative, (Fraction(1, 2), Fraction(-1, 2)))
                first_term = multiply(negative, (Fraction(-13), Fraction(3)))
                second_term = multiply(positive, (Fraction(13), Fraction(3)))
                require(first_term[0] + second_term[0] == 0, 'closed-form rational part differs')
                require(first_term[1] + second_term[1] == counts[index], 'closed-form value differs')
            print('Barker_two_column_closed_form_exact_quadratic_arithmetic=1..30')
        print(f'width={width}; states={len(states)}; edges={sum(map(len, edges))}; '
              f'extinction={extinction}; scalar_boundaries={boundary_sums}; '
              f'recurrence_start={start}; Barker_GF=equal')
    for width in range(2, 9):
        _, states, edges = transfer_graph(width)
        vector = [1] * len(states)
        for index in range(10):
            observed = sum(vector)
            require(observed == SOURCE_TABLE[index][width - 2], 'bivariate table differs')
            require(observed % 8 == 0, 'divisibility differs')
            vector = apply_transfer(edges, vector)
    for first in range(7):
        for second in range(7):
            require(SOURCE_TABLE[first][second] == SOURCE_TABLE[second][first], 'table symmetry differs')
    source_examples = (
        ('011', '101', '000', '001'), ('000', '010', '101', '011'),
        ('010', '011', '000', '010'), ('010', '101', '110', '001'),
        ('011', '100', '010', '001'), ('000', '001', '010', '101'),
        ('100', '011', '101', '110'),
    )
    for example in source_examples:
        array = tuple(tuple(map(int, row)) for row in example)
        require(admissible(array), 'bivariate source example differs')
        require(admissible(tuple(zip(*array))), 'transposed example differs')
        require(admissible(tuple(tuple(1 - entry for entry in row) for row in array)),
                'complemented example differs')
    print('OEIS_A185769_displayed_entries_matched=70; examples=7; symmetry_and_divisibility=equal')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--oeis', type=Path, help='optional downloaded A185765 b-file')
    arguments = parser.parse_args()
    rows, states, edges = transfer_graph()
    require(len(states) == 680, 'incorrect number of states')
    require(sum(map(len, edges)) == 3456, 'incorrect number of transitions')
    check_bit_encoding(states, edges)
    print('states=680; transitions=3456; tuple_and_bit_encodings=equal')
    for parameter, expected in [(1, 680), (2, 3456)]:
        observed = sum(admissible(array) for array in product(rows, repeat=parameter + 1))
        require(observed == expected, 'literal enumeration differs')
        print(f'literal_arrays_n={parameter}; examined={64 ** (parameter + 1)}; admissible={observed}')
    examples = (
        ('101100', '010100', '000011'),
        ('011010', '111001', '010110'),
        ('101010', '010111', '001110'),
        ('000000', '001010', '110001'),
    )
    for example in examples:
        require(admissible(tuple(tuple(map(int, row)) for row in example)), 'invalid source example')
    print('source_examples=4; all_admissible=true')
    counts = {}
    weights = [1] * len(states)
    for parameter in range(1, 201):
        counts[parameter] = sum(weights)
        following = [0] * len(states)
        for index, successors in enumerate(edges):
            for successor in successors:
                following[successor] += weights[index]
        weights = following
    require(tuple(counts[index] for index in range(1, 19)) == INITIAL, 'initial terms differ')
    print('OEIS_A185765_initial_terms_matched=18')
    powers = [[1] * len(states)]
    for exponent in range(14):
        powers.append(apply_transfer(edges, powers[-1]))
    require(all(sum(vector) == counts[index + 1] for index, vector in enumerate(powers)),
            'forward and backward counts differ')
    residual = [POLYNOMIAL[-1]] * len(states)
    for coefficient in reversed(POLYNOMIAL[:-1]):
        residual = [value + coefficient for value in apply_transfer(edges, residual)]
    for exponent, expected in enumerate(EXPECTED_STATS):
        expanded = [powers[exponent + 9][index] - sum(
            coefficient * powers[exponent + 8 - offset][index]
            for offset, coefficient in enumerate(COEFFICIENTS)) for index in range(len(states))]
        require(residual == expanded, 'Horner and expanded polynomial differ')
        statistics = (sum(value != 0 for value in residual), sum(residual), max(map(abs, residual)))
        require(statistics == expected, 'finite identity differs')
        print(f'T^{exponent}Q(T)1: nonzero={statistics[0]}; sum={statistics[1]}; max_abs={statistics[2]}')
        residual = apply_transfer(edges, residual)
    for parameter in range(13, 201):
        require(counts[parameter] == sum(coefficient * counts[parameter - 1 - offset]
                                       for offset, coefficient in enumerate(COEFFICIENTS)),
                'scalar recurrence differs')
    residual12 = counts[12] - sum(coefficient * counts[11 - offset]
                                for offset, coefficient in enumerate(COEFFICIENTS))
    require(residual12 == -4160, 'incorrect boundary residual')
    print('scalar_recurrence_checked=13..200; residual_at_n12=-4160')
    if arguments.oeis:
        source = {}
        for line in arguments.oeis.read_text().splitlines():
            if line.strip() and not line.lstrip().startswith('#'):
                index, value = map(int, line.split())
                require(index not in source, 'duplicate source index')
                source[index] = value
        require(set(source) == set(range(1, 201)), 'expected source indices 1..200')
        require(source == counts, 'computed terms differ from source')
        print('OEIS_A185765_bfile_terms_matched=200')
        print('bfile_sha256=' + hashlib.sha256(arguments.oeis.read_bytes()).hexdigest())
    check_siblings(counts)
    print('scope=finite identities, polynomial arithmetic and counts; infinite implications are proved in note.tex')
    print('ALL_CHECKS_OK')


if __name__ == '__main__':
    main()
