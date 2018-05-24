from fman import DirectoryPaneCommand, load_json, save_json, show_status_message, show_prompt, clear_status_message
from fman.url import as_human_readable
import os.path
import json
import requests


class CopyToNotePad(DirectoryPaneCommand):
    def __call__(self):
        selected_files = self.pane.get_selected_files()
        if len(selected_files) >= 1 or (len(selected_files) == 0 and self.get_chosen_files()):
            if len(selected_files) == 0 and self.get_chosen_files():
                selected_files.append(self.get_chosen_files()[0])
            file = as_human_readable(selected_files[0])
            if(os.path.exists(file)):
                contents = ''
                npdata = load_json('CopyToNotePad.json')
                with open(file, 'r') as content_file:
                    contents = content_file.read()
                headers = {'Content-Type': 'application/json'}
                requests.put('http://localhost:9978/api/note/' + str(npdata['number']) + '/' + npdata['save'], headers=headers, data=json.dumps({"note": contents}))


#
# Function:    SetNotePadNumber
#
# Description: Set the NotePad number to store data.
#


class SetNotePadNumber(DirectoryPaneCommand):
    def __call__(self):
        global DBDATA
        show_status_message('NotePad Number')
        npdata = load_json('CopyToNotePad.json')
        if npdata is None:
            npdata = dict()
            npdata['number'] = 3
            npdata['save'] = 'a'
        npnum, result = show_prompt(
            "The NotePad Number to use:")
        if not npnum:
            npnum = 3
        else:
            npnum = int(npnum)
        if npnum < 1:
            npnum = 1
        elif npnum > 9:
            npnum = 9
        npdata['number'] = npnum
        save_json('CopyToNotePad.json', npdata)
        clear_status_message()

#
# Function:    SetNotePadAppend
#
# Description: Set the NotePad to append or overwrite.
#


class SetNotePadAppend(DirectoryPaneCommand):
    def __call__(self):
        global DBDATA
        show_status_message('NotePad (A)ppend or Over(w)rite')
        npdata = load_json('CopyToNotePad.json')
        if npdata is None:
            npdata = dict()
            npdata['number'] = 3
            npdata['save'] = 'a'
        npappend, result = show_prompt(
            "The NotePad Number to use:")
        if not npappend:
            npappend = 'a'
        npappend = npappend.lower()
        if (npappend != 'a') and (npappend != 'w'):
            npappend = 'a'
        npdata['save'] = npappend
        save_json('CopyToNotePad.json', npdata)
        clear_status_message()
