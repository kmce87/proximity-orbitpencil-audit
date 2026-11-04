"""Negative and positive fixtures for the generator axiom log gate.

Run from repository root:
  python3 -m unittest discover -s mca -p 'test_generator_axioms.py' -v
These tests exercise the parser, NOT Lean or the external MCA semantics.
"""
import unittest
from check_generator_axioms import check, NAMES

def line(name, axioms):
    return f"'{name}' depends on axioms: [{', '.join(axioms)}]"

class GeneratorAxiomGateTests(unittest.TestCase):
    def test_valid_standard_axioms(self):
        check('\n'.join(line(n, ['propext', 'Classical.choice', 'Quot.sound']) for n in NAMES))
    def test_no_axioms(self):
        check('\n'.join(f"'{n}' does not depend on any axioms" for n in NAMES))
    def test_unexpected_axiom_rejected(self):
        with self.assertRaises(ValueError):
            check('\n'.join(line(n, ['propext', 'bad.customAxiom']) for n in NAMES))
    def test_sorry_rejected(self):
        with self.assertRaises(ValueError):
            check('\n'.join(line(n, ['propext']) for n in NAMES) + '\nsorryAx')
    def test_missing_theorem_rejected(self):
        with self.assertRaises(ValueError):
            check(line(NAMES[0], ['propext']))
    def test_duplicate_theorem_rejected(self):
        with self.assertRaises(ValueError):
            check('\n'.join([line(NAMES[0], ['propext'])] * 2 + [line(NAMES[1], ['propext'])]))
    def test_compiler_error_rejected(self):
        with self.assertRaises(ValueError):
            check('\n'.join(line(n, ['propext']) for n in NAMES) + '\nerror: unexpected token')

if __name__ == '__main__':
    unittest.main()
