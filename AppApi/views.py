from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import numpy as np
import cv2
import os
import cvlib as cv

import logging

from django.conf import settings
from django.db import IntegrityError
from django.http import JsonResponse
# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .forms import ImageUploadForm
from .models import UploadedImage, FaceDetected

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name='dispatch')
class UploadImage(View):
    @staticmethod
    def get(request, *args, **kwargs):
        return JsonResponse({'status': 'false', 'message': 'Not valid form'}, status=500)

    @staticmethod
    def post(request, *args, **kwargs):
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            uploaded_file = data["ImageFile"]

            obj_img_uploaded = UploadedImage(ImageFile=uploaded_file)
            try:
                obj_img_uploaded.save()
            except IntegrityError as e:
                logger.error(e)
                return JsonResponse({'status': 'false', 'message': 'Error saving file'}, status=500)

            model_path = getattr(settings, "MODEL_PATH", "")
            image_dir = getattr(settings, "MEDIA_ROOT", "")
            image_path = image_dir / obj_img_uploaded.ImageFile.name

            print(image_path)
            img = cv2.imread(str(image_path))
            model = load_model(model_path)
            classes = ['man', 'woman']

            face, confidence = cv.detect_face(img)
            img_label = "None"

            for idx, f in enumerate(face):
                # get corner points of face rectangle
                (startX, startY) = f[0], f[1]
                (endX, endY) = f[2], f[3]

                # draw rectangle over face
                cv2.rectangle(img, (startX, startY), (endX, endY), (0, 255, 0), 2)
                cv2.imwrite(str(image_path) + "1.jpg", img)

                # crop the detected face region
                face_crop = np.copy(img[startY:endY, startX:endX])
                if (face_crop.shape[0]) < 10 or (face_crop.shape[1]) < 10:
                    continue

                # preprocessing for gender detection model
                face_crop = cv2.resize(face_crop, (96, 96))
                face_crop = face_crop.astype("float") / 255.0
                face_crop = img_to_array(face_crop)
                face_crop = np.expand_dims(face_crop, axis=0)

                conf = model.predict(face_crop)[0]
                idx = np.argmax(conf)
                img_label = classes[idx]

                obj_face_detected = FaceDetected(Gender=img_label, StartX=startX, StartY=startY,
                                                 EndX=endX, EndY=endY, Image=obj_img_uploaded)
                try:
                    obj_face_detected.save()
                except IntegrityError as e:
                    logger.error(e)

            return JsonResponse({'status': 'true', 'message': img_label})

        return JsonResponse({'status': 'false', 'message': 'Not valid form'}, status=500)