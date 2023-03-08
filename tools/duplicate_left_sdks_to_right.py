from maya import cmds


"""
old solution, needs a clean up
"""


nodes_to_duplicate = cmds.ls(sl=True)
nodes_to_duplicate = [x for x in nodes_to_duplicate if len(x.split('_')) == 3]
nd_dict = {}
for nd in nodes_to_duplicate:
    desc, side, usage = nd.split('_')

    out_con = cmds.listConnections(nd, plugs=True, destination=True, source=False, skipConversionNodes=True)[:-1][0]
    out_con_in = cmds.listConnections(out_con, plugs=True, destination=False, source=True, skipConversionNodes=True)[0]
    in_con = cmds.listConnections(nd, plugs=True, destination=False, source=True, skipConversionNodes=True)[0]
    in_con_out = cmds.listConnections(in_con, plugs=True, destination=True, source=False, skipConversionNodes=True)
    in_con_out = [x for x in in_con_out if x.startswith(nd)][0]

    nd_dict[nd] = [in_con_out.replace('_l_', '_r_'), in_con.replace('_l_', '_r_'), out_con.replace('_l_', '_r_'),
                   out_con_in.replace('_l_', '_r_')]

    nd_right = cmds.rename(cmds.duplicate(nd)[0], '{}_r_{}'.format(desc, usage))

for nd in nodes_to_duplicate:
    nd_right = nd.replace('_l_', '_r_')
    cmds.connectAttr(nd_dict[nd][3], nd_dict[nd][2], f=True)
    cmds.connectAttr(nd_dict[nd][1], nd_dict[nd][0], f=True)
