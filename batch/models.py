from django.db import models
from django.utils import timezone

# Create your models here.


class BatchModel(models.Model):
    INFORMATION_SCIENCE = 'ISE'
    COMPUTER_SCIENCE = 'CSE'
    DEPARTMENT = (
        (INFORMATION_SCIENCE, 'Information Science Engg.'),
        (COMPUTER_SCIENCE, 'Computer Science Engg.'),
    )

    YEAR_CHOICES = [(2015, 2015), (2016, 2016), (2017, 2017),
                    (2018, 2018), (2019, 2019), (2020, 2020)]


    A_SECTION = "A"
    B_SECTION = "B"
    C_SECTION = "C"
    D_SECTION = "D"

    SECTION = (
        (A_SECTION, "A Section"),
        (B_SECTION, "B Section"),
        (C_SECTION, "C Section"),
        (D_SECTION, "D Section"),
    )


    department = models.CharField(max_length=3, choices=DEPARTMENT)
    year = models.IntegerField(choices=YEAR_CHOICES, help_text="Year of joining college")
    section = models.CharField(max_length = 1, choices=SECTION)

    class Meta:
        verbose_name = "Batch"
        verbose_name_plural = "Batches"
        unique_together = ('department', 'year', 'section')

    def get_year(self):
        year = timezone.now().year - self.year + 1
        if(year == 1):
            suffix = "st"
        elif(year == 2):
            suffix = "nd"
        elif(year == 3):
            suffix = "rd"
        else:
            suffix = "th"
        return str(year) + suffix + " year"

    def __str__(self):
        return self.department + " " + self.get_year() + " " + self.section + " section"
