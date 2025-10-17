from django.db import models
import uuid
import datetime

class AllDjangoFields(models.Model):
    # Numeric fields
    auto_field = models.AutoField(primary_key=True)
    big_auto_field = models.BigAutoField()
    integer_field = models.IntegerField(default=0)
    small_integer_field = models.SmallIntegerField(default=0)
    positive_small_integer_field = models.PositiveSmallIntegerField(default=0)
    positive_integer_field = models.PositiveIntegerField(default=0)
    big_integer_field = models.BigIntegerField(default=0)
    big_integer_field = models.PositiveBigIntegerField(default=0)
    float_field = models.FloatField(default=0.0)
    decimal_field = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # String/Text fields
    char_field = models.CharField(max_length=255)
    text_field = models.TextField()
    slug_field = models.SlugField(unique=True)
    email_field = models.EmailField() #[name]@[domain].[tld]
    url_field = models.URLField()
    file_path_field = models.FilePathField(path="/tmp", blank=True, null=True)
    uuid_field = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    # Date and time fields
    date_field = models.DateField(default=datetime.date.today)
    time_field = models.TimeField(default=datetime.datetime.now)
    datetime_field = models.DateTimeField(auto_now_add=True)
    duration_field = models.DurationField(default=datetime.timedelta)

    # Boolean fields
    boolean_field = models.BooleanField(default=False)
    null_boolean_field = models.BooleanField(null=True)

    # File/Image fields
    file_field = models.FileField(upload_to='files/', blank=True, null=True)
    image_field = models.ImageField(upload_to='images/', blank=True, null=True)

    # Relationship fields
    foreign_key_field = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='fk_examples')
    one_to_one_field = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='oto_examples')
    many_to_many_field = models.ManyToManyField('auth.Group', blank=True)
    # one_to_many
    # many_to_one
    # Other special fields 
    generic_ip_address_field = models.GenericIPAddressField(protocol='both', unpack_ipv4=False, null=True, blank=True)
    binary_field = models.BinaryField(blank=True, null=True)
    json_field = models.JSONField(default=dict, blank=True, null=True)

    class Meta:
        ordering = ['-datetime_field']
        indexes = [models.Index(fields=['slug_field'])]

    def __str__(self):
        return f"All Fields Example #{self.auto_field}"




class Example(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        null=False,
        blank=False,
        default="Untitled",
        db_index=True,
        verbose_name="Full Name",
        help_text="Enter full name",
        validators=[],
        error_messages={'unique': 'This name already exists.'}
    )

    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='examples',
        related_query_name='example',
        limit_choices_to={'is_staff': True}
    )

    created_at = models.DateTimeField(auto_now_add=True)
