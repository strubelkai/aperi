
def storage_sample():
    return """
Cloud: Azure
Resource: Storage Container
Name Prefix: kastrube
Terraform: 

    provider "azurerm" {{
        subscription_id = "${{var.subscription_id}}"
        client_id       = "${{var.client_id}}"
        client_secret   = "${{var.client_secret}}"
        tenant_id       = "${{var.tenant_id}}"
    }}

    resource "azurerm_resource_group" "kastrube" {{
    name     = "kastrube-resources"
    location = "West Europe"
    }}

    resource "azurerm_storage_account" "kastrube" {{
    name                     = "kastrubestoraccount"
    resource_group_name      = azurerm_resource_group.kastrube.name
    location                 = azurerm_resource_group.kastrube.location
    account_tier             = "Standard"
    account_replication_type = "LRS"

    tags = {{
        environment = "Test"
    }}
    }}

    resource "azurerm_storage_container" "kastrube" {{
    name                  = "vhds"
    storage_account_name  = azurerm_storage_account.kastrube.name
    container_access_type = "private"
    }}

"""


def cosmos_sample():
    return """
Cloud: Azure
Resource: CosmosDb Account 
Name Prefix: phil
Terraform: 
    provider "azurerm" {{
        subscription_id = "${{var.subscription_id}}"
        client_id       = "${{var.client_id}}"
        client_secret   = "${{var.client_secret}}"
        tenant_id       = "${{var.tenant_id}}"
    }}


    resource "azurerm_resource_group" "phil" {{
        name     = "phil-resource-group"
        location = "West Europe"
    }}

    resource "azurerm_cosmosdb_account" "db" {{
        name                = "tfex-cosmos-db-3242"
        location            = azurerm_resource_group.phil.location
        resource_group_name = azurerm_resource_group.phil.name
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

def multiple():
    return """
Cloud: Azure
Resource: sql, storage
Name Prefix: test
Terraform: 
    provider "azurerm" {{
        subscription_id = "${{var.subscription_id}}"
        client_id       = "${{var.client_id}}"
        client_secret   = "${{var.client_secret}}"
        tenant_id       = "${{var.tenant_id}}"
    }}

    resource "azurerm_resource_group" "test" {{
    name     = "test-resource-group"
    location = "West Europe"
    }}

    resource "azurerm_sql_database" "test_sql" {{
    name                         = "test-sql-database"
    resource_group_name          = azurerm_resource_group.test.name
    server_name                  = azurerm_sql_server.test_sql.name
    edition                      = "Basic"
    collation                    = "SQL_Latin1_General_CP1_CI_AS"
    max_size_bytes               = "1073741824"
    }}

    resource "azurerm_storage_account" "test_storage" {{
    name                = "teststorage"
    resource_group_name = azurerm_resource_group.test.name
    location            = azurerm_resource_group.test.location
    account_tier        = "Standard"
    account_replication = "LRS"
    }}
"""