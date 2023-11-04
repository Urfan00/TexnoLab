

class Uploader:

    @staticmethod
    def blog_category(instance, filename):
        return f"Blog_Category/{instance.title}/{filename}"

    @staticmethod
    def service_image(instance, filename):
        return f"Service/{instance.service.title}/{filename}"

    @staticmethod
    def service_image_home(instance, filename):
        return f"Service-Home/{instance.title}/{filename}"

    @staticmethod
    def user_image(instance, filename):
        return f"User_Image/{instance.id_code}/{filename}"

    @staticmethod
    def course_main_photo(instance, filename):
        return f"Course/{instance.title}/Course_main_photo/{filename}"

    @staticmethod
    def course_gallery(instance, filename):
        return f"Course/{instance.title}/Course_Gallery/{filename}"

    @staticmethod
    def partners_image(instance, filename):
        return f"Partners_image/{instance.title}/{filename}"

    @staticmethod
    def about_us(instance, filename):
        return f"About_US/{instance.title}/{filename}"

    @staticmethod
    def course_program(instance, filename):
        return f"Course/{instance.course.title}/Program/{filename}"

    @staticmethod
    def all_galery(instance, filename):
        return f"Galery/{filename}"
