

class Uploader:

    @staticmethod
    def blog_category(instance, filename):
        return f"Blog_Category/{instance.title}/{filename}"

    @staticmethod
    def service_image(instance, filename):
        return f"Service/{instance.service.title}/{filename}"
