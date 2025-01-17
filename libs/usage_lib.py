# Imports
import inspect


# Usages
inputs = 'inputs'
outputs = 'outputs'
controls = 'controls'
skeleton = 'skeleton'
logic = 'logic'

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
prebind = 'prebind'

# Constraint usages
parent_constraint = 'pacns'
orient_constraint = 'orcns'
point_constraint = 'pocns'
scale_constraint = 'sccns'
aim_constraint = 'aicns'
pole_vector_constraint = 'pvcns'
constraint_valid_usages = [parent_constraint, orient_constraint, point_constraint,
                           scale_constraint, aim_constraint, pole_vector_constraint]

geometry = 'geo'
trigger = 'trg'
driver = 'driver'
macro = 'macro'
snap = 'snap'

# Deformers
skin_cluster = 'skin'
blend_shape = 'bs'
lattice_ffd = 'ffd'
squash = 'sq'
bend = 'bend'
twist = 'twist'

corrective = 'crr'
animation_curve = 'acrv'

multiply = 'mult'
divide = 'div'
add = 'add'
sub = 'sub'
condition = 'cond'
plus_minus_Average = 'pma'
angle_between = 'ab'
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
poly_cube = 'pc'
uvpin = 'uvp'
curve_info = 'cinfo'
norm = 'norm'
blend_color = 'bc'
ik_handle = 'ikh'
ik_spline = 'iks'
power = 'pow'
square_root = 'sqrt'
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
component_match = 'cmatch'
closest_point_on_mesh = 'cpom'
closest_point_on_surface = 'cpos'

test = 'test'
temp = 'temp'

# Valid usages
def get_all_usages():
    return [v for k, v in globals().items() if isinstance(v, str) and not k.startswith('_')]

valid_usages = get_all_usages()

def get_usage_capitalize(usage):
    """
    Get the usage capitalized

    Args:
        usage (str): usage to capitalize

    Returns:
        str: usage capitalized
    """
    return '{}{}'.format(usage[0].upper(), usage[1:])
