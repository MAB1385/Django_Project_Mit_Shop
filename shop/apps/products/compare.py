class CompareProduct:
    def __init__(self, request) -> None:
        self.session = request.session
        compare_product = self.session.get("compare_product")
        if not compare_product:
            compare_product = self.session["compare_product"] = []
        self.compare_product = compare_product
        self.count = len(self.compare_product)
        self.max_product = 4

    def __iter__(self):
        compare_product = self.compare_product.copy()
        for item in compare_product:
            yield item

    def add_to_compare_product(self, productId):
        productId = int(productId)
        if productId not in self.compare_product:
            if not self.count >= self.max_product:
                self.compare_product.append(productId)
                self.count = len(self.compare_product)
                self.session.modified = True
                return "به لیست مقایسه افزوده شد"
            else:
                return "لیست مقایسه پر شده است"
        else:
            return "در لیست مقایسه موجود هست"

    def delete_from_compare_product(self, productId):
        self.compare_product.remove(int(productId))
        self.count = len(self.compare_product)
        self.session.modified = True

    def clear_compare_product(self):
        del self.session["compare_product"]
        self.session.modified = True
