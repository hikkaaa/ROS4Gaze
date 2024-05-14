import numpy as np
import shutil

N_FRAMES = 50
STILL_FRAMES = 10000

YAW_ANGLE = 20
PITCH_ANGLE = 30
N_DOF = 6


def create_movement(angles, n_frames=N_FRAMES, symmetrical=True):
    """
    Create symmetrical movements
    Returns a vector of n_frames long
    """
    if symmetrical:
        output = [x*(angles/(n_frames/2)) for x in range(int(n_frames/2))]
        return output + output[::-1]
    else:
        return [x*(angles/n_frames) for x in range(int(n_frames))]



def construct_bvh(output_name):
    # Create a copy of the existing file
    output_filename = output_name[:-4] + 'v1.bvh'
    shutil.copyfile(output_name, output_filename)
    # Open the original file in read mode and read its content up to line 19
    with open(output_filename, 'r') as input_file:
        lines = input_file.readlines()[:14]
    # Update Frame numbers
    lines[-2] = f'Frames: {str(N_FRAMES + STILL_FRAMES)}\n'
    # Open the original file in write mode to truncate it
    with open(output_filename, 'w') as input_file:
        input_file.writelines(lines)

    move_matrix = np.ones((N_FRAMES, N_DOF))
    yaw = create_movement(YAW_ANGLE, symmetrical=False)
    pitch = create_movement(PITCH_ANGLE, symmetrical=False)
    for col in range(len(move_matrix.T)):
        if col in range(4):
            move_matrix.T[col] *= 0
        else:
            if col == len(move_matrix.T)-2:
                move_matrix.T[col] *= yaw
            if col == len(move_matrix.T)-1:
                move_matrix.T[col] *= pitch

    still_matrix = np.array([move_matrix[-1]] * STILL_FRAMES)
    try:
        with open(output_filename, 'a') as output_file:
            np.savetxt(output_file, move_matrix, delimiter=' ', fmt='%f')
            np.savetxt(output_file, still_matrix, delimiter=' ', fmt='%f')
        print(f"NumPy matrix has been written to {output_filename}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    construct_bvh('gaze.bvh')