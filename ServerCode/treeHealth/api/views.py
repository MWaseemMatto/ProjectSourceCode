from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

# from rest_framework.views import APIView
from rest_framework import filters
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser, DjangoMultiPartParser
from rest_framework.views import APIView
from rest_framework.generics import (CreateAPIView)
from rest_framework.generics import (UpdateAPIView)
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework import viewsets
from shapely.geometry import Point, Polygon
from datetime import datetime

from treeHealth.models import (
    User,  MobileImages, #Images,
    HealthResults, Processes,
    Backup,
    Feedback
)
from treeHealth.api.serializers import (
    UserSerializer,
    MobileImagesSerializer,

    HealthResultsSerializer,
    ProcessSerializer,
    BackupSerializer,
    FeedbackSerializer
)

import imutils as imul
import numpy as np
from scipy.spatial import distance as dist
from imutils import perspective
import cv2
import math
from PIL import Image
from imutils import contours
from django.db.models import Max, Q


# ################### User Functions and Classes #############
# list of all users in the DB
@api_view(['GET', ])
def api_users_view(request, ):
    try:
        users = User.objects.all()
        # users_name = User.objects.get(name = name)

    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


# Get particular user
@api_view(['GET', ])
def api_user_view(request, aid):
    try:
        user = User.objects.get(android_id=aid)
        # users_name = User.objects.get(name = name)

    except User.DoesNotExist:
        return Response("null", status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_302_FOUND)


# update a user info
@api_view(['PUT', ])
def api_update_user_view(request, android_id):
    try:
        # users = User.objects.all()
        user = User.objects.get(android_id=android_id)
        request.POST._mutable = True;
        request.data['android_id'] = android_id
        request.POST._mutable = False;
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        print(request)
        serializer = UserSerializer(user, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data["success"] = "update successful"
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Partial update  a user record
class UserPartialUpdateView(generics.UpdateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'android_id'

    def partial_update(self, request, *args, **kwargs):
        # model = self.get_object()
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

# delete a user on the basis of user_id
@api_view(['DELETE', ])
def api_delete_user_view(request, user_id):
    try:
        user = User.objects.get(user_id=user_id)

    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "DELETE":
        operation = user.delete()
        data = {}
        if operation:
            data["success"] = "delete successful"
        else:
            data["failure"] = "delete failed"
        return Response(data=data)


# Create a new user
@api_view(['POST', ])
def api_create_user_view(request):
    user = User()
    if request.method == "POST":
        serializer = UserSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # Unsuccessful insertion


# Save a new mobile image info  in mobile_images table and return the latest entry info
class ImageCreateAPIView(CreateAPIView):
    serializer_class = MobileImagesSerializer
    images = MobileImages.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        # return Response(serializer.data['mobile_image_id'], status=status.HTTP_201_CREATED, headers=headers)


# Update complete Image record in mobile_images table, missing values in update query will store null
class ImageUpdateAPIView(UpdateAPIView):
    serializer_class = MobileImagesSerializer
    # queryset = MobileImages.objects.filter(android_id=uid).last()
    queryset = MobileImages.objects.all()
    lookup_field = 'mobile_image_id'


# Partial update  in mobile_images table
class ImagePartialUpdateView(generics.UpdateAPIView):

    queryset = MobileImages.objects.all()
    serializer_class = MobileImagesSerializer
    lookup_field = 'mobile_image_id'

    #def put(self, request, *args, **kwargs):
    #    return self.partial_update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        # model = self.get_object()
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    '''
    def partial_update(self, request):
        serializer = MobileImagesSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    '''


#####   Due to logic update , Image model and its methods and classes are no more in use now. #######
'''
# Save a new mobile image info in images table and return the latest entry info
class NewImageCreateAPIView(CreateAPIView):
    serializer_class = ImagesSerializer
    images = Images.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        # return Response(serializer.data['mobile_image_id'], status=status.HTTP_201_CREATED, headers=headers)


# Update complete Image record in image table, missing values in update query will store null
class UpdateImageAPIView(UpdateAPIView):
    serializer_class = ImagesSerializer
    # queryset = MobileImages.objects.filter(android_id=uid).last()
    queryset = Images.objects.all()
    lookup_field = 'image_id'


# Partial update - image info
class PartialUpdateImageView(generics.UpdateAPIView):
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer
    lookup_field = 'image_id'

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
'''
# Calculate Target Object's height using trunk n canopy endpoints
@api_view(['POST', ])
def api_save_health_parameters_view(request):
    try:
        '''
        # Retrieve latest image id
        mobile_image_dict = MobileImages.objects.all().aggregate(Max('mobile_image_id'))
        mobile_image_id = mobile_image_dict.get('mobile_image_id__max')
        image_info = MobileImages.objects.get(mobile_image_id=mobile_image_id)
        '''
        android_id = request.data['android_id']

        # image_info1 = MobileImages.objects.get.aggregate(Max('date_time'))
        # date_time_dict = MobileImages.objects.all().aggregate(Max('date_time'))
        # date_time = date_time_dict.get('date_time__max')
        # date_time = MobileImages.objects.all().aggregate(Max('date_time')).get('date_time__max')
        # image_info = MobileImages.objects.get(Q(android_id=android_id), Q(date_time=date_time))

        user_info = User.objects.get(android_id=android_id)
        # image_info_list = MobileImages.objects.filter(android_id=android_id)
        # image_info = MobileImages.objects.get(date_time=date_time)  # , date_time=date_time)
        # latest_image = image_info_list.objects.get(date_time=image_info_list.objects.all().aggregate(Max('date_time')).get('date_time__max'))
        # image_info = MobileImages.objects.get(android_id=android_id, date_time = MobileImages.objects.all().aggregate(Max('date_time')).get('date_time__max'))  #, date_time=date_time)
        # image_info = MobileImages.objects.get(android_id__exact=android_id, date_time__exact=date_time)

        # image_info = MobileImages.objects.filter(android_id=android_id).latest('date_time')
        # Get the last/latest image stored in the DB against a particular user
        image_info = MobileImages.objects.filter(android_id=android_id).last()
        image = getattr(image_info, 'image')
        mobile_image_id = getattr(image_info, 'mobile_image_id')

        # Mobile Screen Width in pixels
        screen_width = int(getattr(user_info, 'mobile_screen_width'))
        # Mobile Screen Height in pixels
        screen_height = int(getattr(user_info, 'mobile_screen_height'))

        # Reference object points in pixels
        ref_right_top_x = int(getattr(image_info, 'ref_right_top_x'))
        ref_right_top_y = int(getattr(image_info, 'ref_right_top_y'))

        ref_right_bottom_x = int(getattr(image_info, 'ref_right_bottom_x'))
        ref_right_bottom_y = int(getattr(image_info, 'ref_right_bottom_y'))

        ref_left_top_x = int(getattr(image_info, 'ref_left_top_x'))
        ref_left_top_y = int(getattr(image_info, 'ref_left_top_y'))

        ref_left_bottom_x = int(getattr(image_info, 'ref_left_bottom_x'))
        ref_left_bottom_y = int(getattr(image_info, 'ref_left_bottom_y'))

        # Target object points in pixels
        target_right_top_x = int(getattr(image_info, 'target_right_top_x'))
        target_right_top_y = int(getattr(image_info, 'target_right_top_y'))

        target_right_bottom_x = int(getattr(image_info, 'target_right_bottom_x'))
        target_right_bottom_y = int(getattr(image_info, 'target_right_bottom_y'))

        target_left_top_x = int(getattr(image_info, 'target_left_top_x'))
        target_left_top_y = int(getattr(image_info, 'target_left_top_y'))

        target_left_bottom_x = int(getattr(image_info, 'target_left_bottom_x'))
        target_left_bottom_y = int(getattr(image_info, 'target_left_bottom_y'))

        # Image height and width in pixels
        image_height = int(getattr(image_info, 'image_height'))
        image_width = int(getattr(image_info, 'image_width'))

        # Reference object coordinates in pixels (Integer)
        ref_rty = int(((int(ref_right_top_y)) * image_height) / screen_height)      # Right top x-axis point
        ref_rtx = int(((int(ref_right_top_x)) * image_width) / screen_width)        # Right top y-axis point

        ref_rby = int(((int(ref_right_bottom_y)) * image_height) / screen_height)   # Right bottom x-axis point
        ref_rbx = int(((int(ref_right_bottom_x)) * image_width) / screen_width)     # Right bottom y-axis point

        ref_lty = int(((int(ref_left_top_y)) * image_height) / screen_height)       # Left top x-axis point
        ref_ltx = int(((int(ref_left_top_x)) * image_width) / screen_width)         # Left top y-axis point

        ref_lby = int(((int(ref_left_bottom_y)) * image_height) / screen_height)    # Left bottom x-axis point
        ref_lbx = int(((int(ref_left_bottom_x)) * image_width) / screen_width)      # Right bottom y-axis point

        # Target object coordinates in pixels (Integer)
        target_rty = int(((int(target_right_top_y)) * image_height) / screen_height)
        target_rtx = int(((int(target_right_top_x)) * image_width) / screen_width)

        target_rby = int(((int(target_right_bottom_y)) * image_height) / screen_height)
        target_rbx = int(((int(target_right_bottom_x)) * image_width) / screen_width)

        target_lty = int(((int(target_left_top_y)) * image_height) / screen_height)
        target_ltx = int(((int(target_left_top_x)) * image_width) / screen_width)

        target_lby = int(((int(target_left_bottom_y)) * image_height) / screen_height)
        target_lbx = int(((int(target_left_bottom_x)) * image_width) / screen_width)

        # Reference Object's Width/diameter in Inches
        diameter = float(getattr(image_info, 'diameter'))


        # ROI of objects
        # Coordinates in (x,y) format
        all_coordinates = [[[(ref_rtx, ref_rty), (ref_rbx, ref_rby), (ref_ltx, ref_lty), (ref_lbx, ref_lby)]],
                [[(target_rtx, target_rty), (target_rbx, target_rby), (target_ltx, target_lty), (target_lbx, target_lby)]]]
        counter = 0

        for coordinate in all_coordinates:
            # mask with same size of image
            # image_path = image.path
            # img = cv2.imread('C:/Users/habiba.saim/git_repo/narl/ForestAssetManagementSystem/media/images/IMG_20191205_114522_buddskt.jpg')
            img = cv2.imread(image.path)
            # img = cv2.cv.LoadImage(image.path)
            mask = np.ones(img.shape, dtype=np.uint8)
            mask.fill(255)
            # points to be cropped
            roi_corners = np.array(tuple(coordinate), dtype=np.int32)
            # fill the ROI into the mask
            cv2.fillPoly(mask, roi_corners, 0)
            masked_image = cv2.bitwise_or(img, mask)
            # save ROI in a folder
            cv2.imwrite("C:/Users/habiba.saim/git_repo/narl/ForestAssetManagementSystem/media/ROI_images/image%d.jpg" % counter, masked_image)
            #cv2.imwrite(   "C:/Users/habiba.saim/git_repo/narl/ForestAssetManagementSystem/media/ROI_images/image13.jpg", mask)
            counter += 1

            # read ROI images from folder
        image1 = cv2.imread("C:/Users/habiba.saim/git_repo/narl/ForestAssetManagementSystem/media/ROI_images/image0.jpg")
        image2 = cv2.imread("C:/Users/habiba.saim/git_repo/narl/ForestAssetManagementSystem/media/ROI_images/image1.jpg")

        # combine ROI images
        combined_image = image1 + image2
        #combined_image = combined_image + image3
            # rotate image
        combined_image = cv2.rotate(combined_image, cv2.ROTATE_90_CLOCKWISE)
            # convert to gray scale and find edges
        gray = cv2.cvtColor(combined_image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)
        edged = cv2.Canny(blurred, 10, 10)
        dilated_image = cv2.dilate(edged, None, iterations=1)
        eroded_image = cv2.erode(dilated_image, None, iterations=1)
        # cv2.imwrite("ROI_images/edged_image12result.jpg", eroded_image)
        # find the contours
        cnts = cv2.findContours(eroded_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imul.grab_contours(cnts)
        # sort the contours
        (cnts, _) = contours.sort_contours(cnts)

        pixels_per_matrix = None
        ref_height = []
        target_height = []
        ref_point = []
        taget_point = []
        count = 0
        # loop over the contours individually
        for image_contour in cnts:
            # if the contour is not sufficiently large, ignore it
            if cv2.contourArea(image_contour) < 500:
                continue
            # compute the rotated bounding box of the contour
            orig = img.copy()
            orig = cv2.rotate(orig, cv2.ROTATE_90_CLOCKWISE)
            box = cv2.minAreaRect(image_contour)
            box = cv2.cv.BoxPoints(box) if imul.is_cv2() else cv2.boxPoints(box)
            box = np.array(box, dtype="int")

            # order the points in the contour such that they appear
            # in top-left, top-right, bottom-right, and bottom-left
            # order, then draw the outline of the rotated bounding
            # box
            box = perspective.order_points(box)
            cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)

            # loop over the original points and draw them
            for (x, y) in box:
                cv2.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)
            # unpack the ordered bounding box, then compute the midpoint
            # between the top-left and top-right coordinates, followed by
            # the midpoint between bottom-left and bottom-right coordinates
            (tl, tr, br, bl) = box
            (tltrX, tltrY) = calculate_midpoint(tl, tr)
            (blbrX, blbrY) = calculate_midpoint(bl, br)

            # compute the midpoint between the top-left and top-right points,
            # followed by the midpoint between the top-righ and bottom-right
            (tlblX, tlblY) = calculate_midpoint(tl, bl)
            (trbrX, trbrY) = calculate_midpoint(tr, br)
            # draw the midpoints on the image
            cv2.circle(orig, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
            cv2.circle(orig, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
            cv2.circle(orig, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
            cv2.circle(orig, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)

            # draw lines between the midpoints
            cv2.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)), (255, 0, 255), 2)
            cv2.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)), (255, 0, 255), 2)
            # compute the Euclidean distance between the midpoints
            dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
            dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

            # if the pixels per metric has not been initialized, then
            # compute it as the ratio of pixels to supplied metric
            # (in this case, inches)
            if pixels_per_matrix is None:
                pixels_per_matrix = dA / diameter  # height
            dimA = (dA / pixels_per_matrix)     # Object height
            dimB = (dB / pixels_per_matrix)     # Object width - inches

            dimB = dimB / 12
            if count == 0:
                ref_height.append(dimB)
                print("ref height ")
                print(ref_height)
            elif count == 1:
                target_height.append(dimB)
                print("target height and width")
                print(target_height)
            else:
                print("Nothing apend!!!")
            #request.data['height'] = dimB
            #calculate_biomass(diameter)
            # draw the object sizes on the image
            #cv2.putText(orig, "{:.1f}ft".format(dimA / 12),
             #           (int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,
              #          0.65, (255, 255, 255), 5)
           # cv2.putText(orig, "{:.1f}ft".format(dimB / 12),
                       # (int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,
                      #  0.65, (255, 255, 255), 5)
            # rotate image again before saving
            orig = cv2.rotate(orig, cv2.ROTATE_90_COUNTERCLOCKWISE)
            # save resulted image
            count += 1
        # tree_height=67
        tree_height = float(ref_height[0] + target_height[0])
        above_biomass = calculate_biomass(diameter, tree_height)
        below_biomass = above_biomass * 0.20
        total_biomass = (above_biomass + below_biomass) / 2.2
        carbon_stock = (total_biomass/2)

        img2 = img.copy()
        cv2.putText(img2, "Tree Height", (int(img2.shape[1] / 2), int(img2.shape[0] - 320)), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (0, 255, 0), 10)
        cv2.putText(img2, "%.2fft" % tree_height,
                  (int(img2.shape[1] / 2), int(img2.shape[0] - 230)), cv2.FONT_HERSHEY_SIMPLEX,
                  2, (0, 255, 0), 20)
        # draw the lower and upper points on the image
        # cv2.circle(img2, (ref_point[0][0], ref_point[0][1]), 20, (255, 0, 0), -1)
        # cv2.circle(img2, (taget_point[0][0], taget_point[0][1]), 20, (255, 0, 0), -1)
        # cv2.line(img2, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)), (255, 0, 255), 10)
        cv2.imwrite("C:/Users/habiba.saim/git_repo/narl/ForestAssetManagementSystem/media/Resultant_images/image.jpg", img2)

        #  Enable editing in request
        request.POST._mutable = True;
        request.data['height'] = tree_height
        request.data['mobile_image_id'] = mobile_image_id

        request.data['biomass'] = total_biomass
        request.data['carbon_content'] = carbon_stock
        request.POST._mutable = False;

        health_results = HealthResults()
        # #### Resolving duplicate health results entries###
        # Stopping the server from trying to store multiple health results
        '''
        if request.method == "POST" and HealthResults.objects.filter(mobile_image_id=mobile_image_id).exists() is False:
            serializer = HealthResultsSerializer(health_results, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response("Record already exists, duplicate entry not allowed")
        # #### END - Resolving duplicate health results entries###
        '''
        if request.method == "POST":
            serializer = HealthResultsSerializer(health_results, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

    except MobileImages.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

# Calculate Target Object's height using cropped images
@api_view(['POST', ])
def api_calculate_health_parameters_view(request):

    try:
        android_id = request.data['android_id']
        user_info = User.objects.get(android_id=android_id)

        # Get the last/latest image stored in the DB against a particular user
        image_info = MobileImages.objects.filter(android_id=android_id).last()
        mobile_image_id = getattr(image_info,'mobile_image_id')
        # image = getattr(image_info, 'image')
        canopy = getattr(image_info, 'canopy')
        trunk = getattr(image_info, 'trunk')

        image_names = [canopy, trunk]
        images = []
        max_width = 0  # find the max width of all the images
        total_height = 0  # the total height of the images (vertical stacking)

        for name in image_names:
            # open all images and find their sizes
            images.append(cv2.imread(name.path))
            if images[-1].shape[1] > max_width:
                max_width = images[-1].shape[1] + 20
            total_height += images[-1].shape[0] + 20

        # create a new array with a size large enough to contain all the images
        final_image = np.zeros((total_height, max_width, 3), dtype=np.uint8)

        current_y = 20  # keep track of where your current image was last placed in the y coordinate
        for image in images:
            # add an image to the final array and increment the y coordinate
            final_image[current_y:image.shape[0] + current_y, :image.shape[1], :] = image
            current_y += image.shape[0] + 20

        cv2.imwrite('C:/Users/habiba.saim/git_repo/narl/ForestAssetManagementSystem/media/images/cropped/combined_image%d.jpg' %mobile_image_id, final_image)

        img = cv2.imread('C:/Users/habiba.saim/git_repo/narl/ForestAssetManagementSystem/media/images/cropped/combined_image%d.jpg' %mobile_image_id)

        # cv2.imwrite('C:/Users/habiba.saim/git_repo/narl/ForestAssetManagementSystem/media/images/results/rotated.jpg', rotated_img)
        # imgmatto = cv2.imread('C:/Users/habiba.saim/git_repo/narl/ForestAssetManagementSystem/media/images/cropped/final.jpg')

        rotated_img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        gray = cv2.cvtColor(rotated_img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)
        edged = cv2.Canny(blurred, 5, 5)
        dilated_image = cv2.dilate(edged, None, iterations=1)
        eroded_image = cv2.erode(dilated_image, None, iterations=1)

        cnts = cv2.findContours(eroded_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imul.grab_contours(cnts)
        (cnts, _) = contours.sort_contours(cnts)
        # Reference Object's Width/diameter in Inches
        diameter = float(getattr(image_info, 'diameter'))

        pixelsPerMetric = None
        cont = 0
        ref = []
        trg = []
        # loop over the contours individually
        for c in cnts:
            # if the contour is not sufficiently large, ignore it
            if cv2.contourArea(c) < 10000:
                continue
            # compute the rotated bounding box of the contour
            orig = rotated_img.copy()
            box = cv2.minAreaRect(c)
            box = cv2.cv.BoxPoints(box) if imul.is_cv2() else cv2.boxPoints(box)
            box = np.array(box, dtype="int")
            # order the points in the contour such that they appear
            # in top-left, top-right, bottom-right, and bottom-left
            # order, then draw the outline of the rotated bounding
            # box
            box = perspective.order_points(box)
            cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)
            # loop over the original points and draw them
            for (x, y) in box:
                cv2.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)
            # unpack the ordered bounding box, then compute the midpoint
            # between the top-left and top-right coordinates, followed by
            # the midpoint between bottom-left and bottom-right coordinates
            (tl, tr, br, bl) = box
            (tltrX, tltrY) = calculate_midpoint(tl, tr)
            (blbrX, blbrY) = calculate_midpoint(bl, br)
            # compute the midpoint between the top-left and top-right points,
            # followed by the midpoint between the top-righ and bottom-right
            (tlblX, tlblY) = calculate_midpoint(tl, bl)
            (trbrX, trbrY) = calculate_midpoint(tr, br)
            # draw the midpoints on the image
            cv2.circle(orig, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
            cv2.circle(orig, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
            cv2.circle(orig, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
            cv2.circle(orig, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)
            # draw lines between the midpoints
            cv2.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),
                     (255, 0, 255), 2)
            cv2.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
                     (255, 0, 255), 2)
            # compute the Euclidean distance between the midpoints
            dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
            dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
            # if the pixels per metric has not been initialized, then
            # compute it as the ratio of pixels to supplied metric
            # (in this case, inches)
            if pixelsPerMetric is None:
                pixelsPerMetric = dA / diameter
            # compute the size of the object
            dimB = dB / pixelsPerMetric
            dimA = dA / pixelsPerMetric

            ref.append(dimB)

            # draw the object sizes on the image
            cv2.putText(orig, "{:.1f}ft".format(dimA / 12),
                        (int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,
                        0.65, (255, 255, 255), 2)
            cv2.putText(orig, "{:.1f}ft".format(dimB / 12),
                        (int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,
                        0.65, (255, 255, 255), 2)
            #rotated_image = cv2.rotate(orig, cv2.ROTATE_90_COUNTERCLOCKWISE)
            cv2.imwrite("C:/Users/habiba.saim/git_repo/narl/ForestAssetManagementSystem/media/images/results/image%d.jpg" % cont, orig)
            cont += 1

        #original_image = cv2.imread("images/im.jpg")
        n = len(ref)
        trg_height = canopy_height(ref, n)
        ref_height = trunk_height(ref)
        height = (trg_height + ref_height) / 12

        above_biomass = calculate_biomass(diameter, height)
        below_biomass = above_biomass * 0.20
        total_biomass = (above_biomass + below_biomass) / 2.2
        carbon_stock = (total_biomass / 2)
        #cv2.putText(original_image, "%.2fft" % (height / 12),
        #            (original_image.shape[1] - 1200, original_image.shape[0] - 200), cv2.FONT_HERSHEY_SIMPLEX,
         #           10, (0, 255, 0), 10)
        #cv2.imwrite("matto/final.jpg", original_image)

        #  Enable editing in request
        request.POST._mutable = True
        request.data['height'] = height
        request.data['mobile_image_id'] = mobile_image_id
        request.data['biomass'] = total_biomass
        request.data['carbon_content'] = carbon_stock
        # request.data['original_image'] = rotated_image
        request.POST._mutable = False

        health_results = HealthResults()

        if request.method == "POST":

            serializer = HealthResultsSerializer(health_results, data=request.data)
            if serializer.is_valid():
                serializer.save()
                # print("take_backup(android_id)")
                # view = api_create_backup_view(request._request)
                # view = CreateBackupAPIView.as_view()
                # print (view)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                print("Error")
    except MobileImages.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


def calculate_sensor_height(focalLength, viewAngle):
    SH = 2 * (focalLength * (math.tan(viewAngle/2)))
    return SH


# Calculate Target Object's height using two images of same object
@api_view(['POST', ])
def api_find_health_parameters_view(request):

    try:
        android_id = request.data['android_id']
        user_info = User.objects.get(android_id=android_id)

        # Get the last/latest image stored in the DB against a particular user
        image_info = MobileImages.objects.filter(android_id=android_id).last()
        image_id = getattr(image_info, 'mobile_image_id')
        original_image = getattr(image_info, 'original_image')
        far_image = getattr(image_info, 'far_image')
        close_image = getattr(image_info, 'close_image')
        s = float(getattr(user_info, 'sensor_height'))
        f = float(getattr(user_info, 'focal_length'))
        diameter_of_tree = float(getattr(image_info, 'diameter'))
        diameter_of_tree = diameter_of_tree / 12  # convert diameter in ft from inches
        distance = float(getattr(image_info, 'distance'))
        distance = distance * 304.8  # convert distance in mm

        original_image = cv2.imread(original_image.path)
        [h, w, z] = original_image.shape

        far_image = cv2.imread(far_image.path)
        [ah, aw, az] = far_image.shape

        close_image = cv2.imread(close_image.path)
        [bh, bw, bz] = close_image.shape

        #f = 3.83
        # s = 4.69
        L = h
        l = ah
        Angle = 52.4098
        #s = Sensor_Height(f, Angle)

        if diameter_of_tree != 0:
            # distance calculation
            object_distance = distance / (1 - (ah / bh))
            df = object_distance * 0.00328084

            # height calculation
            Height = (object_distance * s * l) / (f * L)
            hf = Height * 0.00328084
            above_biomass = calculate_biomass(diameter_of_tree, hf)
            below_biomass = above_biomass * 0.20
            total_biomass = (above_biomass + below_biomass) / 2.2
            carbon_stock = (total_biomass / 2)
            carbon_sequestration = (carbon_stock * 3.68)
            request.POST._mutable = True
            request.data['height'] = hf
            request.data['mobile_image_id'] = image_id
            request.data['distance'] = df
            request.data['biomass'] = total_biomass
            request.data['carbon_content'] = carbon_stock
            request.data['total_carbon_absorbed'] = carbon_sequestration
            request.POST._mutable = False
        else:
            # distance calculation
            object_distance = distance / (1 - (ah / bh))
            df = object_distance * 0.00328084

            # height calculation
            Height = (object_distance * s * l) / (f * L)
            hf = Height * 0.00328084
            #  Enable editing in request
            request.POST._mutable = True
            request.data['height'] = hf
            request.data['mobile_image_id'] = image_id
            request.data['distance'] = df
            request.POST._mutable = False


        health_results = HealthResults()

        if request.method == "POST":
            serializer = HealthResultsSerializer(health_results, data=request.data)
            if serializer.is_valid():
                serializer.save()
                # print("take_backup(android_id)")
                # view = api_create_backup_view(request._request)
                # view = CreateBackupAPIView.as_view()
                # print (view)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                print("Error")
    except MobileImages.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)



'''
# Get particular image info from images table
@api_view(['GET', ])
def api_image_view(request, mid):
    try:
        image_info = Images.objects.filter(image_id=mid).first()
        # image_info = MobileImages.objects.get(mobile_image_id=image_id)
        context = {
            "request": request,
        }
        # image = getattr(image_info, 'image')
        # print(image)

    except Images.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ImagesSerializer(image_info, context=context)
        response = serializer.data
        return Response(response)


# Get all images info from images table
@api_view(['GET', ])
def api_images_list(request, ):
    try:
        results = Images.objects.all()

    except Images.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ImagesSerializer(results, many=True)
        return Response(serializer.data)

# ********* Delete particular image from images table*********
@api_view(['DELETE', ])
def api_del_image_view(request, mid):
    try:
        image = Images.objects.get(image_id=mid)

    except Images:
        return Response(status = status.HTTP_404_NOT_FOUND)

    if request.method == "DELETE":
        operation = image.delete()
        data = {}
        if operation:
            data["success"] = "Delete successful"
        else:
            data["failure"] = "Delete failed"
        return Response(data=data)
    return Response("Error")
'''

# Store backup of recent image upload and results calculation
# In use
@api_view(['POST', ])
def api_create_backup_view(request):
    backup = Backup()

    print("Inside create backup")
    if request.method == "POST":
        # try:
            serializer = BackupSerializer(backup, data=request.data)
            android_id = request.data['android_id']
            image_info = MobileImages.objects.filter(android_id=android_id).last()
            mobile_image_id = getattr(image_info, 'mobile_image_id', "NULL")
            diameter = getattr(image_info, 'diameter')
            if image_info.original_image:
                original_image = getattr(image_info, 'original_image', None)     #image_path = cv2.imread(image.path)
            else:
                original_image = None
            if image_info.canopy:
                canopy = getattr(image_info, 'canopy', None)
            else:
                canopy = None

            if image_info.trunk:
                trunk = getattr(image_info, 'trunk')
            else:
                trunk = None

            if image_info.far_image:
                far_image = getattr(image_info, 'far_image')
            else:
                far_image = None

            if image_info.close_image:
                close_image = getattr(image_info, 'close_image')
            else:
                close_image = None

            distance = getattr(image_info, 'distance')
            latitude = getattr(image_info, 'latitude')
            longitude = getattr(image_info, 'longitude')
            date_time = str(getattr(image_info, 'date_time'))

            health_results = HealthResults.objects.filter(mobile_image_id = mobile_image_id).last()
            health_results_id = getattr(health_results, 'health_results_id')
            height = getattr(health_results, 'height')
            biomass = getattr(health_results, 'biomass')
            carbon_content = getattr(health_results, 'carbon_content')
            total_carbon_absorbed = getattr(health_results,'total_carbon_absorbed')

            request.POST._mutable = True
            request.data['mobile_image_id'] = mobile_image_id
            request.data['diameter'] = diameter
            request.data['original_image'] = original_image
            request.data['canopy'] = canopy
            request.data['trunk'] = trunk
            request.data['far_image'] = far_image
            request.data['close_image'] = close_image
            request.data['distance'] = distance
            request.data['latitude']= latitude
            request.data['longitude'] = longitude
            request.data['date_time'] = date_time
            request.data['health_results_id'] = health_results_id
            request.data['height'] = height
            request.data['biomass'] = biomass
            request.data['carbon_content'] = carbon_content
            request.data['total_carbon_absorbed'] = total_carbon_absorbed
            # request.data['original_image'] = rotated_image
            request.POST._mutable = False
            # print(request)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Unsuccessful insertion
        # except AttributeError as error:
            # response = "Missing values of some attributes"
            # return Response(response, status=status.HTTP_206_PARTIAL_CONTENT)


# update an image record, add canopy - not using for now
@api_view(['PUT', ])
def api_add_cropped_image_view(request, uid):

    try:
        image_info = MobileImages.objects.filter(android_id=uid).last()
    except MobileImages.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        serializer = MobileImagesSerializer(image_info, data=request.data, partial=True)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data["success"] = "update successful"
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def calculate_midpoint(point_a, point_b):
    return (point_a[0] + point_b[0]) * 0.5, (point_a[1] + point_b[1]) * 0.5


def canopy_height(arr, n):
    maximum = arr[0]
    for i in range(1, n):
        if arr[i] > maximum:
            maximum = arr[i]
    return maximum


def trunk_height(list1):
    largest = list1[0]
    lowest = list1[0]
    largest2 = None
    lowest2 = None
    for item in list1[1:]:
        if item > largest:
            largest2 = largest
            largest = item
        elif largest2 == None or largest2 < item:
            largest2 = item
        if item < lowest:
            lowest2 = lowest
            lowest = item
        elif lowest2 == None or lowest2 > item:
            lowest2 = item
    return largest2


# Calculates above ground biomass
def calculate_biomass(diameter, height):

    if diameter == 0:
        above_biomass = 0
    elif 0 < diameter < 11:
        above_biomass = ((diameter * diameter) * height) * 0.25
    elif diameter >= 11:
        above_biomass = ((diameter * diameter) * height) * 0.15

    return above_biomass


# Get particular image info of mobile_images table
@api_view(['GET', ])
def api_image_info_view(request, image_id):
    try:
        image_info = MobileImages.objects.filter(mobile_image_id=image_id).first()
        # image_info = MobileImages.objects.get(mobile_image_id=image_id)
        context = {
            "request": request,
        }
        # image = getattr(image_info, 'image')
        # print(image)

    except MobileImages.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = MobileImagesSerializer(image_info, context=context)
        response = serializer.data
        return Response(response)


# Get all images info of mobile_images table
@api_view(['GET', ])
def api_images_view(request, ):
    try:
        results = MobileImages.objects.all()

    except MobileImages.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = MobileImagesSerializer(results, many=True)
        return Response(serializer.data)

# ################### HealthResults Functions and Classes #############
# list of all health results in the DB
@api_view(['GET', ])
def api_health_results_view(request, ):
    try:
        results = HealthResults.objects.all()

    except HealthResults.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = HealthResultsSerializer(results, many=True)
        return Response(serializer.data)


# Get particular tree health results through health result id
@api_view(['GET', ])
def api_health_results_view_single(request, health_results_id):
    try:
        result = HealthResults.objects.get(health_results_id=health_results_id)

    except HealthResults.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = HealthResultsSerializer(result)
        return Response(serializer.data)


# Get particular tree health results through image id
@api_view(['GET', ])
def api_tree_health_results_view_single(request, mobile_image_id):
    try:
        result = HealthResults.objects.filter(mobile_image_id=mobile_image_id).first()

    except HealthResults.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = HealthResultsSerializer(result)
        return Response(serializer.data)

# ************Get user and his images history ************
# Get images associated to a particular android_id -in use
@api_view(['GET', ])
def api_user_images_history_view(request, android_id):
    try:

        images = MobileImages.objects.filter(android_id=android_id).exclude(close_image__isnull=True).exclude(close_image__exact='')
        context = {
            "request": request,
        }

    except MobileImages.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        image_serializer = MobileImagesSerializer(images, many=True, context=context)
        response = image_serializer.data
        return Response(response)


# Get user and images associated to his android_id by combining relevant serializers
@api_view(['GET', ])
def user_history_view(request, android_id):
    try:
        user = User.objects.filter(android_id=android_id)
        images = MobileImages.objects.filter(android_id=android_id)

        context = {
            "request": request,
        }

    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        user_serializer = UserSerializer(user, many=True, context=context)
        image_serializer = MobileImagesSerializer(images, many=True, context=context)

        response = user_serializer.data + image_serializer.data
        return Response(response)

# Get user  images count
@api_view(['GET', ])
def api_user_images_count_view(request, uid):
    try:
        images = MobileImages.objects.filter(android_id=uid)

    except MobileImages.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        total = images.count()
        return Response(total)


# Get image id on the basis of latitude and longitude
@api_view(['GET', ])
def api_imageid_view(request, latitude, longitude):
    try:
        # latitude = request.data['latitude']
        # longitude = request.data['longitude']
        image = MobileImages.objects.get(latitude=latitude, longitude=longitude)
        image_id = int(getattr(image, 'mobile_image_id'))

    except MobileImages.DoesNotExist:
        image_id = 0
        return Response(image_id, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        return Response(image_id, status= status.HTTP_200_OK)


# Get all  images IDs, Longitude, and Latitude
@api_view(['GET', ])
def api_images_location_view(request):
    try:
        #images = MobileImages.objects.exclude(latitude='')
        # Return image_id, latitude and longitude of complete image records
        images = MobileImages.objects.exclude(latitude__isnull=True).exclude(latitude__exact='').\
            exclude(close_image__isnull=True).exclude(close_image__exact='').values('mobile_image_id', 'latitude',
                                                                                    'longitude')
        # images = MobileImages.objects.all()


    except MobileImages.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = MobileImagesSerializer(images, many = True)
        return Response(serializer.data)

# Get user and images associated to his android_id through DB view ----- not working on it for now
'''
@api_view(['GET', ])
def api_user_history_view(request, android_id):
    try:
        # user = User.objects.get(android_id=android_id)
        # images = MobileImages.objects.filter(android_id=android_id)
        history_list = UserHistory.objects.filter(android_id=android_id)

    except UserHistory.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = UserHistorySerializer(history_list)
        return Response(serializer.data)
'''

# *******************Delete user's history, on his request **************
# delete a user on the basis of user_id - not complete yet
@api_view(['DELETE', ])
def api_delete_user_history_view(request, mid):
    try:
        images = MobileImages.objects.filter(android_id=mid)

    except MobileImages.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "DELETE":
        operation = images.delete()
        data = {}
        if operation:
            data["success"] = "delete successful"
        else:
            data["failure"] = "delete failed"
        return Response(data=data)


# ********* Delete particular image *********
@api_view(['DELETE', ])
def api_delete_image_view(request, mid):
    try:
        image = MobileImages.objects.get(mobile_image_id=mid)
        #results = HealthResults.objects.filter(mobile_image_id=id)   ----- Not needed due to On delete cascade
    except MobileImages:
        return Response(status = status.HTTP_404_NOT_FOUND)
    if request.method == "DELETE":
        operation1 = image.delete()
        #operation2 = results.delete()
        data = {}
        if operation1:
            data["success"] = "Delete successful"
        else:
            data["failure"] = "Delete failed"
        return Response(data=data)
    return Response("Error")

# Get accumulated biomass for a particular user during a particular date range
@api_view(['POST', ])
def api_calculate_accumulated_biomass_view(request, param1, param2, param3):
    try:


        process_id = param1
        start_date = param2
        end_date = param3
        # print('Id:', process_id, ' lower date:', start_date, ' upper_date: ', end_date)
        description = "The process takes process id, start date, end date as input from the user and calculates " \
                      "total biomass of the records stored by that particular user in the specified time period and " \
                      "the tree count of the trees that participated in the biomass calculation"

        # images_info = MobileImages.objects.filter(android_id=android_id, date_time__range=(start_date, end_date))
        images_info = MobileImages.objects.filter(process_id=process_id, date_time__lte=end_date, date_time__gte=start_date)
        # print('images_info: ',images_info)
        total_biomass = 0
        image_count = 0
        user = None
        if images_info is None:
            return Response("No tree images were stored during the specified period")
        for image in images_info:
            image_id = int(getattr(image, 'mobile_image_id'))
            result = HealthResults.objects.filter(mobile_image_id=image_id).first()
            biomass = float(getattr(result, 'biomass'))
            total_biomass += biomass
            image_count += 1
            user =getattr(image, 'android_id')    # object is being returned here
            # print('android_id: ', user)
        # print('Total biomass///////,', total_biomass)
        # images = MobileImages.objects.filter(android_id=android_id)
        # user = User.objects.get(android_id=android_id)
        # android_id = getattr(user, 'android_id')
        process_owner = getattr(user, 'name', 'not found')

        request.POST._mutable = True;
        request.data['process_owner'] = process_owner
        request.data['description'] = description
        request.data['param1'] = start_date
        request.data['param2'] = end_date
        request.data['result1'] = total_biomass
        request.data['result2'] = image_count
        request.data['process_id'] = process_id  # The Id generated at KMAT
        request.POST._mutable = False;

        process = Processes()

        if request.method == "POST":
            serializer = ProcessSerializer(process, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Processes.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


# Get particular process
@api_view(['GET', ])
def api_process_view(request, pid):
    try:
        process = Processes.objects.filter(process_id=pid).last()
        # users_name = User.objects.get(name = name)

    except Processes.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ProcessSerializer(process)
        return Response(serializer.data)


# Delete all entries of a KMAT process with its results
@api_view(['DELETE', ])
def api_delete_process_view(request, pid):
    try:
        images = MobileImages.objects.filter(process_id=pid)
    except MobileImages:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "DELETE":
        operation = images.delete()

        data = {}
        if operation:
            data["success"] = "Delete successful"
        else:
            data["failure"] = "Delete failed"
        return Response(data=data)
    return Response("Error")

# ********** Feedback *********** #

# Enter new feedback
@api_view(['POST', ])
def api_create_feedback_view(request):
    feedback = Feedback()
    if request.method == "POST":
        serializer = FeedbackSerializer(feedback, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # Unsuccessful insertion


# list of all feedbacks
@api_view(['GET', ])
def api_feedbacks_view(request, ):
    try:
        feedbacks = Feedback.objects.all()

    except Feedback.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = FeedbackSerializer(feedbacks, many=True)
        return Response(serializer.data)


# Get particular feedback
@api_view(['GET', ])
def api_feedback_view(request, fid):
    try:
        feedback = Feedback.objects.get(feedback_id=fid)

    except Feedback.DoesNotExist:
        return Response("null", status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = FeedbackSerializer(feedback)
        return Response(serializer.data, status=status.HTTP_302_FOUND)



