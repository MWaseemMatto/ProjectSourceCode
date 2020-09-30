from django.urls import path

from treeHealth.api.views import (
    api_user_view,
    api_create_user_view,
    api_delete_user_view,
    api_update_user_view,
    api_users_view,
    UserPartialUpdateView,

    # api_input_mobile_info_view,

    # for images_info table
    api_image_info_view,
    api_images_view,
    ImageCreateAPIView,
    ImageUpdateAPIView,
    ImagePartialUpdateView,
    api_images_location_view,
    api_imageid_view,


    api_save_health_parameters_view,
    api_calculate_health_parameters_view,
    api_find_health_parameters_view,
    api_health_results_view,
    api_health_results_view_single,

    user_history_view,
    api_user_images_count_view,

    api_tree_health_results_view_single,
    api_user_images_history_view,
    api_delete_user_history_view,
    api_delete_image_view,
    api_add_cropped_image_view,

    api_calculate_accumulated_biomass_view,
    api_process_view,
    api_delete_process_view,
    api_create_backup_view,

    api_create_feedback_view,
    api_feedbacks_view,
    api_feedback_view,
)

app_name = 'treeHealth'

urlpatterns = [
    # user views
    path('users/', api_users_view, name = "users-list"),
    path('<aid>/get-user/', api_user_view, name="user-info"),
    path('<android_id>/update-user/', api_update_user_view, name="update"),
    path('<user_id>/delete-user/', api_delete_user_view, name="delete"),
    path('create-user/', api_create_user_view, name="create"),
    path('<android_id>/update-profile/', UserPartialUpdateView.as_view(), name="partial-update-user-record"),

    # mobile views for model MobileImages
    # path('create-mobile-info/', api_input_mobile_info_view, name="create-mobile"),

    # image views for model - MobileImages
    path('create-new-image/', ImageCreateAPIView.as_view(), name="create-new-image"),
    # path('create-image-info/', api_save_image_view, name="create-image"),
    # path('create-new-image1/', ImageCreateAPIView1.as_view(), name="create-new-image"),
    # path('create-image/', ApiSaveImageClassView.as_view(), name="create-new-image"),
    path('<image_id>/image-info/', api_image_info_view, name="image-info"),
    path('image-list/', api_images_view, name="image-info-list"),
    path('<uid>/add-cropped/', api_add_cropped_image_view, name="add-cropped"),
    path('<mobile_image_id>/update-image-info/', ImageUpdateAPIView.as_view(), name="update-image-info"), # Update complete record
    path('<mobile_image_id>/update-image/', ImagePartialUpdateView.as_view(), name="partial-update-image-info"), # Partial update in the image record
    path('<latitude>/<longitude>/get-id/', api_imageid_view, name="get-imageid-from-lat-long"),

    # health views
    # Manual - Calculate Target Object's height using trunk n canopy endpoints
    path('calculate-health-results/', api_save_health_parameters_view, name="calculate-health"),

    # Manual - Calculate Target Object's height using cropped images
    path('calculate-tree-health/', api_calculate_health_parameters_view, name="calculate-tree-health"),
    path('health-results/', api_health_results_view, name="health-results-list"),
    path('<health_results_id>/result/', api_health_results_view_single, name="health-result"),
    path('<mobile_image_id>/health-result/', api_tree_health_results_view_single, name="tree-health-result"),
    path('calc-health/', api_find_health_parameters_view, name = "Calculate-health"),


    # User and his images history
    path('<android_id>/user-history/', user_history_view, name='user-history'),
    path('<android_id>/history/', api_user_images_history_view, name='user-images-history'),
    path('location/', api_images_location_view, name='images-lat-long'),

    path('<mid>/delete-history/', api_delete_user_history_view, name='delete-history'),  # Delete complete user history
    path('<mid>/delete-image/', api_delete_image_view, name='delete-image'),             # Delete only one image and its results
    path('<uid>/images-count/', api_user_images_count_view, name='total-images'),        # Returns total user images stored in DB
    # path('<android_id>/history/', api_user_history_view, name="history"),
    # path('<android_id>/user-history/', UserHistory.as_view(), name='user-history'),

    # Process creation and execution
    path('<param1>/<param2>/<param3>/calculate-combined-biomass/', api_calculate_accumulated_biomass_view,
         name='accumulated-biomass'),
    path('<pid>/process-result/', api_process_view, name='process'),
    path('<pid>/delete-process/', api_delete_process_view, name='delete-process'),

    # Backup Creation
    path('backup/',api_create_backup_view, name='create-backup'),

    # Feedback
    path('feedback/', api_create_feedback_view, name='enter-feedback'),
    path('allfeedbacks/', api_feedbacks_view, name='all-feedbacks'),
    path('<fid>/getfeedback', api_feedback_view, name = 'one-feedback'),
]
