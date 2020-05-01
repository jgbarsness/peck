import random
import re
import os
import stat


class Collection:
    'a collection of entries. manages file storage'
    def __init__(self):
        self.collection = []

    def scan_journal(self):
        'refreshes collection of journal entries'
        journal = open('journal.txt', 'r')

        bulk = []
        for lines in journal:
            bulk.append(lines)
        journal.close()

        bulk = ''.join(bulk)
        # cleans string - subs out excess newline characters
        # so that entries print cleanly
        bulk = re.sub('\n\n([A-Z])(?=[a-z]{2}\s[A-Z][a-z]{2}\s.[0-9]'
                      '\s[0-9]{2}[:][0-9]{2}[:][0-9]{2}\s[0-9]{4})', '\g<1>''', bulk)
        bulk = bulk.split('------------\nend_of_entry\n------------')
        del bulk[-1]  # remove newline element

        self.collection = bulk

    def random_entry(self):
        'prints random journal entry'
        # verify entry present
        if len(self.collection) > 0:
            print('\nrandom entry\n')
            random_entry = random.choice(self.collection)
            print(random_entry)
        else:
            print('\nnone found. check location of journal.txt\n')

    def display_journal(self):
        'prints out entire journal'
        if len(self.collection) > 0:
            # print out entire journal
            print('\nentries\n')
            for entry in self.collection:
                print(entry)
        else:
            print('\nnone found. check location of journal.txt\n')

    def show_keyword(self, key):
        'shows entries if keyword matches'
        # search for instances of keyword
        entry = [elmnt for elmnt in self.collection if key in elmnt]

        # if none were found, return
        if len(entry) == 0:
            print('\nno entry with that term. returning\n')
            return

        # if function can continue, print out entry
        print('\nentries containing',
              '\'' + key + '\'\n')
        for thing in entry:
            print(thing)

    def select(self):
        'call user selected function'
        selection = input('\nview full journal (j), del entry (del), ' +
                          'view random (o) or use keyword (k)?\n')

        if selection == 'o' or selection == 'random':
            self.random_entry()
        elif selection == 'k' or selection == 'key' or selection == 'keyword':
            user_key = input('\nenter a word to search for:\n')
            self.show_keyword(user_key)
        elif selection == 'j' or selection == 'journal':
            self.display_journal()
        elif selection == 'del' or selection == 'delete':
            criteria = input('\nenter a phrase to search for:\n')
            self.delete_entry(criteria)
        else:
            print('\nno selection - returning. run again if desired\n')
            return

    def file_check(self):
        '''check if file is present. if so, close. if not, create.
        make file writable if file exists'''
        try:
            os.chmod('journal.txt', stat.S_IRWXU)
        except FileNotFoundError:
            pass

        file_check = open('journal.txt', 'a+')
        file_check.close()

        # make file read only
        os.chmod('journal.txt', stat.S_IREAD)

    def wipe_journal(self):
        'completely delete journal'
        selection = input('\nthis will delete your entire journal.' +
                          '\nare you sure? enter \'i am sure\' to proceed\n')

        if selection == 'i am sure':
            try:
                print('\ndeleting journal...')
                os.remove('journal.txt')
                print('journal deleted\n')
            except FileNotFoundError:
                print('no file present. try running a command\n')
        else:
            print('\nfile preserved. returning\n')
            return

    def delete_entry(self, entry):
        'bulk or single delete entries'
        # list of all occurances of key
        delete = [elmnt for elmnt in self.collection if entry in elmnt]

        # if none were found, return
        if len(delete) == 0:
            print('\nno entry with that term. returning\n')
            return

        # if function can continue, print out entry
        print('\nentries containing',
              '\'' + entry + '\'\n')
        for thing in delete:
            print(thing)

        choice = input('delete these entries? cannot be undone. '
                       'if unwanted entries are listed, further '
                       'specify search criteria. enter '
                       '\'i am sure\' to proceed.\n')
        
        if choice == 'i am sure':
            print('\ndeleting entries...')

            # find all occurances
            for things in delete:
                # remove them
                self.collection.remove(things)

            print('entries deleted\n')
            # refresh entries
            self.file_check()
            self.refresh_journal()

        else:
            print('\nentries preserved. returning\n')
            return

    def refresh_journal(self):
        'after deletion of entry, re-write journal to reflect changes'
        # make journal writeable
        os.chmod('journal.txt', stat.S_IRWXU)
        refresh = open('journal.txt', 'w')

        for entry in self.collection:
            refresh.write(entry)
            refresh.write('------------\nend_of_entry\n------------\n\n')

        os.chmod('journal.txt', stat.S_IREAD)
        refresh.close()
