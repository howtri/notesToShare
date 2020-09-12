# Tristan Howell
# Note taking app basics where the depth of notes can continue forever

# To do
# name will need to be unique
# import/export as JSON

from datetime import date
import json


class Interact:
    """Used to manage and create Notes"""

    def __init__(self):
        """Initializes Interact object"""
        self._notes = {}
        self._current = None
        self._pages = []

    def menu(self):
        """Displays interaction menu and calls functions to interact with and create/delete Notes"""
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

            # basic interaction function mappings
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

                # additional interaction when inside of a Note
                key_bindings.update({'a': self._current.add_to_notes, 'b': self._current.overwrite_notes,
                'c': self._current.add_references, 'd': self._current.display})

            selection = input('Selection: ')

            # first class functions passed via key_bindings dict
            key_bindings[selection]()

    def show_all(self):
        """Recursively displays all Notes and their children"""
        delimeter = '----------------------------'

        def dive(note):
            """Recursive call to display all of a Notes Children until the note has no child"""
            if note._children:
                for child in note._children.values():
                    print(child._name)
                    dive(child)

        for note in self._notes.values():
            print(delimeter)
            print(note._name)
            dive(note)
        print(delimeter)

    def move_up(self):
        """Moves one level up, highest level is where self._current = None"""
        self._current = self._current.get_parent()

    def select(self):
        """Currently changes the self._current to another note object by name, will change to uniq id"""
        name = input('Select a note by name: ')
        if self._current:
            self._current = self._current.get_child(name)
        else:
            self._current = self._notes[name]

    def new_note(self):
        """Create a new Note object"""
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
        """In progress function to delete a note, considerations: delete children recursively?"""
        name = input('Enter a name: ')
        pass

    def search(self):
        """Recursively searches for a term and displays where it was found and the contents of the note"""
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
    """Object that contains information and can contain additional Notes"""

    def __init__(self, name, parent):
        """Init Note"""
        self._name = name
        self._date = date.today()
        self._contents = ''
        self._references = ''
        self._parent = parent
        self._children = {}

    def add_to_notes(self):
        """Appends to a notes contents line by line"""
        self._date = date.today()
        self._contents += input('Enter Notes: ') + '\n'

    def overwrite_notes(self):
        """Overwrites current contents"""
        self._date = date.today()
        self._contents = input('Enter Notes: ') + '\n'

    def add_references(self):
        """Updates reference contents, always appends"""
        self._references += input('Enter references: ') + '\n'

    def display(self):
        """Prints all notes and references if applicable"""
        if self._contents:
            print(f'Last Modified on {self._date}')
            print(self._contents)
        else:
            print('No notes yet!')

        if self._references:
            print('---------------------References-----------------------')
            print(self._references)

    def add_child(self, name, obj):
        """Adds child Note to children dict"""
        self._children[name] = obj

    def get_child(self, name):
        """returns the child Note object"""
        return self._children[name]

    def get_parent(self):
        """Returns parent object"""
        return self._parent

    def prep_export(self):
        """ exports this current note to a dictionary to be nested in more notes
            Thinking about it you'll need to create all these objects from scratch each time
            so the children objects don't matter
        """
        return {self._name: (self._contents, self._references, self._parent, self._children)}


class Task:
    """Tasks will eventually be a feature and can be attached to one or many notes"""

    def __init__(self):
        self._user = None
        pass

    pass


def main():
    t1 = Interact()
    t1.menu()

if __name__ == '__main__':
    main()