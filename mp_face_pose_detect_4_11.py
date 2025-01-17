# STEP 1: Import the necessary modules.
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import math
#from Misty_commands import Misty
import base64
import time
import json
import Experiment_code

# STEP 1B: viusalisation tools
# #@markdown We implemented some functions to visualize the face landmark detection results. <br/> Run the following cell to activate the functions.

from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np
import matplotlib.pyplot as plt
from Misty_commands import Misty
import datetime
from Hardcoded_experiment_code import head_position_left, IDP1, IPD2 # niet handig bestanden die elkaar importeren, .... gaat niet goed

def log_facepose(IDP1, IDP2, head_position_left, pitch, yaw):
    ct = datetime.datetime.now()
    file_name = "headpose_" + str(IDP1) + '_' + str(IDP2) + ".txt"
    f = open(file_name, 'a')
    f.write(str(head_position_left) + '\t' + str(pitch) + '\t' + str(yaw) +'\t' + str(ct) + '\t' + '\n')
    f.close()

def draw_landmarks_on_image(rgb_image, detection_result):
  face_landmarks_list = detection_result.face_landmarks
  annotated_image = np.copy(rgb_image)

  # Loop through the detected faces to visualize.
  for idx in range(len(face_landmarks_list)):
    face_landmarks = face_landmarks_list[idx]

    # Draw the face landmarks.
    face_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
    face_landmarks_proto.landmark.extend([
      landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in face_landmarks
    ])

    solutions.drawing_utils.draw_landmarks(
        image=annotated_image,
        landmark_list=face_landmarks_proto,
        connections=mp.solutions.face_mesh.FACEMESH_TESSELATION,
        landmark_drawing_spec=None,
        connection_drawing_spec=mp.solutions.drawing_styles
        .get_default_face_mesh_tesselation_style())
    solutions.drawing_utils.draw_landmarks(
        image=annotated_image,
        landmark_list=face_landmarks_proto,
        connections=mp.solutions.face_mesh.FACEMESH_CONTOURS,
        landmark_drawing_spec=None,
        connection_drawing_spec=mp.solutions.drawing_styles
        .get_default_face_mesh_contours_style())
    solutions.drawing_utils.draw_landmarks(
        image=annotated_image,
        landmark_list=face_landmarks_proto,
        connections=mp.solutions.face_mesh.FACEMESH_IRISES,
          landmark_drawing_spec=None,
          connection_drawing_spec=mp.solutions.drawing_styles
          .get_default_face_mesh_iris_connections_style())

  return annotated_image

def plot_face_blendshapes_bar_graph(face_blendshapes):
  # Extract the face blendshapes category names and scores.
  face_blendshapes_names = [face_blendshapes_category.category_name for face_blendshapes_category in face_blendshapes]
  face_blendshapes_scores = [face_blendshapes_category.score for face_blendshapes_category in face_blendshapes]
  # The blendshapes are ordered in decreasing score value.
  face_blendshapes_ranks = range(len(face_blendshapes_names))

  fig, ax = plt.subplots(figsize=(12, 12))
  bar = ax.barh(face_blendshapes_ranks, face_blendshapes_scores, label=[str(x) for x in face_blendshapes_ranks])
  ax.set_yticks(face_blendshapes_ranks, face_blendshapes_names)
  ax.invert_yaxis()

  # Label each bar with values
  for score, patch in zip(face_blendshapes_scores, bar.patches):
    plt.text(patch.get_x() + patch.get_width(), patch.get_y(), f"{score:.4f}", va="top")

  ax.set_xlabel('Score')
  ax.set_title("Face Blendshapes")
  plt.tight_layout()
  plt.show()

def FaceLandmarker():
    # STEP 2: Create an FaceLandmarker object.
    base_options = python.BaseOptions(model_asset_path='face_landmarker_v2_with_blendshapes.task')
    options = vision.FaceLandmarkerOptions(base_options=base_options,
                                           output_face_blendshapes=True,
                                           output_facial_transformation_matrixes=True,
                                           num_faces=1)
    detector = vision.FaceLandmarker.create_from_options(options)
    return detector

def getMistyImage(misty):
    result = misty.take_picture(base64 = True, fileName = "TempImage01", width = 800, height = 600, displayOnScreen = False, overwriteExisting = True)
    if (result.json()['status'] == "Success"):
        returnvalue = True
        result = misty.get_image(fileName = "TempImage01.jpg", base64 = True)
        image = result.json()['result']['base64']  # raw data with base64 encoding
        decoded_data = base64.b64decode(image)
        np_data = np.fromstring(decoded_data,np.uint8)
        img = cv2.imdecode(np_data,cv2.IMREAD_UNCHANGED)

    else:
        returnvalue = False
        img = None
    return returnvalue, img

def DetectHeadPose(cv_image, detector):
    image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv_image)
    print("I received the Image in the DetectHeadPose()")
    # STEP 4: Detect face landmarks from the input image.
    detection_result = detector.detect(image)
    return detection_result, image 

def rotation_matrix_to_angles(rotation_matrix):
    """
    Calculate Euler angles from rotation matrix.
    :param rotation_matrix: A 3*3 matrix with the following structure
    [Cosz*Cosy  Cosz*Siny*Sinx - Sinz*Cosx  Cosz*Siny*Cosx + Sinz*Sinx]
    [Sinz*Cosy  Sinz*Siny*Sinx + Sinz*Cosx  Sinz*Siny*Cosx - Cosz*Sinx]
    [  -Siny             CosySinx                   Cosy*Cosx         ]
    :return: Angles in degrees for each axis
    """
    x = math.atan2(rotation_matrix[2, 1], rotation_matrix[2, 2])
    y = math.atan2(-rotation_matrix[2, 0], math.sqrt(rotation_matrix[0, 0] ** 2 +
                                                     rotation_matrix[1, 0] ** 2))
    z = math.atan2(rotation_matrix[1, 0], rotation_matrix[0, 0])
    return np.array([x, y, z]) * 180. / math.pi         

def init_detector():
    detector = FaceLandmarker()        
    
    return detector    

def get_pitch_yaw(cv_image, detector):
    pitch = None
    yaw = None
    roll = None
    
    #print("I will try to import the image of Misty...")
    detection_result, image = DetectHeadPose(cv_image, detector)
    face_coordination_in_real_world = np.array([
            [285, 528, 200],
            [285, 371, 152],
            [197, 574, 128],
            [173, 425, 108],
            [360, 574, 128],
            [391, 425, 108]
            ], dtype=np.float64)

    h, w, channels = cv_image.shape
    face_coordination_in_image = []
    
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence = 0.5, min_tracking_confidence = 0.5)
    results = face_mesh.process(cv_image)
    #print("Got the result of the face_mesh processing")

    if results.multi_face_landmarks:
        print("Face landmarks detected!")
        for face_landmarks in results.multi_face_landmarks:
            print("I will start the for loop and go through each of the face_landmarks")
            for idx, lm in enumerate(face_landmarks.landmark):
                if idx in [1, 9, 57, 130, 287, 359]:
                    x, y = int(lm.x * w), int(lm.y * h)
                    face_coordination_in_image.append([x, y])
                    print("I appended the face_coordination_in_image")

            face_coordination_in_image = np.array(face_coordination_in_image,
                                                    dtype=np.float64)

            # The camera matrix
            focal_length = 1 * w
            cam_matrix = np.array([[focal_length, 0, w / 2],
                                    [0, focal_length, h / 2],
                                    [0, 0, 1]])

            # The Distance Matrix
            dist_matrix = np.zeros((4, 1), dtype=np.float64)

            # Use solvePnP function to get rotation vector
            success, rotation_vec, transition_vec = cv2.solvePnP(
                face_coordination_in_real_world, face_coordination_in_image,
                cam_matrix, dist_matrix)
            print("I have succesfully solved the matrix")

            # Use Rodrigues function to convert rotation vector to matrix
            rotation_matrix, jacobian = cv2.Rodrigues(rotation_vec)

            result = rotation_matrix_to_angles(rotation_matrix)
            
            #Print results of pitch and yaw
            pitch, yaw, roll = result[0], result[1], result[2]
            print(f'Pitch: {pitch:.2f} degrees, Yaw: {yaw:.2f} degrees')
                
<<<<<<< HEAD
                #Print results of pitch and yaw
                pitch, yaw, roll = result[0], result[1], result[2]
                print(f'Pitch: {pitch:.2f} degrees, Yaw: {yaw:.2f} degrees')
                    
                time_passed = int(time.time() - start_time)

                # Misty looks to the left participants --> 1 (participant 1)
                # Misty looks to the right participant --> 2 (participant 2)
                # Misty looks at neither --> 0
                if Experiment_code.head_moved_left == True:
                    misty_gaze_direction = 1
                elif Experiment_code.head_moved_right == True:
                    misty_gaze_direction = 2
                else:
                    misty_gaze_direction = 0

                #check if participant looks at Misty's eyes:
                if abs(int(result[0])) <= 7 and abs(int(result[1]))<= 7 :
                    participant_looks = True
                else:
                    participant_looks = False 

                #check if participant and misty look at eachother simultaneously: (left--> 1, right--> 2 , no eye contact made--> 0)
                if misty_gaze_direction == 1 and participant_looks == True:
                    eye_contact = 1
                elif misty_gaze_direction == 2 and participant_looks == True:
                    eye_contact = 2 
                else:
                    eye_contact = 0 
                           
                eyecontact_data = {
                    "time": time_passed,
                    "gaze_direction": eye_contact
                    }
                # will also add time since having started the code (in seconds)
                # Append the dictionary to the list
                headposition_data.append(eyecontact_data)

                with open("headposition_data.json", "w") as f:
                    json.dump(headposition_data, f)

                # Show picture
                for i, info in enumerate(zip(('pitch', 'yaw', 'roll'), result)):
                    k, v = info
                    text = f'{k}: {int(v)}'
                    cv2.putText(cv_image, text, (20, i*30 + 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 0, 200), 2)
    
    
            #cv2.imshow('Head Pose Angles', cv_image)
            # STEP 5: Process the detection result. In this case, visualize it.
            annotated_image = draw_landmarks_on_image(cv_image, detection_result)
            print("Displaying image window...")
            cv2.imshow(im_name, cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR))
            print("Image window displayed.")
            key = cv2.waitKey(100) 
            if key%256 == 27:
                # ESC pressed
                done = True
                break
        else:
            annotated_image = draw_landmarks_on_image(cv_image, detection_result)
            print("Displaying image window...")
            cv2.imshow(im_name, cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR))
            print("Image window displayed.")
            key = cv2.waitKey(100)
            key = cv2.waitKey(1)
            if key%256 == 27:
                # ESC pressed
                done = True
                break
    cv2.destroyWindow(im_name)
=======
            # Show picture
            for i, info in enumerate(zip(('pitch', 'yaw', 'roll'), result)):
                k, v = info
                text = f'{k}: {int(v)}'
                cv2.putText(cv_image, text, (20, i*30 + 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 0, 200), 2)


        #cv2.imshow('Head Pose Angles', cv_image)
        # # STEP 5: Process the detection result. In this case, visualize it.
        # cv_image = draw_landmarks_on_image(cv_image, detection_result)
        # print("Displaying image window...")
        # cv2.imshow(im_name, cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR))
        # print("Image window displayed.")
        log_facepose(IDP1, IPD2, head_position_left, pitch=pitch, yaw=yaw)
        # key = cv2.waitKey(100) 
        # if key%256 == 27:
        #     # ESC pressed
        #     done = True

        # cv2.destroyWindow(im_name)

>>>>>>> 23753f12dfefcdfc0fb74f13d5d3797076f540d0
    
if __name__ == "__main__":
    #misty = Misty(ip_address="192.168.0.100")
    print("Main was started")
    headposition_data = []
    start_time = time.time()
    try:
        get_pitch_yaw()
    except Exception as e:
        print(f"An error occurred: {e}")