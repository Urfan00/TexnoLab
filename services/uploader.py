

import os


class Uploader:

    @staticmethod
    def blog_category(instance, filename):
        return f"Blog/{instance.title}/{filename}"

    @staticmethod
    def service_image(instance, filename):
        return f"Service/{instance.service.title}/{filename}"

    @staticmethod
    def tim_image(instance, filename):
        return f"TIM/TIM-Image/{filename}"

    @staticmethod
    def service_image_home(instance, filename):
        return f"Service-Home/{instance.title}/{filename}"

    @staticmethod
    def user_cv(instance, filename):
        return f"User_Image/{instance.id_code}/CV/{filename}"

    @staticmethod
    def certificate(instance, filename):
        return f"Certificate/{filename}"

    @staticmethod
    def user_image(instance, filename):
        return f"User_Image/{instance.id_code}/{filename}"

    @staticmethod
    def course_main_photo(instance, filename):
        return f"Course/{instance.title}/{filename}"

    @staticmethod
    def course_gallery(instance, filename):
        return f"Course/{instance.course.title}/Course_Gallery/{filename}"

    @staticmethod
    def partners_image(instance, filename):
        return f"Partners_image/{instance.title}/{filename}"

    @staticmethod
    def about_us(instance, filename):
        return f"About_US/{filename}"

    @staticmethod
    def course_program(instance, filename):
        return f"Course/{instance.course.title}/Program/{filename}"

    @staticmethod
    def all_galery(instance, filename):
        return f"Galery/{filename}"

    @staticmethod
    def question_image(instance, filename):
        return f"Question_Image/{instance.course_topic_test.name}/{instance.pk}/{filename}"

    @staticmethod
    def get_file_extension(file_name):
        _, file_extension = os.path.splitext(file_name)
        return file_extension
