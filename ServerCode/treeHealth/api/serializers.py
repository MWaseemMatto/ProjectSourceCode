from rest_framework import serializers
from treeHealth.models import (
    User,
    MobileImages,

    HealthResults,
    Processes,
    Backup,
    Feedback,

)


class UserSerializer (serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ('name', 'field_of_interest', 'organization')
        fields = '__all__'


class MobileImagesSerializer (serializers.ModelSerializer):

    # image = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = MobileImages
        fields = '__all__'



class HealthResultsSerializer (serializers.ModelSerializer):
    class Meta:
        model = HealthResults
        fields = '__all__'
        #  fields={'height', 'biomass', 'id_mobile_image'}


class ProcessSerializer (serializers.ModelSerializer):
    class Meta:
        model = Processes
        fields = '__all__'


class BackupSerializer (serializers.ModelSerializer):
    class Meta:
        model = Backup
        fields = '__all__'

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'


'''
class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension
'''
'''
class UserMobileSerializer (serializers.ModelSerializer):
    class Meta:
        model = UserMobile
        fields = '__all__'
        # fields=['imei_number','mobile_focal_length']

'''

