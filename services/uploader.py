

class Uploader:

    @staticmethod
    def blog_category(instance, filename):
        return f"Blog_Category/{instance.title}/{filename}"

    @staticmethod
    def service_image(instance, filename):
        return f"Service/{instance.service.title}/{filename}"

    @staticmethod
    def user_image(instance, filename):
        return f"User_Image/{instance.id_code}/{filename}"
