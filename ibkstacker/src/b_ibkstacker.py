#######################################################################################################################

__author__ = "Boris Martinez Castillo"
__version__ = "1.0.1"
__maintainer__ = "Boris Martinez Castillo"
__email__ = "boris.vfx@outlook.com"

########################################################################################################################

#IMPORTS

import nuke
import nukescripts


def create_ibk_colour():

    ibk_colour = nuke.createNode("IBKColourV3")
    return ibk_colour


def create_ibk_gizmo():

    ibk_gizmo = nuke.createNode("IBKGizmoV3")
    return ibk_gizmo
    
    
def create_merge_with_roto(input_node):

    merge = nuke.createNode("Merge2")
    clamp = nuke.nodes.Clamp()
    roto = nuke.nodes.Roto()

    input_node_position_x = input_node.xpos()
    input_node_position_y = input_node.ypos()

    merge.setYpos(input_node_position_y + 25)
    merge.setXpos(input_node_position_x)

    merge_position_x = merge.xpos()
    merge_position_y = merge.ypos()

    clamp.setYpos(merge_position_y)
    clamp.setXpos(merge_position_x + 150)

    clamp_position_x = clamp.xpos()
    clamp_position_y = clamp.ypos()
        
    roto.setYpos(clamp_position_y)
    roto.setXpos(clamp_position_x + 150) 

    merge.setInput(1,clamp)
    merge.setInput(0,input_node)
        
    clamp.setInput(0,roto)
    clamp['MinClampTo_enable'].setValue(True)
    clamp['MaxClampTo_enable'].setValue(True)
    clamp['maximum'].setValue(0)
    
    
def exponential_multi(master,max):

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
    
    
def stack_ibk(_max,_bool):

    #CONSTANTS

    MAX = _max

    MULTIVALUE = 0
    
    #VALIDATION
    
    try:
        MASTER_IBK = nuke.selectedNode().name()
        M_IBK_NAME = str(MASTER_IBK)
    except:
        nuke.message("Please select an IBKColourV3, Dude")
        
    if nuke.selectedNode().Class() != "IBKColourV3":
        nuke.message("Please select an IBKColourV3, dude")
        return None
    else:
        
        if _bool:
            input_node = MASTER_IBK
            create_merge_with_roto(nuke.toNode(input_node))
            loop(MASTER_IBK,M_IBK_NAME,MAX)
        else:
            loop(MASTER_IBK,M_IBK_NAME,MAX)
    

def loop(_input_node,_input_node_name,_max):
    
    
    #LOOPING UNTIL EXPONENTIAL LEVEL IS REACHED
    
    exponential_multi(_input_node,_max)

    #CREATING AND HOOKING UP IBK GIZMO
    
    target = nuke.selectedNode()
    dep_node = nuke.dependencies(nuke.toNode(_input_node_name))
    topnode_node = nuke.toNode(dep_node[0].name())
    
    screen_color = nuke.toNode(_input_node_name)['screen_type'].value()

    ibk_gizmo = create_ibk_gizmo()
    expression = "C-{}".format(screen_color)
    ibk_gizmo['st'].setValue(expression)
    ibk_gizmo.setInput(0, topnode_node)
    ibk_gizmo.setInput(1, target)
    ibk_gizmo.setInput(2, None)
    #ibk_gizmo.setXpos(nuke.toNode(_input_node_name).xpos() - 250)
    
    return

  
class StackPanel(nukescripts.PythonPanel):
   def __init__(self):
        nukescripts.PythonPanel.__init__(self,"b_ibkstacker")
        
        # CREATE KNOBS
        
        self.limit = nuke.Enumeration_Knob("limit", "ibk colour stack recursion limit", ["1","2","4","8","16","32","64","128","256","512"])
        self.limit.clearFlag(nuke.STARTLINE)
        self.checker = nuke.Boolean_Knob("add corrective roto")
    
        self.author = nuke.Text_Knob("written by Boris Martinez")
        
        # ADD KNOBS

        for i in (self.limit,self.checker,self.author):
            self.addKnob(i)


def main_function():
        
    context= StackPanel()

    if not context.showModalDialog():
        print "script aborted"
        return
    else:
        max_value = int(context.limit.value())
        checker_value = context.checker.value()
        print max_value
        stack_ibk(max_value,checker_value)
        

if __name__ == "__main__":
    main_function()





