import face_recognition

# Load the image file
image = face_recognition.load_image_file("/test/Aaron_Eckhart.jpg")

# Find all the faces in the image
face_locations = face_recognition.face_locations(image)

# Get the age estimates for each face
for face_location in face_locations:
    top, right, bottom, left = face_location
    face_image = image[top:bottom, left:right]
    age_estimates = face_recognition.face_age_estimation(face_image)
    print(f"Estimated age: {age_estimates[0]} +/- {age_estimates[1]} years")