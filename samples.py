
def storage_sample():
    return """

Resource: Azure Storage Container
Name Prefix: kastrube
Terraform: 
    resource "azurerm_resource_group" "kastrube" {{
    name     = "kastrube-resources"
    location = "West Europe"
    }}

    resource "azurerm_storage_account" "kastrube" {{
    name                     = "kastrubestoraccount"
    resource_group_name      = azurerm_resource_group.example.name
    location                 = azurerm_resource_group.example.location
    account_tier             = "Standard"
    account_replication_type = "LRS"

    tags = {{
        environment = "Test"
    }}
    }}

    resource "azurerm_storage_container" "kastrube" {{
    name                  = "vhds"
    storage_account_name  = azurerm_storage_account.example.name
    container_access_type = "private"
    }}

"""


def cosmos_sample():
    return """

Resource: Azure CosmosDb Account 
Name Prefix: phil
Terraform: 
    resource "azurerm_resource_group" "phil" {{
    name     = "phil-resource-group"
    location = "West Europe"
    }}

    resource "azurerm_cosmosdb_account" "db" {{
    name                = "tfex-cosmos-db-3242"
    location            = azurerm_resource_group.example.location
    resource_group_name = azurerm_resource_group.example.name
    offer_type          = "Standard"
    kind                = "MongoDB"

    enable_automatic_failover = true

    capabilities {{
        name = "EnableAggregationPipeline"
    }}

    capabilities {{
        name = "mongoEnableDocLevelTTL"
    }}

    capabilities {{
        name = "MongoDBv3.4"
    }}

    capabilities {{
        name = "EnableMongo"
    }}

    consistency_policy {{
        consistency_level       = "BoundedStaleness"
        max_interval_in_seconds = 300
        max_staleness_prefix    = 100000
    }}

    geo_location {{
        location          = "eastus"
        failover_priority = 1
    }}

    geo_location {{
        location          = "westus"
        failover_priority = 0
    }}
    }}

"""