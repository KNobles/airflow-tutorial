class Property:
    def __init__(self, json_obj) -> None:
        self.property_data = json_obj
        self.id = self.id()
        self.locality = self.locality()
        self.postal_code = self.postal_code()
        self.province = self.province()
        self.region = self.region()
        self.type = self.type()
        self.sub_type = self.sub_type()
        self.sale_type = self.sale_type()
        self.price = self.price()
        self.bedroom_count = self.bedroom_count()
        self.surface = self.surface()
        self.is_kitchen_fully_equipped = self.is_kitchen_fully_equipped()
        self.kitchen_type = self.kitchen_type()
        self.is_furnished = self.is_furnished()
        self.has_open_fire = self.has_open_fire()
        self.has_terrace = self.has_terrace()
        self.has_garden = self.has_garden()
        self.terrace_surface = self.terrace_surface()
        self.garden_surface = self.garden_surface()
        self.land_surface = self.land_surface()
        self.facade_count = self.facade_count()
        self.has_swimming_pool = self.has_swimming_pool()
        self.building_state = self.building_state()
    
    def id(self):
        property_id = self.property_data["id"]
        return property_id

    def garden_surface(self)-> int:
        garden_surface = self.property_data["property"]["gardenSurface"]
        if garden_surface is None:
            return -1
        return garden_surface

    def terrace_surface(self)-> int:
        terrace_surface = self.property_data["property"]["terraceSurface"]
        if terrace_surface is None:
            return -1
        return terrace_surface

    def has_terrace(self)-> int:
        has_terrace = self.property_data["property"]["hasTerrace"]
        val = self.convert_boolean(has_terrace)
        return val

    def has_open_fire(self)-> int:
        has_open_fire = self.property_data["property"]["fireplaceExists"]
        val = self.convert_boolean(has_open_fire)
        return val

    def is_furnished(self)-> int:
        is_furnished = self.property_data["transaction"]["sale"]["isFurnished"]
        val = self.convert_boolean(is_furnished)
        return val

    def has_garden(self)-> int:
        has_garden = self.property_data["property"]["hasGarden"]
        val = self.convert_boolean(has_garden)
        return val

    def is_kitchen_fully_equipped(self)-> int:
        try:
            is_kitchen_fully_equipped = self.property_data["property"]["kitchen"]["type"]
            if is_kitchen_fully_equipped is None:
                is_kitchen_fully_equipped = -1
            elif is_kitchen_fully_equipped == "HYPER_EQUIPPED" or is_kitchen_fully_equipped == "USA_HYPER_EQUIPPED":
                is_kitchen_fully_equipped = 1
        except TypeError:
            is_kitchen_fully_equipped = -1
        return is_kitchen_fully_equipped

    def has_swimming_pool(self)-> int:
        has_swimming_pool = self.property_data["property"]["hasSwimmingPool"]
        val = self.convert_boolean(has_swimming_pool)
        return val

    def surface(self):
        surface = self.property_data["property"]["netHabitableSurface"]
        if surface is None:
            surface = -1
        return surface

    def price(self):
        price = self.property_data["price"]["mainValue"]
        if price is None:
            price = -1
        return price

    def sale_type(self):
        sale_type = self.property_data["price"]["type"]
        if sale_type is None:
            sale_type = "NO_INFO"
        return sale_type
    
    def sub_type(self):
        sub_type = self.property_data["property"]["subtype"]
        if sub_type is None:
            sub_type = "NO_INFO"
        return sub_type

    def type(self):
        type = self.property_data["property"]["type"]
        if type is None:
            type = "NO_INFO"
        return type

    def locality(self):
        locality = self.property_data["property"]["location"]["locality"]
        if locality is None:
            locality = "NO_INFO"
        return locality
    
    def postal_code(self)-> int:
        postal_code = self.property_data["property"]["location"]["postalCode"]
        if postal_code is None:
            return -1
        return postal_code

    def province(self):
        province = self.property_data["property"]["location"]["province"]
        if province is None:
            return "NO_INFO"
        return province

    def region(self):
        region = self.property_data["property"]["location"]["region"]
        if region is None:
            region = "NO_INFO"
        return region

    def bedroom_count(self)-> int:
        bedroom_count = self.property_data["property"]["bedroomCount"]
        if bedroom_count is None:
            bedroom_count = -1
        return bedroom_count

    def land_surface(self)-> int:
        try:
            land_surface = self.property_data["property"]["land"]["surface"]
            if land_surface is None:
                land_surface = -1
        except TypeError:
            land_surface = -1
        return land_surface

    def building_state(self):
        try:
            building_state = self.property_data["property"]["building"]["condition"]
            if building_state is None:
                building_state = "NO_INFO"
        except TypeError:
            building_state = "NO_INFO"
        return building_state

    def facade_count(self)-> int:
        try:
            facade_count = self.property_data["property"]["building"]["facadeCount"]
            if facade_count is None:
                facade_count = -1
        except TypeError:
            facade_count = -1
        return facade_count

    def kitchen_type(self):
        try:
            has_kitchen = self.property_data["property"]["kitchen"]["type"]
            if has_kitchen is None:
                has_kitchen = "NO_INFO"
        except TypeError:
            has_kitchen = "NO_INFO"
        return has_kitchen
    
    def convert_boolean(self, answer)-> int:
        match answer:
            case True: return 1
            case False: return 0
            case None: return -1