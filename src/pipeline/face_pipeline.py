import dlib 
import numpy as np 
import face_recognition_models
from sklearn.svm import SVC
import streamlit as st
from src.database.db import get_all_students

@st.cache_resource
def load_dlib_models():
    detector = dlib.get_frontal_face_detector()
    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )
    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )
    
    return detector, sp, facerec


def get_face_embeddings(image_np):
    detector, sp, facerec = load_dlib_models()
    # Increase upsampling to 2 to improve detection of new/unclear faces
    faces = detector(image_np, 2)
    encodings = []

    for face in faces:
        shape = sp(image_np, face)
        face_descriptor = facerec.compute_face_descriptor(image_np, shape, 1)
        encodings.append(np.array(face_descriptor))

    return encodings


@st.cache_resource
def get_trained_model():
    x = []
    y = []
    student_db = get_all_students()

    if not student_db:
        return None

    for student in student_db:
        embedding = student.get('face_embedding')
        if embedding:
            x.append(np.array(embedding))
            y.append(student.get('student_id'))

    if len(x) == 0:
        return None

    clf = SVC(kernel="linear", probability=True, class_weight="balanced")

    try:
        clf.fit(x, y)
    except ValueError as e:
        # Happens if only one class is present or data is invalid
        print(f"SVM training skipped: {e}")
        return {"clf": None, "x": x, "y": y}

    return {"clf": clf, "x": x, "y": y}


def train_classifier():
    st.cache_resource.clear()
    model_data = get_trained_model()
    return bool(model_data)


def predict_attendance(class_image_np):
    encodings = get_face_embeddings(class_image_np)
    detected_student = {}
    
    num_faces = len(encodings)
    if num_faces == 0:
        return {}, [], 0

    model_data = get_trained_model()
    if not model_data:
        # No students in DB, so no one can be "detected"
        return {}, [], num_faces

    clf = model_data['clf']
    x_train = model_data['x']
    y_train = model_data['y']

    all_students = sorted(list(set(y_train)))

    for encoding in encodings:
        predicted_id = None
        
        # If we have a trained classifier, use it
        if clf is not None and len(all_students) >= 2:
            predicted_id = int(clf.predict([encoding])[0])
        elif len(all_students) > 0:
            # Only one student in DB, they are the only possible prediction
            predicted_id = int(all_students[0])

        if predicted_id is not None:
            # Verify if the match is actually close enough (Resemblance Check)
            student_embedding = x_train[y_train.index(predicted_id)]
            best_match_score = np.linalg.norm(student_embedding - encoding)

            # Strict threshold for recognition (0.6)
            # If score > 0.6, it's a "New Face"
            if best_match_score <= 0.6:
                detected_student[predicted_id] = True

    return detected_student, all_students, num_faces