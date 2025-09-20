from django.db import models


class ChannelEnumChoices(models.TextChoices):
    SMS = "SMS"
    EMAIL = "EMAIL"
    WHATSAPP = "WHATSAPP"


class RuleStatusEnumChoices(models.TextChoices):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class Charge(BaseModel):
    customer_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.customer_name


class Installment(BaseModel):
    charge = models.ForeignKey(
        Charge, on_delete=models.CASCADE, related_name="installments"
    )
    number = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=5)
    due_date = models.DateField()
    payment_link = models.CharField(max_length=255, null=True, blank=True)
    barcode_line = models.CharField(max_length=255, null=True, blank=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.charge.customer_name} - Parcela {self.number}"


class Rule(BaseModel):
    name = models.CharField(max_length=100)
    status = models.CharField(
        max_length=10,
        choices=RuleStatusEnumChoices,
        default=RuleStatusEnumChoices.ENABLED,
    )

    def __str__(self):
        return self.name


class Template(BaseModel):
    name = models.CharField(max_length=100)
    channel = models.CharField(max_length=10, choices=ChannelEnumChoices, default="")
    content = models.TextField()

    def __str__(self):
        return self.name


class RuleStep(BaseModel):
    rule = models.ForeignKey(Rule, on_delete=models.CASCADE, related_name="steps")
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    channel = models.CharField(
        max_length=10, choices=ChannelEnumChoices, default=ChannelEnumChoices.SMS
    )
    day_offset = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.rule.name} - Step {self.id}"
