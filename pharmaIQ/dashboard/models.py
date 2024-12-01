from django.db import models
from django.core.validators import MinValueValidator  
from datetime import date 
from datetime import timedelta

class Drug(models.Model):
    class Pp_gn(models.TextChoices):
        GENERIC = 'GN', 'Générique'
        OWNED = 'PP', 'Produit Propriétaire'

    class StatutAMM(models.TextChoices):
        ENREGISTREE = 'AMME', 'AMM Enregistrée'
        RETIREE = 'AMMR', 'AMM Retirée'

    class StatutCommercialisation(models.TextChoices):
        COMMERCIALISE = 'C', 'Commercialisé'
        NON_COMMERCIALISE = 'NC', 'Non Commercialisé'
        RETIRE_DU_MARCHE = 'RM', 'Retiré du Marché'
        COMMERCIALISE_APPEL_D_OFFRE = 'C/AO', 'Commercialisé / appel d offre'
    name = models.CharField(max_length=100, null=False, blank=False)
    dosage = models.CharField(max_length=100, null=False, blank=False) # exp: 500mg, 1000mg, etc.
    form = models.CharField(max_length=100, null=False, blank=False) # exp: comprimé, sachet, etc.
    substances = models.CharField(max_length=200, null=False, blank=False) # exp: paracétamol & Cafeine, ibuprofène, etc.
    statutAMM = models.CharField(choices=StatutAMM.choices, max_length=4, null=False, blank=False) # Autorisation de Mise sur le Marché
    statutCommercialisation = models.CharField(choices=StatutCommercialisation.choices, max_length=4, null=False, blank=False) # commercialisé ou non
    presentation = models.CharField(max_length=100, null=False, blank=False) # exp: boite de 10 comprimés
    pp_gn = models.CharField(choices=Pp_gn.choices, max_length=2, null=False, blank=False) # générique ou produit propriétaire
    class_therapeutique = models.CharField(max_length=250, null=False, blank=False)
    EPI = models.CharField(max_length=150, null=False, blank=False)  # Etablissement Pharmaceutique Industriel
    PPV = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False) # Prix Public de Vente
    PH = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False) # prix hopital
    PFHT = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False) # Prix Fabricant Hors Taxe
    code_ATC = models.CharField(max_length=10, null=False, blank=False) # Code ATC
    TVA = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True) # Taux de la TVA
    def __str__(self):
        return f"{self.id} - {self.name} - {self.dosage} {self.form} - {self.class_therapeutique} ({self.presentation})"
    def update_drug_status(self, statutAMM, statutCommercialisation ):
        self.statutAMM = statutAMM
        self.statutCommercialisation = statutCommercialisation
        self.save()
        
    def update_presentation(self, presentation):
        self.presentation = presentation
        self.save()
        
    def update_EPI(self, EPI):
        self.EPI = EPI
        self.save()
        
    def getMedGroup(self):
        return self.class_therapeutique
    
    def update_price(self, PFHT, PH, PPV , TVA ):
        correct_data = True
        correct_data = ( PFHT < PPV ) and ( PH > PFHT )
        for data in [PFHT, PH, PPV , TVA ]:
            if data <= 0:
                correct_data =False
        if correct_data:
            self.PFHT = PFHT
            self.PH = PH
            self.PPV = PPV
            self.TVA = TVA
            self.save()
    def checkAllTimeSales(self):
        # the process
        return 0
    
    def checkSales(self, start_date: date, end_date: date):
        # the process 
        return 0

class Stock(models.Model):
    # The PROTECT option in on_delete prevents the deletion of a Drug instance
    drug = models.ForeignKey(Drug, on_delete=models.PROTECT)
    
    level = models.IntegerField(validators=[MinValueValidator(0)], null=False, blank=False, default=0)
    reorderPoint = models.IntegerField(validators=[MinValueValidator(0)], null=False, blank=False, default=10)
    lastReorderDate = models.DateField(null=True, blank=True)
    class SellingSpeed(models.TextChoices):
        VERY_SLOW = 'VS', 'Very Slow'
        SLOW = 'S', 'Slow'
        MEDIUM = 'M', 'Medium'
        FAST = 'F', 'Fast'
        VERY_FAST = 'VF', 'Very Fast'
        
    sellingSpeed = models.CharField(max_length=2, choices=SellingSpeed.choices, default=SellingSpeed.SLOW, null=False, blank=False)
    
    def getStockLevel(self):
        return self.level
    
    def getLastReorderDate(self):
        return self.lastReorderDate
    
    def updateStockLevel(self, refill_quantity):
        self.level += refill_quantity
        self.save()
        
    def updateLastReorderDate(self):
        self.lastReorderDate = date.today()
        self.save()
        
    def checkShortage(self):
        return self.level > self.reorderPoint 
    
    def isOutOFStock(self):
        return self.level <= self.reorderPoint
    def predict(self):
        # the process 
        return 0
    
    @staticmethod
    def countOutOfStock():
        """Static method to count all out-of-stock items"""
        return Stock.objects.filter(level__lte=models.F('reorderPoint')).count()
    
    def archiveWeek(self):
        # the process 
        return 0
    
    @staticmethod
    def countOutOfStock():
        """Static method to count all out-of-stock items"""
        return Stock.objects.filter(level__lte=models.F('reorderPoint')).count()
    def __str__(self):
        return f"Stock of {self.drug.name} - Level: {self.level} - Reorder Point: {self.reorderPoint} - Last Reorder Date: {self.lastReorderDate} - Selling Speed: {self.sellingSpeed}"

class Sale(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.PROTECT)
    
    quantity = models.IntegerField()
    date = models.DateField()
    time = models.TimeField()


    def get_total(self):
        return float(self.drug.PPV) * self.quantity

    def getDrugName(self):
        return self.drug.name
    
    def __str__(self):
        return f"{self.drug} - quantity: {self.quantity} - on {self.date} - at {self.time} : total = {self.get_total()} DHS"

    def getDrugGroup(self):
        return self.drug.class_therapeutique
    
    
    """
    @staticmethod
    def countLifeTimeSales():
        # Static method to count all out-of-stock items
        totalNumber = 0 
        for sale in Sale.objects.all() :
            totalNumber += sale.quantity 
        return totalNumber
    """
    
    @staticmethod
    def countLifeTimeSales():
        return Sale.objects.count()
    @staticmethod
    def countLifeTimeSalesTotal():
        """Static method to count all out-of-stock items"""
        total = 0 
        for sale in Sale.objects.all() :
            total += sale.get_total()
        return total
    
    @staticmethod
    def getTodaySalesEarnings():
        """Static method to get Todays earnings """
        total = 0 
        for sale in Sale.objects.all().filter(date=date.today()) :
            total += sale.get_total()
        return total
    
    @staticmethod
    def getCategorySales():
        """Static method to get category sales """
        category_sales = {}
        for sale in Sale.objects.all():
            drug = sale.drug
            category = drug.class_therapeutique
            if category in category_sales:
                category_sales[category] += sale.quantity
            else:
                category_sales[category] = sale.quantity
        return category_sales

    @staticmethod
    def getLastThirtyDaysSales():
        """
        Static method to calculate total sales from the last 30 days.
        """
        thirty_days_ago = date.today() - timedelta(days=30)
        sales = Sale.objects.filter(date__gte=thirty_days_ago)
        total_sales = sum(sale.quantity for sale in sales)
        return total_sales
    
class Archive(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.PROTECT)
    
    # sows : start of week stock
    sows = models.IntegerField(validators=[MinValueValidator(0)], null=False, blank=False)
    # eows : end of week stock
    eows = models.IntegerField(validators=[MinValueValidator(0)], null=False, blank=False)
    # sales : total sales of the week
    sales = models.IntegerField(validators=[MinValueValidator(0)], null=False, blank=False)
        
    # sowd : start of week date
    sowd = models.DateField(null=False, blank=False)
    # eowd : end of week date
    eowd = models.DateField(null=False, blank=False)
    
    shortage = models.BooleanField(null=False, blank=False)
    
    
    def __str__(self):
        return f"Archive of {self.stock.drug.name} - from {self.sowd} to {self.eowd} : start of week stock = {self.sows} - end of week stock = {self.eows} - {self.sales} items sold - shortage = {self.shortage}"

class Report(models.Model):
    date = models.DateField(null=False, blank=False)
    time = models.TimeField(null=False, blank=False)
    # Store shortages as a JSON array
    shortages = models.JSONField()  

    # Store sales and stock predictions as JSON objects
    sales = models.JSONField()  # for dictionaries
    stock_predictions = models.JSONField()
    
    url = models.URLField(blank=True, null=True)
    
    def generateReport(self):
        # the process 
        self.url = "" #the generated report path
        return 0
    
class Alert(models.Model):
    
    class Severity(models.TextChoices):
        LOW = 'L', 'Low'
        MEDIUM = 'M', 'Medium'
        HIGH = 'H', 'High'
    
    class Message(models.TextChoices):
        OUTOFSTOCK = 'OS', 'Medicines possibly out of stock in the next week'
        SHORTAGES = 'SH', 'Medicines currently in shortage'
        POSSIBLESHORTAGES = 'PS', 'Medicines possibly in shortage next week'

    message = models.CharField(choices=Message.choices, max_length=2, null=False, blank=False)
    severity = models.CharField(choices=Severity.choices, max_length=1, null=False, blank=False)
    date = models.DateField(null=False, blank=False)
    time = models.TimeField(null=False, blank=False)
    data = models.JSONField()
    total = models.IntegerField(validators=[MinValueValidator(0)], null=False, blank=False)
    
    def __str__(self):
        return f"{self.total} {self.message} - severity: {self.severity}"
