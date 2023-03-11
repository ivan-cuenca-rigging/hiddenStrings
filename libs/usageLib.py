"""
Usages for all the nodes in maya
"""

# Control usages
control = 'ctr'
control_valid_usages = [control]

# Nurbs usages
nurbs = 'nurbs'
nurbs_valid_usages = [nurbs]

# Guide usages
guide = 'guide'
guide_valid_usages = [guide]

# Joint usages
skin_joint = 'skn'
joint = 'jnt'
nurbs_skin_joint = 'nskn'
curve_skin_joint = 'cskn'
skeleton_valid_usages = [skin_joint, joint, nurbs_skin_joint, curve_skin_joint]

# Constraint usages
parent_constraint = 'pacns'
orient_constraint = 'orcns'
point_constraint = 'pocns'
scale_constraint = 'sccns'
aim_constraint = 'aicns'
pole_vector_constraint = 'pvcns'
constraint_valid_usages = [parent_constraint, orient_constraint, point_constraint,
                           scale_constraint, aim_constraint, pole_vector_constraint]

# Deformers
skin_cluster = 'skin'
blend_shape = 'bs'

multiply = 'mult'
divide = 'div'
add = 'add'
sub = 'sub'
maximum = 'max'
minimum = 'min'
distance = 'dist'
curve = 'crv'
spline = 'spl'
locator = 'loc'
group = 'grp'
zero = 'zero'
set_driven_key = 'sdk'
reference = 'ref'
uvpin = 'uvp'
curve_info = 'cinfo'
norm = 'norm'
blend_color = 'bc'
ik_handle = 'ikh'
ik_spline = 'iks'
power = 'pow'
remap_value = 'rv'
reverse = 'rev'
clamp = 'clamp'
mult_matrix = 'multmat'
inverse_matrix = 'invmat'
decompose_matrix = 'decmat'
compose_matrix = 'cmat'
aim_matrix = 'aimmat'
blend_matrix = 'blendmat'
pick_matrix = 'pickmat'
point_matrix_mult = 'pmatmult'
quat_to_euler = 'qte'
point_on_curve_info = 'pocinfo'
nearest_point_on_curve = 'npoc'

test = 'test'

# Valid usages
valid_usages = [control,
                nurbs,
                guide,
                blend_shape,
                skin_joint, joint, nurbs_skin_joint, curve_skin_joint,
                parent_constraint, orient_constraint, point_constraint,
                scale_constraint, aim_constraint, pole_vector_constraint,
                multiply, divide, add, sub, maximum, minimum, distance, remap_value, reverse, clamp,
                curve, spline,
                uvpin,
                skin_cluster,
                locator,
                norm, blend_color, power,
                ik_spline, ik_handle,
                curve_info,
                mult_matrix, inverse_matrix, decompose_matrix, compose_matrix, blend_matrix, pick_matrix, aim_matrix,
                point_matrix_mult,
                quat_to_euler,
                point_on_curve_info, nearest_point_on_curve,
                group, zero, set_driven_key, reference]


def get_usage_capitalize(usage):
    return '{}{}'.format(usage[0].upper(), usage[1:])
