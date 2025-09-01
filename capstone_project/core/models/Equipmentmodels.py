# Predefined choices for usage domains and support phases
USAGE_DOMAINS = [
    ('Electronics', 'Electronics'),
    ('Mechanical', 'Mechanical'),
    ('IoT', 'IoT'),
    # Add more if needed based on project needs
]

SUPPORT_PHASES = [
    ('Training', 'Training'),
    ('Prototyping', 'Prototyping'),
    ('Testing', 'Testing'),
    ('Commercialization', 'Commercialization'),
]

class Equipment(models.Model):
    equipment_id = models.AutoField(primary_key=True)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='equipments')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    capabilities = models.CharField(max_length=200, blank=True)  # free text field; you can store comma-separated capabilities, e.g., 'CNC,PCB Fabrication'
    inventory_code = models.CharField(max_length=100, blank=True)
    usage_domain = models.CharField(max_length=50, choices=USAGE_DOMAINS, blank=True)
    support_phase = models.CharField(max_length=50, choices=SUPPORT_PHASES, blank=True)

    def __str__(self):
        return self.name