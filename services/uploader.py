

class Uploader:

    @staticmethod
    def blog_category(instance, filename):
        return f"Blog_Category/{instance.title}/{filename}"

