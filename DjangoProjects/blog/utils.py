from uuid import uuid4
import os


class Utils(object):
    """ Utils Class """

    @staticmethod
    def rename_image_article_images(obj, filename):
        """ Rename image and path """

        upload_to = 'blog/static/blog/img/articles'
        ext = filename.split('.')[-1]
        filename = '{}.{}'.format(uuid4().hex, ext)

        return os.path.join(upload_to, filename)
