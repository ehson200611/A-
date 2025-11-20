from django.db import models

# Option: change to ImageField if you want uploads (requires Pillow)
def optional_image_field(max_length=255):
    return models.CharField(max_length=max_length, blank=True, null=True)

from django.db import models

class SwiperItem(models.Model):
    name = models.JSONField()
    title = models.JSONField()
    href = models.CharField(max_length=255, blank=True)
    image = models.CharField(max_length=255)

    def __str__(self):
        return self.name.get("en", "Swiper Item")


class Feature(models.Model):
    order = models.PositiveIntegerField(default=0)
    name_ru = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    name_tj = models.CharField(max_length=255)
    description_ru = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    description_tj = models.TextField(blank=True)
    image = optional_image_field()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name_en

class WhyUsItem(models.Model):
    order = models.PositiveIntegerField(default=0)
    icon = models.CharField(max_length=100, blank=True)
    text_ru = models.TextField()
    text_en = models.TextField()
    text_tj = models.TextField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"WhyUs #{self.pk}"

class Stat(models.Model):
    order = models.PositiveIntegerField(default=0)
    number = models.CharField(max_length=50)
    title_ru = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    title_tj = models.CharField(max_length=255)
    image = optional_image_field()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.number

class Partner(models.Model):
    order = models.PositiveIntegerField(default=0)
    image = optional_image_field()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Partner #{self.pk}"

class Testimonial(models.Model):
    order = models.PositiveIntegerField(default=0)
    video = models.CharField(max_length=500, blank=True)
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

class GalleryItem(models.Model):
    order = models.PositiveIntegerField(default=0)
    image = optional_image_field()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Gallery #{self.pk}"

class Course(models.Model):
    order = models.PositiveIntegerField(default=0)
    image = optional_image_field()
    title_ru = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    title_tj = models.CharField(max_length=255)
    description_ru = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    description_tj = models.TextField(blank=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title_en

class InfoSwiperItem(models.Model):
    order = models.PositiveIntegerField(default=0)
    title_ru = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    title_tj = models.CharField(max_length=255)
    description_ru = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    description_tj = models.TextField(blank=True)
    background_image = optional_image_field()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title_en
