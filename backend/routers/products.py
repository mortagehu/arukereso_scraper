from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..scraping import scrape_product_prices
from ..models import Product, PriceHistory

router = APIRouter(prefix="/products", tags=["products"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/search")
def search_products(query: str, db: Session = Depends(get_db)):
    scraped_data = scrape_product_prices(query)
    results = []

    for item in scraped_data:
        product = db.query(Product).filter(Product.name == item["name"]).first()
        if not product:
            product = Product(name=item["name"], category="unknown", url="")
            db.add(product)
            db.commit()
            db.refresh(product)

        price_history = PriceHistory(product_id=product.id, price=item["price"])
        db.add(price_history)
        db.commit()

        results.append({"name": item["name"], "current_price": item["price"]})

    return results
