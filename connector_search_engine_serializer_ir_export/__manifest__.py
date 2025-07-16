{
    "name": "Connector Search Engine Serializer Ir Export",
    "summary": "Use Exporter (ir.exports) as serializer for index",
    "version": "17.0.1.0.0",
    "development_status": "Alpha",
    "category": "Uncategorized",
    "website": "https://github.com/OCA/search-engine",
    "author": "Akretion, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "external_dependencies": {
        "python": [],
        "bin": []
    },
    "depends": [
        "connector_search_engine",
        "jsonifier"
    ],
    "data": [
        "views/se_index_view.xml"
    ],
    "demo": [],
    "installable": True
}
