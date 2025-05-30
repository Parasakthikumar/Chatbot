schema_docs = {
    "Departments": (
        "The Departments table holds information about different departments "
        "within the company. Each department has a unique ID, a name, and the "
        "name of the department head responsible for operations."
    ),
    "Employees": (
        "This table stores details about employees, including their unique ID, "
        "full name, official email, job title, date of joining, and which "
        "department they belong to. It is used to manage employee records and roles."
    ),
    "Assets": (
        "Assets table contains all company assets information such as asset tag, "
        "name, category (e.g., laptop, furniture), physical location, purchase date, "
        "warranty expiry date, current status (active, retired), the department that owns "
        "the asset, and the employee to whom the asset is assigned."
    ),
    "Maintenance_Logs": (
        "This table records all maintenance activities related to assets. Each "
        "log entry includes a unique maintenance log ID, references the asset ID, "
        "details the issue reported, current maintenance status, who reported the issue, "
        "the technician responsible for fixing it, and the resolution date. It helps track "
        "asset condition and ensures timely maintenance."
    ),
    "Vendors": (
        "The Vendors table keeps information about vendors providing services or "
        "products to the company. It includes vendor name, contact person, email, phone number, "
        "and physical address to facilitate communication and contract management."
    ),
    "Asset_Vendor_Link": (
        "This is a linking table that maps company assets to their respective vendors. "
        "It specifies the type of service the vendor provides for each asset and records "
        "the date of the last service performed, helping manage vendor relationships and service history."
    )
}
