from django.db import models

# Create your models here.
from django.db import models

from datetime import datetime


class User(models.Model):
    user_id = models.AutoField(db_column='id_user', primary_key=True)
    profile_pic = models.ImageField(db_column='profile_pic', blank=True, null=True, upload_to="images/profile/")
    name = models.CharField(db_column='name', max_length=100, blank=True, null=True)
    field_of_interest = models.CharField(db_column='field_of_interest', max_length=200, blank=True, null=True)
    organization = models.CharField(db_column='organization', max_length=250, blank=True, null=True)
    focal_length = models.FloatField(db_column='focal_length', blank=True, null=True)
    sensor_height = models.FloatField(db_column='sensor_height', blank=True, null=True)
    android_id = models.CharField(db_column='android_id', max_length=100, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'users'


# for height finding using cropping method
class MobileImages(models.Model):
    mobile_image_id = models.AutoField(db_column='id_mobile_image', primary_key=True)
    original_image = models.ImageField(db_column='original_image', blank=True, null=True, upload_to="images/original/", width_field='image_width',
                              height_field='image_height') #, default='images/no-image.png')
    canopy = models.ImageField(db_column='canopy', blank=True, null=True, upload_to="images/cropped/")
    trunk = models.ImageField(db_column='trunk', blank=True, null=True, upload_to="images/cropped/")
    image_width = models.IntegerField(db_column='image_width', default=0)
    image_height = models.IntegerField(db_column='image_height', default=0)
    latitude = models.TextField(db_column='latitude', blank=True, null=True)
    longitude = models.TextField(db_column='longitude', blank=True, null=True)
    diameter = models.FloatField(db_column='diameter', blank=True, default=0)
    date_time = models.TextField(db_column='date_time', blank=True, null=True) # default=datetime.now())
    far_image = models.ImageField(db_column='far_image', blank=True, null=True, upload_to="images/far/")
    distance = models.FloatField(db_column='moved_distance', blank=True, null=True)
    close_image = models.ImageField(db_column='close_image', blank=True, null=True, upload_to="images/close/")
    process_id = models.TextField(db_column='process_id', blank=True, null=True)

    android_id = models.ForeignKey('User', models.DO_NOTHING, db_column='android_id', to_field= 'android_id', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mobile_images'

'''
# for height finding using object image height and distance relationship method
class Images(models.Model):
    image_id = models.AutoField(db_column='id_image', primary_key=True)
    original_image = models.ImageField(db_column='image', blank=True, null=True, upload_to="images/original/")
    far_image = models.ImageField(db_column='far_image', blank=True, null=True, upload_to="images/far/")
    distance = models.FloatField(db_column='distance', blank=True, null=True)
    close_image = models.ImageField(db_column='close_image', blank=True, null=True, upload_to="images/close/")
    latitude = models.TextField(db_column='latitude', blank=True, null=True)
    longitude = models.TextField(db_column='longitude', blank=True, null=True)
    date_time = models.TextField(db_column='date_time', blank=True, null=True)

    process_id = models.TextField(db_column='process_id', blank=True, null=True)
    android_id = models.ForeignKey('User', models.DO_NOTHING, db_column='android_id', to_field= 'android_id', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'images'
'''

class HealthResults(models.Model):
    health_results_id = models.AutoField(db_column='id_health_results', primary_key=True)
    height = models.FloatField(db_column='height', blank=True, null=True)
    distance = models.FloatField(db_column='distance', blank=True, null=True)
    biomass = models.FloatField(db_column='biomass', blank=True, null=True)
    carbon_content = models.FloatField(db_column='carbon_content', blank=True, null=True)
    total_carbon_absorbed = models.FloatField(db_column='total_carbon_absorbed', blank=True, null=True)
    original_image = models.ImageField(db_column='original_image', blank=True, null=True, upload_to="images/original/")
    mobile_image_id = models.ForeignKey('MobileImages', models.DO_NOTHING, db_column='id_mobile_image', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'health_results'

# Process model for KMAT
class Processes(models.Model):
    id = models.AutoField(db_column='id_process', primary_key=True)
    description = models.TextField(db_column='description', blank=True, null=True)
    param1 = models.TextField(db_column='param1', blank=True, null=True)
    param2 = models.TextField(db_column='param2', blank=True, null=True)
    param3 = models.TextField(db_column='param3', blank=True, null=True)
    param4 = models.TextField(db_column='param4', blank=True, null=True)
    param5 = models.TextField(db_column='param5', blank=True, null=True)
    result1 = models.TextField(db_column='result1', blank=True, null=True)
    result2 = models.TextField(db_column='result2', blank=True, null=True)
    result3 = models.TextField(db_column='result3', blank=True, null=True)
    process_owner = models.TextField(db_column='process_owner', blank=True, null=True)
    process_id = models.TextField(db_column='process_id', blank=True, null=True)     # Generated at KMAT

    class Meta:
        managed = False
        db_table = 'processes'


class Backup(models.Model):
    backup_id = models.AutoField(db_column='id_backup', primary_key=True)
    android_id = models.CharField(db_column='android_id', max_length=100, blank=True, null=True)
    mobile_image_id = models.IntegerField( db_column='id_mobile_image', blank=True, null=True)
    reference_object_circumference = models.FloatField(db_column='reference_object_circumference', blank=True,
                                                       null=True)
    original_image = models.ImageField(db_column='original_image', blank=True, null=True)
    canopy = models.ImageField(db_column='canopy', blank=True, null=True)
    trunk = models.ImageField(db_column='trunk', blank=True, null=True)
    far_image = models.ImageField(db_column='far_image', blank=True, null=True)
    distance = models.FloatField(db_column='distance', blank=True, null=True)
    close_image = models.ImageField(db_column='close_image', blank=True, null=True)
    latitude = models.TextField(db_column='latitude', blank=True, null=True)
    longitude = models.TextField(db_column='longitude', blank=True, null=True)
    date_time = models.TextField(db_column='date_time', blank=True, null=True)
    height = models.FloatField(db_column='height', blank=True, null=True)
    biomass = models.FloatField(db_column='biomass', blank=True, null=True)
    carbon_content = models.FloatField(db_column='carbon_content', blank=True, null=True)
    total_carbon_absorbed = models.FloatField(db_column='total_carbon_absorbed', blank=True, null=True)
    health_results_id = models.IntegerField(db_column='id_health_results', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'backup'


class Feedback(models.Model):
    feedback_id = models.AutoField(db_column='id_feedback', primary_key=True)
    comment = models.CharField(db_column='comment', max_length=5000, blank=True, null=True)
    email = models.CharField(db_column='email', max_length=100, blank=True, null=True)
    android_id = models.CharField(db_column='android_id', max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feedback'


'''
# Not in use
class UserMobile(models.Model):
    user_mobile_id = models.AutoField(db_column='id_user_mobile', primary_key=True)
    screen_width = models.TextField(db_column='screen_width', blank=True, null=True)
    screen_height = models.TextField(db_column='screen_height', blank=True, null=True)

    android_id = models.ForeignKey('User', models.DO_NOTHING, db_column='android_id',  blank=True, null=True)

    ########### Not needed for current method ##########
    # imei_number = models.IntegerField(db_column='imei_number',  blank=True, null=True, unique=False) # Inaccessible
    # object_known_distance = models.FloatField(db_column='object_known_distance', blank=True, null=True)
    # object_known_width = models.FloatField(db_column='object_known_width', blank=True, null=True)
    # object_apparent_width = models.FloatField(db_column='object_apparent_width', blank=True, null=True)
    # mobile_focal_length = models.FloatField(db_column='mobile_focal_length', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users_mobile'
'''

# Based on the view 'user_history_view' created in DB
'''
class UserHistory(models.Model):
    # id = models.BigIntegerField(primary_key=True)
    user_id = models.IntegerField(db_column='id_user')
    android_id = models.CharField(db_column='android_id', max_length=100,)
    image = models.ImageField(db_column='image')
    # carbon_content = models.FloatField(db_column='carbon_content', blank=True, null=True)
    # total_carbon_absorbed = models.FloatField(db_column='total_carbon_absorbed', blank=True, null=True)
    # mobile_image_id = models.ForeignKey('MobileImages', models.DO_NOTHING, db_column='id_mobile_image', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_history_view'

'''