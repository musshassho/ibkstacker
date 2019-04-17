#######################################################################################################################

__author__ = "Boris Martinez Castillo"
__version__ = "1.0.1"
__maintainer__ = "Boris Martinez Castillo"
__email__ = "boris.vfx@outlook.com"

########################################################################################################################

# IMPORTS

import nuke
import nukescripts


def create_ibk_colour():
    ibk_colour = nuke.createNode("IBKColourV3")
    return ibk_colour


def create_ibk_gizmo():
    ibk_gizmo = nuke.createNode("IBKGizmoV3")
    return ibk_gizmo


def exponential_multi(master, max):
    MULTIVALUE = 0

    while MULTIVALUE < max:

        new = create_ibk_colour()

        screen_type_expression = "{}{}{}".format(master, ".", "screen_type")
        size_expression = "{}{}{}".format(master, ".", "Size")
        off_expression = "{}{}{}".format(master, ".", "off")
        mult_expression = "{}{}{}".format(master, ".", "mult")
        erode_expression = "{}{}{}".format(master, ".", "erode")
        multi_expression = "{}{}{}".format(master, ".", "multi")

        size_value = size_expression

        print "MULTI INI: ", MULTIVALUE

        if MULTIVALUE == 0:
            MULTIVALUE += 1
            print MULTIVALUE

        elif MULTIVALUE > 0:
            MULTIVALUE *= 2
            print MULTIVALUE

        new["screen_type"].setExpression(screen_type_expression)
        new["Size"].setExpression(size_expression)
        new["off"].setExpression(off_expression)
        new["mult"].setExpression(mult_expression)
        # new["erode"].setExpression(erode_expression)
        new["erode"].setValue(0)
        new["multi"].setValue(MULTIVALUE)


def stack_ibk(max):
    # CONSTANTS

    MAX = max
    MULTIVALUE = 0
    MASTER_IBK = nuke.thisNode().name()
    M_IBK_NAME = str(MASTER_IBK)

    # LOOPING UNTIL EXPONENTIAL LEVEL IS REACHED

    exponential_multi(MASTER_IBK, MAX)

    # CREATING AND HOOKING UP IBK GIZMO

    target = nuke.selectedNode()
    dep_node = nuke.dependencies(nuke.toNode(M_IBK_NAME))
    topnode_node = nuke.toNode(dep_node[0].name())

    ibk_gizmo = create_ibk_gizmo()
    ibk_gizmo.setInput(0, topnode_node)
    ibk_gizmo.setInput(1, target)
    ibk_gizmo.setInput(2, None)

    return


