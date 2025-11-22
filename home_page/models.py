from django.db import models


# --- SWIPER ---
class SwiperItem(models.Model):
    name = models.JSONField()
    title = models.JSONField()
    href = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to="swiper/", blank=True, null=True)

    def __str__(self):
        return self.name.get("en", "Swiper Item")


# --- FEATURE ---
class Feature(models.Model):
    order = models.PositiveIntegerField(default=0)
    name_ru = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    name_tj = models.CharField(max_length=255)
    description_ru = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    description_tj = models.TextField(blank=True)
    image = models.ImageField(upload_to="features/", blank=True, null=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name_en


# --- WHY US ---
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


# --- STATISTICS ---
class Stat(models.Model):
    order = models.PositiveIntegerField(default=0)
    number = models.CharField(max_length=50)
    title_ru = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    title_tj = models.CharField(max_length=255)
    image = models.ImageField(upload_to="stats/", blank=True, null=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.number


# --- PARTNER ---
class Partner(models.Model):
    order = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="partners/", blank=True, null=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Partner #{self.pk}"


# --- TESTIMONIAL ---
class Testimonial(models.Model):
    order = models.PositiveIntegerField(default=0)
    video = models.CharField(max_length=500, blank=True)
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


# --- GALLERY ---
class GalleryItem(models.Model):
    order = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="gallery/", blank=True, null=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Gallery #{self.pk}"


# --- COURSE ---
class Course(models.Model):
    order = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="courses/", blank=True, null=True)
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


# --- INFO SWIPER ---
class InfoSwiperItem(models.Model):
    order = models.PositiveIntegerField(default=0)
    title_ru = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    title_tj = models.CharField(max_length=255)
    description_ru = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    description_tj = models.TextField(blank=True)
    background_image = models.ImageField(upload_to="info_swiper/", blank=True, null=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title_en
