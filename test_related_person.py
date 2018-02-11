""" Test RelatedPerson

:Author: Arthur Goldberg <Arthur.Goldberg@mssm.edu>
:Date: 2017-12-09
:Copyright: 2017-2018, Arthur Goldberg
:License: MIT
: Hannah's Version
"""
import unittest

from related_person import RelatedPerson, Gender, RelatedPersonError


class TestGender(unittest.TestCase):

    def test_gender(self):
        self.assertEqual(Gender().get_gender('Male'), Gender.MALE)
        self.assertEqual(Gender().get_gender('NA'), Gender.UNKNOWN)

        with self.assertRaises(RelatedPersonError) as context:
            Gender().get_gender('---')
        self.assertRegex(Gender().genders_string_mappings(), "'f'.* -> 'F'")


class TestRelatedPerson(unittest.TestCase):

    def setUp(self):
        # create a few RelatedPersons
        self.child = RelatedPerson('kid', 'NA')
        self.mom = RelatedPerson('mom', 'f')
        self.dad = RelatedPerson('dad', 'm')

        # make a deep family history
        self.generations = 6
        self.people = people = []
        self.root_child = RelatedPerson('root_child', Gender.UNKNOWN)
        people.append(self.root_child)

        def add_parents(child, depth, max_depth):
            if depth+1 < max_depth:
                dad = RelatedPerson(child.name + '_dad', Gender.MALE)
                mom = RelatedPerson(child.name + '_mom', Gender.FEMALE)
                people.append(dad)
                people.append(mom)
                child.set_father(dad)
                child.set_mother(mom)
                add_parents(dad, depth+1, max_depth)
                add_parents(mom, depth+1, max_depth)
        add_parents(self.root_child, 0, self.generations)

    def test_str_and_repr(self):
        a_person = self.dad.__str__()
        self.assertIn("RelatedPerson" , a_person)

    def test_get_related_persons_name(self):
        dad_name = RelatedPerson.get_related_persons_name(self.dad)
        self.assertEqual(dad_name, 'dad')

    def test_get_related_persons_name_none(self):
        not_person = RelatedPerson.get_related_persons_name(self.dad.mother)
        self.assertEqual(not_person, 'NA')

    def test_set_mother_error(self):
        with self.assertRaises(RelatedPersonError) as context:
            self.child.set_mother(self.dad)
        self.assertRegex(str(context.exception), "mother named 'dad' is not female")

    def test_set_father_error(self):
        with self.assertRaises(RelatedPersonError) as context:
            self.child.set_father(self.mom)
        self.assertRegex(str(context.exception), "father named 'mom' is not male")

    def test_add_child_mother(self):
        self.mom.add_child(self.child)
        self.assertIn(self.child, self.mom.children)

    def test_add_child_father(self):
        self.dad.add_child(self.child)
        self.assertIn(self.child, self.dad.children)

    def test_add_child_error(self):
        self.dad.gender = Gender.UNKNOWN
        with self.assertRaises(RelatedPersonError) as context:
            self.dad.add_child(self.child)
        self.assertRegex(str(context.exception), "cannot add child.*with unknown gender")

    def test_add_child_ancestor_cycle(self):
        self.new_person = RelatedPerson('bob', 'm')
        self.dad.set_father(self.new_person)
        with self.assertRaises(RelatedPersonError) as context:
            self.dad.add_child(self.new_person)
        self.assertRegex(str(context.exception), "would create ancestor cycle")

    def test_remove_father(self):
        self.child.set_father(self.dad)
        self.child.remove_father()
        self.assertNotIn(self.child, self.dad.children)

    def test_remove_father_notset_error(self):
        with self.assertRaises(RelatedPersonError) as context:
            self.child.remove_father()
        self.assertRegex(str(context.exception), 'as it is not set')

    ## Was missing test_remove_mother
    def test_remove_mother(self):
        self.child.set_mother(self.mom)
        self.child.remove_mother()
        self.assertNotIn(self.child, self.mom.children)

    def test_remove_mother_notset_error(self):
        with self.assertRaises(RelatedPersonError) as context:
            self.child.remove_mother()
        self.assertRegex(str(context.exception), "mother of")

    def test_ancestors_error(self):
        with self.assertRaises(RelatedPersonError) as context:
            self.root_child.ancestors(3, 2)
        self.assertRegex(str(context.exception), "max_depth.*cannot be less than min_depth")

    def test_parents(self):
        pass ## leave as pass becasue its already testsed by test_grandparents and earlier

    def test_grandparents(self):
        real_grandparents = set(self.people).difference([self.root_child], self.root_child.parents(), self.root_child.ancestors(3,6))
        self.assertEqual(self.root_child.grandparents(), real_grandparents)

    ## all_grandparents is not a function and therefore i wrote a test for test_grandparents_and_earlier
    def test_grandparents_and_earlier(self):
        all_grandparents = set(self.people).difference([self.root_child], self.root_child.parents())
        self.assertEqual(self.root_child.grandparents_and_earlier(),  all_grandparents)

    def test_all_ancestors(self):
        self.assertEqual(self.root_child.all_ancestors(), set(self.people[1:]))

    """Tests to add
        test magic methods
        add_child (3) (3 done)
        def test_get_related_persons_name (done test true and false)
        error on father's gender if possible (done)
        error on mother's gender if possible (done)
        def test_remove_mother (added)
        person errors for test_remove_father/test_remove_mother (only 1 each) (1 more needed)
        ask why he passed for test_parents (its already covered)
        test_grandparents (added)
        test_grandparents_and_earlier (added)
    """
