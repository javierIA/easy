from sqlalchemy import null
import db.controllers.clientsController as clientsController
import db.controllers.providersController as proviversController
import db.controllers.invoicesController as invoicesController
import db.controllers.itemsController as itemsController
import db.models.invoice as invoice

def main():


    insert_invoice = itemsController.add_item(desc="TestDATA", quant=3, mes="Testdata", cost=80.5, nom="1")
if __name__ == '__main__':

    main()