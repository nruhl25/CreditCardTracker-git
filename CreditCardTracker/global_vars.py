def reload_category_keys():
    with open("categories.txt", "r") as f:
        category_keys = f.readlines()
        category_keys = [key.strip() for key in category_keys]
    return category_keys

def reload_vendorIDs(category_keys):
    all_vendorIDs = []
    for category in category_keys:

        with open(f"VendorIDs/{category}.txt", "r") as f:
            vendorIDs = f.readlines()
            vendorIDs = [vendor.strip() for vendor in vendorIDs]

        for vendorID in vendorIDs:
            all_vendorIDs.append(vendorID)
    return all_vendorIDs

months = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]
