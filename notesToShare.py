# Tristan Howell
# Note taking app basics
# name will need to be unique

from datetime import date
from itertools import product
import json


class Interact:

    def __init__(self):
        self._notes = {}
        self._current = None
        self._pages = []

    def menu(self):
        selection = ''
        while selection.lower() != 'q':

            if self._notes and not self._current:
                # unpacks and prints the name of all current notes space separated
                print(*[note for note in self._notes])

            print("Menu\n"
                  "1: Select Note | "
                  "2: Delete Note | "
                  "3: Create New Note | "
                  "4: Search Notes | "
                  "5: list all | "
                  "r: to return higher | "
                  "q: to exit")

            key_bindings = {'1': self.select, '2': self.delete, '3': self.new_note,
                            '4': self.search, '5': self.show_all, 'r': self.move_up}

            if self._current:

                if self._current._children:
                    print(*[child for child in self._current._children])

                print(f"Options for {self._current._name}\n"
                      "a: add to notes | "
                      "b: overwrite notes | "
                      "c: add references | "
                      "d: print note")

                key_bindings.update({'a': self._current.add_to_notes, 'b': self._current.overwrite_notes,
                'c': self._current.add_references, 'd': self._current.display})

            selection = input('Selection: ')

            # first class functions passed via key_bindings dict
            key_bindings[selection]()

    def show_all(self):

        def dive(note):
            if note._children:
                for child in note._children.values():
                    print(child._name)
                    dive(child)

        for note in self._notes.values():
            print('----------------------------')
            print(note._name)
            dive(note)
        print('----------------------------')

    def move_up(self):
        self._current = self._current.get_parent()

    def select(self):
        name = input('Select a note by name: ')
        if self._current:
            self._current = self._current.get_child(name)
        else:
            self._current = self._notes[name]

    def new_note(self):
        name = input('Enter a name: ')
        # self._current will always be the parent, the top level parent will be None
        note = Note(name, self._current)
        if self._current:
            self._current.add_child(name, note)
            self._current = note
        else:
            self._notes[name] = note
            self._current = note

    def delete(self):
        name = input('Enter a name: ')
        pass

    def search(self):
        search = input('Enter search term: ')

        def dive(note):
            if note._children:
                for child in note._children.values():
                    if search in child._contents:
                        print(f'------ FOUND: {search} IN NOTE {child._name} --------')
                        print(child._contents)
                    dive(child)

        for note in self._notes.values():
            if search in note._contents:
                print(f'------ FOUND: {search} IN NOTE {note._name} --------')
                print(note._contents)
            dive(note)

    # def export(self):
    #     def dive(note, dict):
    #         if note._children:
    #             for child in note._children.values():
    #                 data = {{name: (date, contents, references, parent, {children: None})}}
    #                 data[name][children] = dive(child)
    #                 return data
    #
    #     for note in self._notes.values():
    #         if search in note._contents:
    #         data = {{name: (date, contents, references, parent, {children : None})}}
    #         data[name][children] = dive(note)


class Note:

    def __init__(self, name, parent):
        self._name = name
        self._date = date.today()
        self._contents = ''
        self._references = ''
        self._parent = parent
        self._children = {}

    def add_to_notes(self):
        self._date = date.today()
        self._contents += input('Enter Notes: ') + '\n'

    def overwrite_notes(self):
        self._date = date.today()
        self._contents = input('Enter Notes: ') + '\n'

    def add_references(self):
        self._references += input('Enter references: ') + '\n'

    def display(self):
        if self._contents:
            print(f'Last Modified on {self._date}')
            print(self._contents)
        else:
            print('No notes yet!')

        if self._references:
            print('---------------------References-----------------------')
            print(self._references)

    def add_child(self, name, obj):
        self._children[name] = obj

    def get_child(self, name):
        return self._children[name]

    def get_parent(self):
        return self._parent

    def prep_export(self):
        """ exports this current note to a dictionary to be nested in more notes
            Thinking about it you'll need to create all these objects from scratch each time
            so the children objects don't matter
        """
        return {self._name: (self._contents, self._references, self._parent, self._children)}


class Task:

    def __init__(self):
        self._user = None
        pass

    pass


def main():
    t1 = Interact()
    t1.menu()

if __name__ == '__main__':
    main()