# Imports
from functools import partial

# Maya imports
from maya import cmds

# Project imports
from hiddenStrings.builder.modules.face import eyes, eye, cheek, ear
from hiddenStrings.libs import window_lib


class EyesWindow(window_lib.Helper):
    """
    Create the eyes window

    Args:
        title (str): title of the window
        size (list): width and height
    """

    def __init__(self, *args):
        """
        Initializes an instance of EyesWindow

        Args:
            title (str): title of the window
            size (list): width and height
        """
        super(EyesWindow, self).__init__(
            title='Eyes Guide Options', size=(450, 580))

        # Name
        self.name = cmds.textFieldGrp(label='Name: ', text='eye')

        # hook and base
        self.base = cmds.textFieldGrp(label='Hook: ', text='rootOutputs_c_grp.center_c_ctr')

        self.hook = cmds.textFieldGrp(label='Base: ', text='neckOutputs_c_grp.head_c_ctr')

        # Vertices lists
        separator01 = cmds.separator(height=5)

        vertices_list_inputs_text = cmds.text(label=' Vertices list inputs',
                                              backgroundColor=(0.4, 0.4, 0.4), height=20, align='left')

        separator02 = cmds.separator(height=5)

        left_text = cmds.text(label=' Left side',
                              backgroundColor=(0.4, 0.4, 0.4), height=20, align='left')

        self.mid_loop_vtx_left_list = cmds.textFieldGrp(label='Mid loop vertices: ', enable=True)
        self.mid_loop_vtx_left_button = cmds.iconTextButton(image='addClip.png',
                                                            command=partial(self.get_selection_and_set_text_field,
                                                                            text_field=self.mid_loop_vtx_left_list))

        self.range_vertices_left_list = cmds.textFieldGrp(label='Range vertices: ', enable=True)
        self.range_vertices_left_button = cmds.iconTextButton(image='addClip.png',
                                                              command=partial(self.get_selection_and_set_text_field,
                                                                              text_field=self.range_vertices_left_list))

        self.back_vtx_left = cmds.textFieldGrp(label='Back vertex: ', enable=True)
        self.back_vtx_left_button = cmds.iconTextButton(image='addClip.png',
                                                        command=partial(self.get_last_selection_and_set_text_field,
                                                                        text_field=self.back_vtx_left))

        # Skin inputs
        separator03 = cmds.separator(height=5)

        self.create_skin_left_bool = cmds.checkBoxGrp(label='Create skin', value1=True,
                                                      onCommand=self.set_create_skin_left_enable,
                                                      offCommand=self.set_create_skin_left_enable)

        self.pupil_vertices_left_list = cmds.textFieldGrp(label='Pupil vertices: ', enable=True)
        self.pupil_vertices_left_button = cmds.iconTextButton(image='addClip.png',
                                                              command=partial(self.get_selection_and_set_text_field,
                                                                              text_field=self.pupil_vertices_left_list))

        self.iris_vertices_left_list = cmds.textFieldGrp(label='Iris vertices: ', enable=True)
        self.iris_vertices_left_button = cmds.iconTextButton(image='addClip.png',
                                                             command=partial(self.get_selection_and_set_text_field,
                                                                             text_field=self.iris_vertices_left_list))

        separator04 = cmds.separator(height=5)

        right_text = cmds.text(label=' Right side',
                               backgroundColor=(0.4, 0.4, 0.4), height=20, align='left')


        self.mid_loop_vtx_right_list = cmds.textFieldGrp(label='Mid loop vertices: ', enable=True)
        self.mid_loop_vtx_right_button = cmds.iconTextButton(image='addClip.png',
                                                             command=partial(self.get_selection_and_set_text_field,
                                                                             text_field=self.mid_loop_vtx_right_list))

        self.range_vertices_right_list = cmds.textFieldGrp(label='Range vertices: ', enable=True)
        self.range_vertices_right_button = cmds.iconTextButton(image='addClip.png',
                                                               command=partial(self.get_selection_and_set_text_field,
                                                                               text_field=self.range_vertices_right_list))

        self.back_vtx_right = cmds.textFieldGrp(label='Back vertex: ', enable=True)
        self.back_vtx_right_button = cmds.iconTextButton(image='addClip.png',
                                                         command=partial(self.get_last_selection_and_set_text_field,
                                                                         text_field=self.back_vtx_right))

        # Skin inputs
        separator05 = cmds.separator(height=5)

        self.create_skin_right_bool = cmds.checkBoxGrp(label='Create skin', value1=True,
                                                       onCommand=self.set_create_skin_right_enable,
                                                       offCommand=self.set_create_skin_right_enable)

        self.pupil_vertices_right_list = cmds.textFieldGrp(label='Pupil vertices: ', enable=True)
        self.pupil_vertices_right_button = cmds.iconTextButton(image='addClip.png',
                                                               command=partial(self.get_selection_and_set_text_field,
                                                                               text_field=self.pupil_vertices_right_list))

        self.iris_vertices_right_list = cmds.textFieldGrp(label='Iris vertices: ', enable=True)
        self.iris_vertices_right_button = cmds.iconTextButton(image='addClip.png',
                                                              command=partial(self.get_selection_and_set_text_field,
                                                                              text_field=self.iris_vertices_right_list))

        # --------------------------------------------------------------------------------------------------------------
        cmds.formLayout(self.main_layout, edit=True,

                        attachForm=[(self.name, 'top', 20),
                                    (separator01, 'left', 5), (separator01, 'right', 5),
                                    (separator02, 'left', 5), (separator02, 'right', 5),
                                    (separator03, 'left', 5), (separator03, 'right', 5),
                                    (separator04, 'left', 5), (separator04, 'right', 5),
                                    (separator05, 'left', 5), (separator05, 'right', 5),
                                    (vertices_list_inputs_text, 'left', 5), (vertices_list_inputs_text, 'right', 5),
                                    (left_text, 'left', 5), (left_text, 'right', 5),
                                    (right_text, 'left', 5), (right_text, 'right', 5)],

                        attachControl=[(self.base, 'top', 5, self.name),
                                       (self.hook, 'top', 5, self.base),
                                       (separator01, 'top', 5, self.hook),
                                       (vertices_list_inputs_text, 'top', 5, separator01),
                                       (separator02, 'top', 5, vertices_list_inputs_text),
                                       (left_text, 'top', 5, separator02),
                                       (self.mid_loop_vtx_left_list, 'top', 5, left_text),
                                       (self.mid_loop_vtx_left_button, 'top', 5, left_text),
                                       (self.mid_loop_vtx_left_button, 'left', 5, self.mid_loop_vtx_left_list),
                                       (self.range_vertices_left_list, 'top', 5, self.mid_loop_vtx_left_list),
                                       (self.range_vertices_left_button, 'top', 5, self.mid_loop_vtx_left_list),
                                       (self.range_vertices_left_button, 'left', 5, self.range_vertices_left_list),
                                       (self.back_vtx_left, 'top', 5, self.range_vertices_left_list),
                                       (self.back_vtx_left_button, 'top', 5, self.range_vertices_left_list),
                                       (self.back_vtx_left_button, 'left', 5, self.back_vtx_left),
                                       (separator03, 'top', 5, self.back_vtx_left),
                                       (self.create_skin_left_bool, 'top', 5, separator03),
                                       (self.pupil_vertices_left_list, 'top', 5, self.create_skin_left_bool),
                                       (self.pupil_vertices_left_button, 'top', 5, self.create_skin_left_bool),
                                       (self.pupil_vertices_left_button, 'left', 5, self.pupil_vertices_left_list),
                                       (self.iris_vertices_left_list, 'top', 5, self.pupil_vertices_left_list),
                                       (self.iris_vertices_left_button, 'top', 5, self.pupil_vertices_left_list),
                                       (self.iris_vertices_left_button, 'left', 5, self.iris_vertices_left_list),
                                       (separator04, 'top', 5, self.iris_vertices_left_button),
                                       (right_text, 'top', 5, separator04),
                                       (self.mid_loop_vtx_right_list, 'top', 5, right_text),
                                       (self.mid_loop_vtx_right_button, 'top', 5, right_text),
                                       (self.mid_loop_vtx_right_button, 'left', 5, self.mid_loop_vtx_right_list),
                                       (self.range_vertices_right_list, 'top', 5, self.mid_loop_vtx_right_list),
                                       (self.range_vertices_right_button, 'top', 5, self.mid_loop_vtx_right_list),
                                       (self.range_vertices_right_button, 'left', 5, self.range_vertices_right_list),
                                       (self.back_vtx_right, 'top', 5, self.range_vertices_right_list),
                                       (self.back_vtx_right_button, 'top', 5, self.range_vertices_right_list),
                                       (self.back_vtx_right_button, 'left', 5, self.back_vtx_right),
                                       (separator05, 'top', 5, self.back_vtx_right),
                                       (self.create_skin_right_bool, 'top', 5, separator05),
                                       (self.pupil_vertices_right_list, 'top', 5, self.create_skin_right_bool),
                                       (self.pupil_vertices_right_button, 'top', 5, self.create_skin_right_bool),
                                       (self.pupil_vertices_right_button, 'left', 5, self.pupil_vertices_right_list),
                                       (self.iris_vertices_right_list, 'top', 5, self.pupil_vertices_right_list),
                                       (self.iris_vertices_right_button, 'top', 5, self.pupil_vertices_right_list),
                                       (self.iris_vertices_right_button, 'left', 5, self.iris_vertices_right_list)]
                        )

    def apply_command(self, *args):
        """
        Apply button command
        """
        descriptor = cmds.textFieldGrp(self.name, query=True, text=True)

        base = cmds.textFieldGrp(self.base, query=True, text=True)

        hook = cmds.textFieldGrp(self.hook, query=True, text=True)

        mid_loop_vtx_left_list = cmds.textFieldGrp(self.mid_loop_vtx_left_list, query=True, text=True)
        range_vertices_left_list = cmds.textFieldGrp(self.range_vertices_left_list, query=True, text=True)
        back_vtx_left = cmds.textFieldGrp(self.back_vtx_left, query=True, text=True)

        create_skin_left_bool = cmds.checkBoxGrp(self.create_skin_left_bool, query=True, value1=True)
        pupil_vertices_left_list = cmds.textFieldGrp(self.pupil_vertices_left_list, query=True, text=True)
        iris_vertices_left_list = cmds.textFieldGrp(self.iris_vertices_left_list, query=True, text=True)

        mid_loop_vtx_right_list = cmds.textFieldGrp(self.mid_loop_vtx_right_list, query=True, text=True)
        range_vertices_right_list = cmds.textFieldGrp(self.range_vertices_right_list, query=True, text=True)
        back_vtx_right = cmds.textFieldGrp(self.back_vtx_right, query=True, text=True)

        create_skin_right_bool = cmds.checkBoxGrp(self.create_skin_right_bool, query=True, value1=True)
        pupil_vertices_right_list = cmds.textFieldGrp(self.pupil_vertices_right_list, query=True, text=True)
        iris_vertices_right_list = cmds.textFieldGrp(self.iris_vertices_right_list, query=True, text=True)

        eyes_module = eyes.Eyes(descriptor=descriptor)

        eyes_module.create_guides(base_default_value=base,
                                  hook_default_value=hook,
                                  mid_loop_vertices_left_value=mid_loop_vtx_left_list,
                                  range_vertices_left_value=range_vertices_left_list,
                                  back_vtx_left_value=back_vtx_left,
                                  create_skin_bool_default_left_value=create_skin_left_bool,
                                  pupil_vertices_left_value=pupil_vertices_left_list,
                                  iris_vertices_left_value=iris_vertices_left_list,
                                  mid_loop_vertices_right_value=mid_loop_vtx_right_list,
                                  range_vertices_right_value=range_vertices_right_list,
                                  back_vtx_right_value=back_vtx_right,
                                  create_skin_bool_default_right_value=create_skin_right_bool,
                                  pupil_vertices_right_value=pupil_vertices_right_list,
                                  iris_vertices_right_value=iris_vertices_right_list)

    def set_create_skin_left_enable(self, *args):
        """
        Set the create skin textFields on or off
        """
        if cmds.checkBoxGrp(self.create_skin_left_bool, query=True, enable=True, value1=True):
            cmds.textFieldGrp(self.iris_vertices_left_list, edit=True, enable=True)
            cmds.iconTextButton(self.iris_vertices_left_button, edit=True, enable=True)
            cmds.textFieldGrp(self.pupil_vertices_left_list, edit=True, enable=True)
            cmds.iconTextButton(self.pupil_vertices_left_button, edit=True, enable=True)
        else:
            cmds.textFieldGrp(self.iris_vertices_left_list, edit=True, enable=False)
            cmds.iconTextButton(self.iris_vertices_left_button, edit=True, enable=False)
            cmds.textFieldGrp(self.pupil_vertices_left_list, edit=True, enable=False)
            cmds.iconTextButton(self.pupil_vertices_left_button, edit=True, enable=False)

    def set_create_skin_right_enable(self, *args):
        """
        Set the create skin textFields on or off
        """
        if cmds.checkBoxGrp(self.create_skin_right_bool, query=True, enable=True, value1=True):
            cmds.textFieldGrp(self.iris_vertices_right_list, edit=True, enable=True)
            cmds.iconTextButton(self.iris_vertices_right_button, edit=True, enable=True)
            cmds.textFieldGrp(self.pupil_vertices_right_list, edit=True, enable=True)
            cmds.iconTextButton(self.pupil_vertices_right_button, edit=True, enable=True)
        else:
            cmds.textFieldGrp(self.iris_vertices_right_list, edit=True, enable=False)
            cmds.iconTextButton(self.iris_vertices_right_button, edit=True, enable=False)
            cmds.textFieldGrp(self.pupil_vertices_right_list, edit=True, enable=False)
            cmds.iconTextButton(self.pupil_vertices_right_button, edit=True, enable=False)


class EyeWindow(window_lib.Helper):
    """
    Create the eye window

    Args:
        title (str): title of the window
        size (list): width and height
    """

    def __init__(self, *args):
        """
        Initializes an instance of EyeWindow

        Args:
            title (str): title of the window
            size (list): width and height
        """
        super(EyeWindow, self).__init__(
            title='Eye Guide Options', size=(450, 400))

        # Name
        self.name = cmds.textFieldGrp(label='Name: ', text='eye')

        # Side
        self.side = cmds.optionMenu(label='Side')
        cmds.menuItem(self.side, label='Left')
        cmds.menuItem(self.side, label='Center')
        cmds.menuItem(self.side, label='Right')
        cmds.optionMenu(self.side, edit=True, value='Left')

        self.connect_to_opposite = cmds.checkBoxGrp(label='Connect to opposite: ', value1=False)

        # hook and base
        self.base = cmds.textFieldGrp(
            label='Hook: ', text='rootOutputs_c_grp.center_c_ctr')

        self.hook = cmds.textFieldGrp(
            label='Base: ', text='neckOutputs_c_grp.head_c_ctr')
        
        self.follow = cmds.textFieldGrp(
            label='Follow: ', text='eyesOutputs_c_grp.eyesLookAt_c_ctr')

        # Vertices lists
        separator01 = cmds.separator(height=5)

        vertices_list_inputs_text = cmds.text(label=' Vertices list inputs',
                                              backgroundColor=(0.4, 0.4, 0.4), height=20, align='left')

        self.mid_loop_vtx_list = cmds.textFieldGrp(label='Mid loop vertices: ', enable=True)
        self.mid_loop_vtx_button = cmds.iconTextButton(image='addClip.png',
                                                       command=partial(self.get_selection_and_set_text_field,
                                                                       text_field=self.mid_loop_vtx_list))

        self.range_vertices_list = cmds.textFieldGrp(label='Range vertices: ', enable=True)
        self.range_vertices_button = cmds.iconTextButton(image='addClip.png',
                                                         command=partial(self.get_selection_and_set_text_field,
                                                                         text_field=self.range_vertices_list))

        self.back_vtx = cmds.textFieldGrp(label='Back vertex: ', enable=True)
        self.back_vtx_button = cmds.iconTextButton(image='addClip.png',
                                                   command=partial(self.get_last_selection_and_set_text_field,
                                                                   text_field=self.back_vtx))

        # Skin inputs
        separator02 = cmds.separator(height=5)

        self.create_skin_bool = cmds.checkBoxGrp(label='Create skin', value1=True,
                                                 onCommand=self.set_create_skin_enable,
                                                 offCommand=self.set_create_skin_enable)

        self.pupil_vertices_list = cmds.textFieldGrp(label='Pupil vertices: ', enable=True)
        self.pupil_vertices_button = cmds.iconTextButton(image='addClip.png',
                                                         command=partial(self.get_selection_and_set_text_field,
                                                                         text_field=self.pupil_vertices_list))

        self.iris_vertices_list = cmds.textFieldGrp(label='Iris vertices: ', enable=True)
        self.iris_vertices_button = cmds.iconTextButton(image='addClip.png',
                                                        command=partial(self.get_selection_and_set_text_field,
                                                                        text_field=self.iris_vertices_list))

        # --------------------------------------------------------------------------------------------------------------
        cmds.formLayout(self.main_layout, edit=True,

                        attachForm=[(self.name, 'top', 20),
                                    (self.side, 'left', 115),
                                    (separator01, 'left', 5), (separator01, 'right', 5),
                                    (separator02, 'left', 5), (separator02, 'right', 5),
                                    (vertices_list_inputs_text, 'left', 5), (vertices_list_inputs_text, 'right', 5)],

                        attachControl=[(self.side, 'top', 5, self.name),
                                       (self.connect_to_opposite, 'top', 7, self.name),
                                       (self.connect_to_opposite, 'left', 4, self.side),
                                       (self.base, 'top', 5, self.connect_to_opposite),
                                       (self.hook, 'top', 5, self.base),
                                       (self.follow, 'top', 5, self.hook),
                                       (separator01, 'top', 5, self.follow),
                                       (vertices_list_inputs_text, 'top', 5, separator01),
                                       (self.mid_loop_vtx_list, 'top', 5, vertices_list_inputs_text),
                                       (self.mid_loop_vtx_button, 'top', 5, vertices_list_inputs_text),
                                       (self.mid_loop_vtx_button, 'left', 5, self.mid_loop_vtx_list),
                                       (self.range_vertices_list, 'top', 5, self.mid_loop_vtx_list),
                                       (self.range_vertices_button, 'top', 5, self.mid_loop_vtx_list),
                                       (self.range_vertices_button, 'left', 5, self.range_vertices_list),
                                       (self.back_vtx, 'top', 5, self.range_vertices_list),
                                       (self.back_vtx_button, 'top', 5, self.range_vertices_list),
                                       (self.back_vtx_button, 'left', 5, self.back_vtx),
                                       (separator02, 'top', 5, self.back_vtx),
                                       (self.create_skin_bool, 'top', 5, separator02),
                                       (self.pupil_vertices_list, 'top', 5, self.create_skin_bool),
                                       (self.pupil_vertices_button, 'top', 5, self.create_skin_bool),
                                       (self.pupil_vertices_button, 'left', 5, self.pupil_vertices_list),
                                       (self.iris_vertices_list, 'top', 5, self.pupil_vertices_list),
                                       (self.iris_vertices_button, 'top', 5, self.pupil_vertices_list),
                                       (self.iris_vertices_button, 'left', 5, self.iris_vertices_list)]
                        )

    def apply_command(self, *args):
        """
        Apply button command
        """
        descriptor = cmds.textFieldGrp(self.name, query=True, text=True)

        side = cmds.optionMenu(self.side, query=True, value=True)
        if side == 'Left':
            side = 'l'
        if side == 'Center':
            side = 'c'
        if side == 'Right':
            side = 'r'

        connect_to_opposite = cmds.checkBoxGrp(self.connect_to_opposite, query=True, value1=True)

        base = cmds.textFieldGrp(self.base, query=True, text=True)

        hook = cmds.textFieldGrp(self.hook, query=True, text=True)

        mid_loop_vtx_list = cmds.textFieldGrp(self.mid_loop_vtx_list, query=True, text=True)
        range_vertices_list = cmds.textFieldGrp(self.range_vertices_list, query=True, text=True)
        back_vtx = cmds.textFieldGrp(self.back_vtx, query=True, text=True)

        create_skin_bool = cmds.checkBoxGrp(self.create_skin_bool, query=True, value1=True)
        pupil_vertices_list = cmds.textFieldGrp(self.pupil_vertices_list, query=True, text=True)
        iris_vertices_list = cmds.textFieldGrp(self.iris_vertices_list, query=True, text=True)

        eye_module = eye.Eye(descriptor=descriptor, side=side)

        eye_module.create_guides(connect_to_opposite_value=connect_to_opposite,
                                 base_default_value=base,
                                 hook_default_value=hook,
                                 mid_loop_vertices_value=mid_loop_vtx_list,
                                 range_vertices_value=range_vertices_list,
                                 back_vtx_value=back_vtx,
                                 create_skin_bool_default_value=create_skin_bool,
                                 iris_vertices_value=iris_vertices_list,
                                 pupil_vertices_value=pupil_vertices_list)

    def set_create_skin_enable(self, *args):
        """
        Set the create skin textFields on or off
        """
        if cmds.checkBoxGrp(self.create_skin_bool, query=True, enable=True, value1=True):
            cmds.textFieldGrp(self.iris_vertices_list, edit=True, enable=True)
            cmds.iconTextButton(self.iris_vertices_button, edit=True, enable=True)
            cmds.textFieldGrp(self.pupil_vertices_list, edit=True, enable=True)
            cmds.iconTextButton(self.pupil_vertices_button, edit=True, enable=True)
        else:
            cmds.textFieldGrp(self.iris_vertices_list, edit=True, enable=False)
            cmds.iconTextButton(self.iris_vertices_button, edit=True, enable=False)
            cmds.textFieldGrp(self.pupil_vertices_list, edit=True, enable=False)
            cmds.iconTextButton(self.pupil_vertices_button, edit=True, enable=False)


class EarWindow(window_lib.Helper):
    """
    Create the ear window

    Args:
        title (str): title of the window
        size (list): width and height
    """

    def __init__(self, *args):
        """
        Initializes an instance of EarWindow

        Args:
            title (str): title of the window
            size (list): width and height
        """
        super(EarWindow, self).__init__(
            title='Ear Guide Options', size=(450, 190))

        # Name
        self.name = cmds.textFieldGrp(label='Name: ', text='ear')

        # Side
        self.side = cmds.optionMenu(label='Side')
        cmds.menuItem(self.side, label='Left')
        cmds.menuItem(self.side, label='Center')
        cmds.menuItem(self.side, label='Right')
        cmds.optionMenu(self.side, edit=True, value='Left')

        self.connect_to_opposite = cmds.checkBoxGrp(
            label='Connect to opposite: ', value1=False)

        # hook and base
        self.base = cmds.textFieldGrp(
            label='Hook: ', text='rootOutputs_c_grp.center_c_ctr')

        self.hook = cmds.textFieldGrp(
            label='Base: ', text='neckOutputs_c_grp.head_c_ctr')

        # --------------------------------------------------------------------------------------------------------------
        cmds.formLayout(self.main_layout, edit=True,

                        attachForm=[(self.name, 'top', 20),
                                    (self.side, 'left', 115)],

                        attachControl=[(self.side, 'top', 5, self.name),
                                       (self.connect_to_opposite,
                                        'top', 5, self.side),
                                       (self.base, 'top', 5,
                                        self.connect_to_opposite),
                                       (self.hook, 'top', 5, self.base)]
                        )

    def apply_command(self, *args):
        """
        Apply button command
        """
        descriptor = cmds.textFieldGrp(self.name, query=True, text=True)

        side = cmds.optionMenu(self.side, query=True, value=True)
        if side == 'Left':
            side = 'l'
        if side == 'Center':
            side = 'c'
        if side == 'Right':
            side = 'r'

        connect_to_opposite = cmds.checkBoxGrp(
            self.connect_to_opposite, query=True, value1=True)

        base = cmds.textFieldGrp(self.base, query=True, text=True)

        hook = cmds.textFieldGrp(self.hook, query=True, text=True)

        ear_module = ear.Ear(descriptor=descriptor, side=side)

        ear_module.create_guides(connect_to_opposite_value=connect_to_opposite,
                                 base_default_value=base,
                                 hook_default_value=hook)


class CheekWindow(window_lib.Helper):
    """
    Create the cheek window

    Args:
        title (str): title of the window
        size (list): width and height
    """
    def __init__(self, *args):
        """
        Initializes an instance of CheekWindow

        Args:
            title (str): title of the window
            size (list): width and height
        """
        super(CheekWindow, self).__init__(title='Cheek Guide Options', size=(450, 190))

        # Name
        self.name = cmds.textFieldGrp(label='Name: ', text='cheek')

        # Side
        self.side = cmds.optionMenu(label='Side')
        cmds.menuItem(self.side, label='Left')
        cmds.menuItem(self.side, label='Center')
        cmds.menuItem(self.side, label='Right')
        cmds.optionMenu(self.side, edit=True, value='Left')

        self.connect_to_opposite = cmds.checkBoxGrp(label='Connect to opposite: ', value1=False)

        # hook and base
        self.base = cmds.textFieldGrp(label='Hook: ', text='rootOutputs_c_grp.center_c_ctr')

        self.hook = cmds.textFieldGrp(label='Base: ', text='neckOutputs_c_grp.head_c_ctr')

        # --------------------------------------------------------------------------------------------------------------
        cmds.formLayout(self.main_layout, edit=True,

                        attachForm=[(self.name, 'top', 20),
                                    (self.side, 'left', 115)],

                        attachControl=[(self.side, 'top', 5, self.name),
                                       (self.connect_to_opposite, 'top', 5, self.side),
                                       (self.base, 'top', 5, self.connect_to_opposite),
                                       (self.hook, 'top', 5, self.base)]
                        )


    def apply_command(self, *args):
        """
        Apply button command
        """
        descriptor = cmds.textFieldGrp(self.name, query=True, text=True)

        side = cmds.optionMenu(self.side, query=True, value=True)
        if side == 'Left':
            side = 'l'
        if side == 'Center':
            side = 'c'
        if side == 'Right':
            side = 'r'

        connect_to_opposite = cmds.checkBoxGrp(self.connect_to_opposite, query=True, value1=True)

        base = cmds.textFieldGrp(self.base, query=True, text=True)

        hook = cmds.textFieldGrp(self.hook, query=True, text=True)

        cheek_module = cheek.Cheek(descriptor=descriptor, side=side)

        cheek_module.create_guides(connect_to_opposite_value=connect_to_opposite,
                                 base_default_value=base,
                                 hook_default_value=hook)

