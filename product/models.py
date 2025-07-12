from django.db import models


class Product(models.Model):
    uploader_id = models.CharField(max_length=128)  # Firebase UID
    title = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    condition = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Info(models.Model):
    PROVINCE_CHOICES = [
        ("Koshi Province", "Koshi Province"),
        ("Madhesh Province", "Madhesh Province"),
        ("Bagmati Province", "Bagmati Province"),
        ("Gandaki Province", "Gandaki Province"),
        ("Lumbini Province", "Lumbini Province"),
        ("Karnali Province", "Karnali Province"),
        ("Sudurpashchim Province", "Sudurpashchim Province"),
    ]

    JOB_CHOICES = [
        ("Student", "Student"),
        ("Seller", "Seller"),
        ("Engineer", "Engineer"),
        ("Doctor", "Doctor"),
        ("Teacher", "Teacher"),
        ("Artist", "Artist"),
        ("Developer", "Developer"),
        ("Farmer", "Farmer"),
        ("Businessperson", "Businessperson"),
        ("Others", "Others"),
    ]

    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200, choices=PROVINCE_CHOICES)
    job = models.CharField(max_length=50, choices=JOB_CHOICES)
    profile_picture = models.ImageField(upload_to="info/")

    def __str__(self):
        return self.name


class Comments(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    name = models.ForeignKey(Info, on_delete=models.CASCADE)
    review = models.CharField(max_length=200)

    def __str__(self):
        return f"Comment by {self.name.name} on {self.product.title}"