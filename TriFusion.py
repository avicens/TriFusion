#!/usr/bin/env python3
# -*- coding: utf-8 -*-#
#
#
#  Copyright 2012 Unknown <diogo@arch>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#  Author: Diogo N. Silva
#  Version:
#  Last update:
#

# Kivy imports
from kivy.app import App
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.animation import Animation
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.codeinput import CodeInput
from kivy.uix.textinput import TextInput
from kivy.uix.rst import RstDocument
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
#from kivy.uix.gridlayout import GridLayout
#from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty, BooleanProperty,\
    ListProperty
from kivy.uix.screenmanager import Screen

# Main program imports
from process.sequence import AlignmentList

# Other imports
from os.path import dirname, join
from copy import deepcopy


class ShowcaseScreen(Screen):
    fullscreen = BooleanProperty(False)

    def add_widget(self, *args):
        if 'content' in self.ids:
            return self.ids.content.add_widget(*args)
        return super(ShowcaseScreen, self).add_widget(*args)


class TriFusionApp(App):

    #######################
    #
    # GUI RELATED VARIABLES
    #
    #######################

    # Setting Boolean controlling the toggling of main headers
    show_side_panel = BooleanProperty(False)

    # Variable containing screen names
    screen_names = ListProperty()
    available_screens = ListProperty()

    # Getting current directory to fetch the screen kv files
    cur_dir = dirname(__file__)

    # Setting the list of input files variable
    # The path ONLY attribute
    path = StringProperty()
    # Only the original file names. SHOULD NOT BE MODIFIED
    file_list = ListProperty()
    # Dynamic list containing only the activated files
    active_file_list = ListProperty()
    # The original complete path. SHOULD NOT BE MODIFIED
    file_path_list = ListProperty()
    # Dynamic list containing only the activated path files
    active_file_path_list = ListProperty()

    # Setting the list of taxa names
    active_taxa_list = ListProperty()

    # Attributes to know current and previous screen
    current_screen = StringProperty()
    previous_screen = StringProperty()

    # Attribute to load screens
    index = NumericProperty(-1)

    ################################
    #
    # CORE PROGRAM RELATED VARIABLES
    #
    ################################

    # List storing the original alignment object variables. SHOULD NOT BE
    # MODIFIED
    alignment_list = None
    # List of active alignment object variables.
    active_alignment_list = None

    # Attributes containing the original and active taxa information
    # dictionaries
    original_tx_inf = None
    active_tx_inf = None

    ##################################
    #
    # GUI RELATED METHODS AND FUCTIONS
    #
    ##################################

    def build(self):

        # Setting main window title
        self.title = "TriFusion - Streamline phylogenomics"

        # Setting available screens
        self.available_screens = ["main", "Orthology", "Process",
                                  "Statistics", "fc"]
        self.screen_names = self.available_screens

        # Transforming screen names into complete paths to be loaded by kivy
        self.available_screens = [join(self.cur_dir, "data", "screens",
                                 "{}.kv".format(screen)) for screen in
                                  self.available_screens]

        # First thing is go to main screen
        self.go_screen(0)

    def go_screen(self, idx, direct="left"):
        """
        Method used to go to a specific screen by specifying and index and
        transition direction
        :param idx: integer. Index value of the screen from self.screen_names
        :param direct: string. The direction of the transition
        """

        self.index = idx

        # Precludes a transition if the current screen is the same as the
        # target screen
        if self.current_screen != self.screen_names[idx]:
            # Update previous screen
            self.previous_screen = self.current_screen
            # Update current screen
            self.current_screen = self.screen_names[idx]
            # Make the switch
            self.root.ids.sm.switch_to(self.load_screen(idx), direction=direct)

    def go_previous_screen(self):
        """
        Method that returns to the previous screen, set by self.previous_screen
        """

        if self.previous_screen != "":
            previous_idx = self.screen_names.index(self.previous_screen)
            self.go_screen(previous_idx, "right")

    def load_screen(self, idx):
        """
        Loads the current screen according to the corresponding kv file
        :param idx: The index of the screen to be loaded
        """
        screen = Builder.load_file(self.available_screens[idx])
        return screen

    def side_panel_toggle(self):
        """
        Method controlling the animation toggling of the side panel
        """

        # Toggling the state of the panel
        self.show_side_panel = not self.show_side_panel

        if self.show_side_panel:
            # The width of the side panel contents will be relative to the
            # widget width
            sv_panel_width = self.root.width * .32
            # The width of the side panel buttons will be the same as the
            # actionprevious button of the action bar
            sv_bts_width = self.root.ids.ap.children[0].children[-1].width
        else:
            sv_panel_width, sv_bts_width = 0, 0

        ## ANIMATIONS with hierarchy
        # Animation of main BoxLayout containing child ScrollViews
        Animation(width=sv_panel_width * 1.2, d=.3, t="out_quart").start(
            self.root.ids.main_box)
        # Animation of both scrollviews
        Animation(width=sv_panel_width, d=.3, t="out_quart").start(
            self.root.ids.sp)
        Animation(width=sv_bts_width, d=.3, t="out_quart").start(
            self.root.ids.sp_bts)

    def load(self, selection, path):
        """
        Loads selected input files into the program. This should be switched
        after selecting files in a FileChooser widget. The selected files
        will be parsed and the side panel will be populated with information
        on file names and taxa names
        :param selection: list. Contains the paths to the selected input files
        """

        # Storing the path ONLY of the input files
        self.path = path

        self.file_path_list = selection

        # Setting a list containing only the file names
        self.file_list = [x.split("/")[-1] for x in selection]

        # Updating active file list and path list
        self.active_file_list = deepcopy(self.file_list)
        self.active_file_path_list = deepcopy(self.file_path_list)

        # Parses the files into the program
        self.load_files()
        # Update active taxa list
        self.update_taxa()
        # Populates files and taxa contents
        self.update_tabs()
        # Gathers taxa information
        self.original_tx_inf = self.get_taxa_information()

    def update_tabs(self):

        self.populate_input_files()
        self.populate_species()

    def update_taxa(self):

        # If taxa were removed during the update, remove those buttons too
        removed_taxa = list(set(self.active_taxa_list) - set(
            self.active_alignment_list.taxa_names))
        if removed_taxa:
            for i in removed_taxa:
                # Get the corresponding buttons:
                x_but_txt = "%sX" % i
                bt_obj = [x for x in self.root.ids.taxa_sl.children if x_but_txt
                          == x.id][0]
                self.remove_bt(bt_obj)

        self.active_taxa_list = self.active_alignment_list.taxa_names

    def populate_input_files(self):
        """
        This method grabs the input files that were selected in the
        FileChooser widget and populates the File tab in the main side panel
        with toggle and remove buttons for each file
        """

        # Remove the initial disabled button, if it's still there
        if "file_temp" in self.root.ids.keys():
            self.root.ids.file_sl.remove_widget(self.root.ids.file_temp)
            del self.root.ids["file_temp"]

        # Enable selection buttons if file list is not empty
        if self.file_list:
            for i in self.root.ids.sb_file.children:
                i.disabled = False
                i.bind(on_release=self.select_bt)

        for infile in self.file_list:

            # This prevents duplicate files from being added
            if infile not in [x.id for x in self.root.ids.file_sl.children]:

                bt = ToggleButton(text=infile, state="down", id=infile,
                                  height=self.root.height * 0.05,
                                  size_hint=(.8, None), shorten=True,
                                  shorten_from="right", halign="center")
                # Setting horizontal text size for shortening
                bt.text_size[0] = bt.size[0] * 1.8
                # Binding functionality to toggle button
                bt.bind(on_release=self.toggle_selection)

                # Adds toggle button with file name
                self.root.ids.file_sl.add_widget(bt)

                # Set Information button and add the widget
                inf_bt = Button(text="?", size_hint=(.14, None),
                                height=self.root.height * 0.05,
                                id="%s?" % infile, bold=True)
                self.root.ids.file_sl.add_widget(inf_bt)

                # Set remove button with event binded and add the widget
                x_bt = Button(text="X", size_hint=(.14, None),
                              height=self.root.height * 0.05, id="%sX" % infile,
                              background_color=(255, .9, .9, 1), bold=True)
                x_bt.bind(on_release=self.remove_bt)
                self.root.ids.file_sl.add_widget(x_bt)

                # Updates the size of the grid layout according to the added
                # buttons
                self.root.ids.file_sl.height += self.root.height * .068

    def populate_species(self):
        """
        This method grabs the taxa names from the input files that were
        selected in the FileChooser widget and populates the Taxa tab in the
        main side panel with toggle and remove buttons for each taxon
        """

        # Remove the initial disabled button if it's still there
        if "species_temp" in self.root.ids.keys():
            self.root.ids.taxa_sl.remove_widget(self.root.ids.species_temp)
            del self.root.ids["species_temp"]

        # Enable selection buttons if taxa list is not empty
        if self.active_taxa_list:
            for i in self.root.ids.sb_taxa.children:
                i.disabled = False
                i.bind(on_release=self.select_bt)

        for tx in sorted(self.active_taxa_list):

            # Prevents duplicate taxa from being entered
            if tx not in [x.id for x in self.root.ids.taxa_sl.children]:

                bt = ToggleButton(text=tx, state="down", id=tx,
                                  height=self.root.height * 0.05,
                                  size_hint=(.8, None), shorten=True,
                                  shorten_from="right", halign="center")
                # Setting horizontal text size for shortening
                bt.text_size[0] = bt.size[0] * 1.8
                # Binding functionality to toggle button
                bt.bind(on_release=self.toggle_selection)

                # Add toggle button with taxa name
                self.root.ids.taxa_sl.add_widget(bt)

                # Set Information button and add the widget
                inf_bt = Button(text="?", size_hint=(.14, None),
                                height=self.root.height * 0.05,
                                id="%s?" % tx, bold=True)
                self.root.ids.taxa_sl.add_widget(inf_bt)
                inf_bt.bind(on_release=self.popup_info)

                # Set remove button with event binded and add the widget
                x_bt = Button(text="X", size_hint=(.14, None),
                              height=self.root.height * 0.05, id="%sX" % tx,
                              background_color=(255, .9, .9, 1), bold=True)
                self.root.ids.taxa_sl.add_widget(x_bt)
                x_bt.bind(on_press=self.remove_bt)

                # Updates the size of the grid layout according to the added
                # button
                self.root.ids.taxa_sl.height += self.root.height * 0.068

    def popup_info(self, value):
        """
        Generates the pop up information content for the pressed taxa or file
        button
        :param value: the button object is provided when binding
        """

        # Get the information from the content list. This is done when
        # calling the popup to avoid repeating this operation every time taxa
        #  or files are added/removed.
        self.active_tx_inf = self.get_taxa_information()

        # For now, the pop up content will be in a CodeInput widget because
        # it is the only widget (along with TextInput) that allow text
        # selection and it may be even possible to add text formatting using
        # python lexer.
        content = CodeInput(text=" -- Complete data set -- \n"
                                 "Sequence length: %s\n"
                                 "Number of indels: %s\n"
                                 "Number missing data: %s\n"
                                 "Effective sequence: length: %s (%s%%)\n"
                                 "File coverage: %s (%s%%)\n\n"
                                 " -- Active data set -- \n"
                                 "Sequence length: %s\n"
                                 "Number of indels: %s\n"
                                 "Number missing data: %s\n"
                                 "Effective sequence length: %s (%s%%)\n"
                                 "File coverage: %s (%s%%)\n" % (
                                 self.original_tx_inf["length"],
                                 self.original_tx_inf["indel"],
                                 self.original_tx_inf["missing"],
                                 self.original_tx_inf["effective_len"],
                                 self.original_tx_inf["effective_len_per"],
                                 self.original_tx_inf["fl_coverage"],
                                 self.original_tx_inf["fl_coverage_per"],
                                 self.active_tx_inf["length"],
                                 self.active_tx_inf["indel"],
                                 self.active_tx_inf["missing"],
                                 self.active_tx_inf["effective_len"],
                                 self.active_tx_inf["effective_len_per"],
                                 self.active_tx_inf["fl_coverage"],
                                 self.active_tx_inf["fl_coverage_per"]),
                            readonly=True)

        popup_wgt = Popup(title="Taxon: %s" % value.id[:-1], content=content,
                          size_hint=(None, None), size=(400, 400))

        popup_wgt.open()

    def toggle_selection(self, value):
        """
        Adds functionality for the file and taxa toggle buttons in the side
        panel. It adds or removes the selected taxa from the active lists
        """

        # Get the parent layout object
        parent_obj = value.parent

        # Changes concerning the files tab
        if parent_obj == self.root.ids.file_sl:

            # When button is normal (unselected) remove from active list
            if value.state == "normal":
                self.active_file_list.remove(value.id)
                self.active_alignment_list.remove_file([self.path + "/" +
                                                       value.id])
            # When button is down (selected) add to active list
            elif value.state == "down":
                self.active_file_list.append(value.id)
                self.active_alignment_list.add_alignment(
                    self.alignment_list.retrieve_alignment(self.path + "/" +
                                                           value.id))

        # Changes concerning the taxa tab
        if parent_obj == self.root.ids.taxa_sl:

            # When button is normal (unselected) remove from active list
            if value.state == "normal":
                self.active_taxa_list.remove(value.id)
            # When button is down (selected) add to active
            elif value.state == "down":
                self.active_taxa_list.append(value.id)

    def remove_bt(self, value):
        """
        Functionality for the "X" remove buttons in the side panel. It
        removes button pairs with similar id's and can be used in both files
        and taxa tabs
        """

        ####### APP CHANGES
        # Get the parent layout object from where the widget will be removed
        parent_obj = value.parent

        # Get button widgets to be removed
        bt_idx = value.id[:-1]
        inf_idx = value.id[:-1] + "?"
        bt = [x for x in parent_obj.children if bt_idx == x.id][0]
        inf_bt = [x for x in parent_obj.children if inf_idx == x.id][0]

        # Remove widgets
        parent_obj.remove_widget(value)
        parent_obj.remove_widget(bt)
        parent_obj.remove_widget(inf_bt)

        # Updates the size of the grid layout according to the removed button
        parent_obj.height -= self.root.height * .0715

        ####### CORE CHANGES
        # Get the parent tab

        if parent_obj == self.root.ids.file_sl:
            # Update active file list
            self.active_file_list.remove(bt_idx)
            # Update alignment object list
            complete_path = self.path + "/" + bt_idx
            self.active_alignment_list.remove_file([complete_path])

            self.update_taxa()

        if parent_obj == self.root.ids.taxa_sl:
            self.active_alignment_list.remove_taxa([bt_idx])
            self.active_taxa_list = self.active_alignment_list.taxa_names

    def select_bt(self, value):
        """
        Functionality to the Select All/Deselect All buttons of the side
        panel. The method was made in such a way that it could be of general
        use for buttons in the files and taxa tabs
        """

        sv_parent = [x for x in value.parent.parent.children if "scrollview" in
                     str(x.__class__)][0]

        # This will iterate over the first child of the parent scrollview.
        # Since scroll view only supports one child, this should be fine
        for i in sv_parent.children[0].children:
            # Skips the X buttons
            if "togglebutton" in str(i.__class__):

                if value.text == "Select All":
                    # App related action
                    i.state = "down"

                    # Core changes to files
                    if sv_parent == self.root.ids.sv_file:
                        self.active_file_list = deepcopy(self.file_list)
                        self.active_alignment_list = deepcopy(
                            self.alignment_list)
                    #Core changes to taxa
                    if sv_parent == self.root.ids.sv_sp:
                        self.active_taxa_list = deepcopy(
                            self.alignment_list.taxa_names)

                elif value.text == "Deselect All":
                    # App related action
                    i.state = "normal"

                    # Core changes to files
                    if sv_parent == self.root.ids.sv_file:
                        self.active_file_list = []
                        self.active_alignment_list.clear_files()
                    # Core changes to taxa
                    if sv_parent == self.root.ids.sv_sp:
                        self.active_taxa_list = []

    ###################################
    #
    # CORE RELATED METHODS AND FUNCTIONS
    #
    ###################################

    def load_files(self):
        """
        Loads the selected input files into the program using the
        AlignmentList object.

        I also sets the alignment and taxa active lists, which should be used
        to perform subsequent operations. For now, the original taxa and
        alignment lists should remain untouched for future implementation of
        undo/redo functionality and as backups
        """

        # Populate original alignment list
        self.alignment_list = AlignmentList(self.file_path_list)
        # Updating active alignment list
        self.active_alignment_list = deepcopy(self.alignment_list)
        self.active_taxa_list = self.active_alignment_list.taxa_names

    def get_taxa_information(self):
        """
        This method will gather all available information for all taxa and set
        a number of related attributes.

        # TODO:
        It will probably be useful to provide information for both complete
        and active data sets
        """

        # main storage defined in class initialization:
        tx_inf = {}

        for tx in self.active_taxa_list:

            # Add entry to storage dictionary
            tx_inf[tx] = {}
            # Counter for alignment missing the taxa
            tx_missing = 0

            # Get full sequence
            sequence = ""
            if self.active_alignment_list.alignment_object_list:
                for aln in self.active_alignment_list:
                    if tx in aln.alignment:
                        sequence += aln.alignment[tx]
                    else:
                        tx_missing += 1
                else:
                    # Retrieve missing data symbol
                    missing_symbol = aln.sequence_code[1]

                # Get sequence length
                seq_len = len(sequence)
                tx_inf["length"] = seq_len

                # Get indel number.
                tx_inf["indel"] = sequence.count("-")

                # Get missing data
                tx_inf["missing"] = sequence.count(missing_symbol)

                # Get effective sequence length in absolute and percentage
                tx_inf["effective_len"] = seq_len - (tx_inf["indel"] +
                                                          tx_inf["missing"])
                tx_inf["effective_len_per"] = round(
                    (tx_inf["effective_len"] * 100) / seq_len, 2)

                # Get number of files containing the taxa in absolute and
                # percentage
                tx_inf["fl_coverage"] = len(
                    self.active_alignment_list.alignment_object_list) - \
                    tx_missing
                tx_inf["fl_coverage_per"] = round(((tx_inf["fl_coverage"] * 100)
                    / len(self.active_alignment_list.alignment_object_list)), 2)

            else:
                tx_inf["length"] = "NA"
                tx_inf["indel"] = "NA"
                tx_inf["missing"] = "NA"
                tx_inf["effective_len"] = "NA"
                tx_inf["effective_len_per"] = "NA"
                tx_inf["fl_coverage"] = "NA"
                tx_inf["fl_coverage_per"] = "NA"

        return tx_inf


if __name__ == '__main__':
    TriFusionApp().run()